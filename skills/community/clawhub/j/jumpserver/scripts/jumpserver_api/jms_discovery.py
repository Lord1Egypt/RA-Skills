from __future__ import annotations

import copy

from .jms_types import EndpointSpec, JumpServerAPIError, PlatformSpec


CORE_ENDPOINTS = {
    "users": "/api/v1/users/users/",
    "groups": "/api/v1/users/groups/",
    "nodes": "/api/v1/assets/nodes/",
    "hosts": "/api/v1/assets/hosts/",
    "assets": "/api/v1/assets/assets/",
    "databases": "/api/v1/assets/databases/",
    "accounts": "/api/v1/accounts/accounts/",
    "account_templates": "/api/v1/accounts/account-templates/",
    "permissions": "/api/v1/perms/asset-permissions/",
    "connect_method_acls": "/api/v1/acls/connect-method-acls/",
    "data_masking_rules": "/api/v1/acls/data-masking-rules/",
    "login_asset_acls": "/api/v1/acls/login-asset-acls/",
    "login_acls": "/api/v1/acls/login-acls/",
    "command_filter_acls": "/api/v1/acls/command-filter-acls/",
    "command_groups": "/api/v1/acls/command-groups/",
    "system_roles": "/api/v1/rbac/system-roles/",
    "org_roles": "/api/v1/rbac/org-roles/",
    "role_bindings": "/api/v1/rbac/role-bindings/",
    "org_role_bindings": "/api/v1/rbac/org-role-bindings/",
    "system_role_bindings": "/api/v1/rbac/system-role-bindings/",
    "platforms": "/api/v1/assets/platforms/",
    "protocols": "/api/v1/assets/protocols/",
    "virtual_accounts": "/api/v1/accounts/virtual-accounts/",
    "labels": "/api/v1/labels/labels/",
    "zones": "/api/v1/assets/zones/",
    "session_logs": "/api/v1/audits/user-sessions/",
    "terminal_sessions": "/api/v1/terminal/sessions/",
    "terminal_commands": "/api/v1/terminal/commands/",
    "operate_logs": "/api/v1/audits/operate-logs/",
    "login_logs": "/api/v1/audits/login-logs/",
    "ftp_logs": "/api/v1/audits/ftp-logs/",
    "password_change_logs": "/api/v1/audits/password-change-logs/",
    "job_logs": "/api/v1/audits/job-logs/",
    "tickets": "/api/v1/tickets/tickets/",
    "settings": "/api/v1/settings/setting/",
    "license_detail": "/api/v1/xpack/license/detail",
    "blocked_ips": "/api/v1/settings/security/block-ip/",
    "unlock_ip": "/api/v1/settings/security/unlock-ip/",
    "terminals": "/api/v1/terminal/terminals/",
    "command_storages": "/api/v1/terminal/command-storages/",
    "replay_storages": "/api/v1/terminal/replay-storages/",
}


def _to_lower(value):
    return str(value or "").strip().lower()


def _titleish(value):
    return _to_lower(value).replace("-", " ").replace("_", " ")


