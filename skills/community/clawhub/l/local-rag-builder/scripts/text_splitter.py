"""
local-rag-builder 文本切分模块
v1.0.0

架构：插件注册 → 守卫栈(多选) → 主策略(单选) → 后处理(单选/不选)

插件化设计：
  - 每个策略/守卫是一个 Plugin 对象，声明 name/description/config_schema/default_config
  - 通过 register_strategy() / register_guard() 注册
  - 外部用户可通过 register_* 添加自定义策略
  - Web UI 通过 plugin.config_schema 动态渲染配置表单

内置策略：fixed / recursive / headers / sentence / semantic（5种）
内置守卫：mermaid / code / math / table / html（5种）
"""

import os
import sys
import re
import json

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "output")

# ==================== 插件注册架构 ====================

class StrategyPlugin:
    """策略插件：包裹一个切分函数及其配置声明"""
    def __init__(self, name, description, fn, config_schema=None, default_config=None):
        self.name = name
        self.description = description
        self.fn = fn  # fn(text, **resolved_config) → List[Document]
        self.config_schema = config_schema or {}  # {key: {type, label, default, options, min, max, ...}}
        self.default_config = default_config or {}

    def execute(self, text, config=None, **kwargs):
        resolved = dict(self.default_config)
        if config:
            resolved.update(config)
        resolved.update(kwargs)
        return self.fn(text, **resolved)


class GuardPlugin:
    """守卫插件：包裹一个 Guard 及其配置声明"""
    def __init__(self, name, description, guard, config_schema=None, default_config=None):
        self.name = name
        self.description = description
        self.guard = guard  # Guard instance
        self.config_schema = config_schema or {}
        self.default_config = default_config or {}


STRATEGY_REGISTRY = {}  # {name: StrategyPlugin}
GUARD_REGISTRY = {}     # {name: GuardPlugin}


def register_strategy(plugin):
    """注册切分策略"""
    STRATEGY_REGISTRY[plugin.name] = plugin


def register_guard(plugin):
    """注册守卫"""
    GUARD_REGISTRY[plugin.name] = plugin


def get_strategy_config_schema(strategy_name):
    """获取策略的 config_schema（供 Web UI 渲染用）"""
    p = STRATEGY_REGISTRY.get(strategy_name)
    return p.config_schema if p else {}


def get_all_strategies_info():
    """返回 [{name, description, config_schema}] 供 Web UI 用"""
    return [{"name": p.name, "description": p.description, "config_schema": p.config_schema}
            for p in STRATEGY_REGISTRY.values()]


def get_all_guards_info():
    """返回 [{name, description, config_schema}] 供 Web UI 用"""
    return [{"name": p.name, "description": p.description, "config_schema": p.config_schema}
            for p in GUARD_REGISTRY.values()]


# 元数据白名单
INHERITABLE_META_KEYS = {"source", "h1", "h2", "h3", "group_id"}


def filter_inheritable_meta(metadata: dict) -> dict:
    """过滤可继承的元数据（扔掉 chunk_id/start_pos 等位置信息）"""
    return {k: v for k, v in metadata.items() if k in INHERITABLE_META_KEYS}


# ==================== 守卫栈 ====================

class Guard:
    """单个守卫：protect 替换 → restore 还原"""
    def __init__(self, name: str, pattern: re.Pattern):
        self.name = name
        self.pattern = pattern
        self._blocks: list[str] = []

    @property
    def _prefix(self):
        return f"__GUARD_{self.name.upper()}_"

    def protect(self, text: str) -> str:
        """替换匹配内容为占位符，返回保护后的文本"""
        self._blocks = []

        def _replacer(m):
            self._blocks.append(m.group(0))
            return f"{self._prefix}{len(self._blocks) - 1}__"

        return self.pattern.sub(_replacer, text)

    def restore(self, text: str) -> str:
        """将占位符还原为原始内容"""
        for i, block in enumerate(self._blocks):
            text = text.replace(f"{self._prefix}{i}__", block)
        return text

    def restore_chunks(self, chunks: list) -> list:
        """对 chunks 列表进行内容还原"""
        for chunk in chunks:
            if hasattr(chunk, "page_content"):
                chunk.page_content = self.restore(chunk.page_content)
        return chunks

    def reset(self):
        self._blocks = []


