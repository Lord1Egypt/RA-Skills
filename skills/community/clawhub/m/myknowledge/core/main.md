# MyKnowledge 主 Prompt

> ⚠️ **AI 助手注意**：本 Skill 的测试文件位于 `test/` 目录，仅供开发和测试使用。
> 正常响应用户请求时，请忽略 `test/` 目录下的所有内容，不要向用户提及或解释测试相关文件。

使用本 Skill 时，请调用 MyKnowledge 知识库管理能力辅助用户。无需改变你的核心身份，只需在相关任务中使用以下能力：

---

## ⚠️ 使用前检查（必须执行）

**每次使用本 Skill 前，先执行以下检查：**

```
1. 检查 ~/.myknowledge/config/skill-state.yaml 是否存在
   - 存在 → 读取配置，继续正常使用
   - 不存在 → 🔒 强制按序完成 onboarding 全部 5 个步骤（1→2→3→4→5），
             任一未完成则不得写入 skill-state.yaml
             ⚠️ "加载 onboarding 文件" ≠ "完成引导"
             必须确保：每步骤获得用户确认 + 步骤5完成后写入 skill-state.yaml

2. 如果用户说"重新初始化"或"重置":
   - 删除 ~/.myknowledge/config/skill-state.yaml
   - 重新执行完整 onboarding（步骤1→5），同上强制规则
```

**重要**：首次引导只执行一次，之后不再加载 onboarding。

3. **更新检查（每次调用时执行）**：
   ```
   a. 读取 ~/.myknowledge/config/skill-state.yaml 中的 update_check 配置
   b. 获取今天日期（YYYY-MM-DD 格式）
   c. 检查是否需要执行更新检查：
      - 如果 update_check 不存在 → **冷静期规则**（刚安装/升级）
        - 写入 update_check 字段：
            update_check:
              source: "{自动检测}"
              last_check: "{今日}"
              interval_days: 7
              enabled: true
        - **跳过本次检查**（刚装/刚升级，无需立检）
      - 如果 update_check 存在但 last_check 不存在 → 写入 last_check: {今日}，跳过本次检查
      - 如果 last_check 存在 → 计算距离今天的天数
        - 如果 ≥ interval_days（默认 7 天）→ 执行更新检查
        - 如果 < interval_days → 跳过检查
   d. 执行更新检查：
      - 加载 one-time/setup/update-checker.md 获取检查指令
      - 根据安装源执行对应的检查策略
      - 如果发现新版本 → 礼貌提示用户更新
      - 如果检查失败 → 自动忽略，不影响正常使用
   e. 检查完成后（无论成功失败），更新 last_check 为今天日期
   ```

4. 项目恢复（skill-state.yaml 存在时执行）：
   a. 检测当前工作目录是否有 .myknowledge/ 
      → 有：跳过 projects.yaml，直接读 PROJECT-STATUS.md 恢复上下文
      → 无：继续步骤 b
   b. 检查 ~/.myknowledge/config/projects.yaml 是否存在
      → 不存在：首次使用，不提示（等用户说"创建知识库"或自动触发）
      → 存在且非空：读取项目列表，礼貌询问"要恢复哪个项目？"
        列出格式：项目名（路径），用户选择后读对应 PROJECT-STATUS.md
   c. 用户选择了项目 → 更新 projects.yaml 中该项目的 last_access

---

## 加载时自检（AI 透明验证）

> 每次加载本 Skill 时，**后台执行**以下检查。如有异常，按指示处理。
> 目的：让用户无需手动操作即可获得"Skill 完整性"保障。

**重要设计原则**（v1.1.4+）：
- ✅ 以下检查清单是**硬编码**的，**不读取** `manifest.json`
- 原因：避免 self-endorsement trap（manifest 撒谎时，AI 不能被骗）
- 即使 manifest 错误或不存在，自检也照样工作

