#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import secrets
import stat
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, quote, unquote, urlparse

import requests
import yaml
from tqdm import tqdm

APP_USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"
APP_OS = "android"
APP_OS_VERSION = "11"
APP_VERSION = "5.0.234"
CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"
AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"
AUTH_LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
AUTH_CALLBACK_PREFIX = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
REDIRECT_URI = AUTH_CALLBACK_PREFIX


class PixivAuthError(Exception):
    pass


def _bool(v: Optional[str]) -> Optional[bool]:
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    v = str(v).strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"无法识别的布尔值: {v}")


class PixivConfig:
    def __init__(self, path: str = "config.yaml"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
        self._ensure_defaults()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {}
        with self.path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _ensure_defaults(self):
        self.data.setdefault("pixiv", {})
        self.data.setdefault("monitor", {})
        pixiv = self.data["pixiv"]
        pixiv.setdefault("proxy", "")
        pixiv.setdefault("download_dir", "./downloads")
        pixiv.setdefault("r", False)
        pixiv.setdefault("auto_download", False)
        pixiv.setdefault("auth", {})
        pixiv["auth"].setdefault("access_token", "")
        pixiv["auth"].setdefault("refresh_token", "")
        pixiv["auth"].setdefault("expires_at", 0)
        pixiv["auth"].setdefault("user", {})

        monitor = self.data["monitor"]
        monitor.setdefault("interval", 3600)
        monitor.setdefault("notify", True)

    def save(self):
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            yaml.safe_dump(self.data, f, allow_unicode=True, sort_keys=False)
        tmp.replace(self.path)
        os.chmod(self.path, stat.S_IRUSR | stat.S_IWUSR)


class PixivAuth:
    def __init__(self, cfg: PixivConfig):
        self.cfg = cfg
        self.session = requests.Session()
        proxy = self.cfg.data["pixiv"].get("proxy")
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    @staticmethod
    def _code_verifier() -> str:
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")

    @staticmethod
    def _code_challenge(verifier: str) -> str:
        digest = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip("=")

    @staticmethod
    def _client_headers() -> Dict[str, str]:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        client_hash = hashlib.md5((now + CLIENT_SECRET).encode()).hexdigest()
        return {
            "User-Agent": APP_USER_AGENT,
            "App-OS": APP_OS,
            "App-OS-Version": APP_OS_VERSION,
            "App-Version": APP_VERSION,
            "Accept-Language": "zh-cn",
            "X-Client-Time": now,
            "X-Client-Hash": client_hash,
        }

    def begin_pkce(self) -> Dict[str, str]:
        verifier = self._code_verifier()
        challenge = self._code_challenge(verifier)
        state = secrets.token_urlsafe(24)
        redirect = quote(REDIRECT_URI, safe="")
        login_url = (
            f"{AUTH_LOGIN_URL}?code_challenge={challenge}"
            "&code_challenge_method=S256&client=pixiv-android"
            f"&redirect_uri={redirect}&state={state}"
        )
        return {"code_verifier": verifier, "state": state, "login_url": login_url}

    def exchange_code(self, code: str, code_verifier: str) -> Dict[str, Any]:
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "include_policy": "true",
        }
        r = self.session.post(
            AUTH_TOKEN_URL,
            data=payload,
            headers=self._client_headers(),
            timeout=30,
        )
        return self._handle_token_response(r)

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "include_policy": "true",
        }
        r = self.session.post(
            AUTH_TOKEN_URL,
            data=payload,
            headers=self._client_headers(),
            timeout=30,
        )
        return self._handle_token_response(r)

    def _handle_token_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            raise PixivAuthError(f"登录接口返回异常(HTTP {response.status_code})，请稍后重试")

        if response.status_code != 200:
            detail = data.get("error_description") or data.get("message") or str(data)
            hint = self._friendly_hint(detail)
            raise PixivAuthError(f"登录失败: {detail}\n提示: {hint}")

        if "access_token" not in data:
            detail = data.get("error_description") or json.dumps(data, ensure_ascii=False)
            hint = self._friendly_hint(detail)
            raise PixivAuthError(f"登录未返回 access_token: {detail}\n提示: {hint}")

        return data

    @staticmethod
    def _friendly_hint(detail: str) -> str:
        d = (detail or "").lower()
        if "captcha" in d or "recaptcha" in d:
            return "触发验证码，请在浏览器中完成验证后重新执行 login-url/login-submit。"
        if "2fa" in d or "two-factor" in d or "verification" in d or "otp" in d:
            return "账号开启了二次验证，请在 Pixiv 官方页面完成二次验证后重试。"
        if "rate" in d or "temporarily" in d or "risk" in d or "suspicious" in d:
            return "可能触发风控/频率限制，建议等待几分钟、更换网络或开启稳定代理后重试。"
        if "invalid_grant" in d or "authorization code" in d:
            return "授权码已过期、已被使用，或回调链接不完整。请重新执行 login-url，并在 5 分钟内提交最新回调链接。"
        return "请检查网络/代理是否可访问 Pixiv，再重试。"

    def persist_token(self, token_data: Dict[str, Any]):
        expires_in = int(token_data.get("expires_in", 3600))
        expires_at = int(time.time()) + max(0, expires_in - 30)
        user = token_data.get("user") or {}

        auth = self.cfg.data["pixiv"]["auth"]
        auth["access_token"] = token_data.get("access_token", "")
        auth["refresh_token"] = token_data.get("refresh_token", "")
        auth["expires_at"] = expires_at
        auth["user"] = {
            "id": user.get("id"),
            "name": user.get("name"),
            "account": user.get("account"),
        }
        # 兼容旧字段：不再使用 cookie，但保留为空避免误用
        self.cfg.data["pixiv"]["cookie"] = ""
        self.cfg.save()

    def clear_token(self):
        auth = self.cfg.data["pixiv"]["auth"]
        auth["access_token"] = ""
        auth["refresh_token"] = ""
        auth["expires_at"] = 0
        auth["user"] = {}
        self.cfg.data["pixiv"]["cookie"] = ""
        self.cfg.save()

    def status(self) -> Dict[str, Any]:
        auth = self.cfg.data["pixiv"]["auth"]
        now = int(time.time())
        ttl = int(auth.get("expires_at", 0)) - now
        return {
            "logged_in": bool(auth.get("refresh_token")),
            "has_access_token": bool(auth.get("access_token")),
            "expires_in": ttl,
            "user": auth.get("user") or {},
        }

    def get_valid_access_token(self) -> str:
        auth = self.cfg.data["pixiv"]["auth"]
        access_token = auth.get("access_token")
        refresh_token = auth.get("refresh_token")
        expires_at = int(auth.get("expires_at", 0))

        if access_token and expires_at > int(time.time()) + 10:
            return access_token

        if not refresh_token:
            raise PixivAuthError("尚未登录，请先执行: python pixiv.py login")

        token_data = self.refresh(refresh_token)
        self.persist_token(token_data)
        return token_data["access_token"]


