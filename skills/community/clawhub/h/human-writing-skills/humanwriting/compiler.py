from __future__ import annotations

import re
from pathlib import Path

from .detection import has_directed_interaction
from .original import build_original_pack, build_original_pack_text
from .protection import build_protection_manifest, detect_serious_document
from .reference import DEFAULT_REFERENCE_BUDGET, build_reference_pack
from .source import DEFAULT_SOURCE_BUDGET, build_source_pack
from .skills import load_many, load_skill

NUMBER_SENSE_REVIEW_STYLES = {"fiction", "webnovel", "self-media"}
NARRATIVE_NATURALNESS_DOCUMENT_TYPES = {"fiction", "webnovel", "self-media"}
DIALOGUE_GENERATION_STYLES = {"fiction", "webnovel"}
DIALOGUE_GENERATION_PATTERN = re.compile(
    r"(?:写|续写|生成|创作|展开|安排).{0,24}(?:对话|对白|谈判|会谈|沟通|交涉|审问|讯问|争论|争吵|聊天|问答|"
    r"人物互动|角色互动|相处|重逢|初见|初次见面|表白|告白|试探|安慰|和解|对峙|冲突)|"
    r"(?:对话|对白|谈判|会谈|沟通|交涉|审问|讯问|争论|争吵|聊天)(?:场景|片段|戏|章节)?|"
    r"(?:两人|二人|人物|角色).{0,12}(?:互动|相处|重逢|初见|试探|安慰|和解|对峙|冲突)|"
    r"\b(?:write|continue|draft|create).{0,40}(?:dialogue|conversation|negotiation|meeting|interview|interrogation|argument|"
    r"character interaction|reunion|confession|reconciliation|confrontation|comforting scene)|"
    r"\b(?:dialogue|conversation|negotiation|interrogation|character interaction|reunion|confession|reconciliation|confrontation)\s+(?:scene|chapter|exchange)\b",
    re.IGNORECASE,
)
DIALOGUE_NEGATION_PATTERN = re.compile(
    r"(?:不要|避免|无需|不需要|不写|没有|无).{0,10}(?:对话|对白|谈判|会谈|沟通|交涉|审问|讯问|争论|争吵|聊天)|"
    r"\b(?:no|without|avoid|exclude).{0,16}(?:dialogue|conversation|negotiation|interview)\b",
    re.IGNORECASE,
)
REGISTER_EVIDENCE_PATTERN = re.compile(
    r"(?:方言|口音|地域|籍贯|母语|外语|双语|多语|翻译|敬语|敬称|称谓|语气词|口头禅|"
    r"国籍|出生地|成长地|东北人|广东人|美国人|日本人|韩国人|"
    r"东北话|粤语|广东话|京片子|北京话|上海话|四川话|闽南语|普通话|英语|日语|韩语|法语|"
    r"西班牙语|葡萄牙语|阿拉伯语|拉丁语|移民|留学|海外生活|语言习惯|说话习惯)|"
    r"\b(?:dialect|accent|regional speech|native language|second language|bilingual|multilingual|"
    r"translation|honorific|register|code-switch|speech habit|discourse particle|slang|idiolect|"
    r"nationality|birthplace|upbringing|American|Japanese|Korean)\b",
    re.IGNORECASE,
)
TRANSLATION_GENERATION_PATTERN = re.compile(
    r"(?:翻译腔|翻译成|从.{0,12}(?:翻译|译为)|译文|本地化|源语言|目标语言)|"
    r"\b(?:translate|translation|translated|locali[sz]e|localization|source language|target language|"
    r"traducci[oó]n|traduc(?:ir|e)|traduz(?:ir|a)|traduction|tradui(?:re|s))\b",
    re.IGNORECASE,
)
WORLD_GENERATION_PATTERN = re.compile(
    r"(?:世界观|架空|时代背景|历史背景|世界规则|科技水平|制度设定|社会规则|"
    r"古代|民国|唐朝|宋朝|明朝|清朝|赛博朋克|蒸汽朋克|修仙|魔法|星际)|"
    r"\b(?:worldbuilding|world rules?|historical setting|alternate history|"
    r"cyberpunk|steampunk|magic system|technology level)\b",
    re.IGNORECASE,
)
PROCESS_GENERATION_PATTERN = re.compile(
    r"(?:调查|侦查|研发|实验|谈判|会谈|审讯|诊断|手术|施工|经营|贷款|"
    r"招标|审判|训练|修炼|炼制|战斗|破案|制作|推演)(?:过程|场景|章节|细节)?|"
    r"\b(?:investigation|research process|experiment|negotiation|interrogation|"
    r"diagnosis|surgery|construction|trial|training|crafting|battle planning)\b",
    re.IGNORECASE,
)
SALIENCE_GENERATION_PATTERN = re.compile(
    r"(?:扩写|长篇|长稿|水文|灌水|篇幅分配|节奏审核|删减冗余|语义重复)|"
    r"\b(?:expand|long-form|attention budget|pacing audit|dilution|semantic repetition)\b",
    re.IGNORECASE,
)
CAPABILITY_GENERATION_PATTERN = re.compile(
    r"(?:战力|境界|等级|阶位|段位|修为|能力|异能|技能|招式|法术|装备|武器|伤势|"
    r"体力|法力|灵力|资源|冷却|克制|越级|突破|升级|训练|权限|权力等级)|"
    r"\b(?:power level|rank|tier|ability|skill|spell|equipment|weapon|injury|stamina|"
    r"mana|resource|cooldown|counter|level up|training|authority level)\b",
    re.IGNORECASE,
)
CORE_REVIEW_MODULES = [
    "editor-loop",
    "ai-trace-rubric",
]
NARRATIVE_REVIEW_MODULES = [
    "relationship-stance-audit",
]
DEEP_REVIEW_MODULES = [
    "cliche-phrase-audit",
    "formulaic-structure-audit",
    "surface-pattern-audit",
    "prose-progress-audit",
    "narrative-naturalness-audit",
]
AI_TRACE_AUDIT_MODULES = [
    "ai-trace-rubric",
    "cliche-phrase-audit",
    "formulaic-structure-audit",
    "surface-pattern-audit",
    "prose-progress-audit",
    "narrative-naturalness-audit",
    "repetition-exposition-audit",
]
NARRATIVE_AI_TRACE_MODULES = {
    "narrative-naturalness-audit",
    "repetition-exposition-audit",
}
RELATIONSHIP_AUDIT_MODULES = [
    "relationship-state",
    "relationship-stance-audit",
]
PHYSICAL_AUDIT_MODULES = [
    "forensic-physical-audit",
]
LIGHT_PHYSICAL_AUDIT_MODULE = "physical-continuity-audit"
LOGIC_AUDIT_MODULES = ["logic-causality-audit"]
CHARACTER_AUDIT_MODULES = ["character-consistency-audit"]
VOICE_AUDIT_MODULES = ["dialogue-voice-audit", "dialogue-performance-audit"]
REGISTER_AUDIT_MODULES = ["speech-register-continuity"]
TRANSLATIONESE_AUDIT_MODULES = ["translationese-audit"]
CAPABILITY_AUDIT_MODULES = ["capability-state-audit"]
SERIAL_AUDIT_MODULES = ["serial-reentry"]
MOMENTUM_AUDIT_MODULES = ["chapter-momentum-audit"]
ENDING_AUDIT_MODULES = ["earned-ending-audit"]
WORLD_AUDIT_MODULES = ["world-ontology-audit"]
PROCESS_AUDIT_MODULES = ["process-earnedness-audit"]
SALIENCE_AUDIT_MODULES = ["attention-budget-audit"]
RECURRENCE_AUDIT_MODULES = ["chapter-pattern-audit"]
REPETITION_AUDIT_MODULES = ["repetition-exposition-audit"]
TEXTURE_AUDIT_MODULES = [
    "narrative-distance-control",
    "imagery-load-audit",
    "paragraph-rhythm-audit",
    "detail-disclosure-audit",
    "scene-entry-audit",
]
PROOFREAD_AUDIT_MODULES = ["proofreading-audit"]
REFERENCE_STYLE_AUDIT_MODULES = ["reference-style-alignment"]
SOURCE_AUDIT_MODULES = ["source-grounding"]
FIDELITY_AUDIT_MODULES = ["rewrite-fidelity"]
PRESERVATION_AUDIT_MODULES = ["voice-ambiguity-preservation"]
PROTECTED_CONTENT_MODULES = ["protected-content"]
FACTUAL_SOURCE_STYLES = {"academic-paper", "formal-document", "news-report", "argumentative", "self-media"}


