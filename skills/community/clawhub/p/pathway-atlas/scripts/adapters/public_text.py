"""Bind host-observed semantic values to exact spans in saved public prose."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import math
import re
from types import MappingProxyType
from typing import Any

if __package__ == "scripts.adapters":
    from . import CellStatus, StructuredAdapterError, validate_public_locator
    from ..source_policy import canonicalize_provenance_url
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from adapters import CellStatus, StructuredAdapterError, validate_public_locator  # type: ignore
    from source_policy import canonicalize_provenance_url  # type: ignore


class PublicTextAdapterError(StructuredAdapterError):
    """A prose field is not bound to the supplied public source text."""


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError):
        raise PublicTextAdapterError("field value must be finite JSON data") from None


def _snapshot_json(value: Any) -> Any:
    return json.loads(_canonical_json(value))


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _safe_public_text(value: Any, name: str) -> str:
    # Source material is not report prose: official pages routinely contain
    # application URLs and public contact sections. Keep exact bounded input;
    # domain adapters still validate every value that can reach a report.
    if not isinstance(value, str) or not value or "\x00" in value:
        raise PublicTextAdapterError(f"{name} must be nonempty public text")
    if len(value.encode("utf-8")) > 4 * 1024 * 1024:
        raise PublicTextAdapterError(f"{name} exceeds the public document size limit")
    return value


def _field_name(value: Any) -> str:
    try:
        return validate_public_locator(value)
    except (TypeError, ValueError):
        raise PublicTextAdapterError("field name must be a safe public identifier") from None


@dataclass(frozen=True)
class PublicTextField:
    """One typed semantic value and the public quote that supports it."""

    value: Any = None
    quote: str | None = None
    start: int | None = None
    end: int | None = None
    status: CellStatus = CellStatus.EXACT

    def __post_init__(self) -> None:
        try:
            status = self.status if type(self.status) is CellStatus else CellStatus(self.status)
        except (TypeError, ValueError):
            raise PublicTextAdapterError("field status is invalid") from None
        value = _snapshot_json(self.value)
        if status is not CellStatus.EXACT and value is not None:
            raise PublicTextAdapterError("non-exact public text field cannot carry a value")
        if self.quote is not None:
            _safe_public_text(self.quote, "field quote")
        if (self.start is None) != (self.end is None):
            raise PublicTextAdapterError("field span requires both start and end")
        if self.start is not None and (
            isinstance(self.start, bool)
            or isinstance(self.end, bool)
            or not isinstance(self.start, int)
            or not isinstance(self.end, int)
            or self.start < 0
            or self.end <= self.start
        ):
            raise PublicTextAdapterError("field span must be an increasing integer range")
        if value is not None and self.quote is None:
            raise PublicTextAdapterError("field value requires an exact public quote")
        if self.quote is None and self.start is not None:
            raise PublicTextAdapterError("field span requires an exact public quote")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "value", value)

    @classmethod
    def missing(cls) -> "PublicTextField":
        """Retain that the field was absent without fabricating prose."""

        return cls()

    @classmethod
    def uncertain(
        cls,
        *,
        quote: str | None = None,
        start: int | None = None,
        end: int | None = None,
    ) -> "PublicTextField":
        """Retain observed but unusable prose without assigning a value."""

        return cls(quote=quote, start=start, end=end, status=CellStatus.UNCERTAIN)


@dataclass(frozen=True)
class PublicTextDocument:
    """Immutable saved public page text with source-bound semantic fields."""

    source_id: str
    url: str
    text: str
    text_hash: str
    fields: Mapping[str, PublicTextField]

    def __post_init__(self) -> None:
        raise TypeError("PublicTextDocument is factory-only; use bind_public_text")

    @classmethod
    def _create(cls, **values: Any) -> "PublicTextDocument":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance


def _semantic_value_is_grounded(value: Any, quote: str) -> bool:
    if value is None or isinstance(value, bool):
        return True
    if isinstance(value, int):
        return re.search(r"(?<![\d.+\-−])" + re.escape(str(value)) + r"(?![\d.])", quote) is not None
    if isinstance(value, float):
        return math.isfinite(value) and re.search(
            r"(?<![\d.+\-−])" + re.escape(format(value, "g")) + r"(?![\d.])", quote
        ) is not None
    if isinstance(value, str):
        return value in quote
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return all(_semantic_value_is_grounded(item, quote) for item in value)
    return True


def _bind_field(text: str, field: str, value: PublicTextField) -> PublicTextField:
    if type(value) is not PublicTextField:
        raise TypeError("fields must contain PublicTextField values")
    quote = value.quote
    if quote is None:
        return value
    start, end = value.start, value.end
    if start is None:
        if text.count(quote) != 1:
            raise PublicTextAdapterError(
                f"field {field} quote is ambiguous; provide an exact start/end span"
            )
        start = text.index(quote)
        end = start + len(quote)
    if end is None or end > len(text) or text[start:end] != quote:
        raise PublicTextAdapterError(f"field {field} span does not match its quote")
    if value.status is CellStatus.EXACT and not _semantic_value_is_grounded(value.value, quote):
        raise PublicTextAdapterError(
            f"field {field} semantic value is not grounded in its quote"
        )
    return PublicTextField(
        value=value.value,
        quote=quote,
        start=start,
        end=end,
        status=value.status,
    )


def bind_public_text(
    *,
    source_id: str,
    url: str,
    text: str,
    fields: Mapping[str, PublicTextField],
) -> PublicTextDocument:
    """Snapshot a public page and resolve every supplied quote to one exact span."""

    source_id = _field_name(source_id)
    try:
        canonical_url = canonicalize_provenance_url(url)
    except (TypeError, ValueError):
        raise PublicTextAdapterError(
            "url must identify a canonical public HTTP source"
        ) from None
    if canonical_url is None or not canonical_url.startswith(("http://", "https://")):
        raise PublicTextAdapterError("url must identify a canonical public HTTP source")
    text = _safe_public_text(text, "saved page text")
    if not isinstance(fields, Mapping):
        raise TypeError("fields must be a mapping")
    snapshot: dict[str, PublicTextField] = {}
    for field, value in fields.items():
        name = _field_name(field)
        if name in snapshot:
            raise PublicTextAdapterError("field names must not repeat")
        snapshot[name] = _bind_field(text, name, value)
    if not snapshot:
        raise PublicTextAdapterError("fields must contain at least one observation")
    return PublicTextDocument._create(
        source_id=source_id,
        url=canonical_url,
        text=text,
        text_hash=_text_hash(text),
        fields=MappingProxyType(dict(sorted(snapshot.items()))),
    )


def public_text_projection(
    document: PublicTextDocument,
    *,
    required_fields: Iterable[str],
    field_map: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Project arbitrary prose bindings into a required canonical field set."""

    if type(document) is not PublicTextDocument:
        raise TypeError("document must be a PublicTextDocument")
    required = tuple(_field_name(item) for item in required_fields)
    if not required or len(required) != len(set(required)):
        raise PublicTextAdapterError("required fields must be unique and nonempty")
    if field_map is None:
        mapping = {item: item for item in required if item in document.fields}
    elif not isinstance(field_map, Mapping):
        raise TypeError("field_map must be a mapping")
    else:
        mapping = dict(field_map)
    if not set(mapping).issubset(required):
        raise PublicTextAdapterError("public text field map contains an unknown canonical field")
    if any(not isinstance(value, str) for value in mapping.values()):
        raise PublicTextAdapterError("public text field map values must name source fields")
    if len(set(mapping.values())) != len(mapping):
        raise PublicTextAdapterError("public text field map must use unique source fields")

    projected: dict[str, Any] = {}
    for canonical in required:
        source_field = mapping.get(canonical)
        if source_field is None:
            selection = PublicTextField.missing()
        else:
            selection = document.fields.get(source_field)
            if selection is None:
                raise PublicTextAdapterError("mapped public text source field is absent")
        if selection.quote is None:
            locator = f"text[{document.text_hash[7:23]}]/field[{canonical}]/missing"
        else:
            locator = f"text[{selection.start}:{selection.end}]"
        warning = None
        if selection.value is None:
            warning = (
                f"{canonical}:missing"
                if selection.status is CellStatus.EXACT
                else f"{canonical}:{selection.status.value}"
            )
        projected[canonical] = {
            "value": selection.value,
            "cell_status": selection.status.value,
            "locator": validate_public_locator(locator),
            "warning": warning,
            "quote": selection.quote,
            "start": selection.start,
            "end": selection.end,
        }
    body = {
        "adapter_kind": "public-text",
        "extraction_method": "host-public-text",
        "source_id": document.source_id,
        "url": document.url,
        "text": document.text,
        "text_hash": document.text_hash,
        "fields": projected,
    }
    body["extraction_digest"] = _digest(body)
    return body