class PixivAPI:
    def __init__(self, config_path: str = "config.yaml"):
        self.cfg = PixivConfig(config_path)
        self.auth = PixivAuth(self.cfg)

        self.download_dir = Path(self.cfg.data["pixiv"]["download_dir"])
        self.r = self.cfg.data["pixiv"]["r"]
        self.auto_download = self.cfg.data["pixiv"]["auto_download"]
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.runtime_cache: Dict[str, Any] = {"updated_at": 0, "items": []}
        self.cache_path = self.download_dir / "search_cache.json"

        self.session = requests.Session()
        proxy = self.cfg.data["pixiv"].get("proxy")
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def _app_headers(self) -> Dict[str, str]:
        token = self.auth.get_valid_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "User-Agent": APP_USER_AGENT,
            "Referer": "https://app-api.pixiv.net/",
            "Accept-Language": "zh-cn",
        }

    def _app_get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        r = self.session.get(url, params=params, headers=self._app_headers(), timeout=30)
        if r.status_code != 200:
            raise PixivAuthError(f"请求失败(HTTP {r.status_code}): {url}")
        data = r.json()
        if data.get("error"):
            message = data["error"].get("message") or str(data["error"])
            raise PixivAuthError(f"Pixiv API 错误: {message}")
        return data

    def _app_post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        r = self.session.post(url, data=data, headers=self._app_headers(), timeout=30)
        if r.status_code != 200:
            raise PixivAuthError(f"请求失败(HTTP {r.status_code}): {url}")
        out = r.json()
        if out.get("error"):
            message = out["error"].get("message") or str(out["error"])
            raise PixivAuthError(f"Pixiv API 错误: {message}")
        return out

    def _to_meta_from_rank(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(item.get("illust_id") or item.get("id") or ""),
            "title": item.get("title"),
            "author": item.get("user_name") or item.get("user") or item.get("userName"),
            "description": item.get("description"),
            "tags": item.get("tags") or [],
            "likes": item.get("yes_rank") or item.get("total_bookmarks") or item.get("bookmark_count"),
            "views": item.get("view_count") or item.get("total_view"),
            "updated_at": item.get("create_date") or item.get("date") or item.get("update_date"),
            "image_url": item.get("url") or item.get("image") or item.get("illust_url"),
            "source": "rank",
        }

    def _to_meta_from_search(self, item: Dict[str, Any]) -> Dict[str, Any]:
        image_urls = item.get("image_urls") or {}
        return {
            "id": str(item.get("id") or ""),
            "title": item.get("title"),
            "author": (item.get("user") or {}).get("name"),
            "description": item.get("caption"),
            "tags": [t.get("name") for t in (item.get("tags") or []) if isinstance(t, dict)],
            "likes": item.get("total_bookmarks"),
            "views": item.get("total_view"),
            "updated_at": item.get("create_date"),
            "image_url": image_urls.get("large") or image_urls.get("medium") or image_urls.get("square_medium"),
            "source": "search",
        }

    def _save_cache(self, items: list[Dict[str, Any]], source: str):
        payload = {
            "updated_at": int(time.time()),
            "source": source,
            "count": len(items),
            "items": items,
        }
        self.runtime_cache = payload
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_rank(self, rank_type="daily", page=1, date=None, r=False, lookback_days=7, download=False):
        mode_map = {
            "day": "daily",
            "week": "weekly",
            "month": "monthly",
            "daily": "daily",
            "weekly": "weekly",
            "monthly": "monthly",
            "rookie": "rookie",
            "original": "original",
        }
        rank_type = mode_map.get(rank_type, rank_type)

        base_url = "https://www.pixiv.net/ranking.php"
        dates = [date] if date else [
            (datetime.now() - timedelta(days=d)).strftime("%Y%m%d") for d in range(lookback_days + 1)
        ]

        public_session = requests.Session()
        proxy = self.cfg.data["pixiv"].get("proxy")
        if proxy:
            public_session.proxies = {"http": proxy, "https": proxy}
        public_session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Referer": "https://www.pixiv.net/",
            }
        )

        for target_date in dates:
            params = {
                "mode": rank_type,
                "content": "illust",
                "format": "json",
                "p": page,
                "date": target_date,
            }
            resp = public_session.get(base_url, params=params, timeout=20)
            if resp.status_code != 200:
                print(f"[{target_date}] 请求失败，状态码：{resp.status_code}")
                continue
            data = resp.json()
            illusts = data.get("contents", [])
            if not illusts:
                print(f"[{target_date}] 无可用榜单：{data.get('error') or '无数据'}")
                continue

            print(f"使用榜单日期: {target_date}，获取到{len(illusts)}个作品")
            metas = [self._to_meta_from_rank(i) for i in illusts]
            self._save_cache(metas, source=f"rank:{rank_type}:{target_date}")
            print(f"已缓存{len(metas)}条作品元信息到: {self.cache_path}")
            if download:
                for illust in illusts:
                    try:
                        self.download_illust(str(illust["illust_id"]))
                    except PixivAuthError:
                        print("下载需要登录，已跳过后续下载（榜单数据仍可用）")
                        break
            return illusts

        print(f"最近{lookback_days + 1}天都未获取到可用排行榜")
        return []

    def search(self, keyword, page=1, order="popular_desc", r=None, download=False):
        if r is None:
            r = self.r
        params = {
            "word": keyword,
            "sort": order,
            "search_target": "partial_match_for_tags",
            "offset": max(0, (page - 1) * 30),
        }
        if r:
            params["search_ai_type"] = 2

        data = self._app_get("https://app-api.pixiv.net/v1/search/illust", params=params)
        illusts = data.get("illusts", [])
        print(f"搜索到{len(illusts)}个作品")
        metas = [self._to_meta_from_search(i) for i in illusts]
        self._save_cache(metas, source=f"search:{keyword}:page{page}")
        print(f"已缓存{len(metas)}条作品元信息到: {self.cache_path}")
        if download:
            for illust in illusts:
                self.download_illust(str(illust["id"]))
        return illusts

    def get_user_illusts(self, user_id, page=1):
        params = {"user_id": user_id, "type": "illust", "offset": max(0, (page - 1) * 30)}
        data = self._app_get("https://app-api.pixiv.net/v1/user/illusts", params=params)
        ids = [str(i["id"]) for i in data.get("illusts", [])]
        print(f"画师{user_id}本页{len(ids)}个作品")
        return ids

    def get_illust_detail(self, illust_id):
        params = {"illust_id": illust_id}
        data = self._app_get("https://app-api.pixiv.net/v1/illust/detail", params=params)
        return data.get("illust")

    def download_illust(self, illust_id):
        illust = self.get_illust_detail(illust_id)
        if not illust:
            return False

        user_id = str(illust["user"]["id"])
        save_dir = self.download_dir / user_id
        save_dir.mkdir(parents=True, exist_ok=True)

        pages = illust.get("meta_pages") or []
        urls = []
        if pages:
            for p in pages:
                original = p.get("image_urls", {}).get("original")
                if original:
                    urls.append(original)
        else:
            original = illust.get("meta_single_page", {}).get("original_image_url")
            if original:
                urls.append(original)

        if not urls:
            print(f"作品{illust_id}无可下载原图")
            return False

        success_count = 0
        for idx, url in enumerate(urls):
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            save_path = save_dir / f"{illust_id}_p{idx}{ext}"
            if save_path.exists():
                print(f"作品{illust_id}_p{idx}已存在，跳过")
                success_count += 1
                continue

            headers = self._app_headers()
            headers["Referer"] = "https://app-api.pixiv.net/"
            try:
                resp = self.session.get(url, headers=headers, stream=True, timeout=40)
                if resp.status_code != 200:
                    print(f"下载{illust_id}_p{idx}失败，状态码：{resp.status_code}")
                    continue
                total_size = int(resp.headers.get("content-length", 0))
                with save_path.open("wb") as f, tqdm(
                    desc=f"下载{illust_id}_p{idx}",
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    leave=False,
                ) as pbar:
                    for chunk in resp.iter_content(chunk_size=1024 * 32):
                        if not chunk:
                            continue
                        written = f.write(chunk)
                        pbar.update(written)
                success_count += 1
            except Exception as e:
                print(f"下载{illust_id}_p{idx}出错：{e}")

        print(f"作品{illust_id}下载完成，共{len(urls)}张，成功{success_count}张")
        return success_count == len(urls)

    def like_illust(self, illust_id):
        self._app_post(
            "https://app-api.pixiv.net/v2/illust/bookmark/add",
            {"illust_id": illust_id, "restrict": "public"},
        )
        print(f"作品{illust_id}点赞/收藏成功")
        return True

    def follow_user(self, user_id):
        self._app_post(
            "https://app-api.pixiv.net/v1/user/follow/add",
            {"user_id": user_id, "restrict": "public"},
        )
        print(f"关注画师{user_id}成功")
        return True

    def monitor_user(self, user_id, interval=None):
        if interval is None:
            interval = self.cfg.data["monitor"]["interval"]
        print(f"开始监控画师{user_id}，检查间隔{interval}秒")
        existing = set(self.get_user_illusts(user_id))
        while True:
            time.sleep(interval)
            current = set(self.get_user_illusts(user_id))
            new_illusts = current - existing
            if new_illusts:
                print(f"画师{user_id}发布了{len(new_illusts)}个新作品！")
                for illust_id in sorted(new_illusts):
                    if self.auto_download:
                        self.download_illust(illust_id)
                    if self.cfg.data["monitor"].get("notify", True):
                        print(f"新作品ID：{illust_id}")
                existing = current


