# TASK-plugin-daily.md — iterate-plugin 每日迭代任务提示词（v2，2026-10-17 修订）

> 用途：`iterate-plugin` 每日定时任务的提示词。**v2 相对 v1 的唯一实质改动**：把「步骤4 UX 缺口清单」与「步骤6 dsh 能力评估」从 bug/适配层重定义为**产品功能层**。发版机制、验证命令、工作区纪律等其余部分原样保留。
>
> v1 的问题：连续多轮把「UX 缺口」做成实现缺陷（无锁 RMW、原型链索引、多实例焦点失效、陈旧文案、半实现列恒 0），把「dsh 能力评估」做成新契约适配（`engines.dsh` 兼容判定、五包钉版、cordis peer 对齐）。这些修复有价值，但**都不在用户可见面，用户无感知**，不是本任务要的「UX 功能缺口」与「dsh 新功能」。

---

## 任务提示词（以下为可直接粘贴到定时任务 Prompt 字段的正文）

```
审查并迭代本机 /Volumes/Eng-Dev/iterate-skill/harness/iterate-plugin（dsh 插件）。
忽略 skill 本体与 iterate-harness 引擎。按 8 步顺序执行，全程无人值守：

【步骤 1】查上游 dsh 更新。
  gh api 或公开 GitHub API 取 deepseek-ai/deepseek-harness 的 releases 与 tags，
  找出当前 package.json 中 dsh.compatibility.dshReleases 声明之外的新发布。
  ★ 对每个新发布，必须拉官方 release notes 全文再判断 ★
    gh release view <tag> --repo deepseek-ai/deepseek-harness --json body
    （或 /releases/tags/<tag> 的 .body），禁止只凭版本号 / 本插件 CHANGELOG 下结论。
    从正文逐条筛出【插件面能力】（新能力 + breaking 迁移），而不是扫一眼就判「无新能力」。

【步骤 2】升级并适配 dsh。
  五包 @deepseek-ai/* 精确钉版到目标版本；cordis 按目标版本 peer 硬性要求同步
  （不满足会 ERESOLVE）。dshReleases 逐条追加声明，两份 README 同步镜像。

【步骤 3】全面审查并修复实现缺陷。
  无锁读改写、崩溃点、NaN/OOM、静默吞错、半实现、安全边界（路径穿越、原型污染、
  symlink 出界）、锁 TOCTOU、跨进程一致性。

【步骤 4】★ UX/UI 功能缺口清单 —— 产品层，不是 bug 层 ★
  定义：用户想做的某件事，在界面上做不到，或要绕很大的路才做到。
  必须回答「用户能少做哪一步 / 多看到什么 / 少切几次屏 / 少复制几次」。

  必须产出（按价值排序，每条写明：用户当下的实际动作序列 → 缺口 → 影响面）：
    - 数据新鲜度：面板数据是否有活通道？还是依赖模型回显 + 剪贴板手动拉取？
    - 操作通道：动作是否需要「复制 JSON → 切输入框 → 粘贴 → 等回显」六跳？
      有没有原生触发路径（斜杠命令、单动作原生确认）？
    - 反馈完整性：加载态 / 进度 / 超时 / 命令输出可见性。
    - 决策可见性：用户能否看到 diff、命令输出、改动前后？
    - 界面割裂：同一个概念是否在多个不互通的界面出现？判定与上下文能否同屏？
    - 决策丢失：用户在 UI 上做出的决定，哪些静默丢弃、无下游效果？
    - 破坏性操作：确认覆盖度、撤销能力。
    - 控制面：哪些开关/策略用户想改但 UI 不可写（隐私开关、审批策略）？
    - 历史与对比：跨会话、跨轮次、时间序列对比能否做？
    - 导出与分享：除 JSON 外有无报告、分诊判定导出、分享链接？
    - 检索：筛选维度、排序、分组、下钻、无结果态是否齐备且对称？
    - 无障碍与本地化：ARIA 契约完整性、lang、reduced-motion、i18n 泄漏。
    - 规模化：大列表渲染、扫描成本、memo。

  ★ 明确不算 UX 功能缺口（不要写进清单，不要作为本步交付）★
    - bug 修复：崩溃、类型错误、竞态、锁、NaN、OOM、静默吞错 → 属步骤 3。
    - 文案错别字、标点、术语不一致 → 不算。
    - 「某列显示为 0」这类半实现接线 → 属步骤 3（除非它导致用户做出错误决策）。
    - 内部重构、命名、注释、代码风格 → 不算。
    - 若某项确实只有工程价值而无用户可见差异，写明「不计入 UX 缺口」。

【步骤 5】完整实现步骤 4 的缺口。
  每条必须真实可交付：完整实现，禁止占位 / 模拟 / 半截 / TODO / 桩函数 /
  假数据；配套单元测试 + 文档同步。若某条本迭代实现成本过高，必须明确写出
  「本轮不实现，原因是 X」并进入 DESIGN-iterate-plugin.md 的 backlog，
  不允许静默降级为占位。

【步骤 6】★ dsh 新能力评估 —— 新功能层，不是适配层 ★
  定义：上游新 API 能让这个插件多做什么用户可感知的新功能。
  ★ 硬性前置：先拉官方 changelog / release notes 全文，逐条列出插件面能力 ★
    用 gh release view <tag> --repo deepseek-ai/deepseek-harness --json body 取正文，
    把「开发者 / 插件 / SDK / 设置图标 / Session API / 工具启用 / 迁移 / breaking」等
    条目全部抽出，逐条给三态判定：
      - 【可转化】新 API 能解锁本插件用户场景 → 列入本轮实现或 DESIGN backlog（写明原因）。
      - 【不可转化】必须给出具体理由（宿主级无插件面 / 域不相关 / 实验性自足插件），
        不得只写「无新能力」。
      - 【breaking 需核验】必须先 grep 本插件是否使用该 API（tools.resolve/executable、
        agent.model / agent/request、sessionProjections、tools.mode / PTC、run_code、
        appendPluginRecord 等），确认不踩坑再声明 compatible；严禁未核验就笼统
        「确认不受影响」。
    未转化的【可转化】能力必须进 DESIGN-iterate-plugin.md backlog，下一轮优先。
  必须逐条给出：新 API 签名 → 它能解锁哪个具体用户场景 → 现状的绕行代价。

  评估面（按已探明的实际能力）：
    - ctx.sessionProjections（register/onChanged/snapshot/checkpoint/restore/
      stateVersion）——能否用推送式类型化状态通道替换「模型回显 + 会话深扫」？
    - ctx.fs.watch + fs/observed / fs/write-intent / fs/edit-intent
    - ctx.jobs.events / read / readAt / wait / kill（进度流与可取消）
    - ctx.approval.setPolicy / request + 'approval/policy'
    - 'session/event' / 'session/flush' + Session.toolHistory()
    - ctx.agents.create / resume / list / roots / withInitiator（子代理派发）
    - tools/post-execute + ToolOutputDefinition.presentationMeta
    - ctx.sessions.list / fork（跨会话对比）
    - ctx.llm.stream + ImageBlock / FileBlock（多模态）
    - 'internal/update'（HMR）、ctx.systemPrompt.section、ctx.sandboxPolicy、
      ctx.logger.exporter

  ★ 必须同时记录「明确不可用 / 走不通」，避免下轮重复投入 ★
    - appendPluginRecord 被 :103 注释禁止非 experimental 调用者使用。
    - presentCall/presentResult 的 DiffCallView / DiffResultView /
      TerminalCallView / SearchResultView / ReadResultView / WebResultView
      ——dsh-tools/README.md:95 明写「The built-in Web Client does not consume
      those values」，即想要 UI 里的 diff/终端卡片必须在插件自己的 slot 组件里画。
    - @deepseek-ai/dsh-client-connection 声明于 client.inject 但未安装，客户端
      slot/theme 真实契约无法从依赖检查，新 UI 必须保持防御式降级。
    - cordis 不是 UI 库（DI + fiber + event + logger + service），不含
      slot/theme/icon/markdown/table/chart/modal 原语，图表表格必须自绘。

【步骤 7】自查。
  重读本轮所有改动，确认无空壳、无桩、无假实现、无资源泄漏、文档与代码同步。

【步骤 8】按 RELEASE.md 项目3 清单发版。
  (a) 只改 plugin 的 package.json + package-lock.json version（独立版本线）；
  (b) 本地 npm run typecheck && npm test 必须全绿；
  (c) commit + push 主仓库 main；
  (d) subtree split 到 jingzhao-l/iterate-plugin，non-fast-forward 时改用
      .release/iterate-plugin 工作区；
  (e) .release/iterate-plugin 里 git pull 后 npm publish；
  (f) 验证 npm latest。
  涉及变更的 .gitignore 屏蔽的设计文档也要照常上传。
```

