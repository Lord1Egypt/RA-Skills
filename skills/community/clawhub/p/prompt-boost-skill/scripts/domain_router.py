#!/usr/bin/env python3
"""
domain_router.py - 初步识别用户问题所属领域和任务类型
输入: {"raw_query": "帮我分析一下销量波动"}
输出: {"domain": "", "task_type": "", "confidence": 0.0, "reasoning": ""}
"""
import json
import sys

DOMAIN_SIGNALS = {
    "data-analysis": {
        "keywords": ["分析", "数据", "指标", "报表", "BI", "SQL", "pandas", "python", "销量", "趋势", "归因", "可视化", "dashboard"],
        "task_types": {
            "root-cause-analysis": ["归因", "波动", "原因", "为什么"],
            "dashboard-design": ["报表", "看板", "dashboard", "BI"],
            "exploratory-analysis": ["探索", "研究", "看看"],
            "metric-design": ["指标", "KPI", "口径"],
        }
    },
    "tech-support": {
        "keywords": ["bug", "报错", "错误", "问题", "安装", "环境", "性能", "慢", "崩溃", "代码", "debug"],
        "task_types": {
            "bug-diagnosis": ["bug", "报错", "错误", "异常"],
            "environment-setup": ["安装", "环境", "配置", "部署"],
            "performance-optimization": ["性能", "慢", "优化", "卡顿"],
            "architecture-debugging": ["架构", "设计", "架构问题"],
        }
    },
    "supply-chain": {
        "keywords": ["供应链", "库存", "采购", "物流", "降本", "订单", "仓储", "供应商", "WMS", "协同"],
        "task_types": {
            "solution-design": ["方案", "优化", "设计"],
            "diagnosis": ["诊断", "问题", "分析"],
            "management-report": ["汇报", "报告", "管理"],
            "optimization-roadmap": ["路线图", "规划", " Roadmap"],
        }
    },
    "product-manager": {
        "keywords": ["产品", "PRD", "需求", "功能", "用户故事", "竞品", " roadmap"],
        "task_types": {
            "prd-writing": ["PRD", "需求文档", "写PRD"],
            "requirement-analysis": ["需求分析", "需求评审"],
            "feature-design": ["功能设计", "功能拆解"],
            "roadmap-planning": [" roadmap", "产品规划", "路线图"],
        }
    },
    "marketing": {
        "keywords": ["市场", "营销", "推广", "品牌", "投放", "增长", "用户增长", "转化", "内容营销", "活动"],
        "task_types": {
            "strategy-design": ["策略", "战略", "方案"],
            "campaign-planning": ["活动", "策划", "推广"],
            "content-angle": ["内容", "选题", "角度"],
            "brand-positioning": ["定位", "品牌定位"],
        }
    },
    "common": {
        "keywords": ["写", "报告", "邮件", "文档", "总结", "方案", "整理", "规划", "计划", "汇报"],
        "task_types": {
            "writing": ["写", "起草", "代写"],
            "analysis": ["分析", "研究", "总结"],
            "planning": ["规划", "计划", "方案"],
            "summarization": ["摘要", "总结", "概括"],
        }
    }
}

def route(raw_query: str) -> dict:
    scores = {}
    for domain, config in DOMAIN_SIGNALS.items():
        score = sum(1 for kw in config["keywords"] if kw in raw_query)
        scores[domain] = score
    
    best_domain = max(scores, key=scores.get)
    confidence = scores[best_domain] / max(sum(scores.values()), 1)
    
    # 识别任务类型
    task_keywords = DOMAIN_SIGNALS[best_domain]["task_types"]
    best_task = "general"
    for task, keywords in task_keywords.items():
        if any(kw in raw_query for kw in keywords):
            best_task = task
            break
    
    return {
        "domain": best_domain,
        "task_type": best_task,
        "confidence": round(confidence, 2),
        "reasoning": f"检测到 {best_domain} 领域（置信度 {confidence:.0%}），任务类型 {best_task}"
    }

if __name__ == "__main__":
    try:
        inp = json.loads(sys.stdin.read())
        result = route(inp.get("raw_query", ""))
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
