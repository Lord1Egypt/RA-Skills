#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud IAM user creation and authorization helper.

This script creates IAM users and authorizes them (user group membership
and identity policy attachment) through the Huawei Cloud IAM v5 OpenAPI.
Execution is KooCLI first (``hcloud IAM <Operation>``), with a transparent
fallback to the official ``huaweicloudsdkiam`` v5 Python SDK when the CLI is
not available.

All REST paths used below come from the SDK ``_http_info`` resource_path of
``huaweicloudsdkiam.v5``:

    create_user_v5                POST /v5/users
    list_users_v5                 GET  /v5/users
    show_user_v5                  GET  /v5/users/{user_id}
    create_group_v5               POST /v5/groups
    list_groups_v5                GET  /v5/groups
    add_user_to_group_v5          POST /v5/groups/{group_id}/add-user
    attach_user_policy_v5         POST /v5/policies/{policy_id}/attach-user
    list_policies_v5              GET  /v5/policies
    list_attached_user_policies_v5 GET /v5/users/{user_id}/attached-policies

Secrets are never hardcoded: AK/SK are read from the environment (or the
active KooCLI profile for the CLI backend). Missing credentials abort with a
clear hint instead of silently degrading.

Usage:
    python3 scripts/iam_user_manage.py create-user --name alice \
        --description "ops account" --group-name ops --policy-name ReadOnlyAccess --confirm
    python3 scripts/iam_user_manage.py authorize --user-name alice \
        --group-name ops --policy-name ReadOnlyAccess --confirm
    python3 scripts/iam_user_manage.py list-users --json
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

SKILL_NAME = "huawei-cloud-iam-user-manage"
DEFAULT_REGION = "cn-north-4"
DEFAULT_TIMEOUT = 60

ENV_AK_CANDIDATES = (
    "HUAWEICLOUD_SDK_AK", "HUAWEI_ACCESS_KEY", "HW_ACCESS_KEY",
    "HUAWEI_AK", "HW_AK", "HWC_ACCESS_KEY",
)
ENV_SK_CANDIDATES = (
    "HUAWEICLOUD_SDK_SK", "HUAWEI_SECRET_KEY", "HW_SECRET_KEY",
    "HUAWEI_SK", "HW_SK", "HWC_SECRET_KEY",
)
ENV_REGION_CANDIDATES = (
    "HUAWEICLOUD_SDK_REGION", "HUAWEI_REGION", "HW_REGION_NAME", "HW_REGION",
)
ENV_TOKEN_CANDIDATES = (
    "HUAWEICLOUD_SDK_SECURITY_TOKEN", "HW_SECURITY_TOKEN", "HUAWEI_SECURITY_TOKEN",
)

# CreateUserReqBody.name: 1-64 chars, letters/digits/_/-/. and space, first char not a digit.
USER_NAME_RE = re.compile(r"^[A-Za-z0-9_\-.]{1,64}$")
# A user name may not start with a digit.
USER_NAME_FIRST_RE = re.compile(r"^[^0-9]")
# CreateGroupReqBody.group_name: 1-128 chars.
GROUP_NAME_RE = re.compile(r"^.{1,128}$", re.DOTALL)
# IAM user/group/policy ids: 1-64 chars, letters/digits/-.
IAM_ID_RE = re.compile(r"^[A-Za-z0-9\-]{1,64}$")
# Description: 0-255 chars, forbids @ # % & < > \ $ ^ *
DESC_FORBIDDEN_RE = re.compile(r"[@#%&<>\\$^*]")


