"""
Longbridge API 共享配置模块

提供配置文件查找和加载功能，供所有脚本使用。
"""

import os


def find_config_file(script_dir=None):
    """
    查找配置文件（支持多种路径）

    优先级：
    1. 环境变量 LONGBRIDGE_CONFIG
    2. 相对于脚本/技能目录的路径
    3. 用户主目录的通用位置

    Args:
        script_dir: 脚本所在目录（可选，自动检测）

    Returns:
        配置文件路径，如果未找到返回 None
    """
    # 1. 环境变量指定（最高优先级）
    env_config = os.getenv('LONGBRIDGE_CONFIG')
    if env_config and os.path.exists(env_config):
        return env_config

    # 确定脚本目录
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        script_dir = os.path.abspath(script_dir)

    # 2. 相对路径：从脚本位置往上查找
    possible_paths = [
        # 和脚本同级（skill 目录）
        os.path.join(script_dir, '../.longbridge_config'),
        os.path.join(script_dir, '.longbridge_config'),
        # workspace 根目录
        os.path.join(script_dir, '../../.longbridge_config'),
        os.path.join(script_dir, '../../../.longbridge_config'),
        # config/secrets 目录（如果使用 workspace 结构）
        os.path.join(script_dir, '../../../config/secrets/.longbridge_config'),
        os.path.join(script_dir, '../../../.longbridge_config'),
    ]

    # 3. 用户主目录的通用位置
    possible_paths.extend([
        os.path.expanduser('~/.longbridge_config'),
        os.path.expanduser('~/.config/longbridge/.longbridge_config'),
        os.path.expanduser('~/.longbridge/longbridge_config'),
    ])

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None  # 未找到


def load_config(config_path):
    """
    从配置文件加载配置

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典，如果失败返回 None
    """
    if not config_path or not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        return None

    config = {}
    try:
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 解析 key=value
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return None

    # 检查必需字段
    required = ['LONGPORT_APP_KEY', 'LONGPORT_APP_SECRET', 'LONGPORT_ACCESS_TOKEN']
    for key in required:
        if key not in config:
            print(f"❌ 配置文件缺少: {key}")
            return None

    return config


def show_config_help(config_path=None):
    """
    显示配置文件帮助信息

    Args:
        config_path: 尝试使用的配置路径（用于错误提示）
    """
    if config_path:
        print(f"❌ 配置文件不存在: {config_path}")
    else:
        print("❌ 未找到配置文件")

    print("\n请创建配置文件，包含以下内容：")
    print("───")
    print("LONGPORT_APP_KEY=<你的App Key>")
    print("LONGPORT_APP_SECRET=<你的App Secret>")
    print("LONGPORT_ACCESS_TOKEN=<你的Access Token>")
    print("LONGPORT_REGION=cn")
    print("LONGPORT_HTTP_URL=https://openapi.longportapp.cn")
    print("LONGPORT_QUOTE_WS_URL=wss://openapi-quote.longportapp.cn")
    print("LONGPORT_TRADE_WS_URL=wss://openapi-trade.longportapp.cn")
    print("───")

    print("\n配置文件可以放在以下位置之一：")
    print("  1. 环境变量指定的路径: export LONGBRIDGE_CONFIG=/path/to/config")
    print("  2. 技能目录: <skill-dir>/.longbridge_config")
    print("  3. 用户主目录: ~/.longbridge_config")

    print("\n获取凭证: https://open.longport.com/")
