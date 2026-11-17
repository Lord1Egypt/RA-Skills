#!/usr/bin/env python3
"""管理家长沟通助手的本地 Markdown 档案。

本脚本只负责目录、索引、备份和文件写入等确定性操作。沟通策略、家长
心理判断以及回复生成必须由调用它的智能体完成，避免把模型判断偷偷写入
长期档案。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path


SCHEMA_VERSION = 1
SETTINGS_DIR_NAME = ".parent-communication-assistant"
SETTINGS_FILE_NAME = "settings.json"

TEACHER_PREFERENCE_INITIAL = """# 表达偏好

尚未初始化。请先由教师确认表达偏好，再写入本文件。
"""

CONFIRMED_SAMPLES_INITIAL = """# 已确认表达样本

尚无经教师确认的表达样本。
"""

STUDENT_INDEX_INITIAL = """# 学生索引

| 编号 | 姓名 | 年级 | 班级 | 目录 | 最近更新 |
|---|---|---|---|---|---|
"""

INDEX_HEADER = """# 学生索引

| 编号 | 姓名 | 年级 | 班级 | 目录 | 最近更新 |
|---|---|---|---|---|---|
"""

STUDENT_ID_RE = re.compile(r"^S\d{4}$")
VALID_GRADES = {"一年级", "二年级", "三年级", "四年级", "五年级", "六年级"}
FORBIDDEN_FIELD_CHARS = {"|", "/", "\\", "\n", "\r"}

CURRENT_PROFILE_HEADINGS = (
    "# 当前概况",
    "## 基本信息",
    "## 已确认的长期表现",
    "## 已采取的支持措施",
    "## 家长关注点与沟通偏好",
    "## 尚未解决的问题",
    "## 最近一次沟通结论",
    "## 信息更新时间",
)

COMMUNICATION_HEADINGS = (
    "# 沟通记录",
    "## 日期与渠道",
    "## 本次问题",
    "## 已确认事实",
    "## 家长核心关注",
    "## 教师实际回应",
    "## 达成共识",
    "## 待跟进事项",
    "## 是否更新长期概况",
)

TEACHER_PROFILE_HEADINGS = (
    "# 表达偏好",
    "## 常用称呼",
    "## 回复长度",
    "## 语气与直接程度",
    "## 语气词与表情",
    "## 开场与收尾",
    "## 避免表达",
)


class ArchiveError(RuntimeError):
    """表示可以直接向教师说明的档案操作错误。"""


@dataclass(frozen=True)
class StudentRecord:
    """学生索引中的一条不可变记录。"""

    student_id: str
    name: str
    grade: str
    class_name: str
    directory: str
    updated_at: str


def default_settings_path() -> Path:
    """返回只保存档案路径和结构版本的用户级设置文件位置。"""
    return Path.home() / SETTINGS_DIR_NAME / SETTINGS_FILE_NAME


def default_data_root() -> Path:
    """返回首次初始化时建议使用的本地档案目录。"""
    return Path.home() / "Documents" / "家长沟通档案"


def _replace_text_without_backup(path: Path, content: str) -> None:
    """在同目录写临时文件后原子替换，失败时保留旧设置。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=path.parent,
        ) as handle:
            handle.write(content)
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
    except Exception as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise ArchiveError(f"设置保存失败，旧设置已保留：{exc}") from exc


def save_settings(data_root: Path, settings_path: Path | None = None) -> Path:
    """保存档案根目录；设置文件不得包含学生或家长信息。"""
    resolved_root = data_root.expanduser().resolve()
    target = (settings_path or default_settings_path()).expanduser()
    payload = {
        "data_root": str(resolved_root),
        "schema_version": SCHEMA_VERSION,
    }
    _replace_text_without_backup(
        target,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )
    return target


def load_settings(settings_path: Path | None = None) -> dict[str, object]:
    """读取并验证设置；路径失效时不擅自新建另一套档案。"""
    target = (settings_path or default_settings_path()).expanduser()
    if not target.is_file():
        raise ArchiveError("尚未初始化档案目录，请先选择保存位置。")

    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ArchiveError(f"设置文件无法读取：{exc}") from exc

    if not isinstance(payload, dict):
        raise ArchiveError("设置文件顶层必须是 JSON 对象。")

    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ArchiveError("档案版本不兼容，请先完成数据迁移。")

    raw_root = payload.get("data_root")
    if not isinstance(raw_root, str) or not raw_root.strip():
        raise ArchiveError("设置文件缺少有效的档案目录。")
    data_root = Path(raw_root).expanduser()
    if not data_root.is_dir():
        raise ArchiveError("档案目录不存在，请重新选择保存位置。")

    return {
        "data_root": str(data_root.resolve()),
        "schema_version": SCHEMA_VERSION,
    }


