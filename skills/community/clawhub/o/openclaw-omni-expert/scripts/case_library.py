#!/usr/bin/env python3
"""
OpenClaw 案例库
THE CASE LIBRARY - 100+ 实战案例与最佳实践

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

涵盖：
1. 客服机器人
2. 数据分析助手
3. 自动化办公
4. 内容创作
5. 开发助手
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# =============================================================================
# 案例分类
# =============================================================================

class CaseCategory(Enum):
    """案例分类"""
    CUSTOMER_SERVICE = "customer_service"      # 客服机器人
    DATA_ANALYSIS = "data_analysis"            # 数据分析
    OFFICE_AUTOMATION = "office_automation"    # 自动化办公
    CONTENT_CREATION = "content_creation"      # 内容创作
    DEVELOPMENT = "development"                # 开发助手
    KNOWLEDGE_BASE = "knowledge_base"          # 知识库问答
    SALES = "sales"                            # 销售助手
    HR = "hr"                                  # HR 助手


# =============================================================================
# 案例库
# =============================================================================

class CaseLibrary:
    """完整案例库 - 100+ 实战案例"""

    # ========== 客服机器人案例 ==========
    CUSTOMER_SERVICE_CASES = {
        "case_001": {
            "id": "case_001",
            "name": "电商客服机器人",
            "category": "customer_service",
            "difficulty": "medium",
            "description": "为电商平台构建智能客服，处理订单查询、退换货、投诉等问题",
            "scenario": """
一家中型电商平台，日均咨询量 500+，需要 7x24 小时客服支持。

痛点：
- 人工客服成本高
- 夜间咨询无人响应
- 常见问题重复回答
- 客户等待时间长
            """,
            "solution": {
                "architecture": "intent_routing",
                "workflow": [
                    {"id": "input", "type": "input"},
                    {"id": "classify", "type": "llm", "config": {
                        "prompt": "识别用户意图：{{message}}",
                        "system_prompt": "你是一个客服意图分类器，输出 JSON: {\"intent\": \"...\", \"entities\": {...}}"
                    }},
                    {"id": "router", "type": "condition"},
                    {"id": "order_query", "type": "tool", "config": {"tool": "db_query"}},
                    {"id": "refund", "type": "tool", "config": {"tool": "refund_api"}},
                    {"id": "transfer_human", "type": "action", "config": {"operation": "notify_human"}},
                    {"id": "output", "type": "output"}
                ],
                "tools": ["db_query", "refund_api", "order_track", "product_search", "send_email"],
                "memory": {"type": "vector", "provider": "chroma"}
            },
            "configuration": {
                "model": {"provider": "openai", "model": "gpt-4o-mini"},
                "channels": [{"type": "telegram"}, {"type": "webchat"}],
                "intents": ["order_query", "refund", "complaint", "product_info", "tracking", "transfer"]
            },
            "metrics": {
                "resolution_rate": 0.85,
                "avg_response_time": "3s",
                "customer_satisfaction": 4.5
            },
            "code_example": {
                "agent_config": '''
{
  "name": "ecommerce_customer_bot",
  "type": "agent",
  "config": {
    "model": "gpt-4o-mini",
    "intents": ["order_query", "refund", "complaint"],
    "fallback_intent": "transfer_human",
    "tools": ["db_query", "refund_api"]
  }
}
'''
            }
        },
        "case_002": {
            "id": "case_002",
            "name": "技术支持工单系统",
            "category": "customer_service",
            "difficulty": "high",
            "description": "企业 IT 支持工单系统，自动分类、转派、处理常见技术问题"
        },
        "case_003": {
            "id": "case_003",
            "name": "保险理赔咨询",
            "category": "customer_service",
            "difficulty": "medium",
            "description": "保险理赔流程咨询，自动指导用户准备材料"
        }
    }

    # ========== 数据分析案例 ==========
    DATA_ANALYSIS_CASES = {
        "case_101": {
            "id": "case_101",
            "name": "销售数据分析仪表盘",
            "category": "data_analysis",
            "difficulty": "medium",
            "description": "自动从数据库提取销售数据，生成可视化报告和趋势分析",
            "scenario": """
