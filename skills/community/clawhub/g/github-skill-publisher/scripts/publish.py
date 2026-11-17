"""
GitHub Skill Publisher - 标准化发布脚本
封装了今天踩过的所有坑（auto_init README 覆盖、URL 转码、PUT 必传 sha 等）

用法：
    export GH_TOKEN='ghp_xxx'  # 必须
    python3 publish.py <owner> <repo-name> <本地目录> [description]

示例：
    python3 publish.py <owner> my-skill ~/Desktop/my-skill "口播博主每条视频卡开头？5 套钩子公式轮换，30 秒出脚本。"
"""
import base64
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

GITHUB_API = 'https://api.github.com'


def auth_headers(token):
    return {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github+json',
    }


def create_repo(token, name, description, private=False, topics=None):
    """建空仓。auto_init=True 是关键,后续上传时记得带 sha。"""
    payload = {
        'name': name,
        'description': description,
        'private': private,
        'auto_init': True,
    }
    req = urllib.request.Request(
        f'{GITHUB_API}/user/repos',
        data=json.dumps(payload).encode('utf-8'),
        headers=auth_headers(token),
        method='POST',
    )
    with urllib.request.urlopen(req) as r:
        repo_data = json.loads(r.read())
    print(f'  ✅ 仓库已建: {repo_data["html_url"]}')

    if topics:
        set_topics(token, name, topics)

    return repo_data


def upload_file(token, owner, repo, path, local_path, message=None):
    """上传单个文件。

    关键坑：auto_init 仓里的 README 必须先 GET 拿 sha 再 PUT,否则 422。
    """
    with open(local_path, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode('utf-8')

    # 先 GET 拿 sha（如果文件已存在）
    sha = None
    url = f'{GITHUB_API}/repos/{owner}/{repo}/contents/{urllib.parse.quote(path, safe="/")}'
    try:
        req = urllib.request.Request(url, headers=auth_headers(token))
        with urllib.request.urlopen(req) as r:
            sha = json.loads(r.read())['sha']
    except urllib.error.HTTPError:
        pass  # 新文件,无 sha

    payload = {
        'message': message or f'feat: 上传 {path}',
        'content': content_b64,
    }
    if sha:
        payload['sha'] = sha

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=auth_headers(token),
        method='PUT',
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
        return result['commit']['sha']


def upload_dir(token, owner, repo, local_dir, file_order=None):
    """递归上传整个目录。

    file_order: 优先上传的文件列表（先根目录 README,再子目录）
    """
    all_files = []
    for root, dirs, files in os.walk(local_dir):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, local_dir)
            all_files.append(rel)

    if file_order:
        # 按指定顺序排
        ordered = [f for f in file_order if f in all_files]
        rest = [f for f in all_files if f not in file_order]
        all_files = ordered + rest

    for rel in all_files:
        full = os.path.join(local_dir, rel)
        sha = upload_file(token, owner, repo, rel, full, message=f'feat: 初始化仓库,上传 {rel}')
        print(f'  ✅ {rel:50s} {sha[:8]}')


def set_topics(token, owner, repo, topics):
    """改 topics。注意 accept header 要带 mercy-preview。"""
    url = f'{GITHUB_API}/repos/{owner}/{repo}/topics'
    req = urllib.request.Request(
        url,
        data=json.dumps({'names': topics}).encode('utf-8'),
        headers={
            **auth_headers(token),
            'Accept': 'application/vnd.github.mercy-preview+json',
        },
        method='PUT',
    )
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read())
        print(f'  ✅ topics: {d["names"]}')


def set_visibility(token, owner, repo, private=False):
    """改公开/私有。"""
    url = f'{GITHUB_API}/repos/{owner}/{repo}'
    req = urllib.request.Request(
        url,
        data=json.dumps({'private': private}).encode('utf-8'),
        headers=auth_headers(token),
        method='PATCH',
    )
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read())
        print(f'  ✅ visibility: {d["visibility"]}')


def create_release(token, owner, repo, tag, name, body):
    """发 release。"""
    url = f'{GITHUB_API}/repos/{owner}/{repo}/releases'
    req = urllib.request.Request(
        url,
        data=json.dumps({
            'tag_name': tag,
            'name': name,
            'body': body,
            'draft': False,
            'prerelease': False,
        }).encode('utf-8'),
        headers=auth_headers(token),
        method='POST',
    )
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read())
        print(f'  ✅ release: {d["tag_name"]} -> {d["html_url"]}')


def privacy_scan(local_dir, ignore_files=None):
    """脱敏检查。返回问题列表。

    ignore_files: 跳过这些文件名(用于排除规则定义自身)
    """
    import re
    patterns = [
        (r'<USER_DIR>/[^\s]+', '本地绝对路径'),
        (r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '邮箱'),
        (r'1[3-9][0-9]{9}', '手机号'),
        (r'sk-[A-Za-z0-9]{20,}', 'OpenAI key'),
        (r'ghp_[A-Za-z0-9]{20,}', 'GitHub PAT (classic)'),
        (r'github_pat_[A-Za-z0-9]{20,}', 'GitHub PAT (fine-grained)'),
    ]
    ignore_files = ignore_files or []
    issues = []
    for root, dirs, files in os.walk(local_dir):
        for f in files:
            full = os.path.join(root, f)
            # 跳过规则定义自身(脚本和 SKILL.md)
            if f in ignore_files:
                continue
            try:
                with open(full, 'r', encoding='utf-8') as fp:
                    content = fp.read()
            except (UnicodeDecodeError, IOError):
                continue
            for pat, desc in patterns:
                m = re.search(pat, content)
                if m:
                    issues.append((full, desc, m.group()[:60]))
    return issues


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]
    local_dir = os.path.expanduser(sys.argv[3])
    description = sys.argv[4] if len(sys.argv) > 4 else ''

    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        print('❌ 请先 export GH_TOKEN=xxx')
        sys.exit(1)

    if not os.path.isdir(local_dir):
        print(f'❌ 目录不存在: {local_dir}')
        sys.exit(1)

    # 1. 脱敏检查(跳过规则定义自身)
    print('=== 脱敏检查 ===')
    issues = privacy_scan(local_dir, ignore_files=['publish.py', 'SKILL.md'])
    if issues:
        print(f'❌ 发现 {len(issues)} 个潜在问题:')
        for path, desc, snippet in issues:
            print(f'   {path}: {desc} -> {snippet}')
        print('请先修复再发布。')
        sys.exit(1)
    print('  ✅ 干净')

    # 2. 建仓
    print(f'\n=== 建仓 {owner}/{repo} ===')
    create_repo(token, repo, description, private=False)

    # 3. 上传文件
    print(f'\n=== 上传文件 ===')
    upload_dir(token, owner, repo, local_dir)

    print(f'\n✅ 完成: https://github.com/{owner}/{repo}')


if __name__ == '__main__':
    main()