def _required_archive_files(data_root: Path) -> tuple[Path, Path, Path]:
    """集中定义首版档案必须存在的三个入口文件。"""
    return (
        data_root / "教师档案" / "表达偏好.md",
        data_root / "教师档案" / "已确认表达样本.md",
        data_root / "学生档案" / "学生索引.md",
    )


def _has_complete_initial_structure(data_root: Path) -> bool:
    """只检查初始化结构是否完整；深层索引一致性由后续校验负责。"""
    return all(path.is_file() for path in _required_archive_files(data_root))


def initialize_archive(
    data_root: Path,
    settings_path: Path | None = None,
) -> dict[str, object]:
    """初始化空档案，或安全连接一套已经存在的完整档案。"""
    resolved_root = data_root.expanduser().resolve()
    skill_root = Path(__file__).resolve().parents[1]
    if resolved_root == skill_root or skill_root in resolved_root.parents:
        raise ArchiveError("真实档案不得保存在 Skill 安装目录内。")

    if resolved_root.exists() and not resolved_root.is_dir():
        raise ArchiveError("所选档案位置不是目录。")

    if resolved_root.is_dir() and any(resolved_root.iterdir()):
        if not _has_complete_initial_structure(resolved_root):
            raise ArchiveError(
                "所选目录不是有效的家长沟通档案，请选择空目录或已有完整档案。"
            )
        save_settings(resolved_root, settings_path)
        return {
            "data_root": str(resolved_root),
            "schema_version": SCHEMA_VERSION,
        }

    # 所有初始文件先在同一父目录的暂存目录中写完；只有全部成功后才一次性
    # 把完整目录切换到正式位置，避免中途失败留下无法再次初始化的半成品。
    resolved_root.parent.mkdir(parents=True, exist_ok=True)
    target_existed_as_empty = resolved_root.is_dir()
    staging_root = Path(
        tempfile.mkdtemp(prefix=f".{resolved_root.name}-初始化-", dir=resolved_root.parent)
    )
    moved_to_target = False
    try:
        initial_documents = (
            (_required_archive_files(staging_root)[0], TEACHER_PREFERENCE_INITIAL),
            (_required_archive_files(staging_root)[1], CONFIRMED_SAMPLES_INITIAL),
            (_required_archive_files(staging_root)[2], STUDENT_INDEX_INITIAL),
        )
        for path, content in initial_documents:
            atomic_write_text(path, content, staging_root, backup=False)

        if target_existed_as_empty:
            resolved_root.rmdir()
        os.replace(staging_root, resolved_root)
        moved_to_target = True
        save_settings(resolved_root, settings_path)
    except Exception as exc:
        # 只清理本次创建的暂存或正式目录；目标原先若是空目录，则恢复为空目录。
        if moved_to_target and resolved_root.exists():
            shutil.rmtree(resolved_root)
        elif staging_root.exists():
            shutil.rmtree(staging_root)
        if target_existed_as_empty and not resolved_root.exists():
            resolved_root.mkdir(parents=True)
        if isinstance(exc, ArchiveError):
            raise
        raise ArchiveError(f"档案初始化失败，未保留半成品：{exc}") from exc
    return {
        "data_root": str(resolved_root),
        "schema_version": SCHEMA_VERSION,
    }


def atomic_write_text(
    path: Path,
    content: str,
    data_root: Path,
    backup: bool = True,
) -> Path | None:
    """安全写入档案文件，并在覆盖前创建保持相对路径的可恢复备份。"""
    resolved_root = data_root.expanduser().resolve()
    resolved_target = path.expanduser().resolve()
    try:
        relative_target = resolved_target.relative_to(resolved_root)
    except ValueError as exc:
        raise ArchiveError("拒绝写入档案根目录之外的文件。") from exc

    resolved_target.parent.mkdir(parents=True, exist_ok=True)
    if resolved_target.is_file():
        try:
            if resolved_target.read_text(encoding="utf-8") == content:
                return None
        except OSError as exc:
            raise ArchiveError(f"原文件无法读取：{exc}") from exc

    backup_path: Path | None = None
    if backup and resolved_target.is_file():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S%f")
        backup_path = resolved_root / ".backups" / stamp / relative_target
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(resolved_target, backup_path)
        except OSError as exc:
            raise ArchiveError(f"备份失败，未修改原文件：{exc}") from exc

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=resolved_target.parent,
        ) as handle:
            handle.write(content)
            temp_path = Path(handle.name)
        os.replace(temp_path, resolved_target)
    except Exception as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise ArchiveError(f"写入失败，原文件已保留：{exc}") from exc

    return backup_path