class IamError(Exception):
    """Base error carrying an optional IAM error code."""

    def __init__(self, message, code=None, operation=None, hint=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.operation = operation
        self.hint = hint


class ValidationError(IamError):
    pass


class ConfirmationRequired(IamError):
    pass


# --------------------------------------------------------------------------
# Input validation
# --------------------------------------------------------------------------

def validate_user_name(name):
    if not name or not USER_NAME_RE.match(name):
        raise ValidationError(
            "非法用户名 %r：长度 1-64，仅允许字母/数字/下划线/连字符/点，且不能包含空格以外的特殊字符"
            % name)
    if not USER_NAME_FIRST_RE.match(name):
        raise ValidationError("非法用户名 %r：首字符不能为数字" % name)
    return name


def validate_group_name(name):
    if not name or not GROUP_NAME_RE.match(name):
        raise ValidationError("非法用户组名 %r：长度 1-128" % name)
    if DESC_FORBIDDEN_RE.search(name):
        raise ValidationError("非法用户组名 %r：不能包含 @ # %% & < > \\ $ ^ *" % name)
    return name


def validate_description(desc):
    if desc is None:
        return None
    if len(desc) > 255:
        raise ValidationError("描述过长（%d > 255）" % len(desc))
    if DESC_FORBIDDEN_RE.search(desc):
        raise ValidationError("描述包含禁用字符（@ # % & < > \\ $ ^ *）")
    return desc


def validate_iam_id(value, what):
    if not value or not IAM_ID_RE.match(value):
        raise ValidationError("非法%s %r：长度 1-64，仅允许字母/数字/连字符" % (what, value))
    return value


# --------------------------------------------------------------------------
# Credentials
# --------------------------------------------------------------------------

def _first_env(candidates):
    for key in candidates:
        value = os.getenv(key)
        if value:
            return value
    return ""


def load_ak_sk():
    ak = _first_env(ENV_AK_CANDIDATES)
    sk = _first_env(ENV_SK_CANDIDATES)
    if not ak or not sk:
        raise IamError(
            "未找到可用的 AK/SK 凭证",
            hint=("请在会话外设置环境变量（禁止在对话里粘贴明文密钥）：\n"
                  "  export HUAWEICLOUD_SDK_AK=\"<your-access-key-id>\"\n"
                  "  export HUAWEICLOUD_SDK_SK=\"<your-secret-access-key>\"\n"
                  "  或先运行 skill-quality-cli run --skill-name %s -- hcloud configure list 确认 CLI 已认证"
                  % SKILL_NAME))
    return ak, sk


def resolve_region(explicit=None):
    if explicit:
        return explicit
    found = _first_env(ENV_REGION_CANDIDATES)
    return found or DEFAULT_REGION


def load_security_token():
    return _first_env(ENV_TOKEN_CANDIDATES)


# --------------------------------------------------------------------------
# CLI backend (KooCLI, primary)
# --------------------------------------------------------------------------

_BRACKET_PAIRS = {"{": "}", "[": "]"}

# KooCLI error payloads (IAM v5 OpenAPI / APIG) use these keys.
_ERROR_CODE_KEYS = ("error_code", "errorCode")
_ERROR_MSG_KEYS = ("error_msg", "error_message", "errorMessage")


def _balanced_json_slice(text, start):
    """Return the balanced ``{...}`` / ``[...]`` slice beginning at ``start``.

    Tracks string literals and escapes so braces/brackets inside strings do not
    affect the balance. Returns ``None`` when no matching closer is present.
    """
    opener = text[start]
    closer = _BRACKET_PAIRS.get(opener)
    if closer is None:
        return None
    depth = 0
    in_string = False
    escaped = False
    for pos in range(start, len(text)):
        ch = text[pos]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start:pos + 1]
    return None


def _extract_json(text):
    """Parse the JSON object embedded in possibly noisy command output.

    KooCLI may append diagnostics after the JSON payload (e.g. "Failed to get
    terminal width ..."), which breaks a whole-string ``json.loads``. Scan for
    the first parseable balanced ``{...}`` / ``[...]`` slice instead, so the
    real payload is not discarded.
    """
    text = (text or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except ValueError:
        pass
    for idx, ch in enumerate(text):
        if ch not in "{[":
            continue
        candidate = _balanced_json_slice(text, idx)
        if candidate is None:
            continue
        try:
            return json.loads(candidate)
        except ValueError:
            continue
    raise IamError("KooCLI 输出无法解析为 JSON：%s" % text[:200])


def _extract_json_or_none(text):
    """Best-effort ``_extract_json`` that returns ``None`` instead of raising."""
    try:
        return _extract_json(text)
    except IamError:
        return None


def _error_details(payload):
    """Return ``(error_code, error_msg)`` for a KooCLI/IAM error payload.

    ``(None, None)`` is returned for a normal (non-error) payload.
    """
    if not isinstance(payload, dict):
        return None, None
    code = next((payload.get(k) for k in _ERROR_CODE_KEYS if payload.get(k)), None)
    msg = next((payload.get(k) for k in _ERROR_MSG_KEYS if payload.get(k)), None)
    err = payload.get("error")
    if isinstance(err, dict):
        code = code or next((err.get(k) for k in _ERROR_CODE_KEYS if err.get(k)), None)
        msg = msg or next((err.get(k) for k in _ERROR_MSG_KEYS if err.get(k)), None)
        if not msg and err.get("code") is not None and code is None:
            code = err.get("code")
        if not msg:
            msg = err.get("message")
    elif isinstance(err, str) and not msg:
        msg = err
    return code, msg


def _cli_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class CliBackend(object):
    """Execute IAM operations through KooCLI (wrapped by skill-quality-cli)."""

    name = "cli"

    def __init__(self, region, timeout=DEFAULT_TIMEOUT, runner=None):
        self.region = region
        self.timeout = timeout
        self._runner = runner or self._default_runner
        self._running_operation = None

    def available(self):
        return shutil.which("hcloud") is not None

    def _base_cmd(self):
        if shutil.which("skill-quality-cli") and shutil.which("hcloud"):
            return ["skill-quality-cli", "run", "--skill-name", SKILL_NAME, "--", "hcloud"]
        return ["hcloud"]

    def build_cmd(self, operation, params):
        cmd = self._base_cmd() + ["IAM", operation, "--cli-region=%s" % self.region]
        for key in sorted(params):
            value = params[key]
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                for item in value:
                    cmd.append("--%s=%s" % (key, _cli_value(item)))
            else:
                cmd.append("--%s=%s" % (key, _cli_value(value)))
        return cmd

    def _default_runner(self, cmd):
        try:
            proc = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, timeout=self.timeout)
        except FileNotFoundError:
            raise IamError("未找到 hcloud 命令（KooCLI 未安装）")
        except subprocess.TimeoutExpired:
            raise IamError("KooCLI 调用超时（%ss）" % self.timeout)
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        payload = None
        parse_error = None
        try:
            payload = _extract_json(stdout)
        except IamError as exc:
            parse_error = exc
        code, msg = _error_details(payload)
        if not (code or msg) and not parse_error:
            # Some KooCLI builds print the error payload on stderr.
            code, msg = _error_details(_extract_json_or_none(stderr))
        if code or msg:
            raise IamError(
                "KooCLI 调用失败：%s" % (msg or code),
                code=code, operation=self._running_operation,
                hint="请检查 IAM 权限、参数取值，或该资源是否已存在")
        if proc.returncode != 0:
            err = (stderr or stdout or "").strip()
            raise IamError("KooCLI 调用失败：%s" % err[:300],
                           operation=self._running_operation)
        if parse_error is not None:
            raise parse_error
        return payload

    def call(self, operation, params):
        cmd = self.build_cmd(operation, params)
        self._running_operation = operation
        return self._runner(cmd)