# 内置守卫定义
GUARD_MERMAID = Guard(
    "mermaid",
    re.compile(r'```mermaid\s*\n[\s\S]*?\n```', re.MULTILINE),
)

GUARD_CODE = Guard(
    "code",
    re.compile(r'```\w*\n[\s\S]*?\n```', re.MULTILINE),
)

GUARD_MATH = Guard(
    "math",
    re.compile(r'\$\$[\s\S]*?\$\$', re.MULTILINE),
)

# 表格守卫：保护标准 Markdown 表格行（不保护单行，保护连续表格块）
# 匹配至少两行连续的 | ... | 模式
_TABLE_PATTERN = re.compile(
    r'(?:\|.*\|(?:\s*$)\n?){2,}',
    re.MULTILINE,
)
GUARD_TABLE = Guard("table", _TABLE_PATTERN)

# HTML 块级标签守卫（div, table, pre, section, article, main, aside, details）
_HTML_BLOCK_PATTERN = re.compile(
    r'<(div|table|pre|section|article|main|aside|details|blockquote|figure|figcaption)'
    r'[^>]*>[\s\S]*?</\1>',
    re.MULTILINE | re.IGNORECASE,
)
GUARD_HTML = Guard("html", _HTML_BLOCK_PATTERN)

ALL_GUARDS = {
    "mermaid": GUARD_MERMAID,
    "code": GUARD_CODE,
    "math": GUARD_MATH,
    "table": GUARD_TABLE,
    "html": GUARD_HTML,
}


class GuardStack:
    """守卫栈：多个守卫按序执行 protect，反向执行 restore"""

    def __init__(self, guard_names=None):
        self.guards: list[Guard] = []
        if guard_names:
            for name in guard_names:
                name = name.strip().lower()
                if name in ALL_GUARDS:
                    self.guards.append(ALL_GUARDS[name])

    def add(self, name: str):
        name = name.strip().lower()
        if name in ALL_GUARDS and name not in [g.name for g in self.guards]:
            self.guards.append(ALL_GUARDS[name])

    def apply(self, text: str) -> str:
        """按序执行所有守卫的 protect"""
        for g in self.guards:
            g.reset()
            text = g.protect(text)
        return text

    def restore(self, text: str) -> str:
        """反向执行所有守卫的 restore"""
        for g in reversed(self.guards):
            text = g.restore(text)
        return text

    def restore_chunks(self, chunks: list) -> list:
        """反向执行所有守卫的 restore_chunks"""
        for g in reversed(self.guards):
            chunks = g.restore_chunks(chunks)
        return chunks

    def __len__(self):
        return len(self.guards)

    def __repr__(self):
        return f"GuardStack({[g.name for g in self.guards]})"


# ==================== 单策略切分函数（保持不变）====================

def split_fixed_size(text, chunk_size=500, chunk_overlap=50):
    """策略1: 固定窗口切分"""
    from langchain_text_splitters import CharacterTextSplitter
    from langchain_core.documents import Document

    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="",
    )
    docs = [Document(page_content=text)]
    return splitter.split_documents(docs)


def split_recursive(text, chunk_size=500, chunk_overlap=50, separators=None):
    """策略2: 递归切分"""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    if separators is None:
        separators = ["\n\n", "\n", "。", "；", "，", " ", ""]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    docs = [Document(page_content=text)]
    return splitter.split_documents(docs)


def split_by_headers(text, headers_to_split_on=None, strip_headers=False):
    """策略3: 层级/标题切分"""
    from langchain_text_splitters import MarkdownHeaderTextSplitter

    if headers_to_split_on is None:
        headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ]

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=strip_headers,
    )
    return splitter.split_text(text)