---

## 环境约束（粘贴时一并保留）

- 每条终端命令前先执行：
  `export PATH="/opt/homebrew/bin:/opt/miniconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"`
  否则 git / node / npm 报 command not found。
- 勿用强传染许可（GPL / AGPL / SSPL）依赖。
- **绝不触碰或提交工作区里其他会话的 WIP**：`kernel/`、`harness/iterate-harness/`、
  `.githooks/pre-push` 等已 modified 的文件保持原状，只 `git add` 插件目录的具体文件。
  若 `.git/hooks/pre-commit`（删除文件守门）因其他 lane 的未暂存缺失文件拒绝提交，
  先确认本次暂存集 `git diff --cached --diff-filter=D` 为 0，再用 `ALLOW_DELETIONS`
  逐一命名声明排除；**不要恢复他人的改动，也不要暂存它们**。
- 独立仓 `.github/` 必须保留：自带 OIDC 发布 workflow `npm-publish.yml`，
  rsync 必须 `--exclude .github`（曾被 `--delete` 误删）。
- 独立仓有意跟踪 `node_modules`（供 `git clone` 安装）。dsh 升级版本历史先例
  同步提交 node_modules（v3.6.0 nm=1538、v3.7.0 nm=1396），故 `npm ci` 后的
  依赖变更应一并提交；非升级版本不要动它。