# --------------------------------------------------------------------------
# SDK backend (huaweicloudsdkiam v5, fallback)
# --------------------------------------------------------------------------

class SdkBackend(object):
    """Execute IAM operations through the official Python SDK (v5)."""

    name = "sdk"

    def __init__(self, region, ak, sk, security_token="", timeout=DEFAULT_TIMEOUT,
                 client_factory=None):
        self.region = region
        self.ak = ak
        self.sk = sk
        self.security_token = security_token
        self.timeout = timeout
        self._client_factory = client_factory or self._build_client
        self._client = None

    def available(self):
        try:
            import huaweicloudsdkiam.v5  # noqa: F401
            import huaweicloudsdkcore  # noqa: F401
            return True
        except ImportError:
            return False

    def _build_client(self):
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkiam.v5 import IamClient
        # IamRegion is exported from the region submodule, not from the v5
        # top-level package (verified against huaweicloudsdkiam 3.1.219).
        from huaweicloudsdkiam.v5.region.iam_region import IamRegion

        cred = BasicCredentials(self.ak, self.sk)
        if self.security_token:
            cred.with_security_token(self.security_token)
        http_config = HttpConfig.get_default_config()
        http_config.ignore_ssl_verification = True
        http_config.timeout = (30, self.timeout)
        return (IamClient.new_builder()
                .with_credentials(cred)
                .with_http_config(http_config)
                .with_region(IamRegion.value_of(self.region))
                .build())

    @property
    def client(self):
        if self._client is None:
            self._client = self._client_factory()
        return self._client

    def call(self, operation, params):
        from huaweicloudsdkcore.exceptions import exceptions
        handler = getattr(self, "_op_" + operation.lower(), None)
        if handler is None:
            raise IamError("SDK 后端不支持操作 %s" % operation, operation=operation)
        try:
            return handler(params)
        except exceptions.ClientRequestException as exc:
            raise IamError(
                getattr(exc, "error_msg", None) or str(exc),
                code=getattr(exc, "error_code", None) or getattr(exc, "status_code", None),
                operation=operation,
                hint="请检查 IAM 权限、参数取值，或该资源是否已存在")
        except exceptions.ServerResponseException as exc:
            raise IamError(str(exc), code=getattr(exc, "status_code", None), operation=operation)
        except IamError:
            raise
        except Exception as exc:  # noqa: BLE001 - normalized to a single error type
            raise IamError("%s: %s" % (type(exc).__name__, exc), operation=operation)

    # -- operation handlers -------------------------------------------------

    def _op_createuserv5(self, params):
        from huaweicloudsdkiam.v5 import CreateUserV5Request, CreateUserReqBody
        body = CreateUserReqBody(
            name=params["name"],
            description=params.get("description"),
            enabled=params.get("enabled", True))
        return self.client.create_user_v5(CreateUserV5Request(body=body)).to_json_object()

    def _op_listusersv5(self, params):
        from huaweicloudsdkiam.v5 import ListUsersV5Request
        req = ListUsersV5Request(limit=params.get("limit", 100))
        return self.client.list_users_v5(req).to_json_object()

    def _op_showuserv5(self, params):
        from huaweicloudsdkiam.v5 import ShowUserV5Request
        return self.client.show_user_v5(
            ShowUserV5Request(user_id=params["user_id"])).to_json_object()

    def _op_creategroupv5(self, params):
        from huaweicloudsdkiam.v5 import CreateGroupV5Request, CreateGroupReqBody
        body = CreateGroupReqBody(
            group_name=params["group_name"],
            description=params.get("description"))
        return self.client.create_group_v5(CreateGroupV5Request(body=body)).to_json_object()

    def _op_listgroupsv5(self, params):
        from huaweicloudsdkiam.v5 import ListGroupsV5Request
        req = ListGroupsV5Request(limit=params.get("limit", 100))
        return self.client.list_groups_v5(req).to_json_object()

    def _op_addusertogroupv5(self, params):
        from huaweicloudsdkiam.v5 import AddUserToGroupV5Request, AddUserToGroupReqBody
        req = AddUserToGroupV5Request(
            group_id=params["group_id"],
            body=AddUserToGroupReqBody(user_id=params["user_id"]))
        return self.client.add_user_to_group_v5(req).to_json_object()

    def _op_attachuserpolicyv5(self, params):
        from huaweicloudsdkiam.v5 import AttachUserPolicyV5Request, AttachUserPolicyReqBody
        req = AttachUserPolicyV5Request(
            policy_id=params["policy_id"],
            body=AttachUserPolicyReqBody(user_id=params["user_id"]))
        return self.client.attach_user_policy_v5(req).to_json_object()

    def _op_listpoliciesv5(self, params):
        from huaweicloudsdkiam.v5 import ListPoliciesV5Request
        req = ListPoliciesV5Request(limit=params.get("limit", 100))
        return self.client.list_policies_v5(req).to_json_object()

    def _op_listattacheduserpoliciesv5(self, params):
        from huaweicloudsdkiam.v5 import ListAttachedUserPoliciesV5Request
        req = ListAttachedUserPoliciesV5Request(user_id=params["user_id"],
                                                limit=params.get("limit", 100))
        return self.client.list_attached_user_policies_v5(req).to_json_object()


