"""Strict, metadata-driven discovery for province datasets.

Only a fixed ``province.json`` immediately below each direct child directory is
considered.  Metadata names identify datasets; metadata never supplies a path.
"""

from __future__ import annotations

import json
import math
import os
import stat
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__:
    from .contracts import OrdinaryBatchPolicy
else:
    from contracts import OrdinaryBatchPolicy


class ProvinceRegistryError(ValueError):
    """Base class for controlled province-registry failures."""


class ProvincePathError(ProvinceRegistryError):
    """The registry root or a candidate path could not be trusted."""


class ProvinceConfigError(ProvinceRegistryError):
    """A province metadata document violates the public contract."""


class DuplicateProvinceError(ProvinceConfigError):
    """Two direct child datasets declare the same province name."""


class UnknownProvinceError(ProvinceRegistryError):
    """The requested province is absent from the discovered registry."""


class SubjectSelectionError(ProvinceRegistryError):
    """A selected subject group is invalid for a province configuration."""


_REPARSE_POINT = 0x0400
_SCHEMA_VERSION = "1.0"
_MODES = frozenset(("3+1+2", "3+3"))
_PRIMARY_312_SUBJECTS = ("物理", "历史")
_SECONDARY_312_SUBJECTS = ("化学", "生物", "政治", "地理")
_SUBJECTS_33 = ("物理", "化学", "生物", "政治", "历史", "地理")
_REQUIRED_FIELDS = frozenset(
    (
        "province",
        "mode",
        "primary_subjects",
        "secondary_subjects",
        "score_scale",
        "schema_version",
        "ordinary_batch_policy",
    )
)
_MAX_METADATA_BYTES = 256 * 1024


@dataclass(frozen=True)
class ProvinceConfig:
    """Validated, immutable province metadata plus its verified directory."""

    province: str
    mode: str
    primary_subjects: tuple[str, ...]
    secondary_subjects: tuple[str, ...]
    score_scale: int | float
    schema_version: str
    ordinary_batch_policy: OrdinaryBatchPolicy
    directory: Path

    def to_dict(self) -> dict[str, Any]:
        return {
            "province": self.province,
            "mode": self.mode,
            "primary_subjects": list(self.primary_subjects),
            "secondary_subjects": list(self.secondary_subjects),
            "score_scale": self.score_scale,
            "schema_version": self.schema_version,
            "ordinary_batch_policy": self.ordinary_batch_policy.to_dict(),
            "directory": str(self.directory),
        }


@dataclass(frozen=True)
class _DirectoryIdentity:
    path: Path
    device: int
    inode: int
    attributes: int

    @classmethod
    def capture(cls, value: os.PathLike[str] | str, description: str) -> "_DirectoryIdentity":
        requested = Path(value)
        try:
            absolute = Path(os.path.abspath(os.fspath(requested)))
            info = os.lstat(absolute)
            resolved = absolute.resolve(strict=True)
            resolved_info = os.lstat(resolved)
        except (OSError, RuntimeError, TypeError, ValueError) as error:
            raise ProvincePathError(f"{description}不可访问或不存在") from error
        attributes = getattr(info, "st_file_attributes", 0)
        resolved_attributes = getattr(resolved_info, "st_file_attributes", 0)
        if (
            not stat.S_ISDIR(info.st_mode)
            or stat.S_ISLNK(info.st_mode)
            or attributes & _REPARSE_POINT
            or not stat.S_ISDIR(resolved_info.st_mode)
            or stat.S_ISLNK(resolved_info.st_mode)
            or resolved_attributes & _REPARSE_POINT
            or (info.st_dev, info.st_ino) != (resolved_info.st_dev, resolved_info.st_ino)
        ):
            raise ProvincePathError(f"{description}必须是真实目录，不能是链接或重解析点")
        return cls(
            resolved,
            resolved_info.st_dev,
            resolved_info.st_ino,
            resolved_attributes,
        )

    def verify(self, description: str) -> None:
        try:
            info = os.lstat(self.path)
            resolved = self.path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise ProvincePathError(f"{description}在扫描期间发生变化") from error
        attributes = getattr(info, "st_file_attributes", 0)
        if (
            resolved != self.path
            or not stat.S_ISDIR(info.st_mode)
            or stat.S_ISLNK(info.st_mode)
            or attributes & _REPARSE_POINT
            or (info.st_dev, info.st_ino, attributes) != (self.device, self.inode, self.attributes)
        ):
            raise ProvincePathError(f"{description}在扫描期间发生变化")


