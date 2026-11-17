# iterate-plugin 设计文档 v3.1

> 目标：把 iterate-plugin 从「收敛看板 / 分诊 / 审查闭环的被动观察面板」升级为「质量指挥中心 + 经验银行」。
> 状态：v3.0 设计已落地（plugin 3.3.0）；**v3.4 记录 0.1.5 上游兼容窗口扩展与审查闭环补齐（plugin 3.5.1）**；**v3.5 记录全量实现审查 + 运行时重置操作闭环 + 防御性硬化（plugin 3.5.3）**；**v3.6 记录 0.2.1-alpha.1 升级 + 15 项 UX 缺口全量实现（plugin 3.6.0，§14 补记）**；**v3.7 记录 0.2.1-alpha.2 适配 + 双语 UI + 配置回读闭环（plugin 3.7.0）**；**v3.8 重定义「UX 缺口」与「dsh 能力评估」为产品功能层面，产出 14 项 UX/UI 产品缺口 + 13 项 dsh 新能力→新功能机会 + 4 项明确不可用（plugin 3.8.0）**；**v3.9 采纳 dsh 会话状态记录 API（`appendPluginRecord` → 会话绑定运行记录）并落地报告导出（Markdown/SARIF 工具 + 观测台按钮），修正 §14 C1（该 API 已公开可用）（plugin 3.9.0，同日 3.9.1/3.9.2 补 11+1 项实现审查修复）**；**v3.10 落地双向集成场景③ TS 半边（插件写出去 iterate-kernel 契约格式 + 运行时依赖）、v3.11 落地无损报告 JSON（`iterate_report format:"json"` + 观测台「导出 JSON 报告」按钮）并追上游 `0.2.2-alpha.2` 兼容、v3.12 落地开跑预检（`iterate_preflight` + 观测台 F11）、v3.13 落地验证命令自动检测（`iterate_config operation:"detect"` + 一键应用 + 预检阻断项携带建议 + F11「应用建议」）并追上游 `0.2.1-rc.5` 兼容、v3.14 把上游 `0.2.2-alpha.3` 的**统一右键菜单**新能力转化为插件的**新交互面**（会话/文件/目录右键菜单 + 观测台 open-event 桥）并追 `0.2.2-alpha.3` 兼容，设计文档迭代至 v3.14。
> 版本记录：见文末。

> **v3.0 设计主线（新增，保留 v2 全部内容不变）**：见 §5-§11。核心变化——① 定位从"被动观察面板"升级为"主动指挥中心 + 知识库"；② 新增质量门禁视图（各维度收敛度 / 验证通过率 / PASS-FAIL）；③ 新增经验银行（浏览 / 搜索 / 命中高亮 / 一键采纳）；④ 新增防御事件流（前置失败 / 回滚 / 不变量违反 / 假设被证伪）；⑤ 指挥操作原生按钮化（审批 / 指派 / 回滚 / 触发新一轮，底层仍走主工作流）；⑥ 与 harness 2.0 task_mode 打通，dsh UI 同步显示 code/iterate 指示灯。

---

## 1. 背景与现状回顾（v2 承载）

> 本节记录 v2 系列已实现能力（保留，作为 v3.0 迭代的基线），后续版本迭代不得删减本节内容。

### 1.1 项目定位
- **iterate-plugin** 是 iterate 生态的「dsh 桌面客户端插件」组件：把 iterate 生态同一套 review/fix loop 直接搬进 DeepSeek Harness (dsh) 桌面客户端界面。
- 提供**自治闭环代码迭代**（normal 模式）与 **dry-run 纯多轮审查**（只读）两种能力。
- 生态关系：skill（跨助手对话式）/ harness（无头引擎）/ plugin（dsh 桌面插件），三者共用同一套 `iterate.config.yaml` 与 9 维度审查体系。
- 开发与评审在主仓库 `jingzhao-l/iterate-skill` 完成，通过 `git subtree` 同步到独立发布仓库 `jingzhao-l/iterate-plugin`，版本发版与 npm 发布在插件仓库进行。

### 1.2 v2 已实现能力清单（当前发布 2.12.3）

#### 工具层（13 个纯函数工具）
- `iterate_config` / `iterate_validate` / `iterate_decision_log` / `iterate_context` / `iterate_review` / `iterate_triage` / `iterate_fix` / `iterate_diff` / `iterate_rollback` / `iterate_checkpoint` / `iterate_status` / `iterate_history` / `iterate_prune`
- **findings 分诊闭环**：审查 → UI 分诊（y/n/a）→ `iterate_triage` 写回 `known_intentional` → 下一轮自动过滤。
- **结构化修复系统**：每次修复先备份、写注册表、记录 diff，验证失败可 `iterate_rollback` 还原。
- **断点续跑**：长迭代在每轮开头保存 checkpoint，中断后可恢复进度。
- **历史审计**：`iterate_history` 读取决策日志与修复注册表汇总。
- **运行时清理**：`iterate_prune` 清理过期决策日志、陈旧断点、孤儿修复备份与空轮次。
- **配置读写**：`iterate_config` 支持带校验、备份、回滚的局部写入。

#### UI 层（客户端免构建槽位，防御式设计）
| UI 组件 | 挂载槽位 | 功能 |
|---|---|---|
| 收敛看板 `ConvergenceDashboard` | `conversation.input.dock` | 输入框上方实时轮次进度、严重度统计、维度徽章、趋势迷你图、修复计数徽章、运行阶段芯片 |
| 运行时观测台 `ObservatoryPanel` | `conversation.input.dock` | 输入框下方七个标签页：实时活动流 / 审查线程 / 收敛趋势 / 发现定位 / 修复与回滚 / 断点恢复 / 决策时间线；支持筛选与 JSON 导出 |
| Findings 分诊面板 `TriagePanel` | `conversation.chat.turnTail` | 逐条 y/n/a 判定，支持筛选、批量、键盘快捷键、localStorage 持久化、复制 YAML/应用指令 |
| 收敛统计卡片 `StatsCard` | `conversation.chat.turnTail` | 无 findings 时显示收敛统计、历史轮次表、趋势图、完成摘要 |
| iterate 主题皮肤 | `theme.overrideTokens` | 暖琥珀配色 13 个 dsw token 覆盖，明暗双模式 |
| 进度胶囊 `ProgressCapsule` | `shell.overlay` | 每轮完成/收敛时右下角弹出通知 |
| iterate 设置区 `SettingsPanel` | `settings.section` | 主题开关、分诊持久化说明、配置管理指引、运行时状态概览、一键清空分诊数据 |

- UI 层为**防御式设计**：`slots` / `theme` / `React` 任一不可用时自动降级，不会崩溃客户端。

### 1.3 v2 的边界与 v3.0 升级动机
- **现状**：v2 是"监控 + 轻度操作"——能看收敛进度、能分诊，但 rollback/resume 等操作需复制 `iterate_*` 命令文本（为遵守 dsh 主工作流约束）。
- **升级动机**：方向确认——**经验银行（方向 1）最适配 harness 和 plugin**。plugin 作为 dsh 界面层，v3.0 把"看"升级为"指挥 + 知识"：既能看（门禁/事件流），又能做（原生指挥操作），还能学（经验银行浏览/采纳），让积累的质量知识成为 dsh 用户的一等公民。

---

