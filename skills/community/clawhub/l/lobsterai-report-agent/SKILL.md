---
name: lobsterai-report-agent
description: Multi-Agent system for writing ultra-long feasibility study reports. Phase 0 Requirement Confirmation - Phase 1 Planner outputs outline - Phase 2 Batch parallel sub-Agent writing - Phase 2.5 Cross-chapter consistency review - Phase 3 Integrator assembles polished docx.
version: "4.0.0"
homepage: https://github.com/jinqiu193/lobsterai-report-agent
license: MIT
metadata:
  openclaw:
    category: document-generation
    triggers:
      - "写可研"
      - "写报告"
      - "多章节"
      - "并行撰写"
      - "agent写文档"
---

  Phase 2.5 跨章一致性审查 → Phase 3 整合师汇总输出精美 docx。
  核心文件：src/engine.py（核心逻辑）、src/config.py（配置）、integrate_report.py（兼容 facade）。
---

# 超长可研报告多Agent协作撰写 v3.3

## 更新日志（v4.0）

- ✅ 重构拆分：`src/config.py`（配置+I/O） + `src/engine.py`（核心逻辑） + `src/cli.py`（CLI入口）
- ✅ `integrate_report.py` 保留为 facade，100% 向后兼容旧接口
- ✅ Mermaid CLI 惰性加载（import 时不执行 subprocess）
- ✅ 路径全部可配置（环境变量 `LOBAI_CHAPTERS_DIR` / `LOBAI_OUTPUT_DIR`）
- ✅ 通知渠道可配置（`notify.py`：`log` / `feishu` / `openclaw-weixin`）
- ✅ 新增 `README.md` + `LICENSE`

## 核心能力

- **多Agent并行**：最多5个子Agent并发撰写，效率翻倍
- **增量更新**：内容未变化的章节跳过重写，速度提升
- **精美排版**：自动生成封面、表格式目录、彩色章节标题、重点标注盒、美化表格
- **飞书RAG**：自动检索飞书知识库补充参考资料
- **6种封面风格**：随意切换，适合不同场景

---

## 文件结构

```
skill_dir/
├── SKILL.md                    # 本文件
├── README.md                   # 项目说明（开源版）
├── LICENSE                    # MIT License
├── requirements.txt           # Python 依赖
├── integrate_report.py         # facade（兼容旧接口）+ CLI 入口
├── parallel_tracker.py         # 并行进度追踪
├── notify.py                  # 可配置通知渠道
├── src/
│   ├── __init__.py            # 公共 API 导出
│   ├── config.py              # 路径配置 + 文件 I/O
│   ├── engine.py               # 核心业务逻辑
│   └── cli.py                 # CLI 入口
└── references/                # 子流程参考文档
    ├── phase0_guide.md         # Phase 0 需求确认流程
    ├── phase1_guide.md         # 规划师 prompt 模板
    ├── phase2_guide.md         # 子Agent prompt 模板
    ├── table_format_guide.md   # Markdown表格格式规范
    └── bug_fix_guide.md        # Bug排查与强制重建
```

> **首次使用前**：工作目录为 `~/.config/lobsterai-report-agent/`（自动创建），可通过 `LOBAI_CHAPTERS_DIR` 环境变量覆盖。

---

## Pipeline 路由

```
用户任务
├─ 首次提出撰写需求（"我要写xxx"/"帮我写可研报告"）
│   → Phase 0 需求确认 → Phase 1 规划师
│
├─ 已有大纲，要求开始撰写
│   → Phase 2 分批并行子Agent
│
├─ 某章节需修改
│   → 小改动：直接编辑 F:/agent/chapters/0X-xxx.txt
│   → 大改动：重新生成该章节
│
├─ 所有章节已完成，要求生成 docx
│   → Phase 2.5 审查 → Phase 3 整合师汇总
│
├─ 独立小方案（2~5章，无现有chapters依赖）
│   → 直接写作 Markdown → make_docx.py 生成精美 docx
│   → 参考：references/bug_fix_guide.md "make_docx.py 模式"
│
└─ 只需查看进度/术语表/参考资料
    → 直接 CLI 命令
```

---

## Phase 0：需求确认

依次确认4项，全部确认后进入 Phase 1：

1. **写作主题**：文档类型/读者/风格/特殊约束
2. **背景信息**：项目背景/建设目标/行业背景
3. **参考资料**（最重要）：
   - A. 本地文件路径或直接粘贴
   - B. 飞书文档（RAG检索）
   - C. 直接粘贴内容
   - D. 暂不提供
4. **大纲确认**：规划师输出大纲后，用户选择 A.开始 / B.调整 / C.取消

