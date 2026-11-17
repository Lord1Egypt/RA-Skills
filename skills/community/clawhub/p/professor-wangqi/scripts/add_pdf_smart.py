#!/usr/bin/env python3
"""
智能PDF添加脚本 - 使用LLM进行语义级分片和知识提取

与传统的机械式处理不同，此脚本：
1. 使用LLM理解文档语义结构
2. 智能识别标题、作者、摘要、结论等
3. 提取真正有价值的知识点（非模板生成）
4. 生成语义相关的分片用于向量检索

使用方式：
    python scripts/add_pdf_smart.py --pdf path/to/paper.pdf --type paper
    python scripts/add_pdf_smart.py --pdf path/to/experience.pdf --type experience
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from runtime_paths import DEFAULT_OUTPUT_DIR, DEFAULT_PERSIST_DIR, load_runtime_env

# Import confidence system
try:
    from extract_knowledge_cards import ConfidenceCalculator, generate_review_structure
    HAS_CONFIDENCE = True
except ImportError:
    HAS_CONFIDENCE = False
    print("Warning: ConfidenceCalculator not available, cards will not have confidence data")

load_runtime_env()

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package required. Run: pip install openai")
    sys.exit(1)

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def strip_thinking_chain(content: str) -> str:
    """
    Strip thinking chain from Qwen's reasoning_content.
    
    Qwen thinking models output reasoning process before the actual content.
    This function extracts only the final result, not the thinking process.
    
    Patterns to strip:
    - "Here's a thinking process:" followed by numbered steps
    - Content wrapped in thinking tags
    - Reasoning prefixes
    """
    if not content:
        return content
    
    # Common thinking chain markers
    thinking_markers = [
        "Here's a thinking process:",
        "Here is a thinking process:",
        "**Thinking Process:**",
        "**思考过程：**",
        "<thinking>",
    ]
    
    # Check if content starts with thinking markers
    content_lower = content.lower()
    for marker in thinking_markers:
        marker_lower = marker.lower()
        if marker_lower in content_lower:
            # Find where the thinking process ends
            idx = content_lower.find(marker_lower)
            if idx >= 0:
                # Look for the end of thinking process
                # Usually followed by the actual content after a blank line or specific pattern
                after_marker = content[idx + len(marker):]
                
                # Try to find where actual content starts
                # Pattern: numbered list ends, then actual content begins
                lines = after_marker.split('\n')
                actual_content_start = -1
                
                for i, line in enumerate(lines):
                    # Skip empty lines and numbered list items
                    stripped = line.strip()
                    if not stripped:
                        continue
                    # Check if it's a numbered list item (e.g., "1.", "2.", etc.)
                    if re.match(r'^\d+\.', stripped):
                        continue
                    # Check if it's a bullet point
                    if stripped.startswith('-') or stripped.startswith('*'):
                        continue
                    # Check if it's a continuation of thinking
                    if any(kw in stripped.lower() for kw in ['analyze', 'identify', 'consider', 'step', '分析', '识别', '考虑']):
                        continue
                    # This might be the start of actual content
                    actual_content_start = i
                    break
                
                if actual_content_start >= 0:
                    return '\n'.join(lines[actual_content_start:]).strip()
    
    # If no thinking markers found, return as-is
    return content


def get_llm_client() -> Tuple[OpenAI, str]:
    """获取LLM客户端"""
    api_key = os.getenv("API_KEY", "sk-lm-dummy")
    base_url = os.getenv("BASE_URL", "http://localhost:1234/v1")
    model = os.getenv("MODEL_NAME", "qwen/qwen3.6-35b-a3b")
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, model


def extract_pdf_text(pdf_path: str) -> Dict:
    """提取PDF文本"""
    if fitz is None:
        raise ImportError("PyMuPDF required: pip install pymupdf")
    
    doc = fitz.open(pdf_path)
    
    pages = []
    full_text = []
    
    for page_num, page in enumerate(doc, 1):
        text = page.get_text()
        pages.append({"page_num": page_num, "text": text})
        full_text.append(text)
    
    doc.close()
    
    return {
        "full_text": "\n".join(full_text),
        "pages": pages,
        "total_pages": len(pages)
    }


def llm_extract_structure(client: OpenAI, model: str, text: str, source_type: str) -> Dict:
    """使用LLM提取文档结构"""
    
    # 截取前8000字符用于结构识别
    text_sample = text[:8000] if len(text) > 8000 else text
    
    if source_type == "paper":
        prompt = f"""分析以下学术论文文本，提取结构化信息。