## 2. 设计原则（v3.0 延续 v2，新增指挥与知识原则）
- **防御式 UI 不变**：`slots` / `theme` / `React` 任一不可用仍自动降级，不崩溃客户端。
- **主工作流不被绕过**：所有指挥操作底层仍走 iterate 主工作流（通过插件工具触发，不绕过审查/审批/日志），只是把"复制命令文本"封装为原生按钮。
- **只读默认 + 显式确认**：写操作沿用"只读默认 + 显式确认 + 写入前备份 + 失败回滚"（与 harness WebUI §17.3 一致）。
- **经验即资产**：经验银行是方向 1 在 UI 的落地——让用户"看得到"项目积累的质量知识，并一键复用。
- **跨形态一致**：与 harness 2.0 / skill 3.0 共享同一套防御式术语与数据（task_mode / 防御事件 / 经验库）。

---

## 3. 防御式编程概念界定（与 harness 2.0 / skill 3.0 对齐）

> 生态统一词汇表（与 harness 2.0 §20.1.3、skill 3.0 §3 一致）：
> ① 最小化假设；② 信任边界验证；③ 快速失败、响亮失败（fail fast, fail loud）；④ 前置/后置条件 + 断言。
> plugin 作为界面层，其职责是**可视化这些防御事件**（发生了什么、防御住了什么），而非实现防御机制本身。

---

## 4. v3.0 总览：质量指挥中心 + 经验银行

- **定位变化**：从"被动观察面板" → **"主动指挥中心 + 知识库"**。
- **心智模型**：`被动观察` → `指挥 + 知识`：既能看（门禁/事件流），又能做（原生指挥），还能学（经验银行）。
- **实现形态**：保留免构建 Web UI 层 + 13 纯函数工具，新增/扩展面板与操作（§5-§11）。

---

## 5. 新增：质量门禁视图（Quality Gate View）

> **实现状态（plugin 3.6.0）**：已实现——F8 页签实渲染会话流中的门禁证书（PASS/FAIL + 分维度评分条）；工作流收尾处 `iterate_quality_gate({operation:"compute"})` 持久化证书；`clear` 可重置陈旧门禁。

- **功能**：显示项目门禁状态——各维度收敛度、验证通过率、整体 `PASS/FAIL` 与理由。
- **数据来源**：来自 skill 3.0 写入的**机器可读质量证书**（JSON）与 harness 决策日志聚合；`iterate_status` / `iterate_history` 扩展输出门禁快照。
- **UI 位置**：新增 `QualityGatePanel`，挂 `conversation.input.dock`（与收敛看板并列，或以新标签页并入 ObservatoryPanel）。
- **视觉**：对齐既有 severity 固定色表（严重度→红/琥珀/绿），门禁 PASS/FAIL 用绿/红徽章。

---

## 6. 新增：经验银行（Experience Bank）

> **实现状态（plugin 3.6.0）**：已实现——F9 页签渲染经验条目（含采纳按钮 + 客户端搜索）；工作流在每轮验证通过后 `iterate_experience add` 沉淀经验；`remove` 可清理错误条目。

- **功能**：浏览 / 搜索项目历史修复经验，命中高亮（"这次命中了第 N 条历史经验"），一键采纳。
- **数据来源**：harness 2.0 经验库（跨会话沉淀的修复经验）+ 决策日志 + 修复注册表；skill 3.0 作为经验生产者写入。
- **UI 位置**：新增 `ExperienceBankPanel`（可并入 ObservatoryPanel 新标签页）。
- **采纳机制**：采纳时把经验对应的修复模式/已验证修法注入当前上下文，底层仍走 iterate 主工作流（不绕过审查）。

---

## 7. 新增：防御事件流（Defense Event Stream）

> **实现状态（plugin 3.6.0）**：已实现——F10 页签渲染防御事件计数 + 事件流（标签跟随 `language`）；工作流在回滚 / 前置失败 / 不变量破坏处 `iterate_defense_events record`；`clear` 可清空事件流。

- **功能**：在观测台新增"防御事件"标签页——前置校验失败、回滚、不变量违反、假设被证伪；每次触发都显示"防御住了什么"。
- **数据来源**：harness 2.0 防御式内核事件（工具前置/后置校验结果、事务回滚、不变量违反、假设声明）经事件流推送；skill 3.0 `guard` / `invariant` 结果同步展示。
- **UI 位置**：ObservatoryPanel 新增标签页（对齐既有活动流交互：筛选、JSON 导出）。

---

## 8. 指挥操作：原生按钮化

- **功能**：审批架构修复、指派 findings、回滚到检查点、触发新一轮——原生按钮一键执行。
- **约束**：底层仍走 iterate 主工作流（通过既有 13 工具触发，记录决策日志、走审批），不绕过审查/审批/日志；写操作沿用"只读默认 + 显式确认 + 写入前备份 + 失败回滚"。
- **UI 位置**：TriagePanel（审批/指派）、ConvergenceDashboard（回滚/触发新一轮）、StatsCard（完成摘要附操作）。
- **与 v2 差异**：v2 需复制 `iterate_*` 命令文本；v3.0 封装为按钮，保留审计纪律（每次操作写入决策日志）。

---

## 9. 跨会话趋势（从质量账本读取）

> **实现状态（plugin 3.16.0）：部分实现**——单会话内跨轮对比已落地（观测台 F2 页签渲染跨轮对比表：每轮 findings / fixed / 严重度分布 / 验证结果，数据来自 report + `iterate_transcript` 的 `validations`）；**跨会话对比在 3.16.0 升级为一等交互**：F2 的「存为对比基准 / 与基准对比」把当前运行摘要（轮次/发现/critical+high/修复/验证通过率/门禁得分）持久化到 localStorage，下次运行一键并排对比（含方向着色差值），取代「导出 JSON 并排比较两次运行」的手工路径；损坏/过期的已存基准读作「无基准」而非幽灵运行。harness 趋势库（`trend_store`）直连仍未接入。

- **功能**：从质量账本读取长期趋势——顽固问题、回归检测、收敛速度变化、经验命中率。
- **数据来源**：harness 趋势库（`trend_store`）+ skill 3.0 质量账本；现有 StatsCard 趋势图升级为跨会话维度。

---

## 10. task_mode 指示灯（与 harness 2.0 打通）

- **功能**：dsh UI 同步显示当前 task_mode（code / iterate），与 harness TUI 的竖向色条一致（code=primary / iterate=amber）。
- **数据来源**：harness 2.0 status 推送 `task_mode`；plugin 读取并渲染指示灯。
- **UI 位置**：ConvergenceDashboard 或输入框区域。

---

## 11. 后端支撑与数据流

| 数据 | 来源 | 消费 |
|---|---|---|
| 质量证书（门禁快照） | skill 3.0 写入 JSON + harness 决策日志聚合 | QualityGatePanel |
| 经验库 | harness 2.0 经验库 + skill 3.0 生产者 + 决策日志/修复注册表 | ExperienceBankPanel |
| 防御事件 | harness 2.0 防御式内核事件 + skill 3.0 guard/invariant 结果 | 防御事件流标签页 |
| task_mode | harness 2.0 status 推送 | 模式指示灯 |
| 指挥操作结果 | 既有 13 工具（走主工作流） | 决策日志 + UI 刷新 |

- **实现形态**：保留免构建 Web UI（`slots` / `theme` / `React` 防御式降级），工具层扩展既有 `iterate_status` / `iterate_history` 输出，新增少量只读查询工具（经验库/门禁/防御事件），不引入新的常驻服务。

---

## 12. 里程碑与验收

