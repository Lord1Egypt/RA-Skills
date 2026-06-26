#!/usr/bin/env python3
"""
检查项定义 v1.0

定义13项内容质量检查项，按优先级分类：
- 核心（影响理解）：必须处理
- 完善（提升质量）：建议处理
- 优化（锦上添花）：可选处理
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict


class Priority(Enum):
    """检查项优先级"""
    CORE = "core"        # 核心建议（影响理解的关键项）
    IMPROVE = "improve"  # 完善建议（提升文档质量）
    OPTIMIZE = "optimize"  # 优化建议（锦上添花）


@dataclass
class CheckItem:
    """检查项定义"""
    id: str                    # 检查项ID，如 "C001"
    name: str                  # 检查项名称
    description: str           # 检查项描述
    priority: Priority         # 优先级
    target_sections: List[str] # 对应章节
    check_points: List[str]    # 检查要点（AI检查时关注的内容）
    example_good: str          # 良好示例
    example_bad: str           # 不良示例


# 13项检查定义
CHECK_ITEMS: Dict[str, CheckItem] = {
    # ============ 核心建议（2项）============
    "C001": CheckItem(
        id="C001",
        name="流程描述",
        description="是否有业务流程图或流程说明",
        priority=Priority.CORE,
        target_sections=["业务流程", "功能需求"],
        check_points=[
            "是否有流程图（Mermaid/图片）",
            "是否有文字描述的流程步骤",
            "流程是否有明确的开始和结束",
            "流程是否覆盖正常路径和异常路径"
        ],
        example_good="包含完整的业务流程图，使用Mermaid绘制，标注了正常流程和异常处理分支。",
        example_bad="仅有一句话描述'用户完成操作后系统处理'，无流程图。"
    ),
    "C002": CheckItem(
        id="C002",
        name="异常处理",
        description="异常场景和错误提示是否说明",
        priority=Priority.CORE,
        target_sections=["功能需求", "异常处理"],
        check_points=[
            "是否列出可能的异常场景",
            "是否有异常处理逻辑说明",
            "是否有错误提示文案",
            "是否说明异常后的状态（回滚/重试/终止）"
        ],
        example_good="定义了超时、网络失败、数据校验失败3种异常，每种异常有处理方式和提示文案。",
        example_bad="功能描述未提及任何异常情况。"
    ),

    # ============ 完善建议（7项）============
    "C003": CheckItem(
        id="C003",
        name="改造内容标注",
        description="新增/改造/优化内容是否清晰标注",
        priority=Priority.IMPROVE,
        target_sections=["全文"],
        check_points=[
            "是否标注了新增功能",
            "是否标注了改造功能",
            "是否标注了优化功能",
            "标注是否清晰可识别"
        ],
        example_good="每个功能点标注了【新增】【改造】【优化】标签。",
        example_bad="未标注功能类型，无法区分新旧功能。"
    ),
    "C004": CheckItem(
        id="C004",
        name="元素完整性",
        description="输入/输出/处理/界面元素是否完整",
        priority=Priority.IMPROVE,
        target_sections=["功能需求"],
        check_points=[
            "是否定义了输入字段（名称、类型、必填、校验规则）",
            "是否定义了输出字段（名称、类型、含义）",
            "是否说明了处理逻辑",
            "是否说明了界面元素（按钮、列表、表单）"
        ],
        example_good="输入：金额（数字，必填，>0），输出：订单号（字符串），处理：调用支付接口。",
        example_bad="只写了'用户输入金额后提交'，未说明输入校验和输出内容。"
    ),
    "C005": CheckItem(
        id="C005",
        name="交互逻辑",
        description="用户操作流程和系统响应逻辑是否清晰",
        priority=Priority.IMPROVE,
        target_sections=["功能需求"],
        check_points=[
            "是否说明了用户操作步骤",
            "是否说明了系统响应行为",
            "是否说明了前置条件",
            "是否说明了后置条件"
        ],
        example_good="用户点击'提交'→系统校验表单→调用后端接口→显示结果/错误提示。",
        example_bad="只写了'提交功能'，未说明交互过程。"
    ),
    "C006": CheckItem(
        id="C006",
        name="算法公式",
        description="计算逻辑、公式规则是否说明",
        priority=Priority.IMPROVE,
        target_sections=["功能需求"],
        check_points=[
            "是否说明了计算公式",
            "是否说明了参数含义",
            "是否说明了计算精度要求",
            "是否提供了计算示例"
        ],
        example_good="收益 = 本金 × 收益率 × 天数 / 365，精度保留2位小数。",
        example_bad="只写了'系统自动计算收益'，未说明计算方式。"
    ),
    "C007": CheckItem(
        id="C007",
        name="查询关联",
        description="数据查询逻辑、表关联关系是否说明",
        priority=Priority.IMPROVE,
        target_sections=["数据需求", "功能需求"],
        check_points=[
            "是否说明了查询条件",
            "是否说明了数据来源表",
            "是否说明了表关联关系",
            "是否说明了查询性能要求"
        ],
        example_good="查询用户持仓：从t_position表关联t_product表，按user_id过滤。",
        example_bad="只写了'查询用户持仓数据'，未说明数据来源。"
    ),
    "C008": CheckItem(
        id="C008",
        name="GWT验收标准",
        description="是否有Given-When-Then格式的验收标准",
        priority=Priority.IMPROVE,
        target_sections=["验收标准"],
        check_points=[
            "是否使用Given-When-Then格式",
            "Given是否描述了前置条件",
            "When是否描述了操作行为",
            "Then是否描述了预期结果"
        ],
        example_good="Given 用户已登录 When 用户点击'购买' Then 系统跳转到支付页面。",
        example_bad="验收标准只写了'功能正常'。"
    ),
    "C009": CheckItem(
        id="C009",
        name="系统对接描述",
        description="系统对接是否包含对接方、数据内容、频率、方式",
        priority=Priority.IMPROVE,
        target_sections=["系统对接", "接口设计"],
        check_points=[
            "是否说明了上游对接方（数据来源）",
            "是否说明了下游对接方（数据输出）",
            "是否说明了对接数据内容（字段、类型）",
            "是否说明了对接频率（实时/定时/批量）",
            "是否说明了对接方式（API/文件/MQ）",
            "是否说明了数据时效性（T+0/T+1）"
        ],
        example_good="上游对接核心系统，获取用户信息，API方式，实时调用，T+0。",
        example_bad="只写了'与核心系统对接'，未说明具体内容。"
    ),

    # ============ 优化建议（4项）============
    "C010": CheckItem(
        id="C010",
        name="分项描述",
        description="功能点是否拆分清晰",
        priority=Priority.OPTIMIZE,
        target_sections=["功能需求"],
        check_points=[
            "功能是否按模块拆分",
            "每个功能点是否有独立章节",
            "功能点之间是否有明确边界"
        ],
        example_good="功能拆分为：下单、支付、查询、退款4个独立章节。",
        example_bad="所有功能混在一个大段落中描述。"
    ),
    "C011": CheckItem(
        id="C011",
        name="界面细节",
        description="UI/UX说明、原型图是否完整",
        priority=Priority.OPTIMIZE,
        target_sections=["界面设计"],
        check_points=[
            "是否有界面原型图",
            "是否有UI元素说明",
            "是否有交互说明",
            "是否有样式规范"
        ],
        example_good="包含原型图、字段说明、交互说明、样式参考。",
        example_bad="无界面设计相关内容。"
    ),
    "C012": CheckItem(
        id="C012",
        name="改造类型",
        description="新增/改造/优化类型是否标注",
        priority=Priority.OPTIMIZE,
        target_sections=["全文"],
        check_points=[
            "是否标注了改造类型",
            "标注是否准确"
        ],
        example_good="明确标注了功能为【新增】或【改造】或【优化】。",
        example_bad="未标注改造类型。"
    ),
    "C013": CheckItem(
        id="C013",
        name="原型附件",
        description="是否有原型图或截图",
        priority=Priority.OPTIMIZE,
        target_sections=["界面设计", "附录"],
        check_points=[
            "是否有原型图附件",
            "是否有界面截图",
            "附件是否清晰可读"
        ],
        example_good="包含Figma原型链接和PNG截图。",
        example_bad="无原型附件。"
    )
}


def get_items_by_priority(priority: Priority) -> List[CheckItem]:
    """按优先级获取检查项"""
    return [item for item in CHECK_ITEMS.values() if item.priority == priority]


def get_items_for_section(section_name: str) -> List[CheckItem]:
    """获取适用于指定章节的检查项"""
    items = []
    for item in CHECK_ITEMS.values():
        # 检查章节名是否匹配
        for target in item.target_sections:
            if target in section_name or section_name in target:
                items.append(item)
                break
    return items


# 按优先级分组的检查项
CORE_ITEMS = get_items_by_priority(Priority.CORE)
IMPROVE_ITEMS = get_items_by_priority(Priority.IMPROVE)
OPTIMIZE_ITEMS = get_items_by_priority(Priority.OPTIMIZE)


if __name__ == "__main__":
    print("=" * 60)
    print("检查项定义")
    print("=" * 60)

    print(f"\n核心建议（{len(CORE_ITEMS)}项）：")
    for item in CORE_ITEMS:
        print(f"  - {item.id}: {item.name}")

    print(f"\n完善建议（{len(IMPROVE_ITEMS)}项）：")
    for item in IMPROVE_ITEMS:
        print(f"  - {item.id}: {item.name}")

    print(f"\n优化建议（{len(OPTIMIZE_ITEMS)}项）：")
    for item in OPTIMIZE_ITEMS:
        print(f"  - {item.id}: {item.name}")