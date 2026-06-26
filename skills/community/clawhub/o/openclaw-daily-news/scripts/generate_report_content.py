#!/usr/bin/env python3
"""
OpenClaw报告内容生成脚本
功能：创建报告结构、生成Markdown报告内容
"""

import datetime
import json
from typing import Dict, Any, List, Optional

def create_report_structure(date_str: str) -> Dict[str, Any]:
    """
    创建标准报告结构
    
    Args:
        date_str: 日期字符串
        
    Returns:
        Dict[str, Any]: 报告结构字典
    """
    return {
        "metadata": {
            "report_date": date_str,
            "creation_time": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "output_mode": "conversation_markdown"
        },
        "sections": {
            "overview": {
                "title": "当日资讯概况",
                "subsections": {
                    "statistics": {
                        "title": "总体统计",
                        "items": []
                    },
                    "key_findings": {
                        "title": "关键发现",
                        "items": []
                    }
                }
            },
            "detailed_categories": {
                "title": "详细分类资讯",
                "categories": {}
            },
            "core_analysis": {
                "title": "核心分析与展望",
                "subsections": {
                    "risk_alerts": {
                        "title": "风险提示",
                        "items": []
                    },
                    "focus_points": {
                        "title": "关注重点",
                        "items": []
                    },
                    "future_outlook": {
                        "title": "未来展望",
                        "items": []
                    }
                }
            },
            "appendix": {
                "title": "附录",
                "subsections": {
                    "data_sources": {
                        "title": "数据来源说明",
                        "items": []
                    },
                    "generation_info": {
                        "title": "生成信息",
                        "items": []
                    },
                    "disclaimer": {
                        "title": "免责声明",
                        "items": []
                    }
                }
            }
        }
    }

def add_item_to_structure(structure: Dict[str, Any], news_item: Dict[str, Any]) -> None:
    """
    添加资讯项到报告结构
    
    Args:
        structure: 报告结构
        news_item: 资讯项
    """
    # 确定分类
    category = news_item.get("category", "other")
    
    # 初始化分类结构
    if category not in structure["sections"]["detailed_categories"]["categories"]:
        structure["sections"]["detailed_categories"]["categories"][category] = {
            "name": get_category_name(category),
            "risk_groups": {
                "high": [],
                "medium": [],
                "low": []
            }
        }
    
    # 添加到相应风险组
    risk_level = news_item.get("risk_level", "low")
    structure["sections"]["detailed_categories"]["categories"][category]["risk_groups"][risk_level].append(news_item)

def get_category_name(category_id: str) -> str:
    """
    获取分类名称
    
    Args:
        category_id: 分类ID
        
    Returns:
        str: 分类名称
    """
    category_names = {
        "security_regulation": "安全监管与风险警示",
        "industry_ecology": "产业生态与市场动态",
        "technology_development": "技术发展与社区生态",
        "ai_trends": "AI产业宏观趋势",
        "policy_regulation": "政策与监管",
        "other_tech_progress": "其他重要科技进展",
        "other": "其他资讯"
    }
    
    return category_names.get(category_id, "其他资讯")

