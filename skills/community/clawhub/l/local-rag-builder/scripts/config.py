"""
local-rag-builder 配置管理模块
v0.1.0
"""

import os
import sys
from utils import cfg_dir, safe_json_load, safe_json_dump

DEFAULT_CONFIG = {
    "mode": "integrated",
    "input_sources": {
        "enable_pdf": False,
        "enable_ocr": False,
        "enable_html2md": False,
        "pdf_backend": "pypdf",  # pypdf / pdfplumber
    },
    "splitting": {
        "strategy": "recursive",
        "chunk_size": 500,
        "chunk_overlap": 50,
        "separators": ["\n\n", "\n", "。", "；", "，", " ", ""],
        "headers_to_split_on": [["#", "h1"], ["##", "h2"], ["###", "h3"]],
        "strip_headers": False,
        "semantic_breakpoint": "percentile",
        "secondary_strategy": None,
        "guards": ["code"],
        "strategy_overrides": {
            "headers": {"chunk_size": None, "chunk_overlap": None},
            "semantic": {"chunk_size": None, "chunk_overlap": None},
            "sentence": {"chunk_size": None, "chunk_overlap": None},
        },
    },
    "retrieval": {
        "k": 3,
        "score_threshold": None,
        "search_type": "similarity",
    },
    "llm": {
        "base_url": "http://localhost:1234/v1",
        "api_key": "not-needed",
        "temperature": 0.1,
        "max_tokens": 512,
        "model_name": "",
    },
    "kb": {
        "active_kb": "default",
        "auto_classify": False,
    },
    "prompt": {
        "template_file": "default_template.txt",
    },
}


def get_config_path():
    return os.path.join(cfg_dir, "rag_config.json")


def load_config():
    """加载配置，不存在则返回默认"""
    cfg = safe_json_load(get_config_path())
    if cfg is None:
        return DEFAULT_CONFIG.copy()
    # 合并缺失的默认字段（兼容顶层非 dict 字段）
    merged = DEFAULT_CONFIG.copy()
    if isinstance(cfg, dict):
        for k, v in cfg.items():
            if k in DEFAULT_CONFIG and isinstance(DEFAULT_CONFIG[k], dict) and isinstance(v, dict):
                merged[k].update(v)
                # 补全子字段
                for sk, sv in DEFAULT_CONFIG[k].items():
                    if sk not in v:
                        merged[k][sk] = sv
            else:
                merged[k] = v
    return merged


def save_config(cfg):
    """保存配置"""
    try:
        safe_json_dump(cfg, get_config_path())
        return True
    except (OSError, IOError) as e:
        return False


def get_section(section_name):
    """获取配置中的某个 section"""
    try:
        cfg = load_config()
        return cfg.get(section_name, DEFAULT_CONFIG.get(section_name, {}))
    except Exception:
        return DEFAULT_CONFIG.get(section_name, {})


def update_section(section_name, updates):
    """更新配置中的某个 section"""
    try:
        cfg = load_config()
        if section_name not in cfg:
            cfg[section_name] = {}
        cfg[section_name].update(updates)
        save_config(cfg)
        return cfg[section_name]
    except (OSError, IOError, KeyError) as e:
        return DEFAULT_CONFIG.get(section_name, {})


def reset_config():
    """重置为默认配置"""
    save_config(DEFAULT_CONFIG.copy())
    return DEFAULT_CONFIG.copy()
