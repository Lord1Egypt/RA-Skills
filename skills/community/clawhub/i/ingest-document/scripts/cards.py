from __future__ import annotations

from typing import Any


CARD_VERSION = "paper-kb-card-v1"


def option(label: str, value: str, description: str = "", style: str = "default") -> dict[str, Any]:
    return {
        "label": label,
        "value": value,
        "description": description,
        "style": style,
    }


def card(
    card_id: str,
    title: str,
    summary: str,
    actions: list[dict[str, Any]] | None = None,
    hidden: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "type": "feishu_interactive_card",
        "version": CARD_VERSION,
        "card_id": card_id,
        "title": title,
        "summary": summary,
        "fallback_text": summary,
        "actions": actions or [],
        "hidden": hidden or {},
        "callback_contract": {
            "action_value_field": "CardActionValue",
            "form_values_field": "CardFormValues",
            "hidden_fields_included": True,
        },
    }


def target_confirm(reason: str, has_team: bool) -> dict[str, Any]:
    actions = [option("存入个人知识库", "ingest_target:personal", "作为个人资料保存", "primary")]
    if has_team:
        actions.append(option("存入团队知识库", "ingest_target:team", "作为团队资料保存", "primary"))
        actions.append(option("个人和团队都存", "ingest_target:both", "双写两边知识库"))
    return card(
        "ingest.target.confirm",
        "确认入库位置",
        reason or "请确认这条资料要保存到哪里。",
        actions=actions,
    )


def duplicate_confirm(title: str, existing: dict[str, Any], possible: bool = False) -> dict[str, Any]:
    existing_title = existing.get("title") or existing.get("name") or "已有资料"
    relation = "疑似重复" if possible else "重复"
    return card(
        "ingest.duplicate.confirm",
        "确认重复资料处理方式",
        f"「{title}」与「{existing_title}」{relation}。请选择处理方式。",
        actions=[
            option("覆盖已有资料", "duplicate:overwrite", "用新内容更新旧页面", "danger"),
            option("继续保存为新资料", "duplicate:save_new", "保留两个页面"),
            option("取消保存", "duplicate:cancel", "不写入知识库"),
        ],
        hidden={"existing_path": existing.get("file", ""), "title": title},
    )
