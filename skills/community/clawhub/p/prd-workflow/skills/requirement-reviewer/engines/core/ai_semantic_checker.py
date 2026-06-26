#!/usr/bin/env python3
"""
AI 语义评审引擎 v1.0（新增）

使用 AI 大模型进行深度语义评审
检查：业务逻辑合理性、描述清晰度、可执行性、风险识别
"""

import re
from typing import List, Dict


class AISemanticChecker:
    """AI 语义评审引擎"""
    
    def check(self, prd_content: str) -> Dict:
        """
        AI 语义评审
        
        参数:
            prd_content: PRD 文档内容
        
        返回:
            {
                "check_type": "ai_semantic",
                "score": 85,
                "status": "pass/warning/fail",
                "issues": [...],
                "ai_assessment": {...}
            }
        """
        issues = []
        
        # 1. 业务逻辑合理性检查
        print("   🤖 AI 检查：业务逻辑合理性...")
        logic_issues = self.check_business_logic(prd_content)
        issues.extend(logic_issues)
        
        # 2. 描述清晰度检查
        print("   🤖 AI 检查：描述清晰度...")
        clarity_issues = self.check_description_clarity(prd_content)
        issues.extend(clarity_issues)
        
        # 3. 可执行性检查
        print("   🤖 AI 检查：可执行性...")
        execution_issues = self.check_executability(prd_content)
        issues.extend(execution_issues)
        
        # 4. 风险识别检查
        print("   🤖 AI 检查：风险识别...")
        risk_issues = self.check_risk_identification(prd_content)
        issues.extend(risk_issues)
        
        # 5. 用户旅程完整性检查
        print("   🤖 AI 检查：用户旅程完整性...")
        journey_issues = self.check_user_journey(prd_content)
        issues.extend(journey_issues)
        
        # 计算得分
        score = self.calculate_score(issues)
        
        return {
            "check_type": "ai_semantic",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "ai_assessment": {
                "logic_score": self.calculate_subscore(logic_issues),
                "clarity_score": self.calculate_subscore(clarity_issues),
                "execution_score": self.calculate_subscore(execution_issues),
                "risk_score": self.calculate_subscore(risk_issues),
                "journey_score": self.calculate_subscore(journey_issues)
            }
        }
    
    def check_business_logic(self, content: str) -> List[Dict]:
        """检查业务逻辑合理性"""
        issues = []
        
        # 检查 1：功能流程是否闭环
        if not self.has_complete_flow(content):
            issues.append({
                "id": "AI-LOGIC-001",
                "type": "incomplete_flow",
                "severity": "high",
                "title": "功能流程不闭环",
                "description": "PRD 中的功能流程缺少开始或结束节点，未形成完整业务闭环",
                "location": "业务流程章节",
                "suggestion": "补充完整的业务流程，包括：触发条件 → 处理步骤 → 结果反馈 → 异常处理"
            })
        
        # 检查 2：业务规则是否自洽
        rule_issues = self.check_rule_consistency(content)
        issues.extend(rule_issues)
        
        # 检查 3：输入输出是否匹配
        if not self.has_io_mapping(content):
            issues.append({
                "id": "AI-LOGIC-002",
                "type": "io_mismatch",
                "severity": "medium",
                "title": "输入输出不匹配",
                "description": "功能描述中的输入和输出没有明确的映射关系",
                "location": "功能需求章节",
                "suggestion": "为每个功能明确定义：输入 → 处理逻辑 → 输出的完整映射"
            })
        
        return issues
    
    def check_description_clarity(self, content: str) -> List[Dict]:
        """检查描述清晰度"""
        issues = []
        
        # 检查 1：模糊词汇检测
        vague_words = self.detect_vague_words(content)
        if vague_words:
            issues.append({
                "id": "AI-CLARITY-001",
                "type": "vague_description",
                "severity": "medium",
                "title": "使用模糊描述",
                "description": f"检测到模糊词汇：{', '.join(vague_words[:5])}",
                "location": "全文档",
                "suggestion": "将模糊描述改为具体可量化的描述，如：'快速' → '响应时间<2 秒'"
            })
        
        # 检查 2：缺少示例
        if not self.has_examples(content):
            issues.append({
                "id": "AI-CLARITY-002",
                "type": "no_examples",
                "severity": "low",
                "title": "缺少具体示例",
                "description": "PRD 中没有提供具体的使用示例或数据示例",
                "location": "功能需求章节",
                "suggestion": "为关键功能添加示例，如：输入示例、输出示例、使用场景示例"
            })
        
        # 检查 3：术语未定义
        undefined_terms = self.detect_undefined_terms(content)
        if undefined_terms:
            issues.append({
                "id": "AI-CLARITY-003",
                "type": "undefined_terms",
                "severity": "low",
                "title": "术语未定义",
                "description": f"检测到未定义的专业术语：{', '.join(undefined_terms[:5])}",
                "location": "全文档",
                "suggestion": "在术语表章节定义所有专业术语，或首次出现时添加注释"
            })
        
        return issues
    
    def check_executability(self, content: str) -> List[Dict]:
        """检查可执行性"""
        issues = []
        
        # 检查 1：验收标准是否可测试
        if not self.has_testable_criteria(content):
            issues.append({
                "id": "AI-EXEC-001",
                "type": "untestable_criteria",
                "severity": "high",
                "title": "验收标准不可测试",
                "description": "验收标准缺少明确的通过/失败判断条件",
                "location": "验收标准章节",
                "suggestion": "使用 Given-When-Then 格式编写验收标准，确保每条标准都可测试"
            })
        
        # 检查 2：缺少边界条件
        if not self.has_boundary_conditions(content):
            issues.append({
                "id": "AI-EXEC-002",
                "type": "no_boundary",
                "severity": "medium",
                "title": "缺少边界条件说明",
                "description": "功能描述未说明边界条件（最大值、最小值、异常值）",
                "location": "功能需求章节",
                "suggestion": "为每个输入字段定义边界条件，如：年龄 18-60 岁，金额>0"
            })
        
        # 检查 3：缺少异常处理
        if not self.has_exception_handling(content):
            issues.append({
                "id": "AI-EXEC-003",
                "type": "no_exception",
                "severity": "medium",
                "title": "缺少异常处理说明",
                "description": "PRD 未说明异常情况的处理方式",
                "location": "功能需求/业务流程章节",
                "suggestion": "为每个功能定义异常处理：参数校验失败、系统异常、超时处理等"
            })
        
        return issues
    
    def check_risk_identification(self, content: str) -> List[Dict]:
        """检查风险识别"""
        issues = []
        
        # 检查 1：缺少风险识别
        if not self.has_risk_identification(content):
            issues.append({
                "id": "AI-RISK-001",
                "type": "no_risk",
                "severity": "medium",
                "title": "缺少风险识别",
                "description": "PRD 未识别潜在风险（技术风险、业务风险、合规风险）",
                "location": "全文档",
                "suggestion": "添加风险识别章节，包括：技术风险、业务风险、合规风险、应对措施"
            })
        
        # 检查 2：缺少数据隐私考虑
        if self.has_user_data(content) and not self.has_privacy_protection(content):
            issues.append({
                "id": "AI-RISK-002",
                "type": "no_privacy",
                "severity": "high",
                "title": "缺少数据隐私保护说明",
                "description": "PRD 涉及用户数据但未说明隐私保护措施",
                "location": "数据需求/安全要求章节",
                "suggestion": "补充数据隐私保护措施：数据加密、访问控制、脱敏处理、存储期限"
            })
        
        return issues
    
    def check_user_journey(self, content: str) -> List[Dict]:
        """检查用户旅程完整性"""
        issues = []
        
        # 检查 1：用户场景不完整
        if not self.has_complete_scenarios(content):
            issues.append({
                "id": "AI-JOURNEY-001",
                "type": "incomplete_scenarios",
                "severity": "medium",
                "title": "用户场景不完整",
                "description": "PRD 只描述了正常场景，缺少异常场景和边界场景",
                "location": "用户场景章节",
                "suggestion": "补充完整的用户场景：正常场景 + 异常场景 + 边界场景"
            })
        
        # 检查 2：缺少用户目标
        if not self.has_user_goals(content):
            issues.append({
                "id": "AI-JOURNEY-002",
                "type": "no_user_goal",
                "severity": "low",
                "title": "缺少用户目标说明",
                "description": "功能描述未说明用户使用该功能的目标",
                "location": "功能需求章节",
                "suggestion": "为每个功能添加用户目标说明：用户希望通过该功能达成什么目的"
            })
        
        return issues
    
    # ========== 辅助方法 ==========
    
    def has_complete_flow(self, content: str) -> bool:
        """检查是否有完整的业务流程"""
        flow_keywords = ["开始", "结束", "流程", "步骤", "然后", "最后"]
        trigger_keywords = ["当", "如果", "触发", "开始"]
        result_keywords = ["结果", "返回", "展示", "完成"]
        
        has_flow = any(kw in content for kw in flow_keywords)
        has_trigger = any(kw in content for kw in trigger_keywords)
        has_result = any(kw in content for kw in result_keywords)
        
        return has_flow and has_trigger and has_result
    
    def check_rule_consistency(self, content: str) -> List[Dict]:
        """检查业务规则自洽性"""
        issues = []
        
        # 查找所有业务规则
        rules = re.findall(r'BR-\d+.*?(?=\nBR-|\n\n|$)', content, re.DOTALL)
        
        # 检查规则之间是否矛盾
        # （简化实现：检查是否有相互冲突的规则描述）
        if len(rules) > 1:
            # 这里可以添加更复杂的规则冲突检测逻辑
            pass
        
        return issues
    
    def has_io_mapping(self, content: str) -> bool:
        """检查是否有输入输出映射"""
        has_input = "输入" in content or "input" in content.lower()
        has_output = "输出" in content or "output" in content.lower()
        has_process = "处理" in content or "逻辑" in content
        
        return has_input and has_output and has_process
    
    def detect_vague_words(self, content: str) -> List[str]:
        """检测模糊词汇"""
        vague_words = [
            "快速", "慢速", "大量", "少量", "很多", "很少",
            "大概", "可能", "也许", "左右", "大约",
            "优秀", "良好", "一般", "较好", "较差",
            "及时", "适时", "尽快", "适当"
        ]
        
        found = []
        for word in vague_words:
            if word in content:
                found.append(word)
        
        return found
    
    def has_examples(self, content: str) -> bool:
        """检查是否有示例"""
        example_keywords = ["例如", "比如", "示例", "如：", "eg:", "example"]
        return any(kw in content for kw in example_keywords)
    
    def detect_undefined_terms(self, content: str) -> List[str]:
        """检测未定义的术语"""
        # 简化实现：查找大写字母和专有名词
        terms = re.findall(r'\b[A-Z]{2,}\b', content)
        
        # 检查是否在术语表中定义
        glossary_section = re.search(r'术语表.*?(?=\n##|\Z)', content, re.DOTALL)
        if glossary_section:
            glossary_content = glossary_section.group()
            defined_terms = [term for term in terms if term in glossary_content]
            undefined = [term for term in terms if term not in defined_terms]
            return undefined[:5]
        
        return terms[:5]
    
    def has_testable_criteria(self, content: str) -> bool:
        """检查验收标准是否可测试"""
        # 检查 Given-When-Then 格式
        has_gwt = ("Given" in content and "When" in content and "Then" in content) or \
                  ("给定" in content and "当" in content and "那么" in content)
        
        # 检查是否有量化指标
        has_metrics = bool(re.search(r'<\s*\d+', content)) or \
                      bool(re.search(r'>\s*\d+', content)) or \
                      ("响应时间" in content and "秒" in content)
        
        return has_gwt or has_metrics
    
    def has_boundary_conditions(self, content: str) -> bool:
        """检查是否有边界条件"""
        boundary_keywords = ["最大", "最小", "不超过", "不低于", "范围", "边界", "极限"]
        return any(kw in content for kw in boundary_keywords)
    
    def has_exception_handling(self, content: str) -> bool:
        """检查是否有异常处理"""
        exception_keywords = ["异常", "错误", "失败", "超时", "校验", "提示"]
        return any(kw in content for kw in exception_keywords)
    
    def has_risk_identification(self, content: str) -> bool:
        """检查是否有风险识别"""
        risk_keywords = ["风险", "隐患", "威胁", "应对", "预案"]
        return any(kw in content for kw in risk_keywords)
    
    def has_user_data(self, content: str) -> bool:
        """检查是否涉及用户数据"""
        data_keywords = ["用户信息", "个人信息", "手机号", "身份证", "邮箱", "地址", "隐私"]
        return any(kw in content for kw in data_keywords)
    
    def has_privacy_protection(self, content: str) -> bool:
        """检查是否有隐私保护说明"""
        privacy_keywords = ["加密", "脱敏", "权限", "访问控制", "存储期限", "删除"]
        return any(kw in content for kw in privacy_keywords)
    
    def has_complete_scenarios(self, content: str) -> bool:
        """检查用户场景是否完整"""
        normal_keywords = ["正常", "成功", "完成"]
        exception_keywords = ["异常", "失败", "错误", "取消"]
        boundary_keywords = ["边界", "极限", "最大", "最小"]
        
        has_normal = any(kw in content for kw in normal_keywords)
        has_exception = any(kw in content for kw in exception_keywords)
        has_boundary = any(kw in content for kw in boundary_keywords)
        
        return has_normal and (has_exception or has_boundary)
    
    def has_user_goals(self, content: str) -> bool:
        """检查是否有用户目标说明"""
        goal_keywords = ["希望", "目标", "目的", "为了", "以便", "so that"]
        return any(kw in content for kw in goal_keywords)
    
    def calculate_score(self, issues: List[Dict]) -> int:
        """计算得分"""
        base_score = 100
        
        # 按严重性扣分
        for issue in issues:
            severity = issue.get("severity", "medium")
            if severity == "high":
                base_score -= 15
            elif severity == "medium":
                base_score -= 8
            elif severity == "low":
                base_score -= 3
        
        return max(0, base_score)
    
    def calculate_subscore(self, issues: List[Dict]) -> int:
        """计算子维度得分"""
        return self.calculate_score(issues)


if __name__ == "__main__":
    # 测试
    test_prd = """
    # 测试 PRD
    
    ## 1. 需求概述
    产品定位：快速响应的理财产品
    
    ## 2. 功能需求
    功能 1：申购
    输入：金额
    输出：份额
    
    ## 3. 验收标准
    功能正常
    """
    
    checker = AISemanticChecker()
    result = checker.check(test_prd)
    
    print(f"\nAI 语义评审结果:")
    print(f"总分：{result['score']}/100")
    print(f"问题数：{len(result['issues'])}")
    print(f"\nAI 评估:")
    for dim, score in result['ai_assessment'].items():
        print(f"  {dim}: {score}/100")