def split_by_sentence(text, language="中文", delimiters=None):
    """策略4: 按句切分"""
    from langchain_core.documents import Document

    if delimiters is None:
        if language == "中文":
            delimiters = ["。", "！", "？"]
        elif language == "English":
            delimiters = [".", "!", "?"]
        else:  # 自定义
            delimiters = list("。！？")

    try:
        import nltk
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt", quiet=True)
        if language == "中文":
            sentences = nltk.sent_tokenize(text, language="chinese")
        elif language == "English":
            sentences = nltk.sent_tokenize(text, language="english")
        else:
            raise ImportError("skip")
    except (ImportError, Exception, LookupError):
        delim_pattern = "[" + "".join(re.escape(d) for d in delimiters) + "]"
        sentences = [s.strip() for s in re.split(delim_pattern, text) if s.strip()]
        if sentences:
            last_delim = delimiters[0] if delimiters else "。"
            sentences = [s + last_delim for s in sentences]

    docs = []
    for s in sentences:
        if s.strip():
            docs.append(Document(page_content=s.strip()))
    return docs


def split_semantic(text, embeddings=None, breakpoint_type="percentile"):
    """策略5: 语义切分（需 langchain-experimental）"""
    try:
        from langchain_experimental.text_splitter import SemanticChunker
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        raise ImportError("语义切分需要 langchain-experimental: pip install langchain-experimental")

    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type=breakpoint_type,
    )
    return splitter.split_text(text)


# ==================== 后处理（子切分）====================

def _run_secondary(chunks: list, secondary_strategy: str,
                  chunk_size: int, chunk_overlap: int) -> list:
    """
    对 chunks 执行二次切分，metadata 白名单继承。
    只有 chunks 内容长度超过 chunk_size 的才子切。
    """
    from langchain_core.documents import Document

    if not secondary_strategy or secondary_strategy == "none":
        return chunks

    if secondary_strategy == "recursive":
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    elif secondary_strategy == "fixed":
        from langchain_text_splitters import CharacterTextSplitter
        splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="",
        )
    elif secondary_strategy == "semantic":
        try:
            from langchain_experimental.text_splitter import SemanticChunker
            from langchain_huggingface import HuggingFaceEmbeddings
            splitter = SemanticChunker(
                embeddings=HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5"),
                breakpoint_threshold_type="percentile",
            )
        except ImportError:
            raise ImportError("语义子切需要 langchain-experimental: pip install langchain-experimental")
    else:
        return chunks

    result = []
    for doc in chunks:
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        if len(content) <= chunk_size:
            result.append(doc)
            continue

        parent_meta = filter_inheritable_meta(doc.metadata if hasattr(doc, "metadata") else {})

        if secondary_strategy == "semantic":
            sub_chunks = splitter.split_text(content)
            for sub in sub_chunks:
                if hasattr(sub, "metadata"):
                    sub.metadata.update(parent_meta)
                elif isinstance(sub, str):
                    sub = Document(page_content=sub, metadata=parent_meta)
                result.append(sub)
            continue

        # recursive / fixed
        sub_docs = splitter.split_documents([doc])
        for sub in sub_docs:
            if hasattr(sub, "metadata") and parent_meta:
                sub.metadata.update(parent_meta)
            result.append(sub)

    return result


# ==================== 三层 Pipeline ====================

PRIMARY_MAP = {
    "fixed": split_fixed_size,
    "recursive": split_recursive,
    "headers": split_by_headers,
    "sentence": split_by_sentence,
    "semantic": split_semantic,
}

# 哪些主策略的 metadata 值得传给子切
META_INHERIT_STRATEGIES = {"headers", "semantic"}