- 改完 `src/` 或 `lib/` 后**必须** `npm run build && npm run build:client`：
  `test/package-contract.test.ts` 强制 `dist/` 与 `src/` 齐步、`lib/client.js`
  digest 匹配 `src/client/index.ts` + `lib/parse.js`。
- 发布前在 `.release/iterate-plugin` 里重跑一遍 `npm run typecheck && npm test`
  （全新依赖安装可能暴露 lockfile 与实际安装的不匹配）。

## 背景与依据

- 当前 UX/UI 产品缺口与 dsh 新功能机会的完整清单：
  `DESIGN-iterate-plugin.md` §14 **v3.8** 条目（A 段 14 项 UX/UI 缺口、
  B 段 13 项 dsh 能力→功能机会、C 段 4 项明确不可用、D 段优先级建议）。
- 下一轮建议优先级：**B1（`ctx.sessionProjections`）→ B2（`ctx.fs.watch`）
  → B4（审批策略可写）→ A4（diff 自绘）→ A5+A6（分诊与 F3 合一 + 跳过判定可导出）**。
  B1 与 B2 一起做可一次性删掉「拉取磁盘快照」这条剪贴板路径。
- 每次迭代的结论必须回写 `DESIGN-iterate-plugin.md` §14（新增版本条目）
  与 `harness/iterate-plugin/CHANGELOG.md`，并在 `RELEASE.md` 记发布记录。
