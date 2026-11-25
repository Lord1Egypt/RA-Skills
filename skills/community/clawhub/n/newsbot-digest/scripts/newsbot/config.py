"""Общая конфигурация запуска: пути, ключи, логгер, LLM-клиенты, статус."""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv
from loguru import logger

SKILL_DIR = Path(__file__).resolve().parents[2]
PROMPTS_DIR = SKILL_DIR / "prompts"


def read_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


@dataclass
class RunContext:
    """Все пути одного запуска. История (прошлые выборки) живёт в workdir."""

    workdir: Path
    output_root: Path
    headless: object = True
    now: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.date = self.now.strftime("%Y-%m-%d")
        self.ts = self.now.strftime("%Y-%m-%d %H-%M")

        # --- состояние / история (персистентно между запусками) ---
        self.tg_dir = self.workdir / "tg_posts"
        self.google_dir = self.workdir / "google_news"
        self.claude_dir = self.workdir / "claude_news"
        self.collection_dir = self.workdir / "collection"
        self.selected_dir = self.workdir / "selected"
        self.logs_dir = self.workdir / "logs"
        self.en_dir = self.workdir / "translation" / "en" / self.date
        self.ru_dir = self.workdir / "translation" / "ru" / self.date

        # --- результат запуска (то, что отдаётся пользователю) ---
        self.out_dir = self.output_root / self.date
        self.pdf_dir = self.out_dir / "pdf"

        for d in (self.tg_dir, self.google_dir, self.claude_dir, self.collection_dir,
                  self.selected_dir, self.logs_dir, self.en_dir, self.ru_dir,
                  self.out_dir, self.pdf_dir):
            d.mkdir(parents=True, exist_ok=True)

        # файлы текущего запуска
        self.tg_csv = self.tg_dir / f"{self.ts}.csv"
        self.google_csv = self.google_dir / f"{self.ts}.csv"
        self.claude_xlsx: Optional[Path] = None
        self.collection_xlsx = self.collection_dir / f"collection-{self.date}.xlsx"
        self.selected_xlsx = self.selected_dir / f"{self.ts}.xlsx"
        self.status_json = self.out_dir / "status.json"
        self.result_json = self.out_dir / "result.json"
        self.digest_md = self.out_dir / "digest.md"

    # ---- история ----
    def previous_collection(self) -> Optional[Path]:
        files = sorted(p for p in self.collection_dir.glob("*.xlsx")
                       if p.name < self.collection_xlsx.name)
        return files[-1] if files else None

    def previous_selected(self, n: int) -> list[Path]:
        files = sorted(p for p in self.selected_dir.glob("*.xlsx")
                       if p.name < self.selected_xlsx.name)
        return list(reversed(files))[:n]


CTX: Optional[RunContext] = None


def set_ctx(ctx: RunContext) -> None:
    global CTX
    CTX = ctx


def ctx() -> RunContext:
    if CTX is None:
        raise RuntimeError("RunContext не инициализирован")
    return CTX


# ---------------- статус для агента ----------------
_STATUS: dict = {"stages": []}


def status(stage: str, state: Literal["start", "ok", "error", "skip"], detail: str = "") -> None:
    """Пишет прогресс в status.json и в лог, чтобы агент мог отслеживать долгий запуск."""
    msg = f"[{stage}] {state}" + (f": {detail}" if detail else "")
    (logger.error if state == "error" else logger.info)(msg)
    _STATUS["stages"].append({"time": datetime.now().strftime("%H:%M:%S"),
                              "stage": stage, "state": state, "detail": detail})
    _STATUS["current"] = stage
    _STATUS["done"] = stage == "finish" and state in ("ok", "error")
    try:
        ctx().status_json.write_text(json.dumps(_STATUS, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


# ---------------- окружение и логгер ----------------
def load_env(extra_env: Optional[Path], workdir: Path) -> None:
    for p in (extra_env, workdir / ".env", SKILL_DIR / ".env", Path.cwd() / ".env"):
        if p and Path(p).is_file():
            load_dotenv(p, override=False)


def setup_logger(c: RunContext) -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO",
               format="<green>{time:HH:mm:ss}</green> | {level} | {message}")
    logger.add(c.logs_dir / f"{c.date}.log", level="DEBUG",
               format="{time:YYYY-MM-DD HH:mm:ss} - {level}\n{message}\n" + "=" * 80 + "\n")


# ---------------- LLM ----------------
LLMConfig = Literal["cloud", "deepseek"]


def get_llm(config: LLMConfig = "cloud"):
    """cloud = Claude Sonnet через cloud.ru (OpenAI-совместимый API); deepseek = резерв."""
    from langchain_deepseek import ChatDeepSeek

    cloud_key = os.getenv("CLOUD_API")
    deepseek_key = os.getenv("API_DEEPSEEK")
    if config == "cloud" and not cloud_key:
        config = "deepseek"
    if config == "deepseek" and not deepseek_key:
        if cloud_key:
            config = "cloud"
        else:
            raise RuntimeError("Не задан ни CLOUD_API, ни API_DEEPSEEK")

    if config == "cloud":
        return ChatDeepSeek(
            model=os.getenv("CLOUD_MODEL", "anthropic/claude-sonnet-4.6"),
            api_key=cloud_key,
            api_base=os.getenv("CLOUD_API_BASE", "https://foundation-models.api.cloud.ru/v1"),
            temperature=0.5,
            streaming=True,
        )
    return ChatDeepSeek(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro"),
        api_key=deepseek_key,
        temperature=0.5,
    )
