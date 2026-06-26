# python_snippet 设计原理与实现参考

> **一句话**：当所需操作没有对应专用 action（`api_call` / `excel_write` / `word_write` / 浏览器系列）时，由 AI 生成完整 Python 代码，以 `python_snippet` 步骤注入 RPA 脚本的 `run()` 函数体，录制时**立即执行验证**，通过后写入 `code_block`。

---

## 一、Action 选择原则

```
有专用 action → 用专用 action（禁止用 python_snippet 替代）
没有专用 action → python_snippet（AI 生成代码 + 录制时验证）
```

| 场景 | 应使用的 action |
|------|-----------------|
| HTTP GET/POST | `api_call` |
| 读写 Excel .xlsx | `excel_write`（含 `rows_from_json` / `rows_from_excel` 动态行） |
| 读写 Word .docx（段落/表格） | `word_write` |
| 浏览器操作 | `goto` / `click` / `input` / `extract_text` / `scroll` / … |
| **多源聚合、匹配计算、自定义格式化等** | **`python_snippet`** |

---

## 二、录制时验证机制

`python_snippet` 在录制阶段**真正执行一遍**，行为与其他 action 完全一致：

| 验证阶段 | 行为 |
|----------|------|
| 语法检查 | `compile()` → 报 `SyntaxError` |
| 依赖预检 | 代码里出现 `load_workbook` / `Document` 但库未安装 → 立即返回 `deps-install B/C` 提示 |
| 执行验证 | 在与生成脚本**同构的命名空间**里 `exec()`（见下节）|
| 文件不存在 | `FileNotFoundError` → 提示"前序步骤未执行" |
| 运行时异常 | 返回 `type(e).__name__: message + traceback`（限 5 层）|
| 通过 | 打印 `✓ python_snippet 验证通过`，写入 `code_block` |

> **前序步骤保证**：由于录制器每步都实际执行（`api_call` 真的调接口落盘，`excel_write` 真的写文件），到 `python_snippet` 时所依赖的文件已在 `CONFIG["output_dir"]`（录制期间即 `~/Desktop`）中存在，`exec()` 能真实读取并运行。

---

## 三、执行环境（可用符号表）

代码在以下命名空间中执行，AI 生成代码**只能使用表内符号**：

| 符号 | 类型 | 说明 |
|------|------|------|
| `CONFIG["output_dir"]` | `Path` | 输出目录（录制时 `~/Desktop`，回放时按配置）；**所有文件路径必须通过此前缀构造** |
| `CONFIG["task_name"]` | `str` | 任务名 |
| `Path` | `pathlib.Path` | 路径操作 |
| `json` | module | 标准库 json |
| `os` | module | 标准库 os |
| `re` | module | 标准库 re |
| `datetime` | module | 标准库 datetime |
| `load_workbook` | openpyxl | 读已有 xlsx（需能力 B/F）|
| `Workbook` | openpyxl | 新建 xlsx |
| `get_column_letter` | openpyxl | 列号转字母 |
| `Document` | python-docx | 读写 docx（需能力 C/F）|
| `page` | Playwright Page | 浏览器页对象；纯文件步骤为 `None`，**不可在非浏览器步骤中调用** |

---

## 四、AI 生成 code 的检查清单

> AI 每次生成 `python_snippet.code` 前必须过一遍：

1. **路径**：所有文件路径用 `CONFIG["output_dir"] / "文件名"` 构造，**禁止硬编码** `~/Desktop` 或绝对路径
2. **openpyxl**：引用了 `load_workbook` / `Workbook` → 确认任务能力码包含 **B** 或 **F**
3. **python-docx**：引用了 `Document` → 确认任务能力码包含 **C** 或 **F**
4. **前序文件**：读取前序步骤生成的文件（如 `reconcile_raw.json`）→ 加 `if not _fp.exists(): raise FileNotFoundError(f"请先执行前序步骤，确保 {_fp} 已生成")`
5. **第三方库**：只使用表内符号；若必须引入新库（如 `pandas`），需先 `deps-install` 并在 `requirements.txt` 登记
6. **变量命名**：使用 `_` 前缀（如 `_rows`, `_wb`）避免污染命名空间

---

## 五、完整示例：AP 应付对账三步录制

以下是 AI 在录制"周五应付对账本地报告"时应发出的完整 `record-step` JSON，供参考和验证。

### 步骤 2 — `excel_write` + `rows_from_json`

从 `reconcile_raw.json` 展平嵌套数组写入「系统侧」工作表：

```json
{
  "action": "excel_write",
  "context": "写入系统侧工作表",
  "path": "对账底稿_本周.xlsx",
  "sheet": "系统侧",
  "headers": ["行ID","供应商编码","订单引用","系统金额","币种","到期日","批次号"],
  "rows_from_json": {
    "file": "reconcile_raw.json",
    "outer_key": "batches",
    "inner_key": "lines",
    "fields": ["line_id","vendor_id","po_ref","amount_system","currency","due_date"],
    "parent_fields": ["batch_id"]
  },
  "freeze_panes": "A2"
}
```

### 步骤 3a — `excel_write` + `rows_from_excel`

从 `发票导入_本周.xlsx` 复制发票数据：

```json
{
  "action": "excel_write",
  "context": "写入发票侧工作表",
  "path": "对账底稿_本周.xlsx",
  "sheet": "发票侧",
  "headers": ["发票号码","销方税号","发票金额","税额","订单引用","备注"],
  "rows_from_excel": {
    "file": "发票导入_本周.xlsx",
    "sheet": "发票侧",
    "skip_header": true
  }
}
```

