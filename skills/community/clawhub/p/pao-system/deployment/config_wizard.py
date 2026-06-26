"""PAO系统配置向导"""
import json
from pathlib import Path


class ConfigWizard:
    def __init__(self):
        self.config_path = Path.home() / ".config" / "pao" / "config.json"
        self.config = {
            "device_name": "PAO-Device",
            "port": 8080,
            "encryption": True,
            "auto_sync": True,
            "sync_interval": 60
        }

    def run(self):
        """运行配置向导"""
        print("⚙️ PAO系统配置向导")
        print("=" * 50)

        # 设备名称
        device_name = input(f"设备名称 [{self.config['device_name']}]: ").strip()
        if device_name:
            self.config["device_name"] = device_name

        # 端口
        port = input(f"通信端口 [{self.config['port']}]: ").strip()
        if port and port.isdigit():
            self.config["port"] = int(port)

        # 加密
        encryption = input("启用加密 (y/n) [y]: ").strip().lower()
        self.config["encryption"] = encryption != "n"

        # 自动同步
        auto_sync = input("启用自动同步 (y/n) [y]: ").strip().lower()
        self.config["auto_sync"] = auto_sync != "n"

        # 保存配置
        self._save_config()
        print("✅ 配置已保存!")

    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)


if __name__ == "__main__":
    wizard = ConfigWizard()
    wizard.run()
