import os
import re
import json
from typing import Dict, List, Optional

class PromptOptimizer:
    """LLM Prompt Engineering Toolkit - 优化、分析和增强提示词"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.metrics = {}
    
    def _load_templates(self) -> Dict:
        """加载内置提示词模板库"""
        return {
            "chain_of_thought": "Let's think step by step. {task}",
            "few_shot": "Here are some examples:\n{examples}\nNow, {task}",
            "role_playing": "You are an expert in {domain}. {task}",
            "structured_output": "{task}\n\nPlease provide your response in the following format:\n{format}",
            "constraints": "{task}\n\nConstraints:\n- {constraints}",
        }
    
    def analyze(self, prompt: str) -> Dict:
        """分析提示词质量，返回多维度评分"""
        analysis = {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_context": self._check_context(prompt),
            "has_constraints": self._check_constraints(prompt),
            "has_examples": self._check_examples(prompt),
            "has_role": self._check_role(prompt),
            "has_structure": self._check_structure(prompt),
            "clarity_score": self._score_clarity(prompt),
            "specificity_score": self._score_specificity(prompt),
        }
        analysis["overall_score"] = self._calculate_overall(analysis)
        return analysis
    
    def optimize(self, prompt: str, strategy: str = "auto") -> str:
        """使用指定策略优化提示词"""
        if strategy == "auto":
            strategy = self._detect_best_strategy(prompt)
        
        optimizers = {
            "clarity": self._optimize_clarity,
            "specificity": self._optimize_specificity,
            "context": self._add_context,
            "structure": self._add_structure,
            "role": self._add_role,
        }
        
        if strategy in optimizers:
            return optimizers[strategy](prompt)
        return prompt
    
    def apply_template(self, template_name: str, **kwargs) -> str:
        """应用内置提示词模板"""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        return self.templates[template_name].format(**kwargs)
    
    def suggest_improvements(self, prompt: str) -> List[str]:
        """基于分析结果给出改进建议"""
        analysis = self.analyze(prompt)
        suggestions = []
        
        if not analysis["has_context"]:
            suggestions.append("Add background context to help the model understand the scenario")
        if not analysis["has_constraints"]:
            suggestions.append("Specify constraints (length, format, tone) to guide output")
        if not analysis["has_examples"]:
            suggestions.append("Include few-shot examples for better pattern learning")
        if not analysis["has_role"]:
            suggestions.append("Assign a specific role/expertise to the model")
        if analysis["clarity_score"] < 7:
            suggestions.append("Simplify language and break complex instructions into steps")
        if analysis["specificity_score"] < 7:
            suggestions.append("Be more specific about desired output format and content")
        
        return suggestions
    
    def _check_context(self, prompt: str) -> bool:
        context_keywords = ["context", "background", "given", "assume", "scenario", "situation"]
        return any(kw in prompt.lower() for kw in context_keywords)
    
    def _check_constraints(self, prompt: str) -> bool:
        constraint_keywords = ["must", "should", "constraint", "limit", "maximum", "minimum", "exactly", "only"]
        return any(kw in prompt.lower() for kw in constraint_keywords)
    
    def _check_examples(self, prompt: str) -> bool:
        example_keywords = ["example", "sample", "for instance", "e.g.", "such as", "like:"]
        return any(kw in prompt.lower() for kw in example_keywords)
    
    def _check_role(self, prompt: str) -> bool:
        role_patterns = [r"you are (a|an)", r"act as (a|an)", r"role:", r"expert in"]
        return any(re.search(p, prompt.lower()) for p in role_patterns)
    
    def _check_structure(self, prompt: str) -> bool:
        structure_markers = ["1.", "2.", "3.", "- ", "* ", "step", "first", "then", "finally"]
        return any(marker in prompt for marker in structure_markers)
    
    def _score_clarity(self, prompt: str) -> int:
        score = 5
        if len(prompt) < 500: score += 1
        if self._check_structure(prompt): score += 2
        if not any(c in prompt for c in ["???", "...", "etc."]):
            score += 1
        return min(score, 10)
    
    def _score_specificity(self, prompt: str) -> int:
        score = 5
        if self._check_constraints(prompt): score += 2
        if len(prompt) > 50: score += 1
        if any(w in prompt.lower() for w in ["format", "output", "result", "return"]):
            score += 1
        return min(score, 10)
    
    def _calculate_overall(self, analysis: Dict) -> int:
        factors = [
            analysis["clarity_score"],
            analysis["specificity_score"],
            (2 if analysis["has_context"] else 0),
            (2 if analysis["has_constraints"] else 0),
            (1 if analysis["has_examples"] else 0),
            (1 if analysis["has_role"] else 0),
            (1 if analysis["has_structure"] else 0),
        ]
        return min(int(sum(factors) / len(factors)), 10)
    
    def _detect_best_strategy(self, prompt: str) -> str:
        analysis = self.analyze(prompt)
        if analysis["clarity_score"] < 6:
            return "clarity"
        elif analysis["specificity_score"] < 6:
            return "specificity"
        elif not analysis["has_context"]:
            return "context"
        elif not analysis["has_structure"]:
            return "structure"
        return "role"
    
    def _optimize_clarity(self, prompt: str) -> str:
        # 简化复杂句子
        sentences = re.split(r'(?<=[.!?])\s+', prompt)
        optimized = "\n".join(s.strip() for s in sentences if s.strip())
        return f"Instructions (clear and concise):\n{optimized}\n\nPlease follow each step carefully."
    
    def _optimize_specificity(self, prompt: str) -> str:
        return f"{prompt}\n\nPlease be specific and detailed in your response. Include concrete examples where applicable."
    
    def _add_context(self, prompt: str) -> str:
        return f"Context: I need assistance with the following task.\n\n{prompt}"
    
    def _add_structure(self, prompt: str) -> str:
        return f"{prompt}\n\nPlease structure your response with:\n1. Main points\n2. Supporting details\n3. Summary/conclusion"
    
    def _add_role(self, prompt: str) -> str:
        return f"You are an expert assistant. {prompt}"


class PromptLibrary:
    """提示词库管理 - 存储和检索常用提示词"""
    
    def __init__(self, storage_path: str = "prompts.json"):
        self.storage_path = storage_path
        self.prompts = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save(self, name: str, prompt: str, tags: List[str] = None) -> None:
        self.prompts[name] = {
            "prompt": prompt,
            "tags": tags or [],
            "created_at": self._timestamp()
        }
        self._persist()
    
    def get(self, name: str) -> Optional[str]:
        entry = self.prompts.get(name)
        return entry["prompt"] if entry else None
    
    def search(self, tag: str) -> List[Dict]:
        return [
            {"name": name, **data}
            for name, data in self.prompts.items()
            if tag in data.get("tags", [])
        ]
    
    def list_all(self) -> List[str]:
        return list(self.prompts.keys())
    
    def _persist(self) -> None:
        with open(self.storage_path, 'w') as f:
            json.dump(self.prompts, f, indent=2)
    
    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()


if __name__ == "__main__":
    # 演示
    optimizer = PromptOptimizer()
    
    test_prompt = "Write a story about a robot"
    print(f"Original: {test_prompt}")
    print(f"Analysis: {json.dumps(optimizer.analyze(test_prompt), indent=2)}")
    print(f"Optimized: {optimizer.optimize(test_prompt)}")
    print(f"Suggestions: {optimizer.suggest_improvements(test_prompt)}")
    print(f"\nTemplate example: {optimizer.apply_template('role_playing', domain='creative writing', task='Write a sci-fi story')}")
