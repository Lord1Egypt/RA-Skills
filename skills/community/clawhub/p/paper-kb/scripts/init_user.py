#!/usr/bin/env python3
"""
工具1：新用户初始化
- 默认：验证 Gitea 用户名 → 创建 knowledge-base 仓库 → 初始化结构 → 写 users.json
- action=update_bitable_info：将飞书表格的 app_token/table_id/url 写入 users.json
"""
import sys, json, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.gitea_client import GiteaClient

GITEA_URL    = os.environ.get('GITEA_URL', 'http://43.156.243.152:3000')
SYSTEM_REPO  = os.environ.get('GITEA_SYSTEM_REPO', 'AIFusionBot/system-config')

ARXIV_CATS = [
    'cs.RO', 'cs.LG', 'cs.CV', 'cs.AI', 'cs.SY',
    'cs.HC', 'eess.SP', 'eess.SY', 'math.OC', 'other'
]

INIT_README = """# 我的科研知识库

> 由 paper-kb skill 自动管理

## 使用方式
在飞书向机器人发送 arxiv 链接或 PDF 即可入库，
用自然语言提问即可查询。

## 文件夹
| 文件夹 | 说明 |
|--------|------|
| cs.RO | Robotics |
| cs.LG | Machine Learning |
| cs.CV | Computer Vision |
| cs.AI | Artificial Intelligence |
| cs.SY | Systems and Control |
| cs.HC | Human-Computer Interaction |
| eess.SP | Signal Processing |
| eess.SY | Systems and Control (EE) |
| math.OC | Optimization and Control |
| other | 其他 |
"""

INIT_INDEX = {'total': 0, 'last_updated': '', 'papers': []}


def load_users(gitea):
    data, sha = gitea.read_json(SYSTEM_REPO, 'users.json')
    if data is None:
        return {'users': {}}, None
    return data, sha


def do_register(params, gitea):
    feishu_user_id = params.get('feishu_user_id', '').strip()
    gitea_username  = params.get('gitea_username', '').strip()
    display_name    = params.get('display_name', '').strip()

    if not feishu_user_id or not gitea_username or not display_name:
        return {'success': False, 'error': '缺少必要参数：feishu_user_id / gitea_username / display_name'}

    # 1. 验证 Gitea 用户名
    check = gitea.check_user_exists(gitea_username)
    if not check['success']:
        return {'success': False, 'error': f'Gitea 连接失败：{check["error"]}'}
    if not check['exists']:
        return {
            'success': False,
            'error': f'Gitea 用户名 "{gitea_username}" 不存在，请先在 {GITEA_URL}/user/sign_up 注册'
        }

    repo_full = f'{gitea_username}/knowledge-base'
    repo_url  = f'{GITEA_URL}/{repo_full}'

    # 2. 检查仓库是否已存在
    repo_check = gitea.get_repo(gitea_username, 'knowledge-base')
    if not repo_check['success']:
        return {'success': False, 'error': f'仓库查询失败：{repo_check["error"]}'}

    already_existed = repo_check['exists']

    if not already_existed:
        # 3. 创建私有仓库
        r = gitea.create_repo_for_user(
            gitea_username, 'knowledge-base',
            private=True, description='科研知识库（paper-kb 自动管理）'
        )
        if not r['success']:
            return {'success': False, 'error': f'创建仓库失败：{r["error"]}'}

        # 4. 初始化文件
        gitea.create_file(repo_full, 'README.md',  INIT_README, 'init: README')
        gitea.write_json(repo_full, 'index.json',  INIT_INDEX,  'init: index.json')
        for cat in ARXIV_CATS:
            gitea.create_file(repo_full, f'{cat}/.gitkeep', '', f'init: {cat} folder')

    # 5. 写 users.json
    users, sha = load_users(gitea)
    users.setdefault('users', {})[feishu_user_id] = {
        'display_name':     display_name,
        'gitea_username':   gitea_username,
        'repo':             repo_full,
        'feishu_app_token': '',
        'feishu_table_id':  '',
        'feishu_table_url': '',
        'registered_at':    datetime.now().strftime('%Y-%m-%d')
    }
    wr = gitea.write_json(SYSTEM_REPO, 'users.json', users,
                          f'register: {gitea_username}', sha=sha)
    if not wr['success']:
        return {'success': False, 'error': f'写入 users.json 失败：{wr["error"]}'}

    return {
        'success':        True,
        'repo_url':       repo_url,
        'repo_full':      repo_full,
        'gitea_username': gitea_username,
        'already_existed': already_existed
    }


def do_update_bitable(params, gitea):
    feishu_user_id   = params.get('feishu_user_id', '').strip()
    feishu_app_token = params.get('feishu_app_token', '').strip()
    feishu_table_id  = params.get('feishu_table_id', '').strip()
    feishu_table_url = params.get('feishu_table_url', '').strip()

    if not feishu_user_id or not feishu_app_token or not feishu_table_id:
        return {'success': False, 'error': '缺少 feishu_user_id / feishu_app_token / feishu_table_id'}

    users, sha = load_users(gitea)
    if feishu_user_id not in users.get('users', {}):
        return {'success': False, 'error': '用户未注册，请先完成初始化'}

    users['users'][feishu_user_id].update({
        'feishu_app_token': feishu_app_token,
        'feishu_table_id':  feishu_table_id,
        'feishu_table_url': feishu_table_url,
    })
    wr = gitea.write_json(SYSTEM_REPO, 'users.json', users,
                          f'update bitable: {users["users"][feishu_user_id]["gitea_username"]}',
                          sha=sha)
    return {'success': wr['success'], 'error': wr.get('error', '')}


def main():
    params = json.loads(sys.stdin.read().strip())
    gitea  = GiteaClient()
    action = params.get('action', '')

    if action == 'update_bitable_info':
        result = do_update_bitable(params, gitea)
    else:
        result = do_register(params, gitea)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