销售团队每周需要手动汇总数据，耗时 4+ 小时。

功能需求：
- 自动提取销售数据
- 计算 KPI 指标
- 生成趋势图表
- 异常预警
- 自动发送周报
            """,
            "solution": {
                "architecture": "data_pipeline",
                "workflow": [
                    {"id": "schedule", "type": "trigger", "config": {"cron": "0 9 * * 1"}},
                    {"id": "extract", "type": "tool", "config": {"tool": "db_query"}},
                    {"id": "transform", "type": "action", "config": {"operation": "aggregate"}},
                    {"id": "analyze", "type": "llm", "config": {
                        "prompt": "分析以下销售数据，识别趋势和异常：{{data}}"
                    }},
                    {"id": "generate_report", "type": "action", "config": {"operation": "render_chart"}},
                    {"id": "send", "type": "tool", "config": {"tool": "send_email"}}
                ]
            },
            "code_example": {
                "workflow_config": '''
{
  "name": "sales_analytics_pipeline",
  "type": "workflow",
  "schedule": "0 9 * * 1",
  "nodes": [
    {"id": "extract", "type": "tool", "tool": "db_query"},
    {"id": "analyze", "type": "llm"},
    {"id": "report", "type": "action"},
    {"id": "notify", "type": "tool", "tool": "send_email"}
  ]
}
'''
            }
        },
        "case_102": {
            "id": "case_102",
            "name": "用户行为分析",
            "category": "data_analysis",
            "difficulty": "high",
            "description": "分析用户行为数据，识别用户画像和流失风险"
        },
        "case_103": {
            "id": "case_103",
            "name": "竞品监控分析",
            "category": "data_analysis",
            "difficulty": "medium",
            "description": "自动抓取竞品信息，分析市场动态"
        }
    }

    # ========== 自动化办公案例 ==========
    OFFICE_AUTOMATION_CASES = {
        "case_201": {
            "id": "case_201",
            "name": "会议纪要助手",
            "category": "office_automation",
            "difficulty": "easy",
            "description": "自动生成会议纪要，提取待办事项，发送参与人",
            "scenario": """
团队每周 10+ 个会议，手动整理纪要耗时且容易遗漏。

功能：
- 语音转文字（录音转录）
- 自动提取关键信息
- 生成结构化纪要
- 识别待办事项
- 一键发送
            """,
            "solution": {
                "architecture": "transcription_pipeline",
                "workflow": [
                    {"id": "input", "type": "input"},
                    {"id": "transcribe", "type": "tool", "config": {"tool": "whisper_api"}},
                    {"id": "summarize", "type": "llm", "config": {
                        "prompt": "为以下会议内容生成结构化纪要：\n{{transcript}}\n\n格式要求：\n1. 会议概要\n2. 讨论要点\n3. 决策事项\n4. 待办事项（负责人+截止日期）"
                    }},
                    {"id": "extract_action", "type": "llm", "config": {
                        "prompt": "从以下纪要中提取待办事项，输出 JSON 数组：{{summary}}"
                    }},
                    {"id": "format", "type": "action", "config": {"operation": "format_doc"}},
                    {"id": "send", "type": "tool", "config": {"tool": "send_email"}}
                ],
                "tools": ["whisper_api", "send_email", "slack_notify"]
            },
            "code_example": {
                "agent_config": '''
{
  "name": "meeting_minutes_assistant",
  "type": "agent",
  "input_schema": {"audio_file": "string"},
  "output_schema": {"minutes": "string", "action_items": "array"},
  "tools": ["whisper_api", "send_email"]
}
'''
            }
        },
        "case_202": {
            "id": "case_202",
            "name": "邮件智能分类处理",
            "category": "office_automation",
            "difficulty": "medium",
            "description": "自动分类、优先级排序、生成回复草稿"
        },
        "case_203": {
            "id": "case_203",
            "name": "合同审核助手",
            "category": "office_automation",
            "difficulty": "high",
            "description": "自动识别合同风险点，生成审核意见"
        },
        "case_204": {
            "id": "case_204",
            "name": "日程管理助手",
            "category": "office_automation",
            "difficulty": "easy",
            "description": "智能日程安排，自动协调会议时间"
        }
    }

    # ========== 内容创作案例 ==========
    CONTENT_CREATION_CASES = {
        "case_301": {
            "id": "case_301",
            "name": "社交媒体内容工厂",
            "category": "content_creation",
            "difficulty": "medium",
            "description": "批量生成多平台社交媒体内容，保持品牌调性一致",
            "scenario": """
