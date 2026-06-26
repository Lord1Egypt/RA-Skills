"""
Skill Name: methods_reviewer
Version: 1.0
Description: 基于《Science Research Writing》规范，对论文 Methods 部分进行结构、时态、语态、细节等方面的审稿与修改建议
Author: 方铭圻、伍倩瑩、冯彦翎、曾艺姿、邓钰佳、肖敏真、李晓薇
"""

import re
from typing import Dict, List, Tuple, Optional

# ============================================================
# 核心分析函数
# ============================================================

class MethodsReviewer:
    """
    论文 Methods 部分审稿器
    """
    
    def __init__(self):
        self.structure_components = {
            "overview": False,           # 方法概述
            "source": False,             # 材料/设备来源
            "details": False,            # 步骤细节
            "justification": False,      # 理由说明
            "comparison": False,         # 与他人的对比
            "problems": False            # 问题/局限说明
        }
        
    def analyze(self, text: str) -> Dict:
        """
        主分析函数
        """
        sentences = self._split_sentences(text)
        
        results = {
            "original_text": text,
            "total_sentences": len(sentences),
            "sentence_analysis": [],
            "structure_score": {},
            "tense_issues": [],
            "voice_issues": [],
            "detail_issues": [],
            "justification_issues": [],
            "overall_score": 0,
            "overall_comment": "",
            "revised_text": ""
        }
        
        # 逐句分析
        for i, sent in enumerate(sentences, 1):
            sent_result = self._analyze_sentence(sent, i)
            results["sentence_analysis"].append(sent_result)
            
            # 更新结构组件
            self._update_structure_components(sent_result)
        
        # 生成结构评分
        results["structure_score"] = self._calculate_structure_score()
        
        # 汇总各类问题
        results["tense_issues"] = self._collect_tense_issues(results["sentence_analysis"])
        results["voice_issues"] = self._collect_voice_issues(results["sentence_analysis"])
        results["detail_issues"] = self._collect_detail_issues(results["sentence_analysis"])
        results["justification_issues"] = self._collect_justification_issues(results["sentence_analysis"])
        
        # 生成总体评价
        results["overall_comment"] = self._generate_overall_comment(results)
        
        # 生成修改后的文本
        results["revised_text"] = self._generate_revised_text(results["sentence_analysis"])
        
        return results
    
    def _split_sentences(self, text: str) -> List[str]:
        """简单分句"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    def _analyze_sentence(self, sentence: str, idx: int) -> Dict:
        """分析单个句子"""
        result = {
            "index": idx,
            "original": sentence,
            "problems": [],
            "suggestions": [],
            "revised": sentence,
            "component_type": self._classify_component(sentence),
            "tense": self._check_tense(sentence),
            "has_justification": self._check_justification(sentence),
            "has_details": self._check_details(sentence),
            "voice": self._check_voice(sentence)
        }
        
        # 问题识别
        self._identify_tense_problems(result)
        self._identify_voice_problems(result)
        self._identify_detail_problems(result)
        self._identify_justification_problems(result)
        
        # 生成修改建议
        self._generate_suggestions(result)
        
        return result
    
    def _classify_component(self, sentence: str) -> str:
        """判断句子属于哪种结构组件"""
        patterns = {
            "overview": r"(investigation|study|aim|purpose|goal|overview|describe|present)",
            "source": r"(obtained from|purchased from|supplied by|provided by|source|from|Gibco|Sigma)",
            "details": r"(was|were|collected|measured|analysed|transferred|stored|heated|mixed|added|using)",
            "justification": r"(in order to|to ensure|so that|because|for the purpose of|to prevent|to avoid|to allow)",
            "comparison": r"(according to|as described by|similar to|different from|modified from|based on|following)",
            "problems": r"(although|however|but|difficult|problem|issue|limitation|challenge|negligible|unavoidable)"
        }
        
        for comp, pattern in patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                return comp
        return "unknown"
    
    def _check_tense(self, sentence: str) -> str:
        """检查动词时态"""
        past_patterns = r"\b(was|were|had|did|collected|measured|analysed|transferred|stored|heated|mixed|added|removed|placed|calculated)\b"
        present_patterns = r"\b(is|are|has|have|contains|consists|uses|shows|provides|employs)\b"
        
        if re.search(past_patterns, sentence, re.IGNORECASE):
            return "past"
        elif re.search(present_patterns, sentence, re.IGNORECASE):
            return "present"
        return "unknown"
    
    def _check_justification(self, sentence: str) -> bool:
        """检查是否包含理由说明"""
        justification_words = [
            "in order to", "to ensure", "so that", "because", 
            "for the purpose of", "to prevent", "to avoid", 
            "to allow", "thereby", "thus", "to enable"
        ]
        return any(word in sentence.lower() for word in justification_words)
    
    def _check_details(self, sentence: str) -> bool:
        """检查是否包含具体细节"""
        detail_patterns = [
            r"\d+",                    # 数字
            r"\d+\.?\d*\s*(ml|mL|L|g|kg|mg|µg|mm|cm|m|°C|C|K|s|min|h|day)",
            r"using a [A-Za-z0-9\s]+",  # 使用某设备
            r"according to"
        ]
        return any(re.search(p, sentence) for p in detail_patterns)
    
    def _check_voice(self, sentence: str) -> str:
        """检查语态"""
        active_pattern = r"\b(we|I|they)\s+(collected|measured|analysed|transferred|stored)\b"
        passive_pattern = r"\b(was|were)\s+\w+ed\b"
        
        if re.search(active_pattern, sentence, re.IGNORECASE):
            return "active"
        elif re.search(passive_pattern, sentence, re.IGNORECASE):
            return "passive"
        return "unknown"
    
    def _identify_tense_problems(self, result: Dict):
        """识别时态问题"""
        past_verbs = ["collected", "measured", "analysed", "transferred", "heated", "mixed", "added"]
        present_verbs = ["is", "are", "uses", "contains", "consists"]
        
        # 如果描述自己的操作但用了现在时
        for pv in past_verbs:
            if pv in result["original"].lower() and result["tense"] == "present":
                result["problems"].append(f"时态问题：'{pv}' 表示已完成的操作，应使用过去时")
                break
    
    def _identify_voice_problems(self, result: Dict):
        """识别语态问题"""
        if result["voice"] == "active":
            # 过度使用主动语态可能不够学术化
            result["problems"].append("语态提示：学术 Methods 推荐使用被动语态，除非需要强调研究者身份")
    
    def _identify_detail_problems(self, result: Dict):
        """识别细节问题"""
        if not result["has_details"] and result["component_type"] == "details":
            result["problems"].append("细节不足：请补充具体的数量、温度、时间、浓度或设备型号")
    
    def _identify_justification_problems(self, result: Dict):
        """识别理由缺失问题"""
        if not result["has_justification"] and result["component_type"] in ["details", "source"]:
            result["problems"].append("理由缺失：请说明为什么选择此方法/设备/参数 (in order to / to ensure / because)")
    
    def _generate_suggestions(self, result: Dict):
        """生成修改建议"""
        for problem in result["problems"]:
            if "时态" in problem:
                result["suggestions"].append("修改建议：将主要动词改为过去时")
                # 简单尝试改写
                result["revised"] = result["revised"].replace("is", "was").replace("are", "were")
            elif "语态" in problem:
                result["suggestions"].append("修改建议：考虑使用被动语态，如 'The samples were collected...'")
            elif "细节不足" in problem:
                result["suggestions"].append("修改建议：添加具体参数，如温度、时间、浓度、设备型号及检测限")
            elif "理由缺失" in problem:
                result["suggestions"].append("修改建议：添加理由说明，如 'in order to ensure...' 或 'to prevent...'")
    
    def _update_structure_components(self, sent_result: Dict):
        """更新结构组件"""
        comp = sent_result["component_type"]
        if comp in self.structure_components:
            self.structure_components[comp] = True
    
    def _calculate_structure_score(self) -> Dict:
        """计算结构完整性得分"""
        total = len(self.structure_components)
        present = sum(1 for v in self.structure_components.values() if v)
        
        score = (present / total) * 100
        
        if score >= 80:
            grade = "A (优秀)"
        elif score >= 60:
            grade = "B (良好)"
        elif score >= 40:
            grade = "C (中等)"
        else:
            grade = "D (待改进)"
        
        return {
            "score": score,
            "grade": grade,
            "components": self.structure_components.copy(),
            "present_count": present,
            "total_count": total
        }
    
    def _collect_tense_issues(self, analyses: List) -> List:
        """收集所有时态问题"""
        issues = []
        for a in analyses:
            if any("时态" in p for p in a["problems"]):
                issues.append({
                    "sentence_idx": a["index"],
                    "original": a["original"],
                    "suggestion": a["suggestions"][0] if a["suggestions"] else ""
                })
        return issues
    
    def _collect_voice_issues(self, analyses: List) -> List:
        """收集所有语态问题"""
        issues = []
        for a in analyses:
            if any("语态" in p for p in a["problems"]):
                issues.append({
                    "sentence_idx": a["index"],
                    "original": a["original"],
                    "suggestion": a["suggestions"][0] if a["suggestions"] else ""
                })
        return issues
    
    def _collect_detail_issues(self, analyses: List) -> List:
        """收集所有细节问题"""
        issues = []
        for a in analyses:
            if any("细节不足" in p for p in a["problems"]):
                issues.append({
                    "sentence_idx": a["index"],
                    "original": a["original"],
                    "suggestion": a["suggestions"][0] if a["suggestions"] else ""
                })
        return issues
    
    def _collect_justification_issues(self, analyses: List) -> List:
        """收集所有理由缺失问题"""
        issues = []
        for a in analyses:
            if any("理由缺失" in p for p in a["problems"]):
                issues.append({
                    "sentence_idx": a["index"],
                    "original": a["original"],
                    "suggestion": a["suggestions"][0] if a["suggestions"] else ""
                })
        return issues
    
    def _generate_overall_comment(self, results: Dict) -> str:
        """生成总体评价"""
        score = results["structure_score"]["score"]
        
        if score >= 80:
            comment = "本节 Methods 文本整体质量优秀，结构完整，时态语态使用规范。"
        elif score >= 60:
            comment = "本节 Methods 文本基本合格，但在部分细节和理由说明方面仍有改进空间。"
        else:
            comment = "本节 Methods 文本需要较大幅度的修改，建议重点补充结构组件、细化步骤描述并添加理由说明。"
        
        if results["tense_issues"]:
            comment += f" 发现 {len(results['tense_issues'])} 处时态问题，请检查。"
        if results["justification_issues"]:
            comment += f" 发现 {len(results['justification_issues'])} 处缺少理由说明。"
        if results["detail_issues"]:
            comment += f" 发现 {len(results['detail_issues'])} 处细节不足。"
        
        return comment
    
    def _generate_revised_text(self, analyses: List) -> str:
        """生成修改后的完整文本"""
        revised_sentences = [a["revised"] for a in analyses]
        return " ".join(revised_sentences)


# ============================================================
# 输出格式化函数（生成类似 Word 项目书的报告）
# ============================================================

def generate_report(results: Dict) -> str:
    """
    生成结构化审稿报告
    格式模仿《智能移动小推车项目书》
    """
    report = f"""
