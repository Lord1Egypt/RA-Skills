# RPA 脚本合成指导原则

在 GENERATING 阶段，结合 Action Buffer 或录制产物生成/补全脚本时，以此文档为准。

---

## 与录制器的关系（必读）

| 场景 | 做法 |
|------|------|
| **Recorder 模式**（`record-start` → `record-end`） | 最终脚本由 `recorder_server.py` 的 `_build_final_script()` **直接拼装** `code_block` 链，**不要**用下文旧式 `get_by_role` 示例覆盖整份文件；也**禁止**在 `record-end` 已成功生成 `rpa/*.py` 后，再用 LLM「按任务描述」全文重写该文件（见 SKILL.md GENERATING 步骤 4）。若用户只补改几行，须与 [playwright-templates.md](playwright-templates.md) 及 `_build_final_script` 输出**同结构**（`CONFIG`、`_UA`、`_EXTRACT_JS`、`_wait_for_content`、`locator` + `evaluate`）。 |
| **Legacy**（仅 `add` + `generate` 或手工让 LLM 从 Buffer 合成） | 全文结构仍须对齐 [playwright-templates.md](playwright-templates.md)，**禁止**单独使用本节末尾「旧版示例」那种极简骨架。 |

---

## System Prompt（代码生成角色设定）

```
你是一名资深 Python 自动化工程师，专精 Playwright 异步框架。
将结构化操作日志（Action Buffer）或录制步骤说明转换为与 OpenClaw RPA 录制器兼容的 Python 脚本：
以 CSS `page.locator(...).first` 交互，以 `page.evaluate(_EXTRACT_JS, ...)` 批量提取文本，避免 SPA 下 locator 竞态。
```

---

## Excel / Word（openpyxl / python-docx）— 与 Recorder 拼装共存

| 规则 | 说明 |
|------|------|
| **主路径** | 录制时通过 **`record-step`** 的 **`excel_write`** / **`word_write`**；`recorder_server` 在 **`_build_final_script()`** 中把对应 `code_block` 与 Playwright 步骤写入**同一** `rpa/*.py`（`async def run()` 内），并在文件顶部按需加入 `openpyxl` / `docx` 的 import。 |
| **兜底** | 仅当未录制 Office 步骤但 `task.json` 声明需要且用户已在对话中写清结构时，才允许在 `record-end` 成功后 **向该 `.py` 末尾追加** 补充代码；**不得**覆盖录制器已生成段落。 |
| **禁止** | 删除、重排或全文替换 `_build_final_script` 已写入的 Playwright / `api_call` / Office 录制块。 |
| **依赖** | 见 `requirements.txt` 全量说明；安装：`rpa_manager.py deps-install {能力码}`。 |

`excel_write` / `word_write` 的 JSON 字段定义见 **SKILL.zh-CN.md** / **SKILL.en-US.md**「单步录制协议」表格。

---

## 输入格式

每个 Action Buffer 条目包含：

| 字段 | 说明 |
|------|------|
| `step` | 步骤序号 |
| `timestamp` | ISO 8601 时间戳 |
| `category` | Web / File / OS |
| `action` | 操作类型（与 `record-step` 一致：`goto` / `fill` / `select_option` / `click` / `press` / `extract_text` / `wait` / `scroll` / `scroll_to` 等） |
| `target` | **CSS 选择器** / 键名（`press`）/ URL（`goto`） |
| `value` | 输入值或文件名（无则空字符串） |
| `context` | 操作的一句话描述 |

---

## 脚本结构规范（与 `_build_final_script` 一致）

1. 文件顶部：`# pip install playwright && playwright install chromium` 及任务注释。
2. `CONFIG` 至少包含：`output_dir`、`headless`、`timeout`、`slow_mo`、`spa_settle_ms`、`content_wait`（含义见 [playwright-templates.md](playwright-templates.md)）。
3. 定义 `_UA`、`_EXTRACT_JS`、异步函数 `_wait_for_content(page, selector)`。
4. `async def run()`：`chromium.launch`（含 `args` 反自动化特征）、`new_context`（`user_agent`、`viewport`、`locale`、`extra_http_headers`）、`add_init_script`（隐藏 `navigator.webdriver`）、`new_page`、`set_default_timeout`。
5. 入口：`if __name__ == "__main__": asyncio.run(run())`。
6. 异常：`PlaywrightTimeout` 与通用 `Exception` 分别截图 `error_timeout.png` / `error_unexpected.png`，与录制器一致。

