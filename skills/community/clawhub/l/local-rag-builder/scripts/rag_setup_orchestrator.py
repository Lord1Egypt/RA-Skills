"""
local-rag-builder 标准化搭建编排器 v0.1.0

将 HTML 配置面板映射为可编程参数清单（32 参数，闭合配置域）。
LLM 通过文字交互搭建 RAG 时，必须走完所有参数——自动填/问用户/用默认，不留缺口。

依赖:
- rag_env_setup.py     — 环境检测 & 包安装
- embedding_model_manager.py — 模型下载 & 校验
- knowledge_base_manager.py  — 知识库创建 & 规则
- config.py            — 配置读写
"""

import os
import sys
import json
from typing import Optional, Any

# ═══════════════════════════════════════════════════════════
# 1. 参数定义（32 参数，闭合配置域）
# ═══════════════════════════════════════════════════════════

CONFIG_SCHEMA = {
    "input_sources": {
        "enable_pdf":     {"type": "bool", "default": False, "label": "PDF 支持"},
        "enable_ocr":     {"type": "bool", "default": False, "label": "OCR 支持"},
        "enable_html2md": {"type": "bool", "default": False, "label": "HTML→Markdown"},
        "pdf_backend":    {"type": "enum", "default": "pypdf", "options": ["pypdf", "pdfplumber"], "label": "PDF 引擎"},
    },
    "embedding": {
        "model_path": {"type": "string", "default": "BAAI/bge-small-zh-v1.5", "label": "嵌入模型"},
        "device":     {"type": "enum",  "default": "auto", "options": ["auto", "cuda", "cpu"], "label": "设备"},
    },
    "splitting": {
        "strategy":            {"type": "enum",  "default": "recursive", "options": ["recursive", "fixed", "headers", "sentence", "semantic"], "label": "切分策略"},
        "chunk_size":          {"type": "int",   "default": 500, "min": 50, "max": 10000, "label": "块大小"},
        "chunk_overlap":       {"type": "int",   "default": 50, "min": 0, "max": 500, "label": "重叠"},
        "separators":          {"type": "list",  "default": ["\n\n", "\n", "。", "；", "，", " ", ""], "label": "分隔符"},
        "headers_to_split_on": {"type": "list",  "default": [["#","h1"],["##","h2"],["###","h3"]], "label": "标题层级"},
        "guards":              {"type": "list",  "default": ["code"], "options": ["mermaid","code","math","table","html"], "label": "守卫栈"},
        "secondary_strategy":  {"type": "string","default": None, "label": "后处理策略"},
    },
    "retrieval": {
        "k":               {"type": "int",   "default": 3, "min": 1, "max": 50, "label": "Top-K"},
        "score_threshold": {"type": "float", "default": None, "min": 0, "max": 1, "label": "相似度阈值"},
        "search_type":     {"type": "enum",  "default": "similarity", "options": ["similarity", "mmr"], "label": "检索方式"},
    },
    "kb": {
        "enabled":         {"type": "bool",   "default": True, "label": "多知识库路由"},
        "active_kb":       {"type": "string", "default": "default", "label": "默认知识库"},
        "auto_classify":   {"type": "bool",   "default": False, "label": "自动分类"},
    },
    "router": {
        "enabled":                {"type": "bool",  "default": True, "label": "路由层"},
        "model_path_fallback":    {"type": "string","default": "BAAI/bge-reranker-v2-m3", "label": "回退路由模型"},
        "fallback_threshold":     {"type": "float", "default": 0.3, "min": 0, "max": 1, "label": "回退阈值"},
        "broadcast_on_fail":      {"type": "bool",  "default": True, "label": "广播兜底"},
    },
    "reranker": {
        "enabled":     {"type": "bool",   "default": False, "label": "Rerank 层"},
        "mode":        {"type": "enum",   "default": "model", "options": ["model", "rule", "hybrid"], "label": "Rerank 模式"},
        "model_path":  {"type": "string", "default": "BAAI/bge-reranker-v2-m3", "label": "Rerank 模型"},
        "top_k":       {"type": "int",    "default": 5, "min": 1, "max": 50, "label": "Rerank Top-K"},
        "sort_rules":  {"type": "list",   "default": [], "label": "排序规则"},
    },
    "llm": {
        "base_url":    {"type": "string", "default": "http://localhost:1234/v1", "label": "LLM 地址"},
        "api_key":     {"type": "string", "default": "not-needed", "label": "API Key"},
        "temperature": {"type": "float",  "default": 0.1, "min": 0, "max": 2, "label": "温度"},
        "max_tokens":  {"type": "int",    "default": 512, "min": 1, "max": 16384, "label": "最大 Token"},
        "model_name":  {"type": "string", "default": "", "label": "模型名"},
    },
    "mode": {
        "value": {"type": "enum", "default": "integrated", "options": ["integrated", "standalone"], "label": "运行模式"},
    },
}


