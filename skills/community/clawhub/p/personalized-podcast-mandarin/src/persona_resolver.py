# -*- coding: utf-8 -*-
"""
Persona 解析器
负责 Persona 的匹配、创建、更新、保存全生命周期管理
"""
import copy
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from .persona_manager import PersonaManager, check_first_time
from .setup_wizard import SetupWizard, save_double_persona, generate_complementary_host
from .preset_manager import PresetManager
from .persona_extractor import PersonaExtractor
from pydantic import BaseModel
from typing import Literal


class PersonaMatchResult(BaseModel):
    """Persona匹配API返回结构"""
    match_key: str
    confidence: Literal["high", "medium", "low"] = "low"


class PersonaIdentityMatchResult(BaseModel):
    """Persona身份匹配API返回结构"""
    match_name: Optional[str] = None
    confidence: Literal["high", "medium", "low"] = "low"


@dataclass
class ResolveResult:
    persona_config: Dict[str, Any]          # {"host_a": ..., "host_b": ...}
    source: str                             # 来源标识
    matched_persona_name: Optional[str] = None
    is_first_time: bool = False


class PersonaResolver:
    """轻量级 Persona 解析器。无状态，可被外层 Agent 或 CLI 直接调用。"""

    def __init__(self, user_id: str = "default", skip_client_init: bool = False):
        self.user_id = user_id
        self.client = None
        if not skip_client_init:
            from .config_loader import ConfigLoader
            from .volcano_client_requests import create_ark_client_requests
            config = ConfigLoader().load()
            self.client = create_ark_client_requests(api_key=config.get("doubao_api_key"))

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------
    def resolve(
        self,
        explicit_description: Optional[str] = None,
        document_text: Optional[str] = None,
        preset_name: Optional[str] = None,
        verbose: bool = False
    ) -> ResolveResult:
        """
        解析入口。
        优先级: preset > document_text > explicit_description > default/last
        """
        # 1. preset 最高优先级
        if preset_name:
            return self._resolve_preset(preset_name, verbose=verbose)

        # 2. 文档输入
        if document_text:
            return self._resolve_document(document_text, verbose=verbose)

        # 3. 自然语言描述
        if explicit_description:
            return self._resolve_description(explicit_description, verbose=verbose)

        # 4. 回退到 default（上次使用）
        return self._resolve_default(verbose=verbose)

    def resolve_first_time(self, verbose: bool = False) -> ResolveResult:
        """
        首次使用检测入口。
        如果目录为空，返回 is_first_time=True，由调用方负责追问用户。
        """
        if check_first_time(self.user_id):
            return ResolveResult(
                persona_config={},
                source="first_time",
                is_first_time=True
            )
        return self._resolve_default(verbose=verbose)

    def find_matching_persona(self, description: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        对自然语言描述在所有已存 persona 和 preset 中做轻量级匹配。
        返回 (persona_name, persona_dict) 或 None。
        """
        description = description.strip()
        if not description:
            return None

        # ---- Fast path 0: 特定人物名称检测 ----
        # 如果描述中包含显式的人名（如"潘乱风格"、"罗永浩式"），
        # 且不是精确匹配到同名 preset，则直接创建新 persona
        # 避免将特定人物风格错误匹配到相似的 preset
        import re
        # 匹配 "XXX风格"、"像XXX"、"XXX式" 等模式中的人名
        name_patterns = [
            r'(.+?)(?:风格|style)',
            r'像(.+?)(?:那样|一样|风格)',
            r'(.+?)(?:式|style)的?',
        ]
        explicit_names = []
        for pattern in name_patterns:
            matches = re.findall(pattern, description)
            explicit_names.extend([m.strip() for m in matches if len(m.strip()) >= 2])

        # 去重
        explicit_names = list(set(explicit_names))
        if explicit_names:
            # 检查是否有同名的 preset（精确匹配）
            pm = PresetManager()
            has_exact_name_match = False
            for name in explicit_names:
                # 检查 preset 名称
                for preset_name in pm._presets_cache.keys():
                    if name in preset_name:
                        has_exact_name_match = True
                        break
                # 检查 saved persona 的 display_name
                saved = _load_all_saved_personas(self.user_id)
                for saved_name, config in saved.items():
                    display_name = _extract_display_name(config)
                    if display_name and name in display_name:
                        has_exact_name_match = True
                        break

            if not has_exact_name_match:
                # 描述中包含特定人名但没有精确匹配的 preset，创建新 persona
                return None

        # ---- Fast path 1: 精确匹配 preset ----
        pm = PresetManager()
        preset = pm.get_preset(description)
        if preset:
            applied = pm.apply_preset(preset["preset_name"])
            return (preset["preset_name"], applied["persona_config"])

        # ---- Fast path 2: saved persona 名称精确/包含匹配 ----
        desc_norm = description.replace(" ", "").replace("-", "").lower()
        saved = _load_all_saved_personas(self.user_id)

        for name, config in saved.items():
            name_norm = name.replace(" ", "").replace("-", "").lower()
            if desc_norm == name_norm:
                return (name, config)

        # 额外：如果描述中包含某个 persona 的 display_name
        for name, config in saved.items():
            flat = _flatten_persona_for_matching(config)
            display_name = _extract_display_name(config) or name
            if display_name and display_name.lower() in description.lower():
                return (name, config)

        # ---- Fallback: LLM 语义匹配 ----
        if self.client is None or len(saved) + len(pm.list_presets()) == 0:
            return None

        candidates = []
        # 添加 presets 作为候选
        for p in pm.list_presets():
            candidates.append(f"[preset:{p['name']}] {p['name']} - {p['description']}")
        # 添加 saved personas 作为候选
        for name, config in saved.items():
            flat = _flatten_persona_for_matching(config)
            candidates.append(f"[saved:{name}] {flat}")

        if not candidates:
            return None

        prompt = f"""你是一个 persona 匹配助手。
用户想用以下描述找到最合适的主持人风格："{description}"

现有候选如下（每行一个）：
{candidates}

请判断哪个候选最符合用户描述。
只输出 JSON，不要解释：
{{"match_key": "preset:名称" 或 "saved:名称" 或 "NO_MATCH", "confidence": "high" 或 "medium" 或 "low"}}
如果完全没有匹配的，输出 {{"match_key": "NO_MATCH"}}。
"""
        try:
            result, _ = self.client.chat_completion(
                system_prompt="你是一个严格的 JSON 输出助手，只输出 JSON，不附加任何说明。",
                user_message=prompt,
                output_schema=PersonaMatchResult,
                temperature=0.2,
                max_tokens=256
            )
            parsed = result.model_dump()

            key = parsed.get("match_key", "NO_MATCH")
            confidence = parsed.get("confidence", "low")
            # 只接受 high 置信度的匹配，medium/low 都视为不匹配
            # 这样可以避免将相似但不相同的描述错误匹配到现有 preset
            if key == "NO_MATCH" or confidence != "high":
                return None

            prefix, _, name = key.partition(":")
            if prefix == "preset":
                preset = pm.get_preset(name)
                if preset:
                    applied = pm.apply_preset(preset["preset_name"])
                    return (preset["preset_name"], applied["persona_config"])
            elif prefix == "saved":
                if name in saved:
                    return (name, saved[name])
        except Exception:
            return None

        return None

    def is_doc_persona_match(self, extracted_persona: Dict[str, Any]) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        检查提取出的 persona 是否与某个现存 persona 为同一人。
        返回 (persona_name, existing_persona) 或 None。
        """
        saved = _load_all_saved_personas(self.user_id)
        if not saved or self.client is None:
            return None

        candidates = []
        for name, config in saved.items():
            # 对双人配置，把 host_a 和 host_b 分别展开
            if "host_a" in config and "host_b" in config:
                for hk in ["host_a", "host_b"]:
                    flat = _flatten_single_persona(config[hk])
                    candidates.append(f"[{name}:{hk}] {flat}")
            else:
                flat = _flatten_single_persona(config)
                candidates.append(f"[{name}] {flat}")

        extracted_flat = _flatten_single_persona(extracted_persona)

        prompt = f"""你正在判断：从文档中提取的人物是否与数据库中的某个人物为同一人。

提取的人物：
{extracted_flat}

数据库中的候选（格式：[persona_name:host_key] 简介）：
{candidates}

请判断是否为同一人（真实姓名相同，或风格人格极度相似）。
只输出 JSON，不要解释：
{{"match_name": "对应 persona 名称（不含 :host_key）", "confidence": "high" 或 "medium" 或 "low"}}
如果不是同一人，输出 {{"match_name": null}}。
"""
        try:
            result, _ = self.client.chat_completion(
                system_prompt="你是一个严格的 JSON 输出助手，只输出 JSON，不附加任何说明。",
                user_message=prompt,
                output_schema=PersonaIdentityMatchResult,
                temperature=0.2,
                max_tokens=256
            )
            parsed = result.model_dump()

            match_name = parsed.get("match_name")
            confidence = parsed.get("confidence", "low")
            if not match_name or confidence == "low":
                return None

            if match_name in saved:
                return (match_name, saved[match_name])
        except Exception:
            return None

        return None

    # -----------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------
    def _resolve_preset(self, preset_name: str, verbose: bool = False) -> ResolveResult:
        pm = PresetManager()
        applied = pm.apply_preset(preset_name)
        config = applied["persona_config"]
        save_double_persona(self.user_id, config["host_a"], config["host_b"])
        if verbose:
            print(f"  使用预设: {preset_name}")
        return ResolveResult(persona_config=config, source="preset", matched_persona_name=preset_name)

    def _resolve_description(self, description: str, verbose: bool = False) -> ResolveResult:
        match = self.find_matching_persona(description)
        if match:
            name, config = match
            # 若为双人结构则直接设 default；单人则需补搭档（preset 已确保双人）
            double_config = _ensure_double(config)
            save_double_persona(self.user_id, double_config["host_a"], double_config["host_b"])
            if verbose:
                print(f"  匹配到已有 persona: {name}")
            return ResolveResult(persona_config=double_config, source="description_matched", matched_persona_name=name)

        # 未命中，创建新的
        wizard = SetupWizard(self.user_id)
        host_a, host_b = wizard.parse_two_personas(description)
        save_double_persona(self.user_id, host_a, host_b)
        if verbose:
            print(f"  从描述生成新 persona: '{description[:30]}...'")
        return ResolveResult(
            persona_config={"host_a": host_a, "host_b": host_b},
            source="description_new"
        )

    def _resolve_document(self, document_text: str, verbose: bool = False) -> ResolveResult:
        extractor = PersonaExtractor(skip_client_init=True)
        if self.client:
            extractor.client = self.client

        extracted = extractor.extract(document_text, raise_on_error=False)
        if not extracted or not extracted.get("identity", {}).get("name"):
            if verbose:
                print("  ⚠️ 文档提取失败，回退到默认配置")
            return self._resolve_default(verbose=verbose)

        match = self.is_doc_persona_match(extracted)
        if match:
            name, existing = match
            # 合并：新提取覆盖核心字段，但保留原有 voice_id
            merged = _merge_extracted_with_existing(extracted, existing)
            double_config = _ensure_double(merged)
            # 保存回同名文件并同步 default
            pm = PersonaManager(self.user_id, name)
            pm.update(double_config)
            save_double_persona(self.user_id, double_config["host_a"], double_config["host_b"])
            if verbose:
                print(f"  文档人物匹配到 '{name}'，已更新")
            return ResolveResult(
                persona_config=double_config,
                source="extracted_updated",
                matched_persona_name=name
            )

        # 未匹配，新建
        host_a = extracted
        host_b = generate_complementary_host(host_a)
        # 生成安全文件名
        safe_name = re.sub(r"[^\w\u4e00-\u9fa5]", "", extracted.get("identity", {}).get("name", "doc")) or "doc"
        persona_name = f"{safe_name}_extracted"
        pm = PersonaManager(self.user_id, persona_name)
        double_new = {"host_a": host_a, "host_b": host_b}
        pm.save(double_new)
        save_double_persona(self.user_id, host_a, host_b)
        if verbose:
            print(f"  从文档提取新建 persona: {persona_name}")
        return ResolveResult(persona_config=double_new, source="extracted_new")

    def _resolve_default(self, verbose: bool = False) -> ResolveResult:
        default_manager = PersonaManager(self.user_id, "default")
        if default_manager.exists():
            config = default_manager.load()
            if "host_a" in config and "host_b" in config:
                if verbose:
                    print("  使用上次保存的 default persona")
                return ResolveResult(persona_config=config, source="existing_default")

        # 回退组合 host_a + host_b
        host_a_mgr = PersonaManager(self.user_id, "host_a")
        host_b_mgr = PersonaManager(self.user_id, "host_b")
        if host_a_mgr.exists() and host_b_mgr.exists():
            config = {"host_a": host_a_mgr.load(), "host_b": host_b_mgr.load()}
            if verbose:
                print("  使用 host_a + host_b 组合")
            return ResolveResult(persona_config=config, source="existing_default")

        # 系统默认
        from .config_loader import ConfigLoader
        config_dir = Path(__file__).parent.parent / "config"
        with open(config_dir / "default-persona.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        if verbose:
            print("  使用系统默认 persona")
        return ResolveResult(persona_config=config, source="system_default")


# -----------------------------------------------------------------
# Module-level helpers
# -----------------------------------------------------------------

def _load_all_saved_personas(user_id: str) -> Dict[str, Dict[str, Any]]:
    """加载用户所有 saved personas（排除内部文件）"""
    config_dir = Path(__file__).parent.parent / "config" / "user_personas" / user_id
    if not config_dir.exists():
        return {}

    result = {}
    for json_file in sorted(config_dir.glob("*.json")):
        if json_file.name.startswith("_"):
            continue
        try:
            data = json.load(json_file.open("r", encoding="utf-8"))
            persona = data.get("persona", data)  # 兼容直接保存的裸 dict
            result[json_file.stem] = persona
        except Exception:
            continue
    return result


def _extract_display_name(config: Dict[str, Any]) -> Optional[str]:
    """从双人或单人配置中提取 display name"""
    if "host_a" in config:
        return config["host_a"].get("identity", {}).get("name")
    return config.get("identity", {}).get("name")


def _flatten_single_persona(persona: Dict[str, Any]) -> str:
    """把单人 persona 压平为一句话摘要"""
    identity = persona.get("identity", {})
    expression = persona.get("expression", {})
    phrases = expression.get("signature_phrases", [])[:2]
    return (
        f"名称:{identity.get('name','')} "
        f"原型:{identity.get('archetype','')} "
        f"风格:{expression.get('attitude','')} "
        f"口头禅:{','.join(phrases)}"
    )


def _flatten_persona_for_matching(config: Dict[str, Any]) -> str:
    """把任意 persona 配置压平为匹配摘要"""
    if "host_a" in config and "host_b" in config:
        a = _flatten_single_persona(config["host_a"])
        b = _flatten_single_persona(config["host_b"])
        return f"双人组合 | A:{a} | B:{b}"
    return _flatten_single_persona(config)


def _ensure_double(config: Dict[str, Any]) -> Dict[str, Any]:
    """确保返回的是双人 {host_a, host_b} 结构"""
    if "host_a" in config and "host_b" in config:
        return config
    # 单人结构，补一个搭档
    host_a = config
    host_b = generate_complementary_host(host_a)
    return {"host_a": host_a, "host_b": host_b}


def _merge_extracted_with_existing(extracted: Dict[str, Any], existing: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并文档提取出的 persona 与已有 persona。
    策略：优先使用新提取的核心人格字段，但保留原有 voice_id 和 memory_seed。
    """
    # 先确保是双人结构，但 merge 只针对单人 persona 的核心字段
    existing_single = existing
    if "host_a" in existing and "host_b" in existing:
        # 简化：如果 existing 是双人，默认合并到 host_a（通常是主要人物）
        existing_single = existing["host_a"]

    merged = copy.deepcopy(existing_single)

    # 覆盖 identity 核心字段
    for k, v in extracted.get("identity", {}).items():
        if v:
            merged.setdefault("identity", {})[k] = v

    # 覆盖 expression 核心字段，但保留 voice_id
    old_voice = merged.get("expression", {}).get("voice_id", "")
    for k, v in extracted.get("expression", {}).items():
        if v:
            merged.setdefault("expression", {})[k] = v
    if old_voice:
        merged["expression"]["voice_id"] = old_voice

    # 合并 memory_seed（追加新的）
    old_memories = merged.get("memory_seed", [])
    new_memories = extracted.get("memory_seed", [])
    if new_memories:
        seen = {m.get("title") + m.get("content") for m in old_memories if isinstance(m, dict)}
        for mem in new_memories:
            if isinstance(mem, dict):
                key = mem.get("title", "") + mem.get("content", "")
                if key not in seen:
                    old_memories.append(mem)
        merged["memory_seed"] = old_memories

    return merged