def build_backend(args):
    """Resolve the requested executor, falling back CLI -> SDK -> error."""
    requested = args.executor
    region = resolve_region(args.region)

    def _make_cli():
        return CliBackend(region, timeout=args.timeout)

    def _make_sdk():
        ak, sk = load_ak_sk()
        return SdkBackend(region, ak, sk, security_token=load_security_token(),
                          timeout=args.timeout)

    if requested == "cli":
        backend = _make_cli()
        if not backend.available():
            raise IamError("请求了 cli 执行后端，但未找到 hcloud（KooCLI）命令")
        return backend
    if requested == "sdk":
        backend = _make_sdk()
        if not backend.available():
            raise IamError("请求了 sdk 执行后端，但未安装 huaweicloudsdkiam（可运行 scripts/ensure_env.py）")
        return backend

    # auto: CLI first, then SDK
    cli = _make_cli()
    if cli.available():
        return cli
    sdk = _make_sdk()
    if sdk.available():
        return sdk
    raise IamError(
        "无可用执行后端：未找到 hcloud（KooCLI），也未安装 huaweicloudsdkiam",
        hint="安装 KooCLI 或运行 python3 scripts/ensure_env.py 安装 SDK 后重试")


# --------------------------------------------------------------------------
# Response normalization
# --------------------------------------------------------------------------

def _as_dict(payload):
    return payload if isinstance(payload, dict) else {}


def normalize_user(payload):
    user = _as_dict(payload).get("user") or payload
    user = _as_dict(user)
    return {
        "user_id": user.get("user_id"),
        "user_name": user.get("user_name"),
        "urn": user.get("urn"),
        "enabled": user.get("enabled"),
        "description": user.get("description"),
    }


def normalize_group(payload):
    group = _as_dict(payload).get("group") or payload
    group = _as_dict(group)
    return {
        "group_id": group.get("group_id"),
        "group_name": group.get("group_name"),
        "urn": group.get("urn"),
        "description": group.get("description"),
    }


def normalize_policy(payload):
    policy = _as_dict(payload)
    return {
        "policy_id": policy.get("policy_id"),
        "policy_name": policy.get("policy_name"),
        "policy_type": policy.get("policy_type"),
        "urn": policy.get("urn"),
    }


