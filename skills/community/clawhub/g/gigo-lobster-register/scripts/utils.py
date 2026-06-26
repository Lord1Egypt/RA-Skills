from __future__ import annotations

import json
import math
import os
import platform
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

DEFAULT_OUTPUT_DIRNAME = "output"
DEFAULT_CHECKPOINT_NAME = ".eval_checkpoint.json"
RUN_ARTIFACT_NAMES = (
    "gigo-run.log",
    "lobster-report.html",
    "lobster-cert.png",
    "lobster-cert.svg",
)
SUPPORTED_SKILL_OSES = {"darwin", "linux", "windows"}
VALID_LANGS = {"zh", "en"}
VALID_UPLOAD_MODES = {"ask", "upload", "local", "register"}
I18N_DIR = Path(__file__).resolve().parents[1] / "i18n"
_I18N_CACHE: dict[str, dict[str, str]] = {}


@dataclass
class RunLogState:
    log_path: Path
    log_handle: TextIO
    original_stdout: TextIO
    original_stderr: TextIO


@dataclass
class Task:
    id: str
    prompt: str
    dish_name: str
    dish_hint: str
    primary_dimensions: list[str]
    secondary_dimensions: list[str]
    timeout_seconds: int
    rubric: str = ""
    setup: dict[str, Any] = field(default_factory=dict)
    prompt_en: str = ""
    title_en: str = ""
    track: str = "A"
    task_dir: str = ""
    evaluators: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    task_id: str
    dish_name: str
    prompt: str
    response: str
    status: str
    error: str | None
    elapsed_ms: int
    usage: dict[str, int]
    primary_dimensions: list[str]
    secondary_dimensions: list[str]
    rubric: str = ""
    rule_scores: dict[str, int] = field(default_factory=dict)
    ai_scores: dict[str, int] = field(default_factory=dict)
    total_score: int = 0
    reasoning: str = ""
    task_scores: dict[str, int] = field(default_factory=dict)
    transcript: dict[str, Any] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)
    violations: list[str] = field(default_factory=list)
    judge_receipts: list[dict[str, Any]] = field(default_factory=list)
    workdir: str = ""


@dataclass
class Scores:
    lobster_name: str
    total_score: int
    tier: str
    tier_name: str
    tier_emoji: str
    dimensions: dict[str, int]
    task_breakdowns: list[TaskResult]
    summary_comment: str
    lang: str
    timestamp: str
    partial: bool
    judge_model: str
    anonymous: bool
    bundle_version: str = "unknown"
    bundle_hash: str = ""


@dataclass
class SoulProfile:
    name: str
    tags: list[str]
    personality: str


@dataclass
class EnvironmentInfo:
    os_name: str
    gateway_available: bool
    gateway_model: str | None
    soul_path: str | None
    offline_mode: bool

    def render_confirmation(self, soul: SoulProfile, config: dict[str, Any], ask_to_start: bool = True) -> None:
        lang = config.get("lang", "zh")
        estimated_tokens = config.get("estimated_tokens", "15K")
        estimated_minutes = config.get("estimated_minutes", "15-25")
        print(t(lang, "welcome"))
        print(t(lang, "welcome_intro", total_dishes=config.get("expected_task_count", 12)))
        print(t(lang, "detected_lobster", lobster_name=soul.name))
        if soul.tags:
            print(t(lang, "detected_tags", tags=" / ".join(soul.tags[:6])))
        print(t(lang, "current_system", os_name=friendly_os_name(self.os_name)))
        platform_notice = platform_support_notice(self.os_name, lang)
        if platform_notice:
            print(platform_notice)
        if self.gateway_model:
            print(t(lang, "gateway_connected", gateway_model=self.gateway_model))
        if self.soul_path:
            print(t(lang, "soul_found", soul_path=self.soul_path))
        if self.offline_mode:
            print(t(lang, "offline_notice"))
        print(t(lang, "resume_tip"))
        print(t(lang, "menu_ready"))
        print(t(lang, "estimated_cost", estimated_tokens=estimated_tokens, estimated_minutes=estimated_minutes))
        if ask_to_start:
            answer = input(t(lang, "start_prompt")).strip().lower()
            if answer in {"n", "no"}:
                raise SystemExit(0)


