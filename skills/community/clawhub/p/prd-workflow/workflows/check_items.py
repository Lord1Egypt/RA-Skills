#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 质量检查项数据

自动生成文件 - 请勿手动编辑
源文件：docs/checker.md
生成时间：2026-04-05 13:24:10
生成脚本：scripts/generate_check_items.py
"""

# 检查项数据
CHECK_ITEMS = [
  {
    "id": "CORE-1",
    "code": "CORE",
    "number": 1,
    "name": "业务规则完整性",
    "category": "CORE",
    "checkpoints": [
      "所有业务场景是否都有对应的处理规则",
      "规则之间是否存在冲突或矛盾",
      "规则是否有明确的优先级定义",
      "边界条件是否有明确定义"
    ],
    "questions": [
      "是否存在未定义处理规则的业务场景？",
      "不同规则之间是否存在逻辑冲突？",
      "当多个规则同时适用时，优先级如何确定？",
      "极端情况（最大值、最小值、空值）是否有处理规则？"
    ],
    "criteria": {}
  },
  {
    "id": "CORE-2",
    "code": "CORE",
    "number": 2,
    "name": "输入输出定义",
    "category": "CORE",
    "checkpoints": [
      "所有功能的输入参数是否有明确定义",
      "所有功能的输出结果是否有明确定义",
      "输入数据的格式、类型、范围是否有约束",
      "输出数据的格式、类型、范围是否有约束"
    ],
    "questions": [
      "每个功能模块的输入参数是否完整列出？",
      "每个功能模块的输出结果是否完整列出？",
      "输入数据的合法性校验规则是否明确？",
      "输出数据的格式规范是否明确？"
    ],
    "criteria": {}
  },
  {
    "id": "CORE-3",
    "code": "CORE",
    "number": 3,
    "name": "异常处理",
    "category": "CORE",
    "checkpoints": [
      "所有可能的异常情况是否有识别",
      "每种异常情况是否有对应的处理策略",
      "异常处理是否有用户友好的提示",
      "异常恢复机制是否有定义"
    ],
    "questions": [
      "是否识别了所有可能的异常情况（网络、数据、权限、系统等）？",
      "每种异常情况是否有明确的处理流程？",
      "用户看到的错误提示是否清晰、可理解？",
      "系统是否支持异常后的恢复操作？"
    ],
    "criteria": {}
  },
  {
    "id": "COMPLETE-1",
    "code": "COMPLETE",
    "number": 1,
    "name": "用户角色定义",
    "category": "COMPLETE",
    "checkpoints": [
      "所有用户角色是否有明确定义",
      "每个角色的权限范围是否清晰",
      "角色之间的关系是否有说明",
      "角色切换机制是否有定义"
    ],
    "questions": [
      "系统涉及哪些用户角色？",
      "每个角色可以执行哪些操作？",
      "不同角色之间的权限边界在哪里？",
      "用户是否可以切换角色？如何切换？"
    ],
    "criteria": {}
  },
  {
    "id": "COMPLETE-2",
    "code": "COMPLETE",
    "number": 2,
    "name": "业务流程覆盖",
    "category": "COMPLETE",
    "checkpoints": [
      "主流程是否有完整描述",
      "分支流程是否有完整描述",
      "流程之间的衔接是否清晰",
      "流程状态是否有明确定义"
    ],
    "questions": [
      "核心业务流程是否有完整的步骤描述？",
      "条件分支（if/else）是否有明确说明？",
      "不同流程之间如何切换和衔接？",
      "每个流程节点的状态是否明确？"
    ],
    "criteria": {}
  },
  {
    "id": "COMPLETE-3",
    "code": "COMPLETE",
    "number": 3,
    "name": "数据一致性",
    "category": "COMPLETE",
    "checkpoints": [
      "数据来源是否有明确说明",
      "数据存储方式是否有定义",
      "数据同步机制是否有说明",
      "数据冲突解决策略是否有定义"
    ],
    "questions": [
      "数据从哪里来？（数据库、API、用户输入）",
      "数据如何存储？（表结构、字段定义）",
      "多系统/多端数据如何保持同步？",
      "数据冲突时以哪个为准？"
    ],
    "criteria": {}
  },
  {
    "id": "COMPLETE-4",
    "code": "COMPLETE",
    "number": 4,
    "name": "接口定义完整性",
    "category": "COMPLETE",
    "checkpoints": [
      "所有外部接口是否有定义",
      "接口请求参数是否有说明",
      "接口响应格式是否有说明",
      "接口错误码是否有定义"
    ],
    "questions": [
      "系统需要调用哪些外部接口？",
      "每个接口的请求参数（名称、类型、必填）是否明确？",
      "每个接口的响应数据结构是否明确？",
      "接口错误码和错误信息是否有定义？"
    ],
    "criteria": {}
  },
  {
    "id": "COMPLETE-5",
    "code": "COMPLETE",
    "number": 5,
    "name": "验收标准可测性",
    "category": "COMPLETE",
    "checkpoints": [
      "每个功能是否有明确的验收标准",
      "验收标准是否可量化",
      "验收标准是否可执行",
      "验收标准是否有优先级"
    ],
    "questions": [
      "每个功能点是否有对应的验收标准？",
      "验收标准是否可以用数字或明确的是/否来判断？",
      "测试人员是否可以根据验收标准执行测试？",
      "验收标准的优先级是否明确（P0/P1/P2）？"
    ],
    "criteria": {}
  },
  {
    "id": "OPTIMIZE-1",
    "code": "OPTIMIZE",
    "number": 1,
    "name": "性能指标定义",
    "category": "OPTIMIZE",
    "checkpoints": [
      "关键操作是否有响应时间要求",
      "系统并发能力是否有定义",
      "数据处理量是否有预估",
      "性能优化策略是否有说明"
    ],
    "questions": [
      "关键操作的响应时间要求是多少？（如：页面加载 < 2s）",
      "系统需要支持多少并发用户？",
      "预计每天/每月处理多少数据量？",
      "有哪些性能优化策略？（缓存、异步、分页等）"
    ],
    "criteria": {}
  },
  {
    "id": "OPTIMIZE-2",
    "code": "OPTIMIZE",
    "number": 2,
    "name": "安全合规检查",
    "category": "OPTIMIZE",
    "checkpoints": [
      "敏感数据是否有加密说明",
      "权限验证是否有定义",
      "合规要求是否有说明",
      "审计日志是否有定义"
    ],
    "questions": [
      "敏感数据（密码、身份证号等）如何加密存储？",
      "权限验证在哪些环节执行？",
      "是否符合行业合规要求？（如金融、医疗）",
      "关键操作是否有日志记录？"
    ],
    "criteria": {}
  },
  {
    "id": "OPTIMIZE-3",
    "code": "OPTIMIZE",
    "number": 3,
    "name": "可扩展性设计",
    "category": "OPTIMIZE",
    "checkpoints": [
      "系统是否支持功能扩展",
      "配置是否支持动态调整",
      "架构是否支持水平扩展",
      "未来演进方向是否有说明"
    ],
    "questions": [
      "新增功能模块是否会影响现有功能？",
      "系统参数是否可以通过配置调整？",
      "系统是否支持增加服务器来提升性能？",
      "未来 1-3 年的演进方向是什么？"
    ],
    "criteria": {}
  },
  {
    "id": "OPTIMIZE-4",
    "code": "OPTIMIZE",
    "number": 4,
    "name": "用户体验优化",
    "category": "OPTIMIZE",
    "checkpoints": [
      "操作流程是否简洁",
      "界面反馈是否及时",
      "错误提示是否友好",
      "帮助文档是否有说明"
    ],
    "questions": [
      "用户完成核心任务需要多少步？",
      "操作后是否有明确的反馈？（成功/失败/加载中）",
      "错误提示是否告诉用户如何解决问题？",
      "是否有用户帮助文档或引导？"
    ],
    "criteria": {}
  },
  {
    "id": "OPTIMIZE-5",
    "code": "OPTIMIZE",
    "number": 5,
    "name": "监控告警设计",
    "category": "OPTIMIZE",
    "checkpoints": [
      "关键指标是否有监控",
      "异常情况是否有告警",
      "告警通知渠道是否有定义",
      "告警级别是否有分级"
    ],
    "questions": [
      "哪些关键指标需要监控？（CPU、内存、请求量等）",
      "什么情况下触发告警？",
      "告警通过什么渠道通知？（短信、邮件、钉钉）",
      "告警级别如何分级？（P0/P1/P2/P3）"
    ],
    "criteria": {}
  }
]


def get_all_items():
    """获取所有检查项"""
    return CHECK_ITEMS


def get_items_by_category(category_code):
    """
    按类别获取检查项
    
    Args:
        category_code: 类别代码 (CORE, COMPLETE, OPTIMIZE)
    
    Returns:
        list: 检查项列表
    """
    return [item for item in CHECK_ITEMS if item['code'] == category_code]


def get_item_by_id(item_id):
    """
    按 ID 获取检查项
    
    Args:
        item_id: 检查项 ID (如：CORE-1)
    
    Returns:
        dict: 检查项详情，不存在则返回 None
    """
    for item in CHECK_ITEMS:
        if item['id'] == item_id:
            return item
    return None


def get_items_for_stage(stage):
    """
    按阶段获取检查项
    
    Args:
        stage: 阶段名称 (decomposition, prd_generation, quality_check, optimization)
    
    Returns:
        list: 检查项列表
    """
    stage_mapping = {
        'decomposition': ['CORE'],
        'prd_generation': ['CORE', 'COMPLETE'],
        'quality_check': ['CORE', 'COMPLETE', 'OPTIMIZE'],
        'optimization': ['OPTIMIZE']
    }
    
    allowed_codes = stage_mapping.get(stage, ['CORE', 'COMPLETE', 'OPTIMIZE'])
    return [item for item in CHECK_ITEMS if item['code'] in allowed_codes]


def generate_prompt(stage):
    """
    生成阶段提示词
    
    Args:
        stage: 阶段名称
    
    Returns:
        str: 提示词字符串
    """
    items = get_items_for_stage(stage)
    
    if not items:
        return ''
    
    stage_names = {
        'decomposition': '需求分解阶段',
        'prd_generation': 'PRD 生成阶段',
        'quality_check': '质量检查阶段',
        'optimization': '优化建议阶段'
    }
    
    prompt = f"## {stage_names.get(stage, stage)} - 质量检查项指导\n\n"
    prompt += f"请在{stage_names.get(stage, stage)}中，重点关注以下检查项：\n\n"
    
    # 按类别分组
    grouped = {}
    for item in items:
        code = item['code']
        if code not in grouped:
            grouped[code] = []
        grouped[code].append(item)
    
    category_names = {
        'CORE': '🔴 核心检查项（必须满足）',
        'COMPLETE': '🟡 完善检查项（建议满足）',
        'OPTIMIZE': '🟢 优化检查项（可选满足）'
    }
    
    for code in ['CORE', 'COMPLETE', 'OPTIMIZE']:
        if code not in grouped:
            continue
        
        prompt += f"### {category_names.get(code, code)}\n\n"
        
        for item in grouped[code]:
            prompt += f"#### {item['id']}: {item['name']}\n\n"
            
            if item['checkpoints']:
                prompt += '**检查点**:\n'
                for cp in item['checkpoints']:
                    prompt += f"- {cp}\n"
                prompt += '\n'
            
            if item['questions']:
                prompt += '**关键问题**:\n'
                for idx, q in enumerate(item['questions'], 1):
                    prompt += f"{idx}. {q}\n"
                prompt += '\n'
            
            if item['criteria']:
                prompt += '**验收标准**:\n'
                for key, value in item['criteria'].items():
                    prompt += f"- {key}: {value}\n"
                prompt += '\n'
    
    prompt += "---\n\n"
    prompt += "**使用说明**:\n"
    prompt += "- 核心检查项（CORE）必须 100% 满足，否则 PRD 质量不达标\n"
    prompt += "- 完善检查项（COMPLETE）建议满足 80% 以上\n"
    prompt += "- 优化检查项（OPTIMIZE）根据项目实际情况选择性满足\n"
    
    return prompt


def get_stats():
    """
    获取检查项统计信息
    
    Returns:
        dict: 统计信息
    """
    stats = {
        'total': len(CHECK_ITEMS),
        'by_category': {},
        'total_checkpoints': 0,
        'total_questions': 0
    }
    
    for item in CHECK_ITEMS:
        code = item['code']
        if code not in stats['by_category']:
            stats['by_category'][code] = 0
        stats['by_category'][code] += 1
        stats['total_checkpoints'] += len(item['checkpoints'])
        stats['total_questions'] += len(item['questions'])
    
    return stats


if __name__ == '__main__':
    # 测试代码
    print("PRD 质量检查项数据")
    print("=" * 50)
    
    stats = get_stats()
    print(f"总检查项数：{stats['total']}")
    print(f"按类别统计：{stats['by_category']}")
    print(f"总检查点数：{stats['total_checkpoints']}")
    print(f"总问题数：{stats['total_questions']}")
    
    print("\n示例：CORE-1 详情")
    item = get_item_by_id('CORE-1')
    if item:
        print(f"名称：{item['name']}")
        print(f"检查点数：{len(item['checkpoints'])}")
        print(f"问题数：{len(item['questions'])}")