def generation_brief(style: str) -> str:
    if style in {"fiction", "webnovel"}:
        direction = (
            "Advance the scene through a choice, discovery, resistance, or changed interpretation. "
            "Dialogue responds with speaker-specific knowledge and aims. Avoid repeated gestures "
            "and explaining what action already showed. Quiet scenes and direct emotion labels are valid."
        )
    else:
        direction = (
            "Identify what the reader needs to understand, decide, or do. Put evidence or limits "
            "next to claims. Distinguish facts, inferences, and missing inputs. Do not invent personal experience "
            "or erase uncertainty. Keep terminology stable; formal prose need not be casual."
        )
    return "# Genre-Specific Generation Brief\n\n" + direction


HUMANIZE_QUICK_MODULES = [
    "surface-pattern-audit",
    "voice-ambiguity-preservation",
]
HUMANIZE_DEEP_MODULES = [
    "editor-loop",
    "ai-trace-rubric",
    "cliche-phrase-audit",
    "formulaic-structure-audit",
    "prose-progress-audit",
    "narrative-naturalness-audit",
    "imperfect-prose",
]
AUDIT_PROFILES = {
    "full",
    "logic",
    "character",
    "voice",
    "register",
    "capability",
    "serial",
    "momentum",
    "ending",
    "world",
    "process",
    "salience",
    "recurrence",
    "repetition",
    "texture",
    "physical",
    "relationship",
    "ai-trace",
    "numbers",
    "proofread",
    "style-match",
    "sources",
    "fidelity",
    "preservation",
}