AUTH_SESSION_FILE = Path(".pixiv_auth_session.json")
AUTH_SESSION_TTL = 300


def _extract_callback_candidate(url: str) -> Optional[str]:
    if not url:
        return None
    if url.startswith(AUTH_CALLBACK_PREFIX) and "code=" in url:
        return url

    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "accounts.pixiv.net/post-redirect" in url:
        return_to = query.get("return_to", [""])[0]
        decoded = unquote(return_to) if return_to else ""
        if decoded.startswith(AUTH_CALLBACK_PREFIX) and "code=" in decoded:
            return decoded
    return None


def _short(v: str, keep: int = 6) -> str:
    if not v:
        return "<空>"
    if len(v) <= keep * 2:
        return v
    return f"{v[:keep]}...{v[-keep:]}"


def parse_callback_url(text: str) -> Dict[str, str]:
    text = text.strip()
    parsed = urlparse(text)

    if parsed.scheme == "pixiv":
        query = parse_qs(parsed.query)
        deep_code = query.get("code", [""])[0]
        deep_state = query.get("state", [""])[0]
        if not deep_code:
            raise PixivAuthError("检测到 pixiv:// 深链，但未找到 code 参数，请重新授权后再提交。")
        return {"code": deep_code, "state": deep_state, "raw": text}

    query = parse_qs(parsed.query)
    code = query.get("code", [""])[0]
    state = query.get("state", [""])[0]

    # 处理 Pixiv 中转页（常见白屏）
    if not code and "accounts.pixiv.net/post-redirect" in text:
        return_to = query.get("return_to", [""])[0]
        decoded = unquote(return_to) if return_to else ""
        if decoded:
            d_parsed = urlparse(decoded)
            d_query = parse_qs(d_parsed.query)
            d_code = d_query.get("code", [""])[0]
            if d_code:
                return {"code": d_code, "state": d_query.get("state", [""])[0], "raw": decoded}

        hint = (
            "你提交的是 Pixiv 中转页（post-redirect），还不是最终回调。\n"
            "请继续：\n"
            "1) 复制 return_to 参数\n"
            "2) URL 解码后在浏览器打开\n"
            "3) 把最终包含 code= 的回调链接提交给 login-submit"
        )
        if decoded:
            hint += f"\n\n可直接打开：\n{decoded}"
        raise PixivAuthError(hint)

    if not code:
        raise PixivAuthError(
            "回调链接无效：未找到 code 参数。\n"
            "请确保你提交的是授权完成后的最终地址（以 https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback 开头，并且包含 code=）。"
        )

    if parsed.scheme in {"http", "https"} and not text.startswith(AUTH_CALLBACK_PREFIX):
        raise PixivAuthError(
            "回调链接看起来不是 Pixiv 官方 OAuth 最终回调地址。\n"
            "请提交以 https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback 开头、且带 code= 的完整链接。"
        )

    return {"code": code, "state": state, "raw": text}