文本内容：
{text_sample}

请以JSON格式输出以下信息：
{{
  "title": "论文标题（完整标题，不是文章类型如Review Article）",
  "authors": ["作者1", "作者2"],
  "abstract": "摘要内容",
  "keywords": ["关键词1", "关键词2"],
  "conclusions": "结论部分内容",
  "main_findings": [
    "核心发现1（具体的研究结果，包含数据或结论）",
    "核心发现2",
    "核心发现3"
  ],
  "related_constitutions": ["相关体质类型"],
  "related_diseases": ["相关疾病"],
  "study_type": "研究类型（RCT/队列研究/横断面研究等）"
}}

注意：
1. title必须是真正的论文标题，不是"REVIEW ARTICLE"等文章类型标签
2. authors必须是真实作者名，不是机构名或地址
3. main_findings必须包含具体的研究发现，不要泛泛描述
"""
    else:  # clinical experience
        prompt = f"""分析以下中医诊疗经验文章，提取结构化信息。

文本内容：
{text_sample}

请以JSON格式输出以下信息：
{{
  "title": "文章标题",
  "authors": ["作者"],
  "disease": "主治疾病",
  "syndrome": "辨证分型",
  "constitution": ["相关体质"],
  "treatment_principle": "治则治法",
  "key_formula": "主方",
  "clinical_insights": [
    "临床心得1（具体的诊疗经验或用药心得）",
    "临床心得2"
  ],
  "case_examples": ["典型病例摘要"]
}}

注意：
1. 提取真正有临床价值的经验，不要泛泛描述
2. 包含具体的辨证思路和用药规律
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=4000  # Increased for thinking models
        )
        
        content = response.choices[0].message.content
        
        # Handle thinking models (Qwen with reasoning_content)
        if (not content or not content.strip()) and hasattr(response.choices[0].message, 'reasoning_content'):
            content = response.choices[0].message.reasoning_content
        
        # Strip thinking chain from reasoning_content
        content = strip_thinking_chain(content)
        
        if not content or not content.strip():
            print(f"  LLM returned empty response - model may not be loaded or is busy")
            print(f"  Tip: Check LM Studio server at {client.base_url}")
            return {}
        
        # 尝试解析JSON
        # 处理可能的markdown代码块
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        content = content.strip()
        
        # 检查是否以{开头
        if not content.startswith("{"):
            # 尝试找到第一个{和最后一个}
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1:
                content = content[start:end+1]
            else:
                print(f"  LLM response is not valid JSON: {content[:100]}...")
                return {}
        
        result = json.loads(content)
        return result
        
    except json.JSONDecodeError as e:
        print(f"  LLM JSON parse error: {e}")
        print(f"  Response content: {content[:200] if 'content' in dir() else 'N/A'}...")
        return {}
    except Exception as e:
        print(f"  LLM extraction error: {e}")
        return {}