## 步骤规范

7. 每步骤注释可来自 `context`；每步为独立 `try/except`，失败时 `step_{N}_error.png` 与录制器 `_step_code` 一致。
8. **导航**：`goto(..., wait_until="domcontentloaded")` 后 `await page.wait_for_timeout(CONFIG["spa_settle_ms"])`。**不要**默认写 `networkidle`（易超时；除非 Buffer 明确约定）。
9. **点击 / 填写 / 原生下拉框**：`click()` / `fill()`；**原生 `<select>`** 用 `select_option(value)`，**不要**对 `<select>` 使用 `fill()`。
10. **批量提取**：`extract_text` 类步骤必须使用 `_wait_for_content(page, _sel)` + `page.evaluate(_EXTRACT_JS, [_sel, _lim])`，**不要**用 `inner_text()` 循环代替（除非单节点且 Buffer 明确要求）。

## 选择器策略（录制流水线一致）

11. 优先使用录制 / snapshot 给出的 **CSS 字符串**；组合顺序遵循 DOM 父子关系（父在前、子在后，如 `a h3` 而非 `h3 a`）。
12. `get_by_role` / `get_by_placeholder` 仅作**无法取得 CSS 时**的兜底，且合并进仓库前建议改为 `locator`，便于与 `recorder_server` 再生成 diff 一致。
13. 禁止裸 `xpath=`（必须用时注释原因）。

## 逻辑抽象规范

14. 若 Action Buffer 含重复模式，可抽函数，但**须保持**与模板相同的 `CONFIG` / `_EXTRACT_JS` 调用方式，勿引入与录制器冲突的全局状态。
15. 文件写入：`pathlib.Path`、`encoding="utf-8"`。
16. 关键步骤 `print` 到 stdout。

## 禁止事项

- 禁止硬编码凭据；禁止自动化登录页（需登录时在注释中说明手动登录后运行）。
- 不要用标准库 `time.sleep`；等待使用 `wait_for_load_state`、`wait_for_timeout`、`wait_for_selector`（与录制器一致）。

---

## 输出结构示例（片段 — 完整骨架见 playwright-templates.md）

下列片段仅演示**风格**；**完整顶栏与 `run()` 包装**请复制 [playwright-templates.md](playwright-templates.md) 的「标准脚本骨架」。

```python
# 步骤 N：{context}
try:
    await page.goto("{URL}", wait_until="domcontentloaded")
    await page.wait_for_timeout(CONFIG["spa_settle_ms"])
except Exception:
    await page.screenshot(path="step_{N}_error.png")
    raise

# 步骤 N+1：提取多条文本
try:
    _sel = "{CSS_SELECTOR}"
    _lim = 9999
    await _wait_for_content(page, _sel)
    _texts = await page.evaluate(_EXTRACT_JS, [_sel, _lim])
    _out = CONFIG["output_dir"] / "{filename}.txt"
    _out.write_text("\n".join(_texts), encoding="utf-8")
except Exception:
    await page.screenshot(path="step_{N+1}_error.png")
    raise
```

---

## 代码生成后必须输出的摘要（结构化）

生成完脚本后，在代码块之外**额外输出**以下三项，供 SKILL.md GENERATING 步骤使用：

```
逻辑摘要（脚本做了以下抽象）：
• [说明合并了哪些步骤；若无抽象，写「无，步骤均为线性顺序执行」]

需手动配置的 CONFIG 项：
• output_dir：默认 ~/Desktop
• spa_settle_ms / content_wait：可按目标站点调大

已知限制：
• [如需登录，说明手动登录后再运行]
• [若无，写「无」]
```

---

## User Message 模板

```
任务名称：{任务名}

Action Buffer（共 {N} 步）：
{Action_Buffer JSON 数组}

请严格按照 playwright-templates.md 与本文「与录制器的关系」生成完整脚本；禁止使用与录制器冲突的极简骨架或 get_by_* 为主线的旧版示例。
并在代码后输出逻辑摘要。
```
