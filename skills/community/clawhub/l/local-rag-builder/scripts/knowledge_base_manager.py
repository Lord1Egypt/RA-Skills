"""
local-rag-builder 知识库管理模块
v0.1.0
支持多知识库创建、导入、删除、自动分类
"""

import os
import sys
import json
import glob

from utils import KB_DIR, safe_json_load, safe_json_dump

KB_INDEX_FILE = os.path.join(KB_DIR, "kb_index.json")
AUTO_CLASSIFY_RULES_FILE = os.path.join(KB_DIR, "auto_classify_rules.json")


def _load_index():
    data = safe_json_load(KB_INDEX_FILE, {})
    if not data:
        data = {"default": {"path": os.path.join(KB_DIR, "default"), "description": "默认知识库"}}
        os.makedirs(os.path.join(KB_DIR, "default"), exist_ok=True)
        safe_json_dump(data, KB_INDEX_FILE)
    return data


def _save_index(index):
    safe_json_dump(index, KB_INDEX_FILE)


def _load_rules():
    return safe_json_load(AUTO_CLASSIFY_RULES_FILE, {})


def _save_rules(rules):
    safe_json_dump(rules, AUTO_CLASSIFY_RULES_FILE)


def list_knowledge_bases():
    """列出所有知识库"""
    return _load_index()


def create_knowledge_base(name, description="", model_id=""):
    """创建新知识库"""
    index = _load_index()
    if name in index:
        return False, f"知识库 '{name}' 已存在"

    kb_path = os.path.join(KB_DIR, name)
    os.makedirs(kb_path, exist_ok=True)

    entry = {
        "path": kb_path,
        "description": description,
        "created": str(__import__("datetime").datetime.now()),
        "doc_count": 0,
    }
    if model_id:
        entry["embedding_model"] = model_id
    index[name] = entry
    _save_index(index)
    return True, f"知识库 '{name}' 已创建"


def set_kb_model(kb_name, model_id=""):
    """设置/清除知识库的嵌入模型。空字符串 = 回退到全局默认。"""
    index = _load_index()
    if kb_name not in index:
        return False, f"知识库 '{kb_name}' 不存在"
    if model_id:
        index[kb_name]["embedding_model"] = model_id
    else:
        index[kb_name].pop("embedding_model", None)
    _save_index(index)
    return True, f"知识库 '{kb_name}' 嵌入模型已{'更新' if model_id else '清除（回退全局默认）'}"


def get_kb_model(kb_name):
    """获取知识库指定的嵌入模型 ID，空串表示未指定（回退全局默认）"""
    index = _load_index()
    entry = index.get(kb_name, {})
    return entry.get("embedding_model", "")


def delete_knowledge_base(name):
    """删除知识库"""
    index = _load_index()
    if name not in index:
        return False, f"知识库 '{name}' 不存在"
    if name == "default":
        return False, "不能删除默认知识库"

    import shutil
    kb_path = index[name]["path"]
    if os.path.exists(kb_path):
        shutil.rmtree(kb_path)

    del index[name]
    _save_index(index)
    return True, f"知识库 '{name}' 已删除"


def get_kb_vectorstore(kb_name, embeddings):
    """获取知识库的向量存储对象"""
    from langchain_chroma import Chroma

    index = _load_index()
    if kb_name not in index:
        kb_name = "default"

    persist_dir = index[kb_name]["path"]

    # 检查是否已有数据
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
        )
    return None


def add_documents_to_kb(kb_name, documents, embeddings=None):
    """向知识库添加文档"""
    from langchain_chroma import Chroma

    index = _load_index()
    if kb_name not in index:
        return False, f"知识库 '{kb_name}' 不存在"

    persist_dir = index[kb_name]["path"]
    os.makedirs(persist_dir, exist_ok=True)

    if embeddings is None:
        return False, "需要提供嵌入模型"

    # 检查是否已有向量库
    if os.path.exists(persist_dir) and any(f.endswith(".parquet") for f in os.listdir(persist_dir)):
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
        )
        vectorstore.add_documents(documents)
    else:
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_dir,
        )

    # 更新文档计数
    try:
        count = vectorstore._collection.count()
    except Exception:
        count = len(documents)

    index[kb_name]["doc_count"] = count
    _save_index(index)

    return True, f"已向 '{kb_name}' 添加 {len(documents)} 个文档块 (总计: {count})"