def _users_from_list(payload):
    data = _as_dict(payload)
    users = data.get("users")
    if users is None and isinstance(payload.get("user"), dict):  # pragma: no cover
        users = [payload["user"]]
    return [normalize_user({"user": u}) for u in (users or [])]


def _groups_from_list(payload):
    data = _as_dict(payload)
    return [normalize_group({"group": g}) for g in (data.get("groups") or [])]


def _policies_from_list(payload):
    data = _as_dict(payload)
    return [normalize_policy(p) for p in (data.get("policies") or [])]


# --------------------------------------------------------------------------
# High-level operations
# --------------------------------------------------------------------------

class LazyBackend(object):
    """Defer backend construction until the first call.

    Lets purely offline commands (``--dry-run`` with explicit ids, ``--help``)
    run without credentials, while keeping the CLI->SDK resolution lazy.
    """

    def __init__(self, factory):
        self._factory = factory
        self._inner = None
        self.name = "auto"

    @property
    def backend(self):
        if self._inner is None:
            self._inner = self._factory()
        return self._inner

    def available(self):
        return self.backend.available()

    def call(self, operation, params):
        return self.backend.call(operation, params)


class Manager(object):
    def __init__(self, backend, out):
        self.backend = backend
        self.out = out

    # -- lookup helpers -----------------------------------------------------

    def find_user_by_name(self, name):
        payload = self.backend.call("ListUsersV5", {"limit": 100})
        for user in _users_from_list(payload):
            if user.get("user_name") == name:
                return user
        return None

    def get_user(self, user_id=None, user_name=None):
        if user_id:
            return normalize_user(self.backend.call("ShowUserV5", {"user_id": user_id}))
        if user_name:
            found = self.find_user_by_name(user_name)
            if not found:
                raise IamError("未找到用户名 %r" % user_name)
            return found
        raise ValidationError("需要 --user-id 或 --user-name")

    def resolve_group(self, group_id=None, group_name=None, create=False, description=None):
        if group_id:
            validate_iam_id(group_id, "用户组ID")
            return {"group_id": group_id, "group_name": None, "reused": True, "created": False}
        if not group_name:
            return None
        validate_group_name(group_name)
        payload = self.backend.call("ListGroupsV5", {"limit": 100})
        for group in _groups_from_list(payload):
            if group.get("group_name") == group_name:
                return dict(group, reused=True, created=False)
        if not create:
            raise IamError("未找到用户组 %r（可加 --create-group 自动创建）" % group_name)
        created = normalize_group(self.backend.call(
            "CreateGroupV5", {"group_name": group_name, "description": description}))
        created["reused"] = False
        created["created"] = True
        return created

    def resolve_policy(self, policy_id=None, policy_name=None):
        if policy_id:
            validate_iam_id(policy_id, "策略ID")
            return {"policy_id": policy_id, "policy_name": None}
        if not policy_name:
            return None
        payload = self.backend.call("ListPoliciesV5", {"limit": 100})
        matches = [p for p in _policies_from_list(payload) if p.get("policy_name") == policy_name]
        if not matches:
            raise IamError("未找到权限策略 %r" % policy_name)
        if len(matches) > 1:
            ids = ", ".join(str(m.get("policy_id")) for m in matches)
            raise IamError("策略名 %r 对应多个策略ID（%s），请改用 --policy-id" % (policy_name, ids))
        return matches[0]

    # -- write operations ---------------------------------------------------

    def create_user(self, name, description=None, enabled=True):
        validate_user_name(name)
        validate_description(description)
        try:
            payload = self.backend.call("CreateUserV5", {
                "name": name, "description": description, "enabled": enabled})
            user = normalize_user(payload)
            user["reused"] = False
            return user
        except IamError as exc:
            code = str(exc.code or "")
            if code in ("409", "IAM.0006", "IAM.0202") or "already exists" in exc.message.lower():
                existing = self.find_user_by_name(name)
                if existing:
                    existing["reused"] = True
                    return existing
            raise

    def add_user_to_group(self, user_id, group_id):
        validate_iam_id(user_id, "用户ID")
        validate_iam_id(group_id, "用户组ID")
        try:
            self.backend.call("AddUserToGroupV5",
                              {"user_id": user_id, "group_id": group_id})
            return {"added": True, "already_member": False}
        except IamError as exc:
            code = str(exc.code or "")
            if code in ("409", "IAM.0210") or "already" in exc.message.lower():
                return {"added": True, "already_member": True}
            raise

    def attach_policy(self, user_id, policy_id):
        validate_iam_id(user_id, "用户ID")
        validate_iam_id(policy_id, "策略ID")
        try:
            self.backend.call("AttachUserPolicyV5",
                              {"user_id": user_id, "policy_id": policy_id})
            return {"attached": True, "already_attached": False}
        except IamError as exc:
            code = str(exc.code or "")
            if code in ("409", "IAM.0240") or "already" in exc.message.lower():
                return {"attached": True, "already_attached": True}
            raise

    def authorize(self, user, group, policies):
        result = {"user_id": user.get("user_id"), "user_name": user.get("user_name"),
                  "group": None, "policies": []}
        if group:
            outcome = self.add_user_to_group(user["user_id"], group["group_id"])
            result["group"] = {
                "group_id": group.get("group_id"),
                "group_name": group.get("group_name"),
                "reused": group.get("reused", True),
                "created": group.get("created", False),
                "already_member": outcome["already_member"],
            }
        for policy in policies or []:
            outcome = self.attach_policy(user["user_id"], policy["policy_id"])
            result["policies"].append({
                "policy_id": policy.get("policy_id"),
                "policy_name": policy.get("policy_name"),
                "already_attached": outcome["already_attached"],
            })
        return result


