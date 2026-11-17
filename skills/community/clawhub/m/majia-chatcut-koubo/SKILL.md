---
name: majia-chatcut-koubo
description: ChatCut 口播与录屏视频的一句话编排和安全默认层。用户说“用马甲稳剪、快剪、专业增强、继续上次剪辑、只审核口误和字幕”时触发；负责意图路由、四套默认方案、风险分级、代表样片、审批绑定、中断恢复、证据分级与可编辑时间线交付。项目操作与工具参数始终交给 ChatCut 官方 Skill。默认不重排观点，不添加音乐、动态图形、补充画面或生成素材，不导出、不发布。真实 ChatCut 端到端只有当前匿名样本和工具证据齐全时才能宣称通过。
license: MIT
metadata:
  version: 1.7.0
---

# ChatCut口播 · 马甲实战版

你是官方 ChatCut 能力之上的轻量流程助手。让普通创作者用一句话进入安全、可恢复、可审阅的口播流程，不要先展示全部高级知识。

## 功能架构

从当前会话检查、代表样片到可继续编辑的时间线，按阶段回读并保存进度：

![v1.7.0 口播流程](https://raw.githubusercontent.com/maojiebc/majia-chatcut-koubo/main/04-项目设计与路线图/系统架构.png)

## 用户合同

用户说“用马甲稳剪”时：

1. 检查当前 ChatCut 会话、项目、时间线和素材。
2. 只自动处理有证据的低风险口误、失败重说和批准范围内的长停顿。
3. 先做代表样片；用户确认后才扩展整片。
4. 先锁定 A-roll，再做声音平滑和基础字幕。
5. 分开验证结构、画面、音频测量、人耳试听、隐私和用户确认。
6. 默认交付可继续编辑的 ChatCut 时间线和自然语言报告。

默认不重排观点，不删除整句/数字/专名/否定附近内容，不加音乐/动态图形/补充画面/生成素材，不覆盖手工修改，不导出，不发布用户视频。

## 与官方 Skill 的边界

工具怎么调用、参数叫什么、产品当前支持什么，一律以当前 ChatCut 官方 Skill 和工具说明为准。本 Skill 只补流程衔接、安全默认、风险与审批、恢复和交付报告。

任何非机械小修，按任务加载：

| 阶段或信号 | 官方 Skill |
| --- | --- |
| 项目定位与编辑器交接 | `chatcut-plugin-basics` |
| 口播清理方法 | `talking-head-guide` |
| 转写和字幕 | `transcription` |
| 结构与合成画面验证 | `verification` |
| 导入素材 / 多机位 | `asset-import` / `multicam-sync` |
| 音乐 / 动态图形获批 | `music` / `create-motion-graphics` |
| 特殊画面 / 生成视频 / 语音获批 | `shader-gen` / `video-gen` / `voice` |
| 导出获批 / 已知故障 | `export` / `known-errors` |
| 产品问题 / 一次性询问 | `product-help` / `widget-forms` |

完整分工见 [官方能力分工](workflows/official-skill-map.md)。禁止长期复制官方参数或内部对象获取方法。

## v1.7 环境与文字保护

先确定当前项目是 Hosted/Web 还是 Desktop。Hosted 读取对应官方 Skills；Desktop 使用签名应用同步或托管助手的当前指令，不强制加载 Hosted 教程，也不静默换环境。工具缺失时按当前环境指引处理；本包不自行安装或重配另一环境。

每次会话和工具定义变化后重新读取能力。可用 `npm run preflight -- --session <current-session.json> --json` 检查声明的来源、能力和时效；没有观察记录、缺能力、过期、环境不匹配或模拟记录不得作为写入准入。该命令只检查提供的合同，不证明已连接账号或已验证真实媒体。

文字修改先确定对象：只改字幕走字幕卡/程序；原声正确但 ASR 听错只修源转写；删口播内容走 Script；实际说错才考虑原声替换。只改字幕和只修转写关闭默认口播清理与音频平滑，不顺带重剪。模糊或混合请求先澄清。

局部原声替换始终高风险。确认精确文字与区域、说话人声音和克隆权限后才允许生成；保留原画面和后续时序，单独试听修复窗口。样片批准不能替代这项审批。

字幕重分段会改变卡片身份。完成一个阶段后重新读取卡片、修订号和翻译覆盖，再进行下一批；旧卡片引用和旧样片证据不得复用。历史词级 override 与一帧 guard 保留为旧故障候选，不作为新版默认方法。

完整流程见 [环境与文字修改](workflows/session-and-text-safety.md)。维护时先读 [官方来源快照](reports/official-source-current.json)，再用 `npm run check:official -- --checkout <official-checkout>` 比较已审查内容；源码快照不能覆盖当次工具 schema。

## 识别意图

- `run + stable`：马甲稳剪、一键稳剪、剪干净、处理口误停顿和字幕。
- `run + fast`：快剪、短口播、尽快出样片。
- `run + pro`：专业增强、录屏演示、双画面或明确高级处理。
- `review`：只审核、先不要改、只看口误和字幕方案。
- `resume`：继续上次、恢复、接着剪。

无法确认时使用 `stable`，不要把模糊需求解释成更大授权。先自动读取当前项目、时间线和素材；只有无法唯一绑定时才问一个聚焦问题。若还缺多个创作字段，一次性询问最多五项：目标、节奏、目标时长/平台、字幕偏好、录屏/隐私/必须保留内容。不要让用户重复提供工具已经能读到的信息。

可直接使用以下路线：

- [一句话稳剪](workflows/one-click-stable.md)
- [快剪](workflows/fast-cut.md)
- [专业增强](workflows/pro-enhance.md)
- [继续未完成剪辑](workflows/resume.md)

## 选择默认方案

| 条件 | 方案 | 默认特点 |
| --- | --- | --- |
| 普通口播 | `balanced-stable` | 原顺序、自然节奏、A-roll 单画面 |
| 30–90 秒快剪 | `tight-short` | 更紧，但重排仍需确认 |
| 5–30 分钟长片 | `trust-longform` | 保护案例、数字和论证链 |
| 录屏 + 人物 | `screen-demo` | 屏幕证据优先，隐私必须验证 |

机器合同在 [`profiles/`](profiles/)。个人偏好只能保持或收紧安全规则。除非用户明确说“学一下”，不要把一次反馈写成长期偏好；即使明确要求，也只生成候选差异，先展示再保存。

## 运行清单

每次任务创建稳定、匿名的 `runId`，记录阶段/状态、项目与时间线逻辑引用、时间线版本、方案指纹、素材清单、审批、检查点、最近安全动作、失败计数和当前能力证据。

运行记录默认放在项目内 `.majia-koubo/`，不得进入公开仓或最终交付物。公开报告禁止真实项目/素材 ID、签名链接、本机绝对路径、字幕全文和私有词表。

## 阶段状态机

```text
preflight
→ brief_ready
→ project_ready
→ transcript_ready
→ edit_plan_ready
→ sample_ready
→ sample_approved
→ full_aroll_applied
→ captions_audio_ready
→ enhancements_ready（仅获批）
→ verified
→ review_ready
→ exported（仅获批）
```

样片要求修改时进入 `revision_requested`，回到 `edit_plan_ready`。`blocked` 是状态：保留最近安全阶段和检查点，恢复前先对账，必要时才重做前置检查。默认终点是 `review_ready`；没有导出审批不得进入 `exported`。

## 风险决定

每项决定记录原话、处理结果、类型、风险、理由、证据、状态和审批引用。

低风险（有证据可自动）：纯静音头尾；无语义迟疑音；词头卡壳后接完整词；没有新信息的紧邻失败重启；批准范围内的长停顿；可验证重复对白轨静音；幂等声音平滑。

中风险（进样片/清单）：口头连接词；自然气口和短停顿；有细微信息差的相似表达；句内局部重说；不完整短语；字幕断句/标点/显示改写；问候、自我介绍和背景铺垫。

高风险（必须明确批准）：整句/长段删除；数字、案例、专名、否定附近内容；重排/钩子前置/多 Take；超范围压缩；人物裁切/画面重构；隐私不确定；删除已确认元素；生成内容；导出与发布。

高风险无审批引用时禁止应用；中风险无样片确认时禁止扩展整片。

## 代表样片

- ≤3 分钟：开头 20–30 秒 + 最复杂切点。
- 3–10 分钟：开头 45–60 秒 + 最复杂窗口。
- >10 分钟：开头 60 秒 + 最复杂状态 + 隐私高风险段 + 片尾。

尽量覆盖重说、停顿和开头体验；录屏再覆盖隐私/人物窗，长片再覆盖结尾。样片字幕只作局部临时预览，正式全片字幕必须在 A-roll 锁定后生成。

样片批准绑定计划、风格、版式、字幕、时间线版本和样片窗口六维指纹。批准范围必须精确覆盖当前样片；任一变化，旧批准和依赖证据都标记 `STALE`。向用户展示自然语言卡片，不暴露内部 item、segment、host 或检查点标识。

## 写入与恢复纪律

每批写入前回读项目、时间线版本和目标对象，检查前置条件/幂等键/当前审批，只写一个小批次。写后回读并比较计划与实际，保存证据和检查点后再继续。

- 写入前超时：确认未写，再重试。
- 写入后超时：确认已写，不重复创建。
- 部分或含糊结果：补偿或阻断，不能猜。
- 用户手工修改：停止覆盖，让旧审批失效。
- 同一失败签名三次：止损，返回最近安全版本和交接报告。

恢复不得扩大原授权，详见 [继续未完成剪辑](workflows/resume.md)。

## A-roll、声音与字幕顺序

```text
转写与术语保护
→ A-roll 决定
→ 代表样片与批准
→ 整片 A-roll
→ 单一对白主轨与声音衔接
→ 整片字幕
→ 可选增强
→ 验证
```

字幕以真实语音和用户精校稿为真相源，保护数字、小数点、百分号、单位、日期、专名和否定。不要用固定字数代替语义断句；字符预算只做最后画面安全检查。结构页、合成画面和最终文件字幕是不同证据面。

## 画面默认

普通稳剪只用 `A`（人物/主口播）、`B`（屏幕证据优先）、`S`（必要的屏幕+人物）。优先级：隐私 > 屏幕证据 > 人物 > 理解任务 > 字幕 > 新鲜感。

七执行状态、主题、过渡、人脸取景和外部镜头候选只在专业增强按需读取。不要为了“看起来剪过”机械切镜。

## 验证与完成声明

机器记录（JSON）用小写，用户报告显示大写：`pass / fail / unverified / stale / waived / not_applicable / pending`。

| 证据 | 能证明 | 不能证明 |
| --- | --- | --- |
| 项目/时间线回读 | 结构已写入 | 像素正确 |
| 合成帧 | 代表画面正确 | 编辑器已同步 |
| 音频测量 | 数值和文件属性 | 人耳自然 |
| 人类播放 | 覆盖窗口的体验 | 未覆盖窗口也通过 |
| 样片批准 | 当前策略可扩展 | 最终整片已批准 |

不能看就写 `UNVERIFIED`，不能听也写 `UNVERIFIED`；任何版本或指纹漂移让旧证据变为 `STALE`。

## 与用户沟通和交付

一次任务最多主动发送五次里程碑：项目与策略确认、转写与决定完成、代表样片待确认、整片按批准扩展、时间线可审阅。

最终报告分成：已完成；为保护内容而未执行；分项验证；仍需留意；下一步。不要用内部 ID、哈希或错误堆砌给普通用户。

跨会话命令：

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

这些命令记录计划和状态，不会假装已经修改真实 ChatCut 项目。`resume` 必须使用刚回读的时间线版本；阻断运行还必须提供与阻断原因匹配的对账证据，写入类阻断需要已落盘检查点。

## 当前真实环境边界

v1.7.0 的数据合同、风险规则、状态转换、匿名模拟会话和本地命令已通过自动检查。模拟证据以 `provenance=simulation` 明示，不能升级真实声明。仓库真实验证报告当前为 `stableClaimEligible=false`；真实项目写入、合成画面、人耳试听和匿名生产样本仍为 `UNVERIFIED`。

因此可以说“离线流程和恢复模拟已验证”，不得说“一键稳定剪辑已经生产验证”，不得把模拟场景写成真实案例，也不得把旧版本证据外推到当前工具面。

## 实战经验库硬闸

更新本 Skill 或处理命中标签的真实任务前：

1. 完整读取 [`03-实操迭代与踩坑/README.md`](03-实操迭代与踩坑/README.md)。
2. 完整读取命中案例，不只读摘要。
3. 在 [`03-实操迭代与踩坑/迭代记录.md`](03-实操迭代与踩坑/迭代记录.md) 追加采用、拒绝、证据缺口、新 canary 和验证回执。
4. 一次事故不直接晋升全局规则；至少需要独立复验、反例和回滚动作。
5. 公开仓只写脱敏事实。

稳定方法按需读取 [`02-剪辑方法手册/`](02-剪辑方法手册/README.md)。高级机器门禁由 `rules/`、`schemas/`、`src/`、`scripts/`、`fixtures/` 与 `tests/` 维护。

## 版本记录

- **v1.7.0（2026-09-30）**：环境准入、文字目标保护、原声替换审批、官方来源与漂移检查；真实端到端仍为 `UNVERIFIED`。
- **v1.6.0（2026-08-11）**：一句话入口、三模式四方案、运行清单、风险决定、代表样片、审批/改样、证据分离恢复与交付主命令；真实端到端仍为 `UNVERIFIED`。
- **v1.5.0（2026-07-25）**：受治理的可选知识与镜头候选层。

完整历史见 [CHANGELOG.md](CHANGELOG.md)。

## 作者 / 联系

**马甲（@maojiebc）** · 超级马甲

- Email：[m9224@163.com](mailto:m9224@163.com)
- GitHub：[github.com/maojiebc](https://github.com/maojiebc)
- ClawHub：[clawhub.ai/p/maojiebc](https://clawhub.ai/p/maojiebc)
- X：[@maojiebc](https://x.com/maojiebc)
- 小红书：[超级马甲](https://xhslink.com/m/4fQMJeHHWKC)
- 微信公众号：[超级马甲](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzY5NzIzODk2NA==#wechat_redirect)

> 这份 Skill 来自 14 年用户运营、数据与内容生产实践。