@dataclass(frozen=True)
class _FileIdentity:
    path: Path
    device: int
    inode: int
    attributes: int
    size: int
    modified_ns: int

    @classmethod
    def from_stat(cls, path: Path, info: os.stat_result) -> "_FileIdentity":
        return cls(
            path=path,
            device=info.st_dev,
            inode=info.st_ino,
            attributes=getattr(info, "st_file_attributes", 0),
            size=info.st_size,
            modified_ns=info.st_mtime_ns,
        )

    def verify(self) -> None:
        try:
            info = os.lstat(self.path)
            resolved = self.path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise ProvincePathError("province.json 在扫描期间发生变化") from error
        attributes = getattr(info, "st_file_attributes", 0)
        if (
            resolved != self.path
            or not stat.S_ISREG(info.st_mode)
            or stat.S_ISLNK(info.st_mode)
            or attributes & _REPARSE_POINT
            or (
                info.st_dev,
                info.st_ino,
                attributes,
                info.st_size,
                info.st_mtime_ns,
            )
            != (
                self.device,
                self.inode,
                self.attributes,
                self.size,
                self.modified_ns,
            )
        ):
            raise ProvincePathError("province.json 在扫描期间发生变化")


@dataclass(frozen=True)
class _MetadataDocument:
    child: _DirectoryIdentity
    metadata: _FileIdentity
    payload: dict[str, Any]

    def verify(self, root: _DirectoryIdentity) -> None:
        root.verify("省份数据根目录")
        self.child.verify("省份数据目录")
        self.metadata.verify()
        if (
            not _is_below(self.child.path, root.path)
            or not _is_below(self.metadata.path, self.child.path)
            or self.metadata.path != self.child.path / "province.json"
        ):
            raise ProvincePathError("省份元数据越出数据根目录")


