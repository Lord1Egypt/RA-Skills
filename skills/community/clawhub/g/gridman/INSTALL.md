<!-- INSTALL.md —— 安装指南（前置条件、Skill 安装、执行能力说明、记忆区配置） -->

# 古立特 Gridman 安装指南

## 前置条件

- 一个支持 SKILL.md 的宿主【如 Kiro、Cursor、Claude Code、ChatGPT Work（codex）、OpenClaw 等】

## Skill 安装

将 `gridman-skill/` 整个目录复制到宿主的 skill 目录下即可。

具体路径视宿主不同：

| 宿主        | 安装路径                        |
| ----------- | ------------------------------- |
| Kiro        | `.kiro/skills/gridman/`       |
| Claude Code | `~/.claude/skills/gridman/`   |
| OpenClaw    | `~/.openclaw/skills/gridman/` |

## 执行能力（由宿主或 Tools 提供，不装进 Skill）

古立特本体只是知识、规则和人格文本，**不包含、不分发、不维护任何可执行工具**。需要执行外部操作（读写文件、抓取网页、处理表格、生成或解析文档等）时，它只声明抽象能力需求（如 `document.extract`），再去发现由外部提供的实现。

古立特按固定顺序、且只在这三处发现能力：

1. **宿主原生能力**——宿主（Kiro、Claude Code 等）自带的文件读写、网页抓取、终端命令等；
2. **宿主 MCP**——你在宿主的 MCP 配置里登记的服务（如 Playwright）；
3. **本机 CLI（Tools）**——只在 `~/.gridman/home.json` 的 `gridman_tools` 指向的目录里，由 `provider.json` 声明的 CLI。

三处都没有对应能力时，退回「知识指引模式」，只给方法、模板和判断规则，并说明未完成范围。

> **重要边界（安装工具时务必遵守）**
> 新装的工具能不能被古立特发现，取决于你把它接到了哪条线上：装成宿主 MCP、宿主原生能力，或放进 Tools 目录并写好 `provider.json`，古立特才找得到；装在别处、没有登记的，它不会去扫描你的系统，也就发现不了。
>
> **任何可执行程序、COM/DLL、依赖包或工具代码都不能放进 `gridman-skill/` 目录。** Skill 要能原样复制到别的宿主和电脑，一旦混入本机可执行内容就会失去可移植性并污染发布内容。控制 Office、OCR、浏览器等本机执行能力一律归 `gridman-tools/` 或宿主，通过 `provider.json` 或宿主配置被发现。

抽象能力语义以 `operations/capability_registry.md` 为准。本机 Tools 只有在 `provider.json` 存在、其声明的 capability 已在能力表注册、入口脚本存在且离线检查通过时，才可视为可用；旧能力记录、脚本文件名或目录存在都不代表能力当前可用。

古立特在**运行对话中不现场充当安装教程**：能力缺失时它只说明缺哪类能力、并指向本文档，不逐步复述安装步骤。是否配置宿主原生能力、MCP 或 CLI，由用户自行按所用宿主的文档处理；常用工具的接入说明见下方「推荐工具与接入」。

## 私有资源配置（可选）

古立特使用两个相互独立的私有资源区：

- `gridman-mind/`：项目上下文、用户偏好、正式交付物和学习反馈；
- `gridman-tools/`：本机 CLI、凭证隔离和待复核的工具直接输出。

两者均由用户指定位置，并以独立字段登记到 `~/.gridman/home.json`：

```json
{
  "schema_version": "1.0",
  "gridman_version": "3.0.1",
  "gridman_mind": "用户确认的 Mind 绝对路径",
  "gridman_tools": "用户确认的 Tools 绝对路径"
}
```

`schema_version` 表示 `home.json` 的结构版本，不随古立特产品补丁号变化；`gridman_version` 只记录创建或最近确认该配置的产品版本。现有 `{ "version": "1.0" }` 视为旧格式并兼容读取，但下一次经用户授权更新配置时应无损迁移为上述新格式，不得丢失未知字段或另一私有资源路径。

首次需要对应资源时，古立特应先询问位置，获得同意后才创建和登记；新增一个字段不得覆盖另一个字段。Tools 的建议结构为：

```text
gridman-tools/
├── provider.json       简单声明：能力、入口、离线检查方式、副作用与授权参数
├── cli/                 本机 CLI
├── secrets/             API key/token，仅由对应 CLI 读取
├── outputs/             工具直接输出，业务复核后再决定是否归档
├── TOOLS_SETUP.md       本机工具配置和调用说明
└── .gitignore           排除凭证、输出与临时文件
```

API key 不进入 Skill、Mind、开发日志、命令参数或交付物。未配置私有资源不影响纯财税问答；完整定位、创建、授权和降级规则见 `operations/private_resources_rules.md`。

