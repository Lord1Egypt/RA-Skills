import os
import re
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Knowledge Base Root
KB_ROOT = Path(os.path.expanduser("~/.openclaw/workspace/knowledge-base"))
INDEX_FILE = KB_ROOT / ".index.json"
DEFAULT_CATEGORIES = [
    "学术论文",
    "技术文档",
    "工作资料",
    "读书笔记",
    "项目文档",
    "参考资料",
    "未分类"
]


def ensure_kb_exists():
    """确保知识库目录结构存在"""
    KB_ROOT.mkdir(parents=True, exist_ok=True)
    for cat in DEFAULT_CATEGORIES:
        (KB_ROOT / cat).mkdir(exist_ok=True)
    if not INDEX_FILE.exists():
        save_index({"version": "1.0", "documents": [], "categories": DEFAULT_CATEGORIES.copy()})


def load_index() -> Dict[str, Any]:
    """加载索引文件"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "documents": [], "categories": DEFAULT_CATEGORIES.copy()}


def save_index(index: Dict[str, Any]):
    """保存索引文件"""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def generate_doc_id(filepath: str) -> str:
    """根据文件路径和内容哈希生成文档ID"""
    hasher = hashlib.sha256()
    hasher.update(filepath.encode("utf-8"))
    if os.path.exists(filepath):
        stat = os.stat(filepath)
        hasher.update(str(stat.st_size).encode())
        hasher.update(str(stat.st_mtime).encode())
    return hasher.hexdigest()[:16]


def convert_file_to_markdown(source_path: str) -> tuple[bool, str, str]:
    """
    使用markitdown将文件转换为markdown
    返回: (success, markdown_content, title)
    """
    try:
        # 优先使用Python API
        from markitdown import MarkItDown
        md = MarkItDown(enable_plugins=False)
        result = md.convert(source_path)
        title = result.title or Path(source_path).stem
        return True, result.markdown, title
    except ImportError:
        # 降级到CLI
        try:
            result = subprocess.run(
                ["markitdown", source_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return True, result.stdout, Path(source_path).stem
            else:
                return False, result.stderr, ""
        except Exception as e:
            return False, str(e), ""
    except Exception as e:
        return False, str(e), ""


def guess_category(title: str, content: str, categories: List[str]) -> str:
    """根据标题和内容猜测分类（简单关键词匹配）"""
    text = (title + " " + content[:2000]).lower()
    
    keywords_map = {
        "学术论文": ["论文", "研究", "journal", "conference", "abstract", "methodology", "literature", "综述", "引言", "结论", "参考文献"],
        "技术文档": ["api", "sdk", "文档", "documentation", "guide", "tutorial", "reference", "manual", "spec", "配置", "部署", "代码", "算法", "神经网络", "机器学习", "深度学习", "编程"],
        "工作资料": ["报告", "汇报", "总结", "proposal", "预算", "schedule", "plan", "review", "meeting", "会议纪要", "周报", "月报"],
        "读书笔记": ["读书", "笔记", "读后感", "review", "book", "chapter", "作者", "出版社", "小说", "散文"],
        "项目文档": ["project", "项目", "prd", "需求", "design", "架构", "roadmap", "milestone", "产品", "迭代", "版本"],
        "参考资料": ["reference", "资料", "素材", "collection", "list", "index", "catalog", "工具", "链接", "资源"]
    }
    
    scores = {}
    for cat, kws in keywords_map.items():
        if cat not in categories:
            continue
        score = sum(1 for kw in kws if kw.lower() in text)
        if score > 0:
            scores[cat] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "未分类"


def extract_keywords(content: str, max_keywords: int = 10) -> List[str]:
    """从内容中提取关键词（优先用jieba分词，否则用正则启发式）"""
    # 尝试用jieba做中文分词
    try:
        import jieba
        import jieba.analyse
        # 使用TF-IDF提取关键词
        jieba_keywords = jieba.analyse.extract_tags(content, topK=max_keywords * 2, withWeight=False)
        jieba_keywords = [k for k in jieba_keywords if len(k) >= 2]
        if len(jieba_keywords) >= max_keywords // 2:
            # jieba工作正常，补充英文单词
            english_words = re.findall(r"[a-zA-Z]{3,20}", content.lower())
            from collections import Counter
            eng_freq = Counter([w for w in english_words if w not in {
                "this", "that", "with", "from", "they", "have", "will", "would",
                "there", "their", "what", "about", "which", "when", "make", "like",
                "time", "just", "know", "take", "year", "good", "some", "come",
                "could", "state", "over", "think", "also", "after", "back", "than"
            }])
            top_eng = [w for w, _ in eng_freq.most_common(max_keywords)]
            # 合并中英文，去重
            seen = set()
            keywords = []
            for w in jieba_keywords + top_eng:
                if w not in seen and len(keywords) < max_keywords:
                    seen.add(w)
                    keywords.append(w)
            return keywords[:max_keywords]
    except ImportError:
        pass
    
    # 降级方案：改进的正则启发式
    english_words = re.findall(r"[a-zA-Z]{3,20}", content.lower())
    
    # 中文提取：尝试提取4-8字的片段（更接近中文词的长度）
    # 同时提取2-3字但进行停用词过滤
    long_phrases = re.findall(r"[\u4e00-\u9fa5]{4,8}", content)
    short_phrases = re.findall(r"[\u4e00-\u9fa5]{2,3}", content)
    
    stopwords = set([
        "this", "that", "with", "from", "they", "have", "will", "would",
        "there", "their", "what", "about", "which", "when", "make", "like",
        "time", "just", "know", "take", "year", "good", "some", "come",
        "could", "state", "over", "think", "also", "after", "back", "than",
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
        "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
        "你", "会", "着", "没有", "看", "好", "自己", "这", "那",
        "我们", "可以", "但是", "因为", "所以", "如果", "需要", "进行",
        "表示", "使用", "通过", "方法", "结果", "分析", "数据", "系统",
        "本文", "研究", "提出", "基于", "针对", "以及", "及其", "之中",
        "所示", "如下", "以上", "其中", "因此", "然而", "而且", "或者"
    ])
    
    from collections import Counter
    
    # 优先用长词组，更可能是专业术语
    all_words = [w for w in long_phrases if w not in stopwords]
    # 补充短词组
    all_words += [w for w in short_phrases if w not in stopwords]
    all_words += [w for w in english_words if w not in stopwords]
    
    freq = Counter(all_words)
    top = freq.most_common(max_keywords * 3)
    
    # 去重和过滤：避免包含关系，保留更长的
    seen = set()
    keywords = []
    for word, count in top:
        if len(keywords) >= max_keywords:
            break
        # 检查是否与已有词有包含关系
        skip = False
        for seen_word in list(seen):
            if word != seen_word and (word in seen_word or seen_word in word):
                # 保留更长的
                longer = word if len(word) > len(seen_word) else seen_word
                shorter = seen_word if len(word) > len(seen_word) else word
                if shorter in keywords:
                    keywords[keywords.index(shorter)] = longer
                seen.discard(shorter)
                seen.add(longer)
                skip = True
                break
        if not skip and word not in seen:
            seen.add(word)
            keywords.append(word)
    
    return keywords[:max_keywords]


def generate_summary(content: str, max_length: int = 300) -> str:
    """生成内容摘要（取前N个字符，尝试在句子边界截断）"""
    # 去除markdown标记，保留纯文本
    text = re.sub(r"[#*`\-\[\]\(\)|>=_]", "", content)
    text = re.sub(r"\s+", " ", text).strip()
    
    if len(text) <= max_length:
        return text
    
    # 尝试在句子边界截断
    truncated = text[:max_length]
    # 找最后一个句号、问号或换行
    for delim in [".", "。", "!", "！", "?", "？", "\n"]:
        last = truncated.rfind(delim)
        if last > max_length * 0.5:
            return truncated[:last+1]
    
    return truncated + "..."


def ingest_file(source_path: str, suggested_category: Optional[str] = None) -> Dict[str, Any]:
    """
    接收文件，转换，分类，索引
    返回文档元数据
    """
    ensure_kb_exists()
    index = load_index()
    
    source_path = os.path.abspath(source_path)
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"文件不存在: {source_path}")
    
    doc_id = generate_doc_id(source_path)
    
    # 检查是否已存在
    for doc in index["documents"]:
        if doc["id"] == doc_id:
            return doc  # 已存在，直接返回
    
    # 转换文件
    success, md_content, title = convert_file_to_markdown(source_path)
    if not success:
        raise RuntimeError(f"文件转换失败: {md_content}")
    
    # 分类
    categories = index.get("categories", DEFAULT_CATEGORIES)
    category = suggested_category or guess_category(title, md_content, categories)
    
    # 确保分类目录存在
    cat_dir = KB_ROOT / category
    cat_dir.mkdir(exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r'[^\w\u4e00-\u9fa5\-]', '_', title)[:50]
    md_filename = f"{timestamp}_{safe_title}.md"
    md_path = cat_dir / md_filename
    
    # 写入markdown文件（添加元数据头部）
    header = f"""---
