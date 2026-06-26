# Meeting Notes Assistant — 完善计划

> 全脚本覆盖测试完成时间：2026-04-05
> 所有脚本均已测试，以下为按优先级整理的问题与改进点。
> 进度更新：截至 2026-04-05，原计划中的 11 项问题均已完成修复或收口，本文保留为复盘与能力清单。

---

## 🔴 P0 — 核心缺陷（影响日常使用，建议优先修复）

### 1. `generate_notes.py` 缺少 LLM，结构化提取几乎为空

**状态：已于 2026-04-05 修复**  
`generate_notes.py` 已完成 LLM 化：优先调用 OpenAI 兼容接口提取议题、结论、待办、关键词，支持通过 `~/.workbuddy/meeting-notes-config.json` 或环境变量配置 `llm_base_url` / `llm_api_key` / `llm_model`，同时保留规则解析作为 fallback，并新增 `--no-llm` 强制规则模式。金融场景 Prompt 也已单独补强。  
**回归验证：** 已用真实转写文本完成联调，结构化纪要可稳定产出议题、待办、关键词，并已打通 Word / PDF 导出链路。

---

### 2. `sentiment_analysis.py` 读到的是乱码（繁体+Whisper 转写未 UTF-8 标准化）

**状态：已于 2026-04-05 修复**  
已在 `transcribe_audio.py` 中加入 `opencc` 繁体转简体后处理，并在 `sentiment_analysis.py` 中改为先标准化文本、再按换行/标点逐句拆分与聚合统计，避免把整段口语文本当成单句分析。  
**回归验证：** 真实录音转写的情绪统计已从 `total_sentences=1` 提升到 `total_sentences=125`，乱码与大段文本误判问题已收口。

---

## 🟡 P1 — 功能缺失或行为不完整（应修复）

### 3. `ai_skills.py` 场景检测不覆盖金融业务

**状态：已于 2026-04-05 修复**  
已为 `detect_scenario()` 补齐 `finance` 场景关键词，并新增/完善 `extract_finance_info()`，可提取客户需求、产品方案、收益信号、风险点、下一步跟进；同时优化了口语长段切分与 `notes.json` 结构化字段展开，避免真实 Whisper 转写或结构化纪要只被当作一整段粗糙文本处理。  
**回归验证：** `smoke-test/ai-skills-finance-20260405-2000/` 中已完成 transcript + notes.json 双输入实测，7/7 通过；真实录音 `auto` 已识别为 `finance`，`finance` 提取结果包含产品方案、收益信号、风险点等字段。


---

### 4. `channels.py` `meetings` 命令返回空字段

**状态：已于 2026-04-05 修复**  
已新增共享模块 `scripts/db_config.py`，并让 `storage.py` / `channels.py` 统一复用同一套 WorkBuddy 路径解析逻辑；在相同 `--db-dir` 下，`channels meetings` 已可正确读出主会议库详情。  
**回归验证：** `smoke-test/db-path-unification-20260405-1952/` 中已完成 CLI 实测，`channels meetings 1` 正常返回标题、时间、参会人、关键词等字段。


---

### 5. `meeting_analytics.py` 读不到数据

**状态：已于 2026-04-05 修复**  
已改为复用 `scripts/db_config.py` 中的共享会议库路径解析；在相同 `--db-dir` 下，`meeting_analytics.py` 现已能读到 `storage.py` 写入的数据并输出统计报告。  
**回归验证：** `smoke-test/db-path-unification-20260405-1952/` 中 CLI 实测通过，分析结果显示 `总会议数：1`，不再出现“暂无会议数据”。


---

### 6. `export_pdf.py` 走 reportlab 而非推荐的 weasyprint

**状态：已于 2026-04-05 修复**  
已按 Windows 场景调整自动引擎顺序：`reportlab -> fpdf2 -> html`，不再默认先尝试 `weasyprint`，避免每次都先撞系统动态库缺失；非 Windows 仍保留 `weasyprint -> reportlab -> fpdf2 -> html` 的顺序。  
**回归验证：** `smoke-test/bitable-pdf-followup-20260405-2008/` 中已验证当前 Windows 环境下 `preferred_pdf_engines()` 返回 `['reportlab', 'fpdf2', 'html']`，CLI 自动导出直接生成 PDF，且不再输出 weasyprint 失败提示。


---

### 7. `send_email.py` 无测试 / 无配置引导

