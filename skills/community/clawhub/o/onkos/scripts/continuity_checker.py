#!/usr/bin/env python3
"""
连续性检查器 - 检测OOC、逻辑矛盾、事实冲突、位置矛盾
基于 SQLite 事实表 + 角色心理模型 + 知识图谱 + 伏笔追踪
2000章架构: 双层OOC检测（字符串匹配+智能体裁判决）+ 位置连续性
"""

import os
import json
import sqlite3
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class ContinuityChecker:
    """连续性检查器 - 保证千万字级别的一致性"""

    # 题材→修为等级映射（空列表表示该题材不做修为退化检测）
    GENRE_POWER_LEVELS = {
        "fantasy": [
            "淬体", "练气", "筑基", "金丹", "元婴",
            "化神", "返虚", "合体", "大乘", "渡劫"
        ],
        "wuxia": [
            "三流", "二流", "一流", "后天", "先天",
            "宗师", "大宗师", "绝顶", "化境", "天人"
        ],
        "urban": [],
        "scifi": [],
    }

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.db_path = self.project_path / "data" / "novel_memory.db"
        self.characters_path = self.project_path / "data" / "characters"
        self._fact_engine = None
        self._genre = self._detect_genre()

    @property
    def fact_engine(self):
        """延迟创建并复用 FactEngine 实例"""
        if self._fact_engine is None:
            from fact_engine import FactEngine
            self._fact_engine = FactEngine(str(self.db_path), project_path=str(self.project_path))
        return self._fact_engine

    def _detect_genre(self) -> str:
        """从项目配置检测题材"""
        config_path = self.project_path / "data" / "project_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    import json
                    cfg = json.load(f)
                return cfg.get("genre", "fantasy")
            except Exception:
                pass
        return "fantasy"

    def close(self):
        """释放资源"""
        if self._fact_engine is not None:
            self._fact_engine.close()
            self._fact_engine = None

    def _read_chapter_content(self, chapter: int) -> str:
        """从数据库读取指定章节的所有场景内容"""
        try:
            import sqlite3
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT content FROM scenes_content WHERE chapter = ? ORDER BY id",
                    (chapter,))
                rows = cur.fetchall()
                return "\n".join(row["content"] for row in rows if row["content"])
            finally:
                conn.close()
        except Exception:
            return ""

    def check_chapter(self, chapter: int, chapter_content: str) -> Dict[str, Any]:
        report = {
            "chapter": chapter,
            "passed": True,
            "issues": [],
            "warnings": [],
            "info": []
        }

        # 1. 事实矛盾检查
        fact_issues = self._check_fact_contradictions(chapter, chapter_content)
        report["issues"].extend(fact_issues)

        # 2. 角色OOC检查（双层：字符串+智能体裁）
        ooc_issues = self._check_ooc(chapter, chapter_content)
        report["issues"].extend(ooc_issues)

        # 3. 修为退化检查
        power_issues = self._check_power_regression(chapter, chapter_content)
        report["issues"].extend(power_issues)

        # 4. 位置矛盾检查
        location_issues = self._check_location_contradictions(chapter, chapter_content)
        report["issues"].extend(location_issues)

        # 5. 伏笔状态检查
        hook_warnings = self._check_hook_status(chapter)
        report["warnings"].extend(hook_warnings)

        if report["issues"]:
            report["passed"] = False

        return report

    def _check_fact_contradictions(self, chapter: int, content: str) -> List[Dict]:
        issues = []

        try:
            contradictions = self.fact_engine.detect_contradictions()
            for c in contradictions:
                issues.append({
                    "type": "fact_contradiction",
                    "severity": "high",
                    "entity": c["entity"],
                    "attribute": c["attribute"],
                    "count": c["cnt"],
                    "message": f"实体 '{c['entity']}' 的属性 '{c['attribute']}' 存在 {c['cnt']} 个矛盾值"
                })

            # 修为变化检测（仅当题材有修为体系时生效）
            power_levels = self.GENRE_POWER_LEVELS.get(self._genre, [])
            if power_levels:
                power_patterns = [
                    r"突破.{0,4}(" + "|".join(power_levels) + ")",
                    r"踏入.{0,4}(" + "|".join(power_levels) + ")",
                    r"修为.{0,4}(提升|精进|达到).{0,4}(" + "|".join(power_levels) + ")",
                ]

                for pattern in power_patterns:
                    for m in re.finditer(pattern, content):
                        level = m.group(1)
                        start = max(0, m.start() - 50)
                        context_before = content[start:m.start()]
                        characters = self._find_characters_in_text(context_before)
                        for char_name in characters:
                            current_level = self.fact_engine.get_fact(char_name, "修为")
                            if current_level:
                                if self._is_power_regression(current_level, level):
                                    issues.append({
                                        "type": "power_regression",
                                        "severity": "high",
                                        "entity": char_name,
                                        "old_level": current_level,
                                        "new_level": level,
                                        "message": f"{char_name}的修为从'{current_level}'退化为'{level}'"
                                    })
        except Exception:
            pass

        return issues

    def _check_ooc(self, chapter: int, content: str) -> List[Dict]:
        """双层OOC检测: 第一层字符串匹配，第二层智能体裁判决"""
        issues = []

        if not self.characters_path.exists():
            return issues

        for char_file in self.characters_path.glob("*.json"):
            with open(char_file, 'r', encoding='utf-8') as f:
                char_data = json.load(f)

            char_name = char_data.get("name", "")
            if not char_name or char_name not in content:
                continue

            # 第一层: 禁止行为字符串匹配（增强：精确匹配 + 关键词包含）
            personality = char_data.get("personality", {})
            forbidden = personality.get("forbidden_actions", [])

            for forbidden_action in forbidden:
                # 精确匹配
                if forbidden_action in content:
                    issues.append({
                        "type": "ooc_forbidden_action",
                        "severity": "high",
                        "entity": char_name,
                        "action": forbidden_action,
                        "layer": "string_match",
                        "message": f"{char_name}执行了禁止行为: '{forbidden_action}'"
                    })
                    continue
                # 关键词包含匹配：检查角色附近是否出现了禁止行为的核心动词
                fb_keywords = [kw for kw in forbidden_action.split() if len(kw) >= 2]
                if not fb_keywords and len(forbidden_action) >= 4:
                    fb_keywords = [forbidden_action[i:i+2] for i in range(len(forbidden_action)-1)]
                for kw in fb_keywords:
                    if len(kw) >= 2 and kw in content:
                        nearby = self._get_nearby_text(content, kw, 100)
                        if char_name in nearby:
                            issues.append({
                                "type": "ooc_possible_forbidden_action",
                                "severity": "medium",
                                "entity": char_name,
                                "action": forbidden_action,
                                "matched_keyword": kw,
                                "layer": "keyword_match",
                                "message": f"{char_name}可能执行了禁止行为 '{forbidden_action}'（匹配: '{kw}'），需确认"
                            })
                            break

            # 第二层: Big Five 人格冲突（智能体裁判决提示）
            big_five = personality.get("big_five", {})
            if big_five:
                # 高宜人性 + 残忍行为
                if big_five.get("agreeableness", 0.5) > 0.7:
                    cruel_kw = ["杀害无辜", "背叛朋友", "冷血", "残忍", "无情"]
                    for kw in cruel_kw:
                        if kw in content and char_name in self._get_nearby_text(content, kw, 100):
                            issues.append({
                                "type": "ooc_personality_conflict",
                                "severity": "medium",
                                "entity": char_name,
                                "dimension": "agreeableness",
                                "conflict": kw,
                                "layer": "personality_judgment",
                                "message": f"{char_name}(高宜人性)做出{kw}行为，需要情节压力解释"
                            })
                            break

                # 高尽责性 + 冲动行为
                if big_five.get("conscientiousness", 0.5) > 0.7:
                    impulsive_kw = ["冲动", "鲁莽", "不顾一切", "意气用事"]
                    for kw in impulsive_kw:
                        if kw in content and char_name in self._get_nearby_text(content, kw, 100):
                            issues.append({
                                "type": "ooc_personality_conflict",
                                "severity": "low",
                                "entity": char_name,
                                "dimension": "conscientiousness",
                                "conflict": kw,
                                "layer": "personality_judgment",
                                "message": f"{char_name}(高尽责性)表现出{kw}，需情节压力解释"
                            })
                            break

        return issues

    def _get_nearby_text(self, content: str, keyword: str, radius: int) -> str:
        """获取关键词附近的文本（用于判断角色关联）"""
        idx = content.find(keyword)
        if idx < 0:
            return ""
        start = max(0, idx - radius)
        end = min(len(content), idx + len(keyword) + radius)
        return content[start:end]

    def _check_power_regression(self, chapter: int, content: str) -> List[Dict]:
        return []

    def _check_location_contradictions(self, chapter: int, content: str) -> List[Dict]:
        """位置矛盾检查: 检测同一角色在同一章内出现在不同地点"""
        from memory_engine import MemoryEngine
        engine = MemoryEngine(str(self.db_path), project_path=str(self.project_path))

        issues = []
        try:
            # 提取位置变化（[^，。！；]避免跨句匹配）
            location_patterns = [
                r"(来到|抵达|到达|回到|返回|赶往|飞向)([^，。！；]{1,8})(，|。|！|；)",
                r"(离开|出发|逃离)([^，。！；]{1,8})(，|。|！|；)",
            ]

            locations_found = []
            for pattern in location_patterns:
                for m in re.finditer(pattern, content):
                    verb = m.group(1)
                    place = m.group(2)
                    # 查找附近的角色
                    start = max(0, m.start() - 80)
                    context_before = content[start:m.start()]
                    characters = self._find_characters_in_text(context_before)
                    if characters:
                        locations_found.append({
                            "verb": verb,
                            "place": place,
                            "characters": characters,
                            "position": m.start()
                        })

            # 按文本位置排序，确保逻辑顺序正确
            locations_found.sort(key=lambda x: x["position"])

            # 检测: 同一角色在短距离内出现在矛盾地点
            for i, loc1 in enumerate(locations_found):
                for loc2 in locations_found[i+1:]:
                    if abs(loc1["position"] - loc2["position"]) > 2000:
                        continue
                    common_chars = set(loc1["characters"]) & set(loc2["characters"])
                    for char in common_chars:
                        if loc1["place"] != loc2["place"]:
                            # 离开后到达新地点是正常的（前一个为离开动词）
                            if loc1["verb"] in ("离开", "出发", "逃离"):
                                continue
                            issues.append({
                                "type": "location_contradiction",
                                "severity": "medium",
                                "entity": char,
                                "location1": loc1["place"],
                                "location2": loc2["place"],
                                "message": f"{char}在短距离内出现在不同地点: '{loc1['place']}' 和 '{loc2['place']}'"
                            })
        finally:
            engine.close()

        return issues

    def _check_hook_status(self, chapter: int) -> List[Dict]:
        """检查伏笔状态（使用 SQLite）"""
        from hook_tracker import HookTracker
        tracker = HookTracker(str(self.db_path))

        warnings = []
        try:
            open_hooks = tracker.get_open_hooks(chapter)
            for hook in open_hooks:
                expected = hook.get("expected_resolve")
                if expected and chapter > expected + 5:
                    warnings.append({
                        "type": "overdue_hook",
                        "severity": "medium",
                        "hook_id": hook.get("id"),
                        "desc": hook.get("desc"),
                        "expected_chapter": expected,
                        "current_chapter": chapter,
                        "message": f"伏笔'{hook.get('desc', '')}'已过期（预期第{expected}章回收，当前第{chapter}章）"
                    })
        finally:
            tracker.close()
        return warnings

    def _find_characters_in_text(self, text: str) -> List[str]:
        """在文本中查找已知角色名（优先知识图谱，回退角色JSON）"""
        found = []

        # 优先从知识图谱查找
        try:
            from knowledge_graph import KnowledgeGraph
            kg = KnowledgeGraph(str(self.db_path))
            try:
                characters = kg.list_nodes(node_type="character")
                for char in characters:
                    if char["name"] in text:
                        found.append(char.get("id", char["name"]))
            finally:
                kg.close()
        except Exception:
            pass

        # 回退：从角色JSON文件查找
        if not found and self.characters_path.exists():
            for char_file in self.characters_path.glob("*.json"):
                with open(char_file, 'r', encoding='utf-8') as f:
                    char_data = json.load(f)
                name = char_data.get("name", "")
                if name and name in text:
                    found.append(name)

        return found

    def _is_power_regression(self, old_level: str, new_level: str) -> bool:
        power_levels = self.GENRE_POWER_LEVELS.get(self._genre, [])
        if not power_levels:
            return False
        old_idx = -1
        new_idx = -1
        for i, level in enumerate(power_levels):
            if level in old_level:
                old_idx = i
            if level in new_level:
                new_idx = i
        if old_idx >= 0 and new_idx >= 0:
            return new_idx < old_idx
        return False

    def generate_context_checklist(self, chapter: int) -> Dict[str, Any]:
        checklist = {"chapter": chapter, "checks": []}

        try:
            facts = self.fact_engine.get_relevant_facts(chapter, max_facts=50)
            for fact in facts:
                checklist["checks"].append({
                    "type": "fact_consistency",
                    "entity": fact["entity"],
                    "attribute": fact["attribute"],
                    "expected_value": fact["value"],
                    "importance": fact.get("importance", "chapter-scoped"),
                    "check": f"确认 {fact['entity']} 的 {fact['attribute']} 是否为 {fact['value']}"
                })
        except Exception:
            pass

        return checklist

    def analyze_revision_impact(self, chapter: int,
                                old_content: str, new_content: str) -> Dict[str, Any]:
        """
        章节修订影响分析: 对比修订前后内容，识别受影响的后续章节、事实和伏笔

        Args:
            chapter: 修订的章节号
            old_content: 修订前的章节内容
            new_content: 修订后的章节内容

        Returns:
            影响分析报告，含实体变化、受影响章节、受影响事实、受影响伏笔
        """
        from entity_extractor import EntityExtractor
        from memory_engine import MemoryEngine
        from hook_tracker import HookTracker

        extractor = EntityExtractor(str(self.project_path))

        # 1. 对比实体变化
        old_entities = extractor.extract(old_content)
        new_entities = extractor.extract(new_content)

        old_char_names = {e["name"] for e in old_entities.get("characters", [])}
        new_char_names = {e["name"] for e in new_entities.get("characters", [])}
        old_loc_names = {e["name"] for e in old_entities.get("locations", [])}
        new_loc_names = {e["name"] for e in new_entities.get("locations", [])}
        old_item_names = {e["name"] for e in old_entities.get("items", [])}
        new_item_names = {e["name"] for e in new_entities.get("items", [])}

        entity_changes = {
            "added_characters": list(new_char_names - old_char_names),
            "removed_characters": list(old_char_names - new_char_names),
            "added_locations": list(new_loc_names - old_loc_names),
            "removed_locations": list(old_loc_names - new_loc_names),
            "added_items": list(new_item_names - old_item_names),
            "removed_items": list(old_item_names - new_item_names),
        }

        # 收集所有变化的实体名
        changed_entities = (old_char_names | new_char_names |
                           old_loc_names | new_loc_names |
                           old_item_names | new_item_names)

        # 2. 查找受影响的后续章节
        engine = MemoryEngine(str(self.db_path), project_path=str(self.project_path))
        try:
            affected_chapters = []
            for entity_name in changed_entities:
                search_results = engine.search(entity_name, top_k=10,
                                               chapter_range=(chapter + 1, chapter + 500))
                for r in search_results:
                    ch_num = r.get("chapter", 0)
                    if ch_num > chapter:
                        affected_chapters.append({
                            "chapter": ch_num,
                            "entity": entity_name,
                            "match_text": r.get("text", "")[:100],
                            "relevance": r.get("score", 0),
                        })

            seen = set()
            unique_affected = []
            for ac in sorted(affected_chapters, key=lambda x: x["chapter"]):
                key = (ac["chapter"], ac["entity"])
                if key not in seen:
                    seen.add(key)
                    unique_affected.append(ac)
        finally:
            engine.close()

        # 3. 查找受影响的事实
        try:
            all_facts = self.fact_engine.get_all_facts()
            affected_facts = []
            for fact in all_facts:
                if fact.get("entity", "") in changed_entities:
                    affected_facts.append({
                        "entity": fact["entity"],
                        "attribute": fact["attribute"],
                        "value": fact["value"],
                        "importance": fact.get("importance", ""),
                        "chapter": fact.get("chapter", 0),
                    })
        except Exception:
            affected_facts = []

        # 4. 查找受影响的伏笔
        tracker = HookTracker(str(self.db_path))
        try:
            affected_hooks = []
            open_hooks = tracker.get_open_hooks()
            for hook in open_hooks:
                desc = hook.get("desc", "")
                related = hook.get("related_characters", [])
                if any(e in desc for e in changed_entities) or \
                   any(c in changed_entities for c in related):
                    affected_hooks.append({
                        "hook_id": hook["id"],
                        "desc": desc,
                        "status": hook.get("status", "open"),
                        "planted_chapter": hook.get("planted_chapter", 0),
                        "expected_resolve": hook.get("expected_resolve"),
                    })
        finally:
            tracker.close()

        # 5. 汇总风险等级
        risk_level = "low"
        if entity_changes["removed_characters"] or entity_changes["removed_locations"]:
            risk_level = "high"
        elif unique_affected or affected_hooks:
            risk_level = "medium"

        return {
            "chapter": chapter,
            "risk_level": risk_level,
            "entity_changes": entity_changes,
            "affected_chapters": unique_affected[:20],
            "affected_facts": affected_facts[:20],
            "affected_hooks": affected_hooks[:10],
            "recommendation": self._generate_revision_recommendation(
                risk_level, entity_changes, unique_affected, affected_facts, affected_hooks),
        }

    @staticmethod
    def _generate_revision_recommendation(risk_level, entity_changes,
                                          affected_chapters, affected_facts,
                                          affected_hooks) -> str:
        """生成修订建议"""
        parts = []
        if risk_level == "high":
            parts.append("高风险修订: 存在实体删除，建议逐一检查后续章节中的引用")
        elif risk_level == "medium":
            parts.append("中风险修订: 存在受影响的后续内容，建议检查关键引用")
        else:
            parts.append("低风险修订: 未检测到明显的连锁影响")

        if entity_changes.get("removed_characters"):
            parts.append(f"角色删除: {', '.join(entity_changes['removed_characters'])}，需检查后续出场")
        if entity_changes.get("removed_locations"):
            parts.append(f"地点删除: {', '.join(entity_changes['removed_locations'])}，需检查后续场景设定")
        if affected_facts:
            parts.append(f"受影响事实: {len(affected_facts)}条，建议核实是否需要更新")
        if affected_hooks:
            parts.append(f"受影响伏笔: {len(affected_hooks)}条，建议确认伏笔仍可正常回收")

        return "; ".join(parts)


    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "check-chapter":
            content = params.get("content", "")
            content_file = params.get("content_file")
            if content_file:
                with open(content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            chapter = params.get("chapter")
            if chapter is None:
                return {"error": "需要提供章节编号"}
            chapter = int(chapter)
            # 自动从数据库读取章节内容（当未提供content时）
            if not content:
                content = self._read_chapter_content(chapter)
                if not content:
                    return {"error": "需要提供章节正文(content)，或该章节尚未存储"}
            return self.check_chapter(chapter, content)

        elif action == "checklist":
            chapter = params.get("chapter")
            if chapter is None:
                return {"error": "需要提供章节编号"}
            return self.generate_context_checklist(int(chapter))

        elif action == "analyze-revision":
            chapter = params.get("chapter")
            if chapter is None:
                return {"error": "需要提供章节编号"}
            old_text = params.get("old_content", "")
            new_text = params.get("new_content", "")
            old_file = params.get("old_content_file")
            new_file = params.get("new_content_file")
            if old_file:
                with open(old_file, 'r', encoding='utf-8') as f:
                    old_text = f.read()
            if new_file:
                with open(new_file, 'r', encoding='utf-8') as f:
                    new_text = f.read()
            if not old_text or not new_text:
                return {"error": "需要提供修订前和修订后内容"}
            return self.analyze_revision_impact(int(chapter), old_text, new_text)

        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='连续性检查器')
    parser.add_argument('--project-path', required=True, help='项目路径')
    parser.add_argument('--action', required=True,
                       choices=['check-chapter', 'checklist', 'analyze-revision'],
                       help='操作类型')
    parser.add_argument('--chapter', type=int, help='章节编号')
    parser.add_argument('--content', help='章节正文')
    parser.add_argument('--content-file', help='章节正文文件')
    parser.add_argument('--old-content', help='修订前内容')
    parser.add_argument('--old-content-file', help='修订前内容文件')
    parser.add_argument('--new-content', help='修订后内容')
    parser.add_argument('--new-content-file', help='修订后内容文件')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    checker = ContinuityChecker(args.project_path)

    try:
        skip_keys = {"project_path", "action", "output"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        result = checker.execute_action(args.action, params)
    finally:
        checker.close()

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