title: {title}
source: {os.path.basename(source_path)}
category: {category}
ingested_at: {datetime.now().isoformat()}
doc_id: {doc_id}
---

"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(header + md_content)
    
    # 提取关键词和摘要
    keywords = extract_keywords(md_content)
    summary = generate_summary(md_content)
    
    # 创建索引记录
    doc_record = {
        "id": doc_id,
        "title": title,
        "original_name": os.path.basename(source_path),
        "original_path": source_path,
        "category": category,
        "md_path": str(md_path.relative_to(KB_ROOT)),
        "keywords": keywords,
        "summary": summary,
        "ingested_at": datetime.now().isoformat(),
        "word_count": len(md_content.split()),
        "char_count": len(md_content)
    }
    
    index["documents"].append(doc_record)
    save_index(index)
    
    return doc_record


def search_kb(query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    在知识库中搜索
    支持关键词匹配标题、关键词、摘要、内容
    """
    ensure_kb_exists()
    index = load_index()
    query_lower = query.lower()
    
    results = []
    for doc in index["documents"]:
        # 类别过滤
        if category and doc["category"] != category:
            continue
        
        score = 0
        # 标题匹配（权重最高）
        if query_lower in doc["title"].lower():
            score += 10
        # 关键词匹配
        for kw in doc["keywords"]:
            if query_lower in kw.lower():
                score += 5
        # 摘要匹配
        if query_lower in doc.get("summary", "").lower():
            score += 3
        # 文件名匹配
        if query_lower in doc["original_name"].lower():
            score += 2
        
        # 尝试搜索文件内容
        if score == 0:
            md_path = KB_ROOT / doc["md_path"]
            if md_path.exists():
                try:
                    with open(md_path, "r", encoding="utf-8") as f:
                        content = f.read().lower()
                        if query_lower in content:
                            # 找到匹配片段
                            idx = content.find(query_lower)
                            snippet = content[max(0, idx-100):idx+200]
                            score += 1
                            doc["_snippet"] = snippet
                except:
                    pass
        
        if score > 0:
            doc["_score"] = score
            results.append(doc)
    
    # 按分数排序
    results.sort(key=lambda x: x["_score"], reverse=True)
    return results[:limit]


def list_documents(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """列出知识库中的文档"""
    ensure_kb_exists()
    index = load_index()
    docs = index["documents"]
    if category:
        docs = [d for d in docs if d["category"] == category]
    return docs


def get_document(doc_id: str) -> Optional[Dict[str, Any]]:
    """获取单个文档的详细信息和内容"""
    ensure_kb_exists()
    index = load_index()
    for doc in index["documents"]:
        if doc["id"] == doc_id:
            md_path = KB_ROOT / doc["md_path"]
            if md_path.exists():
                with open(md_path, "r", encoding="utf-8") as f:
                    doc["_content"] = f.read()
            return doc
    return None


def delete_document(doc_id: str) -> bool:
    """删除文档"""
    ensure_kb_exists()
    index = load_index()
    for i, doc in enumerate(index["documents"]):
        if doc["id"] == doc_id:
            # 删除文件
            md_path = KB_ROOT / doc["md_path"]
            if md_path.exists():
                md_path.unlink()
            # 从索引中移除
            index["documents"].pop(i)
            save_index(index)
            return True
    return False


def add_category(name: str) -> bool:
    """添加新分类"""
    ensure_kb_exists()
    index = load_index()
    if name not in index["categories"]:
        index["categories"].append(name)
        (KB_ROOT / name).mkdir(exist_ok=True)
        save_index(index)
        return True
    return False


def get_stats() -> Dict[str, Any]:
    """获取知识库统计信息"""
    ensure_kb_exists()
    index = load_index()
    docs = index["documents"]
    
    cat_counts = {}
    for doc in docs:
        cat = doc["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    
    total_words = sum(d.get("word_count", 0) for d in docs)
    total_chars = sum(d.get("char_count", 0) for d in docs)
    
    return {
        "total_documents": len(docs),
        "total_categories": len(index["categories"]),
        "category_distribution": cat_counts,
        "total_words": total_words,
        "total_chars": total_chars
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Knowledge Base Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    # ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a file")
    ingest_parser.add_argument("filepath", help="Path to the file")
    ingest_parser.add_argument("--category", "-c", help="Suggested category")
    
    # search
    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--category", "-c", help="Filter by category")
    search_parser.add_argument("--limit", "-l", type=int, default=10)
    
    # list
    list_parser = subparsers.add_parser("list", help="List documents")
    list_parser.add_argument("--category", "-c", help="Filter by category")
    
    # stats
    subparsers.add_parser("stats", help="Show statistics")
    
    # get
    get_parser = subparsers.add_parser("get", help="Get document details")
    get_parser.add_argument("doc_id", help="Document ID")
    
    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a document")
    delete_parser.add_argument("doc_id", help="Document ID")
    
    # add-category
    addcat_parser = subparsers.add_parser("add-category", help="Add a category")
    addcat_parser.add_argument("name", help="Category name")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        try:
            result = ingest_file(args.filepath, args.category)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "search":
        results = search_kb(args.query, args.category, args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "list":
        docs = list_documents(args.category)
        print(json.dumps(docs, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        stats = get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "get":
        doc = get_document(args.doc_id)
        if doc:
            print(json.dumps(doc, ensure_ascii=False, indent=2))
        else:
            print("Document not found", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "delete":
        if delete_document(args.doc_id):
            print("Deleted successfully")
        else:
            print("Document not found", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "add-category":
        if add_category(args.name):
            print(f"Category '{args.name}' added")
        else:
            print(f"Category '{args.name}' already exists")
    
    else:
        parser.print_help()
