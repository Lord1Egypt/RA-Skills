#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "2026-04-v1"


def select_option(name: str, hue: str = "Blue", lightness: str = "Light") -> Dict[str, str]:
    return {"name": name, "hue": hue, "lightness": lightness}


@dataclass
class FieldSpec:
    name: str
    field_type: str
    description: str = ""
    multiple: Optional[bool] = None
    options: List[Dict[str, str]] = field(default_factory=list)
    precision: Optional[int] = None
    link_table: Optional[str] = None
    bidirectional: bool = False

    def public_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "name": self.name,
            "type": self.field_type,
            "description": self.description,
        }
        if self.multiple is not None:
            data["multiple"] = self.multiple
        if self.options:
            data["options"] = self.options
        if self.precision is not None:
            data["precision"] = self.precision
        if self.link_table:
            data["link_table"] = self.link_table
            data["bidirectional"] = self.bidirectional
        return data

    def to_feishu_json(self, table_lookup: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        data: Dict[str, Any] = {"name": self.name, "type": self.field_type}
        if self.description:
            data["description"] = self.description
        if self.field_type == "number" and self.precision is not None:
            data["precision"] = self.precision
        if self.field_type == "select":
            data["multiple"] = bool(self.multiple)
            data["options"] = self.options
        if self.field_type == "link":
            if not self.link_table:
                raise ValueError(f"Field {self.name} is missing link_table")
            target = self.link_table
            if table_lookup:
                target = table_lookup.get(self.link_table, self.link_table)
            data["link_table"] = target
            data["bidirectional"] = self.bidirectional
        return data


@dataclass
class ViewSpec:
    name: str
    view_type: str = "grid"

    def public_dict(self) -> Dict[str, str]:
        return {"name": self.name, "type": self.view_type}


@dataclass
class TableSpec:
    name: str
    description: str
    primary_field: FieldSpec
    fields: List[FieldSpec]
    views: List[ViewSpec]

    def public_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "primary_field": self.primary_field.public_dict(),
            "fields": [field.public_dict() for field in self.fields],
            "views": [view.public_dict() for view in self.views],
        }

    def feishu_table_create_fields(self) -> List[Dict[str, Any]]:
        fields = [self.primary_field.to_feishu_json()]
        for field_spec in self.fields:
            if field_spec.field_type == "link":
                continue
            fields.append(field_spec.to_feishu_json())
        return fields

    def feishu_link_fields(self, table_lookup: Dict[str, str]) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for field_spec in self.fields:
            if field_spec.field_type == "link":
                items.append(field_spec.to_feishu_json(table_lookup))
        return items