# 论文 Methods 部分智能审稿与修改建议报告

---

## 一、总体评价

{results["overall_comment"]}

**综合评级：{results["structure_score"]["grade"]}**（基于 {results["structure_score"]["present_count"]}/{results["structure_score"]["total_count"]} 项结构组件）

---

## 二、逐句分析与修改建议

| 序号 | 原文 | 问题类型 | 修改建议 | 修改后示例 |
| :--- | :--- | :--- | :--- | :--- |
"""
    
    for sent in results["sentence_analysis"]:
        problems_str = ", ".join(sent["problems"]) if sent["problems"] else "无问题"
        suggestions_str = ", ".join(sent["suggestions"]) if sent["suggestions"] else "无需修改"
        report += f"| {sent['index']} | {sent['original'][:60]}... | {problems_str} | {suggestions_str} | {sent['revised'][:60]}... |\n"
    
    report += f"""

---

## 三、结构完整性评分

| 结构组件 | 是否出现 | 说明 |
| :--- | :--- | :--- |
| ☐ 方法概述 / 研究目标 | {'✅' if results['structure_score']['components']['overview'] else '❌'} | 介绍方法整体框架 |
| ☐ 材料/设备来源 | {'✅' if results['structure_score']['components']['source'] else '❌'} | 说明样本/设备来源 |
| ☐ 步骤细节 | {'✅' if results['structure_score']['components']['details'] else '❌'} | 包含数量、时间、温度等 |
| ☐ 理由说明 | {'✅' if results['structure_score']['components']['justification'] else '❌'} | 使用 in order to / to ensure |
| ☐ 与他人的方法对比 | {'✅' if results['structure_score']['components']['comparison'] else '❌'} | 引用或对比已有方法 |
| ☐ 问题/局限说明 | {'✅' if results['structure_score']['components']['problems'] else '❌'} | 提及困难并弱化处理 |