def auto_classify(content, rules=None, filename=None):
    """根据规则自动分类内容到对应知识库

    支持：
    - 关键词匹配（内容）
    - 文件扩展名匹配（如 .py .md .pdf）
    """
    if rules is None:
        rules = _load_rules()

    if not rules:
        return "default"

    content_lower = content.lower()
    ext = os.path.splitext(filename or "")[1].lower() if filename else ""
    best_match = "default"
    best_score = 0

    for kb_name, rule in rules.items():
        score = 0
        # 关键词匹配
        for kw in rule.get("keywords", []):
            if kw.lower() in content_lower:
                score += 1
        # 扩展名匹配
        for ex in rule.get("extensions", []):
            if ex.lower() == ext:
                score += 3  # 扩展名匹配权重更高
        if score > best_score:
            best_score = score
            best_match = kb_name

    return best_match


def set_classify_rule(kb_name, keywords=None, extensions=None, description=""):
    """设置自动分类规则"""
    rules = _load_rules()
    entry = {"description": description}
    if keywords:
        entry["keywords"] = keywords if isinstance(keywords, list) else [keywords]
    if extensions:
        entry["extensions"] = extensions if isinstance(extensions, list) else [extensions]
    rules[kb_name] = entry
    _save_rules(rules)
    parts = []
    if keywords:
        parts.append(f"关键词: {keywords}")
    if extensions:
        parts.append(f"扩展名: {extensions}")
    return True, f"分类规则已设置: '{kb_name}' ← {'; '.join(parts)}"


def remove_classify_rule(kb_name):
    """删除分类规则"""
    rules = _load_rules()
    if kb_name in rules:
        del rules[kb_name]
        _save_rules(rules)
        return True, f"已删除 '{kb_name}' 的分类规则"
    return False, f"规则 '{kb_name}' 不存在"


def reset_classify_rules():
    """重置分类规则为默认"""
    default_rules = {
        "tech": {
            "keywords": ["代码", "API", "编程", "函数", "class", "def", "import"],
            "extensions": [".py", ".js", ".ts", ".java", ".cpp", ".go", ".rs"],
            "description": "技术代码类",
        },
        "doc": {
            "keywords": ["说明", "文档", "指南", "教程", "手册", "README"],
            "extensions": [".md", ".txt", ".rst"],
            "description": "文档类",
        },
        "data": {
            "keywords": ["数据", "csv", "json", "数据库", "table", "分析"],
            "extensions": [".csv", ".json", ".xml", ".yaml", ".yml"],
            "description": "数据类",
        },
    }
    _save_rules(default_rules)
    return True, "分类规则已重置为默认"


def get_kb_stats():
    """获取所有知识库统计"""
    index = _load_index()
    stats = {}
    for name, info in index.items():
        path = info["path"]
        size_mb = 0
        if os.path.exists(path):
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        size_mb += os.path.getsize(fp)
                    except OSError:
                        pass
            size_mb = round(size_mb / (1024 * 1024), 2)
        stats[name] = {
            **info,
            "size_mb": size_mb,
        }
    return stats


def load_documents_from_file(filepath):
    """从文件加载文档"""
    from langchain_community.document_loaders import TextLoader
    from langchain_core.documents import Document

    ext = os.path.splitext(filepath)[1].lower()

    if ext in (".txt", ".md", ".py", ".json", ".yaml", ".yml"):
        loader = TextLoader(filepath, encoding="utf-8")
        return loader.load()
    else:
        # 尝试 unstructured
        try:
            from langchain_community.document_loaders import UnstructuredFileLoader
            loader = UnstructuredFileLoader(filepath)
            return loader.load()
        except Exception:
            # 回退到基础文本读取
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return [Document(page_content=content, metadata={"source": filepath})]