def _is_below(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return path != root


def _reject_constant(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _read_metadata(root: _DirectoryIdentity, child: _DirectoryIdentity) -> _MetadataDocument | None:
    metadata = child.path / "province.json"
    try:
        before = os.lstat(metadata)
    except FileNotFoundError:
        child.verify("省份数据目录")
        root.verify("省份数据根目录")
        return None
    except OSError as error:
        raise ProvincePathError("province.json 无法安全读取") from error

    attributes = getattr(before, "st_file_attributes", 0)
    if (
        not stat.S_ISREG(before.st_mode)
        or stat.S_ISLNK(before.st_mode)
        or attributes & _REPARSE_POINT
        or not _is_below(metadata, root.path)
    ):
        raise ProvincePathError("province.json 必须是数据根目录内的真实普通文件")
    if before.st_size > _MAX_METADATA_BYTES:
        raise ProvinceConfigError("province.json 超过允许的元数据大小")
    metadata_identity = _FileIdentity.from_stat(metadata, before)

    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(metadata, flags)
        try:
            opened = os.fstat(descriptor)
            if (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ) != (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ):
                raise ProvincePathError("province.json 在读取期间发生变化")
            chunks: list[bytes] = []
            size = 0
            while True:
                chunk = os.read(descriptor, 64 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > _MAX_METADATA_BYTES:
                    raise ProvinceConfigError("province.json 超过允许的元数据大小")
                chunks.append(chunk)
        finally:
            os.close(descriptor)
    except ProvinceRegistryError:
        raise
    except OSError as error:
        raise ProvincePathError("province.json 无法安全读取") from error

    metadata_identity.verify()
    child.verify("省份数据目录")
    root.verify("省份数据根目录")

    try:
        text = b"".join(chunks).decode("utf-8")
        payload = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ProvinceConfigError("province.json 不是严格 UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise ProvinceConfigError("province.json 顶层必须是对象")
    return _MetadataDocument(child=child, metadata=metadata_identity, payload=payload)


def _normalize_province(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProvinceConfigError("province 必须是非空字符串")
    province = value.strip()
    if province in (".", "..") or any(marker in province for marker in ("/", "\\", "\0")):
        raise ProvinceConfigError("province 只能是显示名称，不能包含路径语法")
    return province


def _normalize_subjects(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ProvinceConfigError(f"{field} 必须是非空字符串数组")
    subjects: list[str] = []
    seen: set[str] = set()
    for item in value:
        if (
            not isinstance(item, str)
            or not item
            or item != item.strip()
            or "\r" in item
            or "\n" in item
        ):
            raise ProvinceConfigError(f"{field} 只能包含无需清洗的非空科目字符串")
        if item in seen:
            raise ProvinceConfigError(f"{field} 不得包含重复科目")
        seen.add(item)
        subjects.append(item)
    return tuple(subjects)


def validate_ordinary_batch_policy(payload: Any) -> OrdinaryBatchPolicy:
    """Apply the runtime semantic layer declared by province.schema.json."""

    if not isinstance(payload, dict):
        raise ProvinceConfigError("ordinary_batch_policy 必须是严格对象")
    try:
        return OrdinaryBatchPolicy(**payload)
    except (TypeError, ValueError) as error:
        raise ProvinceConfigError("ordinary_batch_policy 不符合严格策略契约") from error


def _parse_config(payload: dict[str, Any], directory: Path) -> ProvinceConfig:
    keys = frozenset(payload)
    if keys != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - keys)
        extra = sorted(keys - _REQUIRED_FIELDS)
        details = []
        if missing:
            details.append("缺少字段：" + "、".join(missing))
        if extra:
            details.append("未知字段：" + "、".join(extra))
        raise ProvinceConfigError("province.json 字段不符合契约（" + "；".join(details) + "）")

    province = _normalize_province(payload["province"])
    mode = payload["mode"]
    if not isinstance(mode, str) or mode not in _MODES:
        raise ProvinceConfigError("mode 仅支持 3+1+2 或 3+3")
    primary = _normalize_subjects(payload["primary_subjects"], "primary_subjects")
    secondary = _normalize_subjects(payload["secondary_subjects"], "secondary_subjects")
    if mode == "3+1+2" and len(secondary) < 2:
        raise ProvinceConfigError("3+1+2 模式至少需要两个可配置再选科目")
    if mode == "3+3" and len(primary) + len(secondary) < 3:
        raise ProvinceConfigError("3+3 模式至少需要三个不同的可配置科目")

    score_scale = payload["score_scale"]
    if (
        isinstance(score_scale, bool)
        or not isinstance(score_scale, (int, float))
        or not math.isfinite(score_scale)
        or not 100 <= score_scale <= 1000
    ):
        raise ProvinceConfigError("score_scale 必须是 100 到 1000 之间的有限正数")
    schema_version = payload["schema_version"]
    if not isinstance(schema_version, str) or schema_version != _SCHEMA_VERSION:
        raise ProvinceConfigError("不支持的 province schema_version（当前仅支持 1.0）")
    ordinary_batch_policy = validate_ordinary_batch_policy(
        payload["ordinary_batch_policy"]
    )

    return ProvinceConfig(
        province=province,
        mode=mode,
        primary_subjects=primary,
        secondary_subjects=secondary,
        score_scale=score_scale,
        schema_version=schema_version,
        ordinary_batch_policy=ordinary_batch_policy,
        directory=directory,
    )


def _scan_metadata(
    root: os.PathLike[str] | str,
) -> tuple[_DirectoryIdentity, list[_MetadataDocument]]:
    root_identity = _DirectoryIdentity.capture(root, "省份数据根目录")
    documents: list[_MetadataDocument] = []
    try:
        with os.scandir(root_identity.path) as iterator:
            entries = sorted(iterator, key=lambda entry: entry.name)
    except OSError as error:
        raise ProvincePathError("省份数据根目录无法扫描") from error
    for entry in entries:
        try:
            info = entry.stat(follow_symlinks=False)
        except OSError as error:
            raise ProvincePathError("省份数据根目录包含无法验证的条目") from error
        attributes = getattr(info, "st_file_attributes", 0)
        if entry.is_symlink() or attributes & _REPARSE_POINT:
            raise ProvincePathError("省份数据根目录不能包含链接或重解析点")
        if not stat.S_ISDIR(info.st_mode):
            continue
        child = _DirectoryIdentity.capture(Path(entry.path), "省份数据目录")
        if not _is_below(child.path, root_identity.path):
            raise ProvincePathError("省份数据目录越出数据根目录")
        document = _read_metadata(root_identity, child)
        if document is not None:
            documents.append(document)
    root_identity.verify("省份数据根目录")
    return root_identity, documents


def _discover_strict_records(
    root: os.PathLike[str] | str,
) -> tuple[_DirectoryIdentity, dict[str, tuple[ProvinceConfig, _MetadataDocument]]]:
    root_identity, documents = _scan_metadata(root)
    discovered: dict[str, tuple[ProvinceConfig, _MetadataDocument]] = {}
    for document in documents:
        config = _parse_config(document.payload, document.child.path)
        if config.province in discovered:
            raise DuplicateProvinceError(f"省份名称重复：{config.province}")
        discovered[config.province] = (config, document)
    return root_identity, dict(sorted(discovered.items()))


def discover_provinces(root: os.PathLike[str] | str) -> dict[str, ProvinceConfig]:
    """Discover strict province metadata from direct child directories only."""

    _root, records = _discover_strict_records(root)
    return {name: record[0] for name, record in records.items()}


def resolve_province_dir(root: os.PathLike[str] | str, province: str) -> Path:
    """Resolve a dataset by metadata display name, never by path concatenation."""

    return _resolve_province_dir(root, province)


def _resolve_province_dir(
    root: os.PathLike[str] | str,
    province: str,
    operation_hook: Callable[[], None] | None = None,
) -> Path:
    """Internal resolver with a deterministic post-discovery race-test seam."""

    root_identity, records = _discover_strict_records(root)
    if not isinstance(province, str) or province not in records:
        available = "、".join(sorted(records)) or "无"
        raise UnknownProvinceError(f"未知省份「{province}」；可用省份：{available}")
    config, document = records[province]
    if operation_hook is not None:
        operation_hook()
    document.verify(root_identity)
    return config.directory


def _resolve_legacy_province_dir(root: os.PathLike[str] | str, province: str) -> Path:
    """Resolve strict v1 or unmistakable pre-v1 metadata for one release."""

    root_identity, documents = _scan_metadata(root)
    records: dict[str, _MetadataDocument] = {}
    for document in documents:
        payload = document.payload
        if "schema_version" in payload:
            name = _parse_config(payload, document.child.path).province
        else:
            if "province" not in payload or "subject_groups" not in payload:
                raise ProvinceConfigError(
                    "无 schema_version 的 province.json 必须包含旧版 subject_groups 标记"
                )
            name = _normalize_province(payload["province"])
            legacy_subjects = payload["subject_groups"]
            if (
                not isinstance(legacy_subjects, list)
                or not legacy_subjects
                or any(not isinstance(item, str) or not item.strip() for item in legacy_subjects)
            ):
                raise ProvinceConfigError("旧版 subject_groups 必须是非空科目字符串数组")
        if name in records:
            raise DuplicateProvinceError(f"省份名称重复：{name}")
        records[name] = document
    if province not in records:
        available = "、".join(sorted(records)) or "无"
        raise UnknownProvinceError(f"未知省份「{province}」；可用省份：{available}")
    selected = records[province]
    selected.verify(root_identity)
    return selected.child.path


def _normalize_selection(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SubjectSelectionError(f"{field}必须是一个非空科目名称")
    return value.strip()


def validate_subject_selection(
    config: ProvinceConfig,
    primary: str,
    secondary: tuple[str, ...] | list[str],
) -> None:
    """Validate a complete subject selection according to the declared mode."""

    if not isinstance(config, ProvinceConfig):
        raise SubjectSelectionError("省份配置无效")
    primary_value = _normalize_selection(primary, "首选科目")
    if isinstance(secondary, (str, bytes)) or not isinstance(secondary, (tuple, list)):
        raise SubjectSelectionError("再选科目必须是科目列表")
    secondary_values = tuple(_normalize_selection(item, "再选科目") for item in secondary)
    if len(secondary_values) != 2:
        raise SubjectSelectionError("必须选择恰好两个再选科目")
    if len(set(secondary_values)) != 2:
        raise SubjectSelectionError("三个选科必须互不重复")

    if config.mode == "3+1+2":
        if primary_value not in config.primary_subjects:
            choices = "、".join(config.primary_subjects)
            raise SubjectSelectionError(f"首选科目无效；可选：{choices}")
        unknown = sorted(set(secondary_values) - set(config.secondary_subjects))
        if unknown:
            choices = "、".join(config.secondary_subjects)
            raise SubjectSelectionError(f"再选科目无效；可选：{choices}")
        if primary_value in secondary_values:
            raise SubjectSelectionError("三个选科必须互不重复")
        return

    allowed = set(config.primary_subjects) | set(config.secondary_subjects)
    selection = (primary_value,) + secondary_values
    if len(set(selection)) != 3:
        raise SubjectSelectionError("3+3 模式必须选择三个不同科目")
    unknown = sorted(set(selection) - allowed)
    if unknown:
        choices = "、".join(sorted(allowed))
        raise SubjectSelectionError(f"3+3 选科包含未配置科目；可选：{choices}")


def canonical_subject_selection_key(
    config: ProvinceConfig,
    primary: str,
    secondary: tuple[str, ...] | list[str],
) -> str:
    """Return the one mode-aware dataset/evidence key after full validation."""

    validate_subject_selection(config, primary, secondary)
    primary_value = _normalize_selection(primary, "首选科目")
    if config.mode == "3+1+2":
        return primary_value
    selected = {primary_value, *(_normalize_selection(item, "再选科目") for item in secondary)}
    ordered: list[str] = []
    for subject in (*config.primary_subjects, *config.secondary_subjects):
        if subject in selected and subject not in ordered:
            ordered.append(subject)
    if len(ordered) != 3:
        raise SubjectSelectionError("3+3 模式必须形成三个不同的已配置科目")
    return "+".join(ordered)


def discovery_subjects_33(*, province: str | None = None) -> tuple[str, ...]:
    """Return the stable 3+3 order, including Zhejiang's seventh subject."""

    return _SUBJECTS_33 + (("技术",) if province in ("浙江", "浙江省") else ())


def canonical_discovery_subject_key(
    mode: str,
    primary: str,
    secondary: tuple[str, ...] | list[str],
    *,
    province: str | None = None,
) -> str:
    """Validate subjects using the stable mode and province-specific vocabulary.

    Public research planning must not load a caller-authored ``province.json``.
    This stable discovery projection intentionally knows no score, admission,
    or recommendation thresholds. Zhejiang adds 技术 to the six-subject 3+3
    vocabulary. Omitted province retains the original six-subject contract;
    public callers must pass their validated province. Append new subjects so
    existing canonical keys and query identities do not change.
    """

    if mode not in _MODES:
        raise SubjectSelectionError("考试模式仅支持 3+1+2 或 3+3")
    primary_value = _normalize_selection(primary, "首选科目")
    if isinstance(secondary, (str, bytes)) or not isinstance(secondary, (tuple, list)):
        raise SubjectSelectionError("再选科目必须是科目列表")
    secondary_values = tuple(_normalize_selection(item, "再选科目") for item in secondary)
    if len(secondary_values) != 2 or len({primary_value, *secondary_values}) != 3:
        raise SubjectSelectionError("必须形成三个互不重复的选科")
    if mode == "3+1+2":
        if primary_value not in _PRIMARY_312_SUBJECTS:
            raise SubjectSelectionError("3+1+2 首选科目必须是物理或历史")
        if any(item not in _SECONDARY_312_SUBJECTS for item in secondary_values):
            raise SubjectSelectionError("3+1+2 再选科目不在稳定科目词表中")
        selected_secondary = set(secondary_values)
        ordered_secondary = tuple(
            item for item in _SECONDARY_312_SUBJECTS if item in selected_secondary
        )
        return "+".join((primary_value, *ordered_secondary))
    selected = {primary_value, *secondary_values}
    subjects = discovery_subjects_33(province=province)
    if any(item not in subjects for item in selected):
        raise SubjectSelectionError("3+3 选科不在稳定科目词表中")
    return "+".join(item for item in subjects if item in selected)
