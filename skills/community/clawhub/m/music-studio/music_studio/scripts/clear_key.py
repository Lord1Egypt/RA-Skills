"""clear-key 命令：从 config.json 移除本地保存的 API Key"""

from music_studio import config


def main(_=None):
    cfg = config.load_config()
    if not cfg.get("api_key"):
        print("ℹ️ config.json 中没有保存的 API Key")
        return
    config.remove_keys("api_key")
    print(f"✅ 已从 {config.CONFIG_FILE} 移除 API Key")
