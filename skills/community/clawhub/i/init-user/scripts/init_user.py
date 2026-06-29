# -*- coding: utf-8 -*-
"""
init_user.py — paper-kb Skill 1：用户初始化

三种模式（由 OpenClaw 按 SKILL.md 指引调用）：

1. 查询用户是否已注册：
   python3 init_user.py --check --open_id ou_xxx

2. 注册新用户（创建仓库 + 写映射表）：
   python3 init_user.py --register --open_id ou_xxx \
       --gitea_username mayidan --research_direction "强化学习控制算法"

3. 回填飞书表格信息（OpenClaw 创建表格成功后调用）：
   python3 init_user.py --update-feishu --open_id ou_xxx \
       --feishu_app_token bascnXXX --feishu_table_id tblXXX

所有模式输出单行 JSON 到 stdout，OpenClaw 读取后决定下一步。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta

import gitea_api as g
import doc_types as dt

REPO_NAME = "paper-kb"

# 北京时间
_TZ = timezone(timedelta(hours=8))


def _now() -> str:
    return datetime.now(_TZ).strftime("%Y-%m-%d %H:%M:%S")


def _out(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def _fail(error: str, message: str) -> None:
    _out({"success": False, "error": error, "message": message})
    sys.exit(0)  # 正常退出，让 OpenClaw 读到 JSON 而不是崩溃信息


# ---------------------------------------------------------------- 初始文件内容

def _index_seed(research_direction: str) -> str:
    return f"""# 知识库索引

## 研究方向
{research_direction}

## 文档

## 概念

## 科研资源
"""


_AGENTS_SEED = """# Wiki Schema（paper-kb 知识库结构说明）

本文件定义知识库的目录结构与页面规范。AI 在生成和维护知识库内容时必须遵守。

## 目录结构
- summaries/ — 文档摘要，按资料类型分六个子文件夹：
  - summaries/papers/      论文
  - summaries/surveys/     行业调研
  - summaries/projects/    开源项目
  - summaries/docs_tech/   技术文档
  - summaries/experiments/ 实验记录
  - summaries/meetings/    会议纪要
- concepts/ — 跨文档概念综合页。当一个主题出现在多篇文档中时创建。
- resources/ — 科研资源页：数据集、开源项目、工具、硬件等可复用资源。
- pdfs/ — 原始文件存档（PDF/Word 等）。
- index.md — 知识库索引：所有页面的目录，由代码自动维护，AI 不要手动修改。

## 页面类型
- **摘要页（summaries/）**：单篇文档的关键内容。含 frontmatter 元数据
  （标题、类型、来源、关键词、相关性评分、存入时间）。
- **概念页（concepts/）**：抽象的、反复出现的方法/思想/机制
  （如"力控制"、"强化学习"）。跨文档综合，含不同文档的论述对比。
- **资源页（resources/）**：具体的、有名字的科研资源
  （如"DexYCB 数据集"、"PyBullet"、"GelSight 传感器"）。
  记录该资源在哪些文档中被使用、效果如何、获取方式。

## 概念 vs 资源 的区分
- 概念 = 抽象想法（力控制、模仿学习）
- 资源 = 具体事物（某个数据集、某个开源库、某款传感器）
- 一个名字只归入一类，两类页面之间可以互相链接。

## 链接格式
- 用 [[wikilink]] 链接其他页面，例如 [[concepts/力控制]]、[[summaries/某论文标题]]。
- 只链接实际存在的页面，不要发明不存在的链接目标。

## 内容规范
- 全部使用中文。
- 标准 Markdown 标题层级。
- 每个页面聚焦单一主题。
"""


def _readme_seed(gitea_username: str, research_direction: str) -> str:
    return f"""# {gitea_username} 的科研知识库（paper-kb）

研究方向：{research_direction}

本仓库由 paper-kb 系统自动维护。在飞书里发送 arxiv 链接或上传 PDF 即可入库，
用自然语言提问即可查询。