def llm_extract_knowledge_points(client: OpenAI, model: str, text: str, source_type: str) -> List[Dict]:
    """使用LLM提取知识点（语义级分片）"""
    
    # 使用文本中段（跳过标题和参考文献）
    if len(text) > 10000:
        text_sample = text[2000:8000]
    else:
        text_sample = text[1000:] if len(text) > 1000 else text
    
    if source_type == "paper":
        prompt = f"""从以下学术文本中提取3-5个核心知识点，用于知识库检索。

文本内容：
{text_sample}

请以JSON格式输出知识点列表：
{{
  "knowledge_points": [
    {{
      "content": "具体的研究发现或结论（30-100字，包含具体数据或结论）",
      "category": "finding/method/implication",
      "importance": "high/medium",
      "keywords": ["体质", "痰湿", "肥胖"]
    }}
  ]
}}

要求：
1. 每个知识点必须是具体的研究发现，不要"本文涉及XX相关研究"这种泛泛描述
2. 优先提取有数据支撑的结论，如"P<0.05"、"显著高于"等
3. 知识点应该能独立理解，用于回答用户问题
"""
    else:
        prompt = f"""从以下中医诊疗经验文本中提取3-5个核心知识点。

文本内容：
{text_sample}

请以JSON格式输出：
{{
  "knowledge_points": [
    {{
      "content": "具体的诊疗经验或用药心得（30-100字）",
      "category": "diagnosis/treatment/insight",
      "importance": "high/medium",
      "keywords": ["辨证", "方药", "体质"]
    }}
  ]
}}

要求：
1. 提取真正有临床价值的经验，如"痰湿质肥胖宜用苍术、厚朴"
2. 包含具体的辨证思路、用药规律、配伍特点
"""

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.1,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        
        # Handle thinking models (Qwen with reasoning_content)
        if (not content or not content.strip()) and hasattr(response.choices[0].message, 'reasoning_content'):
            content = response.choices[0].message.reasoning_content
        
        # Strip thinking chain from reasoning_content
        content = strip_thinking_chain(content)
        
        if not content or not content.strip():
            print(f"  LLM returned empty response for knowledge points")
            return []
        
        # For thinking models, try to extract JSON from the content
        # The model might output reasoning before the JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        content = content.strip()
        
        # Try to find JSON object in the content
        if not content.startswith("{"):
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1:
                content = content[start:end+1]
            else:
                print(f"  LLM response is not valid JSON for knowledge points")
                return []
        
        result = json.loads(content)
        return result.get("knowledge_points", [])
        
    except json.JSONDecodeError as e:
        print(f"  LLM JSON parse error for knowledge points: {e}")
        return []
    except Exception as e:
        print(f"  LLM knowledge extraction error: {e}")
        return []


def generate_semantic_chunks(client: OpenAI, model: str, text: str, knowledge_points: List[Dict]) -> List[Dict]:
    """生成语义级分片用于向量检索"""
    
    chunks = []
    
    # 每个知识点作为一个独立分片
    for i, kp in enumerate(knowledge_points):
        chunks.append({
            "chunk_id": f"kp_{i}",
            "content": kp["content"],
            "metadata": {
                "category": kp.get("category", "general"),
                "importance": kp.get("importance", "medium"),
                "keywords": kp.get("keywords", []),
                "chunk_type": "knowledge_point"
            }
        })
    
    # 如果文本较长，额外生成摘要分片
    if len(text) > 5000:
        summary_prompt = f"""请用100-200字概括以下文本的核心内容：

{text[:5000]}

只输出摘要内容，不要其他解释。"""
        
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0.1,
                max_tokens=300,
                messages=[{"role": "user", "content": summary_prompt}]
            )
            
            summary = response.choices[0].message.content
            # Handle thinking models
            if (not summary or not summary.strip()) and hasattr(response.choices[0].message, 'reasoning_content'):
                summary = response.choices[0].message.reasoning_content
            
            # Strip thinking chain from summary
            summary = strip_thinking_chain(summary)
            
            if summary and summary.strip():
                summary = summary.strip()
                # Additional validation: summary should not contain thinking markers
                if not any(marker.lower() in summary.lower() for marker in ["here's a thinking", "here is a thinking", "**thinking process"]):
                    chunks.append({
                        "chunk_id": "summary",
                        "content": summary,
                        "metadata": {
                            "category": "summary",
                            "importance": "high",
                            "chunk_type": "summary"
                        }
                    })
        except:
            pass
    
    return chunks


