#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
character_state_engine.py — 角色状态机锁定算法引擎

参考：《网络小说全维度创新创作与AI工业化稳态落地深度研究报告（进阶迭代版）》
第4章 §4.1.2 角色状态机锁定算法

核心功能：
  - 角色参数台账（性格固定值/情绪浮动值/能力等级/关系数值）
  - 状态变更权限管控（无剧情触发禁止擅自修改）
  - 参数校验（AI生成内容前校验，不符合状态参数的行为自动驳回）
  - 人设动态成长但不崩塌
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

_log = logging.getLogger("character_state_engine")

# 默认角色参数模板
CHARACTER_TEMPLATE = {
    # 固定值（不会轻易改变）
    "personality": {
        "bravery": 5,           # 勇气 1-10
        "intelligence": 5,      # 智力 1-10
        "kindness": 5,          # 善良 1-10
        "stubbornness": 5,      # 固执 1-10
        "caution": 5,           # 谨慎 1-10
    },
    # 浮动值（随剧情变化）
    "emotion": {
        "mood": 5,              # 心情 1-10 (1=极差, 10=极好)
        "stress": 5,            # 压力 1-10
        "trust_to_party": 5,    # 对阵营信任度 1-10
    },
    # 能力等级
    "ability": {
        "level": 1,             # 等级
        "power": 10,            # 战力值
        "skill_count": 0,       # 技能数
    },
    # 关系数值（存人名->亲密度）
    "relationships": {},
    # 核心执念（永不改变）
    "core_drive": "",
    # 底线（违反会导致人设崩塌）
    "bottom_lines": [],
}

# 允许的最大单次变更幅度
MAX_CHANGE_PER_EVENT = {
    "personality": 2,    # 性格固定值单次最多变2
    "emotion": 3,        # 情绪浮动值单次最多变3
    "ability": 5,        # 能力单次最多变5
}



def _self_check_char(c: dict, name: str, issues: list):
    """角色设计自审"""
    goal = c.get('goal', '') or c.get('obsession', '')
    weakness = c.get('weakness', '')
    secret = c.get('secret', '')
    if len(goal) < 5:
        issues.append(f"[P1] [{name}] 执念目标不清晰")
    if weakness and len(weakness) < 8:
        issues.append(f"[P2] [{name}] 弱点太简单")
    if not secret:
        issues.append(f"[P2] [{name}] 缺少反差秘密")
    if not c.get('motivation', ''):
        issues.append(f"[P1] [{name}] 缺少行为动机")