**状态：已于 2026-04-05 修复**  
已为 `send_email.py` 增加 `--config` 与 `--config-path`，可通过向导写入 `meeting-notes-config.json` 的 `email` 字段，并保留已有 LLM 配置；同时兼容非交互式输入，清理 BOM / 零宽字符，避免 PowerShell 管道带入脏字符。  
**回归验证：** 已完成配置写入与真实发送链路联调，当前在无可用 SMTP 服务时会稳定提示配置或连接失败原因，不再直接无提示退出。

---

## 🟢 P2 — 优化项（锦上添花）

### 8. Whisper 转写含繁体字

**状态：已于 2026-04-05 修复**  
`transcribe_audio.py` 已在转写完成后自动执行 `opencc` 繁转简处理，Whisper base 混入的繁体字不会再直接流入后续规则提取与情绪分析。  
**回归验证：** 真实录音补测已确认输出文本为简体，议题/待办提取与情绪词典命中率均明显改善。

---

### 9. `templates.py` 模板与 `export_word.py` 未打通

**状态：已于 2026-04-05 完整修复**  
`export_word.py` 现已支持两类模板：1）直接读取 `templates.py` 管理的模板名，并按 `sections` 渲染对应章节；2）读取用户提供的自定义 `.docx` 占位符模板，通过 `--template custom --template-path <模板文件>` 直接导出，其中 `{{action_items}}` 会自动渲染为三列表格。`simple` / `professional` 仍保留为内置模板别名。  
**回归验证：** `smoke-test/custom-template-regression-20260405-1944/` 已自动生成模板并完成 8/8 项检查，覆盖正文段落、正文表格、页眉、页脚，以及 `{{action_items}}` 表格插入逻辑。




---

### 10. `channels.py` 缺少 `--description` 更新功能

**状态：已于 2026-04-05 修复**  
已新增 `channels update <channel_id> [--description ...] [--color ...]`，可直接更新频道描述或颜色；若只传单个字段，会保留另一个字段的原值；未传更新字段时会返回 `Nothing to update`。  
**回归验证：** `smoke-test/channels-update-20260405-2004/` 中已完成 create / update / get / list / 异常提示全链路实测，8/8 通过。


---

### 11. `export_bitable.py` `records` 格式里的 Action Items 字段名不统一

**状态：已于 2026-04-05 修复**  
已新增 `--field-lang zh/en` 参数，且 `records` / `fields` 两种输出都会使用同一套字段名语言：中文模式输出 `类型` / `会议标题` / `时间` / `参会人` / `截止日期` 等字段，英文模式保持 `type` / `title` / `time` / `attendees` / `due`。  
**回归验证：** `smoke-test/bitable-pdf-followup-20260405-2008/` 中已完成 `records` + `json` 双格式、`zh` + `en` 双语言实测，Action Items 记录在两种语言下都能正常保留。


---

## 优先级执行建议

| 顺序 | 任务 | 当前状态 |
|---|---|---|
| 1 | `generate_notes.py` 接 LLM（最核心） | 已完成（2026-04-05） |
| 2 | `opencc` 繁简转换 | 已完成（2026-04-05） |
| 3 | 统一 DB 路径（channels/analytics/storage） | 已完成（2026-04-05） |
| 4 | `ai_skills.py` 增加金融场景 | 已完成（2026-04-05） |
| 5 | `sentiment_analysis.py` 逐句聚合 + 繁简 | 已完成（2026-04-05） |
| 6 | `send_email.py` 补配置引导 | 已完成（2026-04-05） |
| 7 | PDF 引擎顺序调整（Windows 适配） | 已完成（2026-04-05） |
| 8 | `templates.py` 打通 Word 导出 | 已完成（2026-04-05） |
| 9 | `channels.py` 增加更新能力 | 已完成（2026-04-05） |
| 10 | `export_bitable.py` 字段语言统一 | 已完成（2026-04-05） |
| 11 | 自定义 `.docx` 模板回归与文档收口 | 已完成（2026-04-05） |

当前这轮 11 项问题已全部收口，后续如果继续推进，建议转入“新增能力”阶段，而不是继续补历史缺陷。

---

## 新增能力记录

### 12. `batch_process.py` 目录级批量处理流水线

**状态：已于 2026-04-05 新增**  
新增 `scripts/batch_process.py`，支持三种模式：`full`（音频 -> 转写 -> 纪要）、`transcribe`（仅批量转写）、`notes`（基于已有转写文本批量生成纪要）；支持递归扫描、按相对目录结构输出、`--skip-existing` 增量补跑，以及同名会议信息 JSON 侧车文件。批量本地转写会复用同一个 Whisper 模型，避免逐文件重复加载。  
**回归验证：** `smoke-test/batch-process-20260405-*/` 中已覆盖 full / transcribe / notes 三种模式、递归目录、会议信息侧车文件与跳过已处理文件场景。
