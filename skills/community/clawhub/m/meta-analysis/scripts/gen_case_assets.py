# -*- coding: utf-8 -*-
"""从 cases/case_catalog.py 生成 meta-analysis 案例库全部产物：

  - cases/extraction_templates/TPL-xx_*.xlsx   11 个 Excel 提取模板
  - cases/prompts/<case_id>.md                 14 个案例提示词
  - cases/case_prompts_index.md                案例总览
  - cases/case_catalog.json                    序列化（供 runner 载入）
  - cases/README.md                            模板 ↔ 案例 ↔ 情境 的 1:1 对照索引

用法：
  C:\\Tools\\anaconda3\\python.exe scripts/gen_case_assets.py
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
CASES_DIR = os.path.join(SKILL, "cases")
sys.path.insert(0, CASES_DIR)

from case_catalog import TEMPLATES, CASES, template_by_id, case_by_id  # noqa: E402

import xlsxwriter  # noqa: E402

TPL_DIR = os.path.join(CASES_DIR, "extraction_templates")
PROMPT_DIR = os.path.join(CASES_DIR, "prompts")
os.makedirs(TPL_DIR, exist_ok=True)
os.makedirs(PROMPT_DIR, exist_ok=True)

AUTO_LABEL = {"supported": "✅ 已自动识别", "partial": "⚠️ 部分自动", "manual": "✋ 需人工映射"}


# ── 1) Excel 提取模板 ────────────────────────────────────────────────────────
def build_template_xlsx(tpl):
    path = os.path.join(TPL_DIR, tpl["file"])
    wb = xlsxwriter.Workbook(path, {"in_memory": True})

    # 格式
    title_f = wb.add_format({"bold": True, "font_size": 15, "font_color": "#1F4E78"})
    h2_f = wb.add_format({"bold": True, "font_size": 12, "font_color": "#1F4E78",
                          "bottom": 1, "border_color": "#1F4E78"})
    kv_f = wb.add_format({"text_wrap": True, "valign": "top"})
    kv_k = wb.add_format({"bold": True, "valign": "top", "bg_color": "#DDEBF7"})
    head_f = wb.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "white",
                            "border": 1, "text_wrap": True, "valign": "vcenter", "align": "center"})
    cell_f = wb.add_format({"border": 1, "valign": "vcenter"})
    cell_alt = wb.add_format({"border": 1, "valign": "vcenter", "bg_color": "#F2F7FC"})
    req_f = wb.add_format({"bold": True, "font_color": "#C00000"})
    note_f = wb.add_format({"italic": True, "font_color": "#7F7F7F", "text_wrap": True})

    # —— Sheet 1: 填写说明 ——
    ws = wb.add_worksheet("填写说明")
    ws.set_column("A:A", 18)
    ws.set_column("B:B", 92)
    r = 0
    ws.write(r, 0, "%s · %s" % (tpl["id"], tpl["name_zh"]), title_f); r += 1
    ws.write(r, 0, tpl["name_en"], note_f); r += 2

    def kv(k, v):
        nonlocal r
        ws.write(r, 0, k, kv_k)
        ws.write(r, 1, v, kv_f)
        r += 1

    kv("适用情境", tpl["scenario"])
    kv("效应量", " / ".join(tpl["measures"]))
    kv("PDF 表型", tpl["pdf_table_type"])
    kv("自动识别状态", "%s  %s" % (AUTO_LABEL.get(tpl["auto_status"], tpl["auto_status"]), tpl["auto_note"]))
    kv("校验规则", tpl["validation"])
    r += 1

    ws.write(r, 0, "录入列定义", h2_f); r += 1
    ws.write(r, 0, "列", kv_k); ws.write(r, 1, "说明（必填 / 类型）", kv_k); r += 1
    for c in tpl["columns"]:
        req = "必填" if c["required"] else "选填"
        typ = c.get("type", "")
        extra = ""
        if c.get("choices"):
            extra = " 可选项：" + "/".join(c["choices"])
        ws.write(r, 0, c["zh"], cell_f)
        ws.write(r, 1, "%s（%s，%s）%s" % (c["desc"], req, typ, extra), kv_f)
        r += 1
    ws.write(r, 0, "PDF来源(页/表)", cell_f)
    ws.write(r, 1, "选填。记录该行数据来自哪篇文献的哪一页/哪个表格，便于溯源与 A4 红线闸核验。", kv_f); r += 1
    ws.write(r, 0, "备注", cell_f)
    ws.write(r, 1, "选填。异常值、零事件、SD/SEM 疑问等说明。", kv_f); r += 2

    ws.write(r, 0, "示例数据", h2_f); r += 1
    demo = case_by_id(tpl["demo_case"])
    ws.write(r, 0, "来源案例", kv_k)
    ws.write(r, 1, "%s — %s" % (demo["id"], demo["title"]), kv_f); r += 1
    ws.write(r, 0, "用法", kv_k)
    ws.write(r, 1, "在「数据录入」sheet 已预填该案例示例行；实际使用时请将 PDF 中每篇研究的数据按列填入，删掉示例或保留作参照。", kv_f)

    # —— Sheet 2: 数据录入 ——
    ws2 = wb.add_worksheet("数据录入")
    headers = [c["zh"] for c in tpl["columns"]] + ["PDF来源(页/表)", "备注"]
    widths = [max(12, len(h) + 2) for h in headers]
    for i, w in enumerate(widths):
        ws2.set_column(i, i, w)
    for i, h in enumerate(headers):
        ws2.write(0, i, h, head_f)
    ws2.freeze_panes(1, 0)

    # 数据校验
    for i, c in enumerate(tpl["columns"]):
        if c.get("type") == "choice" and c.get("choices"):
            ws2.data_validation(1, i, 200, i,
                                {"validate": "list", "source": c["choices"]})
        elif c.get("type") in ("int", "float"):
            ws2.data_validation(1, i, 200, i,
                                {"validate": "decimal", "criteria": "greater than",
                                 "value": -1e9 if c["type"] == "float" else 0,
                                 "input_title": c["zh"], "input_message": "请输入数值"})

    # 预填示例行（来自 demo 案例）
    demo = case_by_id(tpl["demo_case"])
    for ri, st in enumerate(demo["studies"]):
        row = [st.get(c["key"], "") for c in tpl["columns"]]
        row += [st.get("pdf_source", ""), st.get("note", "")]
        fmt = cell_f if ri % 2 == 0 else cell_alt
        for ci, val in enumerate(row):
            ws2.write(ri + 1, ci, val, fmt)

    wb.close()
    return path


# ── 2) 案例提示词 markdown ───────────────────────────────────────────────────
def build_prompt_md(c):
    tpl = template_by_id(c["template_id"])
    L = []
    L.append("# %s · %s\n" % (c["id"], c["title"]))
    L.append("> 模板：`%s`（`%s`）｜效应量：`%s`｜设计：`%s`｜类别：`%s`" %
             (tpl["id"], tpl["file"], c["effect_measure"], c["design"], c["category"]))
    L.append("> 机器可读数据：`cases/case_catalog.json` 的 `%s` 条目；驱动见 `adapters/run_case_human.py --case %s`。\n" %
             (c["id"], c["id"]))
    L.append("## 一、研究问题（PICOS）\n")
    L.append("| 维度 | 内容 |")
    L.append("|---|---|")
    for k in ("P", "I", "C", "O", "S"):
        L.append("| **%s** | %s |" % (k, c["picos"].get(k, "")))
    L.append("")
    L.append("**研究类型**：%s\n" % c["design"])
    L.append("## 二、纳入与排除标准\n")
    L.append("- **纳入**：" + "；".join(c["inclusion"]))
    L.append("- **排除**：" + "；".join(c["exclusion"]) + "\n")
    L.append("## 三、纳入研究数据（演示用，虚构但量级参照真实文献）\n")
    # 数据表：按模板列
    cols = tpl["columns"]
    L.append("| " + " | ".join(c["zh"] for c in cols) + " |")
    L.append("|" + "|".join(["---"] * len(cols)) + "|")
    for st in c["studies"]:
        L.append("| " + " | ".join(str(st.get(c["key"], "")) for c in cols) + " |")
    L.append("")
    L.append("## 四、期望产出与回归基准\n")
    exp = c.get("expected", {})
    for k, v in exp.items():
        L.append("- **%s**：`%s`" % (k, v))
    L.append("")
    L.append("## 五、人工介入点（HITL 红线闸）\n")
    L.append("| 闸点 | 阶段 | 人工需核验 |")
    L.append("|---|---|---|")
    L.append("| **A4** | 数据抽取 | 各研究数据形状是否与 `%s` 模板一致、结局定义一致 |" % tpl["id"])
    L.append("| **B4** | 质量门 | GRADE 等级、过度声明条数、合并效应是否有临床意义 |")
    L.append("| **C3** | 参考文献 | 引用是否真实、与结论匹配 |")
    L.append("| **C4** | 稿件批准 | 全文表述、结论是否过度外推 |")
    L.append("")
    L.append("## 六、一句话提示词（可直接复制）\n")
    L.append("> 请对以下研究做 Meta 分析：%s。效应量=%s，数据形状见 `%s`。请在 A4/B4/C3/C4 红线闸处等待我人工核验后继续，最终输出 HTML 报告。\n" %
             (c["topic"], c["effect_measure"], tpl["file"]))
    L.append("---\n*%s*\n" % c.get("source_note", ""))
    return "\n".join(L)


def build_index_md():
    L = []
    L.append("# meta-analysis 案例库总览\n")
    L.append("> 由 `cases/case_catalog.py` 生成。案例库 = 技能最便宜的回归基准：每次改 block_a/b/c、pdf_extractor、run_stage 都跑一遍全套案例比对信封/数值是否漂移。\n")
    L.append("## 案例清单（%d 个）\n" % len(CASES))
    L.append("| 案例 | 标题 | 类别 | 设计 | 效应量 | 模板 |")
    L.append("|---|---|---|---|---|---|")
    for c in CASES:
        L.append("| %s | %s | %s | %s | %s | %s |" %
                 (c["id"], c["title"], c["category"], c["design"], c["effect_measure"], c["template_id"]))
    L.append("")
    L.append("## 模板清单（%d 个）↔ 对应案例\n" % len(TEMPLATES))
    L.append("| 模板 | 情境 | 效应量 | PDF表型 | 自动识别 | 演示案例 |")
    L.append("|---|---|---|---|---|---|")
    for t in TEMPLATES:
        cases_for = ", ".join(c["id"] for c in CASES if c["template_id"] == t["id"])
        L.append("| %s | %s | %s | %s | %s | %s |" %
                 (t["id"], t["name_zh"], "/".join(t["measures"]),
                  t["pdf_table_type"], AUTO_LABEL.get(t["auto_status"], t["auto_status"]), cases_for))
    L.append("")
    L.append("## 1:1 对应关系说明\n")
    L.append("- 每个**数据形状/研究情境**有且仅有一个 Excel 提取模板（`TPL-xx`）。")
    L.append("- 每个模板的「数据录入」sheet 列定义与 `references/data_templates.md` 完全一致，并追加 `PDF来源(页/表)` 与 `备注` 两列用于溯源。")
    L.append("- `pdf_extractor` 当前 P1 仅自动识别 T_DICHOT / T_CONTINUOUS 系列；其余形状标注「需人工映射」，模板即人工映射的落地载体。")
    L.append("- 运行：`python adapters/run_case_human.py --case <案例ID>`（默认 C01）。")
    return "\n".join(L)


def main():
    print("生成 Excel 提取模板 ...")
    for t in TEMPLATES:
        p = build_template_xlsx(t)
        print("  ✓", os.path.basename(p))
    print("生成案例提示词 ...")
    for c in CASES:
        p = os.path.join(PROMPT_DIR, "%s.md" % c["id"])
        with open(p, "w", encoding="utf-8") as f:
            f.write(build_prompt_md(c))
        print("  ✓", os.path.basename(p))
    # 总览
    with open(os.path.join(CASES_DIR, "case_prompts_index.md"), "w", encoding="utf-8") as f:
        f.write(build_index_md())
    # 序列化 catalog
    serial = {
        "templates": [{k: v for k, v in t.items() if k != "columns"} | {"columns": t["columns"]}
                      for t in TEMPLATES],
        "cases": CASES,
    }
    with open(os.path.join(CASES_DIR, "case_catalog.json"), "w", encoding="utf-8") as f:
        json.dump(serial, f, ensure_ascii=False, indent=2)
    # README 对照索引
    with open(os.path.join(CASES_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(build_index_md())
    print("\n完成：%d 模板 / %d 案例 / 索引已生成。" % (len(TEMPLATES), len(CASES)))


if __name__ == "__main__":
    main()