# ═══════════════════════════════════════════════════════════
# 2. 钩子系统：参数合法性 & 完整性检查
# ═══════════════════════════════════════════════════════════

class SetupHook:
    """
    每个参数的钩子处理器。
    5 步决策链：用户给定 → 合法性 → 语义推断 → 默认值 → 询问用户。
    """

    def __init__(self, user_input: str):
        self.user_input = user_input.lower()
        self.missing_params = []
        self.asked_params = []
        self.auto_filled = []

    def resolve(self, section: str, key: str, user_value=None) -> Any:
        """解析单个参数"""
        schema = CONFIG_SCHEMA[section][key]
        default = schema["default"]

        # Step 1: 用户明确给了值？
        if user_value is not None:
            # Step 2: 合法性
            if self._validate(schema, user_value):
                return user_value
            raise ValueError(f"参数 {section}.{key} 值 '{user_value}' 不合法")

        # Step 3: 从用户语义推断
        inferred = self._infer(section, key)
        if inferred is not None:
            self.auto_filled.append(f"{section}.{key}={inferred}")
            return inferred

        # Step 4: 有默认值？
        if default is not None:
            self.auto_filled.append(f"{section}.{key}={default} (默认)")
            return default

        # Step 5: 必须问用户
        self.missing_params.append(f"{section}.{key}")
        return None

    def _validate(self, schema: dict, value: Any) -> bool:
        t = schema["type"]
        if t == "int":
            if not isinstance(value, int):
                return False
            if "min" in schema and value < schema["min"]:
                return False
            if "max" in schema and value > schema["max"]:
                return False
            return True
        elif t == "float":
            if not isinstance(value, (int, float)):
                return False
            if "min" in schema and value < schema["min"]:
                return False
            if "max" in schema and value > schema["max"]:
                return False
            return True
        elif t == "bool":
            return isinstance(value, bool)
        elif t == "enum":
            return value in schema.get("options", [])
        elif t == "string":
            return isinstance(value, str)
        elif t == "list":
            return isinstance(value, list)
        return True

    def _infer(self, section: str, key: str):
        """从用户自然语言推断参数值"""
        inp = self.user_input

        # 嵌入模型
        if section == "embedding" and key == "model_path":
            if any(k in inp for k in ["英文", "english", "多语言"]):
                return "sentence-transformers/all-MiniLM-L6-v2"
            if any(k in inp for k in ["中文", "chinese"]):
                return "BAAI/bge-small-zh-v1.5"
            return None

        # 设备
        if section == "embedding" and key == "device":
            if "cpu" in inp:
                return "cpu"
            if "gpu" in inp or "cuda" in inp or "显卡" in inp:
                return "cuda"
            return None

        # 切片策略
        if section == "splitting" and key == "strategy":
            if any(k in inp for k in ["语义", "精准", "semantic"]):
                return "semantic"
            if any(k in inp for k in ["标题", "层级", "markdown"]):
                return "headers"
            if any(k in inp for k in ["句子", "句"]):
                return "sentence"
            return None

        # 块大小
        if section == "splitting" and key == "chunk_size":
            if any(k in inp for k in ["精细", "小段", "精确"]):
                return 200
            if any(k in inp for k in ["粗略", "大段", "概览"]):
                return 1000
            return None

        # 路由
        if section == "router" and key == "enabled":
            if any(k in inp for k in ["多知识库", "多个库", "分类"]):
                return True
            if "不用路由" in inp or "单库" in inp:
                return False
            return None

        # Rerank
        if section == "reranker" and key == "enabled":
            if any(k in inp for k in ["精确排序", "精度高", "rerank"]):
                return True
            return None

        # 模式
        if section == "mode" and key == "value":
            if any(k in inp for k in ["LLM回答", "自己答", "完整", "standalone"]):
                return "standalone"
            if any(k in inp for k in ["纯检索", "不回", "integrated"]):
                return "integrated"
            return None

        return None

    def report(self) -> dict:
        """返回钩子处理报告"""
        return {
            "auto_filled": self.auto_filled,
            "need_ask": self.missing_params,
            "asked": self.asked_params,
        }


def build_full_config(user_input: str, user_overrides: dict = None) -> dict:
    """
    根据用户输入 + 可选覆盖构建完整 32 参数配置。
    缺失参数走钩子链：推断 → 默认 → 标记需询问。
    
    返回: (config_dict, hook_report, pending_questions)
    """
    hook = SetupHook(user_input)
    config = {}

    for section, fields in CONFIG_SCHEMA.items():
        config[section] = {}
        for key in fields:
            override = (user_overrides or {}).get(section, {}).get(key)
            config[section][key] = hook.resolve(section, key, override)

    report = hook.report()
    return config, report, report["need_ask"]