CORE_DIRECTIVE = """# Core Directive

Write with a human editor's priorities: intention, specificity, continuity, and rhythm.
Avoid generic filler, repetitive sentence frames, inflated transitions, empty certainty,
summary paragraphs that merely restate the prompt, and precision that does not fit
the genre or narrator.
Do not stack parallel comparisons merely to intensify; keep multiple comparison clauses
only when each carries a distinct and necessary fact.
In fiction and webnovels, replace unrequested scene mini-headings or time cards with
a prose bridge from prior residue to elapsed change and the first new action.

Before drafting, identify the active context, genre promise, reader expectation, and
the one thing this passage must change. During drafting, preserve established facts.
After drafting, revise once for cadence, concrete detail, physical state, and continuity.
Use exact measurements, counts, and numbers when the context earns them; otherwise
prefer felt, relational, or scene-specific scale.
Before final output, check that each sentence has the subjects, objects, complements,
and referents its verbs and connectors require; preserve deliberate spoken ellipsis.
"""


CONTINUITY_DIRECTIVE = """# Continuity Protocol

Maintain a running ledger while generating long text:

- Fixed facts: names, dates, locations, relationships, rules, timeline
- Active threads: unresolved conflicts, questions, clues, promises, arguments
- Relationship state: what each important person knows, wants, hides, owes, refuses,
  and can use as leverage
- Relationship stance: who may safely mention, praise, criticize, compare, expose,
  or conceal whom in the current audience
- Voice anchors: diction, directness, disclosure strategy, domain limits,
  audience shifts, pacing, and taboo phrases
- Scene or section state: where the previous output ended and what must connect next
- Beat bridge: what residue from the previous beat enters the next beat, what changes,
  and what pressure or question remains open
- Physical state: positions, resource modes/capacity, occupancy, movement gates,
  transformation gates, clothing, props, injuries, reachable objects
- Change log: what became newly true in the current passage

If context is missing, make the smallest possible assumption and mark it as an assumption.
Do not overwrite established facts for convenience.
Scene and paragraph transitions should be earned by cause, perception, object continuity,
or changed character state rather than generic connective phrasing.
"""


