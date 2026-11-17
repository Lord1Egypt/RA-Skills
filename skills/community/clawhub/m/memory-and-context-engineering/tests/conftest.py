"""公共测试夹具

运行说明：本测试集不依赖真实 Redis（RedisAdapter 使用内存降级模式）。
pytest 为开发期工具，不属于运行时依赖，按需安装: pip install pytest
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture()
def degraded_redis():
    """返回处于内存降级模式的 RedisAdapter（本环境无真实 Redis）"""
    from scripts.redis_adapter import RedisAdapter, RedisConfig

    config = RedisConfig(
        host="127.0.0.1",
        port=6390,  # 无服务端口，快速失败进入降级
        socket_connect_timeout=1,
        socket_timeout=1,
    )
    return RedisAdapter(config, enable_memory_fallback=True, memory_max_entries=100)


class MockEventBus:
    """可记录事件的简易事件总线"""

    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)
