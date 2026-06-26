#!/usr/bin/env python3
"""
完整性检查引擎 v2.0

检查 PRD 文档章节是否完整
"""

import re
from typing import List, Dict, Tuple


class CompletenessChecker:
    """完整性检查引擎"""

    # P0 必需章节（v2.6.3 增强版 - 支持多种 PRD 模板结构）
    P0_SECTIONS = {
        "product_overview": {
            "patterns": [
                "产品概述", "产品简介", "产品背景", "文档信息",
                "需求概述", "需求背景", "项目概述"  # 新模板别名
            ],
            "required_keywords": ["产品定位", "目标用户", "核心价值", "业务目标"],
            "name": "产品概述",
            "content_check": True  # 启用内容识别
        },
        "functional_requirements": {
            "patterns": [
                "功能需求", "功能设计", "功能清单",
                "功能 1", "功能 2", "功能 3"  # 新模板：功能 X：XXX 格式
            ],
            "required_keywords": ["功能", "模块"],
            "name": "功能需求",
            "content_check": True
        },
        "non_functional_requirements": {
            "patterns": [
                "非功能需求", "非功能性需求", "性能需求", "质量属性",
                "非功能需求"  # 新模板
            ],
            "required_keywords": ["性能", "安全", "兼容性", "可用性"],
            "name": "非功能需求",
            "content_check": True
        },
        "business_flow": {
            "patterns": [
                "业务流程", "流程图", "业务流程图",
                "全局业务流程"  # 新模板
            ],
            "required_keywords": ["流程", "步骤"],
            "name": "业务流程",
            "content_check": True
        },
        "compliance_requirements": {
            "patterns": [
                "合规要求", "合规章节", "监管要求",
                "业务规则", "全局业务规则"  # 新模板：业务规则也算合规
            ],
            "required_keywords": ["合规", "监管", "法规", "规则", "限制"],
            "name": "合规要求",
            "content_check": True  # 启用内容识别（即使章节名不匹配，内容包含也算）
        },
        "risk_disclosure": {
            "patterns": [
                "风险揭示", "风险提示", "风险说明",
                "异常处理", "风险管理"  # 新模板：异常处理也算风险相关
            ],
            "required_keywords": ["风险", "风险等级", "异常", "错误"],
            "name": "风险揭示",
            "content_check": True
        },
        "acceptance_criteria": {
            "patterns": [
                "验收标准", "验收条件", "验收测试",
                "验收标准"  # 新模板
            ],
            "required_keywords": ["验收", "测试"],
            "name": "验收标准",
            "content_check": True
        }
    }

    # P1 推荐章节
    P1_SECTIONS = {
        "data_requirements": {
            "patterns": ["数据需求", "数据来源", "数据处理"],
            "name": "数据需求"
        },
        "interface_design": {
            "patterns": ["界面设计", "原型", "UI 设计"],
            "name": "界面设计"
        },
        "appendix": {
            "patterns": ["附录", "参考资料", "术语表"],
            "name": "附录"
        }
    }

    def check(self, prd_content: str) -> Dict:
        """
        检查 PRD 完整性

        参数:
            prd_content: PRD 文档内容

        返回:
            {
                "check_type": "completeness",
                "score": 85,
                "status": "pass/warning/fail",
                "issues": [...],
                "p0_complete": 7,
                "p1_complete": 2
            }
        """
        issues = []
        p0_found = 0
        p1_found = 0

        # 提取文档所有章节标题
        headings = self.extract_headings(prd_content)

        # 检查 P0 章节（v2.6.3 增强版 - 传递 prd_content 支持内容识别）
        for section_id, section_info in self.P0_SECTIONS.items():
            found = self.check_section_exists(headings, section_info["patterns"], prd_content)

            if found:
                p0_found += 1
                # 检查关键字是否覆盖
                missing_keywords = self.check_keywords(prd_content, section_info.get("required_keywords", []))
                if missing_keywords:
                    issues.append({
                        "id": f"C{section_id}",
                        "type": "incomplete_section",
                        "severity": "medium",
                        "title": f"{section_info['name']}内容不完整",
                        "description": f"缺少关键内容：{', '.join(missing_keywords)}",
                        "location": section_info["name"],
                        "suggestion": f"补充{', '.join(missing_keywords)}相关说明"
                    })
            else:
                issues.append({
                    "id": f"M{section_id}",
                    "type": "missing_section",
                    "severity": "high",
                    "title": f"缺失{section_info['name']}章节",
                    "description": f"PRD 缺少必需的{section_info['name']}章节",
                    "location": "全文档",
                    "suggestion": f"添加{section_info['name']}章节，包含{', '.join(section_info.get('required_keywords', []))}等内容"
                })

        # 检查 P1 章节
        for section_id, section_info in self.P1_SECTIONS.items():
            found = self.check_section_exists(headings, section_info["patterns"])
            if found:
                p1_found += 1

        # 检查空洞章节（只有标题没有内容）
        empty_section_issues = self.check_empty_chapters(prd_content, headings)
        issues.extend(empty_section_issues)

        # 计算得分
        score = self.calculate_score(p0_found, len(self.P0_SECTIONS), issues)

        return {
            "check_type": "completeness",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "p0_complete": p0_found,
            "p0_total": len(self.P0_SECTIONS),
            "p1_complete": p1_found,
            "p1_total": len(self.P1_SECTIONS),
            "completeness_rate": p0_found / len(self.P0_SECTIONS) * 100
        }

    def extract_headings(self, content: str) -> List[Tuple[int, str]]:
        """提取文档标题"""
        headings = []
        lines = content.split('\n')

        for line in lines:
            # Markdown 标题
            md_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if md_match:
                level = len(md_match.group(1))
                title = md_match.group(2).strip()
                headings.append((level, title))

            # Word 风格标题（如果有）
            elif re.match(r'^第 [一二三四五六七八九十]+ 章', line):
                headings.append((1, line.strip()))
            elif re.match(r'^第 [一二三四五六七八九十]+ 节', line):
                headings.append((2, line.strip()))

        return headings

    def check_section_exists(self, headings: List[Tuple[int, str]], patterns: List[str], prd_content: str = None) -> bool:
        """检查章节是否存在（v2.6.3 增强版 - 支持内容识别）"""
        heading_texts = [title for _, title in headings]

        # 1. 先检查章节名匹配
        for pattern in patterns:
            for heading in heading_texts:
                if pattern.lower() in heading.lower():
                    return True

        # 2. 章节名不匹配时，检查内容是否包含相关关键词（内容识别）
        # 适用场景：章节名不同但内容实质相同（如"需求概述"vs"产品概述"）
        if prd_content:
            # 定义内容识别规则：章节名不匹配时，检查全文是否包含足够的关键词
            content_keywords = {
                "product_overview": ["产品定位", "目标用户", "核心价值", "业务目标", "产品概述"],
                "compliance_requirements": ["合规", "监管", "法规", "业务规则", "限制", "校验"],
                "risk_disclosure": ["风险", "异常", "错误", "处理", "提示"],
                "functional_requirements": ["功能", "模块", "输入", "输出", "业务规则"],
                "business_flow": ["流程", "步骤", "节点", "流转"],
                "non_functional_requirements": ["性能", "安全", "兼容性", "可用性", "响应时间"],
                "acceptance_criteria": ["验收", "测试", "标准", "Given", "When", "Then"]
            }

            # 遍历所有 patterns，找到对应的 section_id
            for section_id, section_info in self.P0_SECTIONS.items():
                if any(pattern in patterns for pattern in section_info["patterns"]):
                    keywords = content_keywords.get(section_id, [])
                    if keywords:
                        # 检查内容中是否包含足够的关键词
                        match_count = sum(1 for kw in keywords if kw.lower() in prd_content.lower())
                        # 匹配 50% 以上关键词即认为章节存在
                        if match_count >= len(keywords) * 0.5:
                            return True

        return False

    def check_keywords(self, content: str, keywords: List[str]) -> List[str]:
        """检查关键字是否覆盖"""
        missing = []

        for keyword in keywords:
            if keyword.lower() not in content.lower():
                missing.append(keyword)

        # 如果缺失超过一半，才认为是问题
        if len(missing) > len(keywords) * 0.5:
            return missing
        return []

    def check_empty_chapters(self, prd_content: str, headings: List[Tuple[int, str]]) -> List[Dict]:
        """检查空洞章节（只有标题没有内容）"""
        issues = []
        lines = prd_content.split('\n')

        for i, (level, title) in enumerate(headings):
            # 只检查"第 X 章"格式的章节
            if not re.match(r'第 [一二三四五六七八九十\d]+ 章', title):
                continue

            # 找到当前章节的起始行
            start_line = -1
            for j in range(len(lines)):
                if f'## {title}' in lines[j] or f'# {title}' in lines[j]:
                    start_line = j
                    break

            if start_line == -1:
                continue

            # 找到下一章的起始行
            end_line = len(lines)
            for j in range(start_line + 1, len(lines)):
                # 检查是否是同级或更高级别的章节标题
                if re.match(r'^##\s+第 [一二三四五六七八九十\d]+ 章', lines[j]):
                    end_line = j
                    break

            # 提取章节内容
            section_lines = lines[start_line + 1:end_line]
            # 过滤掉空行和子标题
            content_lines = [
                line for line in section_lines
                if line.strip() and not re.match(r'^#{1,4}\s+', line)
            ]

            # 如果内容行数少于 5 行，认为是空洞章节
            if len(content_lines) < 5:
                issues.append({
                    "id": f"E{title[:10]}",
                    "type": "empty_chapter",
                    "severity": "medium",
                    "title": f"{title} 内容空洞",
                    "description": f"该章节只有{len(content_lines)}行内容，缺少实质性内容",
                    "location": title,
                    "suggestion": "补充该章节的具体内容，或删除该章节避免结构冗余"
                })

        return issues

    def calculate_score(self, p0_found: int, p0_total: int, issues: List[Dict]) -> int:
        """计算得分"""
        # 基础分 = P0 章节完成率 * 100
        base_score = (p0_found / p0_total) * 100 if p0_total > 0 else 0

        # 扣分
        deduction = 0
        for issue in issues:
            if issue["severity"] == "high":
                deduction += 10
            elif issue["severity"] == "medium":
                deduction += 5

        return max(0, min(100, int(base_score - deduction)))


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD

    ## 一、产品概述
    产品定位：养老规划工具
    目标用户：35-55 岁中年群体
    核心价值：帮助用户科学规划养老

    ## 二、功能需求
    功能 1: 养老测算
    功能 2: 产品推荐

    ## 三、业务流程
    用户注册 → 风险测评 → 产品购买
    """

    checker = CompletenessChecker()
    result = checker.check(test_prd)

    print("完整性检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"P0 章节：{result['p0_complete']}/{result['p0_total']}")
    print(f"P1 章节：{result['p1_complete']}/{result['p1_total']}")
    print(f"\n问题列表:")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}")