def split_pipeline(text, guards=None, primary="recursive", secondary=None,
                   chunk_size=500, chunk_overlap=50, **kwargs):
    """
    三层切分流水线：守卫栈 → 主切分 → 后处理(子切)

    参数:
        text: 输入文本
        guards: 守卫名称列表，如 ["mermaid", "code", "table"]
        primary: 主策略名，支持 fixed/recursive/headers/sentence/semantic
        secondary: 后处理策略，支持 recursive/fixed/semantic/None
        chunk_size: 块大小
        chunk_overlap: 块重叠
        **kwargs: 传递给主策略的额外参数（headers_to_split_on, strip_headers, separators, etc.）
    """
    from langchain_core.documents import Document

    # 1. 守卫栈（预处理）
    guard_stack = GuardStack(guards or [])
    protected_text = guard_stack.apply(text)

    # 2. 主切分（通过注册表执行）
    plugin = STRATEGY_REGISTRY.get(primary)
    if plugin is None:
        raise ValueError(f"未知切分策略: {primary}，可选: {', '.join(STRATEGY_REGISTRY.keys())}")

    # 策略级覆盖 chunk_size
    strategy_overrides = kwargs.get("strategy_overrides", {})
    if primary in strategy_overrides:
        over = strategy_overrides[primary]
        actual_chunk_size = over.get("chunk_size") if over.get("chunk_size") is not None else chunk_size
        actual_chunk_overlap = over.get("chunk_overlap") if over.get("chunk_overlap") is not None else chunk_overlap
    else:
        actual_chunk_size = chunk_size
        actual_chunk_overlap = chunk_overlap

    # 从 kwargs 中提取策略配置字段
    schema_keys = set(plugin.config_schema.keys())
    strategy_kwargs = {k: v for k, v in kwargs.items() if k in schema_keys}

    # 如果没传，用 default_config
    for k, v in plugin.default_config.items():
        if k not in strategy_kwargs:
            strategy_kwargs[k] = v

    # 覆盖 chunk_size
    if primary in ("fixed", "recursive"):
        strategy_kwargs["chunk_size"] = actual_chunk_size
        strategy_kwargs["chunk_overlap"] = actual_chunk_overlap

    chunks = plugin.execute(protected_text, strategy_kwargs)

    # 3. 守卫还原
    chunks = guard_stack.restore_chunks(chunks)

    # 4. 后处理（子切）
    if secondary and secondary != primary:
        # 只有 headers/semantic 主策略需要 metadata 继承
        if primary in META_INHERIT_STRATEGIES:
            chunks = _run_secondary(chunks, secondary, chunk_size, chunk_overlap)
        else:
            # 固定/递归/按句：纯子切，不继承位置 metadata
            chunks = _run_secondary_without_inherit(chunks, secondary, chunk_size, chunk_overlap)

    return chunks


def _run_secondary_without_inherit(chunks, secondary_strategy, chunk_size, chunk_overlap):
    """后处理但不继承 metadata（用于 fixed/recursive/sentence 主策略）"""
    if not secondary_strategy or secondary_strategy == "none":
        return chunks

    if secondary_strategy == "recursive":
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    elif secondary_strategy == "fixed":
        from langchain_text_splitters import CharacterTextSplitter
        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="")
    else:
        return chunks

    result = []
    for doc in chunks:
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        if len(content) <= chunk_size:
            result.append(doc)
            continue
        # 子切但不继承 metadata（仅保留 source）
        sub_docs = splitter.split_documents([doc])
        for sub in sub_docs:
            if hasattr(sub, "metadata") and "source" in (doc.metadata or {}):
                sub.metadata["source"] = doc.metadata["source"]
            result.append(sub)
    return result


# ==================== 向后兼容 ====================

def combo_split(text, primary_strategy="recursive", secondary_strategy=None,
                chunk_size=500, chunk_overlap=50, **kwargs):
    """
    向后兼容的 combo_split
    内部调用 split_pipeline
    """
    # 从 kwargs 识别守卫
    guards = kwargs.pop("guards", None)

    # 旧版 mermaid 策略 → 转为 guards=["mermaid"] + primary="headers"
    if primary_strategy == "mermaid":
        primary_strategy = "headers"
        if guards is None:
            guards = ["mermaid"]
        elif "mermaid" not in guards:
            guards = list(guards) + ["mermaid"]

    return split_pipeline(
        text,
        guards=guards,
        primary=primary_strategy,
        secondary=secondary_strategy,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        **kwargs
    )


def split_with_mermaid_preserve(text, headers_to_split_on=None, strip_headers=False):
    """旧版 mermaid 保护切分（保留向后兼容，内部走 pipeline）"""
    return split_pipeline(
        text,
        guards=["mermaid"],
        primary="headers",
        headers_to_split_on=headers_to_split_on or [("#", "h1"), ("##", "h2"), ("###", "h3")],
        strip_headers=strip_headers,
    )


# ==================== 注册内置策略和守卫 ====================

