#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent / "openclaw-openai-accounts.py"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def make_jwt(email: str, account_id: str, user_id: str, plan: str = "team") -> str:
    import base64

    def b64(data: object) -> str:
        raw = json.dumps(data, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    header = {"alg": "none", "typ": "JWT"}
    payload = {
        "https://api.openai.com/profile": {"email": email, "email_verified": True},
        "https://api.openai.com/auth": {
            "chatgpt_account_id": account_id,
            "user_id": user_id,
            "chatgpt_plan_type": plan,
        },
    }
    return f"{b64(header)}.{b64(payload)}.sig"


class TestEnv:
    def __init__(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="openclaw-openai-accounts-test-"))
        self.state = self.root / "state"
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.root / "mock-openclaw.log"
        self.codex_log_path = self.root / "mock-codex.log"
        self.mock_rate_limits_path = self.root / "mock-rate-limits.json"
        self._install_mock_openclaw()
        self._install_mock_codex()
        self._start_mock_usage_server()

    def cleanup(self) -> None:
        try:
            self.server.shutdown()
            self.server.server_close()
        except Exception:
            pass
        shutil.rmtree(self.root, ignore_errors=True)

    def env(self, *, primary_agent: str = "main") -> dict[str, str]:
        env = os.environ.copy()
        env["OPENCLAW_HOME"] = str(self.state)
        env["OPENCLAW_PRIMARY_AGENT"] = primary_agent
        env["HOME"] = str(self.root)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env.get('PATH', '')}"
        env["MOCK_CODEX_LOG"] = str(self.codex_log_path)
        env["MOCK_CODEX_RATE_LIMITS_FILE"] = str(self.mock_rate_limits_path)
        env["OPENCLAW_CODEX_USAGE_URL"] = self.mock_usage_url
        return env

    def _install_mock_openclaw(self) -> None:
        script = self.bin_dir / "openclaw"
        script.write_text(
            "#!/usr/bin/env bash\n"
            "echo \"$@\" >> \"${MOCK_OPENCLAW_LOG:?}\"\n"
            "if [ \"$1 $2\" = \"models set\" ]; then\n"
            "  exit 0\n"
            "fi\n"
            "if [ \"$1 $2 $3 $4\" = \"models auth login --provider\" ]; then\n"
            "  echo 'mock auth login not implemented in regression test' >&2\n"
            "  exit 1\n"
            "fi\n"
            "exit 0\n"
        )
        script.chmod(0o755)

    def _install_mock_codex(self) -> None:
        script = self.bin_dir / "codex"
        script.write_text(
            "#!/usr/bin/env bash\n"
            "echo \"$@\" >> \"${MOCK_CODEX_LOG:?}\"\n"
            "echo OK\n"
        )
        script.chmod(0o755)

    def _start_mock_usage_server(self) -> None:
        rate_limits_path = self.mock_rate_limits_path

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/usage':
                    self.send_response(404)
                    self.end_headers()
                    return
                auth = self.headers.get('Authorization', '')
                token = auth.replace('Bearer ', '', 1) if auth.startswith('Bearer ') else None
                email = None
                if token and token.count('.') >= 2:
                    try:
                        payload = token.split('.')[1]
                        payload += '=' * (-len(payload) % 4)
                        data = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
                        email = ((data.get('https://api.openai.com/profile') or {}).get('email'))
                    except Exception:
                        email = None
                payload = json.loads(rate_limits_path.read_text()) if rate_limits_path.exists() else {}
                by_email = payload.get('by_email') or {}
                rate_limits = by_email.get(email) or payload.get('default') or {}
                body = {
                    'plan_type': 'team',
                    'rate_limit': {
                        'primary_window': {
                            'used_percent': (rate_limits.get('primary') or {}).get('used_percent'),
                            'limit_window_seconds': ((rate_limits.get('primary') or {}).get('window_minutes') or 300) * 60,
                            'reset_at': (rate_limits.get('primary') or {}).get('resets_at'),
                        },
                        'secondary_window': {
                            'used_percent': (rate_limits.get('secondary') or {}).get('used_percent'),
                            'limit_window_seconds': ((rate_limits.get('secondary') or {}).get('window_minutes') or 10080) * 60,
                            'reset_at': (rate_limits.get('secondary') or {}).get('resets_at'),
                        }
                    }
                }
                raw = json.dumps(body).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def log_message(self, format, *args):
                return

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.mock_usage_url = f'http://127.0.0.1:{self.server.server_address[1]}/usage'
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def run(self, *args: str, primary_agent: str = "main") -> subprocess.CompletedProcess[str]:
        env = self.env(primary_agent=primary_agent)
        env["MOCK_OPENCLAW_LOG"] = str(self.log_path)
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

    def build_fixture(self) -> None:
        alpha = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("alpha@example.com", "acct-alpha", "user-alpha"),
            "refresh": "refresh-alpha",
            "accountId": "acct-alpha",
            "expires": 2_000_000_000_000,
        }
        beta = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("beta@example.com", "acct-beta", "user-beta"),
            "refresh": "refresh-beta",
            "accountId": "acct-beta",
            "expires": 2_000_000_000_000,
        }
        gamma = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("gamma@example.com", "acct-gamma", "user-gamma"),
            "refresh": "refresh-gamma",
            "accountId": "acct-gamma",
            "expires": 2_000_000_000_000,
        }

        write_json(
            self.state / "openclaw.json",
            {
                "auth": {
                    "profiles": {
                        "openai-codex:default": {"provider": "openai-codex", "mode": "oauth"},
                        "openai-codex:alpha@example.com": {
                            "provider": "openai-codex",
                            "mode": "oauth",
                            "email": "alpha@example.com",
                        },
                        "openai-codex:beta@example.com": {
                            "provider": "openai-codex",
                            "mode": "oauth",
                            "email": "beta@example.com",
                        },
                        "openai-codex:gamma@example.com": {
                            "provider": "openai-codex",
                            "mode": "oauth",
                            "email": "gamma@example.com",
                        },
                    },
                    "order": {
                        "openai-codex": [
                            "openai-codex:default",
                            "openai-codex:gamma@example.com",
                            "openai-codex:beta@example.com",
                            "openai-codex:alpha@example.com",
                        ]
                    },
                },
                "agents": {
                    "list": [
                        {"id": "main"},
                        {"id": "worker"},
                    ]
                },
            },
        )

        main_store = {
            "version": 1,
            "profiles": {
                "openai-codex:default": beta,
                "openai-codex:alpha@example.com": alpha,
                "openai-codex:beta@example.com": beta,
                "openai-codex:gamma@example.com": gamma,
            },
            "lastGood": {"openai-codex": "openai-codex:gamma@example.com"},
            "usageStats": {
                "openai-codex:default": {"lastUsed": 111, "errorCount": 1, "lastFailureAt": None},
                "openai-codex:gamma@example.com": {"lastUsed": 222, "errorCount": 0, "lastFailureAt": None},
            },
        }
        write_json(self.state / "agents" / "main" / "agent" / "auth-profiles.json", main_store)
        write_json(self.state / "agents" / "worker" / "agent" / "auth-profiles.json", main_store)

        accounts_dir = self.state / "openai-codex-accounts"
        profiles_dir = accounts_dir / "profiles"
        write_json(profiles_dir / "account1.json", alpha)
        write_json(profiles_dir / "account2.json", beta)
        write_json(profiles_dir / "account3.json", gamma)
        write_json(
            accounts_dir / "accounts.json",
            {
                "accounts": {
                    "account1": {
                        "email": "alpha@example.com",
                        "accountId": "acct-alpha",
                        "snapshot": str(profiles_dir / "account1.json"),
                        "savedAt": 100,
                        "profileId": "openai-codex:default",
                    },
                    "account2": {
                        "email": "beta@example.com",
                        "accountId": "acct-beta",
                        "snapshot": str(profiles_dir / "account2.json"),
                        "savedAt": 200,
                        "profileId": "openai-codex:default",
                    },
                    "account3": {
                        "email": "gamma@example.com",
                        "accountId": "acct-gamma",
                        "snapshot": str(profiles_dir / "account3.json"),
                        "savedAt": 300,
                        "profileId": "openai-codex:default",
                    },
                },
                "active": "account1",
            },
        )

        write_json(
            profiles_dir / ".account1.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 30.0, "window_minutes": 300},
                    "secondary": {"used_percent": 10.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        write_json(
            profiles_dir / ".account2.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 0.0, "window_minutes": 300},
                    "secondary": {"used_percent": 0.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        write_json(
            profiles_dir / ".account3.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 95.0, "window_minutes": 300},
                    "secondary": {"used_percent": 20.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        write_json(
            self.mock_rate_limits_path,
            {
                "by_email": {
                    "alpha@example.com": {
                        "primary": {"used_percent": 83.0, "window_minutes": 300, "resets_at": 1234567801},
                        "secondary": {"used_percent": 72.0, "window_minutes": 10080, "resets_at": 2234567801},
                    },
                    "beta@example.com": {
                        "primary": {"used_percent": 61.0, "window_minutes": 300, "resets_at": 1234567890},
                        "secondary": {"used_percent": 41.0, "window_minutes": 10080, "resets_at": 2234567890},
                    },
                    "gamma@example.com": {
                        "primary": {"used_percent": 95.0, "window_minutes": 300, "resets_at": 1234567999},
                        "secondary": {"used_percent": 20.0, "window_minutes": 10080, "resets_at": 2234567999},
                    },
                },
                "default": {
                    "primary": {"used_percent": 88.0, "window_minutes": 300, "resets_at": 1234567000},
                    "secondary": {"used_percent": 55.0, "window_minutes": 10080, "resets_at": 2234567000},
                },
            },
        )


class Failure(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def test_metadata_migration_and_active_detection() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        result = env.run("list", "--json")
        payload = json.loads(result.stdout)
        meta = read_json(env.state / "openclaw.json")
        accounts = read_json(env.state / "openai-codex-accounts" / "accounts.json")

        require(payload["active"] == "account2", "active account should resolve from live default token")
        migrated = {name: info["profileId"] for name, info in accounts["accounts"].items()}
        require(
            migrated == {
                "account1": "openai-codex:alpha@example.com",
                "account2": "openai-codex:beta@example.com",
                "account3": "openai-codex:gamma@example.com",
            },
            f"unexpected migrated profile ids: {migrated}",
        )
        require(
            meta["auth"]["order"]["openai-codex"][0] == "openai-codex:default",
            "config order should still keep default first",
        )
    finally:
        env.cleanup()


def test_use_preserves_metadata_and_syncs_agents() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        before_main = read_json(env.state / "agents" / "main" / "agent" / "auth-profiles.json")
        before_worker = read_json(env.state / "agents" / "worker" / "agent" / "auth-profiles.json")
        before_stats = before_main["usageStats"]
        before_last_good = before_main["lastGood"]

        result = env.run("use", "account1")
        main_store = read_json(env.state / "agents" / "main" / "agent" / "auth-profiles.json")
        worker_store = read_json(env.state / "agents" / "worker" / "agent" / "auth-profiles.json")
        config = read_json(env.state / "openclaw.json")
        meta = read_json(env.state / "openai-codex-accounts" / "accounts.json")
        alpha_access = read_json(env.state / "openai-codex-accounts" / "profiles" / "account1.json")["access"]

        require(main_store["profiles"]["openai-codex:default"]["access"] == alpha_access, "main default profile should switch to account1 token")
        require(main_store["profiles"]["openai-codex:alpha@example.com"]["access"] == alpha_access, "main named profile should be upserted with account1 token")
        require(worker_store["profiles"]["openai-codex:default"]["access"] == alpha_access, "worker default profile should sync to account1 token")
        require(main_store["usageStats"] == before_stats, "usageStats should be preserved")
        require(main_store["lastGood"] == before_last_good, "lastGood should be preserved")
        require(before_worker["usageStats"] == worker_store["usageStats"], "worker usageStats should be preserved")
        require(config["auth"]["order"]["openai-codex"][:2] == ["openai-codex:default", "openai-codex:alpha@example.com"], "config auth order should keep default first and selected email profile second")
        require(meta["active"] == "account1", "meta active should update after use")
        require("email_profile=openai-codex:alpha@example.com" in result.stdout, "use output should expose selected email profile")
    finally:
        env.cleanup()


def test_auto_switches_best_account_and_keep_current() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        meta_path = env.state / "openai-codex-accounts" / "accounts.json"
        meta = read_json(meta_path)
        meta["active"] = "account3"
        write_json(meta_path, meta)

        # Simulate a real live switch to account3 by rewriting the live default token,
        # not just meta.active. The script should trust runtime reality over metadata.
        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        gamma_profile = main_store["profiles"]["openai-codex:gamma@example.com"]
        main_store["profiles"]["openai-codex:default"] = gamma_profile
        worker_store["profiles"]["openai-codex:default"] = gamma_profile
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        switched = env.run("auto", "--json")
        switched_payload = json.loads(switched.stdout)
        main_store = read_json(main_store_path)
        beta_access = read_json(env.state / "openai-codex-accounts" / "profiles" / "account2.json")["access"]
        meta_after = read_json(meta_path)
        log_lines = env.log_path.read_text().splitlines()

        require(switched_payload["mode"] == "account", f"expected auto switch, got {switched_payload}")
        require(switched_payload["activeAccount"] == "account2", "auto should choose best healthy account")
        require(main_store["profiles"]["openai-codex:default"]["access"] == beta_access, "auto switch should rewrite default token to best account")
        require(meta_after["active"] == "account2", "meta active should update after auto switch")
        require(any(line == "models set openai-codex/gpt-5.4" for line in log_lines), "auto/account path should call openclaw models set")

        env.log_path.write_text("")
        kept = env.run("auto", "--json")
        kept_payload = json.loads(kept.stdout)
        keep_log_lines = [line for line in env.log_path.read_text().splitlines() if line]
        require(kept_payload["mode"] == "keep-current", f"expected keep-current, got {kept_payload}")
        require(kept_payload["activeAccount"] == "account2", "keep-current should report current best account")
        require(keep_log_lines == ["models set openai-codex/gpt-5.4"], f"keep-current should only set model once, got {keep_log_lines}")
    finally:
        env.cleanup()


def test_probe_forces_fresh_quota_refresh() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        before = read_json(env.state / "openai-codex-accounts" / "profiles" / ".account2.quota.json")
        require(before["rate_limits"]["primary"]["used_percent"] == 0.0, "fixture should start with stale cached quota")

        result = env.run("status", "--probe")
        payload = json.loads(result.stdout)
        after = read_json(env.state / "openai-codex-accounts" / "profiles" / ".account2.quota.json")
        require(payload.get("fiveHourUsedPct") == 61.0, f"status --probe should use fresh 5h quota, got {payload}")
        require(payload.get("weeklyUsedPct") == 41.0, f"status --probe should use fresh weekly quota, got {payload}")
        require(after["rate_limits"]["primary"]["used_percent"] == 61.0, "probe should refresh cached primary quota")
        require(after["rate_limits"]["secondary"]["used_percent"] == 41.0, "probe should refresh cached secondary quota")
        require((after.get("health") or {}).get("reason") == "live-usage-api", f"probe should use official usage API, got {after.get('health')}")
        require((not env.codex_log_path.exists()) or env.codex_log_path.read_text().strip() == '', 'probe should not invoke codex CLI anymore')
        require(not (env.root / '.codex' / 'auth.json').exists(), 'probe should not touch the real HOME .codex/auth.json')
    finally:
        env.cleanup()


def test_auto_blocks_switch_when_recent_sessions_are_active() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        write_json(
            env.state / "agents" / "main" / "sessions" / "sessions.json",
            {
                "agent:main:main": {
                    "sessionId": "session-main",
                    "updatedAt": int(time.time() * 1000),
                    "model": "openai-codex/gpt-5.4",
                }
            },
        )
        write_json(
            env.state / "openai-codex-accounts" / "profiles" / ".account2.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 10.0, "window_minutes": 300},
                    "secondary": {"used_percent": 10.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        write_json(
            env.state / "openai-codex-accounts" / "profiles" / ".account3.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 85.0, "window_minutes": 300},
                    "secondary": {"used_percent": 20.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        meta_path = env.state / "openai-codex-accounts" / "accounts.json"
        meta = read_json(meta_path)
        meta["active"] = "account3"
        write_json(meta_path, meta)

        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        gamma_profile = main_store["profiles"]["openai-codex:gamma@example.com"]
        main_store["profiles"]["openai-codex:default"] = gamma_profile
        worker_store["profiles"]["openai-codex:default"] = gamma_profile
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        blocked = env.run("auto", "--json", "--inactive-minutes", "15", "--five-hour-hard-switch-at", "99")
        payload = json.loads(blocked.stdout)
        meta_after = read_json(meta_path)
        main_store_after = read_json(main_store_path)
        require(payload["mode"] == "blocked-active-sessions", f"expected switch to be blocked by active sessions, got {payload}")
        require(payload["activeAccount"] == "account3", f"blocked result should preserve current active account, got {payload}")
        require(payload["activeSessionCount"] >= 1, f"blocked result should report active sessions, got {payload}")
        require(meta_after["active"] == "account3", f"meta active should remain unchanged when blocked, got {meta_after}")
        require(main_store_after["profiles"]["openai-codex:default"]["access"] == gamma_profile["access"], "blocked switch must not rewrite live default token")
    finally:
        env.cleanup()


def test_auto_forces_immediate_switch_at_hard_five_hour_threshold() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        write_json(
            env.state / "agents" / "main" / "sessions" / "sessions.json",
            {
                "agent:main:main": {
                    "sessionId": "session-main",
                    "updatedAt": int(time.time() * 1000),
                    "model": "openai-codex/gpt-5.4",
                }
            },
        )
        write_json(
            env.state / "openai-codex-accounts" / "profiles" / ".account2.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 10.0, "window_minutes": 300},
                    "secondary": {"used_percent": 10.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        write_json(
            env.state / "openai-codex-accounts" / "profiles" / ".account3.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 96.0, "window_minutes": 300},
                    "secondary": {"used_percent": 20.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        meta_path = env.state / "openai-codex-accounts" / "accounts.json"
        meta = read_json(meta_path)
        meta["active"] = "account3"
        write_json(meta_path, meta)

        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        gamma_profile = main_store["profiles"]["openai-codex:gamma@example.com"]
        beta_profile = main_store["profiles"]["openai-codex:beta@example.com"]
        main_store["profiles"]["openai-codex:default"] = gamma_profile
        worker_store["profiles"]["openai-codex:default"] = gamma_profile
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        forced = env.run("auto", "--json", "--inactive-minutes", "3")
        payload = json.loads(forced.stdout)
        meta_after = read_json(meta_path)
        main_store_after = read_json(main_store_path)
        require(payload["mode"] == "account", f"hard threshold should force account switch, got {payload}")
        require(payload["activeAccount"] == "account2", f"hard threshold should switch to best healthy account, got {payload}")
        require(payload["forcedImmediate"] is True, f"hard threshold result should be marked forcedImmediate, got {payload}")
        require(meta_after["active"] == "account2", f"meta active should update after forced switch, got {meta_after}")
        require(main_store_after["profiles"]["openai-codex:default"]["access"] == beta_profile["access"], "hard threshold should rewrite live default token immediately")
    finally:
        env.cleanup()


def test_auto_forces_immediate_switch_at_hard_weekly_threshold() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        write_json(
            env.state / "agents" / "main" / "sessions" / "sessions.json",
            {
                "agent:main:main": {
                    "sessionId": "session-main",
                    "updatedAt": int(time.time() * 1000),
                    "model": "openai-codex/gpt-5.4",
                }
            },
        )
        write_json(
            env.state / "openai-codex-accounts" / "profiles" / ".account2.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 10.0, "window_minutes": 300},
                    "secondary": {"used_percent": 10.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        write_json(
            env.state / "openai-codex-accounts" / "profiles" / ".account3.quota.json",
            {
                "rate_limits": {
                    "primary": {"used_percent": 70.0, "window_minutes": 300},
                    "secondary": {"used_percent": 96.0, "window_minutes": 10080},
                },
                "cached_at": 1,
                "health": {"status": "healthy", "reason": "cached-rate-limits"},
            },
        )
        mock_usage = read_json(env.mock_rate_limits_path)
        mock_usage.setdefault("by_email", {})["gamma@example.com"] = {
            "primary": {"used_percent": 70.0, "window_minutes": 300, "resets_at": 1234567999},
            "secondary": {"used_percent": 96.0, "window_minutes": 10080, "resets_at": 2234567999},
        }
        write_json(env.mock_rate_limits_path, mock_usage)
        meta_path = env.state / "openai-codex-accounts" / "accounts.json"
        meta = read_json(meta_path)
        meta["active"] = "account3"
        write_json(meta_path, meta)

        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        gamma_profile = main_store["profiles"]["openai-codex:gamma@example.com"]
        beta_profile = main_store["profiles"]["openai-codex:beta@example.com"]
        main_store["profiles"]["openai-codex:default"] = gamma_profile
        worker_store["profiles"]["openai-codex:default"] = gamma_profile
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        forced = env.run("auto", "--json", "--inactive-minutes", "3")
        payload = json.loads(forced.stdout)
        meta_after = read_json(meta_path)
        main_store_after = read_json(main_store_path)
        require(payload["mode"] == "account", f"hard weekly threshold should force account switch, got {payload}")
        require(payload["activeAccount"] == "account2", f"hard weekly threshold should switch to best healthy account, got {payload}")
        require(payload["forcedImmediate"] is True, f"hard weekly threshold result should be marked forcedImmediate, got {payload}")
        require(payload["forcedBy"] == "weekly", f"hard weekly threshold should be marked forcedBy=weekly, got {payload}")
        require(meta_after["active"] == "account2", f"meta active should update after forced weekly switch, got {meta_after}")
        require(main_store_after["profiles"]["openai-codex:default"]["access"] == beta_profile["access"], "hard weekly threshold should rewrite live default token immediately")
    finally:
        env.cleanup()


def test_sync_new_email_same_account_id_auto_enrolls_new_account() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        new_profile = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("delta@example.com", "acct-gamma", "user-delta"),
            "refresh": "refresh-delta",
            "accountId": "acct-gamma",
            "expires": 2_000_000_000_999,
        }
        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        main_store["profiles"]["openai-codex:default"] = new_profile
        worker_store["profiles"]["openai-codex:default"] = new_profile
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        payload = json.loads(env.run("list", "--json").stdout)
        meta = read_json(env.state / "openai-codex-accounts" / "accounts.json")
        snap = read_json(env.state / "openai-codex-accounts" / "profiles" / "account4.json")
        cfg = read_json(env.state / "openclaw.json")
        main_store = read_json(env.state / "agents" / "main" / "agent" / "auth-profiles.json")

        require(payload["active"] == "account4", f"new email should auto-enroll as account4, got {payload}")
        require(meta["active"] == "account4", f"meta active should point to new email account, got {meta}")
        require(meta["accounts"]["account4"]["email"] == "delta@example.com", f"new auto-enrolled email missing: {meta}")
        require(snap["access"] == new_profile["access"], "auto-enrolled snapshot should mirror current live token")
        require("openai-codex:delta@example.com" in (cfg.get("auth", {}).get("profiles", {}) or {}), f"config auth.profiles should add delta alias: {cfg}")
        require("openai-codex:delta@example.com" in ((cfg.get("auth", {}).get("order", {}) or {}).get("openai-codex", [])), f"config auth.order should include delta alias: {cfg}")
        require("openai-codex:delta@example.com" in (main_store.get("profiles", {}) or {}), f"auth store should add delta alias: {main_store}")
    finally:
        env.cleanup()


def test_sync_same_email_updates_existing_account_without_duplicate() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        refreshed_beta = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("beta@example.com", "acct-beta-2", "user-beta-2"),
            "refresh": "refresh-beta-2",
            "accountId": "acct-beta-2",
            "expires": 2_000_000_001_111,
        }
        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        main_store["profiles"]["openai-codex:default"] = refreshed_beta
        worker_store["profiles"]["openai-codex:default"] = refreshed_beta
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        payload = json.loads(env.run("list", "--json").stdout)
        meta = read_json(env.state / "openai-codex-accounts" / "accounts.json")
        snap = read_json(env.state / "openai-codex-accounts" / "profiles" / "account2.json")

        require(payload["active"] == "account2", f"same email should keep existing account2 active, got {payload}")
        require(sorted(meta["accounts"].keys()) == ["account1", "account2", "account3"], f"same email must not create duplicates: {meta}")
        require(meta["accounts"]["account2"]["accountId"] == "acct-beta-2", f"same email should refresh accountId/team: {meta}")
        require(snap["accountId"] == "acct-beta-2", "snapshot should refresh to latest same-email accountId")
        require(snap["access"] == refreshed_beta["access"], "snapshot should refresh to latest same-email token")

        capture = env.run("capture", "renamed-beta")
        meta_after_capture = read_json(env.state / "openai-codex-accounts" / "accounts.json")
        require("现有账号快照: account2" in capture.stdout, f"capture should upsert existing same-email slot, got {capture.stdout}")
        require(sorted(meta_after_capture["accounts"].keys()) == ["account1", "account2", "account3"], f"capture same email must not create duplicates: {meta_after_capture}")
    finally:
        env.cleanup()


def test_list_prunes_stale_config_and_auth_aliases() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        cfg_path = env.state / "openclaw.json"
        cfg = read_json(cfg_path)
        cfg.setdefault("auth", {}).setdefault("profiles", {})["openai-codex:stale@example.com"] = {
            "provider": "openai-codex",
            "mode": "oauth",
            "email": "stale@example.com",
        }
        cfg.setdefault("auth", {}).setdefault("order", {}).setdefault("openai-codex", []).append("openai-codex:stale@example.com")
        write_json(cfg_path, cfg)

        stale_profile = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("stale@example.com", "acct-stale", "user-stale"),
            "refresh": "refresh-stale",
            "accountId": "acct-stale",
            "expires": 2_000_000_001_333,
        }
        for agent_id in ("main", "worker"):
            path = env.state / "agents" / agent_id / "agent" / "auth-profiles.json"
            store = read_json(path)
            store.setdefault("profiles", {})["openai-codex:stale@example.com"] = stale_profile
            write_json(path, store)

        env.run("list", "--json")
        cfg_after = read_json(cfg_path)
        main_after = read_json(env.state / "agents" / "main" / "agent" / "auth-profiles.json")
        worker_after = read_json(env.state / "agents" / "worker" / "agent" / "auth-profiles.json")

        require("openai-codex:stale@example.com" not in (cfg_after.get("auth", {}).get("profiles", {}) or {}), f"stale config alias should be pruned: {cfg_after}")
        require("openai-codex:stale@example.com" not in ((cfg_after.get("auth", {}).get("order", {}) or {}).get("openai-codex", [])), f"stale auth.order alias should be pruned: {cfg_after}")
        require("openai-codex:stale@example.com" not in (main_after.get("profiles", {}) or {}), f"stale main auth alias should be pruned: {main_after}")
        require("openai-codex:stale@example.com" not in (worker_after.get("profiles", {}) or {}), f"stale worker auth alias should be pruned: {worker_after}")
    finally:
        env.cleanup()


def test_sensitive_files_use_restricted_permissions() -> None:
    env = TestEnv()
    try:
        env.build_fixture()
        new_profile = {
            "type": "oauth",
            "provider": "openai-codex",
            "access": make_jwt("secure@example.com", "acct-secure", "user-secure"),
            "refresh": "refresh-secure",
            "accountId": "acct-secure",
            "expires": 2_000_000_001_222,
        }
        main_store_path = env.state / "agents" / "main" / "agent" / "auth-profiles.json"
        worker_store_path = env.state / "agents" / "worker" / "agent" / "auth-profiles.json"
        main_store = read_json(main_store_path)
        worker_store = read_json(worker_store_path)
        main_store["profiles"]["openai-codex:default"] = new_profile
        worker_store["profiles"]["openai-codex:default"] = new_profile
        write_json(main_store_path, main_store)
        write_json(worker_store_path, worker_store)

        env.run("capture", "account4")
        snapshot = env.state / "openai-codex-accounts" / "profiles" / "account4.json"
        meta = env.state / "openai-codex-accounts" / "accounts.json"
        require(stat.S_IMODE(snapshot.stat().st_mode) == 0o600, f"snapshot should be 600, got {oct(stat.S_IMODE(snapshot.stat().st_mode))}")
        require(stat.S_IMODE(meta.stat().st_mode) == 0o600, f"meta should be 600, got {oct(stat.S_IMODE(meta.stat().st_mode))}")
    finally:
        env.cleanup()


def main() -> int:
    tests = [
        test_metadata_migration_and_active_detection,
        test_use_preserves_metadata_and_syncs_agents,
        test_auto_switches_best_account_and_keep_current,
        test_probe_forces_fresh_quota_refresh,
        test_auto_blocks_switch_when_recent_sessions_are_active,
        test_auto_forces_immediate_switch_at_hard_five_hour_threshold,
        test_auto_forces_immediate_switch_at_hard_weekly_threshold,
        test_sync_new_email_same_account_id_auto_enrolls_new_account,
        test_sync_same_email_updates_existing_account_without_duplicate,
        test_list_prunes_stale_config_and_auth_aliases,
        test_sensitive_files_use_restricted_permissions,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:
            failures.append(f"FAIL {test.__name__}: {exc}")
            print(failures[-1], file=sys.stderr)
    if failures:
        return 1
    print(f"OK {len(tests)} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