def read_optional(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8").strip()


def append_missing(selected_modules: list, names: list[str]) -> None:
    selected_names = {module.name for module in selected_modules}
    for name in names:
        if name not in selected_names:
            selected_modules.append(load_skill(name))
            selected_names.add(name)


def compile_prompt(
    style: str,
    task: str,
    context_path: str | None = None,
    modules: list[str] | None = None,
    review: bool = False,
    strict_continuity: bool = False,
    number_sense: bool = False,
    deep_review: bool = False,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    reference_budget: int = DEFAULT_REFERENCE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    original_path: str | None = None,
    protect_content: bool = False,
    protect_terms: list[str] | None = None,
    context_text: str | None = None,
    original_text: str | None = None,
) -> str:
    skill = load_skill(style)
    if skill.kind != "style":
        raise ValueError(f"'{style}' is a module, not a primary style skill.")
    selected_modules = load_many(modules or [])
    append_missing(selected_modules, ["generation-quality"])
    if context_path and context_text is not None:
        raise ValueError("Provide either context_path or context_text, not both.")
    context = context_text.strip() if context_text is not None else read_optional(context_path)
    reference_pack = build_reference_pack(
        reference_paths,
        reference_style,
        task=task,
        budget=reference_budget,
    )
    source_pack = build_source_pack(source_paths, source_budget)
    original_pack = build_original_pack_text(original_text) if original_text is not None else build_original_pack(original_path)
    dialogue_generation_active = (
        style in DIALOGUE_GENERATION_STYLES
        and bool(DIALOGUE_GENERATION_PATTERN.search(task))
        and not DIALOGUE_NEGATION_PATTERN.search(task)
    )
    interaction_generation_active = (
        style in DIALOGUE_GENERATION_STYLES
        and has_directed_interaction(task + "\n" + (original_text or ""))
    )
    if dialogue_generation_active or interaction_generation_active:
        append_missing(selected_modules, VOICE_AUDIT_MODULES)
    if dialogue_generation_active:
        if REGISTER_EVIDENCE_PATTERN.search(
            "\n".join(part for part in [task, context] if part)
        ):
            append_missing(selected_modules, REGISTER_AUDIT_MODULES)
    if TRANSLATION_GENERATION_PATTERN.search("\n".join(part for part in [task, context] if part)):
        append_missing(selected_modules, TRANSLATIONESE_AUDIT_MODULES)
    if style in DIALOGUE_GENERATION_STYLES and WORLD_GENERATION_PATTERN.search(
        "\n".join(part for part in [task, context] if part)
    ):
        append_missing(selected_modules, WORLD_AUDIT_MODULES)
    if style in DIALOGUE_GENERATION_STYLES and PROCESS_GENERATION_PATTERN.search(task):
        append_missing(selected_modules, PROCESS_AUDIT_MODULES)
    if style in DIALOGUE_GENERATION_STYLES and CAPABILITY_GENERATION_PATTERN.search(task):
        append_missing(selected_modules, CAPABILITY_AUDIT_MODULES)
    if style in DIALOGUE_GENERATION_STYLES and SALIENCE_GENERATION_PATTERN.search(task):
        append_missing(selected_modules, SALIENCE_AUDIT_MODULES)
    if reference_pack.active:
        append_missing(selected_modules, REFERENCE_STYLE_AUDIT_MODULES)
    protection_requested = protect_content or bool(protect_terms) or any(
        module.name == "protected-content" for module in selected_modules
    )
    auto_protection, auto_protection_reason = detect_serious_document(
        text=context,
        document_type=style,
        task=task,
    )
    protection_active = protection_requested or auto_protection
    protection_reason = (
        "Explicit protection was requested."
        if protection_requested
        else auto_protection_reason
    )
    if protection_active:
        append_missing(selected_modules, PROTECTED_CONTENT_MODULES)
    source_grounding_active = source_pack.active and (auto_protection or style in FACTUAL_SOURCE_STYLES)
    if source_grounding_active:
        append_missing(selected_modules, SOURCE_AUDIT_MODULES)
    if original_pack.active:
        append_missing(selected_modules, FIDELITY_AUDIT_MODULES)
        append_missing(selected_modules, PRESERVATION_AUDIT_MODULES)
    if strict_continuity:
        append_missing(
            selected_modules,
            [
                "occupancy-capacity",
                "spatial-blocking",
                "appearance-prop-continuity",
            ],
        )
    if review or deep_review:
        append_missing(selected_modules, CORE_REVIEW_MODULES)
    if deep_review:
        append_missing(selected_modules, NARRATIVE_REVIEW_MODULES)
        append_missing(selected_modules, DEEP_REVIEW_MODULES)
    if (number_sense or (deep_review and style in NUMBER_SENSE_REVIEW_STYLES)) and "natural-measurement" not in [
        module.name for module in selected_modules
    ]:
        selected_modules.append(load_skill("natural-measurement"))
    blocks = [
        CORE_DIRECTIVE.strip(),
        generation_brief(style),
        CONTINUITY_DIRECTIVE.strip(),
        f"# Selected Skill: {skill.name}\n\n{skill.content}",
    ]
    for module in selected_modules:
        blocks.append(f"# Technique Module: {module.name}\n\n{module.content}")
    if context:
        blocks.append(f"# Project Context\n\n{context}")
    if reference_pack.active:
        blocks.append(reference_pack.block)
    if source_grounding_active:
        blocks.append(source_pack.block)
    if original_pack.active:
        blocks.append(original_pack.block)
    if protection_active:
        blocks.append(f"# Protection Activation\n\n{protection_reason}")
        protected_source = "\n".join(part for part in [context, task] if part)
        blocks.append(build_protection_manifest(protected_source, protect_terms))
    blocks.append(f"# Task\n\n{task.strip()}")
    blocks.append(
        "# Output Contract\n\n"
        "Return only the requested writing unless the user asks for notes. "
        "Keep continuity with the context above. Make the prose feel edited, lived-in, "
        "and specific to the genre rather than broadly polished."
    )
    return "\n\n---\n\n".join(blocks) + "\n"


def compile_humanize_prompt(
    draft_path: str,
    style: str,
    mode: str = "quick",
    task: str | None = None,
    context_path: str | None = None,
    modules: list[str] | None = None,
    strict_continuity: bool = False,
    with_examples: bool = False,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    reference_budget: int = DEFAULT_REFERENCE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    protect_content: bool = False,
    protect_terms: list[str] | None = None,
) -> str:
    draft = read_optional(draft_path)
    return compile_humanize_prompt_text(
        draft,
        style=style,
        mode=mode,
        task=task,
        context_path=context_path,
        modules=modules,
        strict_continuity=strict_continuity,
        with_examples=with_examples,
        reference_paths=reference_paths,
        reference_style=reference_style,
        reference_budget=reference_budget,
        source_paths=source_paths,
        source_budget=source_budget,
        protect_content=protect_content,
        protect_terms=protect_terms,
    )


def compile_humanize_prompt_text(
    draft: str,
    style: str,
    mode: str = "quick",
    task: str | None = None,
    context_path: str | None = None,
    context_text: str | None = None,
    modules: list[str] | None = None,
    strict_continuity: bool = False,
    with_examples: bool = False,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    reference_budget: int = DEFAULT_REFERENCE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    protect_content: bool = False,
    protect_terms: list[str] | None = None,
) -> str:
    draft = draft.strip()
    if not draft:
        raise ValueError("The humanize command requires a non-empty --draft input.")
    if mode not in {"quick", "deep"}:
        raise ValueError("Humanize mode must be 'quick' or 'deep'.")

    selected = list(modules or [])
    for name in HUMANIZE_QUICK_MODULES:
        if name not in selected:
            selected.append(name)
    if mode == "deep":
        for name in HUMANIZE_DEEP_MODULES:
            if name not in selected:
                selected.append(name)
    if with_examples and "humanize-examples" not in selected:
        selected.append("humanize-examples")

    rewrite_task = task or (
        "Rewrite the supplied draft in the same language and genre. Preserve its facts, "
        "claim scope, useful ambiguity, intentional repetition, recurring motifs, speaker "
        "identity, unresolved interaction pressure, and continuity. Repair only evidenced "
        "AI-shaped wording, formulaic structure, missing grammatical slots, and clarity "
        "problems. Return only the revised text."
    )
    return compile_prompt(
        style=style,
        task=rewrite_task,
        context_path=context_path,
        context_text=context_text,
        modules=selected,
        strict_continuity=strict_continuity,
        reference_paths=reference_paths,
        reference_style=reference_style,
        reference_budget=reference_budget,
        source_paths=source_paths,
        source_budget=source_budget,
        original_text=draft,
        protect_content=protect_content,
        protect_terms=protect_terms,
    )


def compile_audit_prompt(
    draft_path: str | None,
    context_path: str | None = None,
    modules: list[str] | None = None,
    strict_continuity: bool = True,
    number_sense: bool = False,
    profiles: list[str] | None = None,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    reference_budget: int = DEFAULT_REFERENCE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    original_path: str | None = None,
    protect_content: bool = False,
    protect_terms: list[str] | None = None,
    document_type: str = "auto",
    auto_protect: bool = True,
    draft_text: str | None = None,
    context_text: str | None = None,
) -> str:
    selected_modules = load_many(modules or [])
    selected_names = {module.name for module in selected_modules}
    light_physical_requested = LIGHT_PHYSICAL_AUDIT_MODULE in selected_names
    if draft_path and draft_text is not None:
        raise ValueError("Provide either draft_path or draft_text, not both.")
    if context_path and context_text is not None:
        raise ValueError("Provide either context_path or context_text, not both.")
    draft = draft_text.strip() if draft_text is not None else read_optional(draft_path)
    context = context_text.strip() if context_text is not None else read_optional(context_path)
    requested_profiles = set(profiles or ["full"])
    reference_pack = build_reference_pack(
        reference_paths,
        reference_style,
        budget=reference_budget,
    )
    source_pack = build_source_pack(source_paths, source_budget)
    original_pack = build_original_pack(original_path)
    if reference_pack.active:
        requested_profiles.add("style-match")
    if original_pack.active and "preservation" not in requested_profiles:
        requested_profiles.add("fidelity")
    if number_sense:
        requested_profiles.add("numbers")
    serious_document, serious_document_reason = detect_serious_document(
        text=draft,
        document_type=document_type,
    )
    source_eligible = serious_document or document_type in FACTUAL_SOURCE_STYLES
    narrative_naturalness_enabled = document_type in NARRATIVE_NATURALNESS_DOCUMENT_TYPES or (
        document_type == "auto" and not serious_document
    )
    if source_pack.active and source_eligible:
        requested_profiles.add("sources")
    unknown_profiles = requested_profiles - AUDIT_PROFILES
    if unknown_profiles:
        raise ValueError(f"Unknown audit profile: {', '.join(sorted(unknown_profiles))}")
    if "style-match" in requested_profiles and not reference_pack.active:
        raise ValueError("The style-match profile requires --reference or --reference-style.")
    if "fidelity" in requested_profiles and not original_pack.active:
        raise ValueError("The fidelity profile requires --original with the pre-rewrite text.")
    if "preservation" in requested_profiles and not original_pack.active:
        raise ValueError("The preservation profile requires --original with the pre-rewrite text.")
    if "serial" in requested_profiles and not context:
        raise ValueError("The serial profile requires --context with prior chapters or a continuity ledger.")
    if "capability" in requested_profiles and not context:
        raise ValueError("The capability profile requires --context with prior state or a continuity ledger.")
    if "sources" in requested_profiles and not source_pack.active:
        raise ValueError("The sources profile requires one or more --source files.")
    if "sources" in requested_profiles and not source_eligible:
        raise ValueError("The sources profile is limited to serious or explicitly factual document types; choose self-media or argumentative for factual essays.")
    if "repetition" in requested_profiles and not narrative_naturalness_enabled:
        raise ValueError("The repetition profile is limited to fiction, webnovels, and narrative self-media.")
    if "physical" in requested_profiles and light_physical_requested:
        raise ValueError(
            "The physical profile already uses forensic-physical-audit; "
            "do not combine it with physical-continuity-audit."
        )
    physical_enabled = "physical" in requested_profiles or (
        "full" in requested_profiles and strict_continuity and not light_physical_requested
    )
    relationship_enabled = bool(requested_profiles & {"full", "relationship"})
    ai_trace_enabled = bool(requested_profiles & {"full", "ai-trace"})
    numbers_enabled = bool(requested_profiles & {"full", "numbers"})
    logic_enabled = bool(requested_profiles & {"full", "logic"})
    character_enabled = bool(requested_profiles & {"full", "character"})
    voice_enabled = "voice" in requested_profiles
    register_enabled = "register" in requested_profiles
    capability_enabled = "capability" in requested_profiles
    serial_enabled = "serial" in requested_profiles
    momentum_enabled = "momentum" in requested_profiles
    ending_enabled = "ending" in requested_profiles
    world_enabled = "world" in requested_profiles
    process_enabled = "process" in requested_profiles
    salience_enabled = "salience" in requested_profiles
    recurrence_enabled = "recurrence" in requested_profiles
    repetition_enabled = "repetition" in requested_profiles
    texture_enabled = "texture" in requested_profiles
    proofread_enabled = bool(requested_profiles & {"full", "proofread"})
    style_match_enabled = "style-match" in requested_profiles
    sources_enabled = "sources" in requested_profiles
    fidelity_enabled = "fidelity" in requested_profiles
    preservation_enabled = "preservation" in requested_profiles

    if logic_enabled:
        append_missing(selected_modules, LOGIC_AUDIT_MODULES)
    if character_enabled:
        append_missing(selected_modules, CHARACTER_AUDIT_MODULES)
    if voice_enabled:
        append_missing(selected_modules, VOICE_AUDIT_MODULES)
    if register_enabled:
        append_missing(selected_modules, REGISTER_AUDIT_MODULES)
    if capability_enabled:
        append_missing(selected_modules, CAPABILITY_AUDIT_MODULES)
    if serial_enabled:
        append_missing(selected_modules, SERIAL_AUDIT_MODULES)
    if momentum_enabled:
        append_missing(selected_modules, MOMENTUM_AUDIT_MODULES)
    if ending_enabled:
        append_missing(selected_modules, ENDING_AUDIT_MODULES)
    if world_enabled:
        append_missing(selected_modules, WORLD_AUDIT_MODULES)
    if process_enabled:
        append_missing(selected_modules, PROCESS_AUDIT_MODULES)
    if salience_enabled:
        append_missing(selected_modules, SALIENCE_AUDIT_MODULES)
    if recurrence_enabled:
        append_missing(selected_modules, RECURRENCE_AUDIT_MODULES)
    if repetition_enabled:
        append_missing(selected_modules, REPETITION_AUDIT_MODULES)
    if texture_enabled:
        append_missing(selected_modules, TEXTURE_AUDIT_MODULES)
    if physical_enabled:
        append_missing(selected_modules, PHYSICAL_AUDIT_MODULES)
    if relationship_enabled:
        append_missing(selected_modules, RELATIONSHIP_AUDIT_MODULES)
    if ai_trace_enabled:
        append_missing(
            selected_modules,
            [
                module
                for module in AI_TRACE_AUDIT_MODULES
                if module not in NARRATIVE_AI_TRACE_MODULES or narrative_naturalness_enabled
            ],
        )
    if numbers_enabled:
        append_missing(selected_modules, ["natural-measurement"])
    if proofread_enabled:
        append_missing(selected_modules, PROOFREAD_AUDIT_MODULES)
    if style_match_enabled:
        append_missing(selected_modules, REFERENCE_STYLE_AUDIT_MODULES)
    if sources_enabled:
        append_missing(selected_modules, SOURCE_AUDIT_MODULES)
    if fidelity_enabled:
        append_missing(selected_modules, FIDELITY_AUDIT_MODULES)
    if preservation_enabled:
        append_missing(selected_modules, PRESERVATION_AUDIT_MODULES)
    protection_requested = protect_content or bool(protect_terms) or any(
        module.name == "protected-content" for module in selected_modules
    )
    auto_protection, auto_protection_reason = serious_document, serious_document_reason
    protection_active = protection_requested or (auto_protect and auto_protection)
    protection_reason = (
        "Explicit protection was requested."
        if protection_requested
        else auto_protection_reason
    )
    if protection_active:
        append_missing(selected_modules, PROTECTED_CONTENT_MODULES)

    blocks = [
        "# Audit Directive\n\n"
        "You are auditing an existing draft, not generating new prose. "
        "Do not assume the draft is correct. Audit only the selected profiles, extract "
        "evidence before judging, distinguish contradictions from intentional exceptions, "
        "and propose the smallest repair that preserves the author's intent. "
        f"Selected profiles: {', '.join(sorted(requested_profiles))}.",
        CONTINUITY_DIRECTIVE.strip(),
    ]
    for module in selected_modules:
        blocks.append(f"# Audit Module: {module.name}\n\n{module.content}")
    if context:
        blocks.append(f"# Continuity Ledger\n\n{context}")
    if reference_pack.active:
        blocks.append(reference_pack.block)
    if sources_enabled:
        blocks.append(source_pack.block)
    if fidelity_enabled or preservation_enabled:
        blocks.append(original_pack.block)
    if protection_active:
        blocks.append(f"# Protection Activation\n\n{protection_reason}")
        blocks.append(build_protection_manifest(draft, protect_terms))
    blocks.append(f"# Draft To Audit\n\n{draft}")
    task_lines = [
        "# Audit Task",
        "",
        "Return evidence first, then confirmed contradictions, uncertain cases, and a minimal repair plan.",
    ]
    if physical_enabled:
        task_lines.append(
            "For physical continuity, require on-page evidence for movement, occupancy, "
            "resource-mode changes, barriers, reach, clothing, props, and body-state changes."
        )
    if logic_enabled:
        task_lines.append(
            "For logic, map trigger -> action or inference -> result -> consequence and check "
            "time, knowledge, motive, rules, resources, and unresolved costs."
        )
    if character_enabled:
        task_lines.append(
            "For character consistency, compare goals, voice, knowledge, competence, boundaries, "
            "status, and recent change gates before calling a deviation an error."
        )
    if voice_enabled:
        task_lines.append(
            "For dialogue voice, build evidence-backed speaker models and a scene speech contract; "
            "check goals, topic, response linkage, knowledge, role constraints, audience, register, "
            "motivated change gates, and whether pressure-bearing turns receive uptake or become "
            "explicit interaction debt without relying on occupational stereotypes."
            " Inspect every directed speech or action in the assigned scope, in both directions; "
            "separate simultaneous verbal and physical obligations, check adjacent paragraphs, "
            "and report a gap only when reception or an evidenced pending state is absent."
        )
    if register_enabled:
        task_lines.append(
            "For speech register, compare each speaker's established language identity, dialect "
            "exposure, politeness, address forms, discourse particles, vocabulary, translation "
            "convention, and audience shifts; require an evidence-backed gate for code-switching "
            "and distinguish spoken ellipsis from a missing grammatical slot."
        )
    if capability_enabled:
        task_lines.append(
            "For capability continuity, separate permanent baseline from temporary state, then "
            "verify abilities, rank, authority, equipment, injuries, resources, cooldowns, counters, "
            "costs, and every increase, loss, exception, or surprising outcome against an on-page gate."
        )
    if serial_enabled:
        task_lines.append(
            "For serial reentry, compare the draft with supplied prior material, keep only live "
            "carryovers, and flag both recap dumps and chapter resets."
        )
    if momentum_enabled:
        task_lines.append(
            "For chapter momentum, map each chapter's entry pressure, irreversible turn, "
            "payoff, residue, and exit pressure; flag atmosphere-only openings, repeated "
            "resets, and hooks unsupported by the chapter's own action."
        )
    if ending_enabled:
        task_lines.append(
            "For ending earnedness, locate the last meaningful change and test every later "
            "sentence for new consequence, handoff, changed meaning, or required document "
            "function; try deletion before replacing a reflective bookend with another stock exit."
        )
    if world_enabled:
        task_lines.append(
            "For world ontology, extract the active era, technology, institution, social, "
            "and speculative constraints before judging objects or actions as compatible."
        )
    if process_enabled:
        task_lines.append(
            "For process earnedness, map promise -> attempt -> resistance -> judgment or skill "
            "-> cost or evidence -> result and locate the earliest unearned jump."
        )
    if salience_enabled:
        task_lines.append(
            "For attention budget, compare paragraph-level word allocation with the scene contract, "
            "and locate semantic echoes or low-value expansion that displaces consequential beats."
        )
    if recurrence_enabled:
        task_lines.append(
            "For chapter recurrence, fingerprint at least three chapters by entry, pressure, "
            "transaction, turn, crest, and exit before flagging repeated architecture."
        )
    if repetition_enabled:
        task_lines.append(
            "For repetition, map exact echoes, repeated action/choreography frames, and narrator "
            "explanations that merely restate visible dialogue or action; retain deliberate refrains, "
            "motifs, and necessary recap, but identify the smallest cut, merge, or evidence-led repair."
        )
    if texture_enabled:
        task_lines.append(
            "For prose texture, audit narrative distance, image and sensory load, show-then-gloss "
            "duplication, paragraph cadence, and premature detail inventory."
        )
    if relationship_enabled:
        task_lines.append(
            "For relationship continuity, extract speaker -> listener/audience -> referenced "
            "party and check stance, knowledge, rank, mention policy, secrecy, motive, and consequence."
        )
    if ai_trace_enabled:
        task_lines.append(
            "For AI-trace review, identify exact phrases or paragraph structures before scoring; "
            "also locate orphaned pressure-bearing interactions before a topic or scene shift, "
            "and do not flag a pattern without quoting or locating its evidence."
        )
    if numbers_enabled:
        task_lines.append(
            "For number sense, classify every exact number before deciding whether to keep, "
            "soften, generalize, or remove it."
        )
    if proofread_enabled:
        task_lines.append(
            "For proofreading, separate definite mechanical errors from house-style choices and "
            "intentional voice; do not rewrite plot or characterization."
        )
    if style_match_enabled:
        task_lines.append(
            "For reference style, build an evidence-backed style card, compare the draft on each "
            "dimension, and flag copying or context contamination as well as stylistic drift."
        )
    if sources_enabled:
        task_lines.append(
            "For source grounding, map each material claim to a supplied source location, distinguish "
            "existence from support, and mark anything requiring external verification instead of guessing."
        )
    if fidelity_enabled:
        task_lines.append(
            "For rewrite fidelity, compare original and candidate claim units; flag omitted, broadened, "
            "reversed, reattributed, reordered, or invented meaning and propose the smallest repair."
        )
    if preservation_enabled:
        task_lines.append(
            "For voice and ambiguity preservation, compare the original with the candidate and locate "
            "flattened uncertainty, intentional repetition, motifs, hesitation, speaker markers, subtext, "
            "or unresolved interaction pressure; distinguish those losses from legitimate clarity repairs."
        )
    blocks.append("\n".join(task_lines))
    return "\n\n---\n\n".join(blocks) + "\n"


def compile_audit_prompt_text(
    draft: str,
    **kwargs: object,
) -> str:
    """Compile an audit prompt from in-memory text for editors and MCP clients."""

    return compile_audit_prompt(None, draft_text=draft, **kwargs)