def _save_auth_session(data: Dict[str, Any]):
    payload = {
        "code_verifier": data.get("code_verifier", ""),
        "state": data.get("state", ""),
        "redirect_uri": REDIRECT_URI,
        "created_at": int(time.time()),
        "expires_at": int(time.time()) + AUTH_SESSION_TTL,
    }
    AUTH_SESSION_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    os.chmod(AUTH_SESSION_FILE, stat.S_IRUSR | stat.S_IWUSR)


def _load_auth_session() -> Dict[str, Any]:
    if not AUTH_SESSION_FILE.exists():
        raise PixivAuthError("未找到登录会话，请先执行: python pixiv.py login-url")
    try:
        data = json.loads(AUTH_SESSION_FILE.read_text(encoding="utf-8"))
    except Exception:
        raise PixivAuthError("登录会话文件损坏，请重新执行: python pixiv.py login-url")
    if int(data.get("expires_at", 0)) < int(time.time()):
        try:
            AUTH_SESSION_FILE.unlink()
        except Exception:
            pass
        raise PixivAuthError("登录会话已过期（授权码窗口 5 分钟），请重新执行: python pixiv.py login-url")
    return data


def _clear_auth_session():
    if AUTH_SESSION_FILE.exists():
        AUTH_SESSION_FILE.unlink()


