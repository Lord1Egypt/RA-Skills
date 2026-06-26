---
name: kinema-tdd-injector
displayName: "Kinema's TDD Injector (CLAUDE.md generator)"
version: 1.4.0
description: |
  一次性注入器，为目标仓库生成定制版 CLAUDE.md 记忆文件，植入 kinema 的 TDD 方法论（三阶测试体系、分层 conftest、网络/IO 边界、命名规则、覆盖率门槛、fixture 治理）。适用场景：用户想在新仓库初始化 TDD 规范、把测试标准注入/导入到另一个仓库、或在正式开发前确立测试约定。每个仓库只运行一次——这**不是**开发期间的常驻助手。当用户说出诸如 "把测试规范注入到这个仓库" / "init tdd standard here" / "set up testing methodology" / "import kinema's test rules" 之类的话时，请主动提及本 skill。如果检测到仓库已被注入过，进入升级模式而非拒绝。
---

# Kinema TDD 方法论注入器

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/kinema-tdd-injector

## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [references/ONBOARDING.md](references/ONBOARDING.md) 完成环境配置。**

- **首次配置** → 读取 references/ONBOARDING.md 完成全部步骤
- **环境不可用**（jinja2 未安装、模板加载失败）→ 读取 references/ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方工作流

一次性生成器，为目标仓库写入一份定制的 `CLAUDE.md`。**每个仓库仅运行一次**（升级除外），**不是**开发期间的助手。

## 渲染机制

本 skill 使用 **Jinja2 模板**渲染：

```
kinema-tdd-injector/
├── SKILL.md              ← 你正在读
├── assets/
│   └── claude_md.j2      ← 单一模板（含全部条件分支）
└── scripts/
    └── render.py         ← 渲染脚本（jinja2 依赖）
```

**渲染流程**：收集用户回答 → 构造 params dict → 调 `render.py` 输出到目标仓库根目录的临时文件 `<repo>/.kinema-claude.draft.md` → 与既有 `CLAUDE.md` 比对 → 决定写入策略 → 清理临时文件。

**临时文件位置**：始终在目标仓库根目录，命名 `.kinema-claude.draft.md`（以 `.` 开头便于 .gitignore 屏蔽）。流程结束后必须删除。

---

## 产出范围

CLAUDE.md 会包含以下章节（依据用户回答动态裁剪）：

1. 核心原则（三阶 / 两阶矩阵）
2. 测试路径三层命名规则 + 拆分规则 + 数据目录
3. Agent 自动行为规范
4. 网络边界规则
5. 依赖声明（A/B/C 三种模式之一）
6. Conftest / Fixture 治理
7. 覆盖率门槛 + 强制点（A/B/C/D 四种之一）
8. 各阶段测试编写规范（含前端 testenv Playwright e2e 子节）
9. 快速参考命令
10. Commit message（A/B/C 三种之一）
11. 前端包管理器（如有前端）
12. Python 编码规范（可选，由 Q12 控制；与前后端解耦）——含配置唯一入口规则（§.2.1，由 Q15 决定配置来源示例）

---

## 何时拒绝 / 何时进入升级模式

**拒绝条件**：仓库主要源码包含 **非 Python 且非 TS/JS 的语言**（顶层包里有 Go / Rust / Java / C++ 等）。零散脚本或 `.md` 文件不算。告知用户："本规范目前只覆盖 Python + TS/JS，检测到 X 语言，无法生成。"

**升级模式**：目标仓库现有 `CLAUDE.md` 已包含 `<!-- kinema-tdd-injector: injected -->` 标记。这种情况**不拒绝**，进入升级模式：
1. 告知用户检测到既有注入，问是否要升级。读取头部 `injector-version:` 标识符并与本 SKILL.md 当前 `version` 比对；若旧版本低于当前，进入升级模式时告知版本差异（如"检测到 v1.3.0，当前 v1.4.0，建议升级"）。无该标识符（更早产物）按未知旧版处理。
2. 同意后，从既有 CLAUDE.md 中**反解**上次的回答（覆盖率阈值、依赖模式、commit 风格、强制点、包管理器、自动触发设置、testenv 本地运行许可、配置来源），作为问卷默认值。
3. 用户回车即沿用旧值，输入新值即覆盖。
4. 反解失败的字段回退到出厂默认。

---

## 工作流

### 步骤 1 —— 确认目标仓库与语言栈

请用户确认**目标仓库根目录**（默认：当前工作目录）。扫描：

