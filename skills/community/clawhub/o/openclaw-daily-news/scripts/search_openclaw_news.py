#!/usr/bin/env python3
"""
OpenClaw每日资讯搜索脚本
功能：生成搜索关键词、格式化搜索结果、生成报告内容
"""

import json
import datetime
from typing import List, Dict, Any, Optional

def generate_search_queries(date_str: str) -> List[str]:
    """
    生成当日搜索关键词
    
    Args:
        date_str: 日期字符串，格式为YYYY-MM-DD
        
    Returns:
        List[str]: 搜索关键词列表
    """
    # 基本关键词模板
    base_keywords = [
        "安全漏洞", "监管预警", "合规要求",
        "云服务", "企业部署", "产品发布",
        "GitHub进展", "版本更新", "bug修复",
        "AI芯片", "算力成本", "技术架构",
        "政府政策", "法规标准"
    ]
    
    # 组合搜索查询
    queries = [
        f"OpenClaw {date_str} 安全漏洞 监管预警 合规要求",
        f"OpenClaw {date_str} 云服务 企业部署 产品发布",
        f"OpenClaw {date_str} GitHub进展 版本更新 bug修复",
        f"OpenClaw {date_str} AI芯片 算力成本 技术架构",
        f"OpenClaw {date_str} 政府政策 法规标准"
    ]
    
    return queries

