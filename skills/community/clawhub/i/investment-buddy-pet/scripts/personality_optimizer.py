#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物人格自动调优

**功能**：
- 分析用户偏好
- 动态调整宠物人格参数
- 追踪调整后效果

**使用示例**：
```python
from personality_optimizer import PersonalityOptimizer

optimizer = PersonalityOptimizer()

# 分析用户偏好
prefs = optimizer.analyze_user_preference("user_001", "songguo")
print(prefs)

# 调整宠物人格
optimizer.adjust_pet_personality("songguo", prefs)
```
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List


class PersonalityOptimizer:
    """宠物人格自动调优"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "user_preferences"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.interaction_log = Path(__file__).parent.parent / "data" / "interactions.jsonl"
    
    def analyze_user_preference(self, user_id: str, pet_type: str) -> Dict:
        """
        分析用户偏好
        
        Args:
            user_id: 用户 ID
            pet_type: 宠物类型
        
        Returns:
            {
                "prefers_data": True,
                "prefers_stories": False,
                "prefers_direct": True,
                "morning_person": True,
                "night_person": False
            }
        """
        # 读取用户交互历史
        interactions = self._load_user_interactions(user_id, pet_type)
        
        if not interactions:
            return self._get_default_preferences()
        
        # 分析偏好
        preferences = {
            "prefers_data": 0,
            "prefers_stories": 0,
            "prefers_direct": 0,
            "prefers_warm": 0,
            "morning_person": 0,
            "night_person": 0
        }
        
        for log in interactions:
            # 分析时间偏好
            hour = datetime.fromisoformat(log['timestamp']).hour
            if 6 <= hour < 12:
                preferences["morning_person"] += 1
            elif 20 <= hour or hour < 6:
                preferences["night_person"] += 1
            
            # 分析回复长度偏好（长回复 vs 短回复）
            response_len = len(log.get('response', ''))
            if response_len > 200:
                preferences["prefers_data"] += 1
            else:
                preferences["prefers_direct"] += 1
            
            # 分析有帮助的回复特征
            if log.get('helpful') == True:
                # 分析回复中是否包含数据
                if '%' in log.get('response', '') or '历史' in log.get('response', ''):
                    preferences["prefers_data"] += 1
                if '故事' in log.get('response', '') or '比如' in log.get('response', ''):
                    preferences["prefers_stories"] += 1
        
        # 转换为布尔值
        return {
            "prefers_data": preferences["prefers_data"] > preferences["prefers_direct"],
            "prefers_stories": preferences["prefers_stories"] > 0,
            "prefers_direct": preferences["prefers_direct"] > preferences["prefers_data"],
            "prefers_warm": preferences["prefers_warm"] > 0,
            "morning_person": preferences["morning_person"] > preferences["night_person"],
            "night_person": preferences["night_person"] > preferences["morning_person"]
        }
    
    def _load_user_interactions(self, user_id: str, pet_type: str, days: int = 30) -> List[Dict]:
        """加载用户交互历史"""
        interactions = []
        
        if not self.interaction_log.exists():
            return interactions
        
        cutoff = datetime.now() - timedelta(days=days)
        
        with open(self.interaction_log, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    log = json.loads(line)
                    if log.get('user_id') == user_id and log.get('pet_type') == pet_type:
                        log_time = datetime.fromisoformat(log['timestamp'])
                        if log_time >= cutoff:
                            interactions.append(log)
                except:
                    continue
        
        return interactions
    
    def _get_default_preferences(self) -> Dict:
        """默认偏好"""
        return {
            "prefers_data": False,
            "prefers_stories": True,
            "prefers_direct": False,
            "prefers_warm": True,
            "morning_person": True,
            "night_person": False
        }
    
    def adjust_pet_personality(self, pet_type: str, user_preferences: Dict) -> Dict:
        """
        根据用户偏好调整宠物人格
        
        Args:
            pet_type: 宠物类型
            user_preferences: 用户偏好
        
        Returns:
            {
                "status": "success",
                "old_params": {...},
                "new_params": {...}
            }
        """
        # 加载宠物配置
        pets_dir = Path(__file__).parent.parent / "pets"
        pet_file = pets_dir / f"{pet_type}.json"
        
        if not pet_file.exists():
            return {"status": "error", "reason": "宠物配置不存在"}
        
        with open(pet_file, 'r', encoding='utf-8') as f:
            pet_config = json.load(f)
        
        old_params = pet_config.get("personality_traits", {}).copy()
        
        # 调整人格参数
        traits = pet_config.get("personality_traits", {})
        
        # 根据用户偏好调整
        if user_preferences.get("prefers_data"):
            traits["verbosity_level"] = min(100, traits.get("verbosity_level", 50) + 20)
        
        if user_preferences.get("prefers_direct"):
            traits["verbosity_level"] = max(0, traits.get("verbosity_level", 50) - 20)
        
        if user_preferences.get("morning_person"):
            traits["proactivity_level"] = min(100, traits.get("proactivity_level", 50) + 10)
        
        # 保存调整后的配置
        pet_config["personality_traits"] = traits
        with open(pet_file, 'w', encoding='utf-8') as f:
            json.dump(pet_config, f, ensure_ascii=False, indent=2)
        
        return {
            "status": "success",
            "old_params": old_params,
            "new_params": traits
        }
    
    def batch_optimize(self, user_pet_pairs: List[tuple]) -> Dict:
        """
        批量优化多个用户 - 宠物对
        
        Args:
            user_pet_pairs: [(user_id, pet_type), ...]
        
        Returns:
            {
                "optimized_count": 5,
                "results": [...]
            }
        """
        results = []
        
        for user_id, pet_type in user_pet_pairs:
            prefs = self.analyze_user_preference(user_id, pet_type)
            result = self.adjust_pet_personality(pet_type, prefs)
            result["user_id"] = user_id
            results.append(result)
        
        return {
            "optimized_count": len(results),
            "results": results
        }


if __name__ == '__main__':
    # 测试
    optimizer = PersonalityOptimizer()
    
    # 分析偏好
    prefs = optimizer.analyze_user_preference("user_001", "songguo")
    print(f"用户偏好：{prefs}")
    
    # 调整人格
    result = optimizer.adjust_pet_personality("songguo", prefs)
    print(f"调整结果：{result}")