- 顶层文件和目录
- 最多 3 层深度内的所有 `pyproject.toml`、`package.json`、`Cargo.toml`、`go.mod`、`pom.xml`、`build.gradle`、`*.csproj`

若发现 `Cargo.toml` / `go.mod` / `pom.xml` / `build.gradle` / `*.csproj`，立即拒绝。

### 步骤 2 —— 发现顶层包

**不要**默认 `backend/` + `frontend/`。通过文件标志发现：

- 含 `pyproject.toml` → Python 包
- 含 `package.json`（且有 `tsconfig.json` 或 `.ts` / `.tsx` 文件） → TS/JS 包
- 仅 `package.json` 无 TS → 纯 JS 包

探测源码根：
- Python：读 `pyproject.toml` 的包配置；否则寻找含 `__init__.py` 的目录
- TS/JS：读 `package.json` 的 `main` / `module`；否则回退 `src/`

向用户列出并确认。

### 步骤 2.5 —— 检测测试根目录

本规范统一使用 `tests/`。扫描根目录：
- 已有 `tests/` → 沿用
- 已有 `test/` / `__tests__/` / `spec/` / `specs/` → **必须询问用户**：
  > 检测到根目录已有 `{{现有目录}}/`，但本规范要求 `tests/`。请选择：
  > A. 仍按规范写入 CLAUDE.md（`tests/` 为目标，迁移留给后续）  (推荐)
  > B. 让本 skill 现在就 `git mv {{现有目录}} tests` 后再生成
  > C. 中止
- 无任何测试目录 → 不询问，直接按 `tests/` 写入

### 步骤 3 —— 按前后端存在性分支

testenv 阶段是否启用，由 `testenv_integration` 控制（前后端可各自有第三阶）：启用且有后端 → 后端 API e2e；启用且有前端 → 前端 Playwright GUI e2e。

- **Python + TS/JS** → 完整三阶（后端 API e2e + 前端 Playwright e2e）
- **仅 Python** → Python 侧完整三阶，模板渲染时 `frontend=False`
- **仅 TS/JS** → 询问是否启用前端 testenv e2e：
  > 未检测到 Python 后端包。是否为前端启用 testenv 阶段（Playwright GUI e2e，连**外部部署的真实后端 + 真实库**）？
  > A. 启用前端 testenv e2e（三阶；`testenv_integration=true`，写 `tests/testenv-integration/<frontend_pkg>/*.spec.ts`）  (推荐)
  > B. 仅两阶（unit + dev-integration；`testenv_integration=false`）
  > C. 中止

**前端 testenv e2e 的 Playwright MCP 前提**：当用户启用前端 testenv（无论纯前端还是 monorepo），编写/调试 Playwright e2e 通常需要 **Playwright MCP**（交互式驱动真实浏览器辅助生成选择器）。该 MCP 一般由系统/运行环境**已提供**；若检测不到（工具列表中无 Playwright MCP），**提醒用户安装 Playwright MCP** 后再进行 e2e 编写。注入流程本身不被阻塞——这只是后续写 e2e 的前提提示。

### 步骤 4 —— 确认输出语言

> 是否使用中文写入 CLAUDE.md？（默认：是）

若用户选英文，渲染后由 Claude 翻译。模板本身仅支持中文（章节标题、表头），翻译可在渲染后做后处理。

### 步骤 5 —— 参数问卷

| # | 问题 | 默认 |
|---|------|------|
| Q1 | 自动测试触发时机（多选）：bug 修复后 / 新功能开发完成 / 重构导致接口变更 | 全选 |
| Q2 | 自动触发哪些阶段：仅 unit / unit + dev-integration | unit + dev-integration |
| Q3 | 依赖声明模式：A 单源 pyproject / B pyproject + 编译 requirements / C 仅 requirements | B |
| Q4 | 后端覆盖率总阈值 | 80 |
| Q5 | 后端每文件覆盖率兜底 | 50 |
| Q6 | 前端覆盖率总阈值 | 60 |
| Q7 | 前端每文件覆盖率兜底 | 50 |
| Q8 | 强制点：A 本地 hook / B 仅 CI / C 双保险 / D 不强制 | A |
| Q9 | Commit 风格：A CC 中文 / B CC 英文 / C 自由 | A |
| Q10 | 前端包管理器：pnpm / npm / yarn / bun | pnpm |
| Q11 | AI 协作署名加入 commit footer | 是 |
| Q12 | 是否注入 Python 编码规范章节 | 是 |
| Q13 | 后端 testenv 是否允许在开发本地运行（仅当 backend 且 testenv_integration）。许可 → Agent 在复杂 Plan 任务完成时自动跑一次；否则用户在测试服务器手动执行 | 否 |
| Q14 | 前端 testenv（Playwright e2e）是否允许在开发本地运行（仅当 frontend 且 testenv_integration） | 否 |
| Q15 | 配置注入来源（仅当 `python_standards`）：A `.env`+环境变量 / B TOML / C YAML | A |