| 里程碑 | 内容 | 验收 |
|---|---|---|
| M1 | QualityGatePanel + 门禁快照输出 | 门禁状态正确渲染；`iterate_status`/`history` 扩展输出单测覆盖（空/进行中/PASS/FAIL） |
| M2 | ExperienceBankPanel + 经验库查询 | 浏览/搜索/命中高亮正确；采纳后注入上下文且走主工作流；无经验时优雅空态 |
| M3 | 防御事件流标签页 | 四类防御事件（前置失败/回滚/不变量违反/假设证伪）正确展示；筛选与 JSON 导出对齐既有交互 |
| M4 | 指挥操作按钮化 | 审批/指派/回滚/触发新一轮原生触发，底层走主工作流并写决策日志；写操作走 confirm + 备份 + 回滚 |
| M5 | task_mode 指示灯 | 与 harness 2.0 status 打通，code/iterate 色条正确 |

**质量门**：
- 工具层：新增/扩展工具单测覆盖正常路径、异常路径与边界场景（沿用既有测试规范）；
- 前端：`npm run typecheck` 零错误、`npm run build` 产出正常；
- 防御式：`slots` / `theme` / `React` 任一不可用时正确降级不崩溃；
- 安全：指挥操作全部走既有权限/审计机制，不新增敏感信息暴露面。

---

## 13. 风险与开放问题
1. **dsh 槽位约束**：新面板挂载槽位可能受 dsh 版本限制——沿用既有 `slots` 防御式降级；若某槽位不可用则退化为 ObservatoryPanel 标签页。
2. **经验库数据规模**：跨会话经验可能膨胀——采纳/浏览分页 + 检索索引；清理沿用 `iterate_prune` 语义（dry-run 只报告）。
3. **指挥操作与主工作流并发**：按钮触发与运行中任务并发——沿用既有断点/暂停机制（harness Esc 暂停），切换只影响下一轮。
4. **跨形态数据一致性**：经验库/门禁/防御事件来自 harness + skill 两处——以统一事件流/JSON 契约对齐，避免双写漂移。

---

