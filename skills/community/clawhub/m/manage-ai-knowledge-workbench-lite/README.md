# AI 自动知识工作台 Lite

把一个用户授权的本地 Markdown 文件夹或 Obsidian Vault，交给 AI 自动构建为可检索的派生知识层和离线 HTML 驾驶舱。首次构建、状态检查、按需增量更新和安全卸载均由 AI 调用随包脚本推进；普通步骤不需要用户逐条复制命令。

> 当前版本：`1.0.3`  
> 许可：MIT-0  
> 默认隐私模式：Metadata-only  
> Obsidian：可选，不是硬依赖

## 适合谁

- 已经在使用 OpenClaw、Codex 或其他能执行终端命令的 AI 智能体，希望快速建立本地知识工作台；
- 有 Markdown 或 Obsidian 笔记，但不想自己编写扫描、索引、HTML 和更新脚本；
- 希望默认保持事实源只读，并明确区分原始资料、派生知识层和展示层；
- 接受 Lite 版“按需自动更新”，暂时不需要后台常驻、语义摘要或云端正文分析。

## 从零开始

### 1. 先准备一个 AI 宿主

Skill 只有在 AI 宿主已经运行后才能被调用。宿主至少需要：

- 已配置一个可正常回复并可持续调用工具的模型；
- 能读取和写入用户明确授权的本地目录；
- 能执行终端命令并取得 stdout、stderr 和退出码；
- 能在权限、安装、删除和外部传输等门禁前询问用户。

OpenClaw 用户可从 [官方 Getting Started](https://docs.openclaw.ai/start/getting-started) 开始。模型、API Key、账号和 Gateway 配置均由宿主管理，本 Skill 不读取、保存或代管这些凭证。

其他智能体如果满足上述能力契约，可以作为候选宿主；未列入实测矩阵的产品或版本不应理解为已经验证兼容。

### 2. 准备 Python 3.10+

运行时只使用 Python 标准库，不要求 Node、数据库、Docker 或 Obsidian 插件。系统需要至少存在 `python3`、`python` 或 Windows `py` 之一，且实际版本为 Python 3.10 或更高。

如果没有 Python，请从 [Python 官方下载页](https://www.python.org/downloads/) 安装。Skill 会先真实探测版本；不会静默调用包管理器、提权或修改 PATH。

### 3. Obsidian 可装可不装

- 没有 Obsidian：直接使用普通 Markdown 文件夹；
- 已有一个 Vault：可把 Vault 同时作为工作区和事实源；
- 有多个候选 Vault：AI 会展示脱敏候选并请求一次选择，不会自动合并。

如需 Obsidian，可从 [官方下载页](https://obsidian.md/download) 安装。Obsidian CLI 和社区插件都不是本 Skill 的必需项。

### 4. 从 ClawHub 安装

在 OpenClaw 的目标工作区中使用 ClawHub 官方安装入口：

```bash
openclaw skills install @alexfengrui/manage-ai-knowledge-workbench-lite
```

安装后开启一个新会话，让宿主重新发现 Skill。其他宿主应使用其官方支持的 Skill 导入方式，不要根据网络帖子猜测隐藏目录。

## 一句话开始

普通 Markdown 文件夹或空目录：

```text
请使用 AI 自动知识工作台，把这个目录自动构建成知识工作台并打开驾驶舱：<目录>
```

已有 Obsidian Vault：

```text
请使用 AI 自动知识工作台接入这个 Vault，把它同时作为工作区和事实源，不修改原笔记，完成后打开驾驶舱：<Vault 目录>
```

以后更新：

```text
请更新这个知识工作台并告诉我实际变化和校验结果。
```

AI 应自行完成工具调用。除非遇到真实门禁，用户不需要手工执行工作台内部命令。

## AI 会自动完成什么

一次首次构建按以下顺序推进：

1. 探测 Python 和当前智能体宿主的真实版本；
2. 确认一个用户授权的工作区和事实源；
3. 诊断权限、路径、输出冲突和可用模式；
4. 安全初始化内部状态；
5. 扫描允许的元数据和显式 Markdown 结构；
6. 生成派生知识索引；
7. 校验计数、链接、敏感边界和输出结构；
8. 生成离线 HTML 驾驶舱；
9. 启动临时 loopback 校验并在验证后停止；
10. 返回实际产物路径和机器可读状态。

成功状态为 `AUTO_RUN_READY`。资料变化后，AI 可按用户请求执行确定性增量更新：没有变化时不重写知识层或 HTML，也不调用模型处理正文。

## 生成内容

默认只在选定工作区内创建三个保留目录：

| 目录 | 用途 | 是否事实源 |
|---|---|---|
| `.ai-workbench` | 配置、索引、状态与校验回执 | 否，可重建 |
| `AI-Knowledge` | 派生 Markdown 索引和导航页 | 否，可重建 |
| `AI-Dashboard` | 离线 HTML、数据和本地资源 | 否，可重建 |

用户原始 Markdown、Obsidian 笔记或指定资料目录才是事实源。请继续在原始资料中编辑，不要把 `AI-Knowledge` 当作新的输入源反复嵌套构建。

## 隐私与安全边界

Lite 固定为 Metadata-only：

- 本地确定性解析器可能读取授权 Markdown，以提取允许的 frontmatter、标题、标签和显式链接；
- 不把笔记正文发送给模型；
- 不把正文、密钥或绝对源路径嵌入 HTML；
- 敏感或未知敏感级别的记录默认不进入可见视图；
- 事实源保持只读，写入仅限三个保留目录；
- 本地页面不使用远程 CDN、统计脚本或源文件写入接口；
- 临时预览只绑定 loopback，并在自动验证后停止。

准确边界是“正文不发送给模型”，不是“程序从不读取 Markdown 文件”。AI 宿主本身可能把用户提示、Skill 指令和结构化工具结果发送给其已配置模型；模型服务的数据政策由宿主和模型提供商决定。

以下动作必须暂停并请求用户确认：访问新的目录、安装软件、提权、解决未知输出冲突、修改或删除事实源、删除派生产物、登录、付款、上传、发布或任何外部数据传输。

## Lite 版边界

Lite 包含：

- 单工作区 Metadata-only 构建；
- 普通 Markdown 与 Obsidian Vault；
- AI 自主首次构建和离线 HTML；
- AI 触发的按需增量更新；
- 状态检查；
- 默认保留事实源和派生产物的安全卸载。

Lite 不包含：

- 模型生成的正文摘要、语义分类或关系推断；
- filesystem watch、session watch 或后台计划任务；
- 持久 Web 服务；
- 多工作区聚合；
- 自动安装宿主、Python、Obsidian、模型或系统服务。

因此，“自动更新”在 Lite 中表示：用户提出更新目标后，AI 自动完成整次增量更新；它不表示宿主退出后仍永久在后台监听。

## 已验证兼容性

| 环境 | 已验证范围 | 边界 |
|---|---|---|
| OpenClaw `2026.6.11` / macOS | Metadata-only 首次构建、状态、安全卸载、卸载后状态，以及按需增量链路 | 不外推到所有 OpenClaw 版本、模型或后台模式 |
| Codex CLI `0.145.0-alpha.18` / macOS | 一次目标到自动构建与本地验证 | 不外推到所有 Codex 版本或 Windows |
| Windows 11 | 运行时设计支持 `python` / `py` 和 Windows 路径 | 尚无真实 Windows 11 端到端回执，暂不标记 verified |
| 其他终端型智能体 | 满足本页宿主能力契约时属于候选兼容 | 必须分别进行版本化测试 |

## 状态、更新与卸载

- 构建完成：以结构化状态 `AUTO_RUN_READY` 为准；
- 查看状态：让 AI 检查当前工作台状态；
- 更新：让 AI 更新工作台；AI 只处理真实差异；
- 默认卸载：移除 Skill 拥有的运行状态，保留事实源、`AI-Knowledge` 和 `AI-Dashboard`；
- 完全删除派生产物：必须另外确认精确路径，不能与默认卸载合并推断。

默认卸载成功后，再查状态应为 `NOT_INITIALIZED`；这表示运行配置已移除，不表示事实源或保留的派生产物被删除。再次使用时应发起一次新的自动构建。

## 常见问题

### 为什么没有自动帮我安装 Python？

安装软件、提权和修改 PATH 属于系统变更。Skill 会给出明确门禁和官方入口，但不会在未授权时静默执行。

### 没有 Obsidian 能用吗？

可以。普通 Markdown 模式具备 Lite 的完整基础闭环；Obsidian 只是可选的编辑和浏览界面。

### 会改我的原笔记吗？

默认不会。原始资料是只读事实源；知识层、状态和 HTML 写入保留目录。若遇到未知既有输出，Skill 会停止并请求处理决定。

### 为什么没有 AI 摘要？

Lite 固定为 Metadata-only，不把正文交给模型。它适合先验证结构化索引、HTML 驾驶舱和更新闭环。

### 为什么关闭 OpenClaw 后不会继续更新？

Lite 不包含 watch 或后台调度代码。需要更新时向 AI 提出一次更新目标即可。

### 排障时可以发什么？

通常只需操作系统、宿主版本、Python 版本、结构化 `code`、退出码和脱敏后的 `next_actions`。不要发送 API Key、Token、Cookie、模型配置、客户正文或整份 Vault。

## 版本 1.0.3

- 显式声明终端、授权文件读写、临时 loopback 与运行环境读取权限；
- 对齐说明与实际行为，明确保留目录、`127.0.0.1` 临时验证及“仅按需打开本地页面”；
- 在 Lite CLI 入口对调用方传入的 `validated_host` 先行做同一套严格校验，再交给工作流；
- 保持 Metadata-only、事实源只读、无外部正文上传、无后台常驻和 MIT-0 边界不变。

## 许可

本 ClawHub Lite 版本使用 MIT-0。任何人均可使用、修改和再分发，且不要求署名。ClawHub 不支持本 Skill 的平台内付费或付费墙；不要把该免费 Lite 版本理解为完整商业版。

## English quick start

AI Knowledge Workbench Lite lets an AI agent autonomously turn one user-authorized Markdown folder or Obsidian vault into a derived knowledge index and an offline HTML dashboard.

Requirements:

- an already configured agent host with local file and terminal tools;
- Python 3.10+ available as `python3`, `python`, or Windows `py`;
- one authorized workspace/source directory;
- Obsidian is optional.

Install from ClawHub:

```bash
openclaw skills install @alexfengrui/manage-ai-knowledge-workbench-lite
```

Then ask your agent: “Use AI Knowledge Workbench Lite to build this folder into a local knowledge workbench and open the dashboard: `<folder>`.”

Lite is fixed to Metadata-only. Its deterministic local parser may read authorized Markdown to extract allowed frontmatter, headings, tags, and links, but it does not send note bodies to a model or embed them in the dashboard. On-demand refresh is automatic after a user request; background watching and semantic/model-based content processing are not included.
