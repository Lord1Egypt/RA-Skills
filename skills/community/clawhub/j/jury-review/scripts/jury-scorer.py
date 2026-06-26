#!/usr/bin/env python3
"""
评审团评分脚本 - Jury Review Scorer
多维评分 + 周期迭代
"""

import json
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class JudgeScore:
    name: str
    emoji: str
    dimension: str
    score: int
    issues: List[str]
    suggestions: List[str]

class JuryReview:
    """评审团评分系统"""
    
    def __init__(self):
        self.judges = {
            "美学": {"emoji": "🎨", "weight": 0.2, "keywords": ["命名", "结构", "可读性", "风格"]},
            "性能": {"emoji": "⚡", "weight": 0.2, "keywords": ["效率", "复杂度", "算法", "性能", "内存"]},
            "安全": {"emoji": "🔒", "weight": 0.2, "keywords": ["漏洞", "验证", "注入", "安全", "权限"]},
            "测试": {"emoji": "🧪", "weight": 0.2, "keywords": ["测试", "覆盖", "边界", "异常", "单元测试"]},
            "文档": {"emoji": "📝", "weight": 0.2, "keywords": ["注释", "README", "文档", "说明"]},
        }
    
    def detect_dimension(self, text: str) -> str:
        """检测文本涉及哪个维度"""
        text = text.lower()
        scores = {}
        for name, config in self.judges.items():
            score = 0
            for keyword in config["keywords"]:
                if keyword in text:
                    score += 1
            scores[name] = score
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "美学"
    
    def calculate_score(self, issues: List[str], dimension: str) -> int:
        """根据问题列表计算维度分数"""
        base_score = 75  # 基础分
        
        # 严重问题扣分
        critical = ["无", "缺失", "没有", "缺少", "漏洞", "严重", "错误", "崩溃"]
        # 中等问题扣分
        medium = ["不足", "一般", "可优化", "建议", "改进"]
        
        for issue in issues:
            issue_lower = issue.lower()
            if any(c in issue_lower for c in critical):
                base_score -= 15
            elif any(m in issue_lower for m in medium):
                base_score -= 8
        
        return max(0, min(100, base_score))
    
    def generate_feedback(self, scores: Dict[str, int]) -> str:
        """生成评审反馈"""
        total = sum(s["score"] * s["weight"] for s in scores.values())
        
        feedback = f"## 评审结果\n\n"
        feedback += f"**综合得分: {total:.1f} 分**\n\n"
        
        for name, data in scores.items():
            emoji = data["emoji"]
            score = data["score"]
            issues = data.get("issues", [])
            
            status = "✅" if score >= 70 else "⚠️" if score >= 50 else "❌"
            feedback += f"| {emoji} {name} | {score} | {status} |\n"
        
        return feedback
    
    def assess(self, code: str, context: str = "") -> Dict:
        """评估代码"""
        results = {}
        
        # 简单规则检测
        issues = {
            "美学": [],
            "性能": [],
            "安全": [],
            "测试": [],
            "文档": [],
        }
        
        # 检测安全问题
        if "scanf" in code and "%s" in code:
            issues["安全"].append("scanf 使用 %s 可能导致缓冲区溢出")
        if "strcpy" in code or "strcat" in code:
            issues["安全"].append("使用不安全的 strcpy/strcat")
        if "system(" in code:
            issues["安全"].append("使用 system() 调用存在命令注入风险")
        
        # 检测测试
        if "int main" in code and "test" not in code.lower():
            issues["测试"].append("缺少单元测试")
        
        # 检测文档
        if "//" not in code and "/*" not in code:
            issues["文档"].append("缺少代码注释")
        if "#include" in code and "///" not in code:
            issues["文档"].append("缺少文档注释")
        
        # 检测性能
        if re.search(r"for.*for", code):
            issues["性能"].append("存在嵌套循环，可能有性能问题")
        
        # 计算分数
        for dimension, issue_list in issues.items():
            score = self.calculate_score(issue_list, dimension)
            results[dimension] = {
                "emoji": self.judges[dimension]["emoji"],
                "weight": self.judges[dimension]["weight"],
                "score": score,
                "issues": issue_list,
            }
        
        # 计算总分
        total = sum(v["score"] * v["weight"] for v in results.values())
        results["total"] = round(total, 1)
        
        return results


def main():
    if len(sys.argv) < 2:
        print("Usage: jury-scorer.py <code_file>")
        sys.exit(1)
    
    code_file = sys.argv[1]
    
    try:
        with open(code_file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File {code_file} not found")
        sys.exit(1)
    
    jury = JuryReview()
    results = jury.assess(code)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    return results


if __name__ == "__main__":
    main()