## 14. 版本记录
- v3.18（2026-11-10，plugin 3.18.0）：**设置页导航图标（dsh 0.2.2-rc.1 插件面能力转化）+ 移动端合规响应式（官方 `dsh-responsive-ui` 硬性要求补齐）**。① **能力转化**：dsh `0.2.2-rc.1` 新增「插件可为自己的设置页提供导航图标，卸载后恢复默认图标」——本插件注册与 `settings.section` 同 `id`（`iterate-settings`）的 `settings.section.icon` 贡献，纯 SVG 组件 `IterateSettingsIcon`（`size`/`active` 由壳层注入，模块级定义保身份稳定），壳层以 iterate 循环箭头替换默认字形；宿主未声明该槽位时优雅降级默认字形。② **移动合规**：此前客户端 0 个 `@media` 查询、11px 输入无地板，按官方 `dsh-responsive-ui` 补齐——5 条 `:hover` 规则全部门控到 `@media (hover: hover)`（触屏无残留高亮）、`(pointer: coarse)` 下 `.iterate-filter-search`/`.iterate-filter-select`/`.iterate-obs-input` 16px 地板（防 iOS 聚焦缩放）、`.iterate-payload` `overflow-wrap: anywhere`（超长 mono 载荷不横向溢出）、`(max-width: 480px)` 松弛进度条/搜索框最小宽度并收紧内边距（390px 最小视口不溢出）。测试 `client-render.test.ts` +4（图标注册+渲染、hover 门控+粗指针地板+载荷换行）；测试台 `boot()` 改同 id 保首个注册（面板不被图标覆盖）。上游 dsh 无新版本（仍 `0.2.2-rc.1`）。测试 1436 → 1440。**审计结论（本轮诚实修正）**：0.2.x 系列至少有 7 条插件面能力，此前仅转化 4 条；未转化候选（Session 事件日志/投影订阅 API、变更请求与工作树、working_directory 工具）已记入本文件 §14 backlog 待后续日更；0.2.2-rc.1 的 breaking（tools.resolve、Session Projection 异步、agent.model、tools.mode）经 grep 核验本插件不使用，compatible 成立但今后须逐条核验（见 TASK-plugin-daily.md 步骤 1/6 新规）。\n- v3.17（2026-11-09，plugin 3.17.0）：**F8 一键重算门禁 + F2 对比表复制（两条「只能手写 / 只能看不能带走」路径变一等交互）**。① **门禁重算闭环**：`iterate_quality_gate` 的 `compute` 载荷含手写极易错的 `findingsByRound`（每维度每轮收敛序列）；新增 `lib/parse.js` 纯构建器 `buildQualityGateComputeInstruction`（产出 `{operation:"compute"}` 指令，空/坏输入容错为裸 `{operation}`，绝不抛错）与纯归约器 `deriveQualityGateComputeInput`（维度 = 各轮线程维度并集、回退已持久化门禁维度集；findings/validationResults 取会话；findingsByRound 每维度 × 每轮补齐（缺维度轮记 0，保收敛率真实）；fixedByDimension 按成功 fix 命中同文件（+同 line 更严）finding 归因）；F8「重算门禁」按钮一键复制完整载荷，无审查/验证数据时禁用并给出明确提示。② **对比表可带走**：v3.16 的跨会话并排表只能看；新增 `src/client/run-compare.ts` 纯渲染器 `buildRunCompareMarkdown`（逐指标 `| 指标 | 基准 | 当前 | 变化 |`，`null` → `—`，标签由调用方按当前语言注入），F2「复制对比表」复制 Markdown 进剪贴板，失败揭示原文。两者均为纯函数（无 React / DOM / 中文依赖），双语标签入 i18n，`package-contract` 强制 dist/`lib/client.js` 与 `src/` 齐步。**修复**：`dist/tools/decision-log.js` 未随 `fix(consumers)`「plugin 校验丢内部空行」重建（`verifyDecisionLedger` 曾按 `decodedLines` 丢内部空行重排账本、掩盖真实断裂）→ 重建 dist 走 `ledgerTextForVerify`；`src/index.ts` 与 README 工具计数统一为 19（原 18/17）。上游 dsh 无新版本（最新仍 `dsh-v0.2.2-rc.1`，无插件面新能力可转化）。测试 1422 → 1436（+14：parse 9 + run-compare 3 + client-render 4，含 1 例修正）。
- v3.14（2026-11-03，plugin 3.14.0）：**把 dsh 0.2.2-alpha.3 的统一右键菜单新能力转化为插件的净新增交互面 + 兼容追到 0.2.2-alpha.3**。上游 alpha.3（2026-11-03）新增 `@deepseek-ai/dsh-client-ui-context-menu`：任何客户端插件可注册作用于会话/文件/目录/URL/图片/页签/工作区的右键菜单动作，无需引入 React 组件，目标在被点击后保持固定，插件卸载自动撤销。本插件新增 `src/client/context-menu.ts`：纯构建器（`buildSessionMenuEntries`/`buildFileMenuEntries`/`buildDirectoryMenuEntries`，双语、可单测）+ 命令式接线（`registerIterateContextMenus`，注入 `copy`/`openPanel`/`notify`）。**Session** 右键提供 5 项（打开 iterate 质量指挥中心 / 复制开跑预检 / 复制 dry-run / 复制断点恢复 / 复制磁盘快照），**File** 提供 2 项（仅审查此文件（带行号）/ 打开指挥中心），**Directory** 提供 3 项（仅审查此目录 / 复制开跑预检 / 打开指挥中心）；指令全部复用观测台同一套构建器（`buildPreflightInstruction`/`START_INSTRUCTIONS.reviewOnly`/`buildCheckpointResumeInstruction`/`buildDiskSnapshotInstruction`），新指令构建器 `buildScopedReviewInstruction`（`iterate_review plan` 无逐次 `scope` 参数，故用自然语言把审查范围限定到被右键路径，空范围防御性返回空串）。「打开指挥中心」经 window 自定义事件 `iterate-plugin:open-observatory` 通知对应观测台面板（携带 `sessionId` 只响应匹配会话，无则单面板回退；目标页签可指定，非法回退 `live`）。服务缺失宿主（<0.2.2-alpha.3）优雅降级为无菜单项，停靠面板仍是入口；重复贡献 id / 不支持 target 家族仅记录并继续。上游兼容：`dshReleases` 28 → 29，三个 dsh peer 加 `|| 0.2.2-alpha.3`，`@deepseek-ai/cordis` peer 扩为 `^4.0.5-alpha.2 || ~4.0.6-alpha.1 || ~4.0.6-alpha.2`，devDeps 全部钉 `0.2.2-alpha.3`/`cordis 4.0.6-alpha.2`；alpha.3 其余插件面变更（Cordis Core 同步、设置页导航图标、SDK 原生命令、动态 pi-ai 请求头、`apply_patch` 工具、`dsh.profile.bundles` 工作树合入等）经评估均无破坏性影响本插件，除 `contextMenus` 外未转化（图标与命令为纯外观/宿主侧，apply_patch 与本插件的原子修复正交，见 C 类逐条）。测试 1374 → 1391（+17：context-menu 9 + parse 5 + client-render 3）。
- v3.13（2026-10-31，plugin 3.13.0）：**验证命令自动检测——新的失败模式防御 + 与主流程更细粒度接入点**。开跑预检的阻断项此前只能手写 YAML（错误嵌套、错误模块键、写了项目根本不存在的命令），现可自动识别项目并一键应用。新增 `src/validation-detect.ts`：`detectValidationCommands` 只读检查项目 manifest——node（`package.json` 的 `test`/`typecheck`/`lint`/`build` 四脚本，按序）、python（`pytest -q` + 配置过的 `ruff check .`/`mypy .`，含 `tests/` 目录兜底）、rust（`cargo test` + 配置过的 `cargo clippy`/`cargo fmt --check`）、go（`go test ./...` + `go vet ./...`）、make（`make test`/`make check` 兜底，仅当无任何生态专属命令）；按序去重、上限 6、坏 JSON / 不可读 / 非对象 manifest 一律降级为"未检测到"而不抛错；`buildValidationUpdates` 生成可深合并的部分配置。`iterate_config` 新增 `operation:"detect"`（可 `apply:true` 一键写入，走与 `write` 相同的备份 + 校验 + 回滚 + 项目锁路径；已配置时拒绝，`force:true` 才覆盖）；`iterate_preflight` 阻断项携带 `suggestedCommands`/`ecosystem`/`detectedFrom`，`render` 输出「检测到 {ecosystem} 项目，建议：…」；观测台 F11 阻断的验证命令行显示「应用建议」按钮（复制 `iterate_config` 的 `operation:"write"` 指令，携带完整 `validation.commands.default` 载荷），无建议时保留原「配置验证命令」。上游 dsh `dsh-v0.2.1-rc.5`（2026-10-30，仅「优化对话中思考内容展示」，无插件面 API 变动）声明 compatible：`dshReleases` 27 → 28，三个 peer 范围加 `|| 0.2.1-rc.5`，devDeps 保持更高线 `0.2.2-alpha.2` 作为构建目标；无破坏性变更不阻断，无新增插件面 API 可转化（C 类记录"无新能力"）。测试 1340 → 1374（+34：validation-detect 18 + config-tool 6 + preflight 6 + parse 3 + client 2，其中 1 例在 validation-detect 内）。
- v3.12（2026-10-29，plugin 3.12.0）：**开跑预检（Preflight）——新的失败模式防御 + 与主流程更细粒度接入点**。新增第 19 个工具 `iterate_preflight`：只读开跑前预检，返回结构化清单——`validation`（**阻断项**，空 `validation.commands` 意味着本轮无法证明修复）、`git`（是否 Git 仓库）、`dirty-tree`（未提交/未跟踪文件数，git 不可用时降级为"未知"而非误报警告）、`stale-gate`（磁盘残留 FAIL 门禁）、`interrupted-checkpoint`（中断断点）；每项携带结构化事实 `{ id, status: pass|warn|fail, detail }`，绝不修改配置/文件/产物。观测台新增 **F11「开跑预检」页签**（第 12 页，仅点击进入）：扫描会话流中最近一次 `iterate_preflight` 结果并渲染真实数据（就绪/未就绪徽章 + 阻断/警告计数 + 每项 PASS/WARN/FAIL 芯片），每个 warn/fail 行给出精确修复指令（配置 `validation.commands`、清除陈旧门禁、恢复断点）复制即用；空态区分"尚未拉取"与"已拉取为空"；`ok:false` 渲染失败信息而非误导性"就绪"摘要。**修复**：`buildCompletionSummary` 读取真实 `stoppedReason`（此前把一切未收敛运行描述为"已达最大轮数"）。测试 1319 → 1340（+21：preflight 12 + parse 6 + client 3）。上游 dsh 无新版本（最新仍 `0.2.2-alpha.2`）。
- v3.11（2026-10-28，plugin 3.11.0）：**无损报告 JSON（C 类新导出格式）+ 上游兼容追到 `0.2.2-alpha.2`**。`iterate_report` 新增 `format:"json"`，产出完整归一化运行模型（`RunReportJson`，`$schema:"iterate-run-report/1"`）——项目、目标、模式、轮次、收敛率、严重度分布、发现、修复、验证、质量门禁、经验银行、防御事件全部结构化（唯一无损格式，缺失/中断运行仍产出合法文档）；观测台 F8 报告区新增「导出 JSON 报告」按钮，与工具共用同一数据模型。上游 `dsh-v0.2.1-rc.4`（bugfix）与 `dsh-v0.2.2-alpha.2`（首个 0.2.2 alpha，含插件面破坏性变更但本插件只从 `dsh-tools` 导入 `defineTool`、从 `dsh-jobs` 导入类型，不触及被迁移接口）均声明 compatible，`dshReleases` 25 → 27，devDeps 8 个 `dsh-*` 追到 `0.2.2-alpha.2`，cordis peer 扩为 `^4.0.5-alpha.2 || ~4.0.6-alpha.1`。测试 1314 → 1319（+5）。
- v3.10（2026-10-25，plugin 3.10.0）：**双向集成场景③ TS 半边——插件写出去 iterate-kernel 契约格式**。`iterate_decision_log` 的 `add`/`list`/`read` 输出对齐 `iterate-kernel` 的 `IterationRecord` 契约（`run_id` / `round_index` / `entry_type` / `payload` 快照），新增运行时依赖 `iterate-kernel@0.1.9`，按语义化版本是一次 minor；上游 `dsh-v0.2.1-rc.3` 声明 compatible。
- v3.6（2026-10-07，plugin 3.6.0）：**上游 0.2.1-alpha.1 升级 + 15 项 UX 缺口全量实现 + ~120 项实现审查修复**（补记：该版发布时只在 §5-§9 挂了实现状态标注，未登记本表）——依赖升到 `0.2.1-alpha.1`、`dshReleases` 扩到 18 个版本；P0 零验证 fail-closed（空 `validation.commands` 中止或显式 `args.unverified`，零验证结果不再判为通过）、启动指令改走已注册指令集、磁盘快照拉取打通读侧工具回显、运行中仪表盘状态、F8/F9/F10 实渲染并接入工作流收尾（§5-§9 实现状态）；`ask.displayReason` + `presentResult` 展示契约对齐；1113 测试。
- v3.7（2026-10-13，plugin 3.7.0）：**上游 0.2.1-alpha.2 适配 + 双语 UI + 配置回读闭环 + 浏览器端渲染测试从 0 到 24**。① **上游适配**：五个 `@deepseek-ai/*` 精确锁到 `0.2.1-alpha.2`（`cordis` 保持 `4.0.5-alpha.1`），`dshReleases` 扩到 19 个版本；唯一有破坏面的变更是**可变会话工作目录**——新 `src/working-directory.ts` 特性探测 `ctx.get('workingDirectory').get(session)` 解析项目根（服务缺失/抛错/敌意 getter/非字符串结果一律回退 `header.cwd`），接入 `index.ts` / `config-loader.ts` / `session-hooks.ts` / `live.ts`。评估但不采纳：session 状态记录接口（依赖 shell 私有记录结构，跨 alpha 脆弱）、共享 `AGENTS.md`（`DSH_AGENTS_HOME`，宿主职责）、实验性 Git Worktrees 插件（与自有 `git.use_worktree` 无关）、被移除的 `both` 展示模式（本插件只用 `presentCall` 卡片）、全局安装 dsh CLI（运行时不 shell 调用）。② **双语 UI**：新增 `src/client/i18n.ts` 字典（≈290 键，`t`/`tf`，中文即键），`src/client/index.ts` 全部界面文案本地化；设置页「界面语言 / Interface language」切换并持久化 `iterate-ui-lang`（无存储选择时按 `navigator.language` 探测且**不写回**偏好，已存选择始终优先）；槽位组件模块级 `withLang` 包裹一次，切语言重绘子树不重挂载（保留分诊/展开状态）；面向模型的指令与指引**按契约保持中文**，两处展开指引挂「中文（粘贴给模型的契约文案）」标签说明原因；`lib/parse.js` 的 `stoppedReasonLabel` / `diskEmptyStateText` / `buildCompletionSummary` 增加 `lang` 参数，`CONFIG_EDIT_FIELDS` 的 label/hint 改为 `{zh,en}` 对（指引与指令构造器仍读 `.zh`）。③ **配置回读闭环**（补齐设置页只有写入指令的缺口）：`buildConfigReadInstruction()` 复制 `iterate_config {operation:"read"}` 指令，`scanSessionForConfigRead()` 反取会话中最新的生效配置（读/写结果均带 `config`，仅接受完整配置、忽略 section 切片，无 envelope 时深度扫描兜底），`configValueByPath()` 按点号键取所选字段当前值，三态区分（未回读 / 当前值 / 已回读缺字段），剪贴板被拒时展开指令兜底；新 `src/client/session-cache.ts` 用 `useSyncExternalStore` 把会话从会话域槽位（dashboard/observatory 的 effect 中发布，避免渲染期通知）传给根域设置区。④ **测试基座**：浏览器半区此前因 `react` 走注入 `require` 而零覆盖——`test/client-render.test.ts` 用 jsdom + 假 `ClientContext` 挂载全部注册槽位（引导契约、降级、看板各状态、分诊、观测台折叠→展开与 F8 快捷键、设置卡与破坏性确认、回读三态、双语），24 用例；`test/client-i18n.test.ts` 12 用例守住典契约（中文必须有英文、无死键、`{aN}` 占位符对齐、切换/持久化行为）；`tsconfig` 拆为 server / test / client 三个程序（server 保持无 DOM lib，避免服务器代码摸 `window` 失去类型告警），`npm run typecheck` 一次跑三个；`scripts/client-digest.mjs` 递归摘要 `src/client/**` + `lib/parse.js`，陈旧的 `lib/client.js` / `dist/` 直接挂测试。1216 测试全绿。
- v3.8（2026-10-17，plugin 3.8.0 后复盘）：**「UX 缺口」与「dsh 能力评估」重定义——从 bug/适配层提升到产品功能层**（本版不修改 plugin 源码，为下一轮迭代 backlog 的依据）。**术语纠偏**：此前数轮把「UX 缺口」当成实现缺陷（无锁 RMW、原型链索引、多实例焦点失效、陈旧文案、半实现列恒 0），把「dsh 能力评估」当成新契约适配（`engines.dsh` 兼容判定、五包钉版、cordis peer 对齐）——两者都不在用户可见面，用户无感知。正确定义：**UX/UI 缺口 = 用户想做的事在界面上做不到，或要绕很大的路才做到**；**dsh 能力评估 = 上游新 API 能让这个插件多做什么用户可感知的新功能**。
  - **A. 用户可见的 UX/UI 产品缺口（按价值排序）**
    1. **整个 UI 是「模型恰好回显了什么」的镜像，没有活的数据通道。** 浏览器半区无文件系统访问，面板数据全靠「模型调工具 → 回显进会话 → 客户端深度扫描会话文本」。实时活动流只有最后一次回显那么新，无轮询、无订阅、无刷新提示；用户看磁盘状态必须手动点「拉取磁盘快照」→ 复制 6 个读侧工具指令 → 粘贴 → 等回显 → 面板才更新。这是全插件最大单一产品债，11 个页签全部受它约束。
    2. **剪贴板是唯一操作通道，且损失性。** 每个动作六跳：点击→复制 JSON→切输入框→粘贴→模型理解→调工具→回显→扫描渲染。插件**未注册任何 `/iterate` 斜杠命令**（`src/index.ts` 只注册 17 工具 + 系统提示），用户没有原生触发路径。
    3. **零加载态、零进度、零超时反馈。** 全客户端无 spinner / skeleton / `aria-busy` / pending 指示。一次多轮 iterate 跑数分钟，唯一反馈是一个 2.4 秒自动消失的胶囊。F6 显示验证命令的 `exit N` 与 `通过/失败` chip，但**看不到命令输出**。
    4. **看不到 diff。** F4「修复与回滚」只显示 `+N/−N` 行数，实际 diff 在任何界面都不可见，用户回滚前无法判断改了什么（插件已有 `iterate_diff` 产出 diff 文本，只是未接到 UI）。
    5. **两个割裂的发现体验。** turn-tail 分诊面板有 y/n/a 判定但无 `suggested_fix`/`acknowledged`；F3「发现定位」有 `suggested_fix` 但不能判定、不能分诊。判定与上下文永远不在同一屏。
    6. **`n`（跳过）判定被静默丢弃。** 分诊 100 条、标 10 条跳过、导出，跳过决定消失——它只有本地 `localStorage` 标注，不进 `iterate_triage apply` 载荷，无任何下游可见效果。
    7. **无撤销，6 个破坏性动作只有 1 个做了确认。** 只有「清除分诊」是两步 arm-then-confirm；回滚修复、清除断点、清除门禁、清除事件、回滚检查点全部点一下即复制走。
    8. **隐私开关与审批策略在 UI 上不可改。** `observatory.capture`（活动是否被记录的隐私闸门）在设置页完全不可见；`observatory.approval` 在 F6 只显示不可写。
    9. **无跨会话/历史对比。** F2 页头明写「跨会话对比超出范围」。
    10. **导出只有 JSON。** 无 Markdown/HTML 报告、无 per-tab 导出、分诊判定（仅存 localStorage）完全无法导出、无分享链接/URL 编码状态、无打印样式。harness 侧已有单文件 HTML 报告（SVG 收敛曲线 + 内嵌 diff），插件侧是功能落差。
    11. **看板是只读的。** 点严重度圆点无反应；维度徽章截断到 6 个，溢出只靠 `title` tooltip 露出（键盘/读屏不可见，且隐藏维度无法从该面板操作）。
    12. **搜索/筛选不对称。** 分诊面板无轮次筛选、无「无结果」文案（F3/F7/F9/F10 都有）；F3 无轮次筛选；全插件无按文件/维度/严重度分组、无排序（除 F7 固定倒序）、无从汇总数字下钻到成员。
    13. **a11y 与本地化缺口。** ARIA 契约不完整（`role="option"` 无 `listbox` 祖先、tab 无 `aria-controls`/`tabpanel`、无 ←/→ 切 tab、容器无 `lang`、无 `aria-live` 覆盖页签切换/筛选计数、无 `aria-expanded`、无 `prefers-reduced-motion`）；英文泄漏穿过「只扫 CJK」的 i18n 检查器（`Round`/`findings`/`fixes`/`attempt`/`PASS`/`FAIL`/`PENDING`/`v3.0`/`known_intentional` 裸标识符）；批量 y/n/a 按钮是单字母、无 `aria-label`。
    14. **规模化性能。** 全插件无虚拟化（200 条发现 = 200 行全渲染）；观测台每次渲染对整段会话做 6+ 次未 memo 深度扫描，F7 每行每次渲染都 `JSON.stringify` 整段 data。
  - **B. dsh 新版本带来的用户可感知新功能机会（按价值排序）**
    1. **`ctx.sessionProjections`（`register`/`onChanged`/`snapshot`/`cachedSnapshot`/`checkpoint`/`restoreFloor`/`viewCheckpoint`/`restore`/`hydrate`，`ProjectionDefinition {key, stateSchema, init, apply, wire: {viewSchema, view}, stateVersion}`）——最高价值采纳项。** 插件可发布的、带类型的、过线上流的客户端可见状态通道，直接替换「模型回显 JSON → 客户端深扫会话」：F1-F10 与实时流变订阅式更新，**「拉取磁盘快照」这条剪贴板指令对读取路径可彻底删掉**；`stateVersion` + `checkpoint`/`restore` 另给了 dsh 原生断点语义。注：v3.7 记录中「评估但不采纳 session 状态记录接口（依赖 shell 私有记录结构，跨 alpha 脆弱）」针对的是 `appendPluginRecord`，**不适用于 projections**——后者是公开注册 API。
    2. **`ctx.fs.watch(target, changed, signal)` + `fs/observed`/`fs/write-intent`/`fs/edit-intent` 事件。** 插件跑服务器端，可直接监听 `.iterate/` 变化并推送刷新，手动拉快照摩擦消失，隐私模型不变（仍在宿主侧）。
    3. **`ctx.jobs.events`/`read`/`readAt`/`wait`/`kill`**（插件已用 `ctx.jobs` 但只用注册与 `JobOutcome`）。真实进度流：每工具耗时、后台任务状态、可取消——正好补 A3 零进度缺口。配 `ToolDefinition.timeoutMs` 与 `dsh-timeout` 的 `deadline`/`idleWatchdog` 给出可见超时。
    4. **`ctx.approval.setPolicy(agent, policy)`/`request(req)`/`'approval/policy'` 事件。** 把审批策略从 F6 只读展示变成真 UI 控件，并用 `request()` 做单动作原生确认替代 JSON 复制。注意张力：`iterate_config` 写操作至今对 `observatory.approval` fail-closed（模型不可自翻审批策略绕过人审），运行时改策略必须走 `ctx.approval` 宿主通道而非配置写。
    5. **`'session/event'`/`'session/flush'` 事件 + `Session.toolHistory()`。** 订阅替代深度扫描，同时修掉「每次渲染 6+ 次深扫」成本。
    6. **`ctx.agents.create`/`resume`/`list`/`roots`/`withInitiator` + `meta.origin:'subagent'`/`agentPreset`/`delegationDepth`。** 「指派修复」可真的派生每条发现的修复子代理，而非复制指令请模型去做；并行审查派发同理。
    7. **`tools/post-execute`（`PostToolDecision {kind:'accept'|'block', content?, additionalContexts?}`）+ `ToolOutputDefinition.presentationMeta`**（可回放、持久化进会话日志的结构化 UI 元数据）。插件工具可发出结构化元数据供客户端直读，替代正则扫回显文本——整个会话扫描架构的可靠性修复。目前只用 `tools/pre-execute`。
    8. **`ctx.sessions.list`/`fork(source, boundary?, childSessionId?)`。** 跨会话对比与「从这轮分叉一次运行」——F2 明写 deferred 的那项。
    9. **`ctx.llm.stream` + `ImageBlock`/`FileBlock`/`ReasoningBlock`/`contentHasImage`/`ModelModality`。** 看板已数「附件图片 N」但从未使用；多模态可让审查者把截图挂到具体发现上。
    10. **`'internal/update'`（cordis HMR 钩子）对应 alpha.3 的插件热重载。** 对热重载做出反应（干净重挂槽位），目前只做防御式不重复注册。
    11. **`ctx.systemPrompt.section`/`variable`/`context` + `SECTION_ORDERS` 预留的 `TOOL_GOAL`/`TOOL_SUBAGENT`/`TOOL_REPORT`/`STRUCTURED_OUTPUT`。** 以正确顺序贡献系统提示段，替代目前平铺提示。
    12. **`ctx.sandboxPolicy.resolve`/`SandboxMode` + `ctx.sandbox.confine`。** 插件执行白名单验证命令，可在设置页暴露并声明沙箱模式。
    13. 其余可用：`ctx.logger.exporter`（自定义 telemetry sink）、`ToolRunContext.deferContext`/`concludeTurn`、`ctx.tools.guard`/`presentAs`/`restrict`/`schemas`。
  - **C. 明确不可用 / 走不通（必须诚实记录，避免下轮重复投入）**
    1. **`appendPluginRecord`（`dsh-session`）不可用**——源码注释在 `:103` 明确禁止 `packages/experimental/` 之外的调用者。
    2. **`presentCall`/`presentResult` 的 `DiffCallView`/`DiffResultView`/`TerminalCallView`/`SearchMatchesResultView`/`SearchPathsResultView`/`ReadResultView`/`WebSearchResultView` 全部不可用于本插件**——`dsh-tools/README.md:95` 原文：「A tool can retain pure `presentCall()` and `presentResult()` methods for Host-local consumers. **The built-in Web Client does not consume those values.**」即**想要 UI 里的 diff / 终端卡片，必须在插件自己的 slot 组件里画**，不能指望 dsh 渲染。
    3. **`@deepseek-ai/dsh-client-connection` 未安装**——`package.json` 的 `client.inject` 声明了它但 `node_modules/@deepseek-ai/` 无此包，客户端 slot/theme 的真实契约无法从依赖检查，只能从 dsh web 客户端观察。任何新 UI 必须保持防御式降级。
    4. **cordis 不是 UI 库**——它是 DI + fiber + event + logger + service 框架，不含 slot/theme/icon/markdown/table/chart/modal/keybinding 原语。插件的 13 个 `--dsw-*` token 与整份 CSS 必须继续自己注入，不能期望上游提供图表/表格组件。
  - **D. 下一版功能批次建议优先级**：B1（projections）→ B2（fs.watch）→ B4（审批策略可写）→ A4（diff 自绘）→ A5+A6（分诊与 F3 合一 + 跳过判定可导出）。B1 与 B2 一起做可一次性删掉「拉取磁盘快照」剪贴板路径。3.8.0 本体是上游 `0.2.1-alpha.4` 升级 + `engines.dsh` 契约采纳 + 15 项实现缺陷修复（该批均属 bug/适配层，不计入本表产品功能）。
