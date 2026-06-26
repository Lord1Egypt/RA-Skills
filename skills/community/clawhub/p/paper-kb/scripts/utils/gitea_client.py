import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class GiteaClient:
    def __init__(self):
        self.base_url = os.environ.get('GITEA_URL', 'http://43.156.243.152:3000').rstrip('/')
        self.token = os.environ.get('GITEA_ADMIN_TOKEN', '')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _url(self, path):
        return f"{self.base_url}/api/v1{path}"

    # ── 用户 ──────────────────────────────────────────────

    def check_user_exists(self, username):
        r = requests.get(self._url(f'/users/{username}'), headers=self.headers, timeout=10)
        if r.status_code == 200:
            return {'success': True, 'exists': True}
        if r.status_code == 404:
            return {'success': True, 'exists': False}
        return {'success': False, 'error': f'HTTP {r.status_code}'}

    # ── 仓库 ──────────────────────────────────────────────

    def get_repo(self, owner, repo_name):
        r = requests.get(self._url(f'/repos/{owner}/{repo_name}'), headers=self.headers, timeout=10)
        if r.status_code == 200:
            return {'success': True, 'exists': True}
        if r.status_code == 404:
            return {'success': True, 'exists': False}
        return {'success': False, 'error': f'HTTP {r.status_code}'}

    def create_repo_for_user(self, username, repo_name, private=True, description=''):
        payload = {
            'name': repo_name,
            'description': description,
            'private': private,
            'auto_init': False,
            'default_branch': 'main'
        }
        r = requests.post(
            self._url(f'/admin/users/{username}/repos'),
            headers=self.headers, json=payload, timeout=15
        )
        if r.status_code in (200, 201):
            return {'success': True}
        return {'success': False, 'error': f'HTTP {r.status_code}: {r.text[:200]}'}

    # ── 文件读取 ──────────────────────────────────────────

    def get_file(self, repo, filepath):
        """返回 {'success': True, 'content': base64str, 'sha': str} 或 {'success': False, ...}"""
        owner, repo_name = repo.split('/', 1)
        r = requests.get(
            self._url(f'/repos/{owner}/{repo_name}/contents/{filepath}'),
            headers=self.headers, timeout=15
        )
        if r.status_code == 200:
            d = r.json()
            return {'success': True, 'content': d['content'], 'sha': d['sha']}
        if r.status_code == 404:
            return {'success': False, 'not_found': True, 'error': 'File not found'}
        return {'success': False, 'error': f'HTTP {r.status_code}'}

    def read_text(self, repo, filepath):
        """直接返回文件文本内容，失败返回 None"""
        r = self.get_file(repo, filepath)
        if not r['success']:
            return None
        return base64.b64decode(r['content']).decode('utf-8')

    def read_json(self, repo, filepath):
        """返回 (dict, sha) 或 (None, None)"""
        r = self.get_file(repo, filepath)
        if not r['success']:
            return None, None
        text = base64.b64decode(r['content']).decode('utf-8')
        return json.loads(text), r['sha']

    # ── 文件写入 ──────────────────────────────────────────

    def _encode(self, content):
        if isinstance(content, str):
            return base64.b64encode(content.encode('utf-8')).decode('utf-8')
        return base64.b64encode(content).decode('utf-8')

    def create_file(self, repo, filepath, content, message):
        owner, repo_name = repo.split('/', 1)
        r = requests.post(
            self._url(f'/repos/{owner}/{repo_name}/contents/{filepath}'),
            headers=self.headers,
            json={'message': message, 'content': self._encode(content)},
            timeout=30
        )
        if r.status_code in (200, 201):
            return {'success': True}
        return {'success': False, 'error': f'HTTP {r.status_code}: {r.text[:200]}'}

    def update_file(self, repo, filepath, content, message, sha):
        owner, repo_name = repo.split('/', 1)
        r = requests.put(
            self._url(f'/repos/{owner}/{repo_name}/contents/{filepath}'),
            headers=self.headers,
            json={'message': message, 'content': self._encode(content), 'sha': sha},
            timeout=30
        )
        if r.status_code in (200, 201):
            return {'success': True}
        return {'success': False, 'error': f'HTTP {r.status_code}: {r.text[:200]}'}

    def upsert_file(self, repo, filepath, content, message):
        """自动判断创建还是更新"""
        r = self.get_file(repo, filepath)
        if r['success']:
            return self.update_file(repo, filepath, content, message, r['sha'])
        return self.create_file(repo, filepath, content, message)

    def write_json(self, repo, filepath, data, message, sha=None):
        text = json.dumps(data, ensure_ascii=False, indent=2)
        if sha:
            return self.update_file(repo, filepath, text, message, sha)
        return self.upsert_file(repo, filepath, text, message)