# ═══════════════════════════════════════════════════════════
# 3. 搭建执行器（6 阶段流水线）
# ═══════════════════════════════════════════════════════════

def phase_env_setup(mirror="default") -> dict:
    """阶段 2: 环境检测 & 修复"""
    print("=" * 50)
    print("  [阶段 2/6] 环境检测与修复")
    print("=" * 50)

    from rag_env_setup import run_full_check, check_missing, install_packages, check_torch_gpu

    report = run_full_check()
    required_missing, _ = check_missing()

    if required_missing:
        print(f"\n  安装缺失包 ({len(required_missing)}): {', '.join(required_missing)}")
        results = install_packages(required_missing, mirror=mirror)
        failed = [p for p, ok in results.items() if not ok]
        if failed:
            return {"success": False, "failed_packages": failed, "report": report}

    return {"success": True, "report": report}


def phase_download_models(config: dict) -> dict:
    """阶段 3: 模型下载"""
    print("\n" + "=" * 50)
    print("  [阶段 3/6] 模型下载")
    print("=" * 50)

    from embedding_model_manager import download_model, list_downloaded_models

    # 需要下载的模型列表
    models_to_download = set()

    # 嵌入模型
    emb = config.get("embedding", {}).get("model_path", "")
    if emb:
        models_to_download.add(emb)

    # 路由回退模型
    if config.get("router", {}).get("enabled", True):
        fb = config.get("router", {}).get("model_path_fallback", "")
        if fb:
            models_to_download.add(fb)

    # Rerank 模型
    if config.get("reranker", {}).get("enabled", False):
        mode = config.get("reranker", {}).get("mode", "model")
        if mode in ("model", "hybrid"):
            rm = config.get("reranker", {}).get("model_path", "")
            if rm:
                models_to_download.add(rm)

    # 检查已下载
    existing = {m.get("model_id", "").lower() for m in list_downloaded_models()}
    to_dl = [m for m in models_to_download if m.lower() not in existing]

    results = {}
    for model_id in to_dl:
        print(f"\n  下载模型: {model_id}")
        try:
            r = download_model(model_id)
            results[model_id] = r.get("success", False)
            print(f"    {'[OK]' if results[model_id] else '[FAIL]'} {r.get('details', '')}")
        except Exception as e:
            results[model_id] = False
            print(f"    [FAIL] {e}")

    failed = [m for m, ok in results.items() if not ok]
    return {"success": len(failed) == 0, "results": results, "failed": failed}


def phase_create_kb(config: dict) -> dict:
    """阶段 4: 知识库创建"""
    print("\n" + "=" * 50)
    print("  [阶段 4/6] 知识库创建")
    print("=" * 50)

    from knowledge_base_manager import create_knowledge_base, list_knowledge_bases, set_classify_rule

    kbs = list_knowledge_bases()
    kb_name = config.get("kb", {}).get("active_kb", "default")
    results = {}

    # 默认知识库确保存在
    if kb_name not in kbs:
        print(f"  创建知识库: {kb_name}")
        ok, msg = create_knowledge_base(kb_name, config.get("kb", {}).get("description", ""))
        results["create"] = {"success": ok, "message": msg}
        print(f"    {'[OK]' if ok else '[FAIL]'} {msg}")

    return {"success": True, "results": results}


def phase_write_config(config: dict) -> dict:
    """阶段 5: 配置写入"""
    print("\n" + "=" * 50)
    print("  [阶段 5/6] 配置写入")
    print("=" * 50)

    from config import save_config, DEFAULT_CONFIG

    # 合并默认 + 用户配置
    full = dict(DEFAULT_CONFIG)
    for section, fields in config.items():
        if section in full and isinstance(full[section], dict):
            full[section].update(fields)
        else:
            full[section] = fields

    save_config(full)
    print("  [OK] 配置已写入 data/config/rag_config.json")
    return {"success": True, "config": full}


