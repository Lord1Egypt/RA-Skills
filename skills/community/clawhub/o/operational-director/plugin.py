"""Ouroboros extension surface carried inside the dual-mode ClawHub skill."""

from __future__ import annotations

import json
from typing import Any

from .scripts.get_data import build_snapshot


RESPONSE_GUIDANCE = """
Ответить на точный вопрос пользователя только по подтверждённым данным снимка.
Для общего вопроса дать компактную управленческую сводку: главные выводы,
ровно один приоритет №1, деньги, риски и ближайшие обязательства; пустые блоки
пропустить. Для короткого запроса дать три главных факта и приоритет №1.
Для конкретного вопроса не пересказывать весь снимок. Не придумывать факты,
динамику, пороги и причинные связи. Недоступное банковское действие не выполнять.
Указать дату состояния. После фактов перечислить источники отдельно по каждой
использованной теме, не смешивая get_data API (ИФТ) и mock. Предложить до трёх
пронумерованных продолжений и закончить фразой:
P.S. ИФТ — тестовый контур, а mock — искусственные демо-данные. Это не данные
реальной компании.
""".strip()


SUMMARY_TOPICS = (
    ("Доступные остатки", "Деньги"),
    ("Остаток после ближайших обязательств", "Резерв после обязательств"),
    ("Ограничения на счёте", "Приоритет №1"),
    ("Платёж ждёт подписи", "Платёж"),
    ("Доверенность представителя не продлена", "Доверенность"),
    ("Налоговые сроки", "Налоги"),
    ("Единый налоговый счёт", "ЕНС"),
)


def _sections_by_topic(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(section.get("topic") or ""): section
        for section in snapshot.get("sections") or []
        if isinstance(section, dict)
    }


def _first_paragraph(value: Any) -> str:
    return str(value or "").strip().split("\n\n", 1)[0]


def _source_label(source: Any) -> str:
    return (
        "get_data API (ИФТ), данные тестового контура"
        if str(source or "").strip().lower() == "ift"
        else "mock, искусственные демо-данные"
    )


def build_management_summary(snapshot: dict[str, Any]) -> str:
    """Build a deterministic zero-token overview for the extension widget."""

    sections = _sections_by_topic(snapshot)
    chosen: list[tuple[str, str, dict[str, Any]]] = []
    for topic, label in SUMMARY_TOPICS:
        section = sections.get(topic)
        if section and section.get("facts"):
            chosen.append((topic, label, section))

    if not chosen:
        return (
            "# Сводка бизнеса\n\n"
            "Не могу построить сводку: в локальном снимке нет доступных разделов."
        )

    lines = [
        "# Сводка бизнеса",
        "",
        f"Состояние на {snapshot.get('as_of') or 'дату снимка'}.",
        "",
    ]
    for _topic, label, section in chosen:
        lines.extend((f"## {label}", "", _first_paragraph(section.get("facts")), ""))

    lines.extend(("## Источники данных", ""))
    for topic, _label, section in chosen:
        lines.append(f"- Информация о «{topic}» — {_source_label(section.get('source'))}.")
    lines.extend(
        (
            "",
            "P.S. ИФТ — тестовый контур, а mock — искусственные демо-данные. "
            "Это не данные реальной компании.",
        )
    )
    return "\n".join(lines)


def get_business_snapshot(ctx: Any, question: str) -> str:
    """Return the current read-only business snapshot for the user's question."""

    del ctx
    exact_question = str(question or "").strip()
    if not exact_question:
        return json.dumps(
            {"ok": False, "reason": "Не передан вопрос пользователя."},
            ensure_ascii=False,
        )

    try:
        snapshot = build_snapshot()
    except RuntimeError as exc:
        return json.dumps({"ok": False, "reason": str(exc)}, ensure_ascii=False)

    return json.dumps(
        {
            **snapshot,
            "question": exact_question,
            "response_guidance": RESPONSE_GUIDANCE,
        },
        ensure_ascii=False,
    )


def get_management_summary(_request: Any) -> dict[str, Any]:
    """Return a directly rendered business overview without an LLM call."""

    try:
        snapshot = build_snapshot()
    except RuntimeError as exc:
        return {
            "ok": False,
            "summary": "# Сводка бизнеса\n\nЛокальный снимок временно недоступен.",
            "error": str(exc),
        }
    return {
        "ok": True,
        "as_of": snapshot.get("as_of"),
        "summary": build_management_summary(snapshot),
    }


def register(api: Any) -> None:
    """Register the chat tool and the zero-token business-summary widget."""

    api.register_tool(
        "get_business_snapshot",
        get_business_snapshot,
        description=(
            "Получить свежие локальные данные бизнеса без API-ключей для "
            "управленческой сводки или ответа о счетах, остатках, оборотах, "
            "платежах, ограничениях, налогах, документах, доверенностях, "
            "картах, наличных, QR, тарифах, ликвидности, рисках и действиях "
            "на сегодня. Вызывать также для ответов 1, 2 или 3."
        ),
        schema={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Точное сообщение пользователя без перефразирования.",
                }
            },
            "required": ["question"],
            "additionalProperties": False,
        },
        timeout_sec=60,
    )
    api.register_route("summary", get_management_summary, methods=("POST",))
    api.register_ui_tab(
        "business",
        "Сводка бизнеса",
        icon="briefcase",
        render={
            "kind": "declarative",
            "schema_version": 1,
            "components": [
                {
                    "type": "markdown",
                    "text": (
                        "Получите свежую локальную сводку без обращения к модели "
                        "и без расхода токенов."
                    ),
                },
                {
                    "type": "action",
                    "route": "summary",
                    "method": "POST",
                    "label": "Обновить сводку",
                    "busy_label": "Собираю данные…",
                    "target": "result",
                },
                {"type": "markdown", "target": "result", "path": "summary"},
            ],
        },
    )