无前端 → 跳 Q6 Q7 Q10 Q14。无后端 → 跳 Q3 Q4 Q5 Q13。**无 testenv 阶段（`testenv_integration=false`）→ Q13 Q14 都跳过**。升级模式下：以反解的旧值替代默认。

**Q15 仅当 `python_standards=true` 时提问**（与配置唯一入口规则 §{{ ps }}.2.1 配套），决定模板渲染哪种 `BaseSettings` 加载示例：A→`config_source="env"`、B→`"toml"`、C→`"yaml"`。**用户若选预制三项之外的组合模式**（如"环境变量优先 + TOML 兜底"），把 `config_source` 置为描述该组合的字符串（如 `"env+toml"`），模板会渲染占位说明，**并由你在注入流程中当场为该项目写出对应的 `config.py` 存储 / 加载方案**（在 `settings_customise_sources` 内显式排序多个 source），写入产物后再继续。`python_standards=false` 时不提问，`config_source` 不写入（模板 `| default('env')` 兜底，但该章节本身不渲染）。

**Q12 始终提问，与前后端存在性无关**——该章节为 package-agnostic 的语义级编码规范，渲染门 `python_standards` 与 `backend` 解耦，纯前端仓库也可注入。

### 步骤 6 —— 构造 params 并渲染

把问卷答案 + 步骤 1–3 探测结果整合为 params dict，写入 `<repo>/.kinema-params.tmp.json`。例：

```json
{
  "backend": true,
  "frontend": true,
  "testenv_integration": true,
  "testenv_backend_local": false,
  "testenv_frontend_local": false,
  "injector_version": "1.4.0",
  "backend_pkg": "backend",
  "backend_src_root": "app",
  "frontend_pkg": "frontend",
  "frontend_src_root": "src",
  "frontend_pkg_manager": "pnpm",
  "frontend_lockfile": "pnpm-lock.yaml",
  "pkg_list": "backend (Python), frontend (TypeScript)",
  "pkg_list_inline": "`backend/`、`frontend/`",
  "source_root_list": "`backend/app/`、`frontend/src/`",
  "auto_trigger_events": ["bug 修复后", "新功能开发完成", "重构导致接口变更"],
  "auto_trigger_stages": ["unit", "dev-integration"],
  "dep_mode": "B",
  "backend_cov_total": 80,
  "backend_cov_per_file": 50,
  "frontend_cov_total": 60,
  "frontend_cov_per_file": 50,
  "enforcement": "A",
  "commit_style": "A",
  "ai_signature": true,
  "python_standards": true,
  "config_source": "env"
}
```

- `injector_version` 取本 SKILL.md frontmatter 的 `version`（当前 `1.4.0`），写入产物头部 `injector-version:` 标识符，供升级时比对。
- `testenv_backend_local` / `testenv_frontend_local` 来自 Q13 / Q14；被跳过的题按默认 `false` 填入（模板对未提供项也用 `| default(false)` 兜底，但应显式写入便于升级反解）。

**渲染命令**（在 skill 目录下执行；`uv run --with` 自动管理 jinja2 依赖）：

```bash
uv run --with jinja2 python "<skill_root>/scripts/render.py" \
  --params "<repo>/.kinema-params.tmp.json" \
  --out "<repo>/.kinema-claude.draft.md"
```

若 `uv` 不可用，报告错误并让用户安装 `uv`（https://docs.astral.sh/uv/getting-started/installation/）后重试。不允许直接调用 `python`。

### 步骤 7 —— 与既有 CLAUDE.md 对比 + 写入

读 `<repo>/.kinema-claude.draft.md` 与 `<repo>/CLAUDE.md`（若存在）：

**Case 1：无既有 CLAUDE.md**
→ 直接 `mv .kinema-claude.draft.md CLAUDE.md`，删除 `.kinema-params.tmp.json`。

**Case 2：既有 CLAUDE.md，无冲突**

冲突判定：既有文件含**任一**以下迹象 → 视为冲突
- 标题含"测试" / "test" / "TDD" / "pytest" / "vitest" / "覆盖率" / "coverage" / "conftest" / "fixture"
- 标题与本次注入的 H1/H2/H3 完全一致

