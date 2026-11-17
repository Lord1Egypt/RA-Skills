#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
character_cognition.py — 角色认知信息差模型

灵感来源: QMAI 的 SoulSkill 角色认知系统
核心思想: 追踪每个角色在每个时间节点的 knows/does_not_know/reader_knows
         防止角色知道不该知道的信息（穿帮）

用法:
  cc = CharacterCognition(book_dir)
  cc.init_character("林北")
  cc.add_knowledge("林北", "系统绑定成功", chapter=1)
  cc.check("林北", "张三的真实身份", chapter=5)  # 返回角色是否应该知道
"""

import json, logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set

_log = logging.getLogger("character_cognition")


class CharacterCognition:
    """角色认知信息差模型"""

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir)
        self._track_dir = self.book_dir / "追踪"
        self._track_dir.mkdir(parents=True, exist_ok=True)
        self._path = self._track_dir / "角色认知.json"
        self._data = self._load()

    def _load(self) -> dict:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"version": "1.0.0", "characters": {}, "global_secrets": []}

    def _save(self):
        self._path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def init_character(self, name: str):
        """初始化一个角色的认知档案"""
        if name not in self._data["characters"]:
            self._data["characters"][name] = {
                "name": name,
                "knows": {},         # {事实: 得知的章节}
                "does_not_know": {}, # {事实: 最后确认不知的章节}
                "suspicions": {},    # {怀疑的事实: 章节}
                "secrets": {},       # {角色持有的秘密: 对谁保密}
                "last_updated": "",
            }
            self._save()

    def add_knowledge(self, name: str, fact: str, chapter: int, source: str = ""):
        """记录角色知道了某个事实"""
        self.init_character(name)
        char = self._data["characters"][name]
        char["knows"][fact] = {
            "chapter": chapter,
            "source": source,
            "timestamp": datetime.now().isoformat(),
        }
        char["last_updated"] = datetime.now().isoformat()
        self._save()

    def mark_unknown(self, name: str, fact: str, chapter: int):
        """标记角色不知道某个事实（用于事后验证）"""
        self.init_character(name)
        char = self._data["characters"][name]
        char["does_not_know"][fact] = chapter
        char["last_updated"] = datetime.now().isoformat()
        self._save()

    def check(self, name: str, fact: str, chapter: int) -> dict:
        """检查角色是否应该知道某个事实

        返回:
          {
            "status": "knows" | "unknown" | "uncertain" | "suspicious",
            "known_since": 章节号（如果知道）,
            "warning": 警告信息（如果可能穿帮）
          }
        """
        if name not in self._data["characters"]:
            return {"status": "uncertain", "warning": f"角色{name}未建立认知档案"}

        char = self._data["characters"][name]

        # 精确匹配
        if fact in char["knows"]:
            k = char["knows"][fact]
            if k["chapter"] <= chapter:
                return {"status": "knows", "known_since": k["chapter"]}
            else:
                return {
                    "status": "unknown",
                    "warning": f"穿帮风险: {name}在第{chapter}章知道{fact}，但记录显示在第{k['chapter']}章才得知",
                }

        # 模糊匹配（部分关键词匹配）
        for known_fact, info in char["knows"].items():
            if self._fuzzy_match(fact, known_fact):
                if info["chapter"] <= chapter:
                    return {"status": "knows", "known_since": info["chapter"], "matched": known_fact}

        # 检查是否在"不知道"列表中
        for unknown_fact in char["does_not_know"]:
            if self._fuzzy_match(fact, unknown_fact):
                return {
                    "status": "unknown",
                    "warning": f"穿帮风险: {name}在第{chapter}章知道了{fact}，但记录显示TA不应该知道",
                }

        # 检查怀疑列表
        for suspicion in char.get("suspicions", {}):
            if self._fuzzy_match(fact, suspicion):
                return {"status": "suspicious", "warning": f"{name}对此有所怀疑但不确定"}

        return {"status": "uncertain"}

    def _fuzzy_match(self, a: str, b: str) -> bool:
        """简单的模糊匹配"""
        # 提取关键词（2字以上中文词）
        import re
        a_words = set(re.findall(r"[\u4e00-\u9fff]{2,}", a))
        b_words = set(re.findall(r"[\u4e00-\u9fff]{2,}", b))
        if not a_words or not b_words:
            return False
        overlap = a_words & b_words
        return len(overlap) >= min(len(a_words), len(b_words)) * 0.5

    def add_suspicion(self, name: str, fact: str, chapter: int):
        """记录角色怀疑某个事实"""
        self.init_character(name)
        char = self._data["characters"][name]
        char["suspicions"][fact] = chapter
        char["last_updated"] = datetime.now().isoformat()
        self._save()

    def add_secret(self, holder: str, secret: str, hidden_from: str, chapter: int):
        """记录角色持有的秘密"""
        self.init_character(holder)
        char = self._data["characters"][holder]
        if "secrets" not in char:
            char["secrets"] = {}
        char["secrets"][secret] = {
            "hidden_from": hidden_from,
            "chapter_established": chapter,
            "revealed": False,
        }
        self._save()

    def add_global_secret(self, secret: str, known_by: List[str], chapter: int):
        """记录全局秘密（多个角色可能知道/不知道）"""
        self._data["global_secrets"].append({
            "secret": secret,
            "known_by": known_by,
            "chapter_revealed_to_reader": chapter,
            "fully_revealed": False,
        })
        self._save()

    def get_character_state(self, name: str) -> Optional[dict]:
        """获取角色认知状态摘要"""
        if name not in self._data["characters"]:
            return None
        char = self._data["characters"][name]
        return {
            "name": name,
            "known_facts": len(char.get("knows", {})),
            "unknown_facts": len(char.get("does_not_know", {})),
            "suspicions": len(char.get("suspicions", {})),
            "secrets_held": len(char.get("secrets", {})),
        }

    def get_knowledge_gap(self, chapter: int) -> List[str]:
        """获取当前章可能的信息差问题（读者知道但角色不知道的）"""
        gaps = []
        for secret in self._data.get("global_secrets", []):
            if secret["chapter_revealed_to_reader"] <= chapter and not secret["fully_revealed"]:
                for name in self._data["characters"]:
                    if name not in secret["known_by"]:
                        # 检查角色是否意外知道了
                        char = self._data["characters"][name]
                        for known_fact in char.get("knows", {}):
                            if self._fuzzy_match(secret["secret"], known_fact):
                                gaps.append(
                                    f"穿帮: {name}知道了'{secret['secret']}'，但TA不应该知道"
                                )
        return gaps