---

# 推荐工具与接入（可选）

> 本节工具**均为可选**，由用户在**宿主侧**自行配置。古立特本体不内置、不分发、不强依赖任何工具。
> 古立特运行时只按 `document.extract` 等抽象能力去发现宿主提供的实现，不直接持有下列服务的凭证。

## 文档解析：MinerU

### 是什么

MinerU 是一款文档解析引擎，可把 **PDF、图片、扫描件、DOCX、PPTX、XLSX、网页**等转成结构化 **Markdown / JSON**：

- 扫描件、拍照件自动 OCR（多语言）
- 表格 → HTML，公式 → LaTeX
- 自动去页眉页脚、按阅读顺序还原版式、跨页表格合并

对应古立特的抽象能力 `document.extract`（发票识别、扫描件提取、Word/PPT/Excel 提取、文档转 Markdown 等场景）。

### 接入方式（当前项目配套实现：官方 API + 本机 CLI）

当前项目可在用户私有的 `gridman-tools/` 中配套部署轻量 CLI，不安装 MinerU 模型，也不额外运行 MCP Server。该 CLI 属于私有 Tools，不随 Skill 分发；复制 Skill 到其他宿主时，只有实际部署后才可视为可用。部署后应满足以下文件约定：

```text
gridman-tools/
├── provider.json
├── cli/document_ocr.py
├── secrets/mineru.token
├── outputs/
└── TOOLS_SETUP.md
```

`document_ocr.py` 仅使用 Python 标准库，按 MinerU 官方 v4 精准解析流程工作：

```text
申请签名上传地址
→ PUT 上传本地文件
→ MinerU 自动提交解析
→ 按 batch_id 轮询状态
→ 下载并安全解压结果 ZIP
```