# --------------------------------------------------------------------------
# CLI wiring
# --------------------------------------------------------------------------

def _emit(out, data, as_json):
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        (out or _print_kv)(data)


def _print_kv(data, prefix=""):
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            print("%s%s: %s" % (prefix, key, json.dumps(value, ensure_ascii=False)))
        else:
            print("%s%s: %s" % (prefix, key, value))


def _require_confirm(args, action_desc):
    if args.dry_run:
        return
    if args.confirm:
        return
    raise ConfirmationRequired(
        "写操作为不可逆变更，需要显式确认：%s\n"
        "请核对后加 --confirm 重新执行（或先 --dry-run 预览）。" % action_desc)


def _collect_policies(manager, args):
    policies = []
    for pid in args.policy_id or []:
        policies.append(manager.resolve_policy(policy_id=pid))
    for pname in args.policy_name or []:
        policies.append(manager.resolve_policy(policy_name=pname))
    return policies


# --------------------------------------------------------------------------
# Offline dry-run planning (no backend, no credentials)
# --------------------------------------------------------------------------

_DRY_RUN_NOTE = ("dry-run：仅预览计划，未解析名称、未调用后端（离线，无需凭证）。"
                 "实际执行时会按需解析名称→ID。")


def _dry_run_group(args):
    """Describe the target group without touching the backend."""
    if args.group_id:
        validate_iam_id(args.group_id, "用户组ID")
        return {"group_id": args.group_id, "group_name": None, "resolved": True}
    if not args.group_name:
        return None
    validate_group_name(args.group_name)
    return {
        "group_id": None,
        "group_name": args.group_name,
        "create": bool(args.create_group),
        "resolved": False,
    }


def _dry_run_policy(policy_id=None, policy_name=None):
    """Describe a policy target without touching the backend."""
    if policy_id:
        validate_iam_id(policy_id, "策略ID")
        return {"policy_id": policy_id, "policy_name": None, "resolved": True}
    if policy_name:
        return {"policy_id": None, "policy_name": policy_name, "resolved": False}
    return None


def _dry_run_policies(args):
    policies = []
    for pid in args.policy_id or []:
        policies.append(_dry_run_policy(policy_id=pid))
    for pname in args.policy_name or []:
        policies.append(_dry_run_policy(policy_name=pname))
    return policies


def _dry_run_authorize(args):
    if not args.user_id and not args.user_name:
        raise ValidationError("需要 --user-id 或 --user-name")
    if args.user_id:
        validate_iam_id(args.user_id, "用户ID")
    group = _dry_run_group(args)
    policies = _dry_run_policies(args)
    if not group and not policies:
        raise ValidationError(
            "authorize 至少需要 --group-name/--group-id 或 --policy-id/--policy-name")
    return {
        "action": "authorize",
        "user": {"user_id": args.user_id, "user_name": args.user_name},
        "group": group,
        "policies": policies,
        "note": _DRY_RUN_NOTE,
    }


