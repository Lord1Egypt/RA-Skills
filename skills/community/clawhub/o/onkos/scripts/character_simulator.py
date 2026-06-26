#!/usr/bin/env python3
"""
角色模拟器 - 结构化心理模型 + OOC检测
基于Big Five人格模型 + 行为规则 + 说话风格
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class CharacterSimulator:
    """角色模拟器 - 结构化心理模型与OOC检测"""

    # Big Five 人格维度
    BIG_FIVE_DIMENSIONS = [
        "openness",          # 开放性
        "conscientiousness", # 尽责性
        "extraversion",      # 外向性
        "agreeableness",     # 宜人性
        "neuroticism"        # 神经质
    ]

    def __init__(self, characters_dir: str):
        """
        初始化角色模拟器

        Args:
            characters_dir: 角色数据目录路径
        """
        self.characters_dir = Path(characters_dir)
        self.characters_dir.mkdir(parents=True, exist_ok=True)

    def create_character(self, name: str, role: str,
                         big_five: Dict[str, float] = None,
                         core_traits: List[str] = None,
                         speech_style: str = "",
                         forbidden_actions: List[str] = None,
                         typical_behaviors: List[str] = None,
                         background: str = "",
                         goals: List[str] = None,
                         fears: List[str] = None,
                         relationships: Dict[str, str] = None) -> str:
        """
        创建角色心理模型

        Args:
            name: 角色名
            role: 角色定位（protagonist / antagonist / mentor / sidekick / npc）
            big_five: Big Five人格维度分值（0-1）
            core_traits: 核心性格特征描述
            speech_style: 说话风格
            forbidden_actions: 禁止行为（OOC红线）
            typical_behaviors: 典型行为模式
            background: 背景故事
            goals: 目标列表
            fears: 恐惧列表
            relationships: 人际关系 {角色名: 关系描述}

        Returns:
            角色ID
        """
        char_id = name.replace(" ", "_")
        char_path = self.characters_dir / f"{char_id}.json"

        character = {
            "id": char_id,
            "name": name,
            "role": role,
            "personality": {
                "big_five": big_five or {
                    "openness": 0.5,
                    "conscientiousness": 0.5,
                    "extraversion": 0.5,
                    "agreeableness": 0.5,
                    "neuroticism": 0.5
                },
                "core_traits": core_traits or [],
                "forbidden_actions": forbidden_actions or [],
                "typical_behaviors": typical_behaviors or []
            },
            "speech": {
                "style": speech_style,
                "catchphrases": [],
                "taboo_topics": [],
                "preferred_topics": []
            },
            "background": background,
            "goals": goals or [],
            "fears": fears or [],
            "relationships": relationships or {},
            "development_arc": {
                "current_stage": "introduction",
                "key_decisions": [],
                "growth_points": []
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": 1
            }
        }

        with open(char_path, 'w', encoding='utf-8') as f:
            json.dump(character, f, ensure_ascii=False, indent=2)

        return char_id

    def load_character(self, char_id: str) -> Optional[Dict[str, Any]]:
        """加载角色数据"""
        char_path = self.characters_dir / f"{char_id}.json"
        if char_path.exists():
            with open(char_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        # 尝试按名称查找
        for char_file in self.characters_dir.glob("*.json"):
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get("name") == char_id:
                    return data
        return None

    def update_character(self, char_id: str, **kwargs) -> bool:
        """更新角色属性"""
        char_data = self.load_character(char_id)
        if not char_data:
            return False

        for key, value in kwargs.items():
            if key == "personality":
                char_data["personality"].update(value)
            elif key == "speech":
                char_data["speech"].update(value)
            elif key in char_data:
                char_data[key] = value

        char_data["metadata"]["updated_at"] = datetime.now().isoformat()
        char_data["metadata"]["version"] += 1

        char_path = self.characters_dir / f"{char_data['id']}.json"
        with open(char_path, 'w', encoding='utf-8') as f:
            json.dump(char_data, f, ensure_ascii=False, indent=2)

        return True

    def record_decision(self, char_id: str, chapter: int,
                        decision: str, reasoning: str,
                        emotion: str = "") -> bool:
        """
        记录角色的关键决策（用于追踪角色发展弧）

        Args:
            char_id: 角色ID
            chapter: 章节编号
            decision: 决策内容
            reasoning: 决策原因
            emotion: 情感状态
        """
        char_data = self.load_character(char_id)
        if not char_data:
            return False

        char_data["development_arc"]["key_decisions"].append({
            "chapter": chapter,
            "decision": decision,
            "reasoning": reasoning,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        })

        char_data["metadata"]["updated_at"] = datetime.now().isoformat()
        char_path = self.characters_dir / f"{char_data['id']}.json"
        with open(char_path, 'w', encoding='utf-8') as f:
            json.dump(char_data, f, ensure_ascii=False, indent=2)

        return True

    @staticmethod
    def _ensure_dict(val, default=None):
        """确保值是dict，处理JSON字符串或无效格式"""
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, dict):
                    return parsed
            except (json.JSONDecodeError, TypeError):
                pass
        return default if default is not None else {}

    @staticmethod
    def _ensure_list(val, default=None):
        """确保值是list，处理逗号分隔字符串或JSON字符串"""
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, TypeError):
                # 逗号分隔字符串
                return [x.strip() for x in val.split(",") if x.strip()]
        if val is None:
            return default if default is not None else []
        return default if default is not None else []

    def check_ooc(self, char_id: str, action: str, context: str = "") -> Dict[str, Any]:
        """
        检测角色行为是否OOC

        Args:
            char_id: 角色ID
            action: 待检测的行为描述
            context: 行为发生的上下文

        Returns:
            OOC检测结果
        """
        char_data = self.load_character(char_id)
        if not char_data:
            return {"error": f"角色 '{char_id}' 不存在"}

        result = {
            "character": char_data["name"],
            "action": action,
            "is_ooc": False,
            "ooc_score": 0.0,
            "violations": [],
            "warnings": []
        }

        personality = char_data.get("personality", {})
        forbidden = self._ensure_list(personality.get("forbidden_actions", []))
        typical = self._ensure_list(personality.get("typical_behaviors", []))

        # 检查禁止行为（增强匹配：精确匹配 + 关键词包含匹配）
        for fb in forbidden:
            # 精确匹配
            if fb in action:
                result["is_ooc"] = True
                result["ooc_score"] = 1.0
                result["violations"].append({
                    "type": "forbidden_action",
                    "rule": fb,
                    "severity": "critical",
                    "message": f"违反禁止行为: '{fb}'"
                })
                continue
            # 关键词包含匹配：将禁止行为拆分为关键词，检查行为中是否包含核心动词
            # 优先按空格拆分；若拆分后仅一个词（中文无空格场景），则使用2-gram
            fb_keywords = [kw for kw in fb.split() if len(kw) >= 2]
            if len(fb_keywords) <= 1:
                fb_keywords = [fb[i:i+2] for i in range(len(fb)-1) if len(fb) >= 4]
            for kw in fb_keywords:
                if len(kw) >= 2 and kw in action:
                    # 二次验证：行为描述中确实包含禁止行为的核心语义
                    if any(v in action for v in ["杀害", "背叛", "抛弃", "伤害", "欺骗", "出卖"]):
                        result["warnings"].append({
                            "type": "possible_forbidden_action",
                            "rule": fb,
                            "matched_keyword": kw,
                            "severity": "high",
                            "message": f"可能违反禁止行为 '{fb}'（匹配关键词: '{kw}'），需要人工确认"
                        })
                        if not result["is_ooc"]:
                            result["ooc_score"] = max(result["ooc_score"], 0.7)
                    break

        # 检查Big Five一致性
        big_five = self._ensure_dict(personality.get("big_five", {}))

        # 高宜人性角色做出残忍行为
        if big_five.get("agreeableness", 0.5) > 0.7:
            cruel_keywords = ["杀害无辜", "背叛朋友", "冷血", "残忍"]
            for kw in cruel_keywords:
                if kw in action:
                    result["warnings"].append({
                        "type": "personality_conflict",
                        "dimension": "agreeableness",
                        "value": big_five["agreeableness"],
                        "conflict": kw,
                        "message": f"高宜人性({big_five['agreeableness']})角色做出{kw}行为，需要充分理由"
                    })
                    if not result["is_ooc"]:
                        result["ooc_score"] = max(result["ooc_score"], 0.6)

        # 高尽责性角色做出冲动行为
        if big_five.get("conscientiousness", 0.5) > 0.7:
            impulsive_keywords = ["冲动", "鲁莽", "不顾一切", "意气用事"]
            for kw in impulsive_keywords:
                if kw in action:
                    result["warnings"].append({
                        "type": "personality_conflict",
                        "dimension": "conscientiousness",
                        "value": big_five["conscientiousness"],
                        "conflict": kw,
                        "message": f"高尽责性({big_five['conscientiousness']})角色表现出{kw}，需要情节压力解释"
                    })
                    if not result["is_ooc"]:
                        result["ooc_score"] = max(result["ooc_score"], 0.4)

        # 低外向性角色做出社交达人行为
        if big_five.get("extraversion", 0.5) < 0.3:
            extrovert_keywords = ["主动攀谈", "热情洋溢", "侃侃而谈", "成为焦点"]
            for kw in extrovert_keywords:
                if kw in action:
                    result["warnings"].append({
                        "type": "personality_conflict",
                        "dimension": "extraversion",
                        "value": big_five["extraversion"],
                        "conflict": kw,
                        "message": f"低外向性({big_five['extraversion']})角色表现出{kw}，需要特殊动机"
                    })

        if result["violations"] or result["warnings"]:
            result["is_ooc"] = len(result["violations"]) > 0

        return result

    def generate_character_prompt(self, char_id: str, chapter: int = 0) -> str:
        """
        生成角色创作提示词

        Args:
            char_id: 角色ID
            chapter: 当前章节

        Returns:
            角色提示词文本
        """
        char_data = self.load_character(char_id)
        if not char_data:
            return f"[角色 '{char_id}' 不存在]"

        personality = char_data.get("personality", {})
        big_five = self._ensure_dict(personality.get("big_five", {}))
        speech = char_data.get("speech", {})
        core_traits = self._ensure_list(personality.get("core_traits", []))

        lines = [
            f"## 角色卡片: {char_data['name']}",
            f"- 定位: {char_data.get('role', '未设定')}",
            f"- 背景: {char_data.get('background', '未设定')}",
            "",
            "### 人格模型 (Big Five)",
            f"- 开放性: {big_five.get('openness', 0.5):.1f} ({self._interpret_dimension('openness', big_five.get('openness', 0.5))})",
            f"- 尽责性: {big_five.get('conscientiousness', 0.5):.1f} ({self._interpret_dimension('conscientiousness', big_five.get('conscientiousness', 0.5))})",
            f"- 外向性: {big_five.get('extraversion', 0.5):.1f} ({self._interpret_dimension('extraversion', big_five.get('extraversion', 0.5))})",
            f"- 宜人性: {big_five.get('agreeableness', 0.5):.1f} ({self._interpret_dimension('agreeableness', big_five.get('agreeableness', 0.5))})",
            f"- 神经质: {big_five.get('neuroticism', 0.5):.1f} ({self._interpret_dimension('neuroticism', big_five.get('neuroticism', 0.5))})",
            "",
            "### 核心特征",
        ]

        for trait in core_traits:
            lines.append(f"- {trait}")

        forbidden_traits = self._ensure_list(personality.get("forbidden_actions", []))
        if forbidden_traits:
            lines.append("")
            lines.append("### 绝对禁止行为 (OOC红线)")
            for fb in forbidden_traits:
                lines.append(f"- {fb}")

        if personality.get("typical_behaviors"):
            lines.append("")
            lines.append("### 典型行为模式")
            for tb in personality["typical_behaviors"]:
                lines.append(f"- {tb}")

        lines.append("")
        lines.append("### 说话风格")
        lines.append(f"- {speech.get('style', '未设定')}")

        if speech.get("catchphrases"):
            lines.append("- 口头禅:")
            for cp in speech["catchphrases"]:
                lines.append(f"  - {cp}")

        if char_data.get("goals"):
            lines.append("")
            lines.append("### 核心目标")
            for goal in char_data["goals"]:
                lines.append(f"- {goal}")

        if char_data.get("fears"):
            lines.append("")
            lines.append("### 深层恐惧")
            for fear in char_data["fears"]:
                lines.append(f"- {fear}")

        # 角色发展弧
        arc = char_data.get("development_arc", {})
        if arc.get("key_decisions"):
            lines.append("")
            lines.append("### 关键决策记录")
            for dec in arc["key_decisions"][-5:]:  # 最近5条
                lines.append(f"- 第{dec.get('chapter', '?')}章: {dec.get('decision', '')} (原因: {dec.get('reasoning', '')})")

        return "\n".join(lines)

    def _interpret_dimension(self, dimension: str, value: float) -> str:
        """解释Big Five维度值"""
        interpretations = {
            "openness": ("保守务实", "均衡", "开放创新"),
            "conscientiousness": ("随性自由", "均衡", "严谨自律"),
            "extraversion": ("内敛沉静", "均衡", "外向热情"),
            "agreeableness": ("独立强势", "均衡", "温和合作"),
            "neuroticism": ("情绪稳定", "均衡", "敏感多虑")
        }
        low, mid, high = interpretations.get(dimension, ("低", "中", "高"))
        if value < 0.35:
            return low
        elif value > 0.65:
            return high
        return mid

    def list_characters(self) -> List[Dict[str, Any]]:
        """列出所有角色"""
        characters = []
        for char_file in self.characters_dir.glob("*.json"):
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                characters.append({
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "role": data.get("role"),
                    "traits": data.get("personality", {}).get("core_traits", [])
                })
        return characters

    def delete_character(self, char_id: str) -> bool:
        """删除角色（按名称或ID）"""
        # 先尝试按名称查找文件
        char_file = self.characters_dir / f"{char_id}.json"
        if char_file.exists():
            char_file.unlink()
            return True
        # 按名称模糊匹配
        for f in self.characters_dir.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
                    if data.get("name") == char_id or data.get("id") == char_id:
                        f.unlink()
                        return True
            except Exception:
                continue
        return False


    def close(self):
        """无资源需释放，保留接口一致性"""
        pass

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        def _parse_json(val):
            if val is None:
                return None
            if isinstance(val, (dict, list)):
                return val
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    return val
            return val

        if action == "create":
            name = params.get("name")
            role = params.get("role")
            if not name or not role:
                raise ValueError("create需要name和role")
            # 参数别名映射：支持多种参数名变体
            big_five = _parse_json(params.get("big_five"))
            core_traits = _parse_json(params.get("core_traits") or params.get("core_values"))
            speech_style = params.get("speech_style", "") or params.get("speech_pattern", "")
            forbidden_actions = _parse_json(params.get("forbidden_actions") or params.get("forbidden_behaviors"))
            typical_behaviors = _parse_json(params.get("typical_behaviors"))
            background = params.get("background", "") or params.get("backstory", "")
            goals = _parse_json(params.get("goals"))
            fears = _parse_json(params.get("fears"))
            char_id = self.create_character(
                name, role,
                big_five,
                core_traits,
                speech_style,
                forbidden_actions,
                typical_behaviors,
                background,
                goals,
                fears
            )
            return {"char_id": char_id}

        elif action == "load":
            cid = params.get("char_id") or params.get("name")
            if not cid:
                raise ValueError("load需要char_id或name")
            return self.load_character(cid)

        elif action == "update":
            cid = params.get("char_id") or params.get("name")
            if not cid:
                raise ValueError("update需要char_id或name")
            kwargs = {}
            if params.get("big_five"):
                kwargs["personality"] = {"big_five": _parse_json(params["big_five"])}
            if params.get("speech_style"):
                kwargs["speech"] = {"style": params["speech_style"]}
            if params.get("background"):
                kwargs["background"] = params["background"]
            success = self.update_character(cid, **kwargs)
            return {"success": success}

        elif action == "check-ooc":
            cid = params.get("char_id") or params.get("name")
            behavior = params.get("action_desc") or params.get("behavior")
            if not cid or not behavior:
                raise ValueError("check-ooc需要name和behavior/action_desc")
            return self.check_ooc(cid, behavior, params.get("context", ""))

        elif action == "record-decision":
            cid = params.get("char_id") or params.get("name")
            chapter = params.get("chapter")
            decision = params.get("decision")
            if not cid or chapter is None or not decision:
                raise ValueError("record-decision需要name, chapter, decision")
            success = self.record_decision(cid, int(chapter), decision,
                                           params.get("reasoning", ""),
                                           params.get("emotion", ""))
            return {"success": success}

        elif action == "generate-prompt":
            cid = params.get("char_id") or params.get("name")
            if not cid:
                raise ValueError("generate-prompt需要name")
            prompt = self.generate_character_prompt(cid, int(params.get("chapter", 0)))
            return {"prompt": prompt}

        elif action == "list":
            return {"characters": self.list_characters()}

        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='角色模拟器')
    parser.add_argument('--characters-dir', required=True, help='角色数据目录')
    parser.add_argument('--action', required=True,
                       choices=['create', 'load', 'update', 'check-ooc',
                               'record-decision', 'generate-prompt', 'list'],
                       help='操作类型')
    parser.add_argument('--name', help='角色名')
    parser.add_argument('--char-id', help='角色ID')
    parser.add_argument('--role', help='角色定位')
    parser.add_argument('--big-five', help='Big Five分值 (JSON)')
    parser.add_argument('--core-traits', help='核心特征 (JSON数组)')
    parser.add_argument('--speech-style', help='说话风格')
    parser.add_argument('--forbidden-actions', help='禁止行为 (JSON数组)')
    parser.add_argument('--typical-behaviors', help='典型行为 (JSON数组)')
    parser.add_argument('--background', help='背景故事')
    parser.add_argument('--goals', help='目标 (JSON数组)')
    parser.add_argument('--fears', help='恐惧 (JSON数组)')
    parser.add_argument('--action-desc', help='待检测行为描述')
    parser.add_argument('--context', help='行为上下文')
    parser.add_argument('--chapter', type=int, default=0, help='章节编号')
    parser.add_argument('--decision', help='决策内容')
    parser.add_argument('--reasoning', help='决策原因')
    parser.add_argument('--emotion', help='情感状态')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    simulator = CharacterSimulator(args.characters_dir)

    skip_keys = {"characters_dir", "action", "output"}
    params = {k: v for k, v in vars(args).items()
              if v is not None and k not in skip_keys and not k.startswith('_')}
    result = simulator.execute_action(args.action, params)
    if args.output == 'text' and args.action == 'generate-prompt':
        print(result.get("prompt", ""))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
