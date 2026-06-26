"""
公共工具模块
功能：配置加载、API 调用、配置保存
"""

import os
import json
import urllib.request
import urllib.error


def get_config_path():
    """获取配置文件路径"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(skill_dir, "config", "user_config.json")


def load_user_config():
    """
    加载用户配置文件。

    Returns:
        配置字典
    """
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        return {"api": {}, "last_used": {}}
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"api": {}, "last_used": {}}


def save_user_config(config):
    """
    保存用户配置。

    Args:
        config: 配置字典
    """
    config_path = get_config_path()
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_prompts():
    """
    加载 Prompt 模板。

    Returns:
        Prompt 字典
    """
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_path = os.path.join(skill_dir, "config", "prompts.json")
    
    with open(prompts_path, "r", encoding="utf-8") as f:
        return json.load(f)


def call_api(config: dict, model: str, messages: list) -> dict:
    """
    调用大模型 API。

    Args:
        config: 配置字典
        model: 模型名称
        messages: 消息列表

    Returns:
        API 响应 JSON

    Raises:
        Exception: API 调用失败时抛出异常
    """
    api_config = config.get("api", {})
    base_url = api_config.get("base_url")
    api_key = api_config.get("api_key")
    timeout = api_config.get("timeout", 60)
    
    if not base_url or not api_key:
        raise ValueError("API 配置不完整，请先运行配置")
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base_url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise Exception(f"API HTTP 错误 {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise Exception(f"网络连接失败: {e.reason}")
    except Exception as e:
        raise Exception(f"调用失败: {str(e)}")