- v3.9（2026-10-18，plugin 3.9.0）：**上游 `0.2.1-rc.2` 升级 + 步骤 6 采纳 dsh 会话状态记录 API（用户可感知新能力）+ 步骤 4 落地报告导出（A10 的「报告」部分）**。
  - **上游**：五包 `@deepseek-ai/*` 精确钉 `0.2.1-rc.2`、`@deepseek-ai/cordis` 升稳定 `4.0.5`（rc.2 各包 peer 硬性 `~4.0.5`）；`dshReleases` 追加 `0.2.1-alpha.5`/`-rc.1`/`-rc.2`（24 个，两份 README 同步）；`engines.dsh` 不变。`dsh-tools`/`dsh-jobs`/`dsh-util-values` 的 d.ts 在 alpha.4→rc.2 间**插件所用 API 无变化**；新增 `@deepseek-ai/dsh-session` optional peer。
  - **步骤 6 采纳（新能力 → 新功能）**：`appendPluginRecord` / `pluginRecordOf`（`@deepseek-ai/dsh-session`，`0.2.1-rc.1` 起公开导出）→ **会话绑定运行记录**：`iterate_transcript capture` 追加 `plugin:iterate/run` 并回传 `sessionRecord`；新增 `recall` 列出本会话运行记录；`read` 在 `.iterate/transcript.json` 丢失/损坏时从会话记录**恢复摘要 manifest**（`recovered:true`）。fail-safe 设计（懒动态 `import()` / 结构类型 / 宿主无该 API 时 `supported:false` 降级，best-effort 写失败绝不使 capture 失败）。
  - **修正 C1**：`appendPluginRecord` 在 rc.1+ 已公开可用，旧「`:103` 禁止非 experimental 调用者」结论不再适用 → 从 C 段移除，改为诚实采纳项。
  - **步骤 4 落地**：A10「导出只有 JSON」的「报告」部分 → `iterate_report` 工具（`format:"markdown"` 可粘贴进 PR / `format:"sarif"` SARIF 2.1.0 供 CI / Code Scanning；`write:true` 落盘 `.iterate/report.md|.sarif`；`lang` zh/en）+ 观测台「导出报告 / 导出 SARIF」按钮，二者**共用同一份无依赖渲染器 `src/report-render.ts`**（server 工具与 client bundle 不可能漂移；该模块不 import 任何模块，避免把 `src/` 之外文件拉进 tsc 程序致 emit 散成 `dist/src/**`，并与 `lib/client.js` 一起纳入 digest）。
  - **本轮明确不实现（原因见 `RELEASE.md` 3.9.0 记录；进 backlog，不做占位降级）**：A1/A2 + B1/B2（`ctx.sessionProjections` + `ctx.fs.watch` 替换「模型回显 + 会话深扫 + 剪贴板拉快照」——替换客户端架构的最大改动，且客户端 slot/theme 真实契约无法从依赖检查，本轮无法在无宿主验证下完成）；A3 + B3（进度流）；A4（diff 自绘）；A5+A6（分诊与 F3 合一 + 跳过判定可导出）；A7（撤销/确认覆盖）；A8 + B4（审批策略可写）；A9 + B8（跨会话对比）；A11–A14。
  - **C 段更新**：C1 移除（见上），C2（`presentCall`/`presentResult` 的 diff/终端卡片宿主 Web 客户端不消费，需自绘）/ C3（`dsh-client-connection` 未安装）/ C4（cordis 非 UI 库）保持。
  - **D 下一轮优先级（不变）**：B1 → B2 → B4 → A4 → A5+A6；建议 B1+B2 同批以一次性删掉「拉取磁盘快照」剪贴板路径。
  - **3.9.1 补记（同日，步骤 3 全量实现审查）**：审查发现 11 项缺陷，全部修复并补回归测试——①跨进程 transcript 锁对 async 回调「零持有」（`withProjectLock` 同步实现 + `nudge` 传 async 回调，`finally` 在首个 `await` 即释放）→ `withProjectLock` 增 promise 重载，持有到回调 settle；②`nudge`/回滚重持久化静默清空顶层 `findings`、`phases`、`round` → `rehydrateBuilder` 补 `restoreFindings` / 回放 `phases` / `advanceRound`，并跳过 `null` round/thread 行（原先会整份 manifest 回退）；③新建锁在「创建→写 pid」窗口为空戳，`Number('')===0` 被当作死锁而窃取活锁 → 仅可解析的正整数 pid 才可判死；④`runGit` 遇 `execFile` 同步抛错（参数含 NUL）→ 改为结构化失败而非 reject；⑤SARIF `executionSuccessful` 不再把未知（`null`）退出码计为失败；⑥Markdown 报告第 1 行位置丢失、小数行号产出非法 SARIF `startLine` → 取整并向 SARIF 对齐；⑦缺/空 transcript 不再渲染为「运行中」；⑧会话记录版本门禁改为整数精确比较（拒绝未来 `1.9`）；⑨会话 API 导入失败不再永久缓存（下次重试）；⑩`qualityStatus` 真正从当前质量门禁写入记录。测试 1262 → 1280。
  - **3.9.2 补记（同日，步骤 3「无锁读改写」扫尾）**：修复最后一处未加锁的读改写——`markFixRolledBackInTranscript` 回滚时重读/重水化/重写 `transcript.json` 全程无锁，两个并发回滚各自读到同一基线，后写者静默丢弃前者的回滚标记（与 3.9.1 修掉的 `nudge` 同类丢更新）→ 改走共享 `transcript` 锁并跨 `await` 持有。经全量扫描后**有意保持无锁**的仅 `appendLive` 的字节封顶活动流：纯追加、可自愈的派生投影，逐事件跨进程加锁会在工具调用热路径上引入最长 1s 等待（该取舍记录于此处与 3.9.2 CHANGELOG）。测试 1280 → 1281。
