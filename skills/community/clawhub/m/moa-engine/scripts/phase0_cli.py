#!/usr/bin/env python3
"""
MoA Phase 0: 任务类型自动判断 CLI

自动分析任务特征，判断任务类型（知识密集型/推理决策型/工具执行型），
评估复杂度与风险等级，推荐执行策略和专家领域。

用法:
  python scripts/phase0_cli.py classify --task "<任务描述>" [--profiles <画像文件>] [--verbose]
  python scripts/phase0_cli.py classify --task "设计高并发微服务架构" --profiles references/capability-profiles.json
  python scripts/phase0_cli.py classify --task "审查支付模块代码安全" --verbose
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional


# ============================================================
# 关键词规则库
# ============================================================

KNOWLEDGE_KEYWORDS = [
    "是什么", "解释", "说明", "概述", "对比", "列举", "总结", "定义",
    "合规", "审查", "审核", "审计", "检查", "评估", "分析报告",
    "调研", "研究", "考证", "溯源", "背景", "原理", "机制",
    "规范", "标准", "法规", "政策", "条款", "要求",
]

REASONING_KEYWORDS = [
    "设计", "架构", "策略", "规划", "方案", "决策",
    "分析", "评估", "权衡", "优化", "改进", "重构",
    "选型", "对比方案", "评审", "讨论", "推演",
    "架构设计", "系统设计", "方案设计", "技术选型",
    "可行性", "最优", "最佳实践", "演进", "路线图",
]

TOOL_KEYWORDS = [
    "生成", "编写", "实现", "配置", "部署", "测试", "构建",
    "编写代码", "脚本", "自动化", "命令行", "工具",
    "代码生成", "数据迁移", "批量处理", "API调用",
    "爬虫", "转换", "解析", "提取", "格式化",
]

COMPLEXITY_HIGH_KEYWORDS = [
    "大规模", "分布式", "高并发", "复杂", "海量", "跨领域",
    "多模块", "微服务", "高可用", "异地多活", "全球部署",
    "千万级", "亿级", "实时", "毫秒", "99.99",
]

COMPLEXITY_MEDIUM_KEYWORDS = [
    "设计", "架构", "多模块", "集成", "对接", "多系统",
    "优化", "重构", "迁移", "升级", "改造",
]

RISK_HIGH_KEYWORDS = [
    "支付", "金融", "隐私", "安全", "合规", "医疗",
    "数据保护", "GDPR", "PCI", "等保", "密码", "加密",
    "敏感数据", "个人信息", "认证", "授权", "鉴权",
    "资金", "交易", "账单", "风控", "反欺诈",
]

RISK_MEDIUM_KEYWORDS = [
    "用户数据", "登录", "注册", "权限", "角色",
    "日志", "审计", "监控", "告警",
]

# ============================================================
# 工具函数
# ============================================================

def tokenize(text: str) -> List[str]:
    """分词：中文按字切分 + 英文按空格，用于 2-gram"""
    return re.findall(r'[\u4e00-\u9fff]+|\w+', text.lower())


def count_matches(text: str, keywords: List[str]) -> int:
    """统计关键词命中数（支持中文子串匹配）"""
    text_lower = text.lower()
    count = 0
    for kw in keywords:
        if kw in text_lower:
            count += 1
    return count


def score_by_keywords(text: str, keywords: List[str]) -> float:
    """基于关键词命中的得分（0-1），考虑密度"""
    matches = count_matches(text, keywords)
    if matches == 0:
        return 0.0
    # 计算密度：命中数 / 文本长度（字符数）
    density = matches / max(len(text), 1) * 100
    # 得分 = 命中数 * 密度因子，归一化到 0-1
    raw = matches * min(density / 5, 1.0)
    return min(raw / 10, 1.0)


# ============================================================
# 核心分类逻辑
# ============================================================

def classify_task(task: str) -> dict:
    """对任务进行多维分析，返回结构化结果"""
    
    # 1. 任务类型判断
    knowledge_score = score_by_keywords(task, KNOWLEDGE_KEYWORDS)
    reasoning_score = score_by_keywords(task, REASONING_KEYWORDS)
    tool_score = score_by_keywords(task, TOOL_KEYWORDS)
    
    scores = {
        "knowledge": knowledge_score,
        "reasoning_decision": reasoning_score,
        "tool_execution": tool_score,
    }
    
    task_type = max(scores, key=scores.get)
    
    # 如果得分都太低（< 0.1），默认推理决策型
    if max(scores.values()) < 0.1:
        task_type = "reasoning_decision"
    
    # 2. 复杂度评估
    high_complexity = count_matches(task, COMPLEXITY_HIGH_KEYWORDS)
    medium_complexity = count_matches(task, COMPLEXITY_MEDIUM_KEYWORDS)
    
    if high_complexity >= 2 or (high_complexity >= 1 and medium_complexity >= 2):
        complexity = "high"
    elif high_complexity >= 1 or medium_complexity >= 2:
        complexity = "medium"
    else:
        complexity = "low"
    
    # 3. 风险等级评估
    high_risk = count_matches(task, RISK_HIGH_KEYWORDS)
    medium_risk = count_matches(task, RISK_MEDIUM_KEYWORDS)
    
    if high_risk >= 2:
        risk_level = "high"
    elif high_risk >= 1 or medium_risk >= 2:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # 4. 推荐策略
    type_config = {
        "knowledge": {
            "protocol": "consensus_first",
            "rounds": 1,
            "description": "共识优先 + 总管复核",
            "critic_focus": "事实核查、数据准确性、引用可靠性",
        },
        "reasoning_decision": {
            "protocol": "debate_weighted",
            "rounds": 2 if complexity == "high" else 1,
            "description": "辩论 + 加权投票",
            "critic_focus": "逻辑漏洞、边界条件、权衡遗漏、假设质疑",
        },
        "tool_execution": {
            "protocol": "orchestrator_dispatch",
            "rounds": 1,
            "description": "总管调度执行",
            "critic_focus": "质量审核、性能隐患、安全风险、异常处理",
        },
    }
    
    strategy = type_config[task_type]
    
    # 高风险加成：增加对抗轮次
    if risk_level == "high" and task_type == "reasoning_decision":
        strategy["rounds"] = max(strategy["rounds"], 2)
    
    # 5. 推荐领域
    domain_map = {
        "安全": ["security", "privacy"],
        "架构": ["architecture", "distributed_systems"],
        "数据库": ["database"],
        "前端": ["frontend", "ux"],
        "产品": ["product", "business"],
        "AI": ["ai", "data_science"],
        "性能": ["performance", "devops"],
        "测试": ["testing", "quality"],
        "合规": ["compliance", "privacy"],
        "API": ["api_design", "architecture"],
        "支付": ["security", "compliance", "architecture"],
        "数据": ["data_science", "database"],
        "部署": ["devops", "infrastructure"],
        "代码": ["backend", "architecture"],
    }
    
    recommended_domains = set()
    for kw, domains in domain_map.items():
        if kw in task:
            for d in domains:
                recommended_domains.add(d)
    
    # 6. 简要理由
    reasons = []
    type_names = {
        "knowledge": "知识密集型",
        "reasoning_decision": "推理决策型",
        "tool_execution": "工具执行型",
    }
    reasons.append(f"任务类型: {type_names[task_type]} (知识得分={knowledge_score:.2f}, 推理得分={reasoning_score:.2f}, 工具得分={tool_score:.2f})")
    
    complexity_names = {"high": "高", "medium": "中", "low": "低"}
    reasons.append(f"复杂度: {complexity_names[complexity]} (高复杂度关键词命中{high_complexity}个)")
    
    risk_names = {"high": "高", "medium": "中", "low": "低"}
    reasons.append(f"风险等级: {risk_names[risk_level]} (高风险关键词命中{high_risk}个)")
    
    if recommended_domains:
        reasons.append(f"推荐领域: {', '.join(sorted(recommended_domains))}")
    
    return {
        "task_type": task_type,
        "complexity": complexity,
        "risk_level": risk_level,
        "scores": scores,
        "recommended_strategy": {
            "protocol": strategy["protocol"],
            "rounds": strategy["rounds"],
            "description": strategy["description"],
            "critic_focus": strategy["critic_focus"],
        },
        "recommended_domains": sorted(recommended_domains),
        "reasons": reasons,
        "risk_flag": risk_level in ("high", "medium"),
        "enable_audit_log": risk_level == "high",
    }


# ============================================================
# 注册表联动
# ============================================================

def suggest_experts(result: dict, profiles_path: Optional[str] = None) -> dict:
    """根据任务分析结果，从注册表推荐专家"""
    if not profiles_path:
        return {"experts": [], "note": "未提供注册表路径，无法推荐专家"}
    
    path = Path(profiles_path)
    if not path.exists():
        return {"experts": [], "note": f"注册表文件不存在: {profiles_path}"}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {"experts": [], "note": f"读取注册表失败: {e}"}
    
    profiles = data.get("profiles", [])
    domains = result.get("recommended_domains", [])
    task_type = result.get("task_type", "")
    
    # 按领域匹配 + 按 performance_vector 排序
    matched = []
    for p in profiles:
        p_domains = p.get("domains", [])
        # 计算领域匹配度
        domain_overlap = len(set(domains) & set(p_domains))
        if domain_overlap > 0:
            pv = p.get("performance_vector", {})
            # 根据任务类型选择不同的排序权重
            if task_type == "knowledge":
                sort_key = pv.get("critique_specificity", 0.5)
            elif task_type == "reasoning_decision":
                sort_key = pv.get("synthesis_novelty", 0.5)
            else:
                sort_key = pv.get("revision_quality", 0.5)
            
            matched.append({
                "id": p["id"],
                "title": p.get("title", ""),
                "domains": p_domains,
                "domain_overlap": domain_overlap,
                "run_count": p.get("meta", {}).get("run_count", 0),
                "sort_key": sort_key,
            })
    
    # 按领域重叠数降序，再按sort_key降序
    matched.sort(key=lambda x: (x["domain_overlap"], x["sort_key"]), reverse=True)
    
    return {
        "experts": matched[:5],
        "total_candidates": len(matched),
        "total_profiles": len(profiles),
    }


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="MoA Phase 0: 任务类型自动判断",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/phase0_cli.py classify --task "设计高并发微服务架构"
  python scripts/phase0_cli.py classify --task "审查支付模块代码安全" --verbose
  python scripts/phase0_cli.py classify --task "生成数据分析报告" --profiles references/capability-profiles.json
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # classify 子命令
    classify_parser = subparsers.add_parser("classify", help="分析任务类型")
    classify_parser.add_argument("--task", required=True, help="任务描述")
    classify_parser.add_argument("--profiles", help="专家画像 JSON 路径（用于推荐专家）")
    classify_parser.add_argument("--verbose", action="store_true", help="输出详细信息")
    
    # list-types 子命令
    list_parser = subparsers.add_parser("list-types", help="列出所有任务类型")
    
    args = parser.parse_args()
    
    if args.command == "classify":
        result = classify_task(args.task)
        
        # 注册表联动
        if args.profiles:
            expert_suggestions = suggest_experts(result, args.profiles)
            result["expert_suggestions"] = expert_suggestions
        
        # 输出
        if args.verbose:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 精简输出
            summary = {
                "task_type": result["task_type"],
                "complexity": result["complexity"],
                "risk_level": result["risk_level"],
                "recommended_strategy": result["recommended_strategy"],
                "recommended_domains": result["recommended_domains"],
                "risk_flag": result["risk_flag"],
            }
            if result.get("expert_suggestions"):
                summary["expert_suggestions"] = {
                    "experts": [
                        {"id": e["id"], "title": e["title"], "match": e["domain_overlap"]}
                        for e in result["expert_suggestions"]["experts"]
                    ]
                }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    elif args.command == "list-types":
        types = {
            "knowledge": {
                "name": "知识密集型",
                "description": "事实查询、概念解释、文献综述、合规审查",
                "protocol": "共识优先 + 总管复核",
                "rounds": "1轮事实核查",
                "examples": "支付模块代码安全审查、GDPR合规分析",
            },
            "reasoning_decision": {
                "name": "推理决策型",
                "description": "方案选择、架构设计、策略规划、风险评估",
                "protocol": "辩论 + 加权投票",
                "rounds": "2轮+深度对抗",
                "examples": "高并发微服务架构设计、技术选型评审",
            },
            "tool_execution": {
                "name": "工具执行型",
                "description": "代码生成、配置编写、数据分析、自动化脚本",
                "protocol": "总管调度执行",
                "rounds": "1轮质量批判",
                "examples": "编写数据迁移脚本、生成API接口文档",
            },
        }
        print(json.dumps(types, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()