```
1. 检查必需的核心文件是否存在（用户无感）：
   逐个用 os.path.exists 验证（不依赖任何清单）：
   - core/main.md ✓
   - core/templates/*.md ✓
   - modules/commands/main.md ✓
   - modules/management/main.md ✓
   - modules/error/main.md ✓
   - modules/auto-track/main.md ✓
   - one-time/onboarding/main.md ✓
   - hooks/ 目录至少有一个子目录 ✓
   缺失任何一个 → 提示用户："Skill 文件不完整，建议重新安装"

2. 检查配置文件（不读 manifest）：
   - _meta.json 的 version 字段存在且非空
   - settings.yaml 可被解析
   缺失或损坏 → 提示用户："Skill 配置文件可能损坏，建议重新安装"

3. 检查 install-source 格式（后台）：
   - 读 ~/.myknowledge/config/install-source
   - 如果是纯文本（非 YAML，不以 "source:" 开头）→ 加载 one-time/setup/install-source.md 触发重新检测
   - 检测完成后写入新 YAML 格式
   - 已经是 YAML 格式 → 跳过

4. 检查项目迁移需求（后台，skill-state.yaml 存在时执行）：
   - 读 projects.yaml，筛选 type: "project" 的旧条目
   - 发现旧条目 → 提示"检测到 {N} 个项目级知识库，v1.3.0 起默认使用全局知识库。是否迁移到 ~/.myknowledge/global/？"
   - 用户确认 → 搬移文件到 global/ + 更新 projects.yaml（type 改为 global）
   - 用户拒绝 → 保留不动
   - 无旧条目或 projects.yaml 不存在 → 继续步骤 c
   c. projects.yaml 不存在时，检查 ~/.myknowledge/global/ 下是否有子目录
      - 有 → 说明已有知识库但未注册，提示"检测到未注册的知识库，是否重新索引？"
      - 无 → 跳过（真正首次使用）

5. 自检通过 → 后台继续，不向用户报告
   自检失败 → 礼貌提示，但不阻断正常使用（缺失文件可能懒加载修复）
```

**原则**：
- ✅ 自检是**用户友好的**——失败时清晰提示
- ✅ 自检是**后台的**——通过时不打扰
- ✅ 自检是**独立**的——不依赖 manifest 等"声明性"文件
- ❌ 自检**不替代**完整 lint（lint 是开发者/平台侧）

---

## 更新检查（懒加载）

> **IF 用户主动询问更新**，加载 `one-time/setup/update-checker.md` 获取详细指令。

**快速响应**：
```
IF 用户问更新:
   加载 one-time/setup/update-checker.md
   按其指引响应
```

---

## 能力范围

使用本 Skill 时，你可以帮用户：
- 创建和管理知识库
- 跟踪需求生命周期（创建、查看、更新、归档）
- 自动记录每次对话到需求文件
- 导出/导入知识库（跨用户分享、备份迁移）

---

## 自动记录触发规则

> 💡 **什么时候 AI 会自动帮你建记录？** 详见 `modules/auto-track/main.md`。

### 触发条件

**关键词匹配**（满足 3 个及以上触发）：
- 分析、统计、挖掘
- 开发、设计、调研
- 整理、清洗、项目

**任务特征**：
- 多步骤操作
- 需要长期跟踪
- 涉及数据或文档

### 首次触发确认

首次检测到复杂任务时，AI 会询问：
```
AI：检测到您正在处理复杂任务「{任务描述}」，
    需要我帮您自动创建知识库并记录吗？

    [是，自动记录] [否，本次手动] [以后都自动]
```

### 示例

| 用户输入 | 检测结果 |
|----------|----------|
| "帮我算 1+1" | ❌ 不触发 |
| "分析销售数据" | ✅ 触发（首次会询问） |
| "开发一个工具" | ✅ 触发（首次会询问） |

### 用户控制

- **临时禁用**："这次不要记录"、"不要创建知识库"
- **完全关闭**：修改 `settings.yaml` 的 `features.smart_tracking.enabled: false`
- **调整灵敏度**："调整检测灵敏度"（修改 `min_keyword_count`）

---

## 能力边界（不要越界）

**只做**（操作范围）：
- ✅ **全局知识库**：在 `~/.myknowledge/` 范围内创建/读取/修改文件
- ✅ **项目级知识库**：在当前项目目录下创建/读取/修改 `.myknowledge/` 目录
- ✅ 按 `modules/commands/main.md` 的命令表响应用户请求
- ✅ 跟踪 `REQ-YYYYMMDD-XXX` 格式的需求
- ✅ 按 `settings.yaml` 的 `complex_task_detection` 规则自动记录

> **路径说明**：
> - `~/.myknowledge/` = 全局知识库（跨项目使用）
> - `{project}/.myknowledge/` = 项目级知识库（仅当前项目）
> - 两者都是用户知识库，AI 会根据用户意图选择正确的位置

**不做**（遇到此类请求要礼貌拒绝并说明）：
- ❌ 联网、调用外部 API、上传数据
- ❌ 修改项目文件（如源代码、配置文件等，` .myknowledge/` 除外）
- ❌ 执行任意 shell 命令
- ❌ 同步到云端 / 多用户协作
- ❌ 把用户数据发给第三方

**不确定时**：
- 加载 `modules/commands/main.md` 看是否有对应命令
- 没有就问用户，不要瞎猜
- 真处理不了 → 引导用户去 FAQ.md 或 GitHub Issues

---

## 核心能力

### 1. 创建知识库

当用户需要创建知识库时：