def generate_markdown_content(structure: Dict[str, Any]) -> str:
    """
    生成Markdown格式报告内容
    
    Args:
        structure: 报告结构
        
    Returns:
        str: markdown格式的报告内容
    """
    # 提取元数据
    metadata = structure["metadata"]
    report_date = metadata["report_date"]
    
    # 生成报告标题
    markdown = f"# OpenClaw {report_date}资讯汇总\n\n"
    
    # 生成概述部分
    overview = structure["sections"]["overview"]
    markdown += f"## 一、{overview['title']}\n\n"
    
    # 总体统计
    stats_section = overview["subsections"]["statistics"]
    markdown += f"### {stats_section['title']}\n"
    
    # 计算统计信息
    total_items = 0
    risk_counts = {"high": 0, "medium": 0, "low": 0}
    
    for category_info in structure["sections"]["detailed_categories"]["categories"].values():
        for risk_level, items in category_info["risk_groups"].items():
            count = len(items)
            total_items += count
            risk_counts[risk_level] += count
    
    # 添加统计信息
    markdown += f"- 发现资讯总数：{total_items}条\n"
    markdown += f"- 高风险资讯：{risk_counts['high']}条（安全漏洞预警等）\n"
    markdown += f"- 中风险资讯：{risk_counts['medium']}条（产业动态、重要更新等）\n"
    markdown += f"- 低风险资讯：{risk_counts['low']}条（社区讨论、一般资讯等）\n\n"
    
    # 关键发现
    key_findings = overview["subsections"]["key_findings"]
    if key_findings["items"]:
        markdown += f"### {key_findings['title']}\n"
        for item in key_findings["items"]:
            markdown += f"- {item}\n"
        markdown += "\n"
    else:
        # 自动生成关键发现
        markdown += f"### {key_findings['title']}\n"
        if risk_counts['high'] > 0:
            markdown += "- **安全风险警报**：发现高风险安全资讯，需要立即关注\n"
        if risk_counts['medium'] > 0:
            markdown += "- **重要动态更新**：关注产业和技术重要进展\n"
        if risk_counts['low'] > 0:
            markdown += "- **常规资讯汇总**：了解相关领域的一般动态\n"
        markdown += "\n"
    
    # 生成详细分类资讯
    detailed_categories = structure["sections"]["detailed_categories"]
    markdown += f"## 二、{detailed_categories['title']}\n\n"
    
    # 按优先级顺序输出分类
    priority_order = [
        ("security_regulation", "高"),
        ("policy_regulation", "高"),
        ("industry_ecology", "高"),
        ("technology_development", "中"),
        ("ai_trends", "中"),
        ("other_tech_progress", "低"),
        ("other", "低")
    ]
    
    for category_id, _ in priority_order:
        if category_id in detailed_categories["categories"]:
            category_info = detailed_categories["categories"][category_id]
            category_name = category_info["name"]
            
            markdown += f"### {category_name}\n\n"
            
            # 按风险等级输出
            for risk_level in ["high", "medium", "low"]:
                items = category_info["risk_groups"][risk_level]
                if items:
                    # 风险等级标题
                    if risk_level == "high":
                        risk_title = "🔴 高风险资讯"
                    elif risk_level == "medium":
                        risk_title = "🟡 中风险资讯"
                    else:
                        risk_title = "🟢 低风险资讯"
                    
                    markdown += f"#### {risk_title}\n\n"
                    
                    # 输出每个资讯项
                    for i, item in enumerate(items, 1):
                        markdown += f"{i}. **{item.get('title', '无标题')}**\n"
                        
                        if item.get('source'):
                            markdown += f"   - **来源**：{item['source']}\n"
                        
                        if item.get('risk_level'):
                            risk_text = {"high": "高", "medium": "中", "low": "低"}[item['risk_level']]
                            markdown += f"   - **风险等级**：{risk_text}\n"
                        
                        if item.get('content'):
                            content = item['content']
                            if len(content) > 150:
                                content = content[:150] + "..."
                            markdown += f"   - **摘要**：{content}\n"
                        
                        if item.get('url'):
                            markdown += f"   - **链接**：{item['url']}\n"
                        
                        markdown += "\n"
            
            markdown += "\n"
    
    # 生成核心分析与展望
    core_analysis = structure["sections"]["core_analysis"]
    markdown += f"## 三、{core_analysis['title']}\n\n"
    
    # 风险提示
    risk_alerts = core_analysis["subsections"]["risk_alerts"]
    markdown += f"### {risk_alerts['title']}\n"
    if risk_alerts["items"]:
        for item in risk_alerts["items"]:
            markdown += f"- {item}\n"
    else:
        # 自动生成风险提示
        if risk_counts['high'] > 0:
            markdown += "- **安全风险**：关注高危漏洞修复和合规要求\n"
        if risk_counts['medium'] > 0:
            markdown += "- **技术风险**：注意版本更新和兼容性问题\n"
        markdown += "- **市场风险**：跟踪产业竞争格局变化\n"
    markdown += "\n"
    
    # 关注重点
    focus_points = core_analysis["subsections"]["focus_points"]
    markdown += f"### {focus_points['title']}\n"
    if focus_points["items"]:
        for i, item in enumerate(focus_points["items"], 1):
            markdown += f"{i}. {item}\n"
    else:
        # 自动生成关注重点
        markdown += "1. **短期关注**（1-3天）：安全漏洞修复进展\n"
        markdown += "2. **中期关注**（1-2周）：产业合作和市场动态\n"
        markdown += "3. **长期关注**（1个月以上）：技术发展趋势\n"
    markdown += "\n"
    
    # 未来展望
    future_outlook = core_analysis["subsections"]["future_outlook"]
    markdown += f"### {future_outlook['title']}\n"
    if future_outlook["items"]:
        for item in future_outlook["items"]:
            markdown += f"- {item}\n"
    else:
        # 自动生成未来展望
        markdown += "- **技术发展**：OpenClaw生态持续完善\n"
        markdown += "- **市场扩张**：企业应用范围不断扩大\n"
        markdown += "- **监管趋严**：安全合规要求更加严格\n"
    markdown += "\n"
    
    # 生成附录
    appendix = structure["sections"]["appendix"]
    markdown += f"## 四、{appendix['title']}\n\n"
    
    # 数据来源说明
    data_sources = appendix["subsections"]["data_sources"]
    markdown += f"### {data_sources['title']}\n"
    if data_sources["items"]:
        for item in data_sources["items"]:
            markdown += f"- {item}\n"
    else:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        markdown += f"- **搜索时间**：{current_time}\n"
        markdown += f"- **搜索范围**：{report_date} 相关资讯\n"
        markdown += "- **来源类型**：官方公告、权威媒体、技术社区\n"
    markdown += "\n"
    
    # 生成信息
    generation_info = appendix["subsections"]["generation_info"]
    markdown += f"### {generation_info['title']}\n"
    if generation_info["items"]:
        for item in generation_info["items"]:
            markdown += f"- {item}\n"
    else:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        markdown += f"- **报告生成时间**：{current_time}\n"
        markdown += "- **技能版本**：1.0.0\n"
    markdown += "\n"
    
    # 免责声明
    disclaimer = appendix["subsections"]["disclaimer"]
    markdown += f"### {disclaimer['title']}\n"
    if disclaimer["items"]:
        for item in disclaimer["items"]:
            markdown += f"- {item}\n"
    else:
        markdown += "- 此报告为自动化生成，内容基于公开信息整理，仅供参考。\n"
        markdown += "- 重要决策请结合多方信息源进行验证。\n"
        markdown += "- 如有疑问，请联系相关技术支持。\n"
    
    return markdown

