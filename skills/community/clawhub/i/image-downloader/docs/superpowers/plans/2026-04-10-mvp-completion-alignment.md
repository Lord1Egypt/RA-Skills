# MVP 文档对齐与完备性验证 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**执行状态（2026-04-10）:** 本计划对应工作已完成并已提交。下面的勾选项已按本轮实际执行结果回填；设计依据见 `docs/superpowers/specs/2026-04-10-mvp-completion-alignment-design.md`。

**Goal:** 按 MVP 标准验证当前多来源图片下载器，并将 README、SKILL、CLAUDE 与开发计划文档整理到与真实实现一致。

**Architecture:** 先做 fresh 验证，再只修改文档层，避免触碰现有下载逻辑。文档更新分为对外说明（README、SKILL）、仓库内指导（CLAUDE）和开发计划去过时三块，最后再做一次 fresh 验证并用中文提交。

**Tech Stack:** Python 3、uv、requests、unittest、git、Markdown

---

## 文件结构映射

### 需验证文件

- `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
  - 当前 CLI 入口；用于冒烟验证，不在本轮修改。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py`
  - CLI 与兼容性测试。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`
  - 模型与来源测试。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_storage.py`
  - 存储与历史去重测试。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`
  - 多来源集成测试。

### 需修改文件

- `D:/0/7/scrape/bing-keyword-image-downloader/README.md`
  - 对齐真实目录结构、测试命令、MVP 能力边界。
- `D:/0/7/scrape/bing-keyword-image-downloader/SKILL.md`
  - 对齐 skill 触发条件、依赖文件、能力边界与说明。
- `D:/0/7/scrape/bing-keyword-image-downloader/CLAUDE.md`
  - 修正“根目录仍是单来源实现”的过时描述，并补充“git 提交信息使用中文”的仓库规则。
- `D:/0/7/scrape/bing-keyword-image-downloader/docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md`
  - 清理 `pipeline.py` / `tests/test_pipeline.py` 等过时计划项，补充 MVP 已完成状态。

### 本轮新增文件

- `D:/0/7/scrape/bing-keyword-image-downloader/docs/superpowers/specs/2026-04-10-mvp-completion-alignment-design.md`
  - 已写好的设计文档，本轮不再修改，作为执行依据。

---

### Task 1: 运行 fresh 验证并记录当前 MVP 状态

**Files:**
- Verify: `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_storage.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`

- [x] **Step 1: 运行完整测试集，确认当前自动化验证通过**

Run:
```bash
uv run --with requests python -m unittest tests.test_bing_image_downloader tests.test_models_and_sources tests.test_storage tests.test_integration_multisource -v
```

Expected:
- PASS
- 输出包含 `Ran 23 tests`
- 输出包含 `OK`

- [x] **Step 2: 运行一轮 CLI 冒烟验证，确认主流程可运行**

Run:
```bash
uv run --with requests python "scripts/bing_image_downloader.py" "mvp-verify-20260410" --limit 5 --pages 3
```

Expected:
- 命令退出码为 0
- 输出中包含 `关键词:`
- 输出中包含 `保存目录: downloads/mvp-verify-20260410`
- 如未下载满 5 张，也必须有摘要输出；不可把第三方源站失败误判为脚本崩溃

- [x] **Step 3: 检查当前工作区状态，确认本轮修改前基线清晰**

Run:
```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" status --short
```

Expected:
- 仅出现设计文档未提交，或工作区为空
- 不应有与本轮无关的意外改动

---

### Task 2: 更新 README.md，使其与当前 MVP 实现一致

**Files:**
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/README.md`

- [x] **Step 1: 写入目录结构修正内容，补齐缺失模块与测试文件**

将 README 的目录结构片段调整为：

```text
bing-keyword-image-downloader/
├── .gitignore
├── README.md
├── SKILL.md
├── CLAUDE.md
├── evals/
│   └── evals.json
├── image_downloader/
│   ├── models.py
│   ├── reporting.py
│   ├── storage.py
│   └── sources/
│       ├── bing.py
│       └── demo.py
├── scripts/
│   └── bing_image_downloader.py
└── tests/
    ├── test_bing_image_downloader.py
    ├── test_models_and_sources.py
    ├── test_storage.py
    └── test_integration_multisource.py
```

- [x] **Step 2: 同步 README 的说明文字，确保文件说明与现有结构一致**

将 README 的说明列表补齐为：

```markdown
- `CLAUDE.md`：仓库内 Claude Code 工作约定与常用命令
- `image_downloader/models.py`：统一候选模型定义
- `tests/test_models_and_sources.py`：模型与来源接口测试
- `tests/test_storage.py`：存储、索引与历史去重测试
```

同时保留现有对 `reporting.py`、`storage.py`、`sources/`、`test_integration_multisource.py` 的说明。

- [x] **Step 3: 在 README 中明确 MVP 边界**

在“注意事项”段落补充或改写为以下意思的文字：

```markdown
- 当前项目已经完成多来源 MVP：支持多来源候选收集、历史去重、续写编号和运行摘要。
- 当前稳定可下载来源主要仍依赖 Bing；`demo` 来源主要用于统一接口、候选补位和失败容错验证。
```

- [x] **Step 4: 复读 README，确认没有再引用不存在的测试文件或旧架构描述**

检查点：
- 不再遗漏 `models.py`
- 不再遗漏 `test_models_and_sources.py` 与 `test_storage.py`
- 不写“当前根目录还是单来源版本”这类已过时说法

---

### Task 3: 更新 SKILL.md，使其与当前仓库能力和依赖一致

