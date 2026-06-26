---
name: inquiry-analyzer
description: 阿里巴巴询盘分析技能 - 分析指定时间窗口内的询盘数据，提取产品分类、客户信息、国家等关键字段，生成结构化报告。当用户需要分析阿里巴巴询盘、生成询盘报告、运行询盘分析时使用。
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# 阿里巴巴询盘分析技能

分析阿里巴巴国际站询盘数据，提取产品分类、客户信息、国家等关键字段，生成结构化 Markdown 和 CSV 报告。

## 安装配置

### 环境变量（可选）

skill 目录是自包含的，无需配置即可运行。如需指定外部路径，可设置环境变量：

```bash
# Windows
set INQUIRY_ANALYZER_PATH=E:\OpenClaw\inquiry-analyzer

# Linux/macOS
export INQUIRY_ANALYZER_PATH=/path/to/inquiry-analyzer
```

### 目录结构（自包含模式）

```
inquiry-analyzer-skill/
├── SKILL.md                    # 本文档
├── lib/                        # 核心库文件
│   ├── inquiry-analyzer.js         # 询盘分析主脚本
│   ├── okki-background.js          # OKKI 背调分析脚本
│   ├── product-groups.js           # 产品分组动态获取模块
│   └── product-mapping.js          # 产品分组配置向导模块
├── reports/                    # MD 报告输出（运行时创建）
├── csv-reports/                # CSV 报告输出（运行时创建）
├── okki-reports/               # OKKI 背调报告输出（运行时创建）
└── scripts/                    # 入口脚本
    ├── run-analysis.js         # 询盘分析入口
    ├── run-okki.js             # OKKI 背调入口
    └── merge-reports.js        # 报告合并入口
```

**自包含说明：** skill 目录包含所有必需文件，无需外部依赖即可运行。

### 路径查找机制

入口脚本按以下顺序查找主脚本：

1. **自包含模式** — 上级目录的 `lib/` 文件夹
2. **环境变量** `INQUIRY_ANALYZER_PATH`
3. **常见位置** — `E:\OpenClaw\inquiry-analyzer`、用户目录等

## 前提条件

### 1. 启动 OpenClaw 浏览器

**步骤 1：查看可用浏览器配置文件**
```bash
openclaw browser profiles
```

**结果示例：**
```
openclaw: stopped
  port: 18800, color: #FF4500  ← 专用浏览器
chrome: running (0 tabs) [default]
  port: 18792, color: #00AA00   ← Chrome 扩展模式
```

**步骤 2：启动专用浏览器**
```bash
openclaw browser start --browser-profile openclaw
```

**步骤 3：确认浏览器状态**
```bash
openclaw browser status --browser-profile openclaw
```

关键字段：
- `running: true` — 浏览器已启动
- `cdpPort: 18800` — CDP 端口号
- `cdpUrl: http://127.0.0.1:18800` — 连接地址

### 2. 登录阿里巴巴

在 OpenClaw 浏览器中登录阿里巴巴账号，确保登录状态有效。

### 3. 常用命令速查

| 命令 | 说明 |
|------|------|
| `openclaw browser profiles` | 查看所有配置文件及端口 |
| `openclaw browser start --browser-profile openclaw` | 启动专用浏览器 |
| `openclaw browser status --browser-profile openclaw` | 查看浏览器状态 |
| `openclaw browser stop --browser-profile openclaw` | 停止浏览器 |
| `openclaw browser tabs --browser-profile openclaw` | 查看当前标签页 |

### 4. 故障排除

**问题 1：Chrome 扩展模式连接失败**
```
Chrome extension relay is running, but no tab is connected.
```
解决方案：改用专用浏览器模式
```bash
openclaw browser start --browser-profile openclaw
```

**问题 2：Gateway 超时**
```
Error: gateway timeout after 1500ms
```
解决方案：启动 Gateway
```bash
openclaw gateway --force
```

**问题 3：端口被占用**
```bash
openclaw browser stop --browser-profile openclaw
openclaw browser start --browser-profile openclaw
```

**问题 4：找不到主脚本**
```
错误: 无法找到 inquiry-analyzer.js
```
解决方案：设置环境变量 `INQUIRY_ANALYZER_PATH` 指向 `inquiry-analyzer` 目录

## 使用方法

### 询盘分析

```bash
# 基本用法：分析指定询盘单号
node run-analysis.js <询盘单号>

# 指定时间窗口
node run-analysis.js <询盘单号> <开始时间> <结束时间>

# 示例
node run-analysis.js 50000126101155
node run-analysis.js 50000126101155 "2026-03-26T15:00:00" "2026-03-27T15:00:00"
```

### OKKI 背调分析

```bash
# 基本用法：对指定询盘进行背调分析
node run-okki.js <询盘单号>

# 指定时间窗口
node run-okki.js <询盘单号> <开始时间> <结束时间>

# 示例
node run-okki.js 50000126101155
node run-okki.js 50000126101155 "2026-03-26T15:00:00" "2026-03-27T15:00:00"
```

### 合并报告

