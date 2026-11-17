#!/usr/bin/env python3
"""协作雷达 v0.4.7 下游导出器（安全写入 + CSV 注入防护）。

将「协作状态卡片 JSON（7 模块）」按 templates/downstream-field-mapping.md 的契约，
导出为可直接落表的格式：
  - csv    : 单一长表（module, table + 各字段），便于人工查看 / 通用导入
  - feishu : 飞书多维表格字段映射 JSON（tables[].fields/rows）
  - notion : Notion Database 字段映射 JSON（同结构，属性类型见模板）

本模块复用 process.py 的输入守卫（_load_json / RadarInputError），异常输入一律
返回友好中文提示 + 非零退出码，绝不甩 Traceback。
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from process import RadarInputError, _load_json, sanitize_and_desensitize, write_output_text


# CSV 公式注入（formula injection）防护：以公式前缀开头的单元格值，在表格软件
# （Excel / WPS / LibreOffice / Google Sheets）打开 CSV 时会被当作公式执行
# （如 "=cmd|..." 或 "=HYPERLINK(...)"），前置单引号可强制按纯文本处理。
# 评审指出的导出安全项：用户来源字段（task/owner/department/ddl 等）可能以
# = + - @ 开头，必须在写入 CSV 前转义。
FORMULA_PREFIXES = ("=", "+", "-", "@")


def escape_csv_formula(value: Any) -> str:
    """对写入 CSV 的单元格值做公式前缀转义。

    仅当值的首字符属于公式前缀时前置单引号；内部常量（module 键、表名）
    不会以这些字符开头，故可对全部单元格统一调用，不影响正常内容。
    """
    s = "" if value is None else str(value)
    if s[:1] in FORMULA_PREFIXES:
        return "'" + s
    return s


# (卡片键, 下游表名, 字段顺序) —— 顺序遵循 7 模块规范键（R4）
MODULE_TABLES = [
    ("project_overview", "项目总览", ["project_name", "stage", "overall_status", "summary", "evidence"]),
    ("progress", "已有进展", ["item", "evidence"]),
    ("confirmed_decisions", "已确认决策", ["decision", "result", "confirmed_by", "evidence"]),
    ("action_items", "Owner×DDL待办", ["task", "owner", "department", "ddl", "deliverable", "status", "evidence", "conflict"]),
    ("risks_dependencies", "风险/阻断/依赖", ["type", "description", "impact", "mitigation", "owner", "evidence"]),
    ("cross_department_relationships", "跨部门协作", ["from", "to", "collaboration_item", "status", "evidence"]),
    ("needs_human_confirmation", "需人工确认", ["item", "reason", "suggested_confirm_with", "evidence"]),
]

# 全部字段的并集（用于 CSV 表头），保持出现顺序稳定
ALL_FIELDS: list[str] = []
for _k, _t, _f in MODULE_TABLES:
    for f in _f:
        if f not in ALL_FIELDS:
            ALL_FIELDS.append(f)


def _as_rows(items: Any) -> list[dict]:
    """把模块的任意值规整成「字典列表」，对非 list/dict 输入做容错（不崩溃）。"""
    if items is None:
        return []
    if isinstance(items, list):
        return [i for i in items if isinstance(i, dict)]
    if isinstance(items, dict):
        return [items]
    return []


def build_tables(card: dict) -> list[dict]:
    """把卡片拆成「表」列表，每张表含 name / fields / rows。"""
    tables: list[dict] = []
    for key, table_name, fields in MODULE_TABLES:
        rows = _as_rows(card.get(key))
        tables.append({
            "name": table_name,
            "module": key,
            "fields": fields,
            "rows": [{f: (r.get(f, "") or "") for f in fields} for r in rows],
        })
    return tables


def export_card(
    card: dict, fmt: str, extra_entities: Iterable[str] | None = None
) -> str:
    """返回导出后的文本（csv / feishu / notion）。card 必须是 dict。"""
    if not isinstance(card, dict):
        raise RadarInputError(f"卡片必须是对象，当前是 {type(card).__name__}。")

    safe_card, _ = sanitize_and_desensitize(card, extra_entities)
    tables = build_tables(safe_card)

    if fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["module", "table"] + ALL_FIELDS)
        for key, table_name, _fields in MODULE_TABLES:
            for row in tables_dict(tables)[key]["rows"]:
                cells = [key, table_name] + [row.get(f, "") for f in ALL_FIELDS]
                # 所有单元格统一做公式前缀转义，阻断 CSV 注入（评审安全项）
                w.writerow([escape_csv_formula(c) for c in cells])
        return buf.getvalue()

    if fmt in ("feishu", "notion"):
        payload = {
            "format": fmt,
            "tables": [
                {"name": t["name"], "fields": t["fields"], "rows": t["rows"]}
                for t in tables
            ],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    raise RadarInputError(f"不支持的导出格式：{fmt}（可选 csv / feishu / notion）")


def tables_dict(tables: list[dict]) -> dict[str, dict]:
    return {t["module"]: t for t in tables}


def _load_entities(path: str | None) -> list[str]:
    if not path:
        return []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise RadarInputError(f"实体名单无法读取：{path}") from exc
    return [line.strip() for line in text.splitlines() if line.strip()]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _cli_entry(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="export_card", description="协作雷达下游导出器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_exp = sub.add_parser("export-card", help="将卡片导出为 csv/feishu/notion")
    p_exp.add_argument("--card", required=True, help="协作状态卡片 JSON 路径")
    p_exp.add_argument("--format", required=True, choices=["csv", "feishu", "notion"], help="导出格式")
    p_exp.add_argument("--entities", help="可选：已知实体名单文件，每行一个")
    p_exp.add_argument("--out", required=True, help="新的输出文件路径")
    p_exp.add_argument("--force", action="store_true", help="明确替换已存在的命名输出文件")

    sub.add_parser("selftest", help="运行导出器自检（含对抗输入）")

    args = parser.parse_args(argv)

    if args.cmd == "selftest":
        return selftest()

    if args.cmd == "export-card":
        try:
            card = _load_json(Path(args.card))
            extra = _load_entities(args.entities)
            text = export_card(card, args.format, extra_entities=extra)
            protected_paths = [Path(args.card)]
            if args.entities:
                protected_paths.append(Path(args.entities))
            write_output_text(
                Path(args.out),
                text,
                protected_paths=protected_paths,
                force=args.force,
            )
        except RadarInputError as e:
            print(f"[输入错误] {e}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as e:
            print(f"[输入错误] JSON 解析失败：{args.card}（第{e.lineno}行）：{e.msg}", file=sys.stderr)
            return 2
        except FileNotFoundError:
            print(f"[输入错误] 卡片文件不存在：{args.card}", file=sys.stderr)
            return 2
        except Exception as e:  # 兜底：任何未预期异常也不甩完整 Traceback
            print(f"[意外错误] {type(e).__name__}: {e}", file=sys.stderr)
            return 1
        print(f"已导出 {args.format} -> {args.out}")
        return 0

    return 1


def selftest() -> int:
    print("== 协作雷达 v0.4.7 下游导出器自测 ==")
    fails = 0
    import tempfile
    from pathlib import Path as _P

    sample = {
        "project_overview": {"project_name": "X项目", "stage": "设计", "overall_status": "正常", "summary": "接口由后端负责", "evidence": "周五确认"},
        "progress": [{"item": "完成设计", "evidence": "评审通过"}],
        "confirmed_decisions": [{"decision": "用方案A", "result": "已拍板", "confirmed_by": "张三", "evidence": "会议纪要"}],
        "action_items": [{"task": "联调", "owner": "李四", "department": "后端", "ddl": "下周三", "deliverable": "接口", "status": "进行中", "evidence": "群聊", "conflict": ""}],
        "risks_dependencies": [{"type": "风险", "description": "依赖外部", "impact": "延期", "mitigation": "预案", "owner": "王五", "evidence": "复盘"}],
        "cross_department_relationships": [{"from": "产品", "to": "研发", "collaboration_item": "需求澄清", "status": "进行中", "evidence": "会议"}],
        "needs_human_confirmation": [{"item": "预算", "reason": "超支", "suggested_confirm_with": "总监", "evidence": "报表"}],
    }

    # E1: CSV 导出含表头与已知值
    csv_text = export_card(sample, "csv")
    ok = "owner" in csv_text and "李四" in csv_text and "module" in csv_text
    print(("PASS" if ok else "FAIL"), "E1 CSV 导出:")
    fails += 0 if ok else 1

    # E2: 飞书 JSON 含 7 张表
    feishu = json.loads(export_card(sample, "feishu"))
    ok = len(feishu["tables"]) == 7 and feishu["tables"][3]["name"] == "Owner×DDL待办"
    print(("PASS" if ok else "FAIL"), "E2 飞书字段映射(7表):", len(feishu["tables"]), "表")
    fails += 0 if ok else 1

    # E3: notion 同结构
    notion = json.loads(export_card(sample, "notion"))
    ok = len(notion["tables"]) == 7
    print(("PASS" if ok else "FAIL"), "E3 Notion 字段映射(7表)")
    fails += 0 if ok else 1

    # E4: CSV 公式注入防护 —— 以 = + - @ 开头的用户字段必须被转义（评审安全项）
    poison = {
        "action_items": [
            {
                "task": "=SUM(A1:A9)",
                "owner": "+8613800138000",
                "department": "-未知部门",
                "ddl": "@2026-07-20",
                "deliverable": "接口",
                "status": "进行中",
                "evidence": "群聊",
                "conflict": "",
            },
        ],
    }
    csv_poison = export_card(poison, "csv")
    ok = (
        "'=SUM(A1:A9)" in csv_poison
        and "'+8613800138000" in csv_poison
        and "'-未知部门" in csv_poison
        and "'@2026-07-20" in csv_poison
    )
    print(("PASS" if ok else "FAIL"), "E4 CSV 公式前缀转义(=+-@):")
    if not ok:
        lines = [ln for ln in csv_poison.splitlines() if "=SUM" in ln]
        print("   实际 CSV 行:", lines[0] if lines else csv_poison.replace("\n", " | "))
    fails += 0 if ok else 1

    # E5: 所有导出格式都必须重新执行 PII、凭据和实体脱敏。
    sensitive = {
        "action_items": [{
            "task": "发送邮件 alice@example.com，password=demo-secret",
            "owner": "张三测试",
        }],
    }
    exports = [export_card(sensitive, fmt, ["张三测试"]) for fmt in ("csv", "feishu", "notion")]
    serialized_exports = "\n".join(exports)
    ok = all(value not in serialized_exports for value in (
        "alice@example.com", "demo-secret", "张三测试"
    ))
    print(("PASS" if ok else "FAIL"), "E5 所有导出格式重新脱敏")
    fails += 0 if ok else 1

    # 对抗：坏 JSON
    with tempfile.TemporaryDirectory() as td:
        bad = _P(td) / "bad.json"
        bad.write_text("{broken,,,", encoding="utf-8")
        try:
            _load_json(bad)
            print("FAIL", "A1 坏JSON 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A1 坏JSON -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A1 抛非预期异常 {type(e).__name__}"); fails += 1

        # 对抗：文件缺失
        try:
            _load_json(_P(td) / "nope.json")
            print("FAIL", "A2 缺文件 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A2 缺文件 -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A2 抛非预期异常 {type(e).__name__}"); fails += 1

        # 对抗：非对象卡片
        try:
            export_card([1, 2, 3], "csv")
            print("FAIL", "A3 非对象卡片 未被拦截"); fails += 1
        except RadarInputError:
            print("PASS", "A3 非对象卡片 -> RadarInputError")
        except Exception as e:
            print("FAIL", f"A3 抛非预期异常 {type(e).__name__}"); fails += 1

    print("=" * 40)
    if fails == 0:
        print("ALL PASS -- v0.4.7 下游导出器自检通过")
        return 0
    print(f"{fails} 项失败 (FAIL)")
    return 1


if __name__ == "__main__":
    raise SystemExit(_cli_entry(sys.argv[1:]))
