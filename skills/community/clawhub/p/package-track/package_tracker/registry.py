"""根据配置或环境选择供应商，支持 JSON 配置与默认供应商。"""

from typing import Any

from package_tracker.base import BaseTracker
from package_tracker.config import get_provider_options, load_config
from package_tracker.kdniao import KdniaoTracker


def get_tracker(
    provider: str | None = None,
    config_path: str | None = None,
    **kwargs: Any,
) -> BaseTracker:
    """
    返回一个 tracker 实例。

    :param provider: 指定供应商名称；不传则使用配置文件中的 default，若无配置则为 kdniao。
    :param config_path: 指定配置文件路径；不传则使用当前目录下的 package_tracker.json（如存在），否则使用默认配置。
    :param kwargs: 传给供应商构造函数的参数，会覆盖配置文件中的同名字段。
    """
    config = load_config(force_path=config_path, use_cache=(config_path is None))
    name = (provider or config.get("default") or "kdniao").strip().lower()
    options = get_provider_options(name, config)
    # 合并：配置 < 传入的 kwargs
    merged = {**options, **kwargs}
    if name == "kdniao":
        return KdniaoTracker(**merged)
    raise ValueError(f"Unknown provider: {name}. Supported: kdniao")