def _index_path(data_root: Path) -> Path:
    """返回学生索引的固定位置。"""
    return data_root.expanduser().resolve() / "学生档案" / "学生索引.md"


def _validate_plain_field(value: str, field_name: str) -> str:
    """校验会进入 Markdown 表格或目录名的短文本，防止结构和路径注入。"""
    normalized = value.strip()
    if not normalized:
        raise ArchiveError(f"{field_name}不能为空。")
    if any(char in normalized for char in FORBIDDEN_FIELD_CHARS):
        raise ArchiveError(f"{field_name}包含非法字符。")
    return normalized


def _validate_student_record(record: StudentRecord) -> None:
    """校验一条索引记录的格式，不检查目录是否真的存在。"""
    if not STUDENT_ID_RE.fullmatch(record.student_id):
        raise ArchiveError(f"学生编号格式错误：{record.student_id}")
    _validate_plain_field(record.name, "学生姓名")
    if record.grade not in VALID_GRADES:
        raise ArchiveError(f"年级不在小学一至六年级范围内：{record.grade}")
    _validate_plain_field(record.class_name, "班级")
    _validate_plain_field(record.directory, "学生目录")
    try:
        date.fromisoformat(record.updated_at)
    except ValueError as exc:
        raise ArchiveError(f"索引日期格式错误：{record.updated_at}") from exc


def load_index(data_root: Path) -> list[StudentRecord]:
    """读取固定六列表格；任何格式异常都阻止后续写入。"""
    path = _index_path(data_root)
    if not path.is_file():
        raise ArchiveError("学生索引不存在，请先初始化或修复档案。")

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ArchiveError(f"学生索引无法读取：{exc}") from exc

    expected_prefix = INDEX_HEADER.rstrip("\n").splitlines()
    if lines[: len(expected_prefix)] != expected_prefix:
        raise ArchiveError("学生索引表头或分隔行已损坏。")

    records: list[StudentRecord] = []
    seen_ids: set[str] = set()
    seen_directories: set[str] = set()
    for line_number, raw_line in enumerate(
        lines[len(expected_prefix) :], start=len(expected_prefix) + 1
    ):
        line = raw_line.strip()
        if not line:
            continue
        if not line.startswith("|") or not line.endswith("|"):
            raise ArchiveError(f"学生索引第 {line_number} 行必须是六列表格行。")
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 6:
            raise ArchiveError(f"学生索引第 {line_number} 行不是固定六列。")
        record = StudentRecord(*cells)
        _validate_student_record(record)
        if record.student_id in seen_ids:
            raise ArchiveError(f"学生索引存在重复编号：{record.student_id}")
        if record.directory in seen_directories:
            raise ArchiveError(f"学生索引存在重复目录：{record.directory}")
        seen_ids.add(record.student_id)
        seen_directories.add(record.directory)
        records.append(record)
    return records


def _render_index(records: list[StudentRecord]) -> str:
    """按学生编号稳定排序，生成唯一格式的可读 Markdown 索引。"""
    rows = [INDEX_HEADER.rstrip("\n")]
    for record in sorted(records, key=lambda item: item.student_id):
        rows.append(
            "| {student_id} | {name} | {grade} | {class_name} | {directory} | "
            "{updated_at} |".format(**record.__dict__)
        )
    return "\n".join(rows) + "\n"


def _find_by_id(records: list[StudentRecord], student_id: str) -> StudentRecord:
    """按稳定编号查找学生，找不到时给出可理解的错误。"""
    for record in records:
        if record.student_id == student_id:
            return record
    raise ArchiveError(f"未找到学生编号：{student_id}")


