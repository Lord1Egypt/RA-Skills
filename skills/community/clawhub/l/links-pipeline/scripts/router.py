#!/usr/bin/env python3
"""内容路由：识别主题 → 匹配 config.yaml → 入库"""
import sys, json, yaml
from pathlib import Path

def load_config():
    """加载路由配置"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        return yaml.safe_load(config_path.read_text())
    return None

def identify_topic(text: str) -> str:
    """基于关键词匹配识别内容主题"""
    text_lower = text.lower()
    config = load_config()
    if not config:
        return None
    
    for rule in config["routing"]["rules"]:
        for topic in rule["topics"]:
            if topic.lower() in text_lower:
                return rule["target"]
    
    # fallback
    if config["routing"].get("fallback") == "ask":
        return None
    return config["routing"].get("fallback_target", "未分类/")

def route(text: str, source_type: str, source_info: dict) -> dict:
    """路由决策：返回目标路径"""
    target = identify_topic(text)
    
    result = {
        "source_type": source_type,
        "source_info": source_info,
        "target": target,
        "chars": len(text),
        "determined": target is not None
    }
    
    if target:
        result["message"] = f"自动识别为 → {target}"
    else:
        result["message"] = "无法确定归属，需要人工确认"
    
    return result

if __name__ == "__main__":
    text = sys.stdin.read()
    source_type = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    result = route(text, source_type, {"url": sys.argv[2] if len(sys.argv) > 2 else ""})
    print(json.dumps(result, ensure_ascii=False, indent=2))