class CharacterStateEngine:
    """角色状态机锁定算法引擎"""

    def __init__(self):
        self._characters: Dict[str, Dict] = {}
        self._change_log: List[Dict] = []
        self._locked = False  # 设定锁死模式

    # ========== 角色初始化 ==========

    def register_character(self, name: str, template: Optional[Dict] = None) -> Dict:
        """注册新角色，返回角色参数"""
        if name in self._characters:
            return self._characters[name]

        char = {}
        if template:
            char = template
        else:
            # 使用模板初始化
            import copy
            char = copy.deepcopy(CHARACTER_TEMPLATE)

        char["_name"] = name
        char["_created_at"] = datetime.now().isoformat()
        char["_last_update"] = datetime.now().isoformat()
        char["_version"] = 1
        char["_change_history"] = []

        self._characters[name] = char
        _log.info(f"角色注册: {name}")
        return char

    # ========== 参数读取 ==========

    def get_character(self, name: str) -> Optional[Dict]:
        return self._characters.get(name)

    def get_param(self, name: str, category: str, key: str) -> Any:
        """获取角色特定参数"""
        char = self._characters.get(name)
        if not char:
            return None
        return char.get(category, {}).get(key)

    def get_character_summary(self, name: str) -> str:
        """生成角色摘要文本（用于注入生成 prompt）"""
        char = self._characters.get(name)
        if not char:
            return ""

        p = char.get("personality", {})
        e = char.get("emotion", {})
        a = char.get("ability", {})
        r = char.get("relationships", {})

        rel_text = "; ".join(f"{k}(亲密度{v})" for k, v in list(r.items())[:5]) if r else "无"

        return (
            f"{name}: 勇{p.get('bravery',5)}/智{p.get('intelligence',5)}/"
            f"善{p.get('kindness',5)}/固{p.get('stubbornness',5)}/慎{p.get('caution',5)}"
            f", 情绪:{e.get('mood',5)}/压力{e.get('stress',5)}"
            f", 等级{a.get('level',1)}/战力{a.get('power',10)}"
            f", 关系: {rel_text}"
            f", 执念: {char.get('core_drive', '无')}"
        )

    # ========== 状态变更（带权限管控） ==========

    def update_character(
        self,
        name: str,
        category: str,
        key: str,
        value: Any,
        reason: str = "",
        chapter: int = 0,
    ) -> Tuple[bool, str]:
        """更新角色参数，返回 (成功否, 消息)

        核心管控：
        - 无剧情触发原因禁止变更
        - 单次变更幅度不得超过 MAX_CHANGE_PER_EVENT
        - 锁死模式下不得修改 personality 固定值
        """
        char = self._characters.get(name)
        if not char:
            return False, f"角色 {name} 不存在"

        # 检查变更原因
        if not reason:
            return False, f"无变更原因，禁止修改 {name}.{category}.{key}"

        if category not in char:
            return False, f"类别 {category} 不存在"

        if key not in char.get(category, {}):
            # 允许新增 key（如关系绑定）
            if category == "relationships":
                char[category][key] = value
                self._record_change(name, category, key, None, value, reason, chapter)
                return True, f"{name}.{category}.{key} = {value}"
            return False, f"键 {key} 不存在于 {category}"

        old_value = char[category][key]

        # 锁死模式检查
        if self._locked and category == "personality":
            return False, f"锁死模式: 禁止修改 {name} 的性格固定值 {key}"

        # 变更幅度检查
        max_change = MAX_CHANGE_PER_EVENT.get(category)
        if max_change is not None and isinstance(old_value, (int, float)) and isinstance(value, (int, float)):
            change = abs(value - old_value)
            if change > max_change:
                return False, (
                    f"变更幅度 {change} 超过上限 {max_change}，"
                    f"禁止 {name}.{category}.{key}: {old_value}->{value}"
                )

        # 执行变更
        char[category][key] = value
        char["_version"] += 1
        char["_last_update"] = datetime.now().isoformat()
        self._record_change(name, category, key, old_value, value, reason, chapter)

        _log.info(f"角色状态变更: {name}.{category}.{key}: {old_value} -> {value} ({reason})")
        return True, f"{name}.{category}.{key}: {old_value} -> {value}"

    def _record_change(self, name, category, key, old_val, new_val, reason, chapter):
        self._change_log.append({
            "name": name, "category": category, "key": key,
            "old": old_val, "new": new_val,
            "reason": reason, "chapter": chapter,
            "ts": datetime.now().isoformat(),
        })

    # ========== 批量检查 ==========

    def validate_text_against_characters(self, text: str, chapter: int) -> List[str]:
        """校验文本中角色行为是否匹配当前状态参数"""
        issues = []
        for name, char in self._characters.items():
            if name not in text:
                continue

            # 检查性格矛盾
            p = char.get("personality", {})
            if p.get("bravery", 5) < 3 and ("冲" in text or "杀" in text):
                # 寻找该角色名附近的"冲/杀"
                import re
                for idx in re.finditer(re.escape(name), text):
                    start, end = max(0, idx.start() - 50), min(len(text), idx.end() + 50)
                    context = text[start:end]
                    if "冲" in context or "杀" in context or "战斗" in context:
                        issues.append(
                            f"[人设] {name} 勇气值 {p['bravery']} 偏低，"
                            f"但附近出现了进攻性行为"
                        )
                        break

            # 检查情绪合理性
            e = char.get("emotion", {})
            if e.get("mood", 5) > 7:
                # 情绪好时不应该有绝望行为
                if any(w in text for w in ["绝望", "想死", "完了", "放弃吧"]):
                    issues.append(f"[人设] {name} 当前心情 {e['mood']}，但出现负面绝望情绪")

        return issues

    # ========== 设定锁死/解锁 ==========

    def lock(self):
        """锁死模式：禁止修改性格固定值"""
        self._locked = True
        _log.info("角色状态机: 已锁死")

    def unlock(self):
        """解锁模式：允许修改性格固定值（需合理剧情触发）"""
        self._locked = False
        _log.info("角色状态机: 已解锁")

    # ========== 持久化 ==========

    def to_dict(self) -> dict:
        return {
            "characters": self._characters,
            "change_log": self._change_log[-200:],  # 保留最近200条
            "locked": self._locked,
        }

    def load_from_dict(self, data: dict):
        self._characters = data.get("characters", {})
        self._change_log = data.get("change_log", [])
        self._locked = data.get("locked", False)
        _log.info(f"CharacterStateEngine: loaded {len(self._characters)} characters")

    def save_to_file(self, book_dir: str):
        path = Path(book_dir) / "追踪" / "character_state.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def load_from_file(self, book_dir: str):
        path = Path(book_dir) / "追踪" / "character_state.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self.load_from_dict(data)
            except Exception as e:
                _log.warning(f"CharacterStateEngine: 加载失败 {e}")

    
    def get_design_formula(self, name: str) -> str:
        c = self._characters.get(name)
        if not c:
            return ''
        tags = c.get('tags', [])
        parts = [
            '身份标签: ' + (tags[0] if tags else '?'),
            '执念目标: ' + (c.get('goal','') or c.get('obsession','') or '?')[:40],
            '致命弱点: ' + (c.get('weakness','') or '?')[:40],
            '反差秘密: ' + (c.get('secret','') or '?')[:40],
        ]
        return ' | '.join(parts)

    def get_arc_path(self, name: str) -> list:
        c = self._characters.get(name)
        if not c:
            return []
        return [
            '过去创伤: ' + (c.get('past_trauma','?') or '?')[:50],
            '现在准则: ' + (c.get('current_principle','?') or '?')[:50],
            '未来弧光: ' + (c.get('future_arc','?') or '?')[:50],
        ]

    def check_show_dont_tell(self, text: str, name: str) -> list:
        issues = []
        c = self._characters.get(name)
        if not c:
            return issues
        import re
        pattern = name + '[是是][个个一一](?:[^\u3002]{0,30})(?:的人|的性格)'
        direct_tell = re.findall(pattern, text[:2000])
        for t in direct_tell:
            issues.append('[P1] Show-Dont-Tell: 旁白直接说明性格')
        psycho = re.findall('[\u5fc3\u60f3][^\u3002]{10,50}[\u3002]', text[:3000])
        if len(psycho) > 3:
            issues.append('[P2] 大段心理描写代替行动')
        return issues

    def create_from_formula(self, name, identity='', obsession='',
                            weakness='', secret='',
                            past_trauma='', current_principle='',
                            future_arc=''):
        template = {
            'tags': [identity] if identity else [],
            'goal': obsession,
            'weakness': weakness,
            'secret': secret,
            'past_trauma': past_trauma,
            'current_principle': current_principle,
            'future_arc': future_arc,
            'motivation': obsession,
        }
        return self.register_character(name, template)

    def reset(self):
        self._characters.clear()
        self._change_log.clear()
        self._locked = False
