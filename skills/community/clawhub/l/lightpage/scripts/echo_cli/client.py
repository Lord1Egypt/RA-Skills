import json
import random
import sys
import time
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

from echo_cli import transport
from echo_cli.compat import UTC, parse_datetime, unlink
from echo_cli.notices import Collector, merge
from echo_cli.notices import decode as decode_notice
from echo_cli.qr import create_login_qr
from echo_cli.skill_version import SKILL_VERSION

DEVICE_GRANT = "urn:ietf:params:oauth:grant-type:device_code"


class APIError(RuntimeError):
    def __init__(self, status, error, notice=None):
        self.status, self.error, self.notice = status, error, notice
        super().__init__(error.get("message", "Request failed"))


def checked(response):
    if response.status_code == 304:
        return with_notice({"not_modified": True, "etag": response.headers.get("etag")}, response)
    if response.status_code >= 300:
        value = {}
        try:
            value = response.json()
            error = value.get("error", {}) if isinstance(value, dict) else {}
            if isinstance(error, str):
                error = {"code": error, "message": value.get("error_description", error)}
            if not isinstance(error, dict):
                error = {}
        except ValueError:
            error = {}
        raise APIError(
            response.status_code,
            {
                "code": error.get("code", "http_error"),
                "message": error.get("message", f"HTTP {response.status_code}"),
                "request_id": response.headers.get("x-request-id"),
            },
            response_notices(value if isinstance(value, dict) else {}, response),
        )
    return with_notice(response.json() if response.content else {"ok": True}, response)


def response_notices(value, response):
    body_notice = decode_notice(value.get("notice"), maximum=8192)
    notice = decode_notice(response.headers.get("echo-notice"), maximum=2048) or {}
    notice = merge(notice, decode_notice(response.headers.get("echo-platform-notice")) or {})
    # Within one response, the body is authoritative for duplicate fields.
    notice.update(body_notice or {})
    return notice or None


def with_notice(value, response):
    if not isinstance(value, dict):
        raise APIError(502, {"code": "invalid_response", "message": "Expected a JSON object"})
    notice = response_notices(value, response)
    value.pop("notice", None)
    if notice:
        value["notice"] = notice
    return value


def retry_after(response):
    value = response.headers.get("retry-after")
    if not value:
        return None
    try:
        return max(0, float(value))
    except ValueError:
        try:
            return max(0, parsedate_to_datetime(value).timestamp() - time.time())
        except (ValueError, TypeError, OverflowError):
            return None