def find_students(
    data_root: Path,
    name: str,
    grade: str | None = None,
    class_name: str | None = None,
) -> list[StudentRecord]:
    """精确匹配学生；返回全部候选，不替教师猜测同名身份。"""
    normalized_name = name.strip()
    normalized_grade = grade.strip() if grade is not None else None
    normalized_class = class_name.strip() if class_name is not None else None
    return [
        record
        for record in load_index(data_root)
        if record.name == normalized_name
        and (normalized_grade is None or record.grade == normalized_grade)
        and (normalized_class is None or record.class_name == normalized_class)
    ]


def _next_student_id(records: list[StudentRecord]) -> str:
    """从现有最大编号递增生成新编号；支持流程不提供删除或复用编号。"""
    highest = max((int(item.student_id[1:]) for item in records), default=0)
    next_number = highest + 1
    if next_number > 9999:
        raise ArchiveError("学生编号已经达到 S9999，无法继续自动编号。")
    return f"S{next_number:04d}"


def _current_profile_template(record: StudentRecord) -> str:
    """创建仅含已知基本信息的概况，不补造任何学生或家长特征。"""
    return f"""# 当前概况

## 基本信息

- 学生编号：{record.student_id}
- 姓名：{record.name}
- 年级：{record.grade}
- 班级：{record.class_name}

## 已确认的长期表现

- 暂无长期结论。

## 已采取的支持措施

- 暂无已确认措施。

## 家长关注点与沟通偏好

- 暂无已确认偏好。

## 尚未解决的问题

- 暂无。

## 最近一次沟通结论

- 暂无。

## 信息更新时间

- {record.updated_at}
"""


def create_student(
    data_root: Path,
    name: str,
    grade: str,
    class_name: str,
    confirmed: bool,
) -> StudentRecord:
    """在教师确认后创建学生目录，并以一次事务更新可读索引。"""
    if not confirmed:
        raise ArchiveError("创建学生档案前必须获得教师确认。")
    normalized_name = _validate_plain_field(name, "学生姓名")
    normalized_grade = grade.strip()
    if normalized_grade not in VALID_GRADES:
        raise ArchiveError("年级必须是一年级至六年级。")
    normalized_class = _validate_plain_field(class_name, "班级")

    resolved_root = data_root.expanduser().resolve()
    records = load_index(resolved_root)
    student_id = _next_student_id(records)
    base_directory = f"{normalized_name}-{normalized_grade}{normalized_class}"
    directory = base_directory
    student_root = resolved_root / "学生档案" / directory
    if student_root.exists():
        directory = f"{base_directory}-{student_id}"
        student_root = resolved_root / "学生档案" / directory
    if student_root.exists():
        raise ArchiveError(f"学生目录已经存在：{directory}")

    today = date.today().isoformat()
    record = StudentRecord(
        student_id,
        normalized_name,
        normalized_grade,
        normalized_class,
        directory,
        today,
    )
    _validate_student_record(record)

    try:
        (student_root / "沟通记录").mkdir(parents=True)
        atomic_write_text(
            student_root / "当前概况.md",
            _current_profile_template(record),
            resolved_root,
            backup=False,
        )
        atomic_write_text(
            _index_path(resolved_root),
            _render_index([*records, record]),
            resolved_root,
        )
    except Exception:
        # 只回滚本次新建且此前不存在的精确目录，绝不删除其他档案。
        if student_root.exists():
            shutil.rmtree(student_root)
        raise
    return record


def _teacher_profile_initialized(data_root: Path) -> bool:
    """判断表达偏好是否已由教师确认写入。

    初始模板中包含“尚未初始化”标记，只有该标记被真实内容替换后才算完成初始化。
    """
    profile_path = data_root / "教师档案" / "表达偏好.md"
    try:
        content = profile_path.read_text(encoding="utf-8")
    except OSError:
        return False
    return "尚未初始化" not in content


