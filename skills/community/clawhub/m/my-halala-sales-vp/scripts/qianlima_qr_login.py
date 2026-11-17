#!/usr/bin/env python3
"""在服务器生成乙方宝微信登录二维码，并在扫码后更新本地授权。"""

from __future__ import annotations

import argparse
import os
import stat
import tempfile
import time
from pathlib import Path
from typing import Any

from curl_cffi import requests


BASE_URL = "https://qiye.qianlima.com"
LOGIN_URL = f"{BASE_URL}/yfbsite/a/login"
QR_API_URL = f"{BASE_URL}/yfbsite/yfbLogin/loginQrCode"
STATUS_API_URL = f"{BASE_URL}/yfbsite/yfbLogin/checkLoginStatus"
APP_URL = f"{BASE_URL}/new_qd_yfbsite/"


class QrLoginError(RuntimeError):
    pass


def update_env(path: Path, updates: dict[str, str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    pending = dict(updates)
    output: list[str] = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line else ""
        if key in pending:
            output.append(f"{key}={pending.pop(key)}")
        else:
            output.append(line)
    if output and pending:
        output.append("")
    output.extend(f"{key}={value}" for key, value in pending.items())

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".env.", dir=path.parent, text=True
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            file.write("\n".join(output).rstrip() + "\n")
        os.chmod(temporary_path, stat.S_IRUSR | stat.S_IWUSR)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _extract_admin_token(session: requests.Session) -> str:
    for name, value in session.cookies.items():
        if name.lower() == "admin-token" and value:
            return str(value).strip()
    return ""


def qr_login(env_path: Path, qr_path: Path, timeout: int) -> None:
    qr_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.Session() as session:
        login_page = session.get(LOGIN_URL, impersonate="chrome", timeout=60)
        login_page.raise_for_status()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": LOGIN_URL,
            "X-Requested-With": "XMLHttpRequest",
        }
        qr_response = session.get(
            QR_API_URL,
            params={"sourceMark": "", "isFromSeo": ""},
            headers=headers,
            impersonate="chrome",
            timeout=60,
        )
        qr_response.raise_for_status()
        qr_data: dict[str, Any] = (qr_response.json().get("data") or {})
        ticket = str(qr_data.get("ticket") or "")
        scan_id = str(qr_data.get("scanId") or "")
        if not ticket or not scan_id:
            raise QrLoginError("二维码接口没有返回 ticket/scanId")

        image_response = session.get(
            "https://mp.weixin.qq.com/cgi-bin/showqrcode",
            params={"ticket": ticket},
            impersonate="chrome",
            timeout=60,
        )
        image_response.raise_for_status()
        if not image_response.content:
            raise QrLoginError("二维码图片为空")
        qr_path.write_bytes(image_response.content)
        os.chmod(qr_path, stat.S_IRUSR | stat.S_IWUSR)
        print(f"[二维码] 已生成 {qr_path.resolve()}")
        print(f"[二维码] 等待扫码，最长 {timeout} 秒")

        deadline = time.monotonic() + timeout
        login_data: dict[str, Any] | None = None
        while time.monotonic() < deadline:
            status_response = session.get(
                STATUS_API_URL,
                params={
                    "scanId": scan_id,
                    "sourceMark": "",
                    "isFromSeo": "",
                },
                headers=headers,
                impersonate="chrome",
                timeout=30,
            )
            status_response.raise_for_status()
            data = status_response.json().get("data")
            if data:
                login_data = data
                break
            time.sleep(1)
        if not login_data:
            raise QrLoginError("二维码等待超时，请重新生成")

        uid = str(login_data.get("uid") or "")
        openid = str(login_data.get("openid") or "")
        if not uid or not openid:
            raise QrLoginError("扫码状态缺少 uid/openid")
        login_response = session.post(
            LOGIN_URL,
            data={
                "uid": uid,
                "openid": openid,
                "hashUrlQr": "",
                "sourcefromQr": "",
            },
            headers={"Referer": LOGIN_URL},
            impersonate="chrome",
            timeout=60,
            allow_redirects=True,
        )
        login_response.raise_for_status()
        session.get(APP_URL, impersonate="chrome", timeout=60).raise_for_status()
        token = _extract_admin_token(session)
        if not token:
            raise QrLoginError("扫码成功，但登录 Session 中没有 Admin-Token")

        update_env(
            env_path,
            {"QIANLIMA_TOKEN": token, "QIANLIMA_OPENID": openid},
        )
        qr_path.unlink(missing_ok=True)
        print("[登录] 新授权已安全写入 .env，二维码已删除")


def _default_workdir() -> Path:
    raw = os.environ.get("QIANLIMA_WORKDIR", "").strip()
    if raw:
        return Path(raw).expanduser()
    return Path.cwd()


def main() -> int:
    parser = argparse.ArgumentParser(description="乙方宝微信扫码登录")
    workdir = _default_workdir()
    env_default = os.environ.get("QIANLIMA_ENV", "").strip() or str(workdir / ".env")
    parser.add_argument(
        "--env",
        default=env_default,
        help="写入 Token 的 .env 路径（默认 $QIANLIMA_WORKDIR/.env）",
    )
    parser.add_argument(
        "--qr",
        default=str(workdir / "runtime" / "login_qrcode.jpg"),
        help="二维码图片输出路径",
    )
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    if args.timeout < 30:
        parser.error("--timeout 不能少于 30 秒")
    try:
        qr_login(Path(args.env), Path(args.qr), args.timeout)
        return 0
    except (QrLoginError, OSError) as error:
        print(f"[登录失败] {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