class API:
    skill_name = "echo"
    skill_version = SKILL_VERSION

    def __init__(self, server, store, client=None, *, client_id="echo-cli", timeout=60):
        self.server, self.store, self.client_id, self.timeout = server, store, client_id, timeout
        self.transport_errors = (transport.TransportError,)
        if client is not None:
            # An injected third-party test/client adapter may have its own errors.
            try:
                import httpx
            except ImportError:
                pass
            else:
                self.transport_errors += (httpx.TransportError,)
        self.client = client or transport.Client(
            base_url=server, timeout=20, follow_redirects=False
        )
        self.client.headers["Echo-Skill-Version"] = self.skill_version
        self.client.headers["Echo-Skill-Name"] = self.skill_name
        self.metadata = None
        self.last_etag = None
        self.notice_collector = Collector()

    def close(self):
        self.client.close()

    def endpoint(self, value):
        origin = urlparse(self.server)
        parsed = urlparse(value)
        if value.startswith("/") and not value.startswith("//"):
            parsed = urlparse(self.server + value)
        if (
            parsed.scheme != origin.scheme
            or parsed.netloc != origin.netloc
            or parsed.username
            or parsed.query
            or parsed.fragment
            or not parsed.path.startswith("/")
            or any(segment in {".", ".."} for segment in parsed.path.split("/"))
            or "%" in parsed.path
        ):
            raise RuntimeError("Protocol endpoint must stay on the configured HTTPS origin")
        return parsed.path

    def send(self, method, path, *, retry=False, response_limit=None, **kwargs):
        path = self.endpoint(path)
        headers = transport.Headers(kwargs.pop("headers", {}))
        headers["Echo-Skill-Version"] = self.skill_version
        headers["Echo-Skill-Name"] = self.skill_name
        kwargs["headers"] = headers
        deadline = time.monotonic() + self.timeout
        for attempt in range(4):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("Request deadline exceeded; preserve the original publish key")
            response = None
            try:
                if response_limit is None:
                    response = self.client.request(
                        method, path, timeout=min(20, remaining), **kwargs
                    )
                else:
                    with self.client.stream(
                        method, path, timeout=min(20, remaining), **kwargs
                    ) as streamed:
                        chunks, size = [], 0
                        for chunk in streamed.iter_bytes(chunk_size=65536):
                            size += len(chunk)
                            if size > response_limit or time.monotonic() > deadline:
                                raise RuntimeError("Download exceeds the size or time budget")
                            chunks.append(chunk)
                        response = transport.Response(
                            streamed.status_code,
                            # iter_bytes has already decoded transfer compression.
                            headers={
                                key: value
                                for key, value in streamed.headers.items()
                                if key.lower() not in {"content-encoding", "content-length"}
                            },
                            content=b"".join(chunks),
                            request=streamed.request,
                        )
            except self.transport_errors:
                if not retry or attempt == 3:
                    raise RuntimeError(
                        "Network request failed; preserve the original publish key"
                    ) from None
            else:
                self.collect_notices(response)
                if (
                    not retry
                    or response.status_code not in {429, 500, 502, 503, 504}
                    or attempt == 3
                ):
                    return response
            delay = retry_after(response) if response is not None else None
            if delay is None:
                delay = min(30, 2**attempt) * random.uniform(1, 1.25)
            if delay >= deadline - time.monotonic():
                if response is not None:
                    return response
                raise RuntimeError("Retry delay exceeds request budget")
            time.sleep(delay)
        raise RuntimeError("Retry budget exhausted")

    def collect_notices(self, response):
        value = {}
        if response.headers.get("content-type", "").split(";")[0] == "application/json":
            try:
                value = response.json()
            except (ValueError, TypeError, RecursionError):
                pass
        self.notice_collector.add(
            response_notices(value if isinstance(value, dict) else {}, response)
        )

    def discover(self):
        value = checked(self.send("GET", "/.well-known/echo", retry=True))
        if (
            value.get("protocol") != "echo"
            or value.get("draft_version") != "0.2"
            or value.get("api_version") != "v1"
            or value.get("origin") != self.server
            or value.get("authorization", {}).get("profile") != "oauth-device-v1"
            or not {"content-v1", "device-access-v1", "conditional-read-v1"}.issubset(
                value.get("capabilities", [])
            )
        ):
            raise RuntimeError("Server does not support Echo Draft 0.2")
        self.endpoint(value["openapi_path"])
        metadata_path = self.endpoint(value["authorization"]["metadata_path"])
        metadata = checked(self.send("GET", metadata_path, retry=True))
        if metadata.get("issuer") != self.server or DEVICE_GRANT not in metadata.get(
            "grant_types_supported", []
        ):
            raise RuntimeError("Server OAuth metadata is incompatible")
        for field in ["device_authorization_endpoint", "token_endpoint", "revocation_endpoint"]:
            self.endpoint(metadata[field])
        self.metadata = metadata
        return value

    def safe_post(self, path, **kwargs):
        return checked(self.send("POST", path, retry=True, **kwargs))

    def refresh(self, value):
        if value.get("client_id"):
            endpoint = self.endpoint(value["token_endpoint"])
            result = self.safe_post(
                endpoint,
                data={
                    "client_id": value["client_id"],
                    "grant_type": "refresh_token",
                    "refresh_token": value["refresh_token"],
                },
            )
            result = {
                **value,
                **result,
                "access_expires_at": (
                    datetime.now(UTC) + timedelta(seconds=result["expires_in"])
                ).isoformat(),
            }
        else:
            # Credentials from the previous local release retain their legacy refresh path.
            result = self.safe_post(
                "/v1/auth/refresh",
                json={
                    "device_id": value["device_id"],
                    "refresh_token": value["refresh_token"],
                },
            )
        self.store.save(result)
        return result

    def credential(self, *, force=False, rejected=None):
        with self.store.lock():
            value = self.store.load()
            if not value:
                raise APIError(
                    401, {"code": "login_required", "message": "Not logged in; run echoctl login"}
                )
            if value.get("credential_profile") == "echo-device-v1":
                if force:
                    raise APIError(
                        401,
                        {
                            "code": "unauthorized",
                            "message": "Device was revoked; explicitly choose login mode",
                        },
                    )
                return value
            expires = parse_datetime(value["access_expires_at"])
            if (
                force and value["access_token"] == rejected
            ) or expires.timestamp() <= time.time() + 30:
                value = self.refresh(value)
            return value

    def request(self, method, path, *, authenticated=False, raw=False, **kwargs):
        headers = dict(kwargs.pop("headers", {}))
        if raw:
            kwargs["response_limit"] = 5 * 1024 * 1024
        credential = None
        if authenticated:
            credential = self.credential()
            headers["Authorization"] = f"Bearer {credential['access_token']}"
        elif path.startswith("/v1/"):
            # Public reads remain anonymous when no usable local credential exists.
            # Do not refresh, inspect identity, or initiate login just for a red dot.
            try:
                with self.store.lock():
                    saved = self.store.load()
                if saved and (
                    saved.get("credential_profile") == "echo-device-v1"
                    or parse_datetime(saved["access_expires_at"]).timestamp() > time.time()
                ):
                    headers["Authorization"] = f"Bearer {saved['access_token']}"
            except (RuntimeError, ValueError, KeyError):
                pass
        safe = method in {"GET", "PUT", "DELETE"} or "Idempotency-Key" in headers
        response = self.send(method, path, retry=safe, headers=headers, **kwargs)
        if response.status_code == 401 and authenticated:
            credential = self.credential(force=True, rejected=credential["access_token"])
            headers["Authorization"] = f"Bearer {credential['access_token']}"
            response = self.send(method, path, retry=safe, headers=headers, **kwargs)
        self.last_etag = response.headers.get("etag")
        if raw and response.status_code < 300:
            return response
        return checked(response)

    def sync_identity(self):
        result = self.request("GET", "/v1/me", authenticated=True)
        with self.store.lock():
            value = self.store.load()
            value.update(
                user_id=result.get("user_id", result["id"]),
                agent_id=result["id"],
                device_id=result["device_id"],
                server=self.server,
                identity_type=result.get("identity_type", "wechat"),
                display_name=result["name"],
                avatar_url=result.get("avatar_url"),
            )
            self.store.save(value)
        return result

    def native_login(
        self,
        device_name,
        *,
        mode=None,
        agent=None,
        force=False,
        binding=False,
        wechat_application=None,
    ):
        with self.store.lock(login=True):
            return self._native_login(
                device_name,
                mode=mode,
                agent=agent,
                force=force,
                binding=binding,
                wechat_application=wechat_application,
            )

    def prepare_login_body(self, body):
        return body

    def _native_login(
        self,
        device_name,
        *,
        mode=None,
        agent=None,
        force=False,
        binding=False,
        wechat_application=None,
    ):
        from secrets import token_urlsafe

        from echo_cli.credentials import atomic_json

        if self.store.backend != "file":
            raise RuntimeError(
                "New logins use file credentials; migrate old keyring credentials first"
            )
        self.store.preflight()
        with self.store.lock():
            existing = self.store.load()
            pending = self.store.pending()
        if existing and not force and not binding and not pending:
            # Never silently replace a revoked device with a fresh anonymous identity.
            return self.sync_identity()
        if binding:
            if not existing:
                raise APIError(
                    401, {"code": "login_required", "message": "Log in anonymously before binding"}
                )
            mode = "bind"
        if not mode:
            raise APIError(
                400,
                {
                    "code": "login_choice_required",
                    "message": "Choose login --anonymous --agent NAME (no scan; lost credentials cannot be recovered), or login --wechat (human approval; recover across environments)",
                },
            )
        if pending and pending["mode"] != mode:
            raise RuntimeError("A different login is pending; resume its original mode")
        if mode == "anonymous":
            if not pending:
                if not agent or not agent.strip():
                    raise RuntimeError("Anonymous login requires --agent NAME")
                pending = {
                    "mode": mode,
                    "body": {
                        "agent": agent,
                        "device_name": device_name,
                        "registration_token": token_urlsafe(48),
                    },
                }
                pending["body"] = self.prepare_login_body(pending["body"])
                with self.store.lock():
                    atomic_json(self.store.pending_path, pending)
            value = self.safe_post("/v1/auth/anonymous", json=pending["body"])
        else:
            if not pending:
                path = "/v1/auth/bind" if binding else "/v1/auth/connect"
                authorization = self.request(
                    "POST",
                    path,
                    authenticated=binding,
                    json=self.prepare_login_body(
                        {
                            "device_name": device_name,
                            "persistent": True,
                            "wechat_application": wechat_application,
                        }
                    ),
                )
                pending = {"mode": mode, "authorization": authorization}
                with self.store.lock():
                    atomic_json(self.store.pending_path, pending)
            authorization = pending["authorization"]
            uri = authorization["authorization_url"]
            self.endpoint(uri)
            qr_path = create_login_qr(uri)
            expires_at = parse_datetime(authorization["expires_at"]).timestamp()
            print(
                json.dumps(
                    {
                        "event": "authorization_required",
                        "qr_path": str(qr_path),
                        "user_code": authorization["verification_code"],
                        "expires_in": max(0, int(expires_at - time.time())),
                        "mode": mode,
                    },
                    ensure_ascii=False,
                ),
                file=sys.stderr,
                flush=True,
            )
            print(
                "请用微信扫码并核对确认；绑定将迁移全部匿名资产和设备，并替换历史显示信息。"
                if binding
                else "请用微信扫码并确认授权；资产可通过同一微信跨环境恢复。",
                file=sys.stderr,
                flush=True,
            )
            path = f"/v1/auth/connect/{authorization['request_id']}"
            headers = {"Authorization": f"Device {authorization['device_secret']}"}
            while time.time() < expires_at:
                state = checked(self.send("GET", path, headers=headers))["state"]
                if state in {"approved", "issued"}:
                    value = self.safe_post(path + "/token", headers=headers)
                    break
                if state in {"denied", "failed"}:
                    with self.store.lock():
                        unlink(self.store.pending_path)
                    raise RuntimeError("WeChat authorization was denied or failed")
                time.sleep(max(1, authorization.get("poll_interval", 5)))
            else:
                if binding:
                    # Ownership may already have committed even if the short-lived
                    # delivery expired before local persistence recovered.
                    result = self.sync_identity()
                    if result.get("identity_type") == "wechat":
                        with self.store.lock():
                            unlink(self.store.pending_path)
                        return result
                with self.store.lock():
                    unlink(self.store.pending_path)
                raise RuntimeError("WeChat authorization expired; start login again")
        with self.store.lock():
            if binding:
                value = {**self.store.load(), **value}
            value.update(server=self.server)
            self.store.save(value)
            unlink(self.store.pending_path)
        return self.sync_identity()

    def login(self, device_name, *, force=False):
        if not force:
            with self.store.lock():
                existing = self.store.load()
            if existing:
                try:
                    result = self.request("GET", "/v1/me", authenticated=True)
                    with self.store.lock():
                        value = self.store.load()
                        value.update({"agent_id": result["id"], "device_id": result["device_id"]})
                        self.store.save(value)
                    return result
                except APIError as exc:
                    if exc.status != 401 and exc.error["code"] != "invalid_grant":
                        raise
        if not self.metadata:
            self.discover()
        endpoint = self.endpoint(self.metadata["device_authorization_endpoint"])
        authorization = checked(
            self.send(
                "POST",
                endpoint,
                data={
                    "client_id": self.client_id,
                    "device_name": device_name,
                },
            )
        )
        uri = authorization.get("verification_uri_complete") or authorization["verification_uri"]
        self.endpoint(authorization["verification_uri"])
        parsed_uri = urlparse(uri)
        if (
            parsed_uri.scheme != "https"
            or parsed_uri.netloc != urlparse(self.server).netloc
            or parsed_uri.username
        ):
            raise RuntimeError("Verification URL must stay on the configured HTTPS origin")
        qr_path = create_login_qr(uri)
        print(
            json.dumps(
                {
                    "event": "authorization_required",
                    "qr_path": str(qr_path),
                    "user_code": authorization["user_code"],
                    "expires_in": authorization["expires_in"],
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
            flush=True,
        )
        print(
            f"请用微信扫描二维码，核对代码 {authorization['user_code']} 并确认授权。",
            file=sys.stderr,
            flush=True,
        )
        endpoint = self.endpoint(self.metadata["token_endpoint"])
        interval = max(1, authorization.get("interval", 5))
        expires = time.monotonic() + min(authorization["expires_in"], 900)
        while time.monotonic() + interval < expires:
            time.sleep(interval)
            try:
                response = self.client.post(
                    endpoint,
                    data={
                        "client_id": self.client_id,
                        "grant_type": DEVICE_GRANT,
                        "device_code": authorization["device_code"],
                    },
                    timeout=min(20, expires - time.monotonic()),
                )
            except self.transport_errors:
                # Device codes are single-use; a lost issuance response cannot be replayed.
                raise RuntimeError("Login response was lost; start login again") from None
            self.collect_notices(response)
            if response.status_code in {429, 500, 502, 503, 504}:
                interval = max(interval * 2, retry_after(response) or 0)
                continue
            try:
                value = checked(response)
            except APIError as exc:
                if exc.error["code"] == "authorization_pending":
                    continue
                if exc.error["code"] == "slow_down":
                    interval += 5
                    continue
                raise
            value.update(
                {
                    "client_id": self.client_id,
                    "token_endpoint": self.metadata["token_endpoint"],
                    "access_expires_at": (
                        datetime.now(UTC) + timedelta(seconds=value["expires_in"])
                    ).isoformat(),
                }
            )
            # Persist a redeemed token before /me: a failed identity read must not lose it.
            with self.store.lock():
                self.store.save(value)
            result = self.request("GET", "/v1/me", authenticated=True)
            with self.store.lock():
                saved = self.store.load()
                saved.update({"agent_id": result["id"], "device_id": result["device_id"]})
                self.store.save(saved)
            return result
        raise RuntimeError("WeChat authorization expired; run login again")