class _TeeStream:
    def __init__(self, *streams: TextIO) -> None:
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()

    def isatty(self) -> bool:
        return any(getattr(stream, "isatty", lambda: False)() for stream in self.streams)

    @property
    def encoding(self) -> str:
        return getattr(self.streams[0], "encoding", "utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_config(path: Path) -> dict[str, Any]:
    config = load_json(path)
    config.setdefault("lang", "zh")
    config.setdefault("offline_mode", False)
    config.setdefault("anonymous", False)
    config.setdefault("site_home_url", "https://eval.agent-gigo.com/")
    config.setdefault("share_url_base", "https://eval.agent-gigo.com/r/?ref_code={ref_code}")
    config.setdefault("landing_url", "https://eval.agent-gigo.com/r/?ref_code={ref_code}&source=cert")
    config.setdefault("estimated_tokens", "15K")
    config.setdefault("estimated_minutes", "15-25")
    config.setdefault("expected_task_count", 12)
    config.setdefault("bundle_cache_dir", str(Path.home() / ".cache" / "gigo-lobster-taster" / "bundles"))
    config.setdefault("v2_cost_baseline_tokens", 50000)
    config.setdefault("v2_cost_scale_tokens", 120000)
    config.setdefault("v2_speed_baseline_ms", 300000)
    config.setdefault("v2_speed_scale_ms", 1200000)
    for env_name, config_key in (
        ("GIGO_API_BASE", "api_base"),
        ("GIGO_GATEWAY_BASE", "gateway_base"),
        ("GIGO_REF_REGISTER_TOKEN", "ref_register_token"),
    ):
        value = os.environ.get(env_name, "").strip()
        if value:
            config[config_key] = value
    return config


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def normalize_score(value: float) -> int:
    return max(0, min(100, int(round(value))))


def calculate_v2_speed_score(total_elapsed_ms: int, task_count: int, config: dict[str, Any] | None = None) -> int:
    config = config or {}
    baseline_floor_ms = int(config.get("v2_speed_baseline_ms", 300000))
    scale_floor_ms = int(config.get("v2_speed_scale_ms", 1600000))
    baseline_per_task_ms = int(config.get("v2_speed_baseline_per_task_ms", 45000))
    scale_per_task_ms = int(config.get("v2_speed_scale_per_task_ms", 150000))
    effective_task_count = max(1, int(task_count or 0))
    baseline_ms = max(baseline_floor_ms, baseline_per_task_ms * effective_task_count)
    scale_ms = max(scale_floor_ms, scale_per_task_ms * effective_task_count)
    return normalize_score(clamp(100 - ((int(total_elapsed_ms) - baseline_ms) / max(scale_ms, 1)) * 100, 0, 100))


def load_tier(config: dict[str, Any], total_score: int) -> dict[str, Any]:
    for tier in config["tiers"]:
        if tier["min"] <= total_score <= tier["max"]:
            return tier
    return config["tiers"][-1]


def score_band_comment(score: int, lang: str) -> str:
    zh_pool = {
        "high": "绝了！这只龙虾已经可以上国宴了。",
        "mid": "这只龙虾火候到位，就是偶尔还会脑子短路。",
        "low": "这只龙虾还能吃，但离招牌菜还有点距离。",
        "fail": "这只龙虾建议回炉，再蒸一轮。",
    }
    en_pool = {
        "high": "This lobster is serving at a banquet level.",
        "mid": "Solid lobster, with a few thinking hiccups left to polish.",
        "low": "Edible, but still far from signature-dish quality.",
        "fail": "This lobster needs another round in the kitchen.",
    }
    pool = zh_pool if lang == "zh" else en_pool
    if score >= 80:
        return pool["high"]
    if score >= 60:
        return pool["mid"]
    if score >= 40:
        return pool["low"]
    return pool["fail"]


def progress_bar(completed: int, total: int, width: int = 20) -> str:
    ratio = 0 if total == 0 else completed / total
    filled = math.floor(width * ratio)
    return "█" * filled + "░" * (width - filled)


def checkpoint_path(output_dir: Path) -> Path:
    return output_dir / DEFAULT_CHECKPOINT_NAME


def detect_openclaw_workspace_root(repo_root: Path) -> Path | None:
    env_candidates = [
        os.environ.get("OPENCLAW_WORKSPACE_DIR"),
        os.environ.get("OPENCLAW_WORKSPACE"),
    ]
    for candidate in env_candidates:
        if not candidate:
            continue
        candidate_path = Path(candidate).expanduser()
        if candidate_path.exists():
            return candidate_path.resolve()

    if repo_root.parent.name == "skills" and repo_root.parent.parent.name == "workspace":
        return repo_root.parent.parent

    return None


def resolve_output_dir(repo_root: Path, requested_output_dir: str) -> Path:
    output_dir = Path(requested_output_dir).expanduser()
    if output_dir.is_absolute():
        return output_dir

    if requested_output_dir == DEFAULT_OUTPUT_DIRNAME:
        workspace_root = detect_openclaw_workspace_root(repo_root)
        if workspace_root:
            return workspace_root / "outputs" / repo_root.name

    return repo_root / output_dir


def prepare_output_dir_for_run(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for artifact_name in RUN_ARTIFACT_NAMES:
        artifact_path = output_dir / artifact_name
        if not artifact_path.exists():
            continue
        archived_path = output_dir / f"{artifact_path.stem}.prev-{stamp}{artifact_path.suffix}"
        suffix_index = 1
        while archived_path.exists():
            archived_path = output_dir / f"{artifact_path.stem}.prev-{stamp}-{suffix_index}{artifact_path.suffix}"
            suffix_index += 1
        artifact_path.replace(archived_path)


def setup_run_logging(output_dir: Path) -> RunLogState:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "gigo-run.log"
    log_handle = log_path.open("w", encoding="utf-8", buffering=1)
    state = RunLogState(
        log_path=log_path,
        log_handle=log_handle,
        original_stdout=sys.stdout,
        original_stderr=sys.stderr,
    )
    sys.stdout = _TeeStream(state.original_stdout, log_handle)  # type: ignore[assignment]
    sys.stderr = _TeeStream(state.original_stderr, log_handle)  # type: ignore[assignment]
    return state


def restore_run_logging(state: RunLogState | None) -> None:
    if not state:
        return
    sys.stdout = state.original_stdout
    sys.stderr = state.original_stderr
    state.log_handle.close()


def _load_i18n(lang: str) -> dict[str, str]:
    normalized = lang if (I18N_DIR / f"{lang}.json").exists() else "zh"
    if normalized not in _I18N_CACHE:
        _I18N_CACHE[normalized] = load_json(I18N_DIR / f"{normalized}.json")
    return _I18N_CACHE[normalized]


def t(lang: str, key: str, **kwargs: Any) -> str:
    payload = _load_i18n(lang)
    value = payload.get(key)
    if value is None and lang != "zh":
        value = _load_i18n("zh").get(key, key)
    elif value is None:
        value = key
    return value.format(**kwargs)


def friendly_os_name(os_name: str) -> str:
    mapping = {
        "darwin": "macOS",
        "linux": "Linux",
        "windows": "Windows",
    }
    return mapping.get(os_name, os_name or "Unknown")


def platform_support_notice(os_name: str, lang: str = "zh") -> str | None:
    if os_name == "windows":
        if lang == "zh":
            return "⚠️ Windows 也可以直接运行；如果你第一次联调，仍建议优先使用 WSL。"
        return "⚠️ Windows is supported too. For the first round of integration, WSL is still recommended."
    if os_name in SUPPORTED_SKILL_OSES:
        return None
    if lang == "zh":
        return f"⚠️ 当前系统 {friendly_os_name(os_name)} 尚未完成官方验证，若遇到问题建议切换到 macOS 或 Linux。"
    return f"⚠️ {friendly_os_name(os_name)} has not been officially validated yet. If you hit issues, try macOS or Linux."


def open_command_for_path(os_name: str, path: Path) -> str:
    resolved = str(path.resolve())
    if os_name == "darwin":
        return f'open "{resolved}"'
    if os_name == "windows":
        return f'start "" "{resolved}"'
    return f'xdg-open "{resolved}"'


def describe_bundle_source(source: str, lang: str) -> str:
    zh_map = {
        "remote": "云端正式题包",
        "remote_session": "云端正式题包",
        "offline_fallback": "离线 demo 包",
        "embedded_fallback": "本地 demo 回退包",
        "cache_fallback": "本地缓存题包",
        "cache_304": "本地缓存题包",
        "embedded_author_bundle": "本地 author v2 题包",
        "embedded_public_bundle": "内置正式题包副本",
        "remote_archive": "云端 public v2 题包",
    }
    en_map = {
        "remote": "remote official bundle",
        "remote_session": "remote official bundle",
        "offline_fallback": "offline demo bundle",
        "embedded_fallback": "local demo fallback bundle",
        "cache_fallback": "cached task bundle",
        "cache_304": "cached task bundle",
        "embedded_author_bundle": "embedded author v2 bundle",
        "embedded_public_bundle": "bundled official task copy",
        "remote_archive": "remote public v2 bundle",
    }
    mapping = zh_map if lang == "zh" else en_map
    return mapping.get(source, source)


def resolve_default_lang(non_interactive: bool, explicit_lang: str | None = None) -> str:
    if explicit_lang in VALID_LANGS:
        return explicit_lang

    selected_lang = (os.environ.get("GIGO_SELECTED_LANG") or "").strip().lower()
    if selected_lang in VALID_LANGS:
        return selected_lang

    configured_lang = (os.environ.get("GIGO_DEFAULT_LANG") or "").strip().lower()
    if configured_lang in VALID_LANGS:
        return configured_lang

    for locale_key in ("LC_ALL", "LC_MESSAGES", "LANG"):
        locale_value = (os.environ.get(locale_key) or "").strip().lower()
        if locale_value.startswith("zh"):
            return "zh"
        if locale_value.startswith("en"):
            return "en"

    return "en" if non_interactive else "zh"


def resolve_upload_mode(non_interactive: bool, explicit_mode: str | None = None) -> str:
    if explicit_mode in VALID_UPLOAD_MODES:
        return explicit_mode

    configured_mode = (os.environ.get("GIGO_UPLOAD_MODE") or "").strip().lower()
    if configured_mode in VALID_UPLOAD_MODES:
        return configured_mode

    return "upload"


def check_environment(config: dict[str, Any], repo_root: Path) -> EnvironmentInfo:
    gateway_available = bool(config.get("offline_mode", False) or os.environ.get("GIGO_GATEWAY_MOCK") == "1")
    gateway_model = "mock-lobster" if gateway_available else None

    if not gateway_available:
        try:
            from .gateway_client import GatewayClient

            gateway = GatewayClient(config["gateway_base"])
            gateway_available = gateway.check_availability()
            if gateway_available:
                gateway_model = gateway.check_lobster().get("id")
        except Exception:
            gateway_available = False

    soul_path = None
    try:
        from .soul_parser import find_soul_md_path

        detected = find_soul_md_path(repo_root)
        if detected:
            soul_path = str(detected)
    except Exception:
        soul_path = None

    return EnvironmentInfo(
        os_name=platform.system().lower(),
        gateway_available=gateway_available,
        gateway_model=gateway_model,
        soul_path=soul_path,
        offline_mode=bool(config.get("offline_mode", False)),
    )


def prompt_upload_choice(lang: str) -> bool:
    answer = input(t(lang, "upload_prompt")).strip().lower()
    return answer not in {"n", "no"}


def prompt_language_choice(default: str = "zh") -> str:
    answer = input(f"请选择语言 / Choose language [zh/en] (default: {default}): ").strip().lower()
    if answer in {"en", "english"}:
        return "en"
    if answer in {"zh", "cn", "chinese", "中文"}:
        return "zh"
    return default


def _parse_tag_input(raw: str) -> list[str]:
    normalized = raw
    for separator in ("，", "、", "/", "|", ";", "；"):
        normalized = normalized.replace(separator, ",")
    tags: list[str] = []
    seen: set[str] = set()
    for item in normalized.split(","):
        cleaned = item.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        tags.append(cleaned)
    return tags


def apply_host_profile_overrides(
    soul: SoulProfile,
    *,
    name_override: str | None = None,
    tags_override: str | list[str] | None = None,
) -> SoulProfile:
    resolved_name = (name_override or os.environ.get("GIGO_LOBSTER_NAME") or "").strip()
    if isinstance(tags_override, list):
        resolved_tags = [tag.strip() for tag in tags_override if tag and tag.strip()]
    else:
        resolved_tags = _parse_tag_input(tags_override or os.environ.get("GIGO_LOBSTER_TAGS") or "")
    if not resolved_name and not resolved_tags:
        return soul
    return SoulProfile(
        name=resolved_name or soul.name,
        tags=resolved_tags or soul.tags or ["adaptive"],
        personality=soul.personality,
    )


def prompt_lobster_profile(lang: str, soul: SoulProfile, soul_path: str | None = None) -> SoulProfile:
    tags = list(soul.tags or [])
    if soul_path:
        print(t(lang, "identity_source_soul", soul_path=soul_path))
        if tags:
            print(t(lang, "identity_tags_detected", tags=" / ".join(tags[:6])))
        name_answer = input(t(lang, "identity_name_override_prompt", lobster_name=soul.name)).strip()
        return SoulProfile(
            name=name_answer or soul.name,
            tags=tags or ["adaptive"],
            personality=soul.personality,
        )

    print(t(lang, "identity_source_manual"))
    name_answer = input(t(lang, "identity_name_prompt", default_name=soul.name)).strip()
    tags_answer = input(t(lang, "identity_tags_prompt")).strip()
    manual_tags = _parse_tag_input(tags_answer)
    return SoulProfile(
        name=name_answer or soul.name,
        tags=manual_tags or tags or ["adaptive"],
        personality=soul.personality,
    )


def prompt_resume_choice(lang: str, completed: int, total: int) -> bool:
    answer = input(t(lang, "resume_prompt", completed=completed, total=total)).strip().lower()
    return answer not in {"n", "no"}


def print_summary(
    scores: Scores,
    report_path: Path,
    cert_path: Path,
    upload_result: dict[str, Any] | None,
    os_name: str | None = None,
) -> None:
    lang = scores.lang
    dims = " | ".join(f"{key} {value}" for key, value in scores.dimensions.items())
    print(t(lang, "summary_title"))
    print(t(lang, "summary_headline", lobster_name=scores.lobster_name, tier_name=scores.tier_name, total_score=scores.total_score))
    print(t(lang, "summary_dimensions", dims=dims))
    if scores.partial:
        print(t(lang, "summary_partial"))
    print(t(lang, "summary_report", report_path=report_path))
    print(t(lang, "summary_cert", cert_path=cert_path))
    if os_name:
        print(t(lang, "summary_open_report", command=open_command_for_path(os_name, report_path)))
        print(t(lang, "summary_open_cert", command=open_command_for_path(os_name, cert_path)))
    if upload_result and upload_result.get("success"):
        print(t(lang, "summary_cloud_success", cloud_payload=json.dumps(upload_result, ensure_ascii=False)))
        print(t(lang, "summary_next_share"))
    elif upload_result and not upload_result.get("success", False):
        print(t(lang, "summary_cloud_failure", cloud_payload=json.dumps(upload_result, ensure_ascii=False)))
        print(t(lang, "summary_next_local"))
    else:
        print(t(lang, "summary_next_local"))
    print(t(lang, "summary_comment", comment=scores.summary_comment))
