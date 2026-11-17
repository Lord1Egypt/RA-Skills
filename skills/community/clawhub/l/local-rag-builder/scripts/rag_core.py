"""
local-rag-builder 共享核心模块
v0.2.0

纯核心层：不涉及任何 LLM 调用，不依赖外部服务。
同时被 rag_skill.py（技能接口）和 rag_standalone.py（独立系统）导入。
"""

import os
import json

from config import load_config
from utils import KB_DIR, MODELS_DIR, find_model_dirs


def get_embeddings(model_path=None, device="auto", kb_name=None):
    """获取嵌入模型实例。
    如果指定 kb_name，优先使用该知识库的专属模型；没有则回退全局默认。
    """
    from langchain_huggingface import HuggingFaceEmbeddings
    import torch

    cfg = load_config()
    emb_cfg = cfg.get("embedding", {})

    # 如果指定了知识库，优先查 KB 专属模型
    if model_path is None and kb_name:
        try:
            from knowledge_base_manager import get_kb_model
            kb_model = get_kb_model(kb_name)
            if kb_model:
                model_path = kb_model
        except Exception:
            pass

    if model_path is None:
        model_path = emb_cfg.get("model_path", "")
    # 校验：路径为空或路径失效时回退到扫描 MODELS_DIR
    if not model_path or not os.path.exists(model_path):
        models = find_model_dirs(MODELS_DIR)
        if not models:
            raise ValueError("未找到嵌入模型。请先运行 embedding_model_manager.py 下载模型")
        model_path = models[0]["path"]

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={"device": device, "local_files_only": True},
        encode_kwargs={"normalize_embeddings": emb_cfg.get("normalize_embeddings", True)},
    )


def retrieve_documents(query, kb_name="default", k=None, score_threshold=None, embeddings=None):
    """检索相关文档"""
    from langchain_chroma import Chroma

    if embeddings is None:
        embeddings = get_embeddings(kb_name=kb_name)

    kb_path = os.path.join(KB_DIR, kb_name)
    if not os.path.exists(kb_path) or not os.listdir(kb_path):
        return []

    vectorstore = Chroma(
        persist_directory=kb_path,
        embedding_function=embeddings,
    )

    cfg = load_config()
    ret_cfg = cfg.get("retrieval", {})
    if k is None:
        k = ret_cfg.get("k", 3)
    if score_threshold is None:
        score_threshold = ret_cfg.get("score_threshold")

    if score_threshold:
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": score_threshold, "k": k},
        )
    else:
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    return retriever.invoke(query)


def build_context(docs):
    """从检索结果构建上下文字符串"""
    parts = []
    for i, doc in enumerate(docs):
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        meta = doc.metadata if hasattr(doc, "metadata") else {}
        source = meta.get("source", meta.get("h1", f"[{i + 1}]"))
        parts.append(f"[片段 {i + 1}] (来源: {source})\n{content}")
    return "\n\n---\n\n".join(parts)


def retrieve_context(question, kb_name="default", k=None, score_threshold=None, embeddings=None):
    """
    纯检索接口：只检索和构建 context，不调用 LLM。
    返回结构化结果，供任何调用方（智能体 / 独立系统）消费。
    """
    docs = retrieve_documents(
        question, kb_name=kb_name, k=k,
        score_threshold=score_threshold, embeddings=embeddings,
    )
    if not docs:
        return {"context": "", "source_docs": [], "source_count": 0, "question": question}

    context = build_context(docs)
    # source_docs 转可序列化格式
    serialized = []
    for d in docs:
        serialized.append({
            "content": d.page_content if hasattr(d, "page_content") else str(d),
            "metadata": d.metadata if hasattr(d, "metadata") else {},
            "length": len(d.page_content) if hasattr(d, "page_content") else len(str(d)),
        })

    return {
        "context": context,
        "source_docs": serialized,
        "source_count": len(docs),
        "question": question,
    }


def format_skill_output(question, kb_name="default", k=None, score_threshold=None,
                        embeddings=None, template=None):
    """
    [技能接口核心] 检索 + 格式化输出。
    返回的 JSON 包含完整的 prompt（已填充 {context} 和 {question}），
    任何智能体直接拿着 prompt 即可作答。

    返回结构:
    {
      "question": str,          # 原始问题
      "kb": str,                # 检索的知识库
      "context": str,           # 检索到的文本块
      "source_count": int,      # 命中的片段数
      "source_docs": [...],     # 每个片段的详情
      "prompt": str,            # 已填充的完整 prompt（含 context + question）
      "prompt_template": str,   # 原始 prompt 模板
      "has_context": bool,      # 是否找到相关内容
    }
    """
    from prompt_manager import load_template, get_default_template

    # 检索
    retrieval = retrieve_context(
        question, kb_name=kb_name, k=k,
        score_threshold=score_threshold, embeddings=embeddings,
    )

    context = retrieval["context"]
    has_context = bool(context)

    # 获取 prompt 模板
    tpl = template or load_template()

    # 填充占位符
    if has_context:
        prompt = tpl.format(context=context, question=question)
    else:
        # 无 context 时也尝试填充，占位符缺失则保留原样
        try:
            prompt = tpl.format(context="（未检索到相关资料）", question=question)
        except KeyError:
            prompt = tpl.replace("{context}", "（未检索到相关资料）").replace("{question}", question)

    return {
        "question": question,
        "kb": kb_name,
        "context": context,
        "source_count": retrieval["source_count"],
        "source_docs": retrieval["source_docs"],
        "prompt": prompt,
        "prompt_template": tpl,
        "has_context": has_context,
    }


def import_documents_to_kb(file_path, kb_name="default", embeddings=None, splitter_config=None):
    """导入文档到知识库"""
    from text_splitter import split_pipeline
    from knowledge_base_manager import add_documents_to_kb

    if embeddings is None:
        embeddings = get_embeddings(kb_name=kb_name)

    try:
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
    except Exception as e:
        raise RuntimeError(f"文档加载失败: {e}")

    cfg = load_config()
    split_cfg = splitter_config or cfg.get("splitting", {})

    # 合并基础配置 + 策略级覆盖
    strategy_overrides = split_cfg.get("strategy_overrides", {})
    primary = split_cfg.get("strategy", "recursive")
    sec_strat = split_cfg.get("secondary_strategy")

    pipeline_kwargs = dict(
        guards=split_cfg.get("guards", ["code"]),
        primary=primary,
        secondary=sec_strat,
        chunk_size=split_cfg.get("chunk_size", 500),
        chunk_overlap=split_cfg.get("chunk_overlap", 50),
        separators=split_cfg.get("separators"),
        headers_to_split_on=split_cfg.get("headers_to_split_on"),
        strip_headers=split_cfg.get("strip_headers", False),
        strategy_overrides=strategy_overrides,
    )

    # 从 strategy_overrides 注入当前策略的专属参数
    over = strategy_overrides.get(primary, {})
    for k in ("separators", "headers_to_split_on", "strip_headers", "breakpoint_type", "language", "delimiters"):
        if k in over:
            pipeline_kwargs[k] = over[k]

    chunks = split_pipeline(docs[0].page_content, **pipeline_kwargs)

    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(file_path)

    ok, msg = add_documents_to_kb(kb_name, chunks, embeddings)

    return {
        "success": ok,
        "message": msg,
        "chunks_count": len(chunks),
        "source": os.path.basename(file_path),
    }