def validate_archive(data_root: Path) -> dict[str, object]:
    """只读校验索引和学生目录一致性，返回适合展示的错误清单。

    额外返回 teacher_profile_initialized 字段，供 Skill 判断初始化门禁是否完成：
    档案结构合法但表达偏好未初始化时，valid 仍为 True，由调用方决定是否放行。
    """
    resolved_root = data_root.expanduser().resolve()
    errors: list[str] = []
    try:
        records = load_index(resolved_root)
    except (ArchiveError, OSError) as exc:
        return {
            "valid": False,
            "errors": [str(exc)],
            "student_count": 0,
            "teacher_profile_initialized": False,
        }

    for record in records:
        student_root = resolved_root / "学生档案" / record.directory
        if not student_root.is_dir():
            errors.append(f"索引中的学生目录不存在：{record.directory}")
            continue
        if not (student_root / "当前概况.md").is_file():
            errors.append(f"学生概况不存在：{record.directory}/当前概况.md")
        if not (student_root / "沟通记录").is_dir():
            errors.append(f"沟通记录目录不存在：{record.directory}/沟通记录")

    students_root = resolved_root / "学生档案"
    indexed_directories = {record.directory for record in records}
    if students_root.is_dir():
        for child in sorted(students_root.iterdir(), key=lambda item: item.name):
            if child.is_dir() and child.name not in indexed_directories:
                errors.append(f"未被索引引用的学生目录：{child.name}")

    return {
        "valid": not errors,
        "errors": errors,
        "student_count": len(records),
        "teacher_profile_initialized": _teacher_profile_initialized(resolved_root),
    }


def _replace_profile_field(content: str, label: str, value: str) -> str:
    """只替换固定基本信息行；缺失字段说明档案结构已损坏。"""
    pattern = re.compile(rf"^- {re.escape(label)}：.*$", re.MULTILINE)
    updated, count = pattern.subn(f"- {label}：{value}", content, count=1)
    if count != 1:
        raise ArchiveError(f"当前概况缺少固定字段：{label}")
    return updated


def _replace_section_first_bullet(content: str, heading: str, value: str) -> str:
    """替换固定章节的首条项目，避免用全局字符串替换误伤其他日期。"""
    pattern = re.compile(rf"({re.escape(heading)}\n\n)- [^\n]*")
    updated, count = pattern.subn(rf"\1- {value}", content, count=1)
    if count != 1:
        raise ArchiveError(f"当前概况缺少固定章节：{heading}")
    return updated


def promote_student(
    data_root: Path,
    student_id: str,
    grade: str,
    class_name: str,
    confirmed: bool,
) -> StudentRecord:
    """在确认后更新年级班级，并在任一步失败时恢复旧目录和索引。"""
    if not confirmed:
        raise ArchiveError("更新年级班级前必须获得教师确认。")
    normalized_grade = grade.strip()
    if normalized_grade not in VALID_GRADES:
        raise ArchiveError("年级必须是一年级至六年级。")
    normalized_class = _validate_plain_field(class_name, "班级")

    resolved_root = data_root.expanduser().resolve()
    records = load_index(resolved_root)
    current = _find_by_id(records, student_id)
    old_root = resolved_root / "学生档案" / current.directory
    if not old_root.is_dir():
        raise ArchiveError(f"学生目录不存在：{current.directory}")

    base_directory = f"{current.name}-{normalized_grade}{normalized_class}"
    new_directory = base_directory
    new_root = resolved_root / "学生档案" / new_directory
    if new_root.exists() and new_root != old_root:
        new_directory = f"{base_directory}-{current.student_id}"
        new_root = resolved_root / "学生档案" / new_directory
    if new_root.exists() and new_root != old_root:
        raise ArchiveError(f"目标学生目录已经存在：{new_directory}")

    updated = StudentRecord(
        current.student_id,
        current.name,
        normalized_grade,
        normalized_class,
        new_directory,
        date.today().isoformat(),
    )
    old_index_text = _index_path(resolved_root).read_text(encoding="utf-8")
    old_profile_path = old_root / "当前概况.md"
    old_profile_text = old_profile_path.read_text(encoding="utf-8")
    new_profile_text = _replace_profile_field(old_profile_text, "年级", normalized_grade)
    new_profile_text = _replace_profile_field(new_profile_text, "班级", normalized_class)
    new_profile_text = _replace_section_first_bullet(
        new_profile_text, "## 信息更新时间", updated.updated_at
    )
    updated_records = [updated if item.student_id == student_id else item for item in records]

    renamed = False
    profile_backup: Path | None = None
    try:
        if new_root != old_root:
            old_root.rename(new_root)
            renamed = True
        profile_backup = atomic_write_text(
            new_root / "当前概况.md", new_profile_text, resolved_root
        )
        atomic_write_text(
            _index_path(resolved_root), _render_index(updated_records), resolved_root
        )
    except Exception as original_exc:
        # 目录映射决定索引能否找到学生，因此先恢复目录；后续每一项补偿独立
        # 尝试，任何一项失败都不能阻断其余回滚动作。
        rollback_errors: list[str] = []
        if renamed and new_root.exists() and not old_root.exists():
            try:
                new_root.rename(old_root)
            except OSError as exc:
                rollback_errors.append(f"目录恢复失败：{exc}")

        restored_root = old_root if old_root.exists() else new_root
        restore_targets = (
            (restored_root / "当前概况.md", old_profile_text, "概况"),
            (_index_path(resolved_root), old_index_text, "索引"),
        )
        for target, old_text, label in restore_targets:
            try:
                if target.is_file() and target.read_text(encoding="utf-8") == old_text:
                    continue
                # 概况已经成功替换、随后索引失败时，优先从写入前生成的备份
                # 直接复制恢复；这样即使原子替换持续故障，也能回到旧内容。
                if label == "概况" and profile_backup and profile_backup.is_file():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(profile_backup, target)
                else:
                    _replace_text_without_backup(target, old_text)
            except (ArchiveError, OSError, UnicodeError) as exc:
                rollback_errors.append(f"{label}恢复失败：{exc}")

        if rollback_errors:
            raise ArchiveError(
                f"升年级失败：{original_exc}；回滚异常：{'；'.join(rollback_errors)}"
            ) from original_exc
        raise
    return updated


