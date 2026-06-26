#!/usr/bin/env python3
"""
工具3：知识查询
- get_index：读取用户 index.json + 用户 bitable 信息
- get_papers：读取指定论文的 MD 文件内容
"""
import sys, json, os, base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.gitea_client import GiteaClient

GITEA_URL   = os.environ.get('GITEA_URL', 'http://43.156.243.152:3000')
SYSTEM_REPO = os.environ.get('GITEA_SYSTEM_REPO', 'AIFusionBot/system-config')


def load_user_info(gitea, feishu_user_id):
    users, _ = gitea.read_json(SYSTEM_REPO, 'users.json')
    if not users:
        return None
    return users.get('users', {}).get(feishu_user_id)


def action_get_index(params):
    feishu_user_id = (params.get('feishu_user_id') or '').strip()
    if not feishu_user_id:
        return {'success': False, 'error': '缺少 feishu_user_id'}

    gitea     = GiteaClient()
    user_info = load_user_info(gitea, feishu_user_id)
    if not user_info:
        return {'success': False, 'error': '用户未注册，请先初始化'}

    repo      = user_info['repo']
    index, _  = gitea.read_json(repo, 'index.json')
    if index is None:
        return {'success': False, 'error': 'index.json 读取失败，请检查仓库是否正常'}

    # 为每篇论文补充访问链接
    for p in index.get('papers', []):
        if p.get('md_path'):
            p['md_url'] = f"{GITEA_URL}/{repo}/src/branch/main/{p['md_path']}"

    return {
        'success':      True,
        'user_info': {
            'display_name':     user_info.get('display_name', ''),
            'gitea_username':   user_info.get('gitea_username', ''),
            'repo':             repo,
            'repo_url':         f"{GITEA_URL}/{repo}",
            'feishu_app_token': user_info.get('feishu_app_token', ''),
            'feishu_table_id':  user_info.get('feishu_table_id', ''),
            'feishu_table_url': user_info.get('feishu_table_url', ''),
        },
        'total':        index.get('total', 0),
        'last_updated': index.get('last_updated', ''),
        'papers':       index.get('papers', [])
    }


def action_get_papers(params):
    feishu_user_id = (params.get('feishu_user_id') or '').strip()
    paper_ids      = params.get('paper_ids') or []

    if not feishu_user_id:
        return {'success': False, 'error': '缺少 feishu_user_id'}
    if not paper_ids:
        return {'success': False, 'error': '缺少 paper_ids'}

    gitea     = GiteaClient()
    user_info = load_user_info(gitea, feishu_user_id)
    if not user_info:
        return {'success': False, 'error': '用户未注册'}

    repo     = user_info['repo']
    index, _ = gitea.read_json(repo, 'index.json')
    if index is None:
        return {'success': False, 'error': 'index.json 读取失败'}

    id_to_path = {p['id']: p['md_path']
                  for p in index.get('papers', [])
                  if 'id' in p and 'md_path' in p}

    results = []
    for pid in paper_ids[:5]:
        md_path = id_to_path.get(pid)
        if not md_path:
            results.append({'id': pid, 'success': False, 'error': f'找不到论文 ID：{pid}'})
            continue

        fr = gitea.get_file(repo, md_path)
        if not fr['success']:
            results.append({'id': pid, 'success': False, 'error': fr.get('error', '')})
            continue

        md_content = base64.b64decode(fr['content']).decode('utf-8')
        results.append({
            'id':         pid,
            'success':    True,
            'md_path':    md_path,
            'md_url':     f"{GITEA_URL}/{repo}/src/branch/main/{md_path}",
            'md_content': md_content
        })

    return {
        'success':        True,
        'papers':         results,
        'fetched':        sum(1 for r in results if r['success']),
        'total_requested': len(paper_ids)
    }


def main():
    params = json.loads(sys.stdin.read().strip())
    action = params.get('action', '')
    handlers = {
        'get_index':  action_get_index,
        'get_papers': action_get_papers,
    }
    handler = handlers.get(action)
    if not handler:
        result = {'success': False, 'error': f'未知 action：{action}'}
    else:
        try:
            result = handler(params)
        except Exception as e:
            result = {'success': False, 'error': str(e)}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
