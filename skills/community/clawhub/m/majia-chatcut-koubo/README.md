# ChatCut口播 · 马甲实战版

![Skill Version](https://img.shields.io/badge/skill-v1.7.0-blue)
[![skills.sh](https://skills.sh/b/maojiebc/majia-chatcut-koubo)](https://skills.sh/maojiebc/majia-chatcut-koubo)

**ChatCut口播 · 马甲实战版｜一句话稳剪与可恢复主流程**

> 给普通创作者的一句话入口：先安全清理口播、做代表样片，确认后再扩展整片，最后交回可继续编辑的 ChatCut 时间线。

![v1.7.0 一句话稳剪流程](https://raw.githubusercontent.com/maojiebc/majia-chatcut-koubo/main/04-项目设计与路线图/系统架构.png)

## 30 秒开始

安装后，在支持 Skill 的助手里说：

```text
$majia-chatcut-koubo 用马甲稳剪当前口播
```

它会先自动读取当前项目、时间线和素材；只有无法唯一确定时才问一个聚焦问题。随后完成低风险口误清理与代表样片。你确认样片后，它才会把相同策略扩展到整片，并依次处理声音衔接、基础字幕和验证。

默认结果是一个可继续手调的 ChatCut 时间线，不是自动发布的视频文件。

本地开发者也可以查看入口。以下命令面向 GitHub 源码 clone；SkillHub 的轻量分发包会省略测试、fixture 和纯 CI validator，完整验证仍以同一提交的源码仓与 CI 为准：

```bash
npm ci
npm run doctor
npm run koubo -- --help
npm run smoke:one-click:fake
```

## v1.7 环境与文字保护

当前版本先分清 Hosted/Web 与 Desktop，使用对应官方指令；会话未知、过期或缺能力时先补齐。只改字幕或只修识别错误会关闭默认口播清理；实际原声替换需要精确授权，模糊的文字请求先澄清。

开发者可用 `npm run preflight -- --session <current-session.json> --json` 检查当前会话合同，用 `npm run check:official -- --checkout <official-checkout>` 对照官方版本、Skill 清单与已审查内容。两个检查都不能证明真实剪辑效果。详见 [环境与文字修改](workflows/session-and-text-safety.md) 和 [本轮官方来源与设计](https://github.com/maojiebc/majia-chatcut-koubo/blob/main/04-%E9%A1%B9%E7%9B%AE%E8%AE%BE%E8%AE%A1%E4%B8%8E%E8%B7%AF%E7%BA%BF%E5%9B%BE/2026-09-30%E5%AE%98%E6%96%B9%E6%9B%B4%E6%96%B0%E4%B8%8Ev1.7%E8%AE%BE%E8%AE%A1.md)。

## 默认会做什么

- 识别“稳剪、快剪、专业增强、继续上次、只审核”等自然语言意图。
- 选择四套可复现默认方案之一，并记录本次选择。
- 保护数字、专名、否定、论证链和用户已经确认的设计。
- 只自动处理有证据的低风险项；中风险进入样片，高风险必须由你决定。
- 按片长选择开头、复杂切点、重说、停顿、隐私和片尾代表窗口。
- 样片确认后，按“小批写入 → 回读 → 检查点”的方式继续。
- 先锁定 A-roll，再做声音平滑与整片字幕。
- 分开报告结构、画面、音频测量、人耳试听、隐私和用户确认状态。

## 默认不会做什么

- 不自动重排观点或把钩子搬到前面。
- 不自动删除整句、数字、专名、否定附近内容。
- 不自动添加音乐、动态图形、补充画面或生成素材。
- 不覆盖用户手工修改；时间线变化会让旧样片确认失效。
- 不把“工具返回成功”写成“画面和声音已经通过”。
- 不自动导出，更不会自动发布用户视频。

## 三种模式，四套默认方案

| 你怎么说 | 默认方案 | 适合 | 关键边界 |
| --- | --- | --- | --- |
| “用马甲稳剪” | `balanced-stable` | 日常单人口播 | 保持原顺序，节奏自然 |
| “快剪这条短口播” | `tight-short` | 30–90 秒短片 | 更紧，但钩子和重排仍需确认 |
| “做专业增强” | 按素材选择 | 长片或录屏 | 高级画面只给候选，不擅自执行 |
| 长片信任表达 | `trust-longform` | 5–30 分钟 | 保护案例、数字和论证链 |
| 录屏演示 | `screen-demo` | 屏幕 + 人物 | 屏幕证据优先，隐私必须验证 |

四套方案的机器合同位于 [`profiles/`](profiles/)。个人方案只能保持或收紧安全边界，不能放宽高风险审批。

## 你会看到的主流程

```text
一句话需求
→ 项目与素材检查
→ 转写与低/中/高风险决定
→ 代表样片
→ 你确认或要求调整
→ 整片 A-roll
→ 声音平滑与字幕
→ 分项验证
→ 可编辑时间线 + 交付报告
```

典型样片确认卡只说人话：

```text
代表样片已做好
已处理：明显口误、失败重说、批准范围内的长停顿
已保护：数字、专名、否定和需要你决定的内容点
未执行：重排、音乐、动态图形、补充画面、导出
请选择：继续整片 / 再自然一点 / 再紧一点 / 查看高风险项
```

## 中断后怎么继续

每次运行都有独立清单、决定记录和检查点。恢复前会先比较项目与时间线版本：

- 写入前超时：回读确认没写，再安全重试。
- 写入后超时：回读确认已经写入，不重复创建。
- 部分写入：补偿或停在最近检查点，等待核对。
- 用户手工修改：停止覆盖，旧审批标记为 `STALE`。
- 同一失败连续三次：止损并交接，不无限重试。

开发者命令：

```bash
npm run run -- --intent "用马甲稳剪当前口播" --dry-run --json
npm run status -- --run-id <run-id>
npm run review -- --run-id <run-id>
npm run approve-decisions -- --run-id <run-id> --decision-id <decision-id>
npm run approve-sample -- --run-id <run-id>
npm run request-revision -- --run-id <run-id> --direction natural
npm run resume -- --run-id <run-id> --timeline-revision <fresh-revision> \
  --reconcile-outcome <blocker-specific-outcome> \
  --evidence-ref <logical:readback-evidence> [--checkpoint-id <checkpoint-id>]
npm run report -- --run-id <run-id>
```

`resume` 不会用清单里的旧版本号自证安全：必须先从 ChatCut 重新回读时间线版本；处于阻断状态时，还必须提交与阻断原因匹配的对账结果和证据。写入类阻断需要最近的已落盘检查点。

`doctor` 在源码 clone 中会运行匿名运行时 fixture 审计；在注册表轻量包中会明确返回 `verificationScope=distribution-package` 与 `runtimeContracts.status=not_packaged`，不会伪造一次本地全量测试。

项目运行记录默认放在项目内 `.majia-koubo/`，已被 Git 忽略，不会进入公开包。

## 完成状态不是一个总勾

交付报告分别使用以下状态：

- `PASS`：有对应证据并通过。
- `FAIL`：有证据且未通过。
- `UNVERIFIED`：当前没有足够证据。
- `STALE`：证据对应的时间线或方案已经变化。
- `WAIVED`：用户明确豁免。
- `NOT_APPLICABLE`：本次不适用。

结构回读只能证明结构；合成帧才能证明画面；音频测量不能替代人耳试听；样片确认也不能替代最终播放确认。

## 当前验证边界

| 能力 | v1.7.0 状态 |
| --- | --- |
| 运行合同、四套方案、风险规则、状态转换 | `PASS`（离线自动检查） |
| 超时前/后、部分写入、手工修改保护 | `PASS`（带结构化模拟证据的匿名会话） |
| 一句话路由与本地命令 | `PASS`（离线自动检查） |
| 真实 ChatCut 工具面与项目写入 | `UNVERIFIED` |
| 真实合成画面、人耳试听、匿名生产样本 | `UNVERIFIED` |

本仓库当前没有可用的真实 ChatCut 会话和匿名媒体，因此 [`reports/live-canary-v1.7.0.json`](reports/live-canary-v1.7.0.json) 如实记录为 `stableClaimEligible=false`。离线模拟不能替代真实端到端证据；在至少 5 条真实匿名样本、三种长度、三种内容形态和恢复/手改保护全部通过前，本项目不会把“一键稳定剪辑已经生产验证”写成事实。

## 与 ChatCut 官方能力怎么分工

ChatCut 当前官方 Skills 负责项目操作、素材导入、转写、口播基础方法、验证、音乐、动效、生成、导出和产品帮助。本包不复制它们的参数教程，只负责：

- 把一句话需求拆成可恢复的阶段；
- 给出安全默认、风险边界和样片策略；
- 保护用户已经确认的内容与设计；
- 把不同证据分开记录并形成交付报告。

完整分工见 [`workflows/official-skill-map.md`](workflows/official-skill-map.md)。官方工具名称和参数始终以当前 ChatCut 工具说明为准。

## 安装

```bash
# GitHub CLI
gh skill install maojiebc/majia-chatcut-koubo

# skills.sh
npx skills add maojiebc/majia-chatcut-koubo

# ClawHub
npx clawhub install majia-chatcut-koubo
```

安装标识始终是 `majia-chatcut-koubo`，展示名是“ChatCut口播 · 马甲实战版”。

## 开发与发布检查

要求 Node 24.18.0：

```bash
npm ci
npm run verify
npm audit --audit-level=high
```

分层检查：

```bash
npm run validate:runtime-contracts
npm run test:orchestration
npm run test:risk-policy
npm run test:run-state
npm run test:starter-prompts
npm run test:cli
npm run smoke:one-click:fake
npm run validate:docs-routing
npm run validate:live-claim
```

旧能力仍保留：Rule Registry、Creator OS IR、SRT 文本桥、七执行状态、预览审批、可恢复写入、媒体检查、外挂知识包与视觉候选治理。它们是高级底座，不再占据普通用户首屏。发布态字幕检查仍需显式配置根目录：

```bash
node scripts/validate-caption-pages.mjs \
  --strict \
  --profile <profile.source.json> \
  --root <profile-config-root> \
  --input <captions.json>
```

工程顺序和真实验证闸见[公开路线图](04-项目设计与路线图/公开路线图.md)，历史升级约束见 [V1.3.1 迁移指南](https://github.com/maojiebc/majia-chatcut-koubo/blob/main/04-%E9%A1%B9%E7%9B%AE%E8%AE%BE%E8%AE%A1%E4%B8%8E%E8%B7%AF%E7%BA%BF%E5%9B%BE/V1.3.1%E8%BF%81%E7%A7%BB%E6%8C%87%E5%8D%97.md)。

## 维护入口

| 你要做的事 | 入口 |
| --- | --- |
| 第一次维护，不知道改哪里 | [01-从这里开始](01-从这里开始/README.md) |
| 查字幕、转场、双画面和人脸取景 | [02-剪辑方法手册](02-剪辑方法手册/README.md) |
| 记录真实任务的新坑 | [03-实操迭代与踩坑](03-实操迭代与踩坑/README.md) |
| 看架构、路线图和迁移说明 | [04-项目设计与路线图](04-项目设计与路线图/README.md) |

目录职责：

```text
agents/       安装后的默认一句话入口
workflows/    稳剪、快剪、专业增强、恢复和官方分工
profiles/     四套可复现默认方案
schemas/      数据合同
templates/    匿名示例与交付模板
src/          路由、状态、风险、检查点和命令
scripts/      自动检查与离线冒烟
fixtures/     匿名正反例和故障场景
reports/      脱敏真实验证状态
```

本地个人词表、项目路径和真实业务内容只放本机配置，不进入公开仓。完整维护地图见 [`01-从这里开始/README.md`](01-从这里开始/README.md)。

## 版本记录

**V1.7.0（2026-09-30）** — 环境准入、Hosted/Desktop 分流、字幕/转写/剪切/原声替换目标保护、官方来源快照与漂移检查、按当前版本选择真实 canary、间接依赖安全修复；真实端到端仍为 `UNVERIFIED`。

**V1.6.0（2026-08-11）** — 新增一句话入口、三种模式、四套默认方案、`run/status/review/approve-decisions/approve-sample/request-revision/resume/report` 主流程、运行清单、决定记录、检查点、六维样片指纹、恢复协议和证据分离交付报告；新增 11 个匿名故障场景与真实验证声明门禁。真实 ChatCut 端到端仍为 `UNVERIFIED`。

**V1.5.0（2026-07-25）** — 新增受治理的可选知识与镜头候选层；外部资源只能扩大候选，不能覆盖内容真相、隐私、审批或证据规则。


完整历史见 [CHANGELOG.md](CHANGELOG.md) 或 [GitHub Releases](https://github.com/maojiebc/majia-chatcut-koubo/releases)。

## 作者 / 联系

**马甲（@maojiebc）** · 超级马甲

如果这份 Skill 帮到你，欢迎交流踩坑、提需求或报问题：

| 渠道 | 链接 |
| --- | --- |
| Email | [m9224@163.com](mailto:m9224@163.com) |
| GitHub | [github.com/maojiebc](https://github.com/maojiebc) |
| ClawHub | [clawhub.ai/p/maojiebc](https://clawhub.ai/p/maojiebc) |
| X | [@maojiebc](https://x.com/maojiebc) |
| 小红书 | [超级马甲](https://xhslink.com/m/4fQMJeHHWKC) |
| 微信公众号 | [超级马甲](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzY5NzIzODk2NA==#wechat_redirect) |

> 这份 Skill 来自 14 年用户运营、数据与内容生产实践。
