# -*- coding: utf-8 -*-
"""数据加载层：按显式省份目录、科目组和年份加载 CSV，并做完整性自检。

自检原则（spec §4.5 / 任务票 AC）：行数为 0、缺科目组/年份、缺文件
一律明确报错并指明缺哪份数据，绝不静默返回空推荐。
"""
import csv
import io
import json
import os
import stat
import warnings
from collections.abc import Callable
from pathlib import Path

try:
    from scripts.province_registry import (
        ProvinceRegistryError,
        _DirectoryIdentity,
        _resolve_legacy_province_dir,
    )
except ModuleNotFoundError:  # Direct ``python scripts/*.py`` compatibility.
    from province_registry import (  # type: ignore
        ProvinceRegistryError,
        _DirectoryIdentity,
        _resolve_legacy_province_dir,
    )

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_ROOT = os.path.join(SKILL_ROOT, "data")

INT_FIELDS = {
    "yifenyiduan": ("year", "score", "rank", "cumulative_count"),
    "tou_dang": ("year", "min_score", "min_rank", "is_inside_hubei"),
    "schools": ("is_in_hubei",),
    "qiangji": ("year", "enrollment_plan", "min_admission_rank"),
    "zongping": ("year", "min_admission_rank"),
    "gangao": ("year", "estimated_rank", "interview_required"),
}

FLOAT_FIELDS = {
    "qiangji": ("min_admission_score",),
    "zongping": ("min_admission_score",),
    "gangao": ("estimated_score",),
}

# 可选的多元升学路径数据表；具体覆盖范围由调用方提供的数据集声明。
PATH_TABLES = ("qiangji", "zongping", "gangao")

MAX_CSV_BYTES = 16 * 1024 * 1024
MAX_CSV_ROWS = 250_000
_REPARSE_POINT = 0x0400


class DataError(Exception):
    """数据缺失/损坏的业务错误，message 必须指明缺哪份数据。"""


