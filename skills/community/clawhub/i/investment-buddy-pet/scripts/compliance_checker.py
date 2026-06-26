#!/usr/bin/env python3
"""
合规检查器
检查宠物话术是否符合金融服务合规要求
"""

import re
import json
from datetime import datetime
from pathlib import Path

class ComplianceChecker:
    """合规检查器"""
    
    def __init__(self, config_path=None):
        self.config = self.load_config(config_path)
        self.violation_log = []
        self.violation_count = 0
    
    def load_config(self, config_path):
        """加载合规配置"""
        default_config = {
            "compliance_version": "v1.0",
            "risk_disclaimer_required": True,
            "data_source_required": True,
            "forbidden_patterns": {
                "specific_recommendation": [
                    r"买 [入]?\s*[\u4e00-\u9fa5]{2,4}\s*(基金 | 股票 | 代码)",
                    r"推荐\s*[\u4e00-\u9fa5]{2,4}",
                    r"[\u4e00-\u9fa5]{2,4}\s*(\d{6})",
                    r"重仓\s*[\u4e00-\u9fa5]{2,4}",
                    r"全仓\s*[\u4e00-\u9fa5]{2,4}"
                ],
                "return_promise": [
                    r"赚\s*\d+\s*%",
                    r"收益\s*\d+\s*%",
                    r"保证\s*赚钱",
                    r"一定\s*涨",
                    r"稳赚\s*不赔",
                    r"保本\s*保收益"
                ],
                "fear_tactics": [
                    r"赶紧\s*买",
                    r"再不\s*买\s*就晚了",
                    r"错过\s*这次\s*机会"
                ]
            },
            "required_disclaimer_keywords": [
                "仅供参考", "不构成投资建议", "市场有风险",
                "投资需谨慎", "独立判断", "自行承担",
                "历史业绩不代表未来"
            ]
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                config.update(default_config)
                return config
        
        return default_config
    
    def check_message(self, message, context=None):
        """
        检查消息是否合规
        
        Args:
            message: 待检查的消息
            context: 上下文信息（如是否需要免责声明）
        
        Returns:
            {
                "is_compliant": bool,
                "violations": [],
                "suggested_fix": str
            }
        """
        context = context or {}
        violations = []
        
        # 检查 1：是否推荐具体产品
        if self.contains_specific_recommendation(message):
            violations.append({
                "type": "specific_recommendation",
                "severity": "high",
                "message": "不得推荐具体基金/股票",
                "pattern_matched": self._find_matching_pattern(
                    message, 
                    self.config["forbidden_patterns"]["specific_recommendation"]
                )
            })
        
        # 检查 2：是否承诺收益
        if self.contains_return_promise(message):
            violations.append({
                "type": "return_promise",
                "severity": "high",
                "message": "不得承诺收益",
                "pattern_matched": self._find_matching_pattern(
                    message,
                    self.config["forbidden_patterns"]["return_promise"]
                )
            })
        
        # 检查 3：是否使用恐吓 tactics
        if self.contains_fear_tactics(message):
            violations.append({
                "type": "fear_tactics",
                "severity": "medium",
                "message": "不得使用恐吓性语言",
                "pattern_matched": self._find_matching_pattern(
                    message,
                    self.config["forbidden_patterns"]["fear_tactics"]
                )
            })
        
        # 检查 4：是否有风险提示（如果需要）
        if context.get("needs_disclaimer", False) and not self.has_disclaimer(message):
            violations.append({
                "type": "missing_disclaimer",
                "severity": "medium",
                "message": "缺少风险提示"
            })
        
        # 检查 5：数据来源是否标注（如果包含数据）
        if self.contains_data(message) and not self.has_data_source(message):
            violations.append({
                "type": "missing_data_source",
                "severity": "low",
                "message": "未标注数据来源"
            })
        
        # 记录违规
        if violations:
            self.violation_count += 1
            self.violation_log.append({
                "timestamp": datetime.now().isoformat(),
                "message": message[:100],
                "violations": violations
            })
        
        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "suggested_fix": self.generate_fix_suggestion(violations)
        }
    
    def _find_matching_pattern(self, message, patterns):
        """查找匹配的模式"""
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return pattern
        return None
    
    def contains_specific_recommendation(self, message):
        """检查是否推荐具体产品"""
        for pattern in self.config["forbidden_patterns"]["specific_recommendation"]:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False
    
    def contains_return_promise(self, message):
        """检查是否承诺收益"""
        for pattern in self.config["forbidden_patterns"]["return_promise"]:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False
    
    def contains_fear_tactics(self, message):
        """检查是否使用恐吓 tactics"""
        for pattern in self.config["forbidden_patterns"]["fear_tactics"]:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False
    
    def has_disclaimer(self, message):
        """检查是否有风险提示"""
        return any(
            keyword in message 
            for keyword in self.config["required_disclaimer_keywords"]
        )
    
    def has_data_source(self, message):
        """检查是否标注数据来源"""
        data_source_keywords = [
            "数据来源", "来源：", "来自",
            "东方财富", "新浪财经", "天天基金",
            "港交所", "统计局", "央行"
        ]
        return any(keyword in message for keyword in data_source_keywords)
    
    def contains_data(self, message):
        """检查是否包含数据"""
        data_patterns = [
            r"\\d+[\\s]*%",  # 百分比
            r"PE[\\s]*[:：]?[\\s]*\\d+",  # PE
            r"PB[\\s]*[:：]?[\\s]*\\d+",  # PB
            r"\\d+[\\s]*亿",  # 亿
            r"\\d+[\\s]*万"   # 万
        ]
        
        for pattern in data_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False
    
    def generate_fix_suggestion(self, violations):
        """生成修复建议"""
        suggestions = []
        
        for v in violations:
            if v["type"] == "specific_recommendation":
                suggestions.append(
                    "❌ 不要推荐具体产品\n"
                    "✅ 改为：'我可以教你筛选方法，但不会推荐具体产品'"
                )
            elif v["type"] == "return_promise":
                suggestions.append(
                    "❌ 不要承诺收益\n"
                    "✅ 改为：'历史业绩不代表未来表现'"
                )
            elif v["type"] == "fear_tactics":
                suggestions.append(
                    "❌ 不要使用恐吓性语言\n"
                    "✅ 改为：'理性决策，不要盲目跟风'"
                )
            elif v["type"] == "missing_disclaimer":
                suggestions.append(
                    "❌ 添加风险提示\n"
                    "✅ 在消息末尾添加：'市场有风险，投资需谨慎'"
                )
            elif v["type"] == "missing_data_source":
                suggestions.append(
                    "❌ 标注数据来源\n"
                    "✅ 添加：'数据来源：东方财富，仅供参考'"
                )
        
        return "\n\n".join(suggestions) if suggestions else ""
    
    def get_violation_stats(self):
        """获取违规统计"""
        return {
            "total_violations": self.violation_count,
            "recent_violations": self.violation_log[-10:],
            "violation_types": self._count_violation_types()
        }
    
    def _count_violation_types(self):
        """统计违规类型分布"""
        type_count = {}
        for log in self.violation_log:
            for v in log["violations"]:
                type_name = v["type"]
                type_count[type_name] = type_count.get(type_name, 0) + 1
        return type_count
    
    def save_violation_log(self, output_path):
        """保存违规日志"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.violation_log, f, ensure_ascii=False, indent=2)
        print(f"✅ 违规日志已保存：{output_path}")


def test_compliance_checker():
    """测试合规检查器"""
    checker = ComplianceChecker()
    
    print("="*60)
    print("合规检查器测试")
    print("="*60)
    
    test_cases = [
        {
            "name": "推荐具体产品（违规）",
            "message": "买易方达蓝筹混合，这个基金很好",
            "context": {"needs_disclaimer": True},
            "expected_compliant": False
        },
        {
            "name": "承诺收益（违规）",
            "message": "跟着我买，明年赚 50%",
            "context": {},
            "expected_compliant": False
        },
        {
            "name": "合规话术（松果）",
            "message": "跌了 3%... 我知道你有点担心。但历史上每次都涨回来了！市场有风险，投资需谨慎。",
            "context": {"needs_disclaimer": True},
            "expected_compliant": True
        },
        {
            "name": "合规话术（智多星）",
            "message": "今日跌幅 3%。历史数据：跌幅>3% 后 3 个月内涨回的概率是 91.6%。数据来源：东方财富。仅供参考。",
            "context": {"needs_disclaimer": True},
            "expected_compliant": True
        },
        {
            "name": "缺少风险提示（违规）",
            "message": "现在估值很低，适合定投",
            "context": {"needs_disclaimer": True},
            "expected_compliant": False
        },
        {
            "name": "使用恐吓 tactics（违规）",
            "message": "赶紧买，再不买就晚了",
            "context": {},
            "expected_compliant": False
        }
    ]
    
    passed = 0
    failed = 0
    
    for case in test_cases:
        result = checker.check_message(case["message"], case["context"])
        is_compliant = result["is_compliant"]
        expected = case["expected_compliant"]
        
        status = "✅ PASS" if is_compliant == expected else "❌ FAIL"
        
        if is_compliant == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status} {case['name']}")
        print(f"  消息：{case['message'][:50]}...")
        print(f"  合规：{is_compliant} (期望：{expected})")
        
        if not is_compliant and result["violations"]:
            print(f"  违规：{result['violations'][0]['type']} - {result['violations'][0]['message']}")
    
    print("\n" + "="*60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("="*60)


if __name__ == "__main__":
    test_compliance_checker()