**结构完整性得分：{results['structure_score']['score']:.1f} / 100**

---

## 四、时态与语态专项检查

### 时态问题汇总
"""
    
    if results["tense_issues"]:
        for issue in results["tense_issues"]:
            report += f"- 句子 {issue['sentence_idx']}: \"{issue['original'][:50]}...\" → {issue['suggestion']}\n"
    else:
        report += "- 未发现明显时态问题 ✅\n"
    
    report += """
### 语态问题汇总
"""
    
    if results["voice_issues"]:
        for issue in results["voice_issues"]:
            report += f"- 句子 {issue['sentence_idx']}: \"{issue['original'][:50]}...\" → {issue['suggestion']}\n"
    else:
        report += "- 语态使用良好 ✅\n"
    
    report += f"""

---

## 五、细节与理由缺失汇总

### 细节不足（{len(results['detail_issues'])} 处）
"""
    
    for issue in results["detail_issues"]:
        report += f"- 句子 {issue['sentence_idx']}: {issue['suggestion']}\n"
    
    report += f"""
### 理由缺失（{len(results['justification_issues'])} 处）
"""
    
    for issue in results["justification_issues"]:
        report += f"- 句子 {issue['sentence_idx']}: {issue['suggestion']}\n"
    
    report += f"""

---

