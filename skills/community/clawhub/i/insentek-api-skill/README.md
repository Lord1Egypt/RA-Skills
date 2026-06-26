# Insentek OpenAPI Skill

> 让终端用户用自然语言轻松查询 insentek（东方智感）物联网设备数据。

---

## 简介

本项目基于 insentek OpenAPI v3，产出一份通用 `skill.md` 技能文件及配套文档与示例。终端用户可在 **OpenClaw、Hermes-Agent、Claude Code、ChatGPT** 等 Agent 平台上直接对话使用，通过自然语言调用 API 完成设备数据查询、报告生成与实时分析。

**支持的设备类型：**
- 🌱 **Z** — 土壤墒情仪（土壤温度、水分、电导率）
- 🌤️ **T** — 气象站（空气温度、湿度、风速、降雨量、PM2.5 等）
- 📏 **J** — 见厘液位计（激光液位、电池电压）

---

## 快速开始

### 前置依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Node.js | ≥ 18 | 运行 `npx @insentek/openapi-skill` CLI |
| Python | ≥ 3.10 | 运行 `scripts/insentek_cli.py` 等脚本（脚本使用了 PEP 604 联合类型语法） |
| openpyxl（可选） | 任意 | 仅当需要 Excel 导出时 |

> macOS / Linux 通常应使用 `python3` 命令调用脚本，不要使用裸 `python`（在新版 macOS 与 Ubuntu/Fedora 上不存在或指向 Python 2）。CLI 的 `info --json` 会输出 `python.command`，Agent 必须以该值作为脚本调用前缀。

### 1. 获取认证信息

