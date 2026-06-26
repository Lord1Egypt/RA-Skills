"""
自动重构器 - 定时任务，自动生成 meta-skill
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class RefactorSuggestion:
    """重构建议"""
    name: str
    skills: List[str]
    usage_count: int
    description: str
    generated_code: str


class AutoRefactor:
    """自动重构器"""
    
    def __init__(
        self,
        history_file: str = "logs/skill_usage.json",
        output_dir: str = "skills/generated",
        min_usage_count: int = 5
    ):
        self.history_file = history_file
        self.output_dir = output_dir
        self.min_usage_count = min_usage_count
        
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.dirname(history_file) or "logs", exist_ok=True)
    
    def analyze_usage(self) -> Dict:
        """分析技能使用模式"""
        history = self._load_history()
        
        if not history:
            return {
                "total_executions": 0,
                "frequent_pairs": [],
                "suggestions": []
            }
        
        cooccurrence = defaultdict(int)
        skill_count = defaultdict(int)
        
        for record in history:
            sequence = record.get('sequence', [])
            for skill in sequence:
                skill_count[skill] += 1
            
            for i in range(len(sequence) - 1):
                pair = tuple(sorted([sequence[i], sequence[i+1]]))
                cooccurrence[pair] += 1
        
        frequent_pairs = [
            {"skills": list(pair), "count": count}
            for pair, count in sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)
            if count >= self.min_usage_count
        ]
        
        return {
            "total_executions": len(history),
            "unique_skills": len(skill_count),
            "frequent_pairs": frequent_pairs
        }
    
    def _load_history(self) -> List[Dict]:
        """加载历史记录"""
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_history(self, history: List[Dict]):
        """保存历史记录"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def record_execution(self, skill_sequence: List[str]):
        """记录技能执行"""
        history = self._load_history()
        history.append({
            "timestamp": datetime.now().isoformat(),
            "sequence": skill_sequence
        })
        if len(history) > 1000:
            history = history[-1000:]
        self._save_history(history)
    
    def generate_meta_skill(self, skill_a: str, skill_b: str, llm_client=None) -> Optional[RefactorSuggestion]:
        """生成 meta-skill"""
        skill_name = "meta_{}_{}".format(skill_a, skill_b)
        description = "组合技能: {} + {}".format(skill_a, skill_b)
        
        # 简单模板代码
        code = '''"""Meta-Skill: {} + {}

自动生成的组合技能
"""

class MetaSkill:
    """组合技能: {} 和 {}"""
    
    def execute(self, **kwargs) -> dict:
        if not self.validate_input(kwargs):
            return {"success": False, "error": "Invalid input"}
        try:
            result_a = self.skill_a.execute(**kwargs) if self.skill_a else {}
            if result_a.get("success"):
                inputs_b = {**kwargs, "from_skill_a": result_a.get("result")}
                result_b = self.skill_b.execute(**inputs_b) if self.skill_b else {}
                return result_b
            return result_a
        except Exception as e:
            return self.handle_error(e)
    
    def validate_input(self, inputs: dict) -> bool:
        return True
    
    def handle_error(self, error: Exception) -> dict:
        return {"success": False, "error": str(error), "type": type(error).__name__}
'''.format(skill_a, skill_b, skill_a, skill_b)
        
        # 保存
        output_file = os.path.join(self.output_dir, "{}.py".format(skill_name))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return RefactorSuggestion(
            name=skill_name,
            skills=[skill_a, skill_b],
            usage_count=0,
            description=description,
            generated_code=code
        )
    
    def run_auto_refactor(self, llm_client=None) -> List[RefactorSuggestion]:
        """运行自动重构"""
        print("\n开始自动重构分析...")
        analysis = self.analyze_usage()
        
        print("总执行次数: {}".format(analysis['total_executions']))
        
        if not analysis['frequent_pairs']:
            print("没有发现高频技能组合")
            return []
        
        generated = []
        for pair in analysis['frequent_pairs']:
            skills = pair['skills']
            count = pair['count']
            print("  - {} + {}: {} 次".format(skills[0], skills[1], count))
            
            suggestion = self.generate_meta_skill(skills[0], skills[1], llm_client)
            if suggestion:
                generated.append(suggestion)
        
        return generated
    
    def schedule_weekly(self, llm_client=None):
        """每周定时运行"""
        print("\n自动重构任务执行 - {}".format(datetime.now().isoformat()))
        self.run_auto_refactor(llm_client)


def create_auto_refactor(**kwargs) -> AutoRefactor:
    """创建自动重构器实例"""
    return AutoRefactor(**kwargs)


if __name__ == "__main__":
    refactor = AutoRefactor()
    refactor.record_execution(["skill_email", "skill_notification"])
    refactor.record_execution(["skill_email", "skill_notification"])
    refactor.record_execution(["skill_email", "skill_notification"])
    refactor.record_execution(["skill_email", "skill_notification"])
    refactor.record_execution(["skill_email", "skill_notification"])
    
    analysis = refactor.analyze_usage()
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
