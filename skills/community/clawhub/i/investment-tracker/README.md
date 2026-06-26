# 值·录 — 投资记录本

对接了openclaw的skills，将investment-tracker-skill文件夹拖放到~/.openclaw/extensions文件夹中即可激活这个技能。现在将你的持仓截图上传给你的小龙🦞让它帮你进行管理吧！

值·录是一款面向个人投资者的本地化投资组合管理工具，包含一个完整的数据看板，对接了claude skill，支持持仓管理、收益曲线、投资日志，以及通过 AI 视觉模型自动识别券商截图并导入持仓数据。

访问https://github.com/20czy/investment-tracker-app.git安装项目的完整后端！

---

## 推荐使用方法

- 让小龙虾🦞设定一个每日的定时任务提醒你上传当日的持仓截图
- 将持仓截图存放在一个固定的文件夹里面让小龙虾🦞自己从这个文件夹导入！

## 功能介绍

### 持仓总览

- 汇总展示总市值、现金余额、持仓占比、浮动盈亏等关键指标
- 按板块或个股维度查看资产分配饼图
- 持仓表格支持查看每笔仓位的成本价、现价、市值、盈亏

### 收益曲线

- 记录并可视化个人账户权益曲线（支持自定义录入数据点）
- 显示总收益率、最大回撤等统计指标
- 内置沪深 300 基准对比图（通过 yfinance 实时拉取），支持展示 180 天与近 30 天两个时间维度

### 投资日志

- 以日记形式记录每笔交易或市场观察
- 支持设置记录类型（买入 / 卖出 / 观察 / 复盘）、关联股票代码、心情与备注
- 日志按时间倒序展示

### 截图导入（AI 识别）

- 支持拖拽或点击上传券商 App 持仓截图
- 调用 AI 视觉模型自动识别截图中的股票代码、名称、持股数量、成本价等字段
- 识别结果与当前持仓逐行对比，以差异表格呈现，可勾选确认后批量更新
- 每次导入前自动保存快照，支持回滚到任意历史版本

## 环境准备

### 运行时要求

| 依赖 | 最低版本 |
|------|---------|
| Node.js | 18+ |
| Python | 3.9+ |

### AI API Key

截图识别功能需要一个支持**视觉（Vision）能力**的 OpenAI 兼容 API Key。推荐以下服务：

| 服务 | 控制台地址 | 推荐模型 |
|------|-----------|---------|
| 阿里云百炼 | https://bailian.console.aliyun.com/ | `qwen3.5-plus` |
| OpenAI | https://platform.openai.com/api-keys 
| Moonshot | https://platform.moonshot.cn/ 

---

## 快速启动（推荐）

项目提供一键启动脚本，**首次运行**会自动完成以下操作：

1. 进入配置向导，引导填写 API Key、接口地址、模型名称
2. 在项目上一级目录创建 Python 虚拟环境（`../.venv/`）
3. 安装后端 Python 依赖
4. 在后台启动 FastAPI 后端（端口 `8000`）
5. 安装前端 npm 依赖
6. 在前台启动 Vite 开发服务器（端口 `5173`）

```bash
# 方式一：通过 npm
npm start

# 方式二：直接执行脚本
bash start.sh
```

启动成功后，在浏览器打开：

- **前端应用**：http://localhost:5173
- **后端 API 文档**：http://localhost:8000/docs

按 `Ctrl+C` 可同时停止前端和后端。

---

## 手动启动

如需分别启动前后端（例如调试时），按以下步骤操作。

### 1. 配置环境变量

```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env，填写 DASHSCOPE_API_KEY 等配置
```

### 2. 启动后端

```bash
# 创建并激活虚拟环境（仅首次需要）
python3 -m venv ../.venv
source ../.venv/bin/activate

# 安装依赖（仅首次或依赖变更时需要）
pip install -r backend/requirements.txt

# 启动后端服务
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端

在另一个终端窗口中执行：

```bash
# 安装依赖（仅首次需要）
npm install