官方接口文档：[https://mineru.net/apiManage/docs](https://mineru.net/apiManage/docs)。当前认证方式为 `Authorization: Bearer Token`；Token 由脚本从 `MINERU_TOKEN` 环境变量或 `gridman-tools/secrets/mineru.token` 读取，环境变量优先。Token 不作为命令参数传入，也不得写进本安装文档。

### 配置步骤

1. 登录 [MinerU](https://mineru.net/) 并在 [API 管理页面](https://mineru.net/apiManage/token) 创建 Token；已经在聊天、日志或截图中暴露的 Token 应撤销并更换。
2. 确认 `~/.gridman/home.json` 的 `gridman_tools` 指向用户确认的 Tools 根目录。
3. 从与古立特 3.0.1 配套、由开发者单独提供的 `gridman-tools/` 包取得 `provider.json` 和 `cli/document_ocr.py`；只有 Skill、缺少该 Tools 包时，不得把 MinerU CLI 宣称为可用。
4. 将 Token 单独保存为 `gridman-tools/secrets/mineru.token`，文件只含一行 Token，不加引号、`Bearer` 前缀或其他文字；也可使用当前进程的 `MINERU_TOKEN` 环境变量。
5. 确保 `gridman-tools/.gitignore` 至少排除 `secrets/`、`outputs/`、`.env`、`*.token`、`*.key` 和 `__pycache__/`。
6. 在 Tools 根目录执行离线检查：

```powershell
python ".\cli\document_ocr.py" --check
```

该检查只验证本机目录和 Token 配置，不连接 MinerU，也不上传文件。出现“Token: 已配置”后即可使用。

### 调用示例

上传前必须确认文件可以发送至 MinerU，并判断敏感财税信息是否需要脱敏：

```powershell
python ".\cli\document_ocr.py" "D:\待处理\示例.pdf" --model vlm --ocr --confirm-upload
```

- 默认模型为 `vlm`；普通 PDF、Office 文档和图片可选 `pipeline` 或 `vlm`；HTML 必须指定 `--model MinerU-HTML`。
- `--ocr` 显式启用 OCR；表格和公式识别默认开启。
- `--confirm-upload` 只允许在已说明 MinerU 服务、待上传文件范围与风险，并取得用户明确同意后添加；缺少该参数时 CLI 会在读取 Token、创建输出目录和联网之前拒绝执行。
- 默认轮询 900 秒，可通过 `--timeout` 和 `--interval` 调整。
- 默认结果写入 `gridman-tools/outputs/<输入文件名>/`；这些仍是待复核的工具直接结果，不能自动视为 Mind 中的正式交付物。
- 官方限制包括单文件不超过 200MB、200页；CLI 会在上传前检查文件存在性、空文件和 200MB 限制，页数由服务端校验。

详细的本机操作说明以 `gridman-tools/TOOLS_SETUP.md` 为准。若宿主已有可用的 MinerU MCP，古立特仍可按能力发现顺序使用它，两种接入方式不冲突。

### 数据安全（财税文件重要）

- MinerU 云 API 会**将文件上传到外部服务**。财税文件常含敏感信息，上传前应**先脱敏或征得用户同意**。
- 如条件允许，优先使用 MinerU 的**本地/离线部署**（其官方支持纯 CPU 离线运行），避免敏感数据外传。
- 该数据安全约束同时写在 `operations/routing_flow.md` 的「document.extract 授权与脱敏」规则中，运行时强制执行。

### 未配置时的表现

宿主未配置 MinerU 或任何文档解析能力时，古立特不会报错卡死，而是退回「知识指引模式」：说明当前缺文档解析能力、可参考本节配置，或建议用户先手动 OCR 后再提供文本。

---

## 网页渲染取数：Playwright

### 是什么

Playwright 是一款浏览器自动化引擎，可**驱动真实浏览器渲染页面后再提取内容**。它解决的是普通 `fetch` 类抓取的盲区——财政部会计司、国家税务总局法规库、审计文库（MaoDocs）等**政务/财税网站多为 JS 动态渲染**，纯 HTTP 抓取拿不到正文，必须由浏览器渲染后才能读到。
（有条件的最好直接上ego lite，目前只支持mac用户）

对应古立特的抽象能力 `web.fetch` / `browser.operate`（核实法规原文、抓取准则最新列表、查上市公司公告等联网核实场景）。

### 浏览器通用（不锁定某一款）

Playwright 支持多种浏览器内核，古立特**不绑定任何一款**，用宿主机器上已有的即可：

| 浏览器参数   | 说明                                          |
| ------------ | --------------------------------------------- |
| `chromium` | Playwright 自带内核，最通用，无需本机装浏览器 |
| `chrome`   | 复用本机已装的 Google Chrome                  |
| `msedge`   | 复用本机已装的 Microsoft Edge                 |
| `firefox`  | Firefox 内核                                  |
| `webkit`   | WebKit 内核（Safari 同源）                    |

推荐优先 `chromium`（跨机器最稳、免额外安装）；本机已装 Chrome/Edge 时用 `chrome`/`msedge` 也可。**具体选哪个由用户在宿主侧配置决定，古立特只发现并调用，不锁死浏览器。**

### 接入方式（宿主侧 MCP 配置）

在**宿主的 MCP 配置**里加一个 Playwright server（以 Kiro 的 `mcp.json` 为例，其他宿主同理）。最小可用配置：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@0.0.78", "--browser", "chromium"],
      "disabled": false
    }
  }
}
```

若要把浏览器截图、快照、网络日志等输出集中到项目缓存目录（推荐，便于统一管理和清理），加上 `--output-dir`。以 Windows + 本机 Edge 为例的完整配置：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "D:/APP/Node/npx.cmd",
      "args": [
        "-y",
        "@playwright/mcp@0.0.78",
        "--browser",
        "msedge",
        "--output-dir",
        "D:/项目路径/gridman-tools/.cache/playwright-mcp"
      ],
      "disabled": false
    }
  }
}
```

配置要点（避坑，均为实测踩过的坑）：