def format_search_results(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    格式化并分类搜索结果
    
    Args:
        raw_results: 原始搜索结果列表
        
    Returns:
        Dict[str, Any]: 格式化后的分类数据
    """
    # 分类定义
    categories = {
        "security_regulation": {
            "name": "安全监管与风险警示",
            "items": [],
            "priority": "high"
        },
        "industry_ecology": {
            "name": "产业生态与市场动态",
            "items": [],
            "priority": "high"
        },
        "technology_development": {
            "name": "技术发展与社区生态",
            "items": [],
            "priority": "medium"
        },
        "ai_trends": {
            "name": "AI产业宏观趋势",
            "items": [],
            "priority": "medium"
        },
        "policy_regulation": {
            "name": "政策与监管",
            "items": [],
            "priority": "high"
        },
        "other_tech_progress": {
            "name": "其他重要科技进展",
            "items": [],
            "priority": "low"
        }
    }
    
    # 关键词映射到分类
    keyword_to_category = {
        # 安全监管关键词
        "安全": "security_regulation",
        "漏洞": "security_regulation",
        "监管": "security_regulation",
        "风险": "security_regulation",
        "预警": "security_regulation",
        "工信部": "security_regulation",
        "网信办": "security_regulation",
        "应急中心": "security_regulation",
        "数据泄露": "security_regulation",
        "合规": "security_regulation",
        "CVE": "security_regulation",
        "CVSS": "security_regulation",
        
        # 产业生态关键词
        "华为云": "industry_ecology",
        "腾讯云": "industry_ecology",
        "阿里云": "industry_ecology",
        "云服务": "industry_ecology",
        "企业部署": "industry_ecology",
        "上线": "industry_ecology",
        "发布": "industry_ecology",
        "价格": "industry_ecology",
        "合作": "industry_ecology",
        "生态": "industry_ecology",
        
        # 技术发展关键词
        "GitHub": "technology_development",
        "社区": "technology_development",
        "issue": "technology_development",
        "PR": "technology_development",
        "版本": "technology_development",
        "更新": "technology_development",
        "bug": "technology_development",
        "修复": "technology_development",
        "功能": "technology_development",
        "贡献者": "technology_development",
        "star": "technology_development",
        
        # AI趋势关键词
        "AI芯片": "ai_trends",
        "算力": "ai_trends",
        "投资": "ai_trends",
        "融资": "ai_trends",
        "股价": "ai_trends",
        "市值": "ai_trends",
        "财报": "ai_trends",
        "竞争": "ai_trends",
        "市场": "ai_trends",
        "预测": "ai_trends",
        
        # 政策监管关键词
        "政策": "policy_regulation",
        "法规": "policy_regulation",
        "两会": "policy_regulation",
        "政府工作报告": "policy_regulation",
        "科技部": "policy_regulation",
        "标准": "policy_regulation",
        "监管": "policy_regulation",
        "规划": "policy_regulation",
        "指导意见": "policy_regulation",
        
        # 其他科技关键词
        "碳纤维": "other_tech_progress",
        "新能源汽车": "other_tech_progress",
        "显示技术": "other_tech_progress",
        "电池": "other_tech_progress",
        "新材料": "other_tech_progress",
        "半导体": "other_tech_progress",
        "量子计算": "other_tech_progress"
    }
    
    # 分类处理
    for result in raw_results:
        # 提取关键信息
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")
        source = result.get("source", "")
        
        # 确定分类
        category = "other_tech_progress"  # 默认分类
        for keyword, cat_id in keyword_to_category.items():
            if keyword in title or keyword in content:
                category = cat_id
                break
        
        # 评估风险等级
        risk_level = assess_risk_level(title, content)
        
        # 构建资讯项
        item = {
            "title": title,
            "content": content[:200] + "..." if len(content) > 200 else content,
            "url": url,
            "source": source,
            "risk_level": risk_level,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 添加到相应分类
        if category in categories:
            categories[category]["items"].append(item)
    
    return categories

def assess_risk_level(title: str, content: str) -> str:
    """
    评估资讯的风险等级
    
    Args:
        title: 资讯标题
        content: 资讯内容
        
    Returns:
        str: 风险等级（high/medium/low）
    """
    title_lower = title.lower()
    content_lower = content.lower()
    
    # 高风险关键词
    high_risk_keywords = [
        "高危", "紧急", "立即", "严重", "数据泄露",
        "工信部预警", "应急响应", "cve-", "cvss:9",
        "远程代码执行", "权限提升"
    ]
    
    # 中风险关键词
    medium_risk_keywords = [
        "中危", "重要", "关注", "建议", "安全更新",
        "漏洞修复", "补丁发布", "合规要求", "监管通知"
    ]
    
    # 检查高风险
    for keyword in high_risk_keywords:
        if keyword in title_lower or keyword in content_lower:
            return "high"
    
    # 检查中风险
    for keyword in medium_risk_keywords:
        if keyword in title_lower or keyword in content_lower:
            return "medium"
    
    # 默认为低风险
    return "low"

def generate_daily_report_content(data: Dict[str, Any], date_str: str) -> str:
    """
    生成每日报告内容（markdown格式）
    
    Args:
        data: 格式化后的分类数据
        date_str: 日期字符串
        
    Returns:
        str: markdown格式的报告内容
    """
    # 统计信息
    total_items = 0
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0
    
    for category in data.values():
        for item in category["items"]:
            total_items += 1
            risk = item.get("risk_level", "low")
            if risk == "high":
                high_risk_count += 1
            elif risk == "medium":
                medium_risk_count += 1
            else:
                low_risk_count += 1
    
    # 生成报告内容
    report = f"""# OpenClaw {date_str}资讯汇总

## 一、当日资讯概况
### 1.1 总体统计
- 发现资讯总数：{total_items}条
- 高风险资讯：{high_risk_count}条（安全漏洞预警等）
- 中风险资讯：{medium_risk_count}条（产业动态、重要更新等）
- 低风险资讯：{low_risk_count}条（社区讨论、一般资讯等）

### 1.2 关键发现
"""
    
    # 添加关键发现
    if high_risk_count > 0:
        report += "- **安全风险警报**：发现高风险安全资讯，需要立即关注\n"
    
    # 添加详细分类资讯
    report += "\n## 二、详细分类资讯\n\n"
    
    # 按优先级排序输出分类
    priority_order = ["high", "medium", "low"]
    
    for priority in priority_order:
        for category_id, category_info in data.items():
            if category_info["priority"] == priority and category_info["items"]:
                report += f"### {category_info['name']}\n\n"
                
                # 按风险等级分组显示
                risk_groups = {"high": [], "medium": [], "low": []}
                for item in category_info["items"]:
                    risk_groups[item["risk_level"]].append(item)
                
                for risk_level in ["high", "medium", "low"]:
                    items = risk_groups[risk_level]
                    if items:
                        if risk_level == "high":
                            report += f"#### 🔴 高风险资讯\n"
                        elif risk_level == "medium":
                            report += f"#### 🟡 中风险资讯\n"
                        else:
                            report += f"#### 🟢 低风险资讯\n"
                        
                        for i, item in enumerate(items, 1):
                            report += f"{i}. **{item['title']}**\n"
                            report += f"   - **来源**：{item['source']}\n"
                            report += f"   - **风险等级**：{risk_level}\n"
                            report += f"   - **摘要**：{item['content']}\n"
                            if item.get('url'):
                                report += f"   - **链接**：{item['url']}\n"
                            report += "\n"
                
                report += "\n"
    
    # 添加核心分析与展望
    report += """## 三、核心分析与展望

### 3.1 风险提示
- **安全风险**：关注高危漏洞修复和合规要求
- **技术风险**：注意版本更新和兼容性问题
- **市场风险**：跟踪产业竞争格局变化

### 3.2 关注重点
1. **短期关注**（1-3天）：安全漏洞修复进展
2. **中期关注**（1-2周）：产业合作和市场动态
3. **长期关注**（1个月以上）：技术发展趋势

### 3.3 未来展望
- **技术发展**：OpenClaw生态持续完善
- **市场扩张**：企业应用范围不断扩大
- **监管趋严**：安全合规要求更加严格
"""
    
    # 添加附录
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report += f"""
## 四、附录

### 4.1 数据来源说明
- **搜索时间**：{current_time}
- **搜索范围**：{date_str} 相关资讯
- **来源类型**：官方公告、权威媒体、技术社区

### 4.2 生成信息
- **报告生成时间**：{current_time}
- **技能版本**：1.0.0
- **输出方式**：markdown格式直接输出到对话

### 4.3 免责声明
此报告为自动化生成，内容基于公开信息整理，仅供参考。重要决策请结合多方信息源进行验证。
"""
    
    return report

if __name__ == "__main__":
    # 示例用法
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    print("=== OpenClaw资讯搜索脚本示例 ===\n")
    
    # 生成搜索关键词
    queries = generate_search_queries(date)
    print("1. 生成的搜索关键词：")
    for i, query in enumerate(queries, 1):
        print(f"   {i}. {query}")
    
    print("\n2. 示例搜索结果格式化：")
    # 模拟一些搜索结果
    sample_results = [
        {
            "title": "OpenClaw发现高危安全漏洞CVE-2026-1234",
            "content": "国家信息安全漏洞共享平台发布预警，OpenClaw存在高危远程代码执行漏洞",
            "url": "https://example.com/cve-2026-1234",
            "source": "国家信息安全漏洞共享平台"
        },
        {
            "title": "华为云宣布全面支持OpenClaw部署",
            "content": "华为云与OpenClaw达成战略合作，提供一站式AI智能体部署服务",
            "url": "https://huaweicloud.com/news",
            "source": "华为云官网"
        }
    ]
    
    formatted_data = format_search_results(sample_results)
    print(f"   格式化后分类数：{len(formatted_data)}")
    
    print("\n3. 生成报告内容示例：")
    report_content = generate_daily_report_content(formatted_data, date)
    print(f"   报告内容长度：{len(report_content)} 字符")
    print("\n   报告前500字符预览：")
    print("-" * 50)
    print(report_content[:500])
    print("-" * 50)