---
name: local-skills-router
description: 本地总路由技能。用于技能很多、请求可能命中多个相近 skill、或当前 agent 需要先判断“该读哪个 skill”时统一分流。先选下游 skill，再读取对应 SKILL.md。重点覆盖 ACP/ACPX harness、Lark、微信/公众号、小红书、OpenCLI 等高重叠技能簇。
---

# Local Skills Router

不要改写上游 skill 的 frontmatter 或说明。把这个 skill 当成本地稳定路由层。

## 工作原则

1. 先判断任务是否属于“技能簇路由问题”。
2. 如果是，先在本文件里选定最合适的下游 skill。
3. 再读取下游 skill 的 `SKILL.md`，按它的要求执行。
4. 如果多个下游 skill 都可能命中，优先选择：
   - 更具体的 skill
   - 直接执行的 skill
   - router / explorer skill 仅用于继续分流
5. 如果需求跨多个 skill，先选主 skill，再补第二个 skill。

## 路由表

### 1) ACP / ACPX / Claude Code / Codex / Gemini CLI / coding harness

- 用户说：
  - “用 Claude Code / Codex / Gemini CLI 做”
  - “走 ACP / ACPX”
  - “开 harness session / 连续线程 / thread 保持上下文”
- 优先路由：
  - `acp-harness-delegation`：当任务明确是“把工作委托给 ACP harness”
  - `acpx`：当任务是查 acpx 命令、flags、session、runtime、兼容客户端
  - `acpx-coding-default`：当当前 agent 需要默认走直接 acpx CLI 编码执行路径
- 路由规则：
  - “委托给 harness”优先 `acp-harness-delegation`
  - “研究 acpx 本身怎么用”优先 `acpx`
  - “当前 agent 默认执行策略”优先 `acpx-coding-default`

### 2) 小红书 / XHS

- 做内容卡片 / 多图图文 / 信息图：`baoyu-xhs-images`
- 真正操作小红书平台：`xiaohongshu-skills`
- 更细分时：
  - 登录/切账号：`xhs-auth`
  - 搜索/看笔记/看博主：`xhs-explore`
  - 发布：`xhs-publish`
  - 点赞/评论/收藏：`xhs-interact`
  - 竞品分析/热点/复合运营：`xhs-content-ops`
- 硬规则：
  - “做小红书图文”默认不是发布，先走 `baoyu-xhs-images`
  - “发到小红书”才走 `xhs-publish`

### 3) 微信公众号 / 微信文章

- 读公众号文章：优先 `wechat-reader`
- 用户给的是 mp.weixin 链接且要浏览器抽取：`wechat-mp-reader`
- 解析文章结构化内容：`wechat-article-parser`
- 搜索公众号文章：`wechat-article-search`
- 提取文章内容（若 extractor 可用且任务偏抽取流水线）：`wechat-article-extractor`
- 发布到公众号：
  - 发布草稿/Markdown 到公众号：`wechat-publisher`
  - 远程微信公众号发布链路：`wechat-mp-publisher`
- 路由规则：
  - “读文章/总结文章”优先 reader
  - “搜文章”优先 search
  - “发公众号”优先 publisher
  - “远程 HTTP MCP 发布链路”才走 mp-publisher

### 4) 飞书 / Lark

- 首次配置、登录、权限问题：`lark-shared`
- 通讯录：`lark-contact`
- 日历/日程：`lark-calendar`
- 云文档：`lark-doc`
- 云空间文件：`lark-drive`
- 即时消息：`lark-im`
- 邮件：`lark-mail`
- 多维表格 Base：`lark-base`
- 电子表格 Sheets：`lark-sheets`
- 任务：`lark-task`
- 知识库：`lark-wiki`
- 视频会议记录/纪要：`lark-vc`
- 妙记：`lark-minutes`
- 事件订阅：`lark-event`
- 自定义飞书 skill 开发：`lark-skill-maker`
- 官方原生 API 探索：`lark-openapi-explorer`
- 工作流类：
  - 会议纪要汇总：`lark-workflow-meeting-summary`
  - 日程+待办摘要：`lark-workflow-standup-report`
- 路由规则：
  - 先判断是“具体业务对象”还是“配置/权限问题”
  - 配置、登录、scope、permission denied 一律先看 `lark-shared`
  - “找资源”若是文档/表格名搜索，优先 `lark-doc`

### 5) OpenCLI

- OpenCLI 统一入口：`opencli`
- 定位：重要兜底技能。适合很多常规 tool、通用 browser、单一站点 skill 搞不定的读取、探测、适配器访问、外部 CLI 透传场景。
- 优先使用场景：
  - 用户明确提到 OpenCLI
  - 已知目标站点/客户端更适合 OpenCLI adapter
  - 需要结构化输出而不是临时浏览器抓取
  - 需要读取某些网站、客户端、外部 CLI 能力
  - 其他路径不稳定时，作为兜底方案
- 路由规则：
  - 明确站点适配器优势时，优先 `opencli`
  - 普通网页手工交互仍优先原生 browser
  - 当任务卡在“读不到内容 / 接不上客户端 / 浏览器方案不稳”时，升级到 `opencli`

## 重叠处理规则

1. 先分目标：内容生成 / 平台操作 / 配置鉴权 / 搜索发现。
2. 再选最具体的 skill，不选大而泛的 skill。
3. 配置、登录、权限问题优先于业务执行。
4. 内容生成和平台操作强制分开。
5. 仍不确定时，先用 router 继续分流。

## 本地维护原则

- 不修改上游 skill 的 frontmatter。
- 路由知识只维护在本 skill。
- 新增同类 skill，先更新本文件。
- 上游 skill 更新后，只校验路由是否仍然成立。