无冲突 → 直接将 draft 内容**追加**到既有 CLAUDE.md 末尾（前后加一行 `---` 分隔），删除临时文件，告知用户已追加。

**Case 3：既有 CLAUDE.md 有冲突**

向用户呈现 diff 摘要：

```
检测到既有 CLAUDE.md 与本次注入存在冲突章节：

【既有保留】不冲突的章节将原样保留：
  - "## CodeGraph 使用"
  - "## 业务域常识"

【冲突需协商】以下章节既存在于既有 CLAUDE.md 又会被本次注入：
  - "## 测试规范"  → 旧 xxx 行 / 新 yyy 行
  - "## Commit Message"

请选择融合方法：
  A. 用本次注入覆盖既有冲突章节，保留不冲突章节
  B. 在文件末尾追加本次注入全文，旧规则保留（可能出现规则重复 / 矛盾）
  C. 让我看完整 diff 后再决定
  D. 中止
```

依据用户选择写入。Case A 实施时：解析既有 markdown 的 H2/H3 章节边界，定位冲突章节区间，整段替换为 draft 中对应区间内容；非冲突章节原样保留。

### 步骤 8 —— 清理 + 注入后提示

无论哪条路径，最后都必须：
- 删除 `<repo>/.kinema-claude.draft.md`
- 删除 `<repo>/.kinema-params.tmp.json`

然后输出：

```
✅ CLAUDE.md 已生成 / 更新。

下一步：现有 tests/ 目录可能不符合新规范。本 skill 不自动迁移，
建议你接下来：

  1. 让 Claude 审计 tests/ 目录违规项（命名、目录结构、conftest 分层、fixture 命名）
  2. 分批迁移：每批 commit 一次，先后端再前端
  3. 迁移完成后启用 git hook（如果你选了强制点 A 或 C）

需要现在就开始审计吗？
```

除非用户明确同意，**不要**自行开始审计 / 迁移。

---

## 输出格式硬约束

- CLAUDE.md 第一行必须是 `<!-- kinema-tdd-injector: injected -->`
- 例子里所有路径用发现的顶层包名（不要写死 `backend` / `frontend`）
- 章节编号保持稳定

## 失败模式

- **0 个包**：报告并请用户手动声明 / 中止
- **5+ 个包**（monorepo）：列出包名并请用户筛选要纳入规范的包
- **render.py 失败**（jinja2 未装 / 模板语法错）：报告完整 stderr，让用户确认 `uv` 可用后重试。不允许直接调用 `python`

## 升级模式反解规则（简要）

升级模式下需从既有 CLAUDE.md 反解出旧参数，对应正则 / 字符串匹配建议：

| 参数 | 反解方式 |
|---|---|
| `backend_cov_total` | 搜索"≥ NN%" 在"后端"行附近 |
| `frontend_cov_total` | 同上"前端"行 |
| `dep_mode` | 看 §5 是否提到"requirements.txt"、"uv pip compile"、"pyproject.toml 唯一" |
| `enforcement` | 看 §7.4 标题文本是 "本地 git hook" / "CI" / "双保险" / "不设强制点" |
| `commit_style` | 看 §10 是中文标题还是英文，或含"自由格式" |
| `frontend_pkg_manager` | 看 §11 提到的工具名 |
| `ai_signature` | 看是否含 "Co-Authored-By" |
| `python_standards` | 检测既有 CLAUDE.md 是否含 "## ... Python 编码规范" 标题 → true，否则 false |
| `config_source` | 看 §{{ ps }}.2.1 "本项目配置来源"措辞：含"环境变量 + `.env`" → `env`；含"TOML" → `toml`；含"YAML" → `yaml`；否则取其标注的自定义组合字符串。无该子节（旧版产物）→ 默认 `env` |
| `testenv_backend_local` | 看 §3.3 后端块措辞：含"允许…开发本地运行"/"Agent…自动执行" → true；"用户在测试服务器手动执行"/"Agent **不得**自行执行" → false |
| `testenv_frontend_local` | 看 §3.3 前端块措辞，规则同上 |
| `injector_version` | 从头部 `<!-- ... injector-version: X -->` 标识符提取；与当前 SKILL.md `version` 比对，旧版本 < 当前则提示"建议升级到 vX"。无标识符 → 视为未知旧版 |

反解不到的字段，直接回退到出厂默认（同步骤 5 的默认列）。`testenv_*_local` 反解不到时默认 `false`。
