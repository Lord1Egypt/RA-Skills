#!/usr/bin/env python3
"""
设定导入器 - 从Markdown设定文件批量导入/更新/删除设定

支持格式: 见 references/settings_format.md
操作对象: KnowledgeGraph, CharacterSimulator, FactEngine, HookTracker
支持动作: import(导入) / update(更新) / delete(删除) / dry-run(预览)
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class SettingsImporter:
    """设定文件批量导入器"""

    # 识别各板块的关键词
    SECTION_KEYWORDS = {
        "character": ["角色", "人物", "characters"],
        "entity": ["势力", "组织", "地点", "物品", "势力/地点/物品", "实体", "entities",
                    "factions", "locations", "items", "世界设定"],
        "relation": ["关系", "关联", "relations", "relationships", "人物关系"],
        "fact": ["事实", "设定事实", "facts"],
        "hook": ["伏笔", "悬念", "hooks", "foreshadowing"],
        "constraint": ["约束规则", "约束", "constraints", "规则", "创作约束"],
    }

    # 实体名中的类型后缀模式（如 "碧落宫 (faction)"）
    TYPE_SUFFIX_RE = re.compile(r'\s*\(([^)]+)\)\s*$')

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self._kg = None
        self._cs = None
        self._fe = None
        self._ht = None

    def _get_engines(self):
        """懒加载引擎实例"""
        if self._kg is None:
            from knowledge_graph import KnowledgeGraph
            from character_simulator import CharacterSimulator
            from fact_engine import FactEngine
            from hook_tracker import HookTracker

            db_path = str(self.project_path / "data" / "novel_memory.db")
            chars_dir = str(self.project_path / "data" / "characters")
            self._kg = KnowledgeGraph(db_path)
            self._cs = CharacterSimulator(chars_dir)
            self._fe = FactEngine(db_path, project_path=str(self.project_path))
            self._ht = HookTracker(db_path)
        return self._kg, self._cs, self._fe, self._ht

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "import":
            return self.import_settings(params)
        elif action == "update":
            return self.update_settings(params)
        elif action == "delete":
            return self.delete_settings(params)
        elif action == "dry-run":
            return self.dry_run(params)
        else:
            raise ValueError(f"未知操作: {action}")

    def import_settings(self, params: dict) -> dict:
        """
        导入设定文件

        Args:
            params: {
                "path": 设定文件路径,
                "chapter": 默认章节号(可选,默认0表示创世设定),
                "dry_run": 仅解析不执行(可选)
            }
        """
        file_path = params.get("path") or params.get("file") or params.get("settings_path")
        if not file_path:
            return {"error": "需要提供设定文件路径(path参数)"}

        path = Path(file_path)
        if not path.exists():
            return {"error": f"设定文件不存在: {file_path}"}

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"读取文件失败: {e}"}

        default_chapter = int(params.get("chapter", 0))
        dry_run = params.get("dry_run", False)

        return self._parse_and_import(content, default_chapter, dry_run)

    def dry_run(self, params: dict) -> dict:
        """仅解析不执行，预览导入内容"""
        params["dry_run"] = True
        return self.import_settings(params)

    def _parse_and_import(self, content: str, default_chapter: int = 0,
                          dry_run: bool = False) -> dict:
        """解析Markdown设定内容并导入"""
        sections = self._parse_sections(content)

        result = {
            "dry_run": dry_run,
            "parsed": {
                "characters": len(sections.get("character", [])),
                "entities": len(sections.get("entity", [])),
                "relations": len(sections.get("relation", [])),
                "facts": len(sections.get("fact", [])),
                "hooks": len(sections.get("hook", [])),
                "constraints": len(sections.get("constraint", [])),
            },
            "imported": {
                "characters": 0, "nodes": 0, "edges": 0,
                "facts": 0, "hooks": 0, "constraints": 0, "errors": []
            }
        }

        if dry_run:
            result["preview"] = sections
            return result

        kg, cs, fe, ht = self._get_engines()

        # 1. 导入实体节点（势力/地点/物品/概念）
        for entity in sections.get("entity", []):
            try:
                clean_name = self._strip_type_suffix(entity["name"])
                kg.add_node(
                    name=clean_name,
                    node_type=entity.get("type", "concept"),
                    properties=entity.get("properties", {})
                )
                result["imported"]["nodes"] += 1
            except Exception as e:
                result["imported"]["errors"].append(f"节点导入失败[{entity['name']}]: {e}")

        # 2. 导入角色（同时创建知识图谱节点）
        for char in sections.get("character", []):
            try:
                cs.create_character(
                    name=char["name"],
                    role=char.get("role", "npc"),
                    big_five=char.get("big_five"),
                    core_traits=char.get("core_traits"),
                    speech_style=char.get("speech_style", ""),
                    forbidden_actions=char.get("forbidden_actions"),
                    typical_behaviors=char.get("typical_behaviors"),
                    background=char.get("background", ""),
                    goals=char.get("goals"),
                    fears=char.get("fears"),
                    relationships=char.get("relationships"),
                )
                # 同步创建知识图谱节点
                kg.add_node(name=char["name"], node_type="character")
                result["imported"]["characters"] += 1
            except Exception as e:
                result["imported"]["errors"].append(f"角色导入失败[{char['name']}]: {e}")

        # 3. 导入关系
        for rel in sections.get("relation", []):
            try:
                source = rel["source"]
                target = rel["target"]
                # 确保端点节点存在，并获取节点ID
                source_node = kg.find_node_by_name(source)
                if not source_node:
                    kg.add_node(name=source, node_type="character")
                    source_node = kg.find_node_by_name(source)
                target_node = kg.find_node_by_name(target)
                if not target_node:
                    kg.add_node(name=target, node_type="character")
                    target_node = kg.find_node_by_name(target)
                # 使用节点ID建立边
                kg.add_edge(source=source_node["id"], target=target_node["id"],
                            relation=rel.get("relation", "关联"))
                result["imported"]["edges"] += 1
            except Exception as e:
                result["imported"]["errors"].append(
                    f"关系导入失败[{rel.get('source','')}→{rel.get('target','')}]: {e}")

        # 4. 导入事实
        for fact in sections.get("fact", []):
            try:
                fe.set_fact(
                    category=fact.get("category", "world"),
                    entity=fact["entity"],
                    attribute=fact["attribute"],
                    value=fact["value"],
                    chapter=fact.get("chapter", default_chapter),
                    importance=fact.get("importance", "permanent"),
                    valid_from=fact.get("valid_from"),
                    valid_until=fact.get("valid_until"),
                )
                result["imported"]["facts"] += 1
            except Exception as e:
                result["imported"]["errors"].append(
                    f"事实导入失败[{fact.get('entity','')}.{fact.get('attribute','')}]: {e}")

        # 5. 导入伏笔
        for hook in sections.get("hook", []):
            try:
                ht.plant(
                    desc=hook["description"],
                    planted_chapter=hook.get("chapter", default_chapter),
                    expected_resolve=hook.get("expected_resolve"),
                    priority=hook.get("priority"),
                )
                result["imported"]["hooks"] += 1
            except Exception as e:
                result["imported"]["errors"].append(
                    f"伏笔导入失败[{hook.get('description','')[:20]}]: {e}")

        # 6. 导入约束规则到 project_config.json
        constraints = sections.get("constraint", [])
        if constraints:
            try:
                config = self._read_config()
                if "constraints" not in config:
                    config["constraints"] = {}
                for c in constraints:
                    name = c.get("name", "")
                    if name:
                        config["constraints"][name] = c
                self._write_config(config)
                result["imported"]["constraints"] = len(constraints)
            except Exception as e:
                result["imported"]["errors"].append(f"约束规则导入失败: {e}")

        return result

    def _parse_sections(self, content: str) -> Dict[str, List[dict]]:
        """解析Markdown内容为结构化板块"""
        sections = {}
        current_section = None
        current_item = None
        current_props = {}

        lines = content.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()

            # ## 二级标题 = 板块
            h2_match = re.match(r'^##\s+(.+)', line)
            if h2_match:
                # 保存上一个item
                if current_section:
                    self._flush_current(sections, current_section,
                                        current_item, current_props)
                current_section = self._classify_section(h2_match.group(1).strip())
                current_item = None
                current_props = {}
                i += 1
                continue

            # ### 三级标题 = 子项名称
            h3_match = re.match(r'^###\s+(.+)', line)
            if h3_match and current_section:
                # 保存上一个item
                self._flush_current(sections, current_section,
                                    current_item, current_props)
                current_item = self._strip_type_suffix(h3_match.group(1).strip())
                current_props = {}
                i += 1
                continue

            # - 属性行
            bullet_match = re.match(r'^[-*]\s+(.+)', line)
            if bullet_match and current_section:
                prop_text = bullet_match.group(1).strip()
                # 关系/事实/伏笔板块：列表项直接解析并入sections
                if current_section in ("relation", "fact", "hook"):
                    self._parse_list_item(sections, current_section,
                                          prop_text)
                else:
                    self._parse_property(prop_text, current_section, current_props)
                i += 1
                continue

            # 空行或非匹配行
            i += 1

        # 保存最后一个item
        if current_section:
            self._flush_current(sections, current_section,
                                current_item, current_props)

        return sections

    def _flush_current(self, sections: dict, section_type: str,
                       item_name: Optional[str], props: dict):
        """将当前累积的item刷入sections"""
        if not section_type:
            return
        # 关系/事实/伏笔板块已在_parse_list_item中直接添加
        if section_type in ("relation", "fact", "hook"):
            return
        if item_name:
            self._add_parsed_item(sections, section_type, item_name, props)

    def _parse_list_item(self, sections: dict, section_type: str, text: str):
        """直接解析列表项并入sections（用于关系/事实/伏笔板块）"""
        if section_type not in sections:
            sections[section_type] = []

        # 关系格式（按优先级匹配）:
        # 1. A → B: 关系描述
        # 2. A -> B: 关系描述
        # 3. A --关系描述--> B
        # 4. A --关系描述-- B
        if section_type == "relation":
            # 格式3/4: A --关系描述--> B  或  A --关系描述-- B
            arrow_desc_match = re.match(
                r'(.+?)\s*--(.+?)-->\s*(.+?)\s*(?:[:：].*)?$', text)
            if arrow_desc_match:
                sections[section_type].append({
                    "source": arrow_desc_match.group(1).strip(),
                    "target": arrow_desc_match.group(3).strip(),
                    "relation": arrow_desc_match.group(2).strip(),
                })
                return
            # 格式3b: A --关系描述-- B (无箭头)
            dash_desc_match = re.match(
                r'(.+?)\s*--(.+?)--\s*(.+?)\s*(?:[:：].*)?$', text)
            if dash_desc_match:
                sections[section_type].append({
                    "source": dash_desc_match.group(1).strip(),
                    "target": dash_desc_match.group(3).strip(),
                    "relation": dash_desc_match.group(2).strip(),
                })
                return
            # 格式1/2: A →/> B: 关系描述
            relation_match = re.match(
                r'(.+?)\s*(?:→|->|--?>)\s*(.+?)\s*[:：]\s*(.+)', text)
            if relation_match:
                sections[section_type].append({
                    "source": relation_match.group(1).strip(),
                    "target": relation_match.group(2).strip(),
                    "relation": relation_match.group(3).strip(),
                })
                return

        # 事实格式: 实体.属性=值 (chapter:N, importance:X, valid_from:N, valid_until:N)
        fact_match = re.match(
            r'(.+?)\.(.+?)\s*=\s*(.+?)(?:\s*\((.+)\))?\s*$', text)
        if section_type == "fact" and fact_match:
            entity = fact_match.group(1).strip()
            attribute = fact_match.group(2).strip()
            value_part = fact_match.group(3).strip()
            params_str = fact_match.group(4) or ""
            fact = {"entity": entity, "attribute": attribute, "value": value_part}
            for param_match in re.finditer(
                    r'(\w+)\s*[:：]\s*([^\s,]+)', params_str):
                pk = param_match.group(1)
                pv = param_match.group(2)
                if pk in ("chapter", "valid_from", "valid_until"):
                    fact[pk] = int(pv)
                else:
                    fact[pk] = pv
            if "category" not in fact:
                fact["category"] = self._infer_category(entity, attribute)
            sections[section_type].append(fact)
            return

        # 伏笔格式: 描述 (chapter:N, priority:X, expected_resolve:N)
        if section_type == "hook":
            hook_match = re.match(r'(.+?)(?:\s*\((.+)\))?\s*$', text)
            if hook_match:
                desc = hook_match.group(1).strip()
                params_str = hook_match.group(2) or ""
                hook = {"description": desc}
                for param_match in re.finditer(
                        r'(\w+)\s*[:：]\s*([^\s,]+)', params_str):
                    pk = param_match.group(1)
                    pv = param_match.group(2)
                    if pk in ("chapter", "expected_resolve"):
                        try:
                            hook[pk] = int(pv)
                        except ValueError:
                            hook[pk] = pv
                    else:
                        hook[pk] = pv
                sections[section_type].append(hook)
            return

    def _classify_section(self, title: str) -> Optional[str]:
        """将二级标题分类为板块类型"""
        title_lower = title.lower()
        for section_type, keywords in self.SECTION_KEYWORDS.items():
            for kw in keywords:
                if kw in title_lower or kw in title:
                    return section_type
        return None

    def _add_parsed_item(self, sections: dict, section_type: str,
                         item_name: str, props: dict):
        """添加解析结果到板块"""
        if section_type not in sections:
            sections[section_type] = []

        if section_type == "character":
            item = {"name": item_name}
            # 映射属性名
            key_map = {
                "角色": "role", "定位": "role", "role": "role",
                "性格": "personality", "personality": "personality",
                "说话风格": "speech_style", "speech_style": "speech_style",
                "核心特质": "core_traits", "核心特征": "core_traits",
                "core_traits": "core_traits",
                "禁止行为": "forbidden_actions", "forbidden_actions": "forbidden_actions",
                "典型行为": "typical_behaviors", "typical_behaviors": "typical_behaviors",
                "背景": "background", "背景故事": "background",
                "background": "background",
                "目标": "goals", "goals": "goals",
                "恐惧": "fears", "fears": "fears",
                "关系": "relationships", "relationships": "relationships",
                "big_five": "big_five", "人格": "big_five",
            }
            for prop_key, prop_val in props.items():
                mapped_key = key_map.get(prop_key, prop_key)
                # 逗号分隔字符串转列表
                if mapped_key in ("core_traits", "forbidden_actions",
                                  "typical_behaviors", "goals", "fears"):
                    if isinstance(prop_val, str):
                        prop_val = [v.strip() for v in prop_val.split(",") if v.strip()]
                item[mapped_key] = prop_val
            sections[section_type].append(item)

        elif section_type == "entity":
            item = {"name": self._strip_type_suffix(item_name)}
            # 从名称中提取类型后缀（如 "碧落宫 (faction)"）
            type_match = self.TYPE_SUFFIX_RE.search(item_name)
            if type_match and "类型" not in props and "type" not in props:
                item["type"] = type_match.group(1).strip()
            else:
                item["type"] = props.get("类型", props.get("type", "concept"))
            item["properties"] = {k: v for k, v in props.items()
                                  if k not in ("类型", "type")}
            sections[section_type].append(item)

        elif section_type == "relation":
            # 关系行已经在 _parse_property 中处理
            if "_relations" in props:
                for rel in props["_relations"]:
                    sections[section_type].append(rel)

        elif section_type == "fact":
            if "_facts" in props:
                for fact in props["_facts"]:
                    sections[section_type].append(fact)
            else:
                # 单个事实作为属性
                item = {"entity": item_name}
                item.update(props)
                sections[section_type].append(item)

        elif section_type == "hook":
            if "_hooks" in props:
                for hook in props["_hooks"]:
                    sections[section_type].append(hook)

        elif section_type == "constraint":
            # 约束规则：### 名称 + - 键: 值 → {"name": "名称", "键": "值", ...}
            item = {"name": item_name}
            item.update(props)
            sections[section_type].append(item)

    def _parse_property(self, text: str, section_type: str, props: dict):
        """解析属性行"""
        # 关系格式（按优先级匹配）
        if section_type == "relation":
            # A --关系描述--> B
            arrow_desc_match = re.match(
                r'(.+?)\s*--(.+?)-->\s*(.+?)\s*(?:[:：].*)?$', text)
            if arrow_desc_match:
                rel = {
                    "source": arrow_desc_match.group(1).strip(),
                    "target": arrow_desc_match.group(3).strip(),
                    "relation": arrow_desc_match.group(2).strip(),
                }
                if "_relations" not in props:
                    props["_relations"] = []
                props["_relations"].append(rel)
                return
            # A --关系描述-- B
            dash_desc_match = re.match(
                r'(.+?)\s*--(.+?)--\s*(.+?)\s*(?:[:：].*)?$', text)
            if dash_desc_match:
                rel = {
                    "source": dash_desc_match.group(1).strip(),
                    "target": dash_desc_match.group(3).strip(),
                    "relation": dash_desc_match.group(2).strip(),
                }
                if "_relations" not in props:
                    props["_relations"] = []
                props["_relations"].append(rel)
                return
            # A →/> B: 关系描述
            relation_match = re.match(
                r'(.+?)\s*(?:→|->|--?>)\s*(.+?)\s*[:：]\s*(.+)', text)
            if relation_match:
                rel = {
                    "source": relation_match.group(1).strip(),
                    "target": relation_match.group(2).strip(),
                    "relation": relation_match.group(3).strip(),
                }
                if "_relations" not in props:
                    props["_relations"] = []
                props["_relations"].append(rel)
                return

        # 事实格式: 实体.属性=值 (chapter:N, importance:X, valid_from:N, valid_until:N)
        fact_match = re.match(
            r'(.+?)\.(.+?)\s*=\s*(.+?)(?:\s*\((.+)\))?\s*$', text)
        if section_type == "fact" and fact_match:
            entity = fact_match.group(1).strip()
            attribute = fact_match.group(2).strip()
            value_part = fact_match.group(3).strip()
            params_str = fact_match.group(4) or ""

            fact = {"entity": entity, "attribute": attribute, "value": value_part}
            # 解析括号内参数
            for param_match in re.finditer(
                    r'(\w+)\s*[:：]\s*([^\s,]+)', params_str):
                pk = param_match.group(1)
                pv = param_match.group(2)
                if pk in ("chapter", "valid_from", "valid_until"):
                    fact[pk] = int(pv)
                else:
                    fact[pk] = pv
            # 默认category
            if "category" not in fact:
                fact["category"] = self._infer_category(entity, attribute)

            if "_facts" not in props:
                props["_facts"] = []
            props["_facts"].append(fact)
            return

        # 伏笔格式: 描述 (chapter:N, priority:X, expected_resolve:N)
        if section_type == "hook":
            hook_match = re.match(
                r'(.+?)(?:\s*\((.+)\))?\s*$', text)
            if hook_match:
                desc = hook_match.group(1).strip()
                params_str = hook_match.group(2) or ""
                hook = {"description": desc}
                for param_match in re.finditer(
                        r'(\w+)\s*[:：]\s*([^\s,]+)', params_str):
                    pk = param_match.group(1)
                    pv = param_match.group(2)
                    if pk == "chapter":
                        hook[pk] = int(pv)
                    else:
                        hook[pk] = pv
                if "_hooks" not in props:
                    props["_hooks"] = []
                props["_hooks"].append(hook)
            return

        # 通用键值对: key: value 或 key=value
        kv_match = re.match(r'(.+?)\s*[:：=]\s*(.+)', text)
        if kv_match:
            key = kv_match.group(1).strip()
            value = kv_match.group(2).strip()
            props[key] = value
            return

        # 纯文本作为description
        props["description"] = text

    @staticmethod
    def _infer_category(entity: str, attribute: str) -> str:
        """根据实体名和属性名推断事实类别"""
        attr_lower = attribute.lower()
        if any(k in attr_lower for k in ["境界", "修为", "实力", "能力", "level", "power"]):
            return "character"
        if any(k in attr_lower for k in ["位置", "地点", "所在", "location"]):
            return "character"
        if any(k in attr_lower for k in ["门派", "势力", "阵营", "faction"]):
            return "character"
        if any(k in attr_lower for k in ["状态", "进行", "发生", "status"]):
            return "event"
        return "world"

    def update_settings(self, params: dict) -> dict:
        """
        更新设定文件中的已有条目

        Args:
            params: {
                "path": 设定文件路径,
                "chapter": 默认章节号(可选,默认0表示创世设定),
                "dry_run": 仅解析不执行(可选)
            }
        """
        file_path = params.get("path") or params.get("file") or params.get("settings_path")
        if not file_path:
            return {"error": "需要提供设定文件路径(path参数)"}

        path = Path(file_path)
        if not path.exists():
            return {"error": f"设定文件不存在: {file_path}"}

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"读取文件失败: {e}"}

        default_chapter = int(params.get("chapter", 0))
        dry_run = params.get("dry_run", False)
        return self._parse_and_update(content, default_chapter, dry_run)

    def _parse_and_update(self, content: str, default_chapter: int = 0,
                          dry_run: bool = False) -> dict:
        """解析Markdown设定内容并更新已有条目"""
        sections = self._parse_sections(content)

        result = {
            "dry_run": dry_run,
            "parsed": {
                "characters": len(sections.get("character", [])),
                "entities": len(sections.get("entity", [])),
                "relations": len(sections.get("relation", [])),
                "facts": len(sections.get("fact", [])),
                "hooks": len(sections.get("hook", [])),
                "constraints": len(sections.get("constraint", [])),
            },
            "updated": {
                "characters": 0, "nodes": 0, "edges": 0,
                "facts": 0, "hooks": 0, "constraints": 0, "errors": []
            }
        }

        if dry_run:
            result["preview"] = sections
            return result

        kg, cs, fe, ht = self._get_engines()

        # 1. 更新实体节点
        for entity in sections.get("entity", []):
            try:
                clean_name = self._strip_type_suffix(entity["name"])
                node = kg.find_node_by_name(clean_name)
                if node:
                    kg.update_node(
                        node_id=node["id"],
                        node_type=entity.get("type"),
                        properties=entity.get("properties"),
                    )
                    result["updated"]["nodes"] += 1
                else:
                    result["updated"]["errors"].append(
                        f"节点更新失败[{clean_name}]: 不存在")
            except Exception as e:
                result["updated"]["errors"].append(f"节点更新失败[{entity['name']}]: {e}")

        # 2. 更新角色
        for char in sections.get("character", []):
            try:
                char_data = cs.load_character(char["name"])
                if not char_data:
                    result["updated"]["errors"].append(
                        f"角色更新失败[{char['name']}]: 不存在")
                    continue
                # 构建更新参数
                # 注意：personality和speech是嵌套dict，不能直接传字符串
                # 只更新可直接赋值的字段
                update_kwargs = {}
                simple_keys = {
                    "role": "role",
                    "core_traits": "core_traits",
                    "forbidden_actions": "forbidden_actions",
                    "typical_behaviors": "typical_behaviors",
                    "background": "background",
                    "goals": "goals",
                    "fears": "fears",
                }
                for src_key, dst_key in simple_keys.items():
                    if src_key in char and char[src_key]:
                        update_kwargs[dst_key] = char[src_key]
                # speech_style需要映射为speech dict
                if char.get("speech_style"):
                    update_kwargs["speech"] = {"style": char["speech_style"]}
                if update_kwargs:
                    cs.update_character(char["name"], **update_kwargs)
                    result["updated"]["characters"] += 1
                else:
                    result["updated"]["errors"].append(
                        f"角色更新跳过[{char['name']}]: 无可更新属性")
            except Exception as e:
                result["updated"]["errors"].append(f"角色更新失败[{char['name']}]: {e}")

        # 3. 更新关系（先删后建）
        for rel in sections.get("relation", []):
            try:
                source = rel["source"]
                target = rel["target"]
                relation = rel.get("relation", "关联")
                old_edges = kg.find_edge_by_names(source, target, relation)
                # 删除旧边
                for edge in old_edges:
                    kg.delete_edge(edge["id"])
                # 重新创建
                source_node = kg.find_node_by_name(source)
                target_node = kg.find_node_by_name(target)
                if source_node and target_node:
                    kg.add_edge(source=source_node["id"],
                                target=target_node["id"], relation=relation)
                    result["updated"]["edges"] += 1
                else:
                    result["updated"]["errors"].append(
                        f"关系更新失败[{source}→{target}]: 端点节点不存在")
            except Exception as e:
                result["updated"]["errors"].append(
                    f"关系更新失败[{rel.get('source','')}→{rel.get('target','')}]: {e}")

        # 4. 更新事实（set_fact是upsert语义，直接调用即可）
        for fact in sections.get("fact", []):
            try:
                fe.set_fact(
                    category=fact.get("category", "world"),
                    entity=fact["entity"],
                    attribute=fact["attribute"],
                    value=fact["value"],
                    chapter=fact.get("chapter", default_chapter),
                    importance=fact.get("importance", "permanent"),
                    valid_from=fact.get("valid_from"),
                    valid_until=fact.get("valid_until"),
                )
                result["updated"]["facts"] += 1
            except Exception as e:
                result["updated"]["errors"].append(
                    f"事实更新失败[{fact.get('entity','')}.{fact.get('attribute','')}]: {e}")

        # 5. 更新伏笔（仅更新priority等属性，不改变状态）
        for hook in sections.get("hook", []):
            try:
                desc = hook["description"]
                found = ht.find_by_description(desc, status="open")
                if found:
                    # 更新priority/expected_resolve
                    if hook.get("priority") or hook.get("expected_resolve"):
                        cur = ht.conn.cursor()
                        updates = []
                        vals = []
                        if hook.get("priority"):
                            updates.append("priority = ?")
                            vals.append(hook["priority"])
                        if hook.get("expected_resolve"):
                            updates.append("expected_resolve = ?")
                            vals.append(int(hook["expected_resolve"]))
                        if updates:
                            vals.append(found[0]["id"])
                            cur.execute(
                                f"UPDATE hooks SET {', '.join(updates)} WHERE id = ?",
                                vals)
                            ht.conn.commit()
                            result["updated"]["hooks"] += 1
                    else:
                        result["updated"]["errors"].append(
                            f"伏笔更新跳过[{desc[:20]}]: 无可更新属性")
                else:
                    result["updated"]["errors"].append(
                        f"伏笔更新失败[{desc[:20]}]: 未找到匹配的open伏笔")
            except Exception as e:
                result["updated"]["errors"].append(
                    f"伏笔更新失败[{hook.get('description','')[:20]}]: {e}")

        # 6. 更新约束规则（合并同名约束的字段）
        constraints = sections.get("constraint", [])
        if constraints:
            try:
                config = self._read_config()
                if "constraints" not in config:
                    config["constraints"] = {}
                for c in constraints:
                    name = c.get("name", "")
                    if name:
                        # 合并：已有约束保留未提及的字段，新字段覆盖
                        existing = config["constraints"].get(name, {})
                        existing.update(c)
                        existing["name"] = name  # 确保name不丢
                        config["constraints"][name] = existing
                self._write_config(config)
                result["updated"]["constraints"] = len(constraints)
            except Exception as e:
                result["updated"]["errors"].append(f"约束规则更新失败: {e}")

        return result

    def delete_settings(self, params: dict) -> dict:
        """
        删除设定文件中指定的条目

        Args:
            params: {
                "path": 设定文件路径,
                "dry_run": 仅解析不执行(可选)
            }
        """
        file_path = params.get("path") or params.get("file") or params.get("settings_path")
        if not file_path:
            return {"error": "需要提供设定文件路径(path参数)"}

        path = Path(file_path)
        if not path.exists():
            return {"error": f"设定文件不存在: {file_path}"}

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"读取文件失败: {e}"}

        dry_run = params.get("dry_run", False)
        return self._parse_and_delete(content, dry_run)

    def _parse_and_delete(self, content: str, dry_run: bool = False) -> dict:
        """解析Markdown设定内容并删除匹配条目"""
        sections = self._parse_sections(content)

        result = {
            "dry_run": dry_run,
            "parsed": {
                "characters": len(sections.get("character", [])),
                "entities": len(sections.get("entity", [])),
                "relations": len(sections.get("relation", [])),
                "facts": len(sections.get("fact", [])),
                "hooks": len(sections.get("hook", [])),
                "constraints": len(sections.get("constraint", [])),
            },
            "deleted": {
                "characters": 0, "nodes": 0, "edges": 0,
                "facts": 0, "hooks": 0, "constraints": 0, "errors": []
            }
        }

        if dry_run:
            result["preview"] = sections
            return result

        kg, cs, fe, ht = self._get_engines()

        # 1. 删除角色（同时删除知识图谱节点）
        for char in sections.get("character", []):
            try:
                name = char["name"]
                # 先删知识图谱节点（级联删边）
                node = kg.find_node_by_name(name)
                if node:
                    kg.delete_node(node["id"])
                # 再删角色文件
                cs.delete_character(name)
                result["deleted"]["characters"] += 1
            except Exception as e:
                result["deleted"]["errors"].append(f"角色删除失败[{char['name']}]: {e}")

        # 2. 删除实体节点（级联删边）
        for entity in sections.get("entity", []):
            try:
                clean_name = self._strip_type_suffix(entity["name"])
                node = kg.find_node_by_name(clean_name)
                if node:
                    kg.delete_node(node["id"])
                    result["deleted"]["nodes"] += 1
                else:
                    result["deleted"]["errors"].append(
                        f"节点删除失败[{clean_name}]: 不存在")
            except Exception as e:
                result["deleted"]["errors"].append(f"节点删除失败[{entity['name']}]: {e}")

        # 3. 删除关系
        for rel in sections.get("relation", []):
            try:
                source = rel["source"]
                target = rel["target"]
                relation = rel.get("relation")
                edges = kg.find_edge_by_names(source, target, relation)
                for edge in edges:
                    kg.delete_edge(edge["id"])
                    result["deleted"]["edges"] += 1
                if not edges:
                    result["deleted"]["errors"].append(
                        f"关系删除失败[{source}→{target}]: 未找到匹配边")
            except Exception as e:
                result["deleted"]["errors"].append(
                    f"关系删除失败[{rel.get('source','')}→{rel.get('target','')}]: {e}")

        # 4. 删除事实（真删除，实体名去除类型后缀再匹配）
        for fact in sections.get("fact", []):
            try:
                entity = self._strip_type_suffix(fact["entity"])
                attribute = fact.get("attribute")
                if attribute:
                    count = fe.delete_fact(entity, attribute)
                else:
                    count = fe.delete_entity_facts(entity)
                if count > 0:
                    result["deleted"]["facts"] += count
                else:
                    result["deleted"]["errors"].append(
                        f"事实删除失败[{entity}.{attribute or '*'}]: 未找到匹配记录")
            except Exception as e:
                result["deleted"]["errors"].append(
                    f"事实删除失败[{fact.get('entity','')}]: {e}")

        # 5. 删除/放弃伏笔
        for hook in sections.get("hook", []):
            try:
                desc = hook["description"]
                found = ht.find_by_description(desc, status="open")
                if found:
                    ht.abandon(found[0]["id"], reason="设定删除")
                    result["deleted"]["hooks"] += 1
                else:
                    result["deleted"]["errors"].append(
                        f"伏笔删除失败[{desc[:20]}]: 未找到匹配的open伏笔")
            except Exception as e:
                result["deleted"]["errors"].append(
                    f"伏笔删除失败[{hook.get('description','')[:20]}]: {e}")

        # 6. 删除约束规则（按name匹配）
        constraints = sections.get("constraint", [])
        if constraints:
            try:
                config = self._read_config()
                existing = config.get("constraints", {})
                for c in constraints:
                    name = c.get("name", "")
                    if name and name in existing:
                        del existing[name]
                        result["deleted"]["constraints"] += 1
                    elif name:
                        result["deleted"]["errors"].append(
                            f"约束规则删除失败[{name}]: 未找到匹配记录")
                if result["deleted"]["constraints"] > 0:
                    config["constraints"] = existing
                    self._write_config(config)
            except Exception as e:
                result["deleted"]["errors"].append(f"约束规则删除失败: {e}")

        return result

    @classmethod
    def _strip_type_suffix(cls, name: str) -> str:
        """去除实体名中的类型后缀，如 '碧落宫 (faction)' → '碧落宫'"""
        return cls.TYPE_SUFFIX_RE.sub('', name).strip()

    def _read_config(self) -> dict:
        """读取 project_config.json"""
        config_path = self.project_path / "data" / "project_config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _write_config(self, config: dict):
        """写入 project_config.json"""
        config_path = self.project_path / "data" / "project_config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def close(self):
        """关闭引擎连接"""
        for engine in (self._kg, self._fe, self._ht):
            if engine and hasattr(engine, 'close'):
                try:
                    engine.close()
                except Exception:
                    pass


def main():
    """CLI入口"""
    import argparse
    parser = argparse.ArgumentParser(description='设定导入器')
    parser.add_argument('--project-path', required=True, help='项目路径')
    parser.add_argument('--action', required=True,
                        choices=['import', 'update', 'delete', 'dry-run'],
                        help='操作类型: import=导入 update=更新 delete=删除 dry-run=预览')
    parser.add_argument('--path', required=True, help='设定文件路径')
    parser.add_argument('--chapter', type=int, default=0, help='默认章节号')
    args = parser.parse_args()

    importer = SettingsImporter(args.project_path)
    try:
        params = {"path": args.path, "chapter": args.chapter}
        if args.action == "dry-run":
            params["dry_run"] = True
        result = importer.execute_action(args.action, params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        importer.close()


if __name__ == "__main__":
    main()