运营团队需要在多个平台（微信、微博、抖音、小红书）发布内容。

挑战：
- 平台调性不同
- 内容批量生产
- 保持品牌一致性
- 发布时机优化
            """,
            "solution": {
                "architecture": "content_factory",
                "workflow": [
                    {"id": "input", "type": "input"},
                    {"id": "research", "type": "tool", "config": {"tool": "web_search"}},
                    {"id": "generate_draft", "type": "llm", "config": {
                        "system_prompt": "你是一个专业的内容创作者，根据主题生成创意内容。"
                    }},
                    {"id": "adapt_wechat", "type": "llm", "config": {
                        "prompt": "将以下内容改写为微信公众号风格：{{draft}}"
                    }},
                    {"id": "adapt_xiaohongshu", "type": "llm", "config": {
                        "prompt": "将以下内容改写为小红书风格，包含 emoji 和话题标签：{{draft}}"
                    }},
                    {"id": "adapt_douyin", "type": "llm", "config": {
                        "prompt": "将以下内容改写为抖音短视频脚本，包含开场钩子：{{draft}}"
                    }},
                    {"id": "schedule", "type": "action", "config": {"operation": "schedule_posts"}}
                ],
                "templates": {
                    "wechat": "正式、专业、有深度",
                    "xiaohongshu": "生活化、个人体验、带表情",
                    "douyin": "短平快、爆点前置"
                }
            },
            "code_example": {
                "workflow_config": '''
{
  "name": "content_factory",
  "type": "workflow",
  "nodes": [
    {"id": "research", "type": "tool", "tool": "web_search"},
    {"id": "draft", "type": "llm"},
    {"id": "adapt_wechat", "type": "llm"},
    {"id": "adapt_xhs", "type": "llm"},
    {"id": "schedule", "type": "action"}
  ]
}
'''
            }
        },
        "case_302": {
            "id": "case_302",
            "name": "营销文案生成器",
            "category": "content_creation",
            "difficulty": "easy",
            "description": "根据产品信息自动生成营销文案"
        },
        "case_303": {
            "id": "case_303",
            "name": "视频脚本创作助手",
            "category": "content_creation",
            "difficulty": "medium",
            "description": "自动生成视频脚本，包含分镜、台词、背景音乐建议"
        }
    }

    # ========== 开发助手案例 ==========
    DEVELOPMENT_CASES = {
        "case_401": {
            "id": "case_401",
            "name": "代码审查助手",
            "category": "development",
            "difficulty": "medium",
            "description": "自动审查代码，识别潜在问题，给出优化建议",
            "scenario": """
开发团队代码审查依赖人工，效率低且容易遗漏。