def validate_public_text_projection(
    value: Any,
    *,
    required_fields: Iterable[str],
) -> dict[str, Any]:
    """Replay raw prose and every field binding from a serialized projection."""

    expected = {
        "adapter_kind",
        "extraction_method",
        "source_id",
        "url",
        "text",
        "text_hash",
        "fields",
        "extraction_digest",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise PublicTextAdapterError("public text projection is incomplete")
    body = dict(value)
    claimed_digest = body.pop("extraction_digest")
    if claimed_digest != _digest(body):
        raise PublicTextAdapterError("public text extraction digest disagrees")
    if value["adapter_kind"] != "public-text" or value["extraction_method"] != "host-public-text":
        raise PublicTextAdapterError("public text extraction identity is invalid")
    source_id = _field_name(value["source_id"])
    try:
        url = canonicalize_provenance_url(value["url"])
    except (TypeError, ValueError):
        raise PublicTextAdapterError("public text URL is not canonical") from None
    if url is None or url != value["url"]:
        raise PublicTextAdapterError("public text URL is not canonical")
    text = _safe_public_text(value["text"], "saved page text")
    if value["text_hash"] != _text_hash(text):
        raise PublicTextAdapterError("public text hash disagrees")
    fields = value["fields"]
    required = tuple(required_fields)
    if not isinstance(fields, Mapping) or set(fields) != set(required):
        raise PublicTextAdapterError("public text field coverage is incomplete")
    for field in required:
        item = fields[field]
        if not isinstance(item, Mapping) or set(item) != {
            "value", "cell_status", "locator", "warning", "quote", "start", "end"
        }:
            raise PublicTextAdapterError("public text field projection is incomplete")
        selection = PublicTextField(
            value=item["value"],
            quote=item["quote"],
            start=item["start"],
            end=item["end"],
            status=item["cell_status"],
        )
        bound = _bind_field(text, field, selection)
        expected_locator = (
            f"text[{value['text_hash'][7:23]}]/field[{field}]/missing"
            if bound.quote is None
            else f"text[{bound.start}:{bound.end}]"
        )
        if item["locator"] != validate_public_locator(expected_locator):
            raise PublicTextAdapterError("public text field locator disagrees")
        expected_warning = None
        if bound.value is None:
            expected_warning = (
                f"{field}:missing"
                if bound.status is CellStatus.EXACT
                else f"{field}:{bound.status.value}"
            )
        if item["warning"] != expected_warning:
            raise PublicTextAdapterError("public text field warning disagrees")
    return dict(value)


__all__ = [
    "PublicTextAdapterError",
    "PublicTextDocument",
    "PublicTextField",
    "bind_public_text",
    "public_text_projection",
    "validate_public_text_projection",
]
