#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库核心模块
提供文档解析、索引构建、语义检索功能
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from .config import load_config, resolve_index_path


class DocumentParser:
    """Markdown文档解析器"""

    FRONTMATTER_PATTERN = re.compile(
        r'^---\s*\n(.*?)\n---\s*\n(.*)$',
        re.DOTALL | re.MULTILINE
    )

    @classmethod
    def parse_file(cls, file_path: Path) -> Optional[Dict]:
        """解析单个Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata = cls._extract_metadata(content, file_path)
            blocks = cls._split_into_blocks(content)

            return {
                'path': str(file_path.absolute()),
                'relative_path': str(file_path),
                'filename': file_path.name,
                **metadata,
                'blocks': blocks,
                'content_hash': cls._compute_hash(content),
                'parsed_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"解析文件失败 {file_path}: {e}")
            return None

    @classmethod
    def _extract_metadata(cls, content: str, file_path: Path) -> Dict:
        """提取文档元数据"""
        metadata = {
            'title': cls._extract_title(content),
            'keywords': cls._extract_keywords(content),
            'tags': cls._extract_tags(content, file_path),
            'summary': cls._extract_summary(content),
            'word_count': len(content),
            'modified': datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat()
        }
        return metadata

    @classmethod
    def _extract_title(cls, content: str) -> str:
        """提取文档标题"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        fm_match = re.search(r'title:\s*(.+?)\n', content)
        if fm_match:
            return fm_match.group(1).strip().strip('"\'')

        return ""

    @classmethod
    def _extract_keywords(cls, content: str) -> List[str]:
        """提取关键词"""
        keywords = []

        for pattern in [
            r'keywords?:\s*\[(.*?)\]',
            r'keywords?:\s*\n((?:\s*-\s*.+\n)+)',
            r'keywords?:\s*(.+?)(?:\n|$)',
        ]:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                kw_str = match.group(1)
                if '[' in kw_str:
                    keywords = re.findall(r'["\']?([^"\'\[\],]+)["\']?', kw_str)
                elif '-' in kw_str:
                    keywords = re.findall(r'-\s*(.+)', kw_str)
                else:
                    keywords = [k.strip() for k in kw_str.split(',')]
                break

        return [k.strip() for k in keywords if k.strip()]

    @classmethod
    def _extract_tags(cls, content: str, file_path: Path) -> List[str]:
        """提取标签"""
        tags = []

        for pattern in [
            r'tags?:\s*\[(.*?)\]',
            r'tags?:\s*\n((?:\s*-\s*.+\n)+)',
        ]:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                tag_str = match.group(1)
                if '[' in tag_str:
                    tags = re.findall(r'["\']?([^"\'\[\],]+)["\']?', tag_str)
                else:
                    tags = re.findall(r'-\s*(.+)', tag_str)
                break

        filename_words = re.findall(
            r'[\u4e00-\u9fff]+|[a-zA-Z]+',
            file_path.stem
        )
        tags.extend([w for w in filename_words if len(w) > 2][:3])

        return list(set([t.strip() for t in tags if t.strip()]))

    @classmethod
    def _extract_summary(cls, content: str) -> str:
        """提取文档摘要"""
        content = re.sub(cls.FRONTMATTER_PATTERN, '', content)
        clean = re.sub(r'[#*`\[\]()>_~\-]|!\[\w+\]', '', content)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
        clean = re.sub(r'\n{2,}', ' ', clean)
        clean = clean.strip()

        return clean[:300].strip()

    @classmethod
    def _split_into_blocks(cls, content: str) -> List[Dict]:
        """将文档分割成可检索的块"""
        blocks = []

        content = re.sub(cls.FRONTMATTER_PATTERN, '', content)
        sections = re.split(r'\n(?=##\s+)', content)

        for idx, section in enumerate(sections):
            if not section.strip():
                continue

            title_match = re.search(r'^(#{1,3})\s+(.+)$', section, re.MULTILINE)
            block_title = title_match.group(2).strip() if title_match else f"段落 {idx + 1}"

            clean = re.sub(r'[#*`\[\]()>_~\-]|!\[\w+\]', '', section)
            clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
            clean = re.sub(r'\n{2,}', '\n', clean)
            clean = clean.strip()

            if len(clean) > 30:
                blocks.append({
                    'id': f"{idx}",
                    'title': block_title,
                    'content': clean[:1500],
                    'char_count': len(clean)
                })

        return blocks if blocks else [{'id': '0', 'title': '全文', 'content': content[:1500], 'char_count': len(content)}]

    @classmethod
    def _compute_hash(cls, content: str) -> str:
        """计算内容哈希"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()


class IndexBuilder:
    """知识库索引构建器"""

    def __init__(self, config: Dict = None):
        if config is None:
            config = load_config()
        self.config = config
        self.knowledge_path = Path(config.get('knowledge_path', '~/Knowledge')).expanduser()
        self.index_path = resolve_index_path(config)
        self.exclude_patterns = config.get('exclude_patterns', ['.markdown', '.trash', '@Recycle'])

    def scan_documents(self) -> List[Dict]:
        """扫描知识库目录"""
        import subprocess
        documents = []
        
        try:
            # 用 ripgrep 获取所有 md 文件
            result = subprocess.run(
                ['rg', '--files', str(self.knowledge_path)],
                capture_output=True, text=True, check=True
            )
            file_paths = [Path(p.strip()) for p in result.stdout.strip().split('\n') if p.strip()]
        except (subprocess.CalledProcessError, FileNotFoundError):
            # fallback：ripgrep 不可用时用原方案
            file_paths = self.knowledge_path.rglob("*.md")
        
        for md_file in file_paths:
            if any(pattern in md_file.parts for pattern in self.exclude_patterns):
                continue

            if any(part.startswith('.') for part in md_file.parts):
                continue

            doc = DocumentParser.parse_file(md_file)
            if doc:
                documents.append(doc)

        return documents

    def build_index(self) -> Dict:
        """构建完整索引"""
        documents = self.scan_documents()

        index_data = {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'knowledge_path': str(self.knowledge_path),
            'total_documents': len(documents),
            'total_blocks': sum(len(doc.get('blocks', [])) for doc in documents),
            'documents': documents
        }

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

        return index_data

    def incremental_update(self, existing_index: Dict) -> Dict:
        """增量更新索引"""
        documents = self.scan_documents()
        existing_hashes = {doc['path']: doc['content_hash'] for doc in existing_index.get('documents', [])}

        updated_docs = []
        new_count = 0
        modified_count = 0

        for doc in documents:
            old_hash = existing_hashes.get(doc['path'])
            if old_hash is None:
                new_count += 1
                updated_docs.append(doc)
            elif old_hash != doc['content_hash']:
                modified_count += 1
                updated_docs.append(doc)
            else:
                updated_docs.append(doc)

        index_data = {
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'knowledge_path': str(self.knowledge_path),
            'total_documents': len(updated_docs),
            'total_blocks': sum(len(doc.get('blocks', [])) for doc in updated_docs),
            'documents': updated_docs,
            'update_stats': {
                'new': new_count,
                'modified': modified_count,
                'unchanged': len(updated_docs) - new_count - modified_count
            }
        }

        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

        return index_data


class KnowledgeSearcher:
    """知识库检索器"""

    def __init__(self, config: Dict = None):
        if config is None:
            config = load_config()
        self.config = config
        self.index_path = resolve_index_path(config)
        self.top_k = config.get('search_top_k', 3)
        self.index_data = self._load_index()

    def _load_index(self) -> Dict:
        """加载索引"""
        if not self.index_path.exists():
            return {'documents': []}

        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {'documents': []}

    def search(self, query: str, top_k: Optional[int] = None) -> List[Dict]:
        """搜索相关文档"""
        results = []
        query_lower = query.lower()
        query_words = self._tokenize(query_lower)
        k = top_k or self.top_k

        for doc in self.get('documents', []):
            score = self._calculate_score(query_lower, query_words, doc)
            if score > 0:
                results.append({
                    'document': doc,
                    'score': score,
                    'matched_blocks': self._get_matched_blocks(query_lower, query_words, doc)
                })

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]

    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        tokens = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text.lower())
        words = tokens.copy()
        for i in range(len(tokens) - 1):
            if len(tokens[i]) > 2 and len(tokens[i + 1]) > 2:
                words.append(tokens[i] + tokens[i + 1])
        return words

    def _calculate_score(self, query: str, query_words: List[str], doc: Dict) -> float:
        """计算相关性分数"""
        score = 0.0

        title = doc.get('title', '').lower()
        for word in query_words:
            if word in title:
                score += 10
                if word == query:
                    score += 5

        for keyword in doc.get('keywords', []):
            kw_lower = keyword.lower()
            for word in query_words:
                if word in kw_lower or kw_lower in word:
                    score += 5

        for tag in doc.get('tags', []):
            tag_lower = tag.lower()
            for word in query_words:
                if word in tag_lower or tag_lower in word:
                    score += 3

        for block in doc.get('blocks', []):
            block_text = block.get('content', '').lower()
            for word in query_words:
                if word in block_text:
                    score += 1

        summary = doc.get('summary', '').lower()
        for word in query_words:
            if word in summary:
                score += 2

        return score

    def _get_matched_blocks(self, query: str, query_words: List[str], doc: Dict) -> List[Dict]:
        """获取匹配的内容块"""
        matched = []

        for block in doc.get('blocks', []):
            block_text = block.get('content', '').lower()

            has_match = any(word in block_text for word in query_words)

            if has_match:
                sentences = re.split(r'[。！？\n]', block_text)
                relevant_sentences = []

                for sentence in sentences:
                    if any(word in sentence for word in query_words):
                        relevant_sentences.append(sentence.strip())

                if relevant_sentences:
                    matched.append({
                        'title': block.get('title', ''),
                        'preview': '。'.join(relevant_sentences[:2])[:300],
                        'score': sum(1 for word in query_words if any(word in s for s in relevant_sentences))
                    })

        matched.sort(key=lambda x: x['score'], reverse=True)
        return matched[:3]

    def format_results(self, results: List[Dict], query: str) -> str:
        """格式化搜索结果"""
        if not results:
            return "未在知识库中找到相关信息。"

        output = ["【知识库检索结果】\n"]

        for i, result in enumerate(results, 1):
            doc = result['document']
            matched_blocks = result['matched_blocks']

            output.append(f"## {i}. {doc.get('title', '无标题')}")
            output.append(f"**相关度：** {'★' * min(int(result['score'] / 5), 5)}")
            output.append(f"**来源：** `{doc.get('relative_path', doc.get('path', ''))}`")
            output.append(f"**摘要：** {doc.get('summary', '')[:150]}...")
            output.append("")

            if matched_blocks:
                output.append("**相关内容：**")
                for block in matched_blocks[:2]:
                    output.append(f"- *{block['title']}*：{block['preview']}...")
                output.append("")

            output.append("---")
            output.append("")

        return "\n".join(output)

    def get(self, key: str, default=None):
        """安全获取索引数据"""
        return self.index_data.get(key, default)

    def get_stats(self) -> Dict:
        """获取统计信息"""
        docs = self.index_data.get('documents', [])

        by_folder = {}
        for doc in docs:
            folder = str(Path(doc.get('relative_path', '')).parent)
            by_folder[folder] = by_folder.get(folder, 0) + 1

        return {
            'total_documents': len(docs),
            'total_blocks': sum(len(doc.get('blocks', [])) for doc in docs),
            'documents_by_folder': by_folder,
            'index_path': str(self.index_path),
            'last_updated': self.index_data.get('created_at', '')
        }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='知识库工具')
    parser.add_argument('command', choices=['build', 'search', 'stats'],
                        help='命令：build构建索引，search搜索，stats统计')
    parser.add_argument('--config', default='~/.openclaw/skills/markdown-knowledge/config.json',
                        help='配置文件路径')
    parser.add_argument('--query', help='搜索查询词')
    parser.add_argument('--top-k', type=int, default=3, help='返回结果数量')

    args = parser.parse_args()

    config_path = Path(args.config).expanduser()
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    if args.command == 'build':
        builder = IndexBuilder(config)
        result = builder.build_index()
        print(f"索引构建完成：{result['total_documents']} 个文档，{result['total_blocks']} 个块")

    elif args.command == 'search':
        if not args.query:
            print("错误：search命令需要 --query 参数")
            exit(1)
        searcher = KnowledgeSearcher(config)
        results = searcher.search(args.query, args.top_k)
        print(searcher.format_results(results, args.query))

    elif args.command == 'stats':
        searcher = KnowledgeSearcher(config)
        stats = searcher.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