def phase_validate(config: dict) -> dict:
    """阶段 6: 验证"""
    print("\n" + "=" * 50)
    print("  [阶段 6/6] 验证")
    print("=" * 50)

    from config import load_config
    from embedding_model_manager import list_downloaded_models
    from knowledge_base_manager import list_knowledge_bases

    checks = {}

    # 1. Config 完整性
    cfg = load_config()
    all_keys = []
    for section, fields in CONFIG_SCHEMA.items():
        for key in fields:
            fq = f"{section}.{key}"
            val = cfg.get(section, {}).get(key, "__MISSING__")
            if val == "__MISSING__" and key != "value":
                all_keys.append((fq, "MISSING"))
            else:
                all_keys.append((fq, "OK"))
    missing = [k for k, s in all_keys if s == "MISSING"]
    checks["config_complete"] = len(missing) == 0
    if missing:
        print(f"  [WARN] 缺失参数: {', '.join(missing)}")
    else:
        print("  [OK] 32 参数完整")

    # 2. 模型就绪
    models = list_downloaded_models()
    model_ids = {m.get("model_id", "").lower() for m in models}
    needed = set()
    if config.get("embedding", {}).get("model_path", ""):
        needed.add(config["embedding"]["model_path"].lower())
    if config.get("router", {}).get("model_path_fallback", ""):
        needed.add(config["router"]["model_path_fallback"].lower())
    if config.get("reranker", {}).get("enabled", False):
        if config.get("reranker", {}).get("model_path", ""):
            needed.add(config["reranker"]["model_path"].lower())
    checks["models_ready"] = needed.issubset(model_ids)
    missing_models = needed - model_ids
    if missing_models:
        print(f"  [WARN] 模型未下载: {missing_models}")
    else:
        print("  [OK] 模型就绪")

    # 3. 知识库就绪
    kbs = list_knowledge_bases()
    kb_name = config.get("kb", {}).get("active_kb", "default")
    checks["kb_ready"] = kb_name in kbs
    if not checks["kb_ready"]:
        print(f"  [WARN] 知识库 '{kb_name}' 不存在")
    else:
        print(f"  [OK] 知识库 '{kb_name}' 就绪")

    all_ok = all(checks.values())
    print(f"\n  {'[OK] 全部验证通过' if all_ok else '[!] 部分验证失败'}")
    return {"success": all_ok, "checks": checks}


# ═══════════════════════════════════════════════════════════
# 4. 完整搭建入口
# ═══════════════════════════════════════════════════════════

def setup_rag(user_input: str, overrides: dict = None, mirror: str = "default") -> dict:
    """
    标准搭建入口——LLM 调用此函数，走完 6 阶段。

    参数:
        user_input: 用户的自然语言描述
        overrides:  可选覆盖（JSON dict），如 {"embedding": {"model_path": "..."}}
        mirror:     pip 镜像源

    返回:
        {
            "success": bool,
            "config": dict,
            "hook_report": {...},
            "pending_questions": [...],  # 需要 LLM 询问用户的参数
            "phases": {
                "env": {...},
                "models": {...},
                "kb": {...},
                "config": {...},
                "validate": {...},
            }
        }
    """
    # === 阶段 1: 参数采集 ===
    print("=" * 50)
    print("  [阶段 1/6] 参数采集")
    print("=" * 50)

    config, hook_report, need_ask = build_full_config(user_input, overrides)
    print(f"  自动填充: {len(hook_report['auto_filled'])} 项")
    for item in hook_report["auto_filled"]:
        print(f"    → {item}")
    if need_ask:
        print(f"  需询问用户 ({len(need_ask)} 项):")
        for p in need_ask:
            print(f"    ? {p}")
        return {
            "success": False,
            "config": config,
            "hook_report": hook_report,
            "pending_questions": need_ask,
            "phases": {},
            "error": f"缺少参数，需先询问用户: {', '.join(need_ask)}",
        }

    # === 阶段 2-6 ===
    phases = {}
    phases["env"] = phase_env_setup(mirror=mirror)
    if not phases["env"]["success"]:
        return {"success": False, "config": config, "hook_report": hook_report,
                "pending_questions": [], "phases": phases, "error": "环境安装失败"}

    phases["models"] = phase_download_models(config)

    phases["kb"] = phase_create_kb(config)

    phases["config"] = phase_write_config(config)

    phases["validate"] = phase_validate(config)

    success = all(p.get("success", False) for p in phases.values())

    print("\n" + "=" * 50)
    print(f"  RAG 搭建{'完成' if success else '失败'}")
    print("=" * 50)

    return {
        "success": success,
        "config": config,
        "hook_report": hook_report,
        "pending_questions": [],
        "phases": phases,
    }


# ═══════════════════════════════════════════════════════════
# 5. CLI 入口（供 LLM / 用户测试）
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RAG 标准化搭建编排器")
    parser.add_argument("--input", type=str, required=True, help="用户的自然语言搭建需求")
    parser.add_argument("--overrides", type=str, help="JSON 参数覆盖")
    parser.add_argument("--mirror", type=str, default="default", help="pip 镜像源")
    parser.add_argument("--schema", action="store_true", help="打印参数清单")
    parser.add_argument("--check-only", action="store_true", help="仅检查参数，不执行搭建")

    args = parser.parse_args()

    if args.schema:
        print(json.dumps(CONFIG_SCHEMA, ensure_ascii=False, indent=2))
        sys.exit(0)

    overrides = json.loads(args.overrides) if args.overrides else None

    if args.check_only:
        config, report, need_ask = build_full_config(args.input, overrides)
        print(json.dumps({
            "config": config,
            "hook_report": report,
            "pending_questions": need_ask,
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    result = setup_rag(args.input, overrides, mirror=args.mirror)
    print()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