def extract_year_from_text(text: str) -> Optional[int]:
    """Extract publication year from text"""
    # Look for year patterns in the first 3000 chars
    text_sample = text[:3000]
    
    # Common patterns: (2024), 2024., published 2024, etc.
    patterns = [
        r'\((\d{4})\)',  # (2024)
        r'Published[:\s]+(\d{4})',  # Published 2024
        r'©\s*(\d{4})',  # © 2024
        r'(\d{4})\s*;',  # 2024;
        r',\s*(\d{4})\s*\.',  # , 2024.
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_sample, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            # Validate year range (1990-2030)
            if 1990 <= year <= 2030:
                return year
    
    return None


def validate_card_quality(card: Dict) -> Tuple[bool, List[str]]:
    """
    Validate minimum quality requirements for a knowledge card.
    
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Check title
    title = card.get("title", "")
    if not title or len(title.strip()) < 5:
        issues.append("Title is empty or too short")
    
    # Check authors
    authors = card.get("authors", [])
    if not authors or len(authors) == 0:
        issues.append("Authors list is empty")
    
    # Check knowledge points
    knowledge_points = card.get("knowledge_points", [])
    if not knowledge_points or len(knowledge_points) == 0:
        issues.append("Knowledge points are empty")
    
    # Check semantic chunks
    chunks = card.get("semantic_chunks", [])
    if not chunks or len(chunks) == 0:
        issues.append("Semantic chunks are empty")
    
    return len(issues) == 0, issues


def build_knowledge_card(
    pdf_path: str,
    source_type: str,
    structure: Dict,
    knowledge_points: List[Dict],
    chunks: List[Dict],
    pdf_content: Dict
) -> Dict:
    """构建知识卡"""
    
    # 生成card_id
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    card_id = f"WQ-{'SCI' if source_type == 'paper' else 'EXP'}-{timestamp}"
    
    # Extract year from text
    year = extract_year_from_text(pdf_content.get("full_text", ""))
    if not year:
        year = datetime.now().year  # Fallback to current year
    
    # Generate confidence metadata for LLM-extracted fields
    field_meta = {}
    if HAS_CONFIDENCE:
        calc = ConfidenceCalculator()
        
        # For LLM-extracted fields, use fixed confidence
        llm_confidence = ConfidenceCalculator.LLM_CONFIDENCE
        
        title = structure.get("title", "")
        authors = structure.get("authors", [])
        journal = structure.get("journal", "")
        abstract = structure.get("abstract", "")
        conclusions = structure.get("conclusions", "")
        keywords = structure.get("keywords", [])
        doi = structure.get("doi", "")
        
        field_meta = {
            "title": {
                "confidence": llm_confidence if title else 0.0,
                "source": "llm_extract" if title else "none",
                "level": "high" if title else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            },
            "authors": {
                "confidence": llm_confidence if authors else 0.0,
                "source": "llm_extract" if authors else "none",
                "level": "high" if authors else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            },
            "year": {
                "confidence": 0.75 if year else 0.0,
                "source": "text_pattern" if year else "none",
                "level": "medium" if year else "none",
                "reasoning": "Extracted from text using pattern matching"
            },
            "journal": {
                "confidence": llm_confidence if journal else 0.0,
                "source": "llm_extract" if journal else "none",
                "level": "high" if journal else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            },
            "abstract": {
                "confidence": llm_confidence if abstract else 0.0,
                "source": "llm_extract" if abstract else "none",
                "level": "high" if abstract else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            },
            "conclusions": {
                "confidence": llm_confidence if conclusions else 0.0,
                "source": "llm_extract" if conclusions else "none",
                "level": "high" if conclusions else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            },
            "keywords": {
                "confidence": llm_confidence if keywords else 0.0,
                "source": "llm_extract" if keywords else "none",
                "level": "high" if keywords else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            },
            "doi": {
                "confidence": llm_confidence if doi else 0.0,
                "source": "llm_extract" if doi else "none",
                "level": "high" if doi else "none",
                "reasoning": "Extracted by LLM semantic analysis"
            }
        }
    
    # Generate _review structure
    review = {}
    if HAS_CONFIDENCE and field_meta:
        review = generate_review_structure(field_meta)
    
    if source_type == "paper":
        card = {
            "card_id": card_id,
            "source_type": "paper",
            "source_file": Path(pdf_path).name,
            "title": structure.get("title", ""),
            "authors": structure.get("authors", []),
            "year": year,
            "language": "en" if re.match(r'[A-Za-z]', structure.get("title", "")) else "zh",
            "abstract": structure.get("abstract", ""),
            "keywords": structure.get("keywords", []),
            "conclusions": structure.get("conclusions", ""),
            "knowledge_points": knowledge_points,
            "related_constitutions": structure.get("related_constitutions", []),
            "related_diseases": structure.get("related_diseases", []),
            "study_type": structure.get("study_type", ""),
            "evidence_sentences": [
                {"sentence": kp["content"], "section": "llm_extracted", "claim_type": kp.get("category", "finding")}
                for kp in knowledge_points
            ],
            "semantic_chunks": chunks,
            "page_info": {
                "total_pages": pdf_content.get("total_pages", 0),
                "sections": {}
            },
            "extraction_method": "llm_semantic",
            "created_at": datetime.now().isoformat()
        }
    else:
        card = {
            "card_id": card_id,
            "source_type": "clinical_experience",
            "source_file": Path(pdf_path).name,
            "title": structure.get("title", ""),
            "authors": structure.get("authors", []),
            "year": year,
            "language": "zh",
            "disease": structure.get("disease", ""),
            "syndrome": structure.get("syndrome", ""),
            "constitution": structure.get("constitution", []),
            "treatment_principle": structure.get("treatment_principle", ""),
            "key_formula": structure.get("key_formula", ""),
            "clinical_insights": structure.get("clinical_insights", []),
            "knowledge_points": knowledge_points,
            "related_constitutions": structure.get("constitution", []),
            "related_diseases": [structure.get("disease", "")] if structure.get("disease") else [],
            "evidence_sentences": [
                {"sentence": kp["content"], "section": "llm_extracted", "claim_type": kp.get("category", "insight")}
                for kp in knowledge_points
            ],
            "semantic_chunks": chunks,
            "page_info": {
                "total_pages": pdf_content.get("total_pages", 0),
                "sections": {}
            },
            "extraction_method": "llm_semantic",
            "created_at": datetime.now().isoformat()
        }
    
    # Add confidence metadata
    if field_meta:
        card["_field_meta"] = field_meta
    if review:
        card["_review"] = review
    
    return card


def add_to_vector_index(card: Dict, collection_name: str = "wangqi_knowledge", persist_dir: Optional[str] = None) -> bool:
    """将知识卡添加到向量索引（使用与build_local_index.py相同的embedding方式）"""
    try:
        import chromadb
        from openai import OpenAI
        
        # Use provided persist_dir or default
        if persist_dir is None:
            persist_dir = DEFAULT_PERSIST_DIR
        
        chroma_path = Path(persist_dir)
        client = chromadb.PersistentClient(path=str(chroma_path))
        
        collection = client.get_or_create_collection(name=collection_name)
        
        # 添加语义分片到索引
        chunks = card.get("semantic_chunks", [])
        
        if not chunks:
            # 如果没有分片，用知识点作为分片
            for kp in card.get("knowledge_points", []):
                chunks.append({
                    "chunk_id": f"kp_{len(chunks)}",
                    "content": kp.get("content", ""),
                    "metadata": {"category": kp.get("category", "general")}
                })
        
        # 使用与build_local_index.py相同的embedding函数
        # 避免向量空间不兼容
        embedding_api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        embedding_base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        
        embedding_client = OpenAI(api_key=embedding_api_key, base_url=embedding_base_url)
        
        # 准备批量数据
        chunk_ids = []
        chunk_docs = []
        chunk_metas = []
        
        for chunk in chunks:
            if not chunk.get("content"):
                continue
            
            chunk_id = f"{card['card_id']}_{chunk['chunk_id']}"
            
            # 构建元数据
            metadata = {
                "card_id": card["card_id"],
                "source_type": card["source_type"],
                "title": card.get("title", "")[:200],  # 限制长度
                "chunk_type": chunk.get("metadata", {}).get("chunk_type", "knowledge_point"),
            }
            # 添加chunk metadata，但需要转换list为string（ChromaDB不支持list）
            chunk_meta = chunk.get("metadata", {})
            for key, value in chunk_meta.items():
                if isinstance(value, list):
                    # 将list转换为逗号分隔的字符串
                    metadata[key] = ", ".join(str(v) for v in value) if value else ""
                elif isinstance(value, (str, int, float, bool)):
                    metadata[key] = value
                # 忽略其他类型
            
            chunk_ids.append(chunk_id)
            chunk_docs.append(chunk["content"])
            chunk_metas.append(metadata)
        
        if not chunk_docs:
            print("  No valid chunks to add")
            return False
        
        # 手动生成embeddings（与build_local_index.py保持一致）
        try:
            response = embedding_client.embeddings.create(
                model=embedding_model,
                input=chunk_docs
            )
            # 安全提取embeddings
            chunk_embeddings = []
            for item in response.data:
                if hasattr(item, 'embedding'):
                    chunk_embeddings.append(item.embedding)
                elif isinstance(item, dict) and 'embedding' in item:
                    chunk_embeddings.append(item['embedding'])
                else:
                    print(f"  Warning: Unexpected embedding format: {type(item)}")
                    return False
            
            if len(chunk_embeddings) != len(chunk_docs):
                print(f"  Embedding count mismatch: {len(chunk_embeddings)} vs {len(chunk_docs)}")
                return False
                
        except Exception as e:
            print(f"  Embedding error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 添加到集合（显式传入embeddings）
        try:
            collection.add(
                ids=chunk_ids,
                documents=chunk_docs,
                embeddings=chunk_embeddings,
                metadatas=chunk_metas
            )
        except Exception as e:
            print(f"  Collection add error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print(f"  Added {len(chunks)} chunks to vector index")
        return True
        
    except Exception as e:
        print(f"  Vector index error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="智能添加PDF到知识库")
    parser.add_argument("--pdf", required=True, help="PDF文件路径")
    parser.add_argument("--type", choices=["paper", "experience"], default="paper", help="文档类型")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR, help="向量数据库目录")
    parser.add_argument("--no-index", action="store_true", help="不添加到向量索引")
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print(f"智能PDF添加 - {args.type}")
    print(f"{'='*50}")
    print(f"PDF: {pdf_path.name}")
    
    # 1. 提取PDF文本
    print("\n[1/4] 提取PDF文本...")
    pdf_content = extract_pdf_text(str(pdf_path))
    print(f"  提取了 {pdf_content['total_pages']} 页，{len(pdf_content['full_text'])} 字符")
    
    # 2. LLM提取结构
    print("\n[2/4] LLM提取文档结构...")
    client, model = get_llm_client()
    structure = llm_extract_structure(client, model, pdf_content["full_text"], args.type)
    print(f"  标题: {structure.get('title', 'N/A')}")
    print(f"  作者: {structure.get('authors', [])}")
    
    # 3. LLM提取知识点
    print("\n[3/4] LLM提取知识点...")
    knowledge_points = llm_extract_knowledge_points(client, model, pdf_content["full_text"], args.type)
    print(f"  提取了 {len(knowledge_points)} 个知识点")
    for i, kp in enumerate(knowledge_points[:3], 1):
        print(f"    {i}. {kp.get('content', '')[:50]}...")
    
    # 4. 生成语义分片
    print("\n[4/4] 生成语义分片...")
    chunks = generate_semantic_chunks(client, model, pdf_content["full_text"], knowledge_points)
    print(f"  生成了 {len(chunks)} 个检索分片")
    
    # 5. 构建知识卡
    card = build_knowledge_card(
        str(pdf_path), args.type, structure, knowledge_points, chunks, pdf_content
    )
    
    # 6. 质量检查
    is_valid, issues = validate_card_quality(card)
    if not is_valid:
        print("\n[ERROR] 知识卡质量检查未通过:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n知识卡未保存。请检查LLM是否正确加载。")
        sys.exit(1)
    
    # 7. 保存知识卡
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / "data" / "cards" / ("papers" if args.type == "paper" else "experiences")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{card['card_id']}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)
    
    print(f"\n知识卡已保存: {output_file}")
    
    # 8. 添加到向量索引
    if not args.no_index:
        print("\n添加到向量索引...")
        if add_to_vector_index(card, persist_dir=args.persist_dir):
            print("  [OK] 已添加到向量索引")
        else:
            print("  [FAIL] 添加到向量索引失败")
    
    print(f"\n{'='*50}")
    print("完成！")
    print(f"{'='*50}")
    
    return card


if __name__ == "__main__":
    main()