```bash
# 将询盘报告和OKKI背调报告合并
node merge-reports.js <询盘单号>

# 示例
node merge-reports.js 50000126101155
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 询盘单号 | 目标询盘的ID，分析该询盘及以上所有询盘 | 50000126101155 |
| 开始时间 | 时间窗口开始（可选） | "2026-03-26T15:00:00" |
| 结束时间 | 时间窗口结束（可选） | "2026-03-27T15:00:00" |

## 输出文件

### 询盘分析输出

| 文件 | 位置 | 说明 |
|------|------|------|
| MD报告 | reports/inquiry-report-*.md | Markdown 格式的询盘分析报告 |
| CSV报告 | csv-reports/inquiry-report-*.csv | Excel 友好的 CSV 格式报告 |
| 聊天记录 | chats/inquiry-*.txt | 原始聊天记录文本 |

### OKKI 背调输出

| 文件 | 位置 | 说明 |
|------|------|------|
| MD报告 | okki-reports/okki-report-*.md | Markdown 格式的背调报告 |
| CSV报告 | okki-reports/okki-report-*.csv | Excel 友好的 CSV 格式报告 |

### 合并报告输出

| 文件 | 位置 | 说明 |
|------|------|------|
| MD报告 | reports/merged-report-*.md | 合并后的完整报告 |
| CSV报告 | csv-reports/merged-report-*.csv | Excel 友好的 CSV 格式 |

## 报告字段

| 字段 | 说明 |
|------|------|
| 询盘单号 | 询盘唯一标识 |
| 月份 | 登记月份 |
| 登记日期 | 询盘日期 |
| 询盘回复人 | 业务员姓名 |
| 产品型号 | 产品分类（厨房橱柜/工具柜/户外厨房等） |
| 时间段 | 询盘时间 |
| 客户类型 | 有效客户/已读未回/未读未回 |
| 国家 | 客户所在国家 |
| 客户名称 | 客户姓名或公司名 |
| L几 | 客户等级（L0-L4） |

## 产品分类

系统支持**动态产品分类**，自动从阿里巴巴产品管理页面获取您的产品分组列表：

### 分类流程

1. **缓存优先** — 使用本地缓存（7天有效）
2. **动态获取** — 从产品管理页面抓取所有分组名
3. **智能匹配** — 标题关键词 → 分组名匹配 → 产品类型
4. **搜索兜底** — 未命中时搜索产品分组页面

### 分类来源

| 来源 | 优先级 | 说明 |
|------|--------|------|
| 关键词匹配 | 1 | 内置产品关键词库 |
| 动态分组列表 | 2 | 从产品管理页面获取 |
| 产品搜索 | 3 | 在产品管理页面搜索标题 |
| 聊天内容分析 | 4 | 从聊天记录提取产品关键词 |

### 缓存文件

| 文件 | 说明 |
|------|------|
| `product-groups-cache.json` | 产品分组列表缓存（7天有效） |
| `product-mapping.json` | 用户自定义分组→产品类型映射 |
| `title-cache.json` | 标题分类缓存（每次运行清除） |
| `chat-products.json` | 聊天内容产品映射（可手动编辑） |

### 首次运行配置

首次运行时，系统会自动检测产品分组并为每个分组分配建议的产品类型：

```
[自动配置] 正在为分组分配建议类型...
  Stainless Steel Kitchen Cabinet → 厨房橱柜
  Outdoor Kitchen Shed → 箱体户外厨房
  Tool Cabinet → 工具柜
  ...
[配置] 已保存映射到 product-mapping.json
```

如需自定义映射，可编辑 `product-mapping.json`：

```json
{
  "version": "1.0",
  "updatedAt": "2026-03-31T00:00:00.000Z",
  "mapping": {
    "Stainless Steel Kitchen Cabinet": "厨房橱柜",
    "Outdoor Kitchen Shed": "箱体户外厨房",
    "Tool Cabinet": "工具柜"
  }
}
```

### 自定义分类

如需自定义产品分类映射，可编辑以下文件：

```bash
# 编辑用户自定义映射
# 格式：{ "分组名": "产品类型" }
notepad product-mapping.json

# 清除分组缓存（强制重新获取）
del product-groups-cache.json

# 清除映射配置（重新自动配置）
del product-mapping.json
```

## 安全说明

### child_process 使用声明

入口脚本使用 `child_process.spawn` 启动 Node.js 进程运行分析器：

- **用途**：隔离运行环境、传递命令行参数
- **安全性**：仅调用本地已知脚本，不执行任意命令
- **替代方案**：直接运行主脚本也可（需在正确目录下）

### Relay Token 配置

Relay Token 在主脚本中配置（`inquiry-analyzer.js`、`okki-background.js`），建议：

1. 生产环境使用环境变量覆盖
2. 不要在公开仓库中提交真实 Token

## 注意事项

1. **浏览器要求**：必须使用 OpenClaw 浏览器，禁止使用 Puppeteer/Playwright 直接启动浏览器（会触发阿里巴巴反爬）
2. **登录状态**：运行前确保已在阿里巴巴登录
3. **文件清理**：系统自动清理旧文件，每个目录只保留最近 10 个文件
