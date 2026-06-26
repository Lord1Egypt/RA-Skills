import os
import json
import requests
from pathlib import Path

MUMU_API_URL = os.getenv("MUMU_API_URL", "http://localhost:8000").rstrip("/")
MUMU_USERNAME = os.getenv("MUMU_USERNAME", "admin")
MUMU_PASSWORD = os.getenv("MUMU_PASSWORD", "admin123")
DEFAULT_TIMEOUT = float(os.getenv("MUMU_HTTP_TIMEOUT", "60"))


def get_request_timeout(stream=False):
    if stream:
        return (DEFAULT_TIMEOUT, None)
    return DEFAULT_TIMEOUT

def get_session_file():
    session_file = os.getenv("MUMU_SESSION_FILE")
    if not session_file:
        return None
    return Path(session_file).expanduser()

class MumuClient:
    def __init__(self, project_id=None, style_id=None):
        self.session = requests.Session()
        self.project_id = project_id or os.getenv("MUMU_PROJECT_ID")
        self.style_id = style_id or os.getenv("MUMU_STYLE_ID")
        
        self._load_cookies()
        if not self._check_auth():
            self.login()
            
    def require_project_id(self):
        if not self.project_id:
            raise Exception("尚未绑定小说项目！请先运行 bind_project.py 进行存量绑定或新建小说。")
        return self.project_id

    def set_project_id(self, project_id: str):
        self.project_id = project_id
        # Removed writing to .env to allow multi-agent concurrency in the same workspace.
        # Agents will must remember this ID and pass it via --project_id <ID> to scripts.
        print(f"[System] MUMU_PROJECT_ID 绑定成功，当前 Agent 需记住此 ID -> {project_id}")

    def set_style_id(self, style_id: str):
        self.style_id = style_id
        # Removed writing to .env to allow multi-agent concurrency
        print(f"[System] MUMU_STYLE_ID 写作风格已成功刻印，当前 Agent 需记住此 Style ID -> {style_id}")

    def _load_cookies(self):
        session_file = get_session_file()
        if session_file and session_file.exists():
            try:
                cookies_dict = json.loads(session_file.read_text())
                self.session.cookies.update(cookies_dict)
            except Exception:
                pass

    def _save_cookies(self):
        session_file = get_session_file()
        if not session_file:
            return
        cookies_dict = self.session.cookies.get_dict()
        session_file.parent.mkdir(parents=True, exist_ok=True)
        session_file.write_text(json.dumps(cookies_dict))

    def _check_auth(self):
        try:
            resp = self.session.get(f"{MUMU_API_URL}/api/users/me", timeout=DEFAULT_TIMEOUT)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def login(self):
        url = f"{MUMU_API_URL}/api/auth/local/login"
        data = {
            "username": MUMU_USERNAME,
            "password": MUMU_PASSWORD
        }
        resp = self.session.post(url, json=data, timeout=DEFAULT_TIMEOUT)
        if resp.status_code == 200:
            # 登录响应会在 Header 中包含 Set-Cookie
            self.session.cookies.update(resp.cookies)
            self._save_cookies()
            print("[System] 登录 MuMuAINovel 成功，已获取授权 Session Cookies。")
        else:
            raise Exception(f"登录失败: {resp.status_code} - {resp.text}")

    def get(self, endpoint, **kwargs):
        url = f"{MUMU_API_URL}/api/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", get_request_timeout())
        resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def post(self, endpoint, json_data=None, data=None, **kwargs):
        url = f"{MUMU_API_URL}/api/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", get_request_timeout(stream=bool(kwargs.get("stream"))))
        resp = self.session.post(url, json=json_data, data=data, **kwargs)
        if kwargs.get('stream'):
            resp.raise_for_status()
            return resp
        resp.raise_for_status()
        return resp.json()

    def put(self, endpoint, json_data=None, data=None, **kwargs):
        url = f"{MUMU_API_URL}/api/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", get_request_timeout())
        resp = self.session.put(url, json=json_data, data=data, **kwargs)
        resp.raise_for_status()
        return resp.json()

if __name__ == "__main__":
    client = MumuClient()
    print("Client Auth Status:", client._check_auth())