def build_parser():
    parser = argparse.ArgumentParser(
        prog="iam_user_manage.py",
        description="Huawei Cloud IAM user creation and authorization (IAM v5).",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--region", default=None,
                        help="Huawei Cloud region (default: env HUAWEI_REGION / cn-north-4)")
    parser.add_argument("--executor", choices=["auto", "cli", "sdk"], default="auto",
                        help="Execution backend (default: auto = CLI first, then SDK)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="Per-call timeout in seconds")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the planned operations without executing them")
    parser.add_argument("--confirm", action="store_true",
                        help="Confirm the (mutating) operation")

    # Common flags are also accepted after the subcommand (SUPPRESS keeps the
    # value parsed before the subcommand when the flag is absent here).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--region", default=argparse.SUPPRESS)
    common.add_argument("--executor", choices=["auto", "cli", "sdk"],
                        default=argparse.SUPPRESS)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    common.add_argument("--timeout", type=int, default=argparse.SUPPRESS)
    common.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS)
    common.add_argument("--confirm", action="store_true", default=argparse.SUPPRESS)

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create-user", parents=[common], help="Create an IAM user (and optionally authorize it)")
    p.add_argument("--name", required=True)
    p.add_argument("--description", default=None)
    p.add_argument("--disabled", action="store_true", help="Create the user disabled")
    p.add_argument("--group-id", default=None)
    p.add_argument("--group-name", default=None)
    p.add_argument("--create-group", action="store_true",
                   help="Create the group if --group-name does not exist")
    p.add_argument("--policy-id", action="append", default=[])
    p.add_argument("--policy-name", action="append", default=[])

    p = sub.add_parser("create-group", parents=[common], help="Create an IAM user group")
    p.add_argument("--name", required=True)
    p.add_argument("--description", default=None)

    p = sub.add_parser("authorize", parents=[common], help="Authorize an existing IAM user")
    p.add_argument("--user-id", default=None)
    p.add_argument("--user-name", default=None)
    p.add_argument("--group-id", default=None)
    p.add_argument("--group-name", default=None)
    p.add_argument("--create-group", action="store_true")
    p.add_argument("--policy-id", action="append", default=[])
    p.add_argument("--policy-name", action="append", default=[])

    p = sub.add_parser("add-user-to-group", parents=[common], help="Add an existing user to a group")
    p.add_argument("--user-id", required=True)
    p.add_argument("--group-id", required=True)

    p = sub.add_parser("attach-policy", parents=[common], help="Attach an identity policy to a user")
    p.add_argument("--user-id", required=True)
    p.add_argument("--policy-id", default=None)
    p.add_argument("--policy-name", default=None)

    p = sub.add_parser("list-users", parents=[common], help="List IAM users")
    p.add_argument("--limit", type=int, default=100)

    p = sub.add_parser("list-groups", parents=[common], help="List IAM user groups")
    p.add_argument("--limit", type=int, default=100)

    p = sub.add_parser("list-policies", parents=[common], help="List identity policies")
    p.add_argument("--limit", type=int, default=100)

    p = sub.add_parser("show-user", parents=[common], help="Show one IAM user")
    p.add_argument("--user-id", default=None)
    p.add_argument("--user-name", default=None)

    return parser


def _human_user(data):
    print("IAM 用户已就绪：")
    print("  user_id:   %s" % data.get("user_id"))
    print("  user_name: %s" % data.get("user_name"))
    print("  enabled:   %s" % data.get("enabled"))
    if data.get("reused"):
        print("  (已存在，复用现有用户)")


def cmd_create_user(args):
    manager, out = _session(args)
    if args.dry_run:
        validate_user_name(args.name)
        validate_description(args.description)
        plan = {"action": "create-user", "name": args.name,
                "description": args.description, "enabled": not args.disabled,
                "group": _dry_run_group(args), "policies": _dry_run_policies(args),
                "note": _DRY_RUN_NOTE}
        _emit(_default_out, plan, args.json)
        return 0
    group = manager.resolve_group(args.group_id, args.group_name,
                                  create=args.create_group, description=args.description)
    policies = _collect_policies(manager, args)
    _require_confirm(args, "创建 IAM 用户 %r 并授权" % args.name)
    user = manager.create_user(args.name, args.description, enabled=not args.disabled)
    result = {"user_id": user.get("user_id"), "user_name": user.get("user_name"),
              "enabled": user.get("enabled"), "reused": user.get("reused", False)}
    if group or policies:
        authorization = manager.authorize(user, group, policies)
        result["authorization"] = authorization
    out(result)
    return 0


def cmd_create_group(args):
    manager, out = _session(args)
    validate_group_name(args.name)
    validate_description(args.description)
    plan = {"action": "create-group", "group_name": args.name,
            "description": args.description, "note": _DRY_RUN_NOTE}
    if args.dry_run:
        _emit(_default_out, plan, args.json)
        return 0
    _require_confirm(args, "创建 IAM 用户组 %r" % args.name)
    existing = None
    payload = manager.backend.call("ListGroupsV5", {"limit": 100})
    for grp in _groups_from_list(payload):
        if grp.get("group_name") == args.name:
            existing = grp
            break
    if existing:
        existing["reused"] = True
        out(existing)
        return 0
    try:
        group = normalize_group(manager.backend.call(
            "CreateGroupV5", {"group_name": args.name, "description": args.description}))
    except IamError as exc:
        if str(exc.code or "") in ("409", "IAM.0210"):
            group = manager.resolve_group(group_name=args.name)
            group["reused"] = True
        else:
            raise
    group["reused"] = group.get("reused", False)
    out(group)
    return 0


