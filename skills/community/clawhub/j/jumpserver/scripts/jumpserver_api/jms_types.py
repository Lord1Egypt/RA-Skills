from __future__ import annotations

from copy import deepcopy


class JumpServerAPIError(Exception):
    def __init__(
        self,
        message,
        status_code=None,
        method=None,
        path=None,
        details=None,
    ):
        self.message = message
        self.status_code = status_code
        self.method = method
        self.path = path
        self.details = details
        super().__init__(self.__str__())

    def __str__(self):
        parts = [self.message]
        if self.method and self.path:
            parts.append("(%s %s)" % (self.method, self.path))
        if self.status_code is not None:
            parts.append("[status=%s]" % self.status_code)
        if self.details:
            parts.append(str(self.details))
        return " ".join(parts)


class JumpServerConfig(object):
    def __init__(
        self,
        base_url,
        access_key="",
        secret_key="",
        username="",
        password="",
        org_id="",
        verify_tls=False,
        test_defaults=None,
        database_targets=None,
    ):
        self.base_url = (base_url or "").rstrip("/")
        self.access_key = access_key or ""
        self.secret_key = secret_key or ""
        self.username = username or ""
        self.password = password or ""
        self.org_id = org_id or ""
        self.verify_tls = bool(verify_tls)
        self.test_defaults = deepcopy(test_defaults or {})
        self.database_targets = deepcopy(database_targets or {})

    @classmethod
    def from_dict(cls, raw):
        if not isinstance(raw, dict):
            raise JumpServerAPIError("Config payload must be a mapping.")
        return cls(
            base_url=raw.get("base_url", ""),
            access_key=raw.get("access_key", ""),
            secret_key=raw.get("secret_key", ""),
            username=raw.get("username", ""),
            password=raw.get("password", ""),
            org_id=raw.get("org_id", ""),
            verify_tls=raw.get("verify_tls", False),
            test_defaults=raw.get("test_defaults") or {},
            database_targets=raw.get("database_targets") or {},
        )

    def uses_access_key_auth(self):
        return bool(self.access_key and self.secret_key)

    def uses_password_auth(self):
        return bool(self.username and self.password)

    def auth_mode(self):
        if self.uses_access_key_auth():
            return "aksk"
        if self.uses_password_auth():
            return "password"
        return ""

    def validate(self, *, require_org_id: bool = True):
        missing = []
        required_fields = ["base_url"]
        if require_org_id:
            required_fields.append("org_id")
        for field in required_fields:
            if not getattr(self, field):
                missing.append(field)

        has_aksk = self.uses_access_key_auth()
        has_password_auth = self.uses_password_auth()
        auth_missing = []
        if not has_aksk and not has_password_auth:
            if self.access_key and not self.secret_key:
                auth_missing.append("secret_key")
            if self.secret_key and not self.access_key:
                auth_missing.append("access_key")
            if self.username and not self.password:
                auth_missing.append("password")
            if self.password and not self.username:
                auth_missing.append("username")
            if not auth_missing:
                auth_missing.append("access_key/secret_key or username/password")
        missing.extend(auth_missing)

        if missing:
            raise JumpServerAPIError(
                "Missing required config fields: %s" % ", ".join(missing)
            )
        return self

    def to_dict(self):
        return {
            "base_url": self.base_url,
            "access_key": self.access_key,
            "secret_key": self.secret_key,
            "username": self.username,
            "password": self.password,
            "org_id": self.org_id,
            "verify_tls": self.verify_tls,
            "test_defaults": deepcopy(self.test_defaults),
            "database_targets": deepcopy(self.database_targets),
        }


class EndpointSpec(object):
    def __init__(self, path, methods=None, request_schema=None, source="live"):
        self.path = path
        self.methods = list(methods or [])
        self.request_schema = deepcopy(request_schema or {})
        self.source = source

    @classmethod
    def from_dict(cls, raw):
        return cls(
            path=raw.get("path", ""),
            methods=raw.get("methods") or [],
            request_schema=raw.get("request_schema") or {},
            source=raw.get("source", "live"),
        )

    def to_dict(self):
        return {
            "path": self.path,
            "methods": list(self.methods),
            "request_schema": deepcopy(self.request_schema),
            "source": self.source,
        }


class PlatformSpec(object):
    def __init__(
        self,
        platform_id,
        name,
        slug,
        category,
        protocols=None,
        automation=None,
        raw=None,
    ):
        self.id = platform_id
        self.name = name
        self.slug = slug
        self.category = category
        self.protocols = deepcopy(protocols or [])
        self.automation = deepcopy(automation or {})
        self.raw = deepcopy(raw or {})

    @classmethod
    def from_api(cls, raw):
        category = raw.get("category") or {}
        type_value = raw.get("type") or {}
        return cls(
            platform_id=raw.get("id"),
            name=raw.get("name", ""),
            slug=type_value.get("value") or raw.get("name", "").lower(),
            category=category.get("value") or "",
            protocols=raw.get("protocols") or [],
            automation=raw.get("automation") or {},
            raw=raw,
        )

    def default_protocols(self):
        chosen = []
        for item in self.protocols:
            if item.get("required") or item.get("primary") or item.get("default"):
                chosen.append({"name": item.get("name"), "port": item.get("port")})
        if not chosen and self.protocols:
            chosen.append(
                {
                    "name": self.protocols[0].get("name"),
                    "port": self.protocols[0].get("port"),
                }
            )
        return chosen

    def default_database_name(self):
        defaults = {
            "clickhouse": "default",
            "db2": "SAMPLE",
            "dameng": "SYSDBA",
            "mariadb": "mysql",
            "mongodb": "admin",
            "mysql": "mysql",
            "oracle": "ORCLCDB",
            "postgresql": "postgres",
            "redis": "0",
            "sqlserver": "master",
        }
        return defaults.get(self.slug, "")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "category": self.category,
            "protocols": deepcopy(self.protocols),
            "automation": deepcopy(self.automation),
            "raw": deepcopy(self.raw),
        }

