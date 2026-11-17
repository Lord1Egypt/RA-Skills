"""Narrative Engine distillation and build pipeline.

Enforces script-driven I/O contracts: the script prepares the staging spec,
locates source files, and builds/validates the final engine artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Optional, Dict, Any, List, Union

from .engine import load_engine, EngineValidationError
from .io import safe_id, write_json_atomic, read_json
from .manifest import write_manifest


_DEFAULT_MODELS = [
    {
        "id": "M1",
        "kind": "model",
        "name": "character-driven causality",
        "when": {"phase": ["outline", "scene", "review"]},
        "requires": ["character"],
        "hardness": "required",
        "prompt": "让关键剧情转折来自人物真实的选择与代价，拒绝机械降神或外部作者意志强推。",
    },
    {
        "id": "M2",
        "kind": "model",
        "name": "concrete emotion",
        "when": {"phase": ["scene", "draft", "review"], "scene_types": ["relationship", "choice", "loss"]},
        "requires": ["emotional_change"],
        "hardness": "required",
        "prompt": "以具体的动作、物件、身体反应或环境承载情感变化，避免虚浮空泛的抒情。",
    },
    {
        "id": "M3",
        "kind": "model",
        "name": "core narrative tension",
        "when": {"phase": ["master-outline", "outline", "review"], "requires": ["long_form"]},
        "hardness": "recommended",
        "prompt": "为故事建立深层且持续的世界/人物内在冲突，使表层事件有扎实的推演动力。",
    },
]

_DEFAULT_TECHNIQUES = [
    {
        "id": "T1",
        "kind": "technique",
        "name": "organic foreshadowing",
        "when": {"phase": ["outline", "draft", "settlement"], "requires": ["hook"]},
        "hardness": "recommended",
        "prompt": "将伏笔以自然、可查证的日常细节植入场景，并在结算中标记兑现或演变路径。",
    },
    {
        "id": "T2",
        "kind": "technique",
        "name": "pacing modulation",
        "when": {"phase": ["scene", "draft", "review"], "scene_types": ["transition", "relationship"]},
        "hardness": "optional",
        "prompt": "在高度紧张的动作或高潮后，设置有功能的信息与关系沉淀，张弛有度。",
    },
    {
        "id": "T3",
        "kind": "technique",
        "name": "chapter cliffhanger",
        "when": {"phase": ["outline", "draft", "review"], "requires": ["chapter_boundary"]},
        "hardness": "required",
        "prompt": "章末必须抛出新的未解疑问、关系变故或行动危机，形成对下一章的强牵引。",
    },
]


def _slug_prefix(engine_id: str) -> str:
    parts = engine_id.replace("_", "-").split("-")
    letters = "".join(part[0].upper() for part in parts if part)
    return letters if len(letters) >= 2 else "ENG"


def _read_sources(source_path: Path) -> List[Dict[str, Any]]:
    sources = []
    if source_path.is_file():
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        sources.append({"name": source_path.name, "path": str(source_path.resolve()), "content": text})
    elif source_path.is_dir():
        for file in sorted(source_path.rglob("*")):
            if file.is_file() and file.suffix.lower() in (".txt", ".md", ".json"):
                text = file.read_text(encoding="utf-8", errors="ignore")
                sources.append({"name": str(file.relative_to(source_path)), "path": str(file.resolve()), "content": text})
    return sources


def build_engine_from_spec(engine_dir: Union[Path, str], spec: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(engine_dir).resolve()
    engine_id = spec.get("id")
    if not isinstance(engine_id, str) or not re.match(r"^[a-z][a-z0-9-]+$", engine_id):
        raise EngineValidationError(f"engine spec requires a lowercase kebab-case id: {engine_id}")

    label = spec.get("label", f"{engine_id} narrative engine")
    prefix = _slug_prefix(engine_id)

    root.mkdir(parents=True, exist_ok=True)
    cards_dir = root / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    research_dir = root / "research"
    research_dir.mkdir(parents=True, exist_ok=True)

    # 1. engine.json
    engine_json = {
        "id": engine_id,
        "version": int(spec.get("version", 1)),
        "kind": "narrative-engine",
        "label": label,
        "card_files": ["cards/models.json", "cards/techniques.json"],
        "activation": "phase-and-state",
        "language_imitation": False,
    }
    write_json_atomic(root / "engine.json", engine_json)

    # 2. cards/models.json
    models_raw = spec.get("models") or _DEFAULT_MODELS
    models = []
    for idx, item in enumerate(models_raw, start=1):
        card_id = item.get("id")
        if not card_id or not re.match(r"^[A-Z][A-Z0-9_-]+$", card_id):
            card_id = f"{prefix}-M{idx}"
        models.append({
            "id": card_id,
            "kind": "model",
            "name": str(item.get("name", f"model-{idx}")),
            "when": item.get("when", {"phase": ["outline", "scene", "review"]}),
            "requires": item.get("requires", ["character"]),
            "hardness": item.get("hardness", "recommended"),
            "prompt": str(item.get("prompt", "")),
        })
    write_json_atomic(cards_dir / "models.json", models)

    # 3. cards/techniques.json
    techs_raw = spec.get("techniques") or _DEFAULT_TECHNIQUES
    techniques = []
    for idx, item in enumerate(techs_raw, start=1):
        card_id = item.get("id")
        if not card_id or not re.match(r"^[A-Z][A-Z0-9_-]+$", card_id):
            card_id = f"{prefix}-T{idx}"
        techniques.append({
            "id": card_id,
            "kind": "technique",
            "name": str(item.get("name", f"technique-{idx}")),
            "when": item.get("when", {"phase": ["scene", "draft"]}),
            "requires": item.get("requires", []),
            "hardness": item.get("hardness", "recommended"),
            "prompt": str(item.get("prompt", "")),
        })
    write_json_atomic(cards_dir / "techniques.json", techniques)

    # 4. applicability.md
    applicability_content = spec.get("applicability") or (
        f"# {label} 适用条件\n\n"
        f"该引擎提取自相关文学样本与叙事素材，提供经过实证的思考工具与技法卡。\n"
        f"只有当前章节的阶段 (phase)、场景类型 (scene_types) 与所需状态满足卡片谓词时，对应卡片才激活。\n"
        f"本引擎不要求特定题材词汇，着重于因果推进、情感落地与场景控制。\n"
    )
    (root / "applicability.md").write_text(applicability_content.strip() + "\n", encoding="utf-8")

    # 5. limits.md
    limits_content = spec.get("limits") or (
        f"# {label} 使用边界与反模式\n\n"
        f"- **非语言模仿**：本引擎提供叙事决策模型，禁止生搬硬套原作者特定修辞或词调。\n"
        f"- **因地制宜**：技法卡不是全局红线，仅在对应场景类型中作为辅助启发式生效。\n"
        f"- **诚实边界**：对未知世界观与未登记实体不擅自脑补设定，缺失依赖必须阻断并显式补充。\n"
        f"- **避免陈词滥调**：拒绝机械降神，拒绝连续章节复用相同冲突化解方式。\n"
    )
    (root / "limits.md").write_text(limits_content.strip() + "\n", encoding="utf-8")

    # 6. research/
    research = spec.get("research", {})
    sources_summary = research.get("sources_summary", "语料提炼沉淀自用户提供的小说或文章参考。")
    principles_text = research.get("craft_principles", "关注 How they write/think，从语料因果逻辑中提炼可复用技法，而非简单复读词句。")
    (research_dir / "README.md").write_text(f"# 蒸馏研究摘要\n\n{sources_summary}\n", encoding="utf-8")
    (research_dir / "craft-principles.md").write_text(f"# 核心叙事法则\n\n{principles_text}\n", encoding="utf-8")

    # 7. manifest.json
    manifest = write_manifest(root)

    # 8. self-verification
    load_engine(root, require_manifest=True)

    return {
        "status": "PASS",
        "engine": engine_id,
        "path": str(root),
        "manifest": manifest,
        "models_count": len(models),
        "techniques_count": len(techniques),
    }


def prepare_distill(
    source_path_input: Union[str, Path],
    engine_id: Optional[str] = None,
    label: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    source_path = Path(source_path_input).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"source path does not exist: {source_path}")

    if not engine_id:
        clean_name = re.sub(r"[^a-zA-Z0-9]+", "-", source_path.stem).strip("-").lower()
        if not clean_name or not re.match(r"^[a-z]", clean_name):
            clean_name = f"eng-{clean_name or 'distilled'}"
        engine_id = clean_name
    elif not re.match(r"^[a-z][a-z0-9-]+$", engine_id):
        raise EngineValidationError(f"engine id must be lowercase kebab-case: {engine_id}")

    label_str = label or f"{engine_id} narrative engine"
    sources = _read_sources(source_path)
    total_chars = sum(len(s["content"]) for s in sources)
    names = [s["name"] for s in sources]
    prefix = _slug_prefix(engine_id)

    # Determine staging workspace
    if output_dir:
        staging_dir = Path(output_dir).resolve() / ".staging" / engine_id
    else:
        staging_dir = Path.cwd().resolve() / ".novelforge" / "staging" / "engines" / engine_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    spec_file = staging_dir / "distill-spec.json"

    # Pre-populate spec template
    spec_payload = {
        "id": engine_id,
        "label": label_str,
        "version": 1,
        "sources_scanned": names,
        "total_source_characters": total_chars,
        "applicability": (
            f"# {label_str} 适用条件\n\n"
            f"基于 {len(sources)} 份参考语料提炼。\n"
            f"适用于人物因果与情节张力推动的叙事场景。\n"
        ),
        "limits": (
            f"# {label_str} 诚实边界与反模式\n\n"
            f"- 仅提供叙事启发式，严禁机械仿造特定作者文风词调。\n"
            f"- 遇到缺失依赖必须阻断，不得擅自编造未登记事实。\n"
            f"- 技法卡只在满足条件时生效，非全局硬红线。\n"
        ),
        "models": [
            {
                "id": f"{prefix}-M1",
                "name": "character agency and causality",
                "when": {"phase": ["outline", "scene", "review"]},
                "requires": ["character"],
                "hardness": "required",
                "prompt": "让转折基于人物核心动机与主动选择，避免由外在巧合主导情节。",
            },
            {
                "id": f"{prefix}-M2",
                "name": "grounded emotional stakes",
                "when": {"phase": ["scene", "draft", "review"], "scene_types": ["choice", "loss"]},
                "requires": ["emotional_change"],
                "hardness": "required",
                "prompt": "通过场景支点、人物肢体细节与具体代价呈现情绪波澜。",
            },
            {
                "id": f"{prefix}-M3",
                "name": "thematic driving root",
                "when": {"phase": ["master-outline", "outline", "review"], "requires": ["long_form"]},
                "hardness": "recommended",
                "prompt": "为故事锚定稳定的深层母题与价值张力，使长篇情节有内在主线。",
            },
        ],
        "techniques": [
            {
                "id": f"{prefix}-T1",
                "name": "unresolved tension hook",
                "when": {"phase": ["outline", "draft", "review"], "requires": ["chapter_boundary"]},
                "hardness": "required",
                "prompt": "章节结尾留下清晰的情节悬念、认知错位或行动代价，驱动后续章节。",
            },
            {
                "id": f"{prefix}-T2",
                "name": "contrastive pacing",
                "when": {"phase": ["scene", "draft"], "scene_types": ["transition", "relationship"]},
                "hardness": "optional",
                "prompt": "激烈对抗后留出沉淀空间，展现角色反思与关系微调。",
            },
        ],
        "research": {
            "sources_summary": f"采样来源共 {len(sources)} 份语料：{', '.join(names[:5])}，文本总量约 {total_chars} 字符。",
            "craft_principles": "叙事引擎提炼：提取跨场景可复用的叙事规律与因果结构，剔除特定词汇与剧情细节依赖。",
        },
    }

    write_json_atomic(spec_file, spec_payload)

    target_engine_dir = Path(output_dir).resolve() / engine_id if output_dir else Path.cwd().resolve() / ".novelforge" / "engines" / engine_id
    build_cmd = f"python3 scripts/novelforgectl.py engine distill build {spec_file} --output {target_engine_dir.parent}"

    return {
        "status": "PREPARED",
        "engine_id": engine_id,
        "staging_spec": str(spec_file),
        "sources_scanned": names,
        "total_characters": total_chars,
        "io_contract": {
            "inputs": [
                {"role": "source_material", "name": s["name"], "path": s["path"]}
                for s in sources
            ],
            "output": {
                "role": "distill_spec",
                "path": str(spec_file),
                "format": "json",
                "description": "待模型提炼回填的叙事引擎规范文件 (包含 models, techniques, applicability, limits)",
            },
            "build_command": build_cmd,
        },
    }


def build_distill_from_spec(
    spec_path_input: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    spec_file = Path(spec_path_input).resolve()
    if not spec_file.is_file():
        raise FileNotFoundError(f"spec file does not exist: {spec_file}")
    spec = read_json(spec_file)

    engine_id = spec.get("id")
    if not isinstance(engine_id, str) or not re.match(r"^[a-z][a-z0-9-]+$", engine_id):
        raise EngineValidationError(f"spec requires a valid lowercase kebab-case id: {engine_id}")

    if output_dir:
        out_root = Path(output_dir).resolve() / engine_id
    else:
        out_root = Path.cwd().resolve() / ".novelforge" / "engines" / engine_id

    result = build_engine_from_spec(out_root, spec)
    result["install_command"] = f"python3 scripts/novelforgectl.py engine install <project-root> {out_root}"
    return result


def distill_engine(
    source_path_input: Union[str, Path],
    engine_id: Optional[str] = None,
    label: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None,
    spec_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    if spec_path:
        return build_distill_from_spec(spec_path, output_dir=output_dir)

    source_path = Path(source_path_input).resolve()
    if source_path.is_file() and source_path.suffix.lower() == ".json":
        try:
            candidate = read_json(source_path)
            if isinstance(candidate, dict) and ("models" in candidate or "techniques" in candidate):
                return build_distill_from_spec(source_path, output_dir=output_dir)
        except (ValueError, OSError):
            pass

    # Two-step automatic pipeline
    prepared = prepare_distill(source_path, engine_id=engine_id, label=label, output_dir=output_dir)
    built = build_distill_from_spec(prepared["staging_spec"], output_dir=output_dir)
    built["sources_scanned"] = prepared["sources_scanned"]
    built["staging_spec"] = prepared["staging_spec"]
    built["io_contract"] = prepared["io_contract"]
    return built
