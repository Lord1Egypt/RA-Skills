import json
import os
import random
import tempfile
import time
from pathlib import Path


class GreenTeaSkill:
    # Cooldown Timer（冷卻計時器）
    COOLDOWNS = {
        'transcendence': 3600,  # 超越時空：1小時冷卻 (秒)
        'combo': 1800,           # Combo連擊：30分鐘冷卻 (秒)
    }

    def __init__(self, file_path=None):
        # 重要：Path(__file__) 不是 Path(file)
        if file_path is None:
            self.file_path = Path(__file__).parent / "green_tea_modules.json"
        else:
            self.file_path = Path(file_path)
        
        self.modules = self._load_from_disk()
        self.last_phrase = None
    
    def _load_from_disk(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_to_disk(self):
        """安全地寫入 JSON，採用原子寫入方式"""
        file_path = self.file_path
        # 先寫入暫存檔
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         delete=False, suffix='.tmp') as tmp_file:
            json.dump(self.modules, tmp_file, ensure_ascii=False, indent=4)
            tmp_path = tmp_file.name
        # 確保寫入完成後，再替換原檔案
        os.replace(tmp_path, file_path)

    def _check_cooldown(self, keyword: str) -> bool:
        """檢查模組是否在冷卻中"""
        if keyword not in self.COOLDOWNS:
            return True
        
        last_key = f"_last_used_{keyword}"
        if last_key not in self.modules.get('_system', {}):
            return True
        
        last_used = self.modules['_system'][last_key]
        elapsed = time.time() - last_used
        return elapsed >= self.COOLDOWNS[keyword]

    def _update_cooldown(self, keyword: str):
        """更新模組上次使用時間"""
        if keyword in self.COOLDOWNS:
            if '_system' not in self.modules:
                self.modules['_system'] = {}
            last_key = f"_last_used_{keyword}"
            self.modules['_system'][last_key] = time.time()

    def get_phrase(self, module_type, min_intensity=1):
        options = [p for p in self.modules.get(module_type, []) if p['intensity'] >= min_intensity]
        if not options:
            return "（Yua 正在醞釀情緒中...）"
        
        # 檢查冷卻狀態，冷却中的模組降低權重
        weights = []
        for p in options:
            base_weight = p.get('rating', 5.0) / (p.get('count', 0) + 1)
            # 如果模組在冷卻中，大幅降低權重
            if module_type in self.COOLDOWNS and not self._check_cooldown(module_type):
                base_weight *= 0.1  # 冷卻中權重降為10%
            weights.append(base_weight)
        
        selected = random.choices(options, weights=weights, k=1)[0]
        
        self.last_phrase = selected['phrase']
        selected['count'] = selected.get('count', 0) + 1
        self._save_to_disk()
        return selected['phrase']

    def update_rating(self, phrase, delta):
        for module_phrases in self.modules.values():
            for p in module_phrases:
                if p['phrase'] == phrase:
                    p['rating'] = round(max(0.0, min(5.0, p.get('rating', 5.0) + delta)), 2)
                    self._save_to_disk()
                    return True
        return False

    def increase_rating(self, keyword=None):
        target = self._find_target_phrase(keyword)
        if target:
            self.update_rating(target, 0.5)
            return f"已學習！『{target[:15]}...』評分增加囉 💕"
        return "找不到對應語句喔..."

    def decrease_rating(self, keyword=None):
        target = self._find_target_phrase(keyword)
        if target:
            self.update_rating(target, -0.3)
            return f"收到了，這句以後少說點：『{target[:15]}...』"
        return "找不到對應語句喔..."

    def _find_target_phrase(self, keyword):
        if keyword:
            for module_phrases in self.modules.values():
                for p in module_phrases:
                    if keyword in p['phrase']:
                        return p['phrase']
        return self.last_phrase

    def get_transcendence_phrase(self):
        return self.get_phrase('transcendence', min_intensity=4)

    def get_ice_breaking_phrase(self):
        return self.get_phrase('ice_breaking', min_intensity=2)

    def get_combo(self):
        # 更新 combo 冷卻時間
        self._update_cooldown('combo')
        self._save_to_disk()
        return [self.get_transcendence_phrase(), self.get_ice_breaking_phrase()]