def load_documents_from_directory(dirpath):
    """从目录加载文档"""
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain_core.documents import Document

    docs = []
    for ext in ("*.txt", "*.md"):
        for filepath in glob.glob(os.path.join(dirpath, "**", ext), recursive=True):
            try:
                loader = TextLoader(filepath, encoding="utf-8")
                docs.extend(loader.load())
            except Exception:
                pass

    return docs


if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="知识库管理工具")
    parser.add_argument("--create", type=str, help="创建知识库")
    parser.add_argument("--desc", type=str, default="", help="知识库描述")
    parser.add_argument("--model", type=str, default="", help="知识库专用嵌入模型 ID 或路径")
    parser.add_argument("--set-model", nargs=2, metavar=("KB_NAME", "MODEL_ID"), help="设置知识库的嵌入模型")
    parser.add_argument("--delete", type=str, help="删除知识库")
    parser.add_argument("--list", action="store_true", help="列出所有知识库")
    parser.add_argument("--stats", action="store_true", help="显示知识库统计")
    parser.add_argument("--import-file", type=str, dest="import_file", help="导入文件到知识库")
    parser.add_argument("--import-dir", type=str, dest="import_dir", help="导入目录到知识库")
    parser.add_argument("--kb", type=str, default="default", help="目标知识库名")
    parser.add_argument("--set-rule", nargs=2, metavar=("KB_NAME", "KEYWORDS"), help="设置分类规则 (逗号分隔关键词)")
    parser.add_argument("--classify", type=str, help="对文本分类到知识库")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.list:
        kbs = list_knowledge_bases()
        if args.json:
            print(json.dumps(kbs, ensure_ascii=False, indent=2))
        else:
            print(f"知识库 ({len(kbs)}):")
            for name, info in kbs.items():
                print(f"  {name}: {info.get('description', '')} [{info.get('doc_count', 0)} 文档]")

    elif args.stats:
        stats = get_kb_stats()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("知识库统计:")
            for name, s in stats.items():
                print(f"  {name}: {s.get('doc_count', 0)} 文档, {s.get('size_mb', 0)} MB")

    elif args.create:
        ok, msg = create_knowledge_base(args.create, args.desc, args.model)
        print(f"[{'OK' if ok else '!'}] {msg}")

    elif args.set_model:
        kb_name, model_id = args.set_model
        ok, msg = set_kb_model(kb_name, model_id)
        print(f"[{'OK' if ok else '!'}] {msg}")

    elif args.delete:
        ok, msg = delete_knowledge_base(args.delete)
        print(f"[{'OK' if ok else '!'}] {msg}")

    elif args.set_rule:
        kb_name, keywords = args.set_rule
        ok, msg = set_classify_rule(kb_name, [k.strip() for k in keywords.split(",")], args.desc)
        print(f"[{'OK' if ok else '!'}] {msg}")

    elif args.classify:
        result = auto_classify(args.classify)
        print(f"分类结果: {result}")

    elif args.import_file:
        if not os.path.exists(args.import_file):
            print(f"[!] 文件不存在: {args.import_file}")
            sys.exit(1)
        docs = load_documents_from_file(args.import_file)
        print(f"加载了 {len(docs)} 个文档")
        # 注：实际向量化需要嵌入模型，此步骤在 rag_core.py 中完成
        output = {"kb": args.kb, "docs_count": len(docs), "docs": [{"content": d.page_content[:100], "metadata": d.metadata} for d in docs]}
        if args.json:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"准备导入知识库 '{args.kb}' ({len(docs)} 块)")
            print(f"运行 rag_core.py --import-kb {args.kb} --input {args.import_file} 完成入库")

    else:
        parser.print_help()