register_strategy(StrategyPlugin(
    "fixed", "固定窗口切分", split_fixed_size,
    config_schema={
        "chunk_size": {"type": "int", "label": "块大小", "default": 500, "min": 50, "max": 5000},
        "chunk_overlap": {"type": "int", "label": "重叠", "default": 50, "min": 0, "max": 1000},
    },
    default_config={"chunk_size": 500, "chunk_overlap": 50},
))

register_strategy(StrategyPlugin(
    "recursive", "递归切分", split_recursive,
    config_schema={
        "chunk_size": {"type": "int", "label": "块大小", "default": 500, "min": 50, "max": 5000},
        "chunk_overlap": {"type": "int", "label": "重叠", "default": 50, "min": 0, "max": 1000},
        "separators": {"type": "text", "label": "分隔符（逗号分隔）", "default": "\\n\\n,\\n,。,；，, ,"},
    },
    default_config={"chunk_size": 500, "chunk_overlap": 50, "separators": ["\n\n", "\n", "。", "；", "，", " ", ""]},
))

register_strategy(StrategyPlugin(
    "headers", "层级/标题切分", split_by_headers,
    config_schema={
        "headers_to_split_on": {"type": "multi-select", "label": "标题级别",
                                 "options": ["#", "##", "###", "####"],
                                 "default": ["#", "##", "###"]},
        "strip_headers": {"type": "bool", "label": "去除标题", "default": False},
    },
    default_config={"headers_to_split_on": [("#", "h1"), ("##", "h2"), ("###", "h3")], "strip_headers": False},
))

register_strategy(StrategyPlugin(
    "sentence", "按句切分", split_by_sentence,
    config_schema={
        "language": {"type": "select", "label": "语言", "options": ["中文", "English", "自定义"],
                      "default": "中文"},
        "delimiters": {"type": "text", "label": "自定义边界符（直接输入字符）", "default": "。！？"},
    },
    default_config={"language": "中文", "delimiters": "。！？"},
))

register_strategy(StrategyPlugin(
    "semantic", "语义切分", split_semantic,
    config_schema={
        "breakpoint_type": {"type": "select", "label": "断点算法",
                             "options": ["percentile", "gradient", "stddev"],
                             "default": "percentile"},
    },
    default_config={"breakpoint_type": "percentile"},
))

# 注册守卫
for g in [GUARD_MERMAID, GUARD_CODE, GUARD_MATH, GUARD_TABLE, GUARD_HTML]:
    descs = {"mermaid": "保护 ```mermaid 流程图", "code": "保护围栏代码块",
             "math": "保护 LaTeX 公式 $$...$$", "table": "保护 Markdown 表格",
             "html": "保护 HTML 块级标签"}
    register_guard(GuardPlugin(g.name, descs.get(g.name, ""), g))

# 后处理策略（与主策略共享注册表，但标记 role=secondary）
SECONDARY_STRATEGIES = {"recursive": split_recursive, "fixed": split_fixed_size, "semantic": split_semantic}

PRIMARY_MAP = {name: p.fn for name, p in STRATEGY_REGISTRY.items()}
ALL_GUARDS = {name: gp.guard for name, gp in GUARD_REGISTRY.items()}


# ==================== CLI 入口 ====================

def format_chunks_report(chunks):
    """格式化切分结果报告"""
    lines = [f"切分结果: {len(chunks)} 个块", ""]
    for i, chunk in enumerate(chunks):
        meta = chunk.metadata if hasattr(chunk, "metadata") else {}
        content = chunk.page_content if hasattr(chunk, "page_content") else str(chunk)
        meta_str = json.dumps(meta, ensure_ascii=False) if meta else ""
        lines.append(f"[{i + 1}] {len(content)} 字符 {meta_str}")
        lines.append(content[:150] + ("..." if len(content) > 150 else ""))
        lines.append("")
    return "\n".join(lines)