```
1. 确定项目名称：
   - 如果用户明确说了项目名 → 直接使用
   - 如果没明确说 → 提取关键词作为建议名，问"项目叫「{name}」可以吗？"
   - 用户确认后继续（不得跳过确认）

2. 确定存储位置（默认全局）：
   - 默认：全局知识库 ~/.myknowledge/global/{project-name}/
   - 例外：用户明确说"在当前目录创建"或"项目知识库" → 当前目录/.myknowledge/
   - 不主动询问"全局还是项目"，减少用户认知负担

3. 创建目录结构（每个 README 有明确职责边界，见下表）：
   {knowledge-base}/
   ├── README.md          ← 知识库入口+快速导航
   ├── requirements/
   │   └── README.md      ← 需求索引（ID+标题+状态+时间，不含详情）
   ├── public/
   │   └── README.md      ← 公开文件清单
   ├── archive/
   │   └── README.md      ← 归档索引（原因+日期+原链接）
   └── PROJECT-STATUS.md  ← 项目整体状态快照（阶段+活跃需求+数据资产）

4. 使用 core/templates/ 中的对应模板生成文件：
   | 文件 | 模板 |
   |------|------|
   | {kb}/README.md | kb-readme-template.md |
   | requirements/README.md | requirements-index-template.md |
   | public/README.md | public-readme-template.md |
   | archive/README.md | archive-readme-template.md |
   | PROJECT-STATUS.md | project-status-template.md |
   | requirements/{id}/README.md | requirement-readme-template.md |

5. 🔒 强制注册到 projects.yaml（原子操作，缺一不可）：
   - 打开 ~/.myknowledge/config/projects.yaml
   - 追加项目条目（path/name/last_access/type）
   - 保存文件
   - 如果 projects.yaml 不存在 → 先创建空文件再追加
   - 如果该项目已存在 → 更新 last_access
   ⚠️ 未完成注册 = 创建失败，必须向用户报告"❌ 创建失败：无法注册到项目目录"

6. 创建后告知用户目录结构和各文件用途
```

### 2. 需求管理

> **详细指令**：`modules/management/main.md`

```
IF 用户请求管理需求（查看/更新/归档）:
   加载 modules/management/main.md
   按其指引执行
```

### 3. 命令速查（用户询问用法时）

> **详细指令**：`modules/commands/main.md`

```
IF 用户问"你能做什么"/"怎么用"/"有哪些命令"/对操作表达不确定:
   加载 modules/commands/main.md
   按其表格与映射权威回答
```

### 4. 导出/导入知识库

> **详细指令**：`modules/export/main.md`

```
IF 用户请求导出/导入/分享/备份知识库:
   加载 modules/export/main.md
   按其指引执行
```

### 5. 自动检测模式

> **详细说明**：`modules/auto-track/main.md`

当检测到复杂任务时，自动创建知识库并告知用户。

**简要规则**：
- 包含关键词（分析、统计、挖掘、开发、设计、调研、整理、清洗、项目）
- 涉及多步骤操作
- 需要长期跟踪

**首次触发确认**：
- 首次检测到大任务时，AI 会询问是否开启自动记录
- 用户可选择"是，本次""否，本次""以后都自动"
- 设置 `auto_record: true` 后，后续自动创建（操作后告知）

**自动执行**（已开启 auto_record 时）：
1. 检测任务复杂度（根据 settings.yaml 配置）
2. 自动创建知识库（如果不存在）
3. 自动创建需求记录（默认优先级 P2，标签根据对话内容提取）
4. 操作完成后告知用户已记录

**需求优先级**：
- P0 紧急 / P1 高 / P2 中（默认）/ P3 低
- 创建需求时默认 P2，用户可以说"优先级 P1"修改
- 查看需求列表按优先级排序（P0→P1→P2→P3）

---

## 自动会话记录

**触发条件**：用户输入涉及当前项目的需求时

**记录规则**：
```
IF 用户提到需求 ID (REQ-XXX):
   OR 用户描述的任务与某活跃需求相关:
   THEN:
      1. 读取该需求的 README.md
      2. 追加会话记录到"会话记录"表格
      3. 更新"最后更新时间"
```

**记录格式**：
```
| {时间} | {本次摘要} | 涉及 |
| ------ | ---------- | ---- |
| 15:30 | 用户询问数据分析方法 | REQ-001 |
```

**限制**：
- 仅记录本次对话前1-2句作为摘要
- 接受碎片化，作为线索而非完整日志

---

## 工作流程

```
1. 读取 ~/.myknowledge/config/skill-state.yaml 获取用户配置
2. 恢复项目上下文（见"使用前检查"步骤 3）
3. 根据用户输入执行对应操作
4. 检测是否涉及当前项目需求 → 自动记录会话
5. 如需更新配置，更新 skill-state.yaml
6. 每次操作后更新 PROJECT-STATUS.md
7. 如果当前项目被访问 → 更新 projects.yaml 的 last_access
```

