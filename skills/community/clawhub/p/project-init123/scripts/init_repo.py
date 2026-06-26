#!/usr/bin/env python3
"""
init_repo.py
科研项目仓库初始化脚本

执行顺序：
  1. 幂等检查（README.md 是否存在）
  2. 创建仓库
  3. 写入目录结构和基础文档（含 profiles/ 成员档案）
  4. 将创建者加为 admin 协作者
  5. 将各成员加为 read 协作者
  6. 创建初始 Issue
  7. 发送邮件通知（调用 imap-smtp-email Skill）
  8. 任何步骤失败时发送失败邮件

用法：
  python3 init_repo.py \
    --repo-name <name> \
    --description <desc> \
    --creator <username> \
    [--private true|false] \
    [--members user1,user2] \
    [--existing]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from string import Template

import requests
from dotenv import load_dotenv

# ── 加载配置 ──────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = Path.home() / '.config' / 'project-init' / '.env'
FALLBACK_ENV = SKILL_DIR / '.env'

if CONFIG_PATH.exists():
    load_dotenv(CONFIG_PATH)
elif FALLBACK_ENV.exists():
    load_dotenv(FALLBACK_ENV)

GITEA_URL        = os.environ.get('GITEA_URL', 'http://43.156.243.152:3000').rstrip('/')
GITEA_TOKEN      = os.environ.get('GITEA_TOKEN', '')
GITEA_ORG        = os.environ.get('GITEA_ORG', 'HKU-AIFusion')
EMAIL_SKILL_PATH = os.environ.get('EMAIL_SKILL_PATH', '')
EMAIL_ACCOUNT    = os.environ.get('EMAIL_ACCOUNT', '')

TEMPLATES_DIR = Path(__file__).parent / 'templates'

# ── Gitea API 工具函数 ─────────────────────────────────────────

def _headers():
    return {
        'Authorization': f'token {GITEA_TOKEN}',
        'Content-Type': 'application/json',
    }

def api_get(path):
    return requests.get(f'{GITEA_URL}/api/v1{path}', headers=_headers(), timeout=15)

def api_post(path, data):
    return requests.post(f'{GITEA_URL}/api/v1{path}', json=data, headers=_headers(), timeout=15)

def api_put(path, data):
    return requests.put(f'{GITEA_URL}/api/v1{path}', json=data, headers=_headers(), timeout=15)

# ── 邮件发送（调用 imap-smtp-email Skill）────────────────────

def send_email(to: str, subject: str, body: str) -> bool:
    """调用 imap-smtp-email Skill 的 smtp.js 发送邮件"""
    if not EMAIL_SKILL_PATH:
        print('[WARN] EMAIL_SKILL_PATH 未配置，跳过邮件发送', file=sys.stderr)
        return False

    smtp_script = Path(EMAIL_SKILL_PATH) / 'scripts' / 'smtp.js'
    if not smtp_script.exists():
        print(f'[WARN] 未找到 smtp.js: {smtp_script}', file=sys.stderr)
        return False

    cmd = ['node', str(smtp_script), 'send', '--to', to, '--subject', subject, '--body', body]
    if EMAIL_ACCOUNT:
        cmd = ['node', str(smtp_script), '--account', EMAIL_ACCOUNT,
               'send', '--to', to, '--subject', subject, '--body', body]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f'[WARN] 邮件发送失败: {result.stderr}', file=sys.stderr)
    return result.returncode == 0


def get_user_email(username: str) -> str | None:
    """通过 Gitea API 获取用户邮箱"""
    resp = api_get(f'/users/{username}')
    if resp.status_code == 200:
        return resp.json().get('email')
    return None


def send_failure_email(creator: str, repo_name: str, failed_step: str, error_msg: str):
    """初始化失败时发邮件通知创建者"""
    email = get_user_email(creator) if creator else None
    if not email:
        print('[WARN] 无法获取创建者邮箱，跳过失败通知', file=sys.stderr)
        return
    subject = f'[AIFusion] 仓库 {repo_name} 初始化失败'
    body = (
        f'仓库初始化过程中出现错误，请手动补全。\n\n'
        f'仓库名称：{repo_name}\n'
        f'失败步骤：{failed_step}\n'
        f'错误信息：{error_msg}\n\n'
        f'仓库地址：{GITEA_URL}/{GITEA_ORG}/{repo_name}\n\n'
        f'--- AIFusion Bot'
    )
    send_email(email, subject, body)

# ── 核心初始化函数 ─────────────────────────────────────────────

def check_idempotent(repo_name: str) -> bool:
    """检查 README.md 是否已存在（幂等保护）"""
    resp = api_get(f'/repos/{GITEA_ORG}/{repo_name}/contents/README.md')
    return resp.status_code == 200


def create_repo(repo_name: str, description: str, private: bool):
    """Step 1: 创建 Gitea 仓库"""
    data = {
        'name': repo_name,
        'description': description,
        'private': private,
        'auto_init': False,
    }
    resp = api_post(f'/orgs/{GITEA_ORG}/repos', data)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f'创建仓库失败 HTTP {resp.status_code}: {resp.text}')


def write_file(repo_name: str, filepath: str, content: str, commit_msg: str):
    """通过 Gitea API 写入单个文件"""
    content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    resp = api_post(
        f'/repos/{GITEA_ORG}/{repo_name}/contents/{filepath}',
        {'message': commit_msg, 'content': content_b64}
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f'写入 {filepath} 失败 HTTP {resp.status_code}: {resp.text}')


def add_collaborator(repo_name: str, username: str, permission: str):
    """Step 4/5: 将用户加为仓库协作者，permission: read / write / admin"""
    resp = api_put(
        f'/repos/{GITEA_ORG}/{repo_name}/collaborators/{username}',
        {'permission': permission}
    )
    if resp.status_code not in (200, 201, 204):
        raise RuntimeError(
            f'将 {username} 加为协作者失败 HTTP {resp.status_code}: {resp.text}'
        )


def create_issue(repo_name: str, title: str, body: str, assignees: list | None = None):
    """Step 6: 创建 Issue"""
    resp = api_post(
        f'/repos/{GITEA_ORG}/{repo_name}/issues',
        {'title': title, 'body': body, 'assignees': assignees or []}
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f'创建 Issue "{title}" 失败 HTTP {resp.status_code}: {resp.text}')


def render_template(tpl_name: str, variables: dict) -> str:
    """读取模板文件并做变量替换"""
    tpl_path = TEMPLATES_DIR / tpl_name
    with open(tpl_path, 'r', encoding='utf-8') as f:
        return Template(f.read()).safe_substitute(variables)


def make_profile(username: str, created_date: str) -> str:
    """生成单个成员档案的 Markdown 内容"""
    return (
        f'# @{username} 的成员档案\n\n'
        f'## 基本信息\n'
        f'- Gitea 用户名：@{username}\n'
        f'- 加入日期：{created_date}\n\n'
        f'## 负责模块\n'
        f'（待本人补充）\n\n'
        f'## 主要职责\n'
        f'（待本人补充）\n\n'
        f'## 技术能力\n'
        f'（待本人补充）\n\n'
        f'## 备注\n'
        f'（待本人补充）\n'
    )

# ── 主流程 ────────────────────────────────────────────────────

def init_repo(repo_name: str, description: str, private: bool,
              creator: str, members: list, existing: bool) -> dict:

    repo_url = f'{GITEA_URL}/{GITEA_ORG}/{repo_name}'
    now = datetime.now().strftime('%Y-%m-%d')

    # ── 幂等检查 ────────────────────────────────────────────
    if not existing and check_idempotent(repo_name):
        return {
            'status': 'skipped',
            'message': f'仓库 {repo_name} 的 README.md 已存在，跳过初始化。',
            'repoUrl': repo_url,
        }

    # ── Step 1: 创建仓库 ─────────────────────────────────────
    if not existing:
        try:
            create_repo(repo_name, description, private)
        except Exception as e:
            send_failure_email(creator, repo_name, '创建仓库', str(e))
            raise

    # ── Step 2: 写入目录结构和文档 ───────────────────────────
    gitkeep = '# 此文件用于保留空目录，请勿删除\n'
    init_msg = 'chore: 初始化标准目录结构'

    # 所有参与成员（创建者 + 其他成员）
    all_members = list(dict.fromkeys([creator] + members))  # 去重，创建者排第一

    # README 变量替换
    members_str = '\n'.join(f'- @{m}' for m in all_members)
    readme_content = render_template('README.tpl.md', {
        'repo_name':    repo_name,
        'description':  description,
        'created_by':   creator,
        'created_date': now,
        'members':      members_str,
        'gitea_url':    GITEA_URL,
        'org':          GITEA_ORG,
    })

    contributing_content = render_template('CONTRIBUTING.tpl.md', {})

    # 基础目录占位文件
    files_to_write = [
        ('meeting/.gitkeep',  gitkeep,               init_msg),
        ('docs/.gitkeep',     gitkeep,               init_msg),
        ('src/.gitkeep',      gitkeep,               init_msg),
        ('data/.gitkeep',     gitkeep,               init_msg),
        ('reports/.gitkeep',  gitkeep,               init_msg),
        ('profiles/.gitkeep', gitkeep,               init_msg),
        ('README.md',         readme_content,        'docs: 添加 README.md'),
        ('CONTRIBUTING.md',   contributing_content,  'docs: 添加 CONTRIBUTING.md'),
    ]

    # 每个成员生成一个档案文件
    for username in all_members:
        profile_content = make_profile(username, now)
        files_to_write.append((
            f'profiles/{username}.md',
            profile_content,
            f'docs: 添加 {username} 成员档案',
        ))

    try:
        for filepath, content, msg in files_to_write:
            write_file(repo_name, filepath, content, msg)
    except Exception as e:
        send_failure_email(creator, repo_name, '写入目录结构和文档', str(e))
        raise

    # ── Step 3: 将创建者加为 admin 协作者 ───────────────────
    try:
        add_collaborator(repo_name, creator, 'admin')
    except Exception as e:
        send_failure_email(creator, repo_name, f'将创建者 {creator} 设为 admin', str(e))
        raise

    # ── Step 4: 将其他成员加为 read 协作者 ──────────────────
    collab_errors = []
    for username in members:
        try:
            add_collaborator(repo_name, username, 'read')
        except Exception as e:
            collab_errors.append(username)
            print(f'[WARN] 加入协作者失败 {username}: {e}', file=sys.stderr)

    # ── Step 5: 创建初始 Issue ───────────────────────────────
    members_mention = ' '.join(f'@{m}' for m in all_members)
    issue1_body = (
        f'仓库 `{repo_name}` 已完成自动初始化，欢迎所有成员查阅！\n\n'
        f'{members_mention}\n\n'
        f'**请务必阅读 [README.md]({repo_url}/src/branch/main/README.md) 了解：**\n'
        f'- 目录结构与各文件夹用途\n'
        f'- 成员档案（profiles/）的填写说明\n'
        f'- 分支命名规范\n'
        f'- Issue 使用说明\n'
        f'- 会议纪要上传规范\n\n'
        f'仓库地址：{repo_url}'
    )

    issue2_body = (
        f'请 @{creator} 在本 Issue 中明确各成员的工作职责，确认后关闭此 Issue。\n\n'
        f'确认分工后，请各成员补充自己在 `profiles/` 目录下的个人档案文件。\n\n'
        f'建议格式：\n'
        f'| 成员 | 职责 |\n'
        f'|------|------|\n'
        f'| @xxx | 负责 xxx |\n\n'
        f'完成后请在此 Issue 留言确认并关闭。'
    )

    try:
        create_issue(repo_name, '【全体通知】新项目仓库已创建，请查阅 README', issue1_body, assignees=[])
        create_issue(repo_name, '【启动任务】确认成员分工与职责', issue2_body, assignees=[creator])
    except Exception as e:
        send_failure_email(creator, repo_name, '创建 Issue', str(e))
        raise

    # ── Step 6: 发送邮件通知 ────────────────────────────────
    email_errors = []

    # 通知其他成员
    for username in members:
        email = get_user_email(username)
        if not email:
            email_errors.append(username)
            continue
        ok = send_email(
            email,
            f'[AIFusion] 你被加入了新项目仓库：{repo_name}',
            (
                f'Hi @{username}，\n\n'
                f'你被加入了新的科研项目仓库：{repo_name}\n\n'
                f'项目描述：{description}\n'
                f'创建者：@{creator}\n'
                f'仓库地址：{repo_url}\n\n'
                f'请查阅 README.md 了解项目结构和协作规范，\n'
                f'并补充 profiles/{username}.md 中的个人档案信息。\n\n'
                f'--- AIFusion Bot'
            )
        )
        if not ok:
            email_errors.append(username)

    # 通知创建者（汇总结果）
    creator_email = get_user_email(creator)
    if creator_email:
        warnings = ''
        if collab_errors:
            warnings += f'  ⚠️  以下成员加入仓库失败，请手动添加：{", ".join(collab_errors)}\n'
        if email_errors:
            warnings += f'  ⚠️  以下成员邮件发送失败，请手动通知：{", ".join(email_errors)}\n'

        send_email(
            creator_email,
            f'[AIFusion] 仓库 {repo_name} 初始化成功',
            (
                f'Hi @{creator}，\n\n'
                f'仓库 {repo_name} 已成功初始化！\n\n'
                f'仓库地址：{repo_url}\n\n'
                f'已完成：\n'
                f'  ✅ 标准目录结构（meeting/ docs/ src/ data/ reports/ profiles/）\n'
                f'  ✅ README.md 和 CONTRIBUTING.md\n'
                f'  ✅ 各成员档案文件（profiles/）\n'
                f'  ✅ 你已被设为仓库管理员\n'
                f'  ✅ 2 个启动期 Issue\n'
                + (warnings if warnings else '  ✅ 所有成员已成功加入仓库并收到通知\n')
                + f'\n--- AIFusion Bot'
            )
        )

    return {
        'status': 'success',
        'repoUrl': repo_url,
        'emailErrors': email_errors,
        'collabErrors': collab_errors,
    }

# ── 命令行入口 ─────────────────────────────────────────────────

def main():
    if not GITEA_TOKEN:
        print(json.dumps({'status': 'error', 'message': 'GITEA_TOKEN 未配置，请运行 setup.sh'}))
        sys.exit(1)

    parser = argparse.ArgumentParser(description='初始化 Gitea 科研项目仓库')
    parser.add_argument('--repo-name',   required=True)
    parser.add_argument('--description', required=True)
    parser.add_argument('--creator',     required=True)
    parser.add_argument('--private',     default='false')
    parser.add_argument('--members',     default='')
    parser.add_argument('--existing',    action='store_true')
    args = parser.parse_args()

    members = [m.strip() for m in args.members.split(',') if m.strip()] if args.members else []
    private = args.private.lower() == 'true'

    try:
        result = init_repo(
            repo_name=args.repo_name,
            description=args.description,
            private=private,
            creator=args.creator,
            members=members,
            existing=args.existing,
        )
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
