"""set-key 命令：显式保存 API Key 到 config.json"""

import getpass
import sys
from music_studio import config, providers


def _validate_api_key(api_key: str, provider: str) -> bool:
    try:
        client = providers.get_api_client(api_key, provider)
        client.lyrics_generation(prompt="test")
        return True
    except Exception:
        return False


def main(_=None):
    provider = config.get_provider()
    print("=== 保存 API Key 到 config.json ===\n")
    if not sys.stdin.isatty():
        print("❌ 未读取到 API Key（需要交互式终端）")
        return
    try:
        api_key = getpass.getpass("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("❌ 未读取到 API Key（需要交互式终端）")
        return
    except Exception:
        try:
            api_key = input("> ").strip()
        except Exception:
            print("❌ 无法读取 API Key（请在交互式终端运行）")
            return
    if not api_key:
        print("❌ API Key 不能为空")
        return

    print("🔑 正在校验 API Key...")
    if not _validate_api_key(api_key, provider):
        print("❌ API Key 验证失败")
        return

    config.update_config({"api_key": api_key})
    print(f"✅ 已保存到: {config.CONFIG_FILE}")