- v1.0-v2.12.3：v2 系列设计随主仓库插件迭代（README/CHANGELOG 逐版本记录，本文档自 v3.0 起独立承载设计演进）。
- v3.0（2026-09-02）：**大版本方向：质量指挥中心 + 经验银行（本文档首版）**——v2 功能趋于做尽，确立 v3.0 升级方向。核心决策：① 定位从"被动观察面板"升级为"主动指挥中心 + 知识库"（§4）；② 新增质量门禁视图（§5）与经验银行（§6，方向 1 在 UI 的落地）；③ 新增防御事件流（§7）与 task_mode 指示灯（§10），与 harness 2.0 防御式内核 / skill 3.0 guard-invariant 打通；④ 指挥操作原生按钮化（§8），底层仍走 iterate 主工作流，不绕过审查/审批/日志；⑤ 跨会话趋势从质量账本读取（§9）。**本版为纯设计细化，不修改 plugin 源文件**。头部状态行更新至 v3.0。
- v3.1（2026-09-06）：**v3.0 设计落地（plugin 3.3.0）**——F8/F9/F10 从复制指令占位升级为**会话流数据实渲染**：新增 `lib/parse.js` 的 `scanSessionForQualityGate` / `scanSessionForExperienceBank` / `scanSessionForDefenseEvents`（反向时序、代理安全、深度/环保护），`get/add` 单条折叠为列表、`record/counts` 折入计数+事件流；§8 新增「指派修复」按钮（按批量作用域复制 `iterate_fix` 指令，携带 file/line/dimension/severity/summary）。task_mode 通道修正：harness status 推送只达 harness 自有前端、不通 dsh 插件，故改由插件服务器端透传——`iterate_transcript capture` 接受显式 `taskMode`，builder 持久化（review-loop 缺省 derive `iterate`），`rehydrateBuilder` 透传，`iterate_status` 经 `readTranscriptTaskMode` 读取持久化 transcript 输出并渲染；客户端 chip 由 `normalizeTranscript` 的 taskMode 透传点亮。
- v3.2（2026-09-06，plugin 3.4.0）：**综合审查与硬化批次**——① `iterate_checkpoint` 新增 `resume` 操作（加载断点 + 累加 resumeCount 原子写回），修复观测台 F5 复制出工具不支持的 `operation:"resume"` 的死指令；② `iterate_status` 补全类型中早已声明却从未填充的 `qualityGate`/`experienceBank`/`defenseEvents` 三个快照输出（质量指挥中心一屏到位）；③ 安全硬化：`applyConfigUpdates` 增加原型污染防护（对齐 `mergeConfig`），`iterate_config` 写操作对 `observatory.approval` fail-closed（模型不可经配置写自翻审批策略绕过人审门禁）；④ 防御/质量存储读取规范化（`readDefenseEvents` 重算 counts 杜绝 NaN、`readQualityGate` 归一 dimensions/数字字段防 render 崩溃）；⑤ `buildReviewReport` 轮次排序修复无序 rounds 的收敛误判；`collectScopeFiles` 改用 `path.relative` 修复 Windows 绝对路径泄漏；⑥ UX：空态 dashboard 新增「完整迭代 / 仅评审」一键复制启动按钮。
- v3.3（2026-09-07，plugin 3.4.1）：**DSH STORE 契约对齐**——回应 AI-Scarlett/DSH-Store#504 自动复检的阻断项：`dsh.compatibility.dshReleases` 精确声明扩到 `0.1.1-rc.1` / `0.1.2-alpha.4/5` / `0.1.2-rc.1` / `0.1.3-alpha.1`（覆盖商店当前最新三窗口，`0.1.1-rc.1` 附带真实一次性 Profile 证据，`0.1.3-alpha.1` 为源码声明）；README 权限披露修正 `commands` 描述（`iterate_validate` 确实经 `node:child_process` 执行配置白名单命令、`git diff` 仅 changed-only 范围使用）；在临时 `$DSH_HOME` 下一键 Profile 实测 install（449ms）/ compose（`--dump-config` 含 iterate-plugin bundle）/ uninstall（602ms）并如实记录证据；start/rollback 因一次性 Profile 无模型提供方保持 `unknown`/`partial`。剩余固定门禁失败（files/commands/credentials 权限信号、运行依赖需独立供应链审查）为该插件固有（真实读写文件、执行受限白名单命令、依赖 `@deepseek-ai/*` 运行包），按商店契约保持 `user-reviewed`/守卫状态，属预期而非可经 manifest 修复。
- v3.4（2026-09-12，plugin 3.5.1）：**上游兼容窗口扩展 + 审查闭环补齐**——① 上游 deepseek-harness 发布 `dsh-v0.1.5-rc.1`（0.1.5 破坏性变更经一次性 Profile 实测不影响插件：`ctx.agent` 移除插件未用、Inbox 仅类型化、Session V3、Web slot 命名未变），`dsh.compatibility.dshReleases` 兼容声明扩到 `0.1.5-alpha.1` / `0.1.5-alpha.2` / `0.1.5-rc.1`（真实一次性 Profile 证据：0.1.5-rc.1 包下 typecheck + 全量测试绿）；构建期依赖维持 `0.1.2-rc.1` 精确锁版（0.1.5 pins 干净 install 会 ERESOLVE，harness 安装期去重）；② 审查缺口 G1-G5 补齐——`iterate_experience` 新增 `remove`、`iterate_quality_gate` 新增 `clear`（陈旧 FAIL 证书/错误经验可清理）、`iterate_rollback` 经失败安全的 `markFixRolledBackInTranscript` 把回滚镜像进持久化 transcript（F4 不再把已回滚修复显示为成功）、`iterate_status` 文本渲染补全 JSON 已含的质量门禁/经验/防御事件摘要、活动流 classifyTool 覆盖三个 v3.0 指挥中心工具。
- v3.5（2026-09-16，plugin 3.5.3）：**全量实现审查 + 运行时重置操作闭环 + 防御性硬化**——① 逐实现审查修复（堵 OOM / 崩溃 / NaN / 静默吞错）：transcript builder `roundStart`/`snapshotConvergence` 对模型可控 round 数预分配数组加 `MAX_ROUNDS` 上限（此前 1e9 级 round 可 OOM 宿主）、`fix()`/`decision()` 拒绝 NaN round；tools/transcript `captureRound`/`normalizeCheckpoint`/`normalizeFix` 的 `<= 0` 守卫改用 `Number.isFinite`（NaN 穿过旧守卫会坍缩进 round 1）；`nudge`/`capture` 的 `persist` 改为结构化错误通道（磁盘失败返回 `{ok:false}` 而非抛异常），`nudge` 对解析成功但形状损坏的 manifest（`rounds:[null]`）降级为全新 builder；`readDefenseEvents`/`readExperienceBank`/`readRegistry` 三个 store 对手工编辑文件做逐条形状归一（timestamp/severity 字符串化、files/tags 数组化、hitCount/记录计数有限化），杜绝 render `.join`/search spread/sort `localeCompare` 崩溃与 NaN 求和；`computeStatus`/`summarizeFixRegistry`/`iterate_diff` 计数强转防 NaN；`iterate_config` 写操作在无配置文件的新项目上改以内置默认值为合并基（部分更新 `{max_rounds:5}` 不再报“缺 goal”）；`validateCheckpoint` 强制 `round ≤ maxRounds` + `readCheckpoint` 归一数字字段 + findings 载荷上限；`iterate_prune` 的 `readdirSync` 加守卫（`.iterate/fixes` 为文件时不再抛）；质量门禁对空审查（无维度/无 findings/无验证）返回 `pending` 而非伪造 FAIL；list `language` 对非 zh/en 配置回退 en。② 运行时重置操作闭环（UX 缺口）：`iterate_defense_events` 新增 `clear`（清 `.iterate/defense-events.json`，与 checkpoint/quality_gate clear 对齐）；观测台 F5「清除断点」、F8「清除门禁」、F10「清除事件」三个复制指令按钮补齐；设置页状态指引补记三个 reset 操作。③ 配套：`dist/` 重建与 src 严格一致、CHANGELOG 3.5.3 记录、576 测试全绿、typecheck + typecheck:client + build + build:client 干净。上游 dsh 停在 `0.1.5-rc.2`（插件已在 3.5.2 升级并声明兼容），本次无新增依赖变更。