# 启动前端开发服务器
npm run dev
```

---

## 环境变量配置

配置文件位于 `backend/.env`，以 `backend/.env.example` 为模板：

```env
DASHSCOPE_API_KEY=sk-your-key-here
AI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_MODEL=qwen-vl-plus
```

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | AI 服务的 API Key（**必填**） | — |
| `AI_BASE_URL` | OpenAI 兼容接口的 Base URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `AI_MODEL` | 使用的模型名称 | `qwen-vl-plus` |

---

## API 接口一览

后端运行后可在 http://localhost:8000/docs 查看完整的交互式文档。

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/holdings` | 获取当前全部持仓 |
| `POST` | `/api/holdings/bulk` | 批量替换持仓（原子操作，自动存快照） |
| `GET` | `/api/diary` | 获取投资日志列表 |
| `POST` | `/api/diary` | 新增日志记录 |
| `GET` | `/api/curve` | 获取权益曲线数据点 |
| `POST` | `/api/curve/point` | 新增 / 更新权益曲线数据点 |
| `GET` | `/api/cash` | 获取现金余额 |
| `POST` | `/api/cash` | 更新现金余额 |
| `GET` | `/api/hs300` | 获取沪深 300 历史收盘价 |
| `POST` | `/api/analyze` | 用 AI 分析 Base64 截图并返回持仓数据 |
| `POST` | `/api/external/upload` | 上传截图文件 → AI 识别 → 计算与当前持仓的差异 |
| `GET` | `/api/imports` | 获取全部导入历史快照 |
| `POST` | `/api/imports/rollback/{id}` | 回滚到指定历史快照 |
| `DELETE` | `/api/imports/{id}` | 删除历史快照 |
| `DELETE` | `/api/reset?confirm=true` | **危险**：清空所有数据 |

---

## 注意事项

**端口占用**
> 后端默认占用 `8000`，前端占用 `5173`。若这两个端口已被其他程序使用，启动会失败。可修改 `start.sh` 中的 `--port 8000` 以及 `vite.config.ts` 中的 `server.port` 来更换端口。

**AI API Key 为必填项（截图功能）**
> 未配置有效 API Key 时，截图上传界面会返回错误。其他功能（持仓管理、日志、收益曲线）无需 API Key，正常可用。

**视觉模型要求**
> 截图识别要求所选模型具备**多模态视觉能力**。纯文本模型（如 `deepseek-chat`、`qwen-turbo`）不支持图片输入，配置后截图识别将报错。

**yfinance**
> 收益曲线的沪深 300 基准数据通过 Yahoo Finance 获取，在中国大陆网络环境下可能需要代理才能正常拉取。若无法访问，基准对比图将无法显示，但不影响其他功能。

**数据库文件**
> 所有数据存储在 `backend/investment.db`（SQLite 本地文件）。该文件不会被提交到 Git，请自行备份。删除此文件等同于清空所有数据。

**危险操作：`/api/reset`**
> `DELETE /api/reset?confirm=true` 会不可恢复地清除数据库中的所有持仓、日志、曲线和现金数据，请勿误操作。

**Python 虚拟环境位置**
> 一键启动脚本会将虚拟环境创建在项目目录的**上一级**（`../.venv/`），而非项目内部，避免被 Vite / TypeScript 扫描到。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 19 + TypeScript + Vite 7 |
| 图表 | Recharts 3 |
| 后端 | Python / FastAPI + Uvicorn |
| 数据库 | SQLite（本地文件，无需额外安装） |
| AI 接口 | OpenAI Python SDK（兼容任何 OpenAI 格式的 API） |
| 行情数据 | yfinance（拉取沪深 300 历史数据） |

---

---

## 目录结构

```
invest-tracker-app/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── start.sh                    # 一键启动脚本
├── src/
│   ├── main.tsx                # React 入口
│   ├── App.tsx                 # 根组件
│   ├── InvestmentTracker.tsx   # 主界面（全部前端逻辑）
│   └── index.css
├── backend/
│   ├── main.py                 # FastAPI 后端（全部路由）
│   ├── prompts.py              # AI 分析提示词
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example            # 环境变量模板
│   └── investment.db           # SQLite 数据库（运行时生成）
└── investment-tracker-skill/
    ├── SKILL.md                # AI Agent 技能描述文件
    └── references/
        └── api-docs.md         # API 快速参考
```