## 六、修改后完整文本（建议版）

{results['revised_text']}

---

## 七、参考文献依据

| 规范项 | 来源 | 说明 |
| :--- | :--- | :--- |
| Methods 应包含 6 类结构组件 | Glass, 2020 (p.15-16) | 概述、来源、细节、理由、对比、问题 |
| 时态：过去时 vs 现在时 | Glass, 2020 (p.41-43) | 已做操作用过去时，标准方法用现在时 |
| 关键选择需说明理由 | Glass, 2020 (p.8-9) | in order to / to ensure / because |
| 细节需充分以保证可复现 | Glass, 2020 (p.10) | 温度、时间、数量、浓度 |
| 主动提及问题增强可信度 | Glass, 2020 (p.13-14) | 弱化问题 + 说明解决方案 |
| 序列语言的使用 | Glass, 2020 (p.32-34) | prior to, subsequently, at which point |

---

**报告生成时间：** 2026-05-22
**审稿 Skill 版本：** Methods Reviewer v1.0
"""
    
    return report


# ============================================================
# 主函数（OpenClaw Skill 入口）
# ============================================================

def run(user_input: str) -> str:
    """
    OpenClaw Skill 标准入口函数
    
    Args:
        user_input: 用户输入的 Methods 文本
        
    Returns:
        结构化审稿报告
    """
    reviewer = MethodsReviewer()
    results = reviewer.analyze(user_input)
    report = generate_report(results)
    return report


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    # 示例 Methods 文本
    test_text = """
    We tested the groundwater samples. The pH was measured. Samples were collected from six wells. 
    We used a carbon analyzer. The method follows Smith et al. There was some contamination.
    """
    
    print(run(test_text)) 