def _read_csv_records(
    path: os.PathLike[str] | str,
    *,
    _parent_identity: _DirectoryIdentity | None = None,
    _operation_hook: Callable[[], None] | None = None,
) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    """Read one bounded, strict UTF-8 regular CSV without following links."""

    candidate = Path(path)
    try:
        absolute = Path(os.path.abspath(os.fspath(candidate)))
        parent_identity = _parent_identity or _DirectoryIdentity.capture(
            absolute.parent, "CSV 父目录"
        )
        if absolute.parent.resolve(strict=True) != parent_identity.path:
            raise DataError(f"CSV 必须位于已验证父目录内：{absolute}")
        absolute = parent_identity.path / absolute.name
        parent_identity.verify("CSV 父目录")
        before = os.lstat(absolute)
        attributes = getattr(before, "st_file_attributes", 0)
        if (
            absolute.resolve(strict=True) != absolute
            or not stat.S_ISREG(before.st_mode)
            or stat.S_ISLNK(before.st_mode)
            or attributes & _REPARSE_POINT
        ):
            raise DataError(f"CSV 必须是真实普通文件，不能是链接或重解析点：{absolute}")
        if before.st_size > MAX_CSV_BYTES:
            raise DataError(f"CSV 超过 {MAX_CSV_BYTES} 字节上限：{absolute}")

        if _operation_hook is not None:
            _operation_hook()
        parent_identity.verify("CSV 父目录")

        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        directory_descriptor = None
        descriptor = None
        try:
            if os.open in os.supports_dir_fd and hasattr(os, "O_DIRECTORY"):
                directory_descriptor = os.open(
                    parent_identity.path,
                    os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0),
                )
                opened_parent = os.fstat(directory_descriptor)
                if (opened_parent.st_dev, opened_parent.st_ino) != (
                    parent_identity.device,
                    parent_identity.inode,
                ):
                    raise DataError(f"CSV 父目录在读取期间发生变化：{absolute.parent}")
                descriptor = os.open(absolute.name, flags, dir_fd=directory_descriptor)
            else:
                descriptor = os.open(absolute, flags)
            opened = os.fstat(descriptor)
            opened_attributes = getattr(opened, "st_file_attributes", 0)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened_attributes & _REPARSE_POINT
                or (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
                != (
                    before.st_dev,
                    before.st_ino,
                    before.st_size,
                    before.st_mtime_ns,
                )
            ):
                raise DataError(f"CSV 在读取期间发生变化：{absolute}")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = os.read(descriptor, 64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_CSV_BYTES:
                    raise DataError(f"CSV 超过 {MAX_CSV_BYTES} 字节上限：{absolute}")
                chunks.append(chunk)
        finally:
            if descriptor is not None:
                os.close(descriptor)
            if directory_descriptor is not None:
                os.close(directory_descriptor)

        parent_identity.verify("CSV 父目录")
        after = os.lstat(absolute)
        after_attributes = getattr(after, "st_file_attributes", 0)
        if (
            absolute.resolve(strict=True) != absolute
            or not stat.S_ISREG(after.st_mode)
            or stat.S_ISLNK(after.st_mode)
            or after_attributes & _REPARSE_POINT
            or (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        ):
            raise DataError(f"CSV 在读取期间发生变化：{absolute}")
        parent_identity.verify("CSV 父目录")
        text = b"".join(chunks).decode("utf-8")
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        try:
            header_row = next(reader)
        except StopIteration:
            return (), []
        headers = tuple(header_row)
        if any(not field or field != field.strip() for field in headers):
            raise DataError(f"CSV 表头包含空字段或首尾空白：{absolute}")
        if len(headers) != len(set(headers)):
            raise DataError(f"CSV 表头包含重复字段：{absolute}")

        rows: list[dict[str, str]] = []
        for number, values in enumerate(reader, start=2):
            if number > MAX_CSV_ROWS + 1:
                raise DataError(f"CSV 超过 {MAX_CSV_ROWS} 行上限：{absolute}")
            if len(values) != len(headers):
                raise DataError(f"CSV 第 {number} 行列数与表头不一致：{absolute}")
            rows.append(dict(zip(headers, values)))
        return headers, rows
    except DataError:
        raise
    except UnicodeDecodeError as error:
        raise DataError(f"CSV 不是严格 UTF-8：{absolute}") from error
    except csv.Error as error:
        raise DataError(f"CSV 格式损坏：{absolute}") from error
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        raise DataError(f"CSV 无法安全读取：{candidate}") from error


def _normalize_alias(
    row: dict[str, str], canonical: str, alias: str
) -> dict[str, str]:
    normalized = dict(row)
    canonical_present = canonical in normalized
    alias_present = alias in normalized
    canonical_value = normalized.get(canonical, "").strip()
    alias_value = normalized.get(alias, "").strip()
    if canonical_present and alias_present and canonical_value != alias_value:
        raise DataError(f"字段 {canonical} 与迁移别名 {alias} 冲突")
    normalized[canonical] = canonical_value if canonical_present else alias_value
    normalized.pop(alias, None)
    return normalized


def _normalize_admission_row(row: dict[str, str]) -> dict[str, str]:
    normalized = _normalize_alias(row, "remarks", "remark")
    return _normalize_alias(normalized, "program_group", "major_group_name")


def load_admission_rows(path: os.PathLike[str] | str) -> list[dict[str, str]]:
    """Load admission rows with canonical ``remarks``/``program_group`` fields."""

    _headers, rows = _read_csv_records(path)
    return [_normalize_admission_row(row) for row in rows]


def get_province_dir(province: str, root: os.PathLike[str] | str = DEFAULT_DATA_ROOT) -> Path:
    """Deprecated name-based bridge; new callers pass an explicit province_dir.

    The compatibility resolver validates strict v1 metadata normally. Its
    narrow legacy classification requires a missing schema version plus the
    old ``subject_groups`` marker in the same safely scanned direct-child
    ``province.json`` file.
    """

    warnings.warn(
        "name-based province loading is deprecated; resolve once and pass province_dir",
        DeprecationWarning,
        stacklevel=2,
    )
    if not isinstance(province, str) or not province.strip():
        raise DataError("省份必填；请先解析省份数据目录")
    try:
        return _resolve_legacy_province_dir(root, province.strip())
    except ProvinceRegistryError as error:
        raise DataError(f"province.json 元数据解析失败：{error}") from error


def _province_dir(province: str, root: os.PathLike[str] | str) -> str:
    """Compatibility alias for callers that still resolve by province name."""

    return os.fspath(get_province_dir(province, root))


def _resolved_data_dir(
    province: str | None,
    root: os.PathLike[str] | str,
    province_dir: os.PathLike[str] | str | None,
) -> Path:
    if province_dir is not None:
        try:
            candidate = Path(province_dir)
            normalized = Path(os.path.abspath(os.fspath(candidate)))
            if not candidate.is_absolute() or candidate != normalized:
                raise DataError("province_dir 必须是调用方预先解析的绝对目录")
            return _DirectoryIdentity.capture(province_dir, "已解析省份数据目录").path
        except DataError:
            raise
        except (TypeError, ValueError) as error:
            raise DataError("province_dir 必须是调用方预先解析的绝对目录") from error
        except ProvinceRegistryError as error:
            raise DataError(str(error)) from error
    if province is None:
        raise DataError("必须提供显式 province_dir；旧调用方可暂时提供 province")
    return get_province_dir(province, root)


def _load_csv(province_dir: Path, table: str, province_label: str,
              int_fields=(), required: bool = True) -> list[dict]:
    path = province_dir / f"{table}.csv"
    if not path.exists():
        if not required:
            return []
        raise DataError(f"数据文件缺失：{path}（{province_label} {table}），"
                        f"请先按省份接入文档准备该数据文件")
    fields = int_fields or INT_FIELDS.get(table, ())
    float_fields = FLOAT_FIELDS.get(table, ())
    if table == "tou_dang":
        raw_rows = load_admission_rows(path)
    else:
        _headers, raw_rows = _read_csv_records(path)
    rows = []
    for raw in raw_rows:
        row = dict(raw)
        for field in fields:
            value = row.get(field)
            row[field] = int(value) if value not in (None, "") else None
        for field in float_fields:
            value = row.get(field)
            row[field] = float(value) if value not in (None, "") else None
        if table == "tou_dang":
            row["major_group_name"] = row.get("program_group", "")
        rows.append(row)
    if not rows and required:
        raise DataError(f"数据文件为空：{path}（{province_label} {table}），"
                        f"不输出空推荐，请先导入数据")
    return rows


def load_province_config(province: str | None = None, root: os.PathLike[str] | str = DEFAULT_DATA_ROOT,
                         require_anchors: bool = True, *,
                         province_dir: os.PathLike[str] | str | None = None) -> dict:
    """加载省份配置（province.json）：科目组、锚点线集合、当年判定与展示参数。

    锚点线名称/数量/列映射全部来自配置，代码不假定具体锚点（spec §4.1）。
    require_anchors=True 时 anchors 缺失或不完整会明确报错；传 False
    时只要求配置文件本身存在且可解析。
    """
    directory = _resolved_data_dir(province, root, province_dir)
    label = province or directory.name
    path = directory / "province.json"
    if not path.exists():
        raise DataError(f"省份配置缺失：{path}（{label} province.json），"
                        f"请先按省份接入文档准备该配置文件")
    with path.open(encoding="utf-8") as f:
        config = json.load(f)
    if not require_anchors:
        return config
    anchors = config.get("anchors") or []
    if not anchors:
        raise DataError(f"省份配置 {path} 未定义任何锚点线（anchors 为空），"
                        f"无法进行校排名折算")
    for a in anchors:
        if not all(a.get(k) for k in ("name", "school_rank_col", "prov_rank_col")):
            raise DataError(f"省份配置 {path} 锚点定义不完整"
                            f"（需含 name/school_rank_col/prov_rank_col）：{a}")
    return config


def load_xibao(province: str | None, config: dict,
               root: os.PathLike[str] | str = DEFAULT_DATA_ROOT, *,
               province_dir: os.PathLike[str] | str | None = None) -> list[dict]:
    """加载喜报锚点数据；锚点列按省份配置解析为整数（配置驱动）。"""
    int_fields = {"year", "qingbei_count", "fenshu_600_count"}
    for a in config["anchors"]:
        int_fields.add(a["school_rank_col"])
        int_fields.add(a["prov_rank_col"])
    directory = _resolved_data_dir(province, root, province_dir)
    return _load_csv(directory, "xibao", province or directory.name,
                     int_fields=sorted(int_fields))


def load_schools(province: str | None = None, root: os.PathLike[str] | str = DEFAULT_DATA_ROOT, *,
                 province_dir: os.PathLike[str] | str | None = None) -> list[dict]:
    """加载可选高中名录；文件缺失时返回空表。"""
    directory = _resolved_data_dir(province, root, province_dir)
    return _load_csv(directory, "schools", province or directory.name, required=False)


def _latest(rows: list[dict], subject_group: str, table: str,
            province: str) -> tuple[int, list[dict]]:
    years = [r["year"] for r in rows if r["subject_group"] == subject_group]
    if not years:
        raise DataError(f"{province} {table} 数据无科目组「{subject_group}」的年份记录，"
                        f"不输出空推荐，请先导入对应数据")
    year = max(years)
    return year, [r for r in rows
                  if r["subject_group"] == subject_group and r["year"] == year]


def load_toudang(province: str | None = None, subject_group: str | None = None,
                 root: os.PathLike[str] | str = DEFAULT_DATA_ROOT, *,
                 province_dir: os.PathLike[str] | str | None = None) -> tuple[int, list[dict]]:
    """加载投档线：返回 (最新年份, 该年该科目组全部行)。"""
    if not isinstance(subject_group, str) or not subject_group.strip():
        raise DataError("科目组必填")
    directory = _resolved_data_dir(province, root, province_dir)
    label = province or directory.name
    rows = _load_csv(directory, "tou_dang", label)
    return _latest(rows, subject_group.strip(), "tou_dang", label)


def load_yifenyiduan(province: str | None = None, subject_group: str | None = None,
                     root: os.PathLike[str] | str = DEFAULT_DATA_ROOT, *,
                     province_dir: os.PathLike[str] | str | None = None) -> tuple[int, list[dict]]:
    """加载一分一段：返回 (最新年份, 该年该科目组全部行)。"""
    if not isinstance(subject_group, str) or not subject_group.strip():
        raise DataError("科目组必填")
    directory = _resolved_data_dir(province, root, province_dir)
    label = province or directory.name
    rows = _load_csv(directory, "yifenyiduan", label)
    return _latest(rows, subject_group.strip(), "yifenyiduan", label)


def load_path_table(province: str | None, table: str,
                    root: os.PathLike[str] | str = DEFAULT_DATA_ROOT, *,
                    province_dir: os.PathLike[str] | str | None = None) -> list[dict]:
    """加载指定路径表（qiangji/zongping/gangao）的全部可用行。"""
    if table not in PATH_TABLES:
        raise DataError(f"未知路径表「{table}」，应为：{'、'.join(PATH_TABLES)}")
    directory = _resolved_data_dir(province, root, province_dir)
    return _load_csv(directory, table, province or directory.name)


def score_to_rank(province: str | None, subject_group: str, score: int,
                  root: os.PathLike[str] | str = DEFAULT_DATA_ROOT, *,
                  province_dir: os.PathLike[str] | str | None = None) -> dict:
    """分数→省排反查：
    精确命中取该分累计人数；分数在表中缺档时取相邻低分的累计；
    低于表中最低分 → 明确报错。"""
    year, rows = load_yifenyiduan(province, subject_group, root=root,
                                  province_dir=province_dir)
    by_score = {r["score"]: r["rank"] for r in rows}
    if score in by_score:
        return {"score": score, "rank": by_score[score], "year": year}
    lower = [s for s in by_score if s < score]
    if not lower:
        label = province if province is not None else (
            Path(province_dir).name if province_dir is not None else "该省"
        )
        raise DataError(f"分数 {score} 低于{label}{subject_group}组{year}年"
                        f"一分一段表最低分，无法反查省排名，请直接提供已验证省排名")
    nearest = max(lower)
    return {"score": score, "rank": by_score[nearest], "year": year}
