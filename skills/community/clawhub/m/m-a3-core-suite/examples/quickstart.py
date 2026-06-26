"""
M-A3 Core Suite — 快速开始示例

Usage:
    cd skills/m-a3-core-suite
    python examples/quickstart.py
"""

import sys
from pathlib import Path

# 添加父目录到路径（支持直接运行）
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.chief_of_staff import ChiefOfStaff


def main():
    print("=" * 60)
    print("M-A3 Core Suite — 快速开始")
    print("=" * 60)

    chief = ChiefOfStaff()

    # 测试用例
    test_cases = [
        {
            "task": "帮我分析北美家具市场的GEO运营机会，我们是做家具出口的",
            "brand": "FurnitureExport",
        },
        {
            "task": "原材料涨价，帮我调整采购策略",
            "brand": "PlasticFactory",
        },
        {
            "task": "优化这个亚马逊Listing：标题太长，五点没数据",
            "brand": "AmazonStore",
        },
        {
            "task": "让另一个Agent帮我分析竞品，我们专注内容创作",
            "brand": "ContentFirst",
        },
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'─' * 50}")
        print(f"📋 测试 {i}：{tc['task'][:35]}...")
        print(f"   品牌：{tc['brand']}")

        result = chief.execute(tc["task"], tc["brand"])

        print(f"\n   ✅ 任务类型：{result['classification']['type']}")
        print(f"   ✅ 复杂度：{result['classification']['complexity']}")
        print(f"   ✅ 执行 Agent：{result['execution_plan']['primary_agent']}")
        print(f"   ✅ Agent 角色：{result['execution_plan']['primary_agent_role']}")
        print(f"   ✅ 能力列表：{', '.join(result['execution_plan']['capabilities_used'][:3])}...")

    print(f"\n{'=' * 60}")
    print("🎉 快速开始测试完成！")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
