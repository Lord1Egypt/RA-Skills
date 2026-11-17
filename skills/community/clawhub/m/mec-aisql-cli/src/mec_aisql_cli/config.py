"""配置管理模块

本模块管理 mec-aisql-cli 的持久化配置, 存储在 ``~/.minglue/aisql_config.json``。

== AI Bot 使用指南 ==

配置用于预设默认参数, 避免每次命令都传入 --client/--brand 等参数。
参数优先级: **命令行参数 > 配置文件 > 内置默认值**

配置项:

    =================  ============================================= ==============================
    配置项             说明                                           默认值
    =================  ============================================= ==============================
    base_url           API 地址                                       https://mec.miaozhen.com/taskmng
    model              AI 模型                                        mlamp/deepseek-v4-flash
    client             默认客户名称                                    (空)
    brand              默认品牌名称                                    (空)
    datafrom           默认数据来源 (ADM/OTT-OM/...)                   (空)
    contype            默认分析类型                                    (空)
    datetimefw         默认时间范围                                    (空)
    timeout            HTTP 请求超时秒数                                120
    max_retries        最大重试次数                                    2
    =================  ============================================= ==============================

管理命令:
    - ``mec-aisql config``          查看全部配置
    - ``mec-aisql config --get X``  查看单个配置项
    - ``mec-aisql config-set --key X --value Y``  设置配置项
    - ``mec-aisql config-reset``    重置全部配置
"""
import json
import os
from typing import Any, Dict, Optional

# 配置文件路径: ~/.minglue/aisql_config.json
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.minglue")
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_DIR, "aisql_config.json")


class Config:
    """持久化配置管理

    配置存储在 ``~/.minglue/aisql_config.json``, 首次使用时自动创建。

    使用方式::

        cfg = Config()
        client = cfg.get("client", "")       # 读取配置
        cfg.set("client", "客户A")           # 写入配置 (自动持久化)
        cfg.unset("client")                  # 重置为默认值
        all_cfg = cfg.all()                  # 获取全部配置
        kwargs = cfg.as_api_kwargs()         # 获取 API 客户端初始化参数
    """

    # 内置默认值: 首次使用或重置时使用
    DEFAULTS = {
        "base_url": "https://mec.miaozhen.com/taskmng",
        "model": "mlamp/deepseek-v4-flash",
        "client": "",
        "brand": "",
        "datafrom": "",
        "contype": "",
        "datetimefw": "",
        "timeout": 120,
        "max_retries": 2,
    }

    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器

        Args:
            config_path: 自定义配置文件路径 (默认 ~/.minglue/aisql_config.json)
        """
        self._path = config_path or DEFAULT_CONFIG_PATH
        self._data = dict(self.DEFAULTS)  # 先填充默认值
        self._load()  # 再从文件加载用户配置 (覆盖默认值)

    def _load(self):
        """从文件加载配置 (文件不存在时使用默认值)"""
        if os.path.exists(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                self._data.update(user_data)  # 用户配置覆盖默认值
            except (json.JSONDecodeError, IOError):
                pass  # 配置文件损坏时静默使用默认值

    def _save(self):
        """保存配置到文件 (自动创建目录)"""
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项的值

        Args:
            key:     配置项名称 (如 "client" / "base_url")
            default: 配置项不存在时的默认返回值
        Returns:
            配置值, 如不存在则返回 default
        """
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        """设置配置项的值并持久化

        Args:
            key:   配置项名称
            value: 配置值
        """
        self._data[key] = value
        self._save()

    def unset(self, key: str):
        """重置配置项为默认值

        Args:
            key: 配置项名称
        """
        if key in self._data:
            self._data[key] = self.DEFAULTS.get(key)
            self._save()

    def all(self) -> Dict[str, Any]:
        """获取全部配置

        Returns:
            包含所有配置项的字典
        """
        return dict(self._data)

    def as_api_kwargs(self) -> Dict[str, Any]:
        """获取 AisqlApiClient 初始化所需的参数

        Returns:
            {"base_url": ..., "timeout": ..., "max_retries": ...}
        """
        return {
            "base_url": self._data.get("base_url", self.DEFAULTS["base_url"]),
            "timeout": self._data.get("timeout", self.DEFAULTS["timeout"]),
            "max_retries": self._data.get("max_retries", self.DEFAULTS["max_retries"]),
        }
