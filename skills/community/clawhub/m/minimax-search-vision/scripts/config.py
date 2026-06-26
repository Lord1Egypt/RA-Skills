"""
配置模块 - 安全加载 MiniMax API 凭据

安全规范 (2026-03-21)：
- 禁止硬编码 API Key
- 从环境变量或 credentials 目录加载凭据
- 输出时脱敏处理
"""

import os
from pathlib import Path


# 凭据文件路径
CREDENTIALS_DIR = Path.home() / ".openclaw" / "credentials"
CREDENTIAL_FILE = CREDENTIALS_DIR / "minimax_mcp.env"


def load_env_file(filepath: Path) -> dict:
    """从 .env 文件加载环境变量"""
    env_vars = {}
    if filepath.exists():
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    return env_vars


def get_api_key() -> str:
    """
    获取 MiniMax API Key
    
    优先级：
    1. 环境变量 MINIMAX_API_KEY
    2. 凭据文件 ~/.openclaw/credentials/minimax_mcp.env
    
    Returns:
        str: API Key
        
    Raises:
        ValueError: 当无法找到 API Key 时
    """
    # 首先检查环境变量
    api_key = os.environ.get('MINIMAX_API_KEY')
    
    if not api_key:
        # 从凭据文件加载
        env_vars = load_env_file(CREDENTIAL_FILE)
        api_key = env_vars.get('MINIMAX_API_KEY')
    
    if not api_key:
        raise ValueError(
            f"未找到 MiniMax API Key。\n"
            f"请确保在以下位置配置了 API Key：\n"
            f"1. 环境变量 MINIMAX_API_KEY\n"
            f"2. 文件 {CREDENTIAL_FILE}"
        )
    
    return api_key


def masked_key(key: str = None) -> str:
    """
    脱敏 API Key 用于日志输出
    
    Args:
        key: API Key，如果不提供则自动获取
        
    Returns:
        str: 脱敏后的 Key，格式如 sk-cp-rOHr...****
    """
    if key is None:
        key = get_api_key()
    
    if not key:
        return "(not set)"
    
    # 显示前8位和后4位，中间用****遮挡
    if len(key) <= 12:
        return f"{key[:4]}****"
    
    return f"{key[:8]}****{key[-4:]}"


def get_api_host() -> str:
    """获取 MiniMax API Host"""
    host = os.environ.get('MINIMAX_API_HOST', 'https://api.minimaxi.com')
    return host


if __name__ == "__main__":
    # 测试配置加载
    try:
        key = get_api_key()
        print(f"API Key: {masked_key(key)}")
        print(f"API Host: {get_api_host()}")
    except ValueError as e:
        print(f"错误: {e}")