def _require_confirmation(confirmed: bool, action: str) -> None:
    """集中执行长期写入确认门，防止某个入口遗漏保护。"""
    if not confirmed:
        raise ArchiveError(f"{action}前必须获得教师确认。")


def _require_headings(content: str, headings: tuple[str, ...], document: str) -> None:
    """校验结构化 Markdown 的必填章节，避免写入无法继续维护的文件。"""
    missing = [heading for heading in headings if heading not in content]
    if missing:
        raise ArchiveError(f"{document}缺少必填章节：{'、'.join(missing)}")


def write_teacher_profile(
    data_root: Path,
    content: str,
    confirmed: bool,
) -> Path:
    """在教师确认后写入精简表达偏好。"""
    _require_confirmation(confirmed, "写入教师表达偏好")
    _require_headings(content, TEACHER_PROFILE_HEADINGS, "教师表达偏好")
    resolved_root = data_root.expanduser().resolve()
    target = resolved_root / "教师档案" / "表达偏好.md"
    atomic_write_text(target, content, resolved_root)
    return target


def write_confirmed_samples(
    data_root: Path,
    content: str,
    confirmed: bool,
) -> Path:
    """写入少量已确认样本；超过十条时要求调用方先筛选代表样本。"""
    _require_confirmation(confirmed, "写入教师表达样本")
    if "# 已确认表达样本" not in content:
        raise ArchiveError("教师表达样本缺少标题：# 已确认表达样本")
    sample_count = len(re.findall(r"^## 样本(?:\s|$)", content, flags=re.MULTILINE))
    if sample_count > 10:
        raise ArchiveError("已确认表达样本最多保留 10 条，请先筛选代表样本。")
    resolved_root = data_root.expanduser().resolve()
    target = resolved_root / "教师档案" / "已确认表达样本.md"
    atomic_write_text(target, content, resolved_root)
    return target


def write_current_profile(
    data_root: Path,
    student_id: str,
    content: str,
    confirmed: bool,
) -> Path:
    """在确认后覆盖当前概况，并核对内容确实属于选中的学生。"""
    _require_confirmation(confirmed, "写入学生当前概况")
    _require_headings(content, CURRENT_PROFILE_HEADINGS, "学生当前概况")
    resolved_root = data_root.expanduser().resolve()
    record = _find_by_id(load_index(resolved_root), student_id)
    expected_lines = (
        f"- 学生编号：{record.student_id}",
        f"- 姓名：{record.name}",
        f"- 年级：{record.grade}",
        f"- 班级：{record.class_name}",
    )
    if any(line not in content for line in expected_lines):
        raise ArchiveError("当前概况中的基本信息与索引不一致，已拒绝写入。")
    today = date.today().isoformat()
    normalized_content = _replace_section_first_bullet(
        content, "## 信息更新时间", today
    )
    updated_record = StudentRecord(
        record.student_id,
        record.name,
        record.grade,
        record.class_name,
        record.directory,
        today,
    )
    records = load_index(resolved_root)
    updated_records = [
        updated_record if item.student_id == student_id else item for item in records
    ]
    target = resolved_root / "学生档案" / record.directory / "当前概况.md"
    old_profile = target.read_text(encoding="utf-8")
    profile_backup: Path | None = None
    try:
        profile_backup = atomic_write_text(target, normalized_content, resolved_root)
        atomic_write_text(
            _index_path(resolved_root), _render_index(updated_records), resolved_root
        )
    except Exception as original_exc:
        if target.is_file() and target.read_text(encoding="utf-8") != old_profile:
            try:
                if profile_backup and profile_backup.is_file():
                    shutil.copy2(profile_backup, target)
                else:
                    _replace_text_without_backup(target, old_profile)
            except (ArchiveError, OSError) as rollback_exc:
                raise ArchiveError(
                    f"概况写入失败：{original_exc}；旧概况恢复失败：{rollback_exc}"
                ) from original_exc
        raise
    return target