### 步骤 3b — `python_snippet`（匹配计算 + 写结果 + 生成 Word）

专用 action 无法表达的计算逻辑，由 AI 生成完整代码：

```json
{
  "action": "python_snippet",
  "context": "本地匹配逻辑 + 写匹配结果 + 生成 Word 报告",
  "code": "from datetime import date as _date\n_fp_json = CONFIG[\"output_dir\"] / \"reconcile_raw.json\"\nif not _fp_json.exists():\n    raise FileNotFoundError(f\"请先执行前序 api_call 步骤，确保 {_fp_json} 已生成\")\n_raw = json.loads(_fp_json.read_text(encoding=\"utf-8\"))\n_sys_lines = []\nfor _b in _raw.get(\"batches\", []):\n    for _l in _b.get(\"lines\", []):\n        _sys_lines.append({**_l, \"batch_id\": _b[\"batch_id\"]})\n_fp_inv = CONFIG[\"output_dir\"] / \"发票导入_本周.xlsx\"\nif not _fp_inv.exists():\n    raise FileNotFoundError(f\"请确认 {_fp_inv} 已放置在输出目录\")\n_inv_wb = load_workbook(str(_fp_inv), read_only=True, data_only=True)\n_inv_ws = _inv_wb[\"发票侧\"] if \"发票侧\" in _inv_wb.sheetnames else _inv_wb.active\n_inv_rows = [list(r) for i, r in enumerate(_inv_ws.iter_rows(values_only=True)) if i > 0]\n_inv_wb.close()\n_inv_by_po = {}\nfor _r in _inv_rows:\n    _po = str(_r[4] or \"\").strip()\n    _inv_by_po.setdefault(_po, []).append(_r)\nTOLERANCE = 1.0\n_match_rows = []\nfor _sl in _sys_lines:\n    _po = str(_sl.get(\"po_ref\") or \"\").strip()\n    _amt_sys = float(_sl.get(\"amount_system\") or 0)\n    _candidates = _inv_by_po.get(_po, [])\n    if not _candidates:\n        _match_rows.append([_sl[\"line_id\"], _po, _amt_sys, \"\", \"\", \"unmatched\", \"无匹配发票\"])\n    elif len(_candidates) == 1:\n        _inv = _candidates[0]\n        _amt_inv = float(_inv[2] or 0)\n        _diff = abs(_amt_sys - _amt_inv)\n        if _diff == 0:\n            _status, _reason = \"matched\", \"\"\n        elif _diff <= TOLERANCE:\n            _status, _reason = \"partial\", f\"金额差 {_diff:.2f}\"\n        else:\n            _status, _reason = \"partial\", f\"金额差 {_diff:.2f}（超阈值）\"\n        _match_rows.append([_sl[\"line_id\"], _po, _amt_sys, _inv[0], _amt_inv, _status, _reason])\n    else:\n        _match_rows.append([_sl[\"line_id\"], _po, _amt_sys, \"\", \"\", \"pending\", f\"重复候选 {len(_candidates)} 条\"])\n_xp = CONFIG[\"output_dir\"] / \"对账底稿_本周.xlsx\"\n_wb2 = load_workbook(str(_xp)) if _xp.exists() else Workbook()\nif \"匹配结果\" in _wb2.sheetnames:\n    del _wb2[\"匹配结果\"]\n_ws2 = _wb2.create_sheet(\"匹配结果\")\n_hdrs2 = [\"系统行ID\",\"订单引用\",\"系统金额\",\"发票号码\",\"发票金额\",\"匹配状态\",\"差异说明\"]\nfor _ci, _h in enumerate(_hdrs2, 1):\n    _ws2.cell(row=1, column=_ci, value=_h)\nfor _ri, _row in enumerate(_match_rows, 2):\n    for _ci, _v in enumerate(_row, 1):\n        _ws2.cell(row=_ri, column=_ci, value=_v)\n_wb2.save(str(_xp))\nprint(\"匹配结果已写入\", _xp)\n_today = _date.today().strftime(\"%Y%m%d\")\n_wp = CONFIG[\"output_dir\"] / f\"对账报告_{_today}.docx\"\n_doc = Document()\n_doc.add_paragraph(f\"应付对账报告 {_today}\")\n_hdrs2_doc = [\"系统行ID\",\"订单引用\",\"系统金额\",\"发票号码\",\"发票金额\",\"匹配状态\",\"差异说明\"]\n_tbl = _doc.add_table(rows=1 + len(_match_rows), cols=len(_hdrs2_doc))\n_tbl.style = \"Table Grid\"\nfor _ci, _h in enumerate(_hdrs2_doc):\n    _tbl.rows[0].cells[_ci].text = str(_h)\nfor _ri, _row in enumerate(_match_rows):\n    for _ci, _v in enumerate(_row):\n        _tbl.rows[_ri + 1].cells[_ci].text = str(_v or \"\")\n_doc.save(str(_wp))\nprint(\"对账报告已生成\", _wp)"
}
```

---

## 六、相关链接

- **[SKILL.zh-CN.md](../SKILL.zh-CN.md)** — action 步骤完整参数表（含 `python_snippet`、`excel_write`、`word_write`）
- **[scenario-ap-reconciliation.md](scenario-ap-reconciliation.md)** — AP 对账完整业务场景
- **[recorder_server.py](../recorder_server.py)** — `_python_snippet_run()` 验证实现