## 目录说明
- `index.md` — 知识库总目录
- `summaries/` — 每篇文档的结构化摘要
- `concepts/` — 跨文档概念综合
- `resources/` — 数据集 / 开源项目 / 工具等科研资源
- `pdfs/` — 原始 PDF 存档
"""


# ---------------------------------------------------------------- 三种模式

def do_check(open_id: str) -> None:
    users = g.read_users()
    info = users.get(open_id)
    if info:
        _out({
            "success": True,
            "registered": True,
            "user": info,
            "repo_url": f"{g.GITEA_URL}/{info['gitea_username']}/{REPO_NAME}",
        })
    else:
        _out({"success": True, "registered": False})


def do_register(open_id: str, gitea_username: str, research_direction: str,
                feishu_app_token: str, feishu_table_id: str) -> None:
    # 0. 前置检测：token 必须是站点管理员
    if not g.token_is_site_admin():
        _fail(
            "not_admin",
            "当前 GITEA_ADMIN_TOKEN 对应的账号不是 Gitea 站点管理员，无法为用户创建仓库。"
            "请用管理员账号登录 Gitea → 管理后台 → 用户管理 → 将机器人账号设为管理员，"
            "或更换为管理员账号的 token。",
        )

    # 1. 自举 system-config
    g.ensure_system_repo()
    users = g.read_users()

    # 2. open_id 已注册 → 幂等返回
    if open_id in users:
        info = users[open_id]
        _out({
            "success": True,
            "already_registered": True,
            "user": info,
            "repo_url": f"{g.GITEA_URL}/{info['gitea_username']}/{REPO_NAME}",
            "message": "该飞书用户已注册过，无需重复初始化。",
        })
        return

    # 3. gitea_username 已被其他 open_id 绑定 → 拒绝
    for oid, info in users.items():
        if info.get("gitea_username") == gitea_username:
            _fail(
                "username_taken",
                f"Gitea 账号 {gitea_username} 已被另一位飞书用户绑定。"
                "每个 Gitea 账号只能绑定一个飞书用户，请确认用户名是否正确。",
            )

    # 4. 验证 Gitea 账号存在
    gitea_user = g.get_user(gitea_username)
    if gitea_user is None:
        _fail(
            "gitea_user_not_found",
            f"Gitea 上找不到用户 {gitea_username}。"
            f"请先在 {g.GITEA_URL} 注册账号，然后重新发送用户名。",
        )
    canonical = gitea_user.get("login", gitea_username)

    # 5. 创建私有仓库（已存在则复用）
    repo = g.create_repo_for_user(
        canonical, REPO_NAME,
        description=f"科研知识库 | 研究方向：{research_direction}",
    )

    # 6. 补齐初始文件（已存在的不覆盖）
    seeded = []
    for path, content in [
        ("README.md", _readme_seed(canonical, research_direction)),
        ("index.md", _index_seed(research_direction)),
        ("AGENTS.md", _AGENTS_SEED),
        ("concepts/.gitkeep", ""),
        ("resources/.gitkeep", ""),
        ("pdfs/.gitkeep", ""),
    ] + [
        (f"summaries/{folder}/.gitkeep", "")
        for folder in dt.all_summary_folders()
    ]:
        try:
            if g.ensure_file(canonical, REPO_NAME, path, content,
                             f"paper-kb init: {path}"):
                seeded.append(path)
        except g.GiteaError as exc:
            _fail("seed_file_failed", f"初始化文件 {path} 失败：{exc}")

    # 7. 写入映射表（并发安全）
    record = {
        "gitea_username": canonical,
        "research_direction": research_direction,
        "feishu_app_token": feishu_app_token or "",
        "feishu_table_id": feishu_table_id or "",
        "created_at": _now(),
    }

    def mutate(u: dict) -> dict:
        u[open_id] = record
        return u

    g.write_users(mutate)

    _out({
        "success": True,
        "already_registered": False,
        "user": record,
        "repo_created": repo["created"],
        "repo_url": repo["html_url"],
        "seeded_files": seeded,
        "feishu_table_pending": not (feishu_app_token and feishu_table_id),
        "message": "初始化完成。",
    })


def do_update_feishu(open_id: str, feishu_app_token: str,
                     feishu_table_id: str) -> None:
    users = g.read_users()
    if open_id not in users:
        _fail("user_not_found", "该 open_id 尚未注册，无法回填飞书表格信息。")

    def mutate(u: dict) -> dict:
        if open_id in u:
            u[open_id]["feishu_app_token"] = feishu_app_token
            u[open_id]["feishu_table_id"] = feishu_table_id
        return u

    g.write_users(mutate)
    _out({
        "success": True,
        "message": "飞书表格信息已写入用户记录。",
        "feishu_app_token": feishu_app_token,
        "feishu_table_id": feishu_table_id,
    })


# ---------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(description="paper-kb 用户初始化")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="查询用户是否已注册")
    mode.add_argument("--register", action="store_true", help="注册新用户")
    mode.add_argument("--update-feishu", action="store_true",
                      help="回填飞书表格信息")

    parser.add_argument("--open_id", required=True, help="当前飞书用户的 open_id")
    parser.add_argument("--gitea_username", default="", help="Gitea 用户名")
    parser.add_argument("--research_direction", default="", help="研究方向")
    parser.add_argument("--feishu_app_token", default="", help="飞书多维表格 app_token")
    parser.add_argument("--feishu_table_id", default="", help="飞书数据表 table_id")
    args = parser.parse_args()

    if not g.ADMIN_TOKEN:
        _fail("missing_token",
              "未配置 GITEA_ADMIN_TOKEN。请在 skill 根目录的 .env 文件中设置。")

    try:
        if args.check:
            do_check(args.open_id)
        elif args.register:
            if not args.gitea_username:
                _fail("missing_arg", "注册模式必须提供 --gitea_username")
            if not args.research_direction:
                _fail("missing_arg", "注册模式必须提供 --research_direction")
            do_register(args.open_id, args.gitea_username.strip(),
                        args.research_direction.strip(),
                        args.feishu_app_token.strip(),
                        args.feishu_table_id.strip())
        else:
            if not (args.feishu_app_token and args.feishu_table_id):
                _fail("missing_arg",
                      "回填模式必须提供 --feishu_app_token 和 --feishu_table_id")
            do_update_feishu(args.open_id, args.feishu_app_token.strip(),
                             args.feishu_table_id.strip())
    except g.GiteaError as exc:
        _fail("gitea_error", str(exc))
    except Exception as exc:  # noqa: BLE001
        _fail("unexpected_error", f"未预期的错误：{exc}")


if __name__ == "__main__":
    main()