> 参考资料越充分，内容与业务越贴合。详见 `references/phase0_guide.md`

---

## Phase 1：规划师

**输入**：Phase 0 的主题/背景/参考资料

**执行**：
```bash
python integrate_report.py glossary
```
自动生成 `plan.json` + `plan_outline_snapshot.md`

> 详细 prompt 模板见 `references/phase1_guide.md`

**完成后通知**（通过 `notify.py`，渠道由 `config.json` 的 `notification_channel` 字段决定）：

```python
# 在 Agent 指令中使用 notify 模块
from notify import notify
notify(f"""📋 报告大纲已生成

📌 《[报告主题]》
📊 章节数：[X]章
🔍 行业：[行业领域]

✅ 大纲确认后请回复"开始撰写"，系统将启动并行创作！""")
```

默认渠道为 `log`（打印到控制台）。开源用户可配置为 `feishu` 或 `openclaw-weixin`。

---

## Phase 2：分批并行子Agent

**执行流程**（全自动，无需人工确认）：
1. 展示大纲/当前批次状态（仅展示，不等待确认）
2. `python parallel_tracker.py clear` 清空上批次状态
3. 最多5并发启动子Agent（`sessions_spawn`），自动执行全部批次
4. `python parallel_tracker.py wait` 后台监控，直至本批全部完成
5. 完成后自动执行 `python integrate_report.py convert-batch`

**子Agent prompt 模板**：见 `references/phase2_guide.md`

**每批次完成后通知**：

```python
from notify import notify
notify(f"""✅ 第[X]批章节撰写完成！

📖 已完成：[已完成数]/[总章节数] 章
📝 本批完成：[章节列表]

⏳ 下一批：[下一批章节列表]
（自动进入下一批，无需人工确认）""")
```

📖 已完成：[已完成数]/[总章节数] 章
📝 本批完成：
   • [章节1标题]
   • [章节2标题]
   • [章节3标题]（如有）

