"""Pydantic models for the twist rule configuration.

Defines Config, Rule, Match, Condition, and Action with full validation.
Replaces the manual validateCondition / validateAction logic from the Go
version with declarative Pydantic validators.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


class ConditionType(StrEnum):
    URL_EQUALS = "urlEquals"
    URL_PREFIX = "urlPrefix"
    URL_SUFFIX = "urlSuffix"
    URL_CONTAINS = "urlContains"
    URL_REGEX = "urlRegex"
    METHOD = "method"
    RESOURCE_TYPE = "resourceType"
    HEADER_EXISTS = "headerExists"
    HEADER_NOT_EXISTS = "headerNotExists"
    HEADER_EQUALS = "headerEquals"
    HEADER_CONTAINS = "headerContains"
    HEADER_REGEX = "headerRegex"
    QUERY_EXISTS = "queryExists"
    QUERY_NOT_EXISTS = "queryNotExists"
    QUERY_EQUALS = "queryEquals"
    QUERY_CONTAINS = "queryContains"
    QUERY_REGEX = "queryRegex"
    COOKIE_EXISTS = "cookieExists"
    COOKIE_NOT_EXISTS = "cookieNotExists"
    COOKIE_EQUALS = "cookieEquals"
    COOKIE_CONTAINS = "cookieContains"
    COOKIE_REGEX = "cookieRegex"
    BODY_CONTAINS = "bodyContains"
    BODY_REGEX = "bodyRegex"
    BODY_JSON_PATH = "bodyJsonPath"


class ActionType(StrEnum):
    BLOCK = "block"
    SET_HEADER = "setHeader"
    REMOVE_HEADER = "removeHeader"
    SET_URL = "setUrl"
    SET_METHOD = "setMethod"
    SET_QUERY_PARAM = "setQueryParam"
    REMOVE_QUERY_PARAM = "removeQueryParam"
    SET_COOKIE = "setCookie"
    REMOVE_COOKIE = "removeCookie"
    SET_FORM_FIELD = "setFormField"
    REMOVE_FORM_FIELD = "removeFormField"
    SET_STATUS = "setStatus"
    SET_BODY = "setBody"
    APPEND_BODY = "appendBody"
    REPLACE_BODY_TEXT = "replaceBodyText"
    PATCH_BODY_JSON = "patchBodyJson"
    REPLACE_ELEMENT = "replaceElement"


class Stage(StrEnum):
    REQUEST = "request"
    RESPONSE = "response"


# ---------------------------------------------------------------------------
# Condition
# ---------------------------------------------------------------------------

_VALUE_CONDITIONS = {
    ConditionType.URL_EQUALS,
    ConditionType.URL_PREFIX,
    ConditionType.URL_SUFFIX,
    ConditionType.URL_CONTAINS,
    ConditionType.BODY_CONTAINS,
}

_PATTERN_CONDITIONS = {
    ConditionType.URL_REGEX,
    ConditionType.BODY_REGEX,
}

_VALUES_CONDITIONS = {
    ConditionType.METHOD,
    ConditionType.RESOURCE_TYPE,
}

_NAME_ONLY_CONDITIONS = {
    ConditionType.HEADER_EXISTS,
    ConditionType.HEADER_NOT_EXISTS,
    ConditionType.QUERY_EXISTS,
    ConditionType.QUERY_NOT_EXISTS,
    ConditionType.COOKIE_EXISTS,
    ConditionType.COOKIE_NOT_EXISTS,
}

_NAME_VALUE_CONDITIONS = {
    ConditionType.HEADER_EQUALS,
    ConditionType.HEADER_CONTAINS,
    ConditionType.QUERY_EQUALS,
    ConditionType.QUERY_CONTAINS,
    ConditionType.COOKIE_EQUALS,
    ConditionType.COOKIE_CONTAINS,
}

_NAME_PATTERN_CONDITIONS = {
    ConditionType.HEADER_REGEX,
    ConditionType.QUERY_REGEX,
    ConditionType.COOKIE_REGEX,
}

_BODY_JSON_PATH = {ConditionType.BODY_JSON_PATH}


class Condition(BaseModel):
    """A single match condition for a rule."""

    type: ConditionType
    name: str = ""
    value: str = ""
    values: list[str] = Field(default_factory=list)
    pattern: str = ""
    path: str = ""

    @model_validator(mode="after")
    def _validate_fields(self) -> Condition:
        t = self.type

        if t in _VALUE_CONDITIONS and not self.value:
            raise ValueError(f"condition {t.value!r} requires field 'value'")

        if t in _PATTERN_CONDITIONS and not self.pattern:
            raise ValueError(f"condition {t.value!r} requires field 'pattern'")

        if t in _VALUES_CONDITIONS and not self.values:
            raise ValueError(f"condition {t.value!r} requires field 'values'")

        if t in _NAME_ONLY_CONDITIONS and not self.name:
            raise ValueError(f"condition {t.value!r} requires field 'name'")

        if t in _NAME_VALUE_CONDITIONS:
            if not self.name:
                raise ValueError(f"condition {t.value!r} requires field 'name'")
            if not self.value:
                raise ValueError(f"condition {t.value!r} requires field 'value'")

        if t in _NAME_PATTERN_CONDITIONS:
            if not self.name:
                raise ValueError(f"condition {t.value!r} requires field 'name'")
            if not self.pattern:
                raise ValueError(f"condition {t.value!r} requires field 'pattern'")

        if t in _BODY_JSON_PATH:
            if not self.path:
                raise ValueError(f"condition {t.value!r} requires field 'path'")
            if not self.value:
                raise ValueError(f"condition {t.value!r} requires field 'value'")

        return self


# ---------------------------------------------------------------------------
# Match
# ---------------------------------------------------------------------------


class Match(BaseModel):
    """Logical combination of conditions. Both allOf and anyOf can be specified."""

    model_config = {"populate_by_name": True}

    all_of: list[Condition] = Field(default_factory=list, alias="allOf")
    any_of: list[Condition] = Field(default_factory=list, alias="anyOf")


# ---------------------------------------------------------------------------
# JSON Patch (RFC 6902 subset)
# ---------------------------------------------------------------------------


class JSONPatchOp(StrEnum):
    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"
    MOVE = "move"
    COPY = "copy"
    TEST = "test"


class JSONPatch(BaseModel):
    """A single RFC 6902 JSON Patch operation."""

    model_config = {"populate_by_name": True}

    op: JSONPatchOp
    path: str
    from_: str = Field(default="", alias="from")
    value: Any = None


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------


class Action(BaseModel):
    """An action to execute when a rule matches."""

    model_config = {"populate_by_name": True}

    type: ActionType
    name: str = ""
    value: Any = None
    search: str = ""
    replace: str = ""
    replace_all: bool = Field(default=False, alias="replaceAll")
    status_code: int = Field(default=0, alias="statusCode")
    headers: dict[str, str] = Field(default_factory=dict)
    body: str = ""
    body_encoding: str = Field(default="", alias="bodyEncoding")
    encoding: str = ""
    patches: list[JSONPatch] = Field(default_factory=list)
    selector: str = ""

    @model_validator(mode="after")
    def _apply_defaults(self) -> Action:
        if self.type == ActionType.BLOCK:
            if self.status_code == 0:
                self.status_code = 200
            if not self.body_encoding:
                self.body_encoding = "text"
        if self.type == ActionType.SET_BODY and not self.encoding:
            self.encoding = "text"
        return self

    @model_validator(mode="after")
    def _validate_fields(self) -> Action:
        t = self.type

        if t in (
            ActionType.SET_URL,
            ActionType.SET_METHOD,
        ):
            if self.value is None:
                raise ValueError(f"action {t.value!r} requires field 'value'")

        if t in (
            ActionType.SET_QUERY_PARAM,
            ActionType.REMOVE_QUERY_PARAM,
            ActionType.SET_COOKIE,
            ActionType.REMOVE_COOKIE,
            ActionType.SET_FORM_FIELD,
            ActionType.REMOVE_FORM_FIELD,
            ActionType.SET_HEADER,
            ActionType.REMOVE_HEADER,
        ):
            if not self.name:
                raise ValueError(f"action {t.value!r} requires field 'name'")

        if t in (
            ActionType.SET_QUERY_PARAM,
            ActionType.SET_COOKIE,
            ActionType.SET_FORM_FIELD,
            ActionType.SET_HEADER,
        ):
            if self.value is None:
                raise ValueError(f"action {t.value!r} requires field 'value'")

        if t == ActionType.SET_STATUS and self.status_code == 0:
            raise ValueError(f"action {t.value!r} requires field 'statusCode'")

        if t in (ActionType.SET_BODY, ActionType.APPEND_BODY):
            if self.value is None:
                raise ValueError(f"action {t.value!r} requires field 'value'")

        if t == ActionType.REPLACE_BODY_TEXT:
            if not self.search:
                raise ValueError(f"action {t.value!r} requires field 'search'")
            if not self.replace:
                raise ValueError(f"action {t.value!r} requires field 'replace'")

        if t == ActionType.PATCH_BODY_JSON:
            if not self.patches:
                raise ValueError(f"action {t.value!r} requires field 'patches'")

        if t == ActionType.REPLACE_ELEMENT:
            if not self.selector:
                raise ValueError(f"action {t.value!r} requires field 'selector'")
            if self.value is None:
                raise ValueError(f"action {t.value!r} requires field 'value'")

        return self


# ---------------------------------------------------------------------------
# Rule
# ---------------------------------------------------------------------------


class Rule(BaseModel):
    """A single interception rule with match conditions and actions."""

    id: str
    name: str
    enabled: bool = True
    priority: int = 0
    stage: Literal["request", "response"] = "request"
    match: Match
    actions: list[Action]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


class Config(BaseModel):
    """Top-level configuration file."""

    id: str
    name: str
    version: str = "1.0"
    description: str = ""
    settings: dict[str, Any] = Field(default_factory=dict)
    rules: list[Rule]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_config(data: bytes | str) -> Config:
    """Parse and validate a JSON config string/bytes into a Config object."""
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    return Config.model_validate_json(data)