def _cookie_help() -> str:
    return (
        "已按要求移除登录流程（login/login-url/login-submit/web-login）。\n"
        "请手动在浏览器登录 Pixiv 后，从 Cookie 中提取鉴权字段并写入 config.yaml。\n"
        "最低可用字段：pixiv.cookie: 'PHPSESSID=...;'\n"
        "示例：\n"
        "pixiv:\n"
        "  cookie: 'PHPSESSID=你的值;'\n"
    )


def cmd_login_url(cfg: PixivConfig):
    raise PixivAuthError(_cookie_help())


def cmd_login_submit(cfg: PixivConfig, callback_url: str):
    raise PixivAuthError(_cookie_help())


def cmd_login(cfg: PixivConfig):
    raise PixivAuthError(_cookie_help())


def cmd_web_login(
    cfg: PixivConfig,
    timeout: int = 300,
    headless: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    raise PixivAuthError(_cookie_help())


def cmd_logout(cfg: PixivConfig):
    auth = PixivAuth(cfg)
    auth.clear_token()
    print("已退出登录并清除本地凭据")


def cmd_status(cfg: PixivConfig):
    auth = PixivAuth(cfg)
    st = auth.status()
    if not st["logged_in"]:
        print("当前未登录")
        return
    user = st.get("user") or {}
    expires_in = st.get("expires_in", 0)
    print("当前已登录")
    print(f"用户: {user.get('name') or '-'} (@{user.get('account') or '-'})")
    if expires_in > 0:
        print(f"access_token 剩余有效期: {expires_in} 秒")
    else:
        print("access_token 已过期，将在下次请求时自动 refresh")


def main():
    parser = argparse.ArgumentParser(description="Pixiv 自动化工具")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("login", help="交互式 OAuth 登录 Pixiv（兼容旧命令）")
    web_login_parser = subparsers.add_parser("web-login", help="浏览器自动登录并自动提取回调（无需手动找 code）")
    web_login_parser.add_argument("--timeout", type=int, default=300, help="等待浏览器登录完成的超时秒数")
    web_login_parser.add_argument("--headless", action="store_true", help="使用无头浏览器（默认关闭，便于人工完成验证码/2FA）")
    web_login_parser.add_argument("--username", default=None, help="可选：自动填入 Pixiv 账号")
    web_login_parser.add_argument("--password", default=None, help="可选：自动填入密码（注意命令行历史泄露风险）")
    subparsers.add_parser("login-url", help="生成 OAuth 授权链接")
    login_submit_parser = subparsers.add_parser("login-submit", help="提交授权回调链接并完成登录")
    login_submit_parser.add_argument("--url", required=True, help="完整回调 URL（包含 code=）")
    subparsers.add_parser("logout", help="退出登录并清除本地凭据")
    subparsers.add_parser("status", help="查看登录状态")

    rank_parser = subparsers.add_parser("rank", help="获取排行榜")
    rank_parser.add_argument("--type", default="daily", choices=["day", "week", "month", "daily", "weekly", "monthly", "rookie", "original"])
    rank_parser.add_argument("--page", type=int, default=1)
    rank_parser.add_argument("--date", default=None, help="指定榜单日期，格式YYYYMMDD")
    rank_parser.add_argument("--lookback", type=int, default=7, help="未指定date时，最多向前回退天数")
    rank_parser.add_argument("--r", type=_bool, default=None, help="特殊模式开关")
    rank_parser.add_argument("--download", action="store_true", help="是否同时下载图片（默认只缓存元信息）")

    search_parser = subparsers.add_parser("search", help="搜索作品")
    search_parser.add_argument("--keyword", required=True)
    search_parser.add_argument("--page", type=int, default=1)
    search_parser.add_argument("--order", default="popular_desc", choices=["popular_desc", "date_desc", "date_asc"])
    search_parser.add_argument("--r", type=_bool, default=None, help="特殊模式开关")
    search_parser.add_argument("--download", action="store_true", help="是否同时下载图片（默认只缓存元信息）")

    cache_parser = subparsers.add_parser("cache", help="查看最近一次缓存的作品元信息")
    cache_parser.add_argument("--id", default=None, help="按作品ID过滤并输出详情")

    download_parser = subparsers.add_parser("download", help="下载作品")
    download_parser.add_argument("--id", required=True, help="作品ID")

    follow_parser = subparsers.add_parser("follow", help="关注画师")
    follow_parser.add_argument("--uid", required=True, help="画师ID")

    like_parser = subparsers.add_parser("like", help="点赞/收藏作品")
    like_parser.add_argument("--id", required=True, help="作品ID")

    monitor_parser = subparsers.add_parser("monitor", help="监控画师新作品")
    monitor_parser.add_argument("--uid", required=True, help="画师ID")
    monitor_parser.add_argument("--interval", type=int, default=None, help="检查间隔(秒)")

    args = parser.parse_args()
    cfg = PixivConfig(args.config)

    try:
        if args.command == "login":
            cmd_login(cfg)
            return
        if args.command == "web-login":
            cmd_web_login(
                cfg,
                timeout=args.timeout,
                headless=args.headless,
                username=args.username,
                password=args.password,
            )
            return
        if args.command == "login-url":
            cmd_login_url(cfg)
            return
        if args.command == "login-submit":
            cmd_login_submit(cfg, args.url)
            return
        if args.command == "logout":
            cmd_logout(cfg)
            return
        if args.command == "status":
            cmd_status(cfg)
            return
    except PixivAuthError as e:
        print(str(e))
        raise SystemExit(1)

    api = PixivAPI(args.config)
    try:
        if args.command == "rank":
            api.get_rank(rank_type=args.type, page=args.page, date=args.date, r=args.r, lookback_days=args.lookback, download=args.download)
        elif args.command == "search":
            api.search(args.keyword, args.page, args.order, args.r, download=args.download)
        elif args.command == "cache":
            if not api.cache_path.exists():
                print(f"暂无缓存，请先执行 rank/search。缓存路径: {api.cache_path}")
            else:
                payload = json.loads(api.cache_path.read_text(encoding="utf-8"))
                items = payload.get("items", [])
                if args.id:
                    items = [i for i in items if str(i.get("id")) == str(args.id)]
                print(json.dumps(items, ensure_ascii=False, indent=2))
        elif args.command == "download":
            api.download_illust(args.id)
        elif args.command == "follow":
            api.follow_user(args.uid)
        elif args.command == "like":
            api.like_illust(args.id)
        elif args.command == "monitor":
            api.monitor_user(args.uid, args.interval)
    except PixivAuthError as e:
        print(str(e))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