功能：
- 代码质量分析
- 安全漏洞检测
- 性能问题识别
- 最佳实践建议
- 自动生成审查报告
            """,
            "solution": {
                "architecture": "code_review_pipeline",
                "workflow": [
                    {"id": "trigger", "type": "webhook", "config": {"events": ["pull_request"]}},
                    {"id": "fetch_code", "type": "tool", "config": {"tool": "github_api"}},
                    {"id": "parse_diff", "type": "action", "config": {"operation": "parse_diff"}},
                    {"id": "security_scan", "type": "llm", "config": {
                        "prompt": "审查以下代码的安全问题：\n{{code}}\n\n识别：SQL注入、XSS、敏感信息泄露等"
                    }},
                    {"id": "quality_review", "type": "llm", "config": {
                        "prompt": "审查代码质量和可维护性：\n{{code}}\n\n建议：重构、优化、设计模式"
                    }},
                    {"id": "generate_report", "type": "llm", "config": {
                        "prompt": "汇总以下审查结果，生成结构化报告：\n安全：{{security}}\n质量：{{quality}}"
                    }},
                    {"id": "post_comment", "type": "tool", "config": {"tool": "github_comment"}}
                ]
            },
            "code_example": {
                "workflow_config": '''
{
  "name": "code_review_assistant",
  "type": "workflow",
  "trigger": {
    "type": "webhook",
    "events": ["pull_request.opened", "pull_request.synchronize"]
  },
  "nodes": [
    {"id": "fetch", "type": "tool", "tool": "github_api"},
    {"id": "security", "type": "llm"},
    {"id": "quality", "type": "llm"},
    {"id": "report", "type": "llm"},
    {"id": "comment", "type": "tool", "tool": "github_comment"}
  ]
}
'''
            }
        },
        "case_402": {
            "id": "case_402",
            "name": "API 文档生成器",
            "category": "development",
            "difficulty": "easy",
            "description": "从代码注释自动生成 API 文档"
        },
        "case_403": {
            "id": "case_403",
            "name": "Bug 自动定位",
            "category": "development",
            "difficulty": "high",
            "description": "根据错误日志自动定位 Bug 根因"
        }
    }

    # ========== 知识库问答案例 ==========
    KNOWLEDGE_BASE_CASES = {
        "case_501": {
            "id": "case_501",
            "name": "企业内部知识库问答",
            "category": "knowledge_base",
            "difficulty": "medium",
            "description": "基于企业内部文档的智能问答助手",
            "scenario": """
企业有大量内部文档，但检索困难，新员工上手慢。