def output_to_conversation(content: str) -> str:
    """
    将内容准备输出到对话（直接返回内容）
    
    Args:
        content: 要输出的内容
        
    Returns:
        str: 相同的内容（用于在对话中输出）
    """
    # 实际的输出由调用者使用message工具完成
    return content

if __name__ == "__main__":
    # 示例用法
    print("=== OpenClaw报告内容生成脚本示例 ===\n")
    
    # 创建报告结构
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    structure = create_report_structure(date)
    print(f"1. 创建报告结构成功，日期：{date}")
    
    # 添加示例资讯项
    sample_items = [
        {
            "title": "OpenClaw高危漏洞CVE-2026-1234",
            "content": "发现远程代码执行漏洞，建议立即更新",
            "source": "国家信息安全漏洞共享平台",
            "category": "security_regulation",
            "risk_level": "high",
            "url": "https://example.com/cve-2026-1234"
        },
        {
            "title": "华为云OpenClaw部署服务上线",
            "content": "提供一站式AI智能体部署解决方案",
            "source": "华为云官网",
            "category": "industry_ecology",
            "risk_level": "medium",
            "url": "https://huaweicloud.com/openclaw"
        }
    ]
    
    for item in sample_items:
        add_item_to_structure(structure, item)
    
    print(f"2. 添加了 {len(sample_items)} 个示例资讯项")
    
    # 生成markdown内容
    markdown_content = generate_markdown_content(structure)
    print(f"3. 生成markdown内容成功，长度：{len(markdown_content)} 字符")
    
    # 准备输出到对话
    conversation_content = output_to_conversation(markdown_content)
    print(f"4. 准备输出到对话，内容长度：{len(conversation_content)} 字符")
    
    print("\n5. 内容预览（前300字符）：")
    print("-" * 50)
    print(conversation_content[:300])
    print("...")
    print("-" * 50)