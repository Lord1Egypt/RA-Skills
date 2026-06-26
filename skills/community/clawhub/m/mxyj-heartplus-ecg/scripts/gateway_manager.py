#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import platform
import stat
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from config_manager import ConfigManager
from phone_manager import PhoneManager
from errors import JsonArgumentParser, SkillError

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
BIN_DIR = SKILL_ROOT / "bin"
APP_DOWNLOAD_URL = "https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848"


@dataclass
class BinarySpec:
    platform_key: str
    url: str
    arch: str
    sha256: str = ""

    @property
    def filename(self) -> str:
        """统一本地文件名为 healthgateway（Windows下加 .exe）。"""
        return "healthgateway.exe" if self.platform_key.startswith("windows") else "healthgateway"


class GatewayManager:

    def __init__(self, session_key: str):
        self.config_manager = ConfigManager()
        self.phone_manager = PhoneManager(session_key=session_key)

    @staticmethod
    def detect_platform_key() -> str:
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":
            if machine in {"arm64", "aarch64"}:
                return "macos-arm64"
            return "macos-amd64"

        if system == "windows":
            if machine in {"arm64", "aarch64"}:
                return "windows-arm64"
            return "windows-amd64"

        if system == "linux":
            if machine in {"arm64", "aarch64"}:
                return "linux-arm64"
            return "linux-amd64"

        raise SkillError("当前设备暂不支持自动准备安全程序，请改在受支持系统执行",
                         {"system": system, "machine": machine})

    @staticmethod
    def _build_subprocess_env() -> dict[str, str]:
        env = dict(os.environ)
        base_path = env.get("PATH", "")
        system = platform.system().lower()
        if system == "darwin":
            required_paths = ["/usr/sbin", "/sbin", "/usr/bin", "/bin"]
        elif system == "linux":
            required_paths = ["/usr/bin", "/bin", "/usr/sbin", "/sbin"]
        else:
            required_paths = []
        segments = [seg for seg in base_path.split(os.pathsep) if seg]
        for p in required_paths:
            if p not in segments:
                segments.append(p)
        env["PATH"] = os.pathsep.join(segments)
        return env

    @staticmethod
    def _is_executable(path: Path) -> bool:
        if not (path.exists() and path.is_file() and path.stat().st_size > 0):
            return False
        if platform.system().lower() == "windows":
            return True
        return os.access(path, os.X_OK)

    @staticmethod
    def _health_check(path: Path) -> bool:
        try:
            result = subprocess.run(
                [str(path), "--help"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
                env=GatewayManager._build_subprocess_env(),
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, OSError):
            return False

    @staticmethod
    def _sha256(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest().lower()

    @staticmethod
    def _normalize_payload(payload: dict, data_default=None):
        if "code" not in payload or "message" not in payload:
            raise SkillError("安全校验返回不完整，请稍后重试", {"payload_keys": list(payload.keys())})
        return {
            "code": str(payload["code"]),
            "message": str(payload["message"]),
            "data": payload.get("data", data_default),
        }

    def _ensure_phone(self) -> str:
        return self.phone_manager.get_phone()

    def _parse_download_list(self) -> dict[str, BinarySpec]:
        downloads = self.config_manager.get("gateway_downloads", {})

        if not downloads:
            raise SkillError("安全程序下载配置缺失，请更新配置后重试", {"path": str(self.config_manager.config_file)})

        specs: dict[str, BinarySpec] = {}
        for key, data in downloads.items():
            if not isinstance(data, dict):
                continue

            url = data.get("url", "")
            if not url:
                continue

            arch = data.get("arch", "")
            spec = BinarySpec(
                platform_key=key,
                url=url,
                arch=arch,
                sha256=data.get("sha256", ""),
            )
            specs[key] = spec
            if arch:
                specs[arch] = spec

        if not specs:
            raise SkillError("安全程序下载配置无可用项，请检查配置后重试",
                             {"path": str(self.config_manager.config_file)})

        return specs

    def _download_binary(self, spec: BinarySpec) -> Path:
        if not spec.url:
            raise SkillError(
                "安全程序下载地址缺失，请检查配置后重试",
                {"platform": spec.platform_key, "url": spec.url},
            )

        BIN_DIR.mkdir(parents=True, exist_ok=True)
        target = BIN_DIR / spec.filename

        try:
            with urllib.request.urlopen(spec.url, timeout=30) as resp:
                data = resp.read()
            target.write_bytes(data)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise SkillError("安全程序下载失败，请检查网络后重试", {"url": spec.url, "reason": str(e)})

        if spec.sha256:
            actual = self._sha256(target)
            if actual != spec.sha256.lower():
                raise SkillError(
                    "下载文件校验未通过，请重试下载",
                    {"expected": spec.sha256, "actual": actual, "file": str(target)},
                )

        if platform.system().lower() != "windows":
            mode = target.stat().st_mode
            target.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        return target

    def _is_binary_valid(self, target_path: Path, spec: BinarySpec) -> bool:
        if not self._is_executable(target_path):
            return False
        if spec.sha256:
            current_hash = self._sha256(target_path)
            if current_hash != spec.sha256.lower():
                return False
        return self._health_check(target_path)

    def ensure_binary(self, auto_download: bool = True) -> Path:
        platform_key = self.detect_platform_key()
        specs = self._parse_download_list()

        spec = specs.get(platform_key)
        if not spec:
            raise SkillError("当前系统缺少可用的安全程序配置，请更新下载清单后重试", {"platform": platform_key})

        target_path = BIN_DIR / spec.filename

        if target_path.exists() and self._is_binary_valid(target_path, spec):
            return target_path

        if not auto_download:
            raise SkillError("安全程序不可用，请先执行 ensure 重新准备", {"path": str(target_path)})

        target_path = self._download_binary(spec)

        if not self._is_binary_valid(target_path, spec):
            raise SkillError("安全程序自检失败，请重新执行 ensure", {"path": str(target_path)})

        return target_path

    def run(self, subcommand: str, args: list[str], timeout: int = 20) -> dict:
        bin_path = self.ensure_binary(auto_download=True)
        cmd = [str(bin_path), subcommand, *args]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                env=self._build_subprocess_env(),
            )
        except (subprocess.TimeoutExpired, OSError, ValueError) as e:
            raise SkillError("安全校验执行失败，请稍后重试", {"reason": str(e)})

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if not stdout:
            raise SkillError("安全校验无返回，请稍后重试")

        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as e:
            raise SkillError("安全校验返回无法解析，请稍后重试", {"reason": str(e)})

        if result.returncode != 0:
            if isinstance(payload, dict):
                payload_code = str(payload.get("code", ""))
                if payload_code in {"1002", "1003"}:
                    return payload
                if payload_code == "2001":
                    error_msg = str(payload.get("message", ""))
                    if "verify cloud error" in error_msg:
                        raise SkillError(
                            "授权校验失败，请确认用户已在心脏+APP完成授权后重试。",
                            {
                                "suggestion": f"先确认用户是否完成APP授权；如未完成可重新发送授权通知，完成后再重试校验。如需先下载并登录心脏+APP，请使用：{APP_DOWNLOAD_URL}"}
                        )
            raise SkillError("安全校验执行未完成，请稍后重试", {"next_action": "ask_send_authorize_notify"})

        if not isinstance(payload, dict):
            raise SkillError("安全校验返回结构异常，请稍后重试")

        return payload

    # 校验加密因子是否有效
    def check_factory(self):
        phone = self._ensure_phone()
        check_json = json.dumps({"action": "check_factory"}, ensure_ascii=False, separators=(",", ":"))

        if self.config_manager.is_dev():
            payload = self.run("encry", [f"--phone={phone}", f"--json={check_json}", "--test"])
        else:
            payload = self.run("encry", [f"--phone={phone}", f"--json={check_json}"])

        return self._normalize_payload(payload, data_default={})

    # 获取加密因子
    def verify(self, code: str):
        phone = self._ensure_phone()

        if self.config_manager.is_dev():
            payload = self.run("verify", [f"--phone={phone}", f"--code={code}", "--test"])
        else:
            payload = self.run("verify", [f"--phone={phone}", f"--code={code}"])

        return self._normalize_payload(payload)

    # 加密
    def encry(self, biz_json: str):
        phone = self._ensure_phone()

        if self.config_manager.is_dev():
            payload = self.run("encry", [f"--phone={phone}", f"--json={biz_json}", "--test"])
        else:
            payload = self.run("encry", [f"--phone={phone}", f"--json={biz_json}"])

        return self._normalize_payload(payload)

    # 解密
    def decry(self, biz_body: str):
        phone = self._ensure_phone()

        if self.config_manager.is_dev():
            payload = self.run("decry", [f"--phone={phone}", f"--body={biz_body}", "--test"])
        else:
            payload = self.run("decry", [f"--phone={phone}", f"--body={biz_body}"])

        return self._normalize_payload(payload)


if __name__ == "__main__":
    try:
        parser = JsonArgumentParser()
        parser.add_argument("--action", choices=["platform", "ensure", "check_factory", "verify"], required=True)
        parser.add_argument("--code")
        parser.add_argument("--session-key", required=True,
                            help="Session key from current conversation context, e.g. agent:main:main")
        args = parser.parse_args()

        gm = GatewayManager(session_key=args.session_key)

        if args.action == "platform":
            print(gm.detect_platform_key())
        elif args.action == "ensure":
            print(gm.ensure_binary())
        elif args.action == "check_factory":
            result = gm.check_factory()

            if result["code"] == "0":
                print(True)
            elif result["code"] in ["1002", "1003"]:
                print(False)
            else:
                raise SkillError("登录校验状态检查失败，请先发起APP授权并重新校验",
                                 {"code": result["code"], "message": result["message"]})
        elif args.action == "verify":
            if not args.code:
                raise SkillError("请先提供授权码，再执行 verify")

            result = gm.verify(args.code)
            if result["code"] == "0":
                print(True)
            elif result["code"] in ["1002", "1003"]:
                print(False)
            else:
                raise SkillError("授权校验未完成，请确认APP授权状态后重试",
                                 {"code": result["code"], "message": result["message"]})
        else:
            raise SkillError("当前操作不受支持，请使用 platform/ensure/check_factory/verify")
    except SkillError as e:
        print(json.dumps(e.to_dict(), ensure_ascii=False))
        raise SystemExit(1)
    except Exception as e:
        wrapped = SkillError("安全校验流程失败，请稍后重试", {"error": str(e)})
        print(json.dumps(wrapped.to_dict(), ensure_ascii=False))
        raise SystemExit(1)