**Files:**
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/SKILL.md`

- [x] **Step 1: 修正依赖文件列表，补齐当前真实测试文件**

将 `SKILL.md` 的“依赖文件”段改为：

```markdown
## 依赖文件
- 主脚本：`scripts/bing_image_downloader.py`
- 模型与来源：`image_downloader/models.py`、`image_downloader/sources/bing.py`、`image_downloader/sources/demo.py`
- 存储与摘要：`image_downloader/storage.py`、`image_downloader/reporting.py`
- 测试文件：`tests/test_bing_image_downloader.py`、`tests/test_models_and_sources.py`、`tests/test_storage.py`
- 集成测试：`tests/test_integration_multisource.py`
```

- [x] **Step 2: 在 SKILL 中明确当前能力边界，避免夸大多来源能力**

将注意事项中的边界整理为：

```markdown
- 当前 skill 复用的是仓库内现有多来源 MVP，而不是通用全网图片下载器。
- 当前来源包含 `bing` 与 `demo`；其中 `demo` 主要用于演示统一接口、补足候选和验证失败容错，不应表述为稳定真实图片来源。
- 当用户要求避免重复下载时，应明确说明当前流程支持基于历史索引跳过重复候选，并在已有文件基础上续写编号。
```

- [x] **Step 3: 保持命令模板与 README 一致**

检查点：
- `uv run --with requests python "scripts/bing_image_downloader.py" ...` 的命令格式保持一致
- 页数经验值仍为 10/50/100 对应 3/5/10 页
- 输出说明仍指向 `downloads/<关键词>/`

- [x] **Step 4: 复读 SKILL，确认说明与 README 不冲突**

检查点：
- 关于来源、失败原因、保存目录、重复跳过的表述一致
- 不引用不存在的文件
- 不把 `demo` 说成生产级来源

---

### Task 4: 更新 CLAUDE.md 与开发计划文档，去除过时描述

**Files:**
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/CLAUDE.md`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md`

- [x] **Step 1: 修正 CLAUDE.md 中“根目录仍是单来源实现”的描述**

将 `CLAUDE.md` 的“当前仓库状态”改成贴合现实的表述，例如：

```markdown
## 当前仓库状态

- 当前项目根目录已经是多来源图片下载器的主线实现。
- 根目录包含 `image_downloader/` 模块、`scripts/bing_image_downloader.py` CLI 入口，以及模型、来源、存储、摘要和集成测试。
- 处理任务时默认以根目录当前实现为准，不再把它描述成“只有 Bing 单来源”的旧版本。
```

- [x] **Step 2: 在 CLAUDE.md 中补充中文提交信息规则**

在合适位置加入：

```markdown
## 提交约定

- 本仓库进行 git 提交时，提交信息使用中文。
```

- [x] **Step 3: 修正 CLAUDE.md 中测试命令与测试结构说明**

将测试命令统一为：

```bash
uv run --with requests python -m unittest tests.test_bing_image_downloader tests.test_models_and_sources tests.test_storage tests.test_integration_multisource -v
```

并在测试结构说明中明确四个测试文件都属于当前根目录实现。

- [x] **Step 4: 清理开发计划文档中的过时文件映射**

在 `docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md` 中：
- 删除或改写 `tests/test_pipeline.py` 相关计划条目
- 删除或改写 `image_downloader/pipeline.py` 作为“必需待建文件”的说法
- 将这部分职责改写为“已由当前 CLI 和现有模块吸收”或等价说明

- [x] **Step 5: 在开发计划文档中增加 MVP 完成状态说明**

补入以下事实：

```markdown
- 当前根目录实现已经完成多来源 MVP：支持多来源候选收集、历史去重、续写编号与运行摘要。
- `demo` 来源当前主要用于统一接口与失败容错验证，不作为稳定真实来源承诺。
- 当前阶段的主要后续工作是文档、skill、评测与后续来源扩展，而不是继续补齐基础 MVP 能力。
```

- [x] **Step 6: 复读两个文档，确认不再互相冲突**

检查点：
- `CLAUDE.md`、README、SKILL 都承认根目录已是多来源主线
- 计划文档不再要求实现当前仓库里不存在且已决定不做的 `pipeline.py`
- 提交信息中文规则已被写入 `CLAUDE.md`

---

### Task 5: 做最终 fresh 验证并使用中文提交

**Files:**
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/README.md`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/SKILL.md`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/CLAUDE.md`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md`

- [x] **Step 1: 查看最终 diff，确认只包含本轮预期文档修改**

Run:
```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" diff -- README.md SKILL.md CLAUDE.md docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md
```

Expected:
- diff 只涉及文档与说明修正
- 不应出现脚本逻辑被意外修改

- [x] **Step 2: 再次运行完整测试集，作为提交前最终验证**

Run:
```bash
uv run --with requests python -m unittest tests.test_bing_image_downloader tests.test_models_and_sources tests.test_storage tests.test_integration_multisource -v
```

Expected:
- PASS
- 输出包含 `Ran 23 tests`
- 输出包含 `OK`

- [x] **Step 3: 如需要，再跑一次 CLI 冒烟验证，确认文档更新未影响使用说明**

Run:
```bash
uv run --with requests python "scripts/bing_image_downloader.py" "mvp-final-verify-20260410" --limit 3 --pages 3
```

Expected:
- 命令退出码为 0
- 输出中包含 `保存目录: downloads/mvp-final-verify-20260410`

- [x] **Step 4: 提交本轮修改，提交信息使用中文**

Run:
```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add README.md SKILL.md CLAUDE.md docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md docs/superpowers/specs/2026-04-10-mvp-completion-alignment-design.md
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "文档: 对齐多来源 MVP 说明与开发计划"
```

Expected:
- commit 成功
- 提交信息为中文

- [x] **Step 5: 提交后检查工作区，确认收尾完成**

Run:
```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" status --short
```

Expected:
- 工作区为空
- 没有遗漏未提交修改