def build_table_specs() -> List[TableSpec]:
    yes_no_options = [
        select_option("是", "Green", "Light"),
        select_option("否", "Red", "Light"),
    ]
    sync_status_options = [
        select_option("仅本地", "Grey", "Light"),
        select_option("待同步", "Orange", "Light"),
        select_option("已同步", "Green", "Light"),
        select_option("同步失败", "Red", "Light"),
    ]
    term_options = [
        select_option("上学期", "Blue", "Light"),
        select_option("下学期", "Purple", "Light"),
        select_option("暑期", "Orange", "Light"),
    ]

    return [
        TableSpec(
            name="班级配置",
            description="单班级的工作台配置与运行状态。",
            primary_field=FieldSpec("班级名称", "text", "班级工作台的显示名称。"),
            fields=[
                FieldSpec("学年", "text", "如 2025-2026。"),
                FieldSpec("当前学期", "select", "当前使用学期。", multiple=False, options=term_options),
                FieldSpec("班主任", "text", "班主任姓名或代号。"),
                FieldSpec(
                    "默认后端",
                    "select",
                    "工作台默认后端。",
                    multiple=False,
                    options=[
                        select_option("feishu_base", "Blue", "Light"),
                        select_option("notion", "Purple", "Light"),
                        select_option("obsidian", "Green", "Light"),
                        select_option("local_only", "Grey", "Light"),
                    ],
                ),
                FieldSpec(
                    "工作台状态",
                    "select",
                    "初始化与可用性状态。",
                    multiple=False,
                    options=[
                        select_option("draft", "Grey", "Light"),
                        select_option("ready", "Green", "Light"),
                        select_option("needs_attention", "Orange", "Light"),
                    ],
                ),
                FieldSpec("备注", "text", "工作台初始化说明或例外。"),
            ],
            views=[ViewSpec("配置总览")],
        ),
        TableSpec(
            name="学生主档",
            description="学生主数据与联系方式。",
            primary_field=FieldSpec("姓名", "text", "学生姓名。"),
            fields=[
                FieldSpec("student_id", "text", "工作台内部稳定 ID。"),
                FieldSpec("学号", "text", "学校或班级学号。"),
                FieldSpec(
                    "性别",
                    "select",
                    "学生性别。",
                    multiple=False,
                    options=[
                        select_option("男", "Blue", "Light"),
                        select_option("女", "Pink", "Light"),
                        select_option("其他", "Grey", "Light"),
                    ],
                ),
                FieldSpec("班级", "text", "班级名。"),
                FieldSpec("学期", "select", "当前学期。", multiple=False, options=term_options),
                FieldSpec(
                    "选科",
                    "select",
                    "学生选科。",
                    multiple=True,
                    options=[
                        select_option("语文"),
                        select_option("数学"),
                        select_option("英语"),
                        select_option("物理"),
                        select_option("化学"),
                        select_option("生物"),
                        select_option("历史"),
                        select_option("地理"),
                        select_option("政治"),
                    ],
                ),
                FieldSpec("毕业学校", "text", "升学前学校。"),
                FieldSpec("宿舍楼", "text", "宿舍楼栋。"),
                FieldSpec("宿舍房间", "text", "宿舍房间号。"),
                FieldSpec("宿舍床位", "text", "宿舍床位号。"),
                FieldSpec("家长1姓名", "text", "主要家长联系人。"),
                FieldSpec(
                    "家长1关系",
                    "select",
                    "与学生关系。",
                    multiple=False,
                    options=[
                        select_option("父亲"),
                        select_option("母亲"),
                        select_option("监护人"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec("家长1电话", "text", "主要联系电话。"),
                FieldSpec("家长2姓名", "text", "备用家长联系人。"),
                FieldSpec(
                    "家长2关系",
                    "select",
                    "与学生关系。",
                    multiple=False,
                    options=[
                        select_option("父亲"),
                        select_option("母亲"),
                        select_option("监护人"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec("家长2电话", "text", "备用联系电话。"),
                FieldSpec("身份证号", "text", "敏感字段，只面向班主任。"),
                FieldSpec("住址", "text", "家庭住址。"),
                FieldSpec(
                    "重点关注标签",
                    "select",
                    "班主任关注标签。",
                    multiple=True,
                    options=[
                        select_option("学业"),
                        select_option("纪律"),
                        select_option("宿舍"),
                        select_option("家校沟通"),
                        select_option("心理支持"),
                    ],
                ),
                FieldSpec("备注", "text", "补充说明。"),
            ],
            views=[ViewSpec("学生总览"), ViewSpec("重点关注")],
        ),
        TableSpec(
            name="考试批次",
            description="考试或阶段测评的元信息。",
            primary_field=FieldSpec("考试名称", "text", "例如 2025 秋期末。"),
            fields=[
                FieldSpec("exam_id", "text", "考试批次稳定 ID。"),
                FieldSpec("考试日期", "datetime", "考试日期。"),
                FieldSpec("学期", "select", "所属学期。", multiple=False, options=term_options),
                FieldSpec(
                    "考试类型",
                    "select",
                    "考试批次类型。",
                    multiple=False,
                    options=[
                        select_option("小测"),
                        select_option("阶段考"),
                        select_option("期中"),
                        select_option("期末"),
                        select_option("模拟考"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec("学科范围", "text", "全科或单科描述。"),
                FieldSpec(
                    "来源",
                    "select",
                    "数据来源。",
                    multiple=False,
                    options=[
                        select_option("班主任录入"),
                        select_option("科任老师导入"),
                        select_option("系统导入"),
                    ],
                ),
                FieldSpec("备注", "text", "补充说明。"),
            ],
            views=[ViewSpec("考试批次")],
        ),
        TableSpec(
            name="成绩明细",
            description="长表成绩记录，一行表示一次考试中的单个学科成绩。",
            primary_field=FieldSpec("记录标题", "text", "建议由脚本生成：学生-考试-学科。"),
            fields=[
                FieldSpec("student_ref", "link", "关联学生主档。", link_table="学生主档"),
                FieldSpec("exam_ref", "link", "关联考试批次。", link_table="考试批次"),
                FieldSpec(
                    "学科",
                    "select",
                    "单科成绩学科。",
                    multiple=False,
                    options=[
                        select_option("语文"),
                        select_option("数学"),
                        select_option("英语"),
                        select_option("物理"),
                        select_option("化学"),
                        select_option("生物"),
                        select_option("历史"),
                        select_option("地理"),
                        select_option("政治"),
                    ],
                ),
                FieldSpec("分数", "number", "原始分数。", precision=1),
                FieldSpec("班排", "number", "班级排名。", precision=0),
                FieldSpec("级排", "number", "年级排名。", precision=0),
                FieldSpec(
                    "等级",
                    "select",
                    "等级或档位。",
                    multiple=False,
                    options=[
                        select_option("A"),
                        select_option("B"),
                        select_option("C"),
                        select_option("D"),
                        select_option("未评级", "Grey", "Light"),
                    ],
                ),
                FieldSpec("缺考", "select", "是否缺考。", multiple=False, options=yes_no_options),
                FieldSpec("来源列名", "text", "迁移时保留原成绩列名。"),
                FieldSpec("备注", "text", "补充说明。"),
            ],
            views=[ViewSpec("全科成绩"), ViewSpec("成绩录入")],
        ),
        TableSpec(
            name="成长事件",
            description="统一事件流：学习、德育、纪律、值日、宿舍、表扬等。",
            primary_field=FieldSpec("事件标题", "text", "事件简述。"),
            fields=[
                FieldSpec("student_ref", "link", "关联学生主档。", link_table="学生主档"),
                FieldSpec("事件日期", "datetime", "事件发生日期。"),
                FieldSpec(
                    "事件域",
                    "select",
                    "事件所属大类。",
                    multiple=False,
                    options=[
                        select_option("学习跟进"),
                        select_option("德育"),
                        select_option("纪律"),
                        select_option("值日"),
                        select_option("宿舍"),
                        select_option("表扬"),
                        select_option("班务"),
                    ],
                ),
                FieldSpec(
                    "事件类型",
                    "select",
                    "事件具体类型。",
                    multiple=False,
                    options=[
                        select_option("作业"),
                        select_option("课堂"),
                        select_option("迟到"),
                        select_option("缺勤"),
                        select_option("卫生"),
                        select_option("扣分"),
                        select_option("表扬"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec(
                    "评价",
                    "select",
                    "结果评价。",
                    multiple=False,
                    options=[
                        select_option("优秀", "Green", "Light"),
                        select_option("一般", "Blue", "Light"),
                        select_option("待改进", "Orange", "Light"),
                        select_option("严重", "Red", "Light"),
                    ],
                ),
                FieldSpec(
                    "标签",
                    "select",
                    "可多选标签。",
                    multiple=True,
                    options=[
                        select_option("作业"),
                        select_option("纪律"),
                        select_option("卫生"),
                        select_option("宿舍"),
                        select_option("课堂"),
                        select_option("家校"),
                    ],
                ),
                FieldSpec("分值变化", "number", "奖惩或评分增减。", precision=1),
                FieldSpec("描述", "text", "详细描述。"),
                FieldSpec("证据附件", "attachment", "相关截图或附件。"),
                FieldSpec("记录人", "text", "谁录入了这条记录。"),
                FieldSpec(
                    "状态",
                    "select",
                    "事件处理状态。",
                    multiple=False,
                    options=[
                        select_option("已记录"),
                        select_option("待跟进", "Orange", "Light"),
                        select_option("已完成", "Green", "Light"),
                    ],
                ),
            ],
            views=[ViewSpec("德育与班务"), ViewSpec("学习跟进"), ViewSpec("成长日历", "calendar")],
        ),
        TableSpec(
            name="家校沟通",
            description="家长电话、面谈、家访、微信等沟通记录。",
            primary_field=FieldSpec("沟通主题", "text", "沟通主题或标题。"),
            fields=[
                FieldSpec("student_ref", "link", "关联学生主档。", link_table="学生主档"),
                FieldSpec("沟通日期", "datetime", "沟通日期。"),
                FieldSpec(
                    "沟通方式",
                    "select",
                    "沟通渠道。",
                    multiple=False,
                    options=[
                        select_option("电话"),
                        select_option("面谈"),
                        select_option("家访"),
                        select_option("微信"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec(
                    "沟通对象",
                    "select",
                    "沟通对象。",
                    multiple=False,
                    options=[
                        select_option("父亲"),
                        select_option("母亲"),
                        select_option("监护人"),
                        select_option("学生本人"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec("摘要", "text", "沟通要点。"),
                FieldSpec("后续动作", "text", "下一步跟进。"),
                FieldSpec(
                    "状态",
                    "select",
                    "处理状态。",
                    multiple=False,
                    options=[
                        select_option("已记录"),
                        select_option("待回访", "Orange", "Light"),
                        select_option("已完成", "Green", "Light"),
                    ],
                ),
                FieldSpec("附件", "attachment", "附件或记录文件。"),
            ],
            views=[ViewSpec("家校沟通"), ViewSpec("待回访")],
        ),
        TableSpec(
            name="座位安排",
            description="结构化座位表数据。",
            primary_field=FieldSpec("座位版本", "text", "座位调整版本。"),
            fields=[
                FieldSpec("student_ref", "link", "关联学生主档。", link_table="学生主档"),
                FieldSpec("生效日期", "datetime", "生效时间。"),
                FieldSpec("行", "number", "座位行。", precision=0),
                FieldSpec("列", "number", "座位列。", precision=0),
                FieldSpec(
                    "区域",
                    "select",
                    "座位区域。",
                    multiple=False,
                    options=[
                        select_option("前排"),
                        select_option("中排"),
                        select_option("后排"),
                        select_option("窗边"),
                        select_option("过道"),
                    ],
                ),
                FieldSpec("同桌", "text", "同桌姓名或说明。"),
                FieldSpec("调整原因", "text", "调整理由。"),
                FieldSpec("当前有效", "select", "是否当前版本。", multiple=False, options=yes_no_options),
            ],
            views=[ViewSpec("当前座位"), ViewSpec("座位日历", "calendar")],
        ),
        TableSpec(
            name="值日安排",
            description="结构化值日表数据。",
            primary_field=FieldSpec("值日标题", "text", "如 2025-09-01 周值日。"),
            fields=[
                FieldSpec("student_ref", "link", "关联学生主档。", link_table="学生主档"),
                FieldSpec("周期开始", "datetime", "值日周期开始。"),
                FieldSpec("周期结束", "datetime", "值日周期结束。"),
                FieldSpec(
                    "岗位",
                    "select",
                    "值日岗位。",
                    multiple=False,
                    options=[
                        select_option("讲台"),
                        select_option("黑板"),
                        select_option("扫地"),
                        select_option("功能室"),
                        select_option("机动"),
                        select_option("其他"),
                    ],
                ),
                FieldSpec("组别", "text", "值日组或任务组。"),
                FieldSpec("组长", "select", "是否组长。", multiple=False, options=yes_no_options),
                FieldSpec("替班说明", "text", "调班或请假说明。"),
                FieldSpec(
                    "补做状态",
                    "select",
                    "是否需要补做。",
                    multiple=False,
                    options=[
                        select_option("正常"),
                        select_option("需补做", "Orange", "Light"),
                        select_option("已补做", "Green", "Light"),
                    ],
                ),
            ],
            views=[ViewSpec("当前值日"), ViewSpec("值日日历", "calendar")],
        ),
        TableSpec(
            name="班委任命",
            description="班委岗位与任命信息。",
            primary_field=FieldSpec("岗位名称", "text", "班委岗位。"),
            fields=[
                FieldSpec("student_ref", "link", "关联学生主档。", link_table="学生主档"),
                FieldSpec("开始日期", "datetime", "任命开始。"),
                FieldSpec("结束日期", "datetime", "任命结束。"),
                FieldSpec("当前有效", "select", "是否当前有效。", multiple=False, options=yes_no_options),
                FieldSpec("备注", "text", "岗位说明。"),
            ],
            views=[ViewSpec("当前班委"), ViewSpec("班委历史")],
        ),
        TableSpec(
            name="产物索引",
            description="生成文件的元数据索引。",
            primary_field=FieldSpec("产物标题", "text", "生成文件名称。"),
            fields=[
                FieldSpec(
                    "产物类型",
                    "select",
                    "文件类型。",
                    multiple=False,
                    options=[
                        select_option("docx"),
                        select_option("xlsx"),
                        select_option("pptx"),
                    ],
                ),
                FieldSpec("关联对象", "text", "相关学生、考试或班级对象。"),
                FieldSpec("模板名称", "text", "使用的模板。"),
                FieldSpec("本地路径", "text", "本地生成路径。"),
                FieldSpec("飞书链接", "text", "同步后写回的飞书链接。"),
                FieldSpec("生成时间", "datetime", "生成时间。"),
                FieldSpec("同步状态", "select", "同步状态。", multiple=False, options=sync_status_options),
                FieldSpec("参数摘要", "text", "渲染参数摘要。"),
            ],
            views=[ViewSpec("产物归档"), ViewSpec("最近生成")],
        ),
    ]


def build_schema_manifest() -> Dict[str, Any]:
    tables = build_table_specs()
    return {
        "schema_version": SCHEMA_VERSION,
        "workspace_backend": ["feishu_base", "notion", "obsidian", "local_only"],
        "tables": [table.public_dict() for table in tables],
        "dashboards": [
            {"name": "班级总览", "theme_style": "default"},
            {"name": "全科成绩看板", "theme_style": "SimpleBlue"},
            {"name": "德育与班务看板", "theme_style": "DarkGreen"},
            {"name": "家校沟通看板", "theme_style": "summerBreeze"},
        ],
        "artifacts": {
            "docx": ["家访记录", "班级通知", "学生谈话记录"],
            "xlsx": ["座位表", "值日表", "班委表", "扣分汇总表"],
            "pptx": ["家长会PPT"],
        },
    }


def build_backend_projection(backend: str) -> Dict[str, Any]:
    manifest = build_schema_manifest()
    if backend == "feishu_base":
        return manifest
    if backend == "notion":
        return {
            "schema_version": SCHEMA_VERSION,
            "backend": "notion",
            "databases": [
                {"name": table["name"], "fields": [table["primary_field"]["name"]] + [field["name"] for field in table["fields"]]}
                for table in manifest["tables"]
            ],
            "limitations": [
                "v1 only guarantees mapping and minimal bootstrap guidance",
                "full runtime parity with Feishu is not implemented",
            ],
        }
    if backend == "obsidian":
        return {
            "schema_version": SCHEMA_VERSION,
            "backend": "obsidian",
            "folders": [
                "00-配置",
                "01-学生主档",
                "02-考试批次",
                "03-成绩明细",
                "04-成长事件",
                "05-家校沟通",
                "06-班级安排",
                "07-产物索引",
            ],
            "limitations": [
                "v1 provides folder and template guidance only",
                "full structured runtime behavior is not implemented",
            ],
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "backend": "local_only",
        "notes": [
            "Use the unified semantic model locally.",
            "Defer backend selection until the user is ready.",
        ],
    }


def render_markdown(data: Dict[str, Any], backend: str) -> str:
    lines: List[str] = [f"# Headteacher Schema ({backend})", ""]
    lines.append(f"- Schema version: `{data.get('schema_version', SCHEMA_VERSION)}`")
    lines.append("")
    if backend == "feishu_base":
        lines.append("## Tables")
        lines.append("")
        for table in data["tables"]:
            lines.append(f"### {table['name']}")
            lines.append(table["description"])
            lines.append("")
            lines.append(f"- Primary field: `{table['primary_field']['name']}`")
            lines.append(f"- Fields: {', '.join(field['name'] for field in table['fields'])}")
            lines.append(f"- Views: {', '.join(view['name'] for view in table['views'])}")
            lines.append("")
        lines.append("## Dashboards")
        lines.append("")
        for dashboard in data["dashboards"]:
            lines.append(f"- {dashboard['name']} ({dashboard['theme_style']})")
    elif backend == "notion":
        lines.append("## Databases")
        lines.append("")
        for database in data["databases"]:
            lines.append(f"- {database['name']}: {', '.join(database['fields'])}")
        lines.append("")
        lines.append("## Limitations")
        lines.append("")
        for item in data["limitations"]:
            lines.append(f"- {item}")
    elif backend == "obsidian":
        lines.append("## Vault folders")
        lines.append("")
        for folder_name in data["folders"]:
            lines.append(f"- {folder_name}")
        lines.append("")
        lines.append("## Limitations")
        lines.append("")
        for item in data["limitations"]:
            lines.append(f"- {item}")
    else:
        lines.append("## Notes")
        lines.append("")
        for note in data["notes"]:
            lines.append(f"- {note}")
    return "\n".join(lines)


def render_summary(data: Dict[str, Any], backend: str) -> str:
    if backend == "feishu_base":
        table_names = ", ".join(table["name"] for table in data["tables"])
        return f"Feishu Base schema with {len(data['tables'])} tables: {table_names}"
    if backend == "notion":
        return f"Notion mapping with {len(data['databases'])} suggested databases"
    if backend == "obsidian":
        return f"Obsidian mapping with {len(data['folders'])} folders"
    return "Local-only schema plan"


def build_workspace_manifest_template(workspace_name: str, backend: str) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "workspace_name": workspace_name,
        "workspace_backend": backend,
        "status": "draft",
        "capabilities": {
            "setup_complete": False,
            "artifact_generation": False,
            "remote_sync": backend == "feishu_base",
        },
        "tables": [],
        "dashboards": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the unified headteacher schema manifest.")
    parser.add_argument(
        "--backend",
        default="feishu_base",
        choices=["feishu_base", "notion", "obsidian", "local_only"],
        help="Target backend projection.",
    )
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "markdown", "summary"],
        help="Output format.",
    )
    parser.add_argument("--workspace-name", default="班主任工作台", help="Workspace name for manifest templates.")
    parser.add_argument("--include-workspace-template", action="store_true", help="Include a workspace manifest template in JSON output.")
    args = parser.parse_args()

    data = build_backend_projection(args.backend)
    if args.include_workspace_template:
        data = dict(data)
        data["workspace_manifest_template"] = build_workspace_manifest_template(args.workspace_name, args.backend)

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(data, args.backend))
    else:
        print(render_summary(data, args.backend))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