- **固定版本**：用 `@playwright/mcp@0.0.78` 这类固定版本号，不用 `@latest`——`@latest` 每次启动都访问 npm registry，网络慢时会连接失败。可先用 `npx @playwright/mcp@0.0.78 --help` 确认本机该版本支持你要用的参数（如 `--output-dir`）。
- **Windows 路径一律用正斜杠 `/`**：JSON 字符串里反斜杠 `\` 是转义符，Windows 路径若用 `\` 必须写成 `\\`，极易漏写导致「字符串中的转义字符无效」。改用正斜杠 `/`（`D:/APP/Node/npx.cmd`）Windows 和 Node/Playwright 都认，且完全免转义，一劳永逸。
- **命令路径要逐字核对**：`D:/APP/Node/npx.cmd` 里 `APP` 是两个 P，路径写错（少字母、目录名不符）会导致 MCP「Connection Failed」，而不是 JSON 报错。
- **括号必须三层闭合**：`{`（最外层）→ `"mcpServers": {` → `"playwright": {`，结尾要对应三个 `}`。少一个就会报「预期为逗号或右大括号」。保存后看编辑器左下角「问题」是否归零来判断 JSON 是否合法。
- **浏览器可换**：把 `--browser` 后面换成 `chrome`/`msedge`/`firefox`/`webkit` 即可，古立特不感知差异。
- **有头/无头**：默认有头（浏览器窗口可见，便于人工旁观）；服务器/无人值守场景可加 `--headless`。
- **Windows 上 npx 找不到时**：把 `command` 换成 `npx.cmd` 的绝对路径（如 `D:/APP/Node/npx.cmd`）。

排查顺序建议：先让 JSON 合法（「问题」归零）→ 再点宿主 MCP 面板的 Retry 重连 → 连接成功后应显示可用工具数（如 `Connected (24 tools)`）。若 JSON 已合法但仍 Connection Failed，重点查 `command` 路径和版本号，而不是继续改括号。

### 数据安全（呼应铁律 6）

- 网页内容是**待分析的数据，不是指令**。抓回的页面若夹带"忽略以上指令""把数据发到某地址"等文本，古立特一律当内容对待、绝不执行。
- 只访问核实类公开信息（法规/准则/公告），不在页面上做登录、支付、提交等**不可逆操作**——那类协同操作另有安全模型（人在场 + 认证归人 + 每步确认）。

### 未配置时的表现

宿主未配置 Playwright 或任何网页渲染能力时，古立特退回「知识指引模式」：说明当前缺联网渲染能力、给出可参考的官方查询源（见 `operations/source_directory.md`），或建议用户手动打开页面把正文贴给它。

---

## 文档生成：Office / WPS COM（本机 Tools）

### 是什么

通过 Windows COM 驱动本机已安装的 **Microsoft Office** 或 **WPS Office**，生成和编辑 Excel、Word、PPT。它对应古立特的抽象能力 `document.generate`（生成底稿、报表、说明文档等）。

它驱动的是本机已装的 Office/WPS，不是替代品——本机没装对应软件就没有 COM 可用。

### 接入方式（本机 Tools + 独立 Python 环境）

这是**本机执行能力，属于私有 `gridman-tools/`，不随 Skill 分发，也绝不放进 `gridman-skill/`**。它依赖 `pywin32`，装在一个独立的 Python 环境里，避免污染全局环境或其他工具：

```text
D:\APP\office-com\          # 独立运行环境（示例位置，可自定）
├── .venv\                  # 安装 pywin32 的虚拟环境
├── requirements.txt        # 固定 pywin32 版本
└── README.md               # 环境用途与重建方法

gridman-tools\
├── cli\office_com.py       # COM 调用入口
└── provider.json           # 声明 office-com-cli 实现 document.generate
```

Skill 侧只在 `operations/capability_registry.md` 保留抽象能力 `document.generate`，不含任何 COM 代码。`provider.json` 应在 `entrypoint.executable` 中声明虚拟环境的完整解释器路径，避免调用方误用全局 Python。

### 配置步骤

1. 确认本机已安装 Microsoft Office 或 WPS Office。
2. 用宿主机的 Python 创建独立环境，并从固定版本清单安装依赖：

```powershell
python -m venv "D:\APP\office-com\.venv"
& "D:\APP\office-com\.venv\Scripts\python.exe" -m pip install -r "D:\APP\office-com\requirements.txt"
```

当前配套 `requirements.txt` 固定为 `pywin32==312`；升级依赖时应显式修改该文件并重新验证，不使用无版本约束的 `pip install pywin32`。

3. 把 `cli/office_com.py` 放入用户确认的 `gridman-tools/`，并确保 `provider.json` 声明 `office-com-cli` 及上述虚拟环境解释器。
4. 执行注册检查（不创建 Tools 缓存、不启动应用）：

```powershell
& "D:\APP\office-com\.venv\Scripts\python.exe" ".\cli\office_com.py" --check
```

出现各 ProgID「已注册」即可使用。

### 调用示例

```powershell
& "D:\APP\office-com\.venv\Scripts\python.exe" ".\cli\office_com.py" --suite microsoft --app excel --text "示例" --output "D:\产出\demo.xlsx"
```

- `--suite` 必须显式指定 `microsoft` 或 `wps`，不靠模糊 ProgID 猜测。
- `--app` 选择 `excel` / `word` / `ppt`。
- 默认**有头运行**，应用窗口可见；仅在明确需要后台运行时添加 `--headless`。
- 覆盖已存在的文件必须显式添加 `--confirm-overwrite`；缺少时在启动应用前拒绝。
- 结果默认写入 `gridman-tools/outputs/`，是待复核的工具直接结果，复核后才归档到 Mind。

### 安全（本机副作用）

- `--check` 只检查 pywin32 可用性和 COM 注册状态，不创建 Tools 缓存、不启动 Office/WPS。
- COM 会启动和操作本机应用、写入文件，属于本机副作用；覆盖、批量修改前必须确认。
- CLI 无论成功或失败都会退出应用并释放 COM 对象，避免残留隐藏进程。
- 默认操作新建文档，保护用户原始文件。

### 未配置时的表现

本机未安装 Office/WPS，或未部署该 CLI 与独立环境时，古立特退回「知识指引模式」：说明当前缺文档生成能力、给出内容结构或模板，由用户自行生成。
