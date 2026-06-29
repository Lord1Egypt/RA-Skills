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


def field(name: str, label: str, placeholder: str = "", required: bool = True, multiline: bool = False) -> dict[str, Any]:
    return {
        "name": name,
        "label": label,
        "placeholder": placeholder,
        "required": required,
        "multiline": multiline,
    }


def card(
    card_id: str,
    title: str,
    summary: str,
    actions: list[dict[str, Any]] | None = None,
    fields: list[dict[str, Any]] | None = None,
    hidden: dict[str, Any] | None = None,
    submit_action: str = "",
) -> dict[str, Any]:
    return {
        "type": "feishu_interactive_card",
        "version": CARD_VERSION,
        "card_id": card_id,
        "title": title,
        "summary": summary,
        "fallback_text": summary,
        "fields": fields or [],
        "actions": actions or [],
        "hidden": hidden or {},
        "submit_action": submit_action,
        "callback_contract": {
            "action_value_field": "CardActionValue",
            "form_values_field": "CardFormValues",
            "hidden_fields_included": True,
        },
    }


def registration_form(gitea_url: str) -> dict[str, Any]:
    return card(
        "init.registration.form",
        "创建个人知识库",
        f"第一次使用需要先在 Gitea 注册账号，然后填写个人初始化信息。Gitea 地址：{gitea_url}",
        fields=[
            field("gitea_username", "Gitea 用户名", "例如 mayidan"),
            field("name", "姓名", "例如 张三"),
            field("research_direction", "研究方向", "例如 多智能体科研知识管理", multiline=True),
        ],
        actions=[option("提交初始化", "register_user", "创建个人知识库", "primary")],
        hidden={"gitea_url": gitea_url},
        submit_action="register_user",
    )


def post_init_choice(open_id: str, personal_repo_url: str = "") -> dict[str, Any]:
    summary = "个人知识库已创建。请选择下一步。"
    if personal_repo_url:
        summary += f" 知识库：{personal_repo_url}"
    return card(
        "init.post_init.choice",
        "下一步",
        summary,
        actions=[
            option("加入已有团队", "join_team", "需要团队名称和邀请码", "primary"),
            option("创建新团队", "create_team", "需要团队名称和研究方向", "primary"),
            option("暂时单独使用", "personal_only", "以后仍可加入或创建团队"),
        ],
        hidden={"open_id": open_id},
    )


def join_team_form(open_id: str) -> dict[str, Any]:
    return card(
        "init.join_team.form",
        "加入已有团队",
        "请填写团队名称和邀请码。",
        fields=[
            field("team_name", "团队名称", "请输入完整团队名称"),
            field("invite_code", "邀请码", "请输入团队邀请码"),
        ],
        actions=[option("提交加入申请", "submit_join_team", "验证邀请码并加入团队", "primary")],
        hidden={"open_id": open_id},
        submit_action="submit_join_team",
    )


def create_team_form(open_id: str) -> dict[str, Any]:
    return card(
        "init.create_team.form",
        "创建新团队",
        "请填写团队名称和团队研究方向。团队知识库仓库名会基于团队名称生成。",
        fields=[
            field("team_name", "团队名称", "例如 AIFusion Lab"),
            field("research_direction", "团队研究方向", "例如 科研团队知识自动化", multiline=True),
        ],
        actions=[option("创建团队", "submit_create_team", "创建团队知识库并写入邀请码", "primary")],
        hidden={"open_id": open_id},
        submit_action="submit_create_team",
    )


def bind_confirm(action: str, confirm_code: str, team_name: str, chat_name: str, ttl_minutes: int) -> dict[str, Any]:
    is_bind = action == "bind"
    title = "确认绑定团队群" if is_bind else "确认解除群绑定"
    verb = "绑定" if is_bind else "解绑"
    return card(
        f"init.group_{action}.confirm",
        title,
        f"将对群聊「{chat_name}」执行{verb}操作，目标团队：{team_name}。确认码 {confirm_code}，{ttl_minutes} 分钟内有效。",
        actions=[
            option(f"确认{verb}", f"confirm_{action}:{confirm_code}", "只有团队管理员可以确认", "danger" if not is_bind else "primary"),
            option("取消", f"cancel_{action}:{confirm_code}", "不执行操作"),
        ],
        hidden={"confirm_code": confirm_code, "action": action},
    )