def _sanitize_topic(topic: str) -> str:
    """将沟通主题转换成安全、仍可读的文件名片段。"""
    normalized = topic.strip()
    normalized = re.sub(r'[<>:"/\\|?*]+', "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("- .")
    if not normalized:
        raise ArchiveError("沟通主题无法生成有效文件名。")
    return normalized


def save_communication(
    data_root: Path,
    student_id: str,
    communication_date: str,
    channel: str,
    topic: str,
    content: str,
    confirmed: bool,
) -> Path:
    """保存经确认的沟通摘要；不保存截图或完整原始聊天。"""
    _require_confirmation(confirmed, "保存沟通记录")
    _require_headings(content, COMMUNICATION_HEADINGS, "沟通记录")
    try:
        parsed_date = date.fromisoformat(communication_date)
    except ValueError as exc:
        raise ArchiveError("沟通日期必须使用 YYYY-MM-DD 格式。") from exc
    if parsed_date.isoformat() != communication_date:
        raise ArchiveError("沟通日期必须使用 YYYY-MM-DD 格式。")

    normalized_channel = _validate_plain_field(channel, "沟通渠道")
    safe_topic = _sanitize_topic(topic)
    if f"- 日期：{communication_date}" not in content:
        raise ArchiveError("沟通记录中的日期与命令参数不一致。")
    if f"- 渠道：{normalized_channel}" not in content:
        raise ArchiveError("沟通记录中的渠道与命令参数不一致。")
    if f"- 主题：{safe_topic}" not in content:
        raise ArchiveError("沟通记录中的主题与命令参数不一致。")
    update_flags = re.findall(r"^- 是否更新：(是|否)\s*$", content, re.MULTILINE)
    if len(update_flags) != 1:
        raise ArchiveError("是否更新长期概况只能填写“是”或“否”，且只能填写一次。")

    resolved_root = data_root.expanduser().resolve()
    records = load_index(resolved_root)
    record = _find_by_id(records, student_id)
    records_root = resolved_root / "学生档案" / record.directory / "沟通记录"
    candidate = records_root / f"{communication_date}-{safe_topic}.md"
    sequence = 2
    while candidate.exists():
        candidate = records_root / f"{communication_date}-{safe_topic}-{sequence:02d}.md"
        sequence += 1

    atomic_write_text(candidate, content, resolved_root, backup=False)
    updated_record = StudentRecord(
        record.student_id,
        record.name,
        record.grade,
        record.class_name,
        record.directory,
        max(record.updated_at, communication_date),
    )
    updated_records = [
        updated_record if item.student_id == student_id else item for item in records
    ]
    try:
        atomic_write_text(
            _index_path(resolved_root), _render_index(updated_records), resolved_root
        )
    except Exception:
        # 新记录尚未对外可见时，只删除本次精确创建的文件以保持索引一致。
        candidate.unlink(missing_ok=True)
        raise
    return candidate


def _read_utf8_input(path: Path) -> str:
    """读取调用方准备的待确认 Markdown，不删除或改写输入文件。"""
    try:
        return path.expanduser().read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ArchiveError(f"输入文件无法按 UTF-8 读取：{exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    """构建稳定的 JSON 命令行接口，供 Skill 直接执行。"""
    parser = argparse.ArgumentParser(description="管理家长沟通助手的本地档案")
    parser.add_argument("--settings", type=Path, default=default_settings_path())
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="初始化或连接档案目录")
    init_parser.add_argument("--data-root", type=Path, default=default_data_root())

    subparsers.add_parser("validate", help="只读校验档案一致性")

    find_parser = subparsers.add_parser("find", help="精确查找学生")
    find_parser.add_argument("--name", required=True)
    find_parser.add_argument("--grade")
    find_parser.add_argument("--class-name")

    create_parser = subparsers.add_parser("create", help="创建学生档案")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--grade", required=True)
    create_parser.add_argument("--class-name", required=True)
    create_parser.add_argument("--confirmed", action="store_true")

    teacher_parser = subparsers.add_parser(
        "write-teacher-profile", help="写入教师表达偏好"
    )
    teacher_parser.add_argument("--input-file", type=Path, required=True)
    teacher_parser.add_argument("--confirmed", action="store_true")

    samples_parser = subparsers.add_parser(
        "write-confirmed-samples", help="写入已确认表达样本"
    )
    samples_parser.add_argument("--input-file", type=Path, required=True)
    samples_parser.add_argument("--confirmed", action="store_true")

    profile_parser = subparsers.add_parser(
        "write-current-profile", help="写入学生当前概况"
    )
    profile_parser.add_argument("--student-id", required=True)
    profile_parser.add_argument("--input-file", type=Path, required=True)
    profile_parser.add_argument("--confirmed", action="store_true")

    communication_parser = subparsers.add_parser(
        "save-communication", help="保存一次沟通摘要"
    )
    communication_parser.add_argument("--student-id", required=True)
    communication_parser.add_argument("--date", required=True)
    communication_parser.add_argument("--channel", required=True)
    communication_parser.add_argument("--topic", required=True)
    communication_parser.add_argument("--input-file", type=Path, required=True)
    communication_parser.add_argument("--confirmed", action="store_true")

    promote_parser = subparsers.add_parser("promote", help="更新学生年级和班级")
    promote_parser.add_argument("--student-id", required=True)
    promote_parser.add_argument("--grade", required=True)
    promote_parser.add_argument("--class-name", required=True)
    promote_parser.add_argument("--confirmed", action="store_true")
    return parser


def _validated_data_root(settings_path: Path) -> Path:
    """读取设置并阻止在索引不一致时执行任何修改命令。"""
    settings = load_settings(settings_path)
    data_root = Path(str(settings["data_root"]))
    result = validate_archive(data_root)
    if not result["valid"]:
        raise ArchiveError("档案校验失败，已停止写入：" + "；".join(result["errors"]))
    return data_root


def main(argv: list[str] | None = None) -> int:
    """执行命令并输出单个 JSON 对象，避免调用方解析自然语言日志。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "init":
            result = initialize_archive(args.data_root, args.settings)
            payload = {"ok": True, **result}
        elif args.command == "validate":
            settings = load_settings(args.settings)
            result = validate_archive(Path(str(settings["data_root"])))
            payload = {"ok": True, **result}
        else:
            data_root = _validated_data_root(args.settings)
            if args.command == "find":
                students = find_students(
                    data_root, args.name, args.grade, args.class_name
                )
                payload = {"ok": True, "students": [asdict(item) for item in students]}
            elif args.command == "create":
                student = create_student(
                    data_root,
                    args.name,
                    args.grade,
                    args.class_name,
                    args.confirmed,
                )
                payload = {"ok": True, "student": asdict(student)}
            elif args.command == "write-teacher-profile":
                path = write_teacher_profile(
                    data_root, _read_utf8_input(args.input_file), args.confirmed
                )
                payload = {"ok": True, "path": str(path)}
            elif args.command == "write-confirmed-samples":
                path = write_confirmed_samples(
                    data_root, _read_utf8_input(args.input_file), args.confirmed
                )
                payload = {"ok": True, "path": str(path)}
            elif args.command == "write-current-profile":
                path = write_current_profile(
                    data_root,
                    args.student_id,
                    _read_utf8_input(args.input_file),
                    args.confirmed,
                )
                payload = {"ok": True, "path": str(path)}
            elif args.command == "save-communication":
                path = save_communication(
                    data_root,
                    args.student_id,
                    args.date,
                    args.channel,
                    args.topic,
                    _read_utf8_input(args.input_file),
                    args.confirmed,
                )
                payload = {"ok": True, "path": str(path)}
            elif args.command == "promote":
                student = promote_student(
                    data_root,
                    args.student_id,
                    args.grade,
                    args.class_name,
                    args.confirmed,
                )
                payload = {"ok": True, "student": asdict(student)}
            else:
                raise ArchiveError(f"未知命令：{args.command}")
    except (ArchiveError, OSError, UnicodeError) as exc:
        print(
            json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return 2

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