登录 [E 生态](https://cloud.ecois.info)，在「应用管理」中创建应用，获取 `appid` 和 `secret`。

### 2. 安装 Skill

**一键安装（推荐）：**

```bash
npx @insentek/openapi-skill
```

| 类型 | 名称 |
|------|------|
| npm package | `@insentek/openapi-skill` |
| skill id | `insentek-openapi` |
| 安装目录 | `insentek-openapi` |

CLI 会引导选择 **runtime**（OpenClaw / Claude Code），支持 **scope**（`global` / `project` / `workspace`），并动态解析本机安装路径。

```bash
npx @insentek/openapi-skill install -r claude -s global -y
npx @insentek/openapi-skill update -r claude -y
npx @insentek/openapi-skill doctor
npx @insentek/openapi-skill info
```

OpenClaw 用户也可通过 ClawHub 单独安装（与本 CLI 无关）：

```bash
clawhub skill install insentek-api-skill
```

| 命令 | 说明 |
|------|------|
| `install` | 安装 skill |
| `update` | 更新到当前包版本 |
| `status` / `doctor` | 查看状态 / 诊断 |
| `uninstall` | 卸载 |

> CLI 源码见 [`packages/insentek-skill-cli/`](packages/insentek-skill-cli/)。路径因 runtime/scope/OS 而异，请用 `info` / `doctor` 查看本机实际位置。

### 命名约定

仓库中涉及三套名字，用途不同，**不要混用**：

| 维度 | 取值 | 用途 |
|------|------|------|
| Skill ID（`skill.json` / SKILL.md frontmatter） | `insentek-openapi` | 安装目录名、Agent 内部标识 |
| ClawHub slug | `insentek-api-skill` | `clawhub skill install <slug>` 时使用 |
| npm 包名 | `@insentek/openapi-skill` | **所有 `npx` 调用必须使用此名**（registry 上没有 `insentek-api-skill`） |
| CLI 二进制名 | `insentek-api-skill` | 仅在 `@insentek/openapi-skill` 已安装时作为可执行别名 |

### 3. 开始对话

```
User: 我的 appid 是 xxx，secret 是 yyy，查看所有设备
```

更多用法见 [`docs/getting-started.md`](docs/getting-started.md)。

---

## 项目结构

```
.
├── SKILL.md                     # 核心技能文件 (Runtime Contract)
├── skill.json                   # Skill manifest (id / version / runtime)
├── docs/
│   ├── getting-started.md       # 快速开始指南
│   ├── platform-setup.md        # 各平台配置指南
│   ├── interaction.md           # 交互规范 (意图/时间/输出格式)
│   └── analysis.md              # 分析策略 (报告/告警/行业参数)
├── reference/
│   └── api-doc.md               # 完整 API 文档 (OpenAPI v3.1.9)
├── examples/
│   ├── queries.md               # 查询类对话示例
│   ├── reports.md               # 报告生成示例
│   └── flows.md                 # 核心交互流程示例
├── scripts/                     # 参考实现脚本
│   ├── insentek_cli.py          # 统一 CLI（认证/查询/实时/导出）
│   ├── credential_store.py      # 加密凭据读写
│   ├── export_excel.py          # Excel 导出
│   ├── write_html.py            # HTML 报告落盘工具
│   └── README.md                # 脚本使用说明
└── packages/insentek-skill-cli/ # npm 包 @insentek/openapi-skill 源码
    ├── bin/                     # CLI 二进制入口
    ├── lib/                     # commander / inquirer 实现
    └── test/                    # node:test 测试
```

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 🔐 自动认证 | appid+secret → token，自动缓存与刷新 |
| 📋 设备管理 | 列表查询、别名解析、单设备详情 |
| 📊 数据查询 | 实时/历史/指定时刻/增量同步 |
| 🧠 智能推断 | 自然语言时间自动解析（"上周"→日期范围） |
| 🔗 链式调用 | alias → SN → 数据，自动串联 |
| 📈 趋势分析 | 平均值/最大值/最小值/变化率自动计算 |
| ⚖️ 跨设备对比 | 并排比较 + 差异高亮 |
| ⚠️ 异常检测 | 电池过低、水分异常、温度突变自动标记 |
| 🏭 多行业适配 | Z/T/J 设备类型自动识别与参数翻译 |
| 🎯 意图确认 | 输出形式不明确时自动询问（查看/导出/报告） |
| 🛡️ 查询边界 | 最大1年/3年回溯/5万条导出上限，超限自动拦截 |
| 📤 数据导出 | CSV / Excel / JSON / HTML 报告一键生成 |
| 🔍 环境检查 | 首次使用前自动检查 Python、脚本、依赖、API 可达性 |

---

## 对话示例

**查看设备列表**
```
User: 查看我的设备
Agent: 📋 设备列表（共 3 台）...
```

**查询实时数据**
```
User: 1号大棚现在的温度
Agent: 📍 1号大棚 — 10cm: 18.5℃, 20cm: 17.2℃ ...
```

**历史趋势**
```
User: 最近7天的土壤湿度变化
Agent: 📊 趋势表格 + 平均/最高/最低/变化率小结
```

**异常检测**
```
User: 检查所有设备的电池
Agent: 🔋 巡检报告 — 2号大棚 2.85V 🔴 过低
```

更多示例见 [`examples/`](examples/)。

---

## 时间表达支持

| 你说 | Agent 理解 |
|------|-----------|
| "现在" / "最新" / "实时" | 调用 /latest |
| "昨天" / "上周" / "本月" | 自动计算 YYYYMMDD,YYYYMMDD |
| "最近7天" / "近一周" | 过去 7 天 |
| "12点30分" / "某时刻" | 调用 /moment/{datetime} |
| "同步" / "增量" | 调用 /incremental |
| *(没提时间)* | 默认最近 24 小时 |

---

## 平台兼容性

| 特性 | OpenClaw | Claude Code | ChatGPT | Hermes-Agent |
|------|:--------:|:-----------:|:-------:|:------------:|
| Function Schema | ✅ | ✅ | ⚠️ Actions | ✅ |
| 自动 Token 刷新 | ✅ | ✅ | ⚠️ | ✅ |
| 别名解析 | ✅ | ✅ | ✅ | ✅ |
| 时间推断 | ✅ | ✅ | ✅ | ✅ |
| 链式调用 | ✅ | ✅ | ✅ | ✅ |

⚠️ = 需额外配置（详见 [`docs/platform-setup.md`](docs/platform-setup.md)）

---

## API 参考

- **Base URL**: `https://openapi.ecois.info`（如需指向自建/测试环境，设置 `INSENTEK_API_BASE` 环境变量）
- **认证**: `GET /v3/token?appid={appid}&secret={secret}`
- **设备**: `/v3/devices`, `/v3/device/{sn}`, `/v3/device/{sn}/description`
- **数据**: `/v3/device/{sn}/data`, `/latest`, `/moment/{datetime}`, `/incremental`

完整参数说明见 [`reference/api-doc.md`](reference/api-doc.md)。

---

## 版本

- **当前版本**: v1.2.2
- **API 版本**: insentek OpenAPI v3
- **更新日期**: 2026-05-26（见 [`CHANGELOG.md`](CHANGELOG.md)）

---

## 贡献

本项目为内容产出型项目，主要交付物为 `skill.md` 及配套文档。

如需反馈问题或建议：
1. 先在本机运行 `npx @insentek/openapi-skill doctor --json` 与 `python3 scripts/insentek_cli.py check` 收集环境信息
2. 提交 issue 到项目仓库，附上 doctor / check 的 JSON 输出

---

## 许可证

待定 / 请参考 insentek 官方使用条款

---

*Generated with Claude Code · 基于 insentek OpenAPI v3*