class JumpServerDiscovery(object):
    def __init__(self, client):
        self.client = client
        self._cache = {}

    def core_endpoint_specs(self, refresh=False):
        cache_key = "core_endpoint_specs"
        if not refresh and cache_key in self._cache:
            return copy.deepcopy(self._cache[cache_key])
        specs = {}
        for name, path in CORE_ENDPOINTS.items():
            data = self.client.options(path)
            methods = []
            if isinstance(data, dict):
                methods = sorted([item.upper() for item in (data.get("actions") or {}).keys()])
                allow = data.get("allow")
                if allow and not methods:
                    methods = [part.strip() for part in allow.split(",") if part.strip()]
            specs[name] = EndpointSpec(
                path=path,
                methods=methods,
                request_schema=(data or {}).get("actions") if isinstance(data, dict) else {},
                source="live",
            )
        self._cache[cache_key] = specs
        return copy.deepcopy(specs)

    def core_inventory_payload(self, refresh=False):
        specs = self.core_endpoint_specs(refresh=refresh)
        return {
            "base_url": self.client.base_url,
            "org_id": self.client.config.org_id,
            "endpoints": {name: spec.to_dict() for name, spec in specs.items()},
        }

    def core_inventory_markdown(self, refresh=False):
        specs = self.core_endpoint_specs(refresh=refresh)
        lines = [
            "# JumpServer Core API Inventory",
            "",
            "- Base URL: `%s`" % self.client.base_url,
            "- Org ID: `%s`" % self.client.config.org_id,
            "",
        ]
        for name in sorted(specs):
            spec = specs[name]
            lines.extend(
                [
                    "## `%s`" % spec.path,
                    "",
                    "- Alias: `%s`" % name,
                    "- Methods: %s" % (", ".join(spec.methods) if spec.methods else "Unknown"),
                    "",
                ]
            )
        return "\n".join(lines) + "\n"

    def list_platforms(self, category=None, refresh=False):
        cache_key = "platforms"
        if refresh or cache_key not in self._cache:
            items = self.client.list_paginated(CORE_ENDPOINTS["platforms"])
            self._cache[cache_key] = [PlatformSpec.from_api(item) for item in items]
        platforms = list(self._cache[cache_key])
        if category:
            platforms = [item for item in platforms if _to_lower(item.category) == _to_lower(category)]
        return platforms

    def get_platform_by_type(self, platform_type):
        wanted = _to_lower(platform_type)
        for platform in self.list_platforms():
            if _to_lower(platform.slug) == wanted or _titleish(platform.name) == _titleish(wanted):
                return platform
        raise JumpServerAPIError("Platform not found for type/name: %s" % platform_type)

    def list_database_platforms(self):
        return self.list_platforms(category="database")

    def list_protocols(self):
        return self.client.list_paginated(CORE_ENDPOINTS["protocols"])

    def list_virtual_accounts(self):
        return self.client.list_paginated(CORE_ENDPOINTS["virtual_accounts"])

    def asset_permission_schema(self, refresh=False):
        cache_key = "asset_permission_schema"
        if refresh or cache_key not in self._cache:
            data = self.client.options(CORE_ENDPOINTS["permissions"])
            self._cache[cache_key] = data.get("actions", {}).get("POST", {}) if isinstance(data, dict) else {}
        return copy.deepcopy(self._cache[cache_key])

    def asset_permission_defaults(self):
        schema = self.asset_permission_schema()
        action_values = []
        for item in schema.get("actions", {}).get("default", []) or []:
            if isinstance(item, dict):
                action_values.append(item.get("value"))
            else:
                action_values.append(item)
        protocols = schema.get("protocols", {}).get("default") or ["all"]
        return {"actions": [item for item in action_values if item], "protocols": list(protocols)}

    def _list_cached(self, key, path, refresh=False):
        if refresh or key not in self._cache:
            self._cache[key] = self.client.list_paginated(path)
        return copy.deepcopy(self._cache[key])

    def list_users(self, refresh=False):
        return self._list_cached("users", CORE_ENDPOINTS["users"], refresh=refresh)

    def list_user_groups(self, refresh=False):
        return self._list_cached("groups", CORE_ENDPOINTS["groups"], refresh=refresh)

    def list_assets(self, refresh=False):
        return self._list_cached("assets", CORE_ENDPOINTS["assets"], refresh=refresh)

    def list_nodes(self, refresh=False):
        return self._list_cached("nodes", CORE_ENDPOINTS["nodes"], refresh=refresh)

    def list_system_roles(self, refresh=False):
        return self._list_cached("system_roles", CORE_ENDPOINTS["system_roles"], refresh=refresh)

    def list_org_roles(self, refresh=False):
        return self._list_cached("org_roles", CORE_ENDPOINTS["org_roles"], refresh=refresh)

    def _resolve_many(self, items, names, candidate_fields):
        if not names:
            return []
        resolved = []
        missing = []
        for raw_name in names:
            wanted = _to_lower(raw_name)
            match = None
            for item in items:
                for field in candidate_fields:
                    value = item.get(field)
                    if value is None and isinstance(item.get(field.split(".")[0]), dict):
                        head, tail = field.split(".", 1)
                        value = item.get(head, {}).get(tail)
                    if _to_lower(value) == wanted or _titleish(value) == _titleish(wanted):
                        match = item
                        break
                if match:
                    break
            if not match:
                for item in items:
                    haystacks = []
                    for field in candidate_fields:
                        value = item.get(field)
                        if value is None and "." in field:
                            head, tail = field.split(".", 1)
                            value = item.get(head, {}).get(tail)
                        haystacks.append(_titleish(value))
                    if any(wanted in hay for hay in haystacks if hay):
                        match = item
                        break
            if not match:
                missing.append(raw_name)
            else:
                resolved.append(match["id"])
        if missing:
            raise JumpServerAPIError("Unable to resolve names: %s" % ", ".join(missing))
        return resolved

    def resolve_user_ids(self, names):
        return self._resolve_many(self.list_users(), names, ("name", "username"))

    def resolve_group_ids(self, names):
        return self._resolve_many(self.list_user_groups(), names, ("name",))

    def resolve_system_role_ids(self, names):
        return self._resolve_many(self.list_system_roles(), names, ("name", "display_name"))

    def resolve_org_role_ids(self, names):
        return self._resolve_many(self.list_org_roles(), names, ("name", "display_name"))

    def resolve_node_ids(self, names_or_paths):
        return self._resolve_many(self.list_nodes(), names_or_paths, ("name", "value", "full_value"))

    def resolve_asset_ids(self, names):
        return self._resolve_many(self.list_assets(), names, ("name", "address"))

    def list_accounts(self):
        return self.client.list_paginated(CORE_ENDPOINTS["accounts"])

    def account_names_for_assets(self, asset_ids):
        asset_ids = set(asset_ids or [])
        names = []
        for account in self.list_accounts():
            asset = account.get("asset") or {}
            if asset.get("id") in asset_ids:
                name = account.get("name") or account.get("username")
                if name:
                    names.append(name)
        return sorted(set(names))