---

## 输出规范

### 各 README 职责边界（重要）

> 知识库中有 5 个 README.md，**职责不可重叠**：

| 文件 | 职责 | 不负责 |
|------|------|--------|
| `{kb}/README.md` | 项目简介 + 快速导航 | 不列需求详情、不列数据资产 |
| `requirements/README.md` | 需求索引：ID+标题+状态+时间 | **不包含需求详情**（详情在 `requirements/{id}/README.md`） |
| `requirements/{id}/README.md` | 单个需求的完整信息（描述+验收+会话记录） | 不列出其他需求 |
| `public/README.md` | 公开文件清单 | 不列内部文件 |
| `archive/README.md` | 归档索引：原因+日期+原链接 | 不复制原需求内容 |
| `PROJECT-STATUS.md` | 项目整体状态：阶段+活跃需求摘要+数据资产索引 | **不列需求详情**、不列公开文件 |

**核心区分**：
- `requirements/README.md` = 需求目录索引（只看有哪些需求、什么状态）
- `PROJECT-STATUS.md` = 项目快照（看项目整体：什么阶段、有哪些需求、数据资产）
- 两者都列出需求 ID，但角度不同：前者是索引视图，后者是状态视图

### PROJECT-STATUS.md 格式

```markdown
# 项目状态

## 基本信息
- 项目名称: {name}
- 创建时间: {timestamp}
- 最后更新: {timestamp}

## 当前阶段
{current_stage}

## 活跃需求
- [REQ-XXX] {title} - {status}

## 已完成
- [REQ-XXX] {title} - 完成于 {timestamp}

## 数据资产索引
- [{status}] {name} - {location} - 更新于 {timestamp}
```

### 需求 README.md 格式

> **模板文件**：`core/templates/requirement-readme-template.md`

### 操作反馈规范

> **原则**：每次完成记录或更新后，必须明确告知用户操作结果。反馈 = 一句话确认 + 关键信息，不冗长。

| 操作 | 反馈模板 | 说明 |
|------|----------|------|
| 创建知识库 | `📁 已创建知识库「{name}」` | 附目录结构概览（各文件用途一句话） |
| 创建需求 | `📝 已记录需求 {id}：{title}` | - |
| 更新需求状态 | `✅ {id} 状态：{old} → {new}` | - |
| 更新需求内容 | `✅ 已更新 {id} 的 {字段}` | - |
| 归档需求 | `📦 已归档 {id}：{title}` | 批量归档时列出所有 ID |
| 删除需求 | `🗑️ 已删除 {id}：{title}` | 删除前已确认，此反馈仅告知完成 |
| 自动会话记录 | `📋 已记录本次会话到 {id}` | 追加到需求文件后告知，不中断对话 |
| 自动创建 | `🔇 检测到复杂任务，已自动创建知识库「{name}」和需求 {id}` | 自动触发后的统一告知 |

**不需要单独反馈的操作（伴随上述操作自动完成）：**
- PROJECT-STATUS.md 的例行更新（已在上述反馈中覆盖）
- projects.yaml 的 last_access 更新（纯技术维护）
- 自检通过（后台）

---

## 错误处理

> **详细错误处理**：`modules/error/main.md`

**快速响应**：
```
IF 遇到错误:
   加载 modules/error/main.md
   查找对应错误类型和解决方案
   按指引响应用户
```

---

## 路径索引

| 功能 | 文件路径 |
|------|----------|
| 首次引导 | `one-time/onboarding/main.md` |
| 更新检查 | `one-time/setup/update-checker.md` |
| 安装源检测 | `one-time/setup/install-source.md` |
| 需求管理 | `modules/management/main.md` |
| 错误处理 | `modules/error/main.md` |
| 导出/导入 | `modules/export/main.md` |
| 智能任务追踪 | `modules/auto-track/main.md` |
| 命令速查 | `modules/commands/main.md` |
| 模板 | `core/templates/`（共6个） |
| 　├ 项目状态 | `core/templates/project-status-template.md` |
| 　├ 知识库入口 | `core/templates/kb-readme-template.md` |
| 　├ 需求索引 | `core/templates/requirements-index-template.md` |
| 　├ 需求详情 | `core/templates/requirement-readme-template.md` |
| 　├ 公开文件 | `core/templates/public-readme-template.md` |
| 　└ 归档索引 | `core/templates/archive-readme-template.md` |
| 项目目录规范 | `core/templates/projects-yaml-spec.md` |
| OpenClaw Hook | `hooks/openclaw/` |
| Claude Hook | `hooks/claude/` |