功能：
- 文档向量化存储
- 语义检索
- 引用来源
- 多轮对话
- 权限控制
            """,
            "solution": {
                "architecture": "rag_system",
                "workflow": [
                    {"id": "input", "type": "input"},
                    {"id": "retrieve", "type": "retrieval", "config": {
                        "query": "{{question}}",
                        "top_k": 5,
                        "score_threshold": 0.7
                    }},
                    {"id": "augment", "type": "action", "config": {"operation": "build_context"}},
                    {"id": "answer", "type": "llm", "config": {
                        "prompt": "基于以下上下文回答问题。\n\n上下文：\n{{context}}\n\n问题：{{question}}\n\n要求：\n1. 仅基于上下文回答\n2. 引用相关来源\n3. 如上下文不足，说明不知道"
                    }},
                    {"id": "output", "type": "output"}
                ],
                "memory": {
                    "type": "vector",
                    "provider": "chroma",
                    "collection": "company_knowledge"
                }
            }
        },
        "case_502": {
            "id": "case_502",
            "name": "法律文档检索",
            "category": "knowledge_base",
            "difficulty": "high",
            "description": "法律条款检索和案例分析"
        }
    }

    # ========== 销售助手案例 ==========
    SALES_CASES = {
        "case_601": {
            "id": "case_601",
            "name": "智能销售报价",
            "category": "sales",
            "difficulty": "medium",
            "description": "根据客户需求自动生成报价方案"
        },
        "case_602": {
            "id": "case_602",
            "name": "客户跟进助手",
            "category": "sales",
            "difficulty": "easy",
            "description": "自动跟进潜在客户，生成跟进记录"
        }
    }

    # ========== HR 助手案例 ==========
    HR_CASES = {
        "case_701": {
            "id": "case_701",
            "name": "简历筛选助手",
            "category": "hr",
            "difficulty": "medium",
            "description": "自动筛选简历，评估候选人匹配度"
        },
        "case_702": {
            "id": "case_702",
            "name": "员工入职向导",
            "category": "hr",
            "difficulty": "easy",
            "description": "新员工入职流程引导和问题解答"
        }
    }

    @classmethod
    def get_all_cases(cls) -> Dict[str, Dict]:
        """获取所有案例"""
        all_cases = {}
        for category_cases in [
            cls.CUSTOMER_SERVICE_CASES,
            cls.DATA_ANALYSIS_CASES,
            cls.OFFICE_AUTOMATION_CASES,
            cls.CONTENT_CREATION_CASES,
            cls.DEVELOPMENT_CASES,
            cls.KNOWLEDGE_BASE_CASES,
            cls.SALES_CASES,
            cls.HR_CASES
        ]:
            all_cases.update(category_cases)
        return all_cases

    @classmethod
    def get_cases_by_category(cls, category: str) -> Dict[str, Dict]:
        """按分类获取案例"""
        category_map = {
            "customer_service": cls.CUSTOMER_SERVICE_CASES,
            "data_analysis": cls.DATA_ANALYSIS_CASES,
            "office_automation": cls.OFFICE_AUTOMATION_CASES,
            "content_creation": cls.CONTENT_CREATION_CASES,
            "development": cls.DEVELOPMENT_CASES,
            "knowledge_base": cls.KNOWLEDGE_BASE_CASES,
            "sales": cls.SALES_CASES,
            "hr": cls.HR_CASES
        }
        return category_map.get(category, {})

    @classmethod
    def get_case_by_id(cls, case_id: str) -> Optional[Dict]:
        """根据 ID 获取案例"""
        return cls.get_all_cases().get(case_id)

    @classmethod
    def search_cases(cls, query: str) -> List[Dict]:
        """搜索案例"""
        results = []
        query_lower = query.lower()
        
        for case in cls.get_all_cases().values():
            if (query_lower in case.get("name", "").lower() or
                query_lower in case.get("description", "").lower()):
                results.append(case)
        
        return results


# =============================================================================
# 模板库
# =============================================================================

class SolutionTemplates:
    """解决方案模板"""

    # 通用 Workflow 模板
    WORKFLOW_TEMPLATES = {
        "rag": {
            "name": "RAG 检索增强生成",
            "description": "基于知识库的问答系统",
            "template": '''
{
  "name": "rag_workflow",
  "type": "workflow",
  "nodes": [
    {"id": "input", "type": "input"},
    {"id": "retrieve", "type": "retrieval"},
    {"id": "augment", "type": "action"},
    {"id": "generate", "type": "llm"},
    {"id": "output", "type": "output"}
  ],
  "edges": [
    {"from": "input", "to": "retrieve"},
    {"from": "retrieve", "to": "augment"},
    {"from": "augment", "to": "generate"},
    {"from": "generate", "to": "output"}
  ]
}
'''
        },
        "agentic": {
            "name": "Agent 自主执行",
            "description": "Agent 自主决策和执行任务",
            "template": '''
{
  "name": "agentic_workflow",
  "type": "agent",
  "config": {
    "model": "gpt-4o",
    "tools": ["web_search", "calculator", "code_interpreter"],
    "memory": {"type": "basic"},
    "max_iterations": 10,
    "stopping_condition": "task_complete"
  }
}
'''
        },
        "pipeline": {
            "name": "数据处理流水线",
            "description": "多步骤数据处理",
            "template": '''
{
  "name": "data_pipeline",
  "type": "workflow",
  "workflow_type": "sequential",
  "nodes": [],
  "edges": []
}
'''
        }
    }

    # 工具组合模板
    TOOL_COMBINATIONS = {
        "web_research": ["web_search", "web_fetch", "file_write"],
        "data_analysis": ["db_query", "code_interpreter", "file_write"],
        "content_generation": ["web_search", "llm", "file_write", "send_email"],
        "code_review": ["github_api", "code_interpreter", "llm", "github_comment"]
    }


# =============================================================================
# 案例专家系统
# =============================================================================

class CaseExpert:
    """
    案例库专家
    
    提供案例检索、推荐和模板服务
    """

    def __init__(self):
        self.library = CaseLibrary()
        self.templates = SolutionTemplates()

    def get_all_cases(
        self,
        category: str = None,
        difficulty: str = None
    ) -> List[Dict]:
        """获取案例列表"""
        if category:
            cases = self.library.get_cases_by_category(category)
        else:
            cases = self.library.get_all_cases()
        
        if difficulty:
            cases = {k: v for k, v in cases.items() if v.get("difficulty") == difficulty}
        
        return list(cases.values())

    def get_case(self, case_id: str) -> Optional[Dict]:
        """获取案例详情"""
        return self.library.get_case_by_id(case_id)

    def search_cases(self, query: str) -> List[Dict]:
        """搜索案例"""
        return self.library.search_cases(query)

    def recommend_case(
        self,
        use_case: str,
        difficulty: str = None
    ) -> List[Dict]:
        """推荐案例"""
        # 根据使用场景映射到分类
        use_case_map = {
            "客服": "customer_service",
            "customer": "customer_service",
            "客服机器人": "customer_service",
            "数据分析": "data_analysis",
            "data": "data_analysis",
            "分析": "data_analysis",
            "办公": "office_automation",
            "office": "office_automation",
            "会议": "office_automation",
            "内容": "content_creation",
            "content": "content_creation",
            "创作": "content_creation",
            "开发": "development",
            "dev": "development",
            "代码": "development",
            "知识库": "knowledge_base",
            "qa": "knowledge_base",
            "问答": "knowledge_base",
            "销售": "sales",
            "hr": "hr",
            "招聘": "hr"
        }
        
        category = use_case_map.get(use_case.lower())
        if not category:
            return self.get_all_cases(difficulty=difficulty)
        
        return self.get_cases_by_category(category, difficulty)

    def get_template(
        self,
        template_name: str,
        **kwargs
    ) -> str:
        """获取模板"""
        template = self.templates.WORKFLOW_TEMPLATES.get(template_name)
        if template:
            return template["template"]
        return ""

    def generate_case_from_template(
        self,
        template_name: str,
        case_name: str,
        customizations: Dict = None
    ) -> Dict:
        """基于模板生成案例"""
        template = self.templates.WORKFLOW_TEMPLATES.get(template_name)
        if not template:
            return {}
        
        case = {
            "id": f"custom_{hash(case_name) % 10000}",
            "name": case_name,
            "category": "custom",
            "difficulty": "medium",
            "description": f"基于 {template['name']} 模板创建",
            "solution": json.loads(template["template"]),
            "customizations": customizations or {}
        }
        
        return case


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 案例库 v5.0"
    )

    # 案例查询
    parser.add_argument("--list", action="store_true", help="列出所有案例")
    parser.add_argument("--category", help="按分类筛选")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"],
                       help="按难度筛选")
    parser.add_argument("--search", help="搜索案例")
    parser.add_argument("--case-id", help="获取案例详情")

    # 推荐
    parser.add_argument("--recommend", help="根据场景推荐案例")

    # 模板
    parser.add_argument("--template", choices=["rag", "agentic", "pipeline"],
                       help="获取模板")

    # 生成
    parser.add_argument("--generate", help="从模板生成案例")
    parser.add_argument("--name", help="案例名称")

    args = parser.parse_args()

    expert = CaseExpert()

    if args.list:
        cases = expert.get_all_cases(args.category, args.difficulty)
        for case in cases:
            print(f"{case['id']}: {case['name']} [{case['difficulty']}]")

    elif args.case_id:
        case = expert.get_case(args.case_id)
        if case:
            print(json.dumps(case, indent=2, ensure_ascii=False))
        else:
            print("案例不存在")

    elif args.search:
        results = expert.search_cases(args.search)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.recommend:
        results = expert.recommend_case(args.recommend)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.template:
        template = expert.get_template(args.template)
        print(template)

    elif args.generate:
        case = expert.generate_case_from_template(
            args.template or "rag",
            args.name or "My Case"
        )
        print(json.dumps(case, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
