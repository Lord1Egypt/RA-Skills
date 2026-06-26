"""unit 阶段特化 fixture。

核心职责：把 config 模块的全局路径常量（指向 ~/.commit-logs/）重定向到
临时目录，确保单元测试绝不读写真实用户目录。
"""

import pytest


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """将 config 模块的全局路径常量重定向到 tmp_path。

    config 内部函数直接引用模块级 DEFAULT_* 常量，故必须 patch 模块属性，
    返回临时配置目录供测试断言。
    """
    import config

    cfg_dir = tmp_path / ".commit-logs"
    monkeypatch.setattr(config, "DEFAULT_CONFIG_DIR", cfg_dir)
    monkeypatch.setattr(config, "DEFAULT_CONFIG_PATH", cfg_dir / "config.toml")
    monkeypatch.setattr(config, "DEFAULT_LABELS_PATH", cfg_dir / "labels.json")
    return cfg_dir