def save_chunks(chunks, output_path=None):
    """保存切分结果到文件"""
    if output_path is None:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, "chunks_output.json")

    data = []
    for chunk in chunks:
        data.append({
            "content": chunk.page_content if hasattr(chunk, "page_content") else str(chunk),
            "metadata": chunk.metadata if hasattr(chunk, "metadata") else {},
            "length": len(chunk.page_content) if hasattr(chunk, "page_content") else len(str(chunk)),
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


# ==================== CLI 入口 ====================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="文本切分工具（三层流水线：守卫栈 → 主策略 → 后处理）")
    parser.add_argument("--input", type=str, required=True, help="输入文件路径 (txt/md)")
    parser.add_argument("--strategy", type=str, default="recursive",
                        choices=["fixed", "recursive", "headers", "sentence", "semantic"],
                        help="主策略")
    parser.add_argument("--guard", type=str, default="",
                        help="守卫栈（多选，逗号分隔）: mermaid,code,math,table,html")
    parser.add_argument("--secondary", type=str, choices=["recursive", "fixed", "semantic", "none"],
                        help="后处理子切策略")
    parser.add_argument("--chunk-size", type=int, default=500, help="块大小")
    parser.add_argument("--overlap", type=int, default=50, help="重叠字符数")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--list-strategies", action="store_true", help="列出可用策略和守卫")

    args = parser.parse_args()

    if args.list_strategies:
        strategies = [
            ("fixed", "固定窗口切分", "按固定字符数切分，可设重叠"),
            ("recursive", "递归切分", "按优先级尝试不同分隔符，性价比最高"),
            ("headers", "层级/标题切分", "基于 Markdown 标题切分，保留结构元数据"),
            ("sentence", "按句切分", "以句子为单位，适合证据抽取"),
            ("semantic", "语义切分", "计算相邻句子相似度，精度最高但成本高"),
        ]
        print("可用主策略:")
        print("-" * 60)
        for name, title, desc in strategies:
            print(f"  {name:<15} {title:<20} {desc}")

        print("\n可用守卫（多选，--guard mermaid,code,math,table,html）:")
        print("-" * 60)
        guards_info = [
            ("mermaid", "保护 ```mermaid 流程图不被切碎"),
            ("code", "保护所有围栏代码块 (```lang ... ```)"),
            ("math", "保护 LaTeX 数学公式 ($$...$$)"),
            ("table", "保护 Markdown 表格不被跨行切断"),
            ("html", "保护 HTML 块级标签 (div/table/pre 等)"),
        ]
        for name, desc in guards_info:
            print(f"  {name:<15} {desc}")

        print("\n可用后处理（--secondary）:")
        print("-" * 60)
        post_info = [
            ("recursive", "递归子切（带 metadata 继承）"),
            ("fixed", "固定窗口子切（带 metadata 继承）"),
            ("semantic", "语义子切（带 metadata 继承）"),
            ("none", "不进行子切"),
        ]
        for name, desc in post_info:
            print(f"  {name:<15} {desc}")
        print("\n注意：headers/semantic 主策略的子切会继承 h1/h2/h3/source 元数据")
        sys.exit(0)

    if not os.path.exists(args.input):
        print(f"[!] 输入文件不存在: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    guard_list = [g.strip() for g in args.guard.split(",") if g.strip()] if args.guard else []
    secondary = args.secondary if args.secondary and args.secondary != "none" else None

    print(f"输入文件: {args.input} ({len(text)} 字符)")
    print(f"守卫: {guard_list or '无'}")
    print(f"主策略: {args.strategy}", end="")
    if secondary:
        print(f" → 后处理: {secondary}")
    else:
        print()

    chunks = split_pipeline(
        text,
        guards=guard_list,
        primary=args.strategy,
        secondary=secondary,
        chunk_size=args.chunk_size,
        chunk_overlap=args.overlap,
    )

    if args.json:
        data = []
        for chunk in chunks:
            data.append({
                "content": chunk.page_content if hasattr(chunk, "page_content") else str(chunk),
                "metadata": chunk.metadata if hasattr(chunk, "metadata") else {},
                "length": len(chunk.page_content) if hasattr(chunk, "page_content") else len(str(chunk)),
            })
        print(json.dumps({"total_chunks": len(chunks), "chunks": data}, ensure_ascii=False, indent=2))
    else:
        print(format_chunks_report(chunks))

    if args.output:
        path = save_chunks(chunks, args.output)
        print(f"\n已保存到: {path}")