⏳ 下一批：[下一批章节列表]
（自动进入下一批，无需人工确认）
```
- 小改动：直接编辑 `F:/agent/chapters/0X-xxx.txt`，保存后重新生成
- 大改动：重新触发子Agent重写，替换原文件

---

## Phase 2.5：跨章一致性审查

```bash
python integrate_report.py check
```
审查数量指标一致性与术语统一性（对照 glossary.json）

**审查完成后通知**：

```python
from notify import notify
notify(f"""🔍 一致性审查完成

✅ 术语统一性：正常
✅ 数量指标：一致
✅ 跨章引用：无冲突

📄 即将进入最终整合阶段...
```

---

## Phase 3：整合师汇总

```bash
python integrate_report.py
```

自动完成：解析章节（错误隔离）→ 更新术语表 → 一致性审查 → 生成精美 docx

**最终完成后通知**：

```python
from notify import notify
notify(f"""🎉🎉🎉 报告撰写完成！🎉🎉🎉

📄 《[报告主题]》
📊 规模：[X]章 / 约[Y]万字
🎨 封面风格：[风格名称]

✅ 精美版报告已生成！
📁 文件位置：F:/agent/chapters/output/

文心，全文已就绪，可进行后续审阅~
```

---

## 文档美化功能（自动应用）

生成报告自动包含以下排版效果（通过 `plan.json` 中 `cover_style` 字段选择）：

1. **6种封面风格** — 修改 `plan.json` → `cover_style` 字段（整数 1～6）
2. **执行摘要** — 深蓝标题条（`#1F4E79`）背景 + 白字 + 正文缩进
3. **表格式目录** — 深蓝标题条 + 三列条目（序号/章节/页码）
4. **彩色章节标题**：
   - H1：整行深藏蓝底色 `#1F4E79` + 白字微软雅黑
   - H2：中蓝底色 `#2E75B6` + 白字
   - H3：淡蓝背景 `#D6E4F0` + 深蓝字 + `▌` 左边条
5. **重点标注盒** — 自动识别【关键】【注意】【优势】【风险】【数据】标签，渲染为彩色卡片（背景/白字/边框）
6. **美化表格** — 表头深藏蓝背景 `#1F4E79` + 白字 + 奇偶行交替底色（`#DEEAF6` / `#FFFFFF`）

---

## 封面样式（6种风格）

封面风格通过 `plan.json` 中的 `cover_style` 字段指定（整数，1～6）：

| 编号 | 风格名称 | 特点 | 推荐场景 |
|------|----------|------|----------|
| 1 | 经典政务风格 | 深藏蓝顶条 + 金色点缀 | 政府/国企审批 |
| 2 | 现代简约风格 | 左侧蓝色重色块 + 右侧信息 | 科技/商务汇报 |
| 3 | 商务典雅风格 | 酒红配色 + 居中递进 | 咨询/投行报告 |
| 4 | 科技数字风格 | 深海蓝铺满 + 大字白字标题 | 互联网/数字化 |
| 5 | 中式传统风格 | 故宫红 + 宣纸米色背景 | 传统文化/国企 |
| 6 | 全屏沉浸风格 | 深海蓝铺满 + 大字白字标题 | 数字化/科技项目 |

> **注意**：`cover_style` 值为整数（如 `4`），代码会自动转换为字符串比较。

---

## CLI 命令速查

| 命令 | 作用 |
|------|------|
| `python integrate_report.py` | 生成整合报告（全量） |
| `python integrate_report.py convert-batch` | 批量生成 docx |
| `python integrate_report.py convert-one <in> <out>` | 单章转 docx |
| `python integrate_report.py check` | 一致性审查 |
| `python integrate_report.py glossary` | 术语表生成/更新 |
| `python integrate_report.py ref show` | 查看参考资料 |
| `python integrate_report.py ref clear` | 清空参考资料 |
| `python integrate_report.py preview [章节前缀]` | 预览章节摘要 |
| `python integrate_report.py feishu-search <query>` | 搜索飞书知识库 |
| `python parallel_tracker.py show` | 查看撰写进度 |
| `python parallel_tracker.py wait` | 阻塞监控（Ctrl+C停止） |
| `python parallel_tracker.py clear` | 清空追踪状态 |

> **封面风格切换**：修改 `F:/agent/chapters/plan.json` 中的 `cover_style` 字段（整数 1～6），然后重新生成。
> 修改代码后需删除 `__pycache__` 下的 `.pyc` 文件 + `content_hashes.json` 强制重建。

---

## 状态文件

> 工作目录默认：`~/.config/lobsterai-report-agent/chapters/`（可通过 `LOBAI_CHAPTERS_DIR` 环境变量覆盖）

| 文件 | 作用 |
|------|------|
| `<CHAPTERS_DIR>/plan.json` | 章节元数据 |
| `<CHAPTERS_DIR>/glossary.json` | 术语表 |
| `<CHAPTERS_DIR>/reference_material.txt` | 参考资料原文 |
| `<CHAPTERS_DIR>/plan_outline_snapshot.md` | 大纲快照 |
| `<CHAPTERS_DIR>/content_hashes.json` | 增量缓存（删后强制重建） |
| `<CHAPTERS_DIR>/writing_tracker.json` | 并行进度追踪 |
| `<CHAPTERS_DIR>/config.json` | 项目配置（封面风格、通知渠道等） |

---

## Critical Rules

### Markdown 表格格式（子Agent必须遵守）

详见 `references/table_format_guide.md`

核心要点：
- 分隔行必须是 `|---|---|---|`（首尾 `|` 不可省略）
- 各行列数必须与表头一致
- 单元格内容避免包含 `|`（用 `～` 或 `-` 表示范围）

### 强制重建（修改代码后必须两步都做）

修改 `src/engine.py` 或 `src/config.py` 后，必须同时删除以下两个文件才能让新代码生效：

```bash
# 1. 删除 .pyc 缓存（修改代码后必须）
# Linux/macOS
find . -type d -name __pycache__ -exec rm -rf {} +
# Windows
Get-ChildItem . -Recurse -Directory __pycache__ | Remove-Item -Recurse -Force

# 2. 删除增量 hash（否则增量模式跳过重写）
# 默认路径
del "%USERPROFILE%\.config\lobsterai-report-agent\chapters\content_hashes.json"

# 3. 重新生成
python integrate_report.py
```

### 已知 Bug 已修复（记录备查）

详见 `references/bug_fix_guide.md`，包括：
- `_flush_table` 未调用 `_parse_md_table` 导致表格逐字拆列（v3 早期版本）
- `ensure_mermaid_deps()` 在 import 时执行 subprocess（现已改为惰性）
- `.pyc` 缓存导致修改后的代码不生效
- `RGBColor` 用索引而非 `.red/.green/.blue` 属性
- `add_cover()` 设置 `section.margin=0` 导致正文无边距

---

## References

| 文件 | 内容 |
|------|------|
| `references/phase0_guide.md` | Phase 0 需求确认完整流程与话术 |
| `references/phase1_guide.md` | 规划师完整 prompt 模板与 plan.json 格式 |
| `references/phase2_guide.md` | 子Agent完整 prompt 模板（含表格格式警告） |
| `references/table_format_guide.md` | Markdown表格格式规范、常见错误与示例 |
| `references/bug_fix_guide.md` | Bug排查与强制重建操作步骤 |