def cmd_authorize(args):
    manager, out = _session(args)
    if args.dry_run:
        _emit(_default_out, _dry_run_authorize(args), args.json)
        return 0
    user = manager.get_user(args.user_id, args.user_name)
    group = manager.resolve_group(args.group_id, args.group_name,
                                  create=args.create_group, description=None)
    policies = _collect_policies(manager, args)
    if not group and not policies:
        raise ValidationError("authorize 至少需要 --group-name/--group-id 或 --policy-id/--policy-name")
    _require_confirm(args, "为用户 %r 授权" % (user.get("user_name") or user.get("user_id")))
    out(manager.authorize(user, group, policies))
    return 0


def cmd_add_user_to_group(args):
    manager, out = _session(args)
    if args.dry_run:
        validate_iam_id(args.user_id, "用户ID")
        validate_iam_id(args.group_id, "用户组ID")
        _emit(_default_out, {"action": "add-user-to-group", "user_id": args.user_id,
                             "group_id": args.group_id, "note": _DRY_RUN_NOTE}, args.json)
        return 0
    _require_confirm(args, "将用户加入用户组")
    out(manager.add_user_to_group(args.user_id, args.group_id))
    return 0


def cmd_attach_policy(args):
    manager, out = _session(args)
    if args.dry_run:
        validate_iam_id(args.user_id, "用户ID")
        policy = _dry_run_policy(args.policy_id, args.policy_name)
        if not policy:
            raise ValidationError("需要 --policy-id 或 --policy-name")
        _emit(_default_out, {"action": "attach-policy", "user_id": args.user_id,
                             "policy": policy, "note": _DRY_RUN_NOTE}, args.json)
        return 0
    policy = manager.resolve_policy(args.policy_id, args.policy_name)
    if not policy:
        raise ValidationError("需要 --policy-id 或 --policy-name")
    _require_confirm(args, "为用户绑定权限策略")
    out(manager.attach_policy(args.user_id, policy["policy_id"]))
    return 0


def cmd_list_users(args):
    manager, out = _session(args)
    data = _users_from_list(manager.backend.call("ListUsersV5", {"limit": args.limit}))
    if args.json:
        _emit(None, data, True)
    else:
        _emit_users(data)
    return 0


def cmd_list_groups(args):
    manager, out = _session(args)
    data = _groups_from_list(manager.backend.call("ListGroupsV5", {"limit": args.limit}))
    if args.json:
        _emit(None, data, True)
    else:
        print("group_id | group_name | description")
        for group in data:
            print("%s | %s | %s" % (group.get("group_id"), group.get("group_name"),
                                    group.get("description")))
    return 0


def cmd_list_policies(args):
    manager, out = _session(args)
    data = _policies_from_list(manager.backend.call("ListPoliciesV5", {"limit": args.limit}))
    if args.json:
        _emit(None, data, True)
    else:
        print("policy_id | policy_name | policy_type")
        for policy in data:
            print("%s | %s | %s" % (policy.get("policy_id"), policy.get("policy_name"),
                                    policy.get("policy_type")))
    return 0


def cmd_show_user(args):
    manager, out = _session(args)
    user = manager.get_user(args.user_id, args.user_name)
    if args.json:
        _emit(None, user, True)
    else:
        _human_user(user)
    return 0


def _emit_users(data):
    print("user_id | user_name | enabled")
    for user in data:
        print("%s | %s | %s" % (user.get("user_id"), user.get("user_name"),
                                user.get("enabled")))


def _session(args):
    backend = LazyBackend(lambda: build_backend(args))
    out = (lambda data: _emit(None, data, True)) if args.json else _default_out
    return Manager(backend, out), out


def _default_out(data):
    _print_kv(data)


HANDLERS = {
    "create-user": cmd_create_user,
    "create-group": cmd_create_group,
    "authorize": cmd_authorize,
    "add-user-to-group": cmd_add_user_to_group,
    "attach-policy": cmd_attach_policy,
    "list-users": cmd_list_users,
    "list-groups": cmd_list_groups,
    "list-policies": cmd_list_policies,
    "show-user": cmd_show_user,
}


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return HANDLERS[args.command](args)
    except ValidationError as exc:
        sys.stderr.write("[ERROR] 参数校验失败：%s\n" % exc.message)
        return 2
    except ConfirmationRequired as exc:
        sys.stderr.write("[CONFIRM] %s\n" % exc.message)
        return 2
    except IamError as exc:
        sys.stderr.write("[ERROR] %s\n" % exc.message)
        if exc.code:
            sys.stderr.write("  error_code: %s\n" % exc.code)
        if exc.hint:
            sys.stderr.write("  hint: %s\n" % exc.hint)
        return 1


if __name__ == "__main__":
    sys.exit(main())