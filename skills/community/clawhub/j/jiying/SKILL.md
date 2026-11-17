---
name: 稽影 · 多Agent信任基础设施
version: 0.4.0
description: 信任不是功能——信任是产品。6-Agent编排·宪法即代码·TEP可信执行协议·Ed25519。Apache 2.0开源。
license: Apache-2.0
disable: false
---

# 稽影 (Jiying) · 多Agent信任基础设施

> 稽察审视，追影溯源 — 让每一次AI执行都变得可验证

## 概述

稽影是一个带价值宪法的多 Agent 知识工作编排系统。你输入一个意图，多个 AI Agent 协作完成——同时三条宪法确保你始终是决策者。

```
用户意图 → Planner → Researcher → Creator → Reviewer → 质量门禁 → 导出
              ↑          ↑          ↑          ↑
          宪法系统    守护进程    审计系统    演化引擎
```

## 快速开始

```bash
# 安装
npx clawhub install jiying

# 启动服务端
cd jiying && node server/index.js

# 或开发模式（含前端 UI）
git clone https://github.com/Vane1981-2011/jiying.git
cd jiying
npm install
npm run dev
```

打开 http://localhost:5173 → 配置 DeepSeek API Key → 输入意图 → 点"开始"

## 核心能力

### ⚖️ 宪法即代码
三条哲学规则直接编译为可执行函数：
- **尊严（康德）**: AI 必须在前 25% 位置声明身份 → 未声明则 **阻断**
- **自主（马尔库塞）**: 每次输出 ≥2 个真正不同的替代方案 → 不足则 **警告**
- **追问（海德格尔）**: 必须声明具体可质疑的前提假设 → 缺失则 **警告**

### 🔗 TEP v1.0 可信执行协议
Agent 间信任验证开放标准。8 组件信封（任务·授权·执行档案·策略决策·行动收据·证据包·质量证明·审计签名），Ed25519 非对称签名。

### 🛡️ 7 项预检门禁
对标 Hermes：宪法状态→Agent 参与→覆盖率≥60%→占位符检测→评分≥3→假设完整→去重(Jaccard>85%)

### 🧠 10 种认知偏见交叉验证
Critic + Defender 双 prompt 架构。检测确认偏误、锚定效应、可得性启发、框架效应、过度自信、群体思维、沉没成本、近期偏差、归因错误、现状偏误。

### 📊 不确定性预算
6 源加权量化（数据/模型/知识/假设/推理/环境）+ 3 级阈值（LOW/MEDIUM/HIGH）+ 自动行动（验证/复审/拒绝）

## 命令参考

| 命令 | 说明 |
|:-----|:-----|
| `npm run dev` | 启动开发服务器 (Vite + React) |
| `npm run dev:electron` | 启动 Electron 桌面应用 |
| `npm test` | 运行全部 179 个测试 |
| `npm run build` | 生产构建 |
| `npm run lint` | 运行 oxlint 静态检查 |
| `node server/index.js` | 启动服务端内核 (端口 3456) |

## API 端点

| 端点 | 方法 | 说明 |
|:-----|:----:|:-----|
| `/health` | GET | 健康检查 |
| `/api/constitution/check` | POST | 宪法检查 `{ text: string }` |
| `/api/quality/review` | POST | 质量门禁审查 |
| `/api/audit/log` | GET/POST | 审计日志查询/写入 |

## 架构

```
src/
├── constitution/    # 规则引擎 + 三条宪法 + Shell 权限 + 语义验证器(L2)
├── guardian/        # 5 项后台守护监控
├── agents/          # 6 Agent + 注册表 + 技能系统
├── orchestrator/    # 编排引擎（并行+断点恢复）
├── quality/         # 7 项门禁 + 魔鬼代言人 + 伦理 + 演化
├── tep/             # TEP 可信执行协议
├── context/         # Token 预算 Context Builder
├── knowledge/       # TF-IDF 向量 RAG
├── audit/           # 代偿审计收集器
├── store/           # Zustand 状态管理 (5 Store)
├── pages/           # 6 个页面
├── components/      # 布局 + Markdown + 错误边界
└── utils/           # Fallback 链 + 重试 + 导出
```

## 技术栈

`React 19` · `Vite 8` · `Zustand` · `Vercel AI SDK` · `DeepSeek` · `Electron` · `Express` · `@noble/ed25519` · `Vitest`

## 故障排除

| 问题 | 解决 |
|:-----|:-----|
| API Key 不生效 | 检查设置页面 → 确认 Key 格式 → 刷新页面 |
| Agent 卡住不动 | 检查浏览器控制台 → 确认网络连接 → 重启 `npm run dev` |
| 宪法不阻断 | 确认 `constitution/rules.js` 中的 RULES 已加载 → 检查 L1 正则是否匹配 |
| 服务端启动失败 | 确认端口 3456 未被占用 → `lsof -i :3456` |
| 测试失败 | `npm test` 查看具体失败项 → 确认 Node.js ≥ 18 |

## 性能提示

- L2 语义验证器有 5 分钟缓存，相同内容不重复调用 LLM
- 开发环境可关闭 L2（`{ enabled: false }`）以节省 API 成本
- 服务端审计日志上限 1000 条，超出自动滚动

## 链接

- GitHub: https://github.com/Vane1981-2011/jiying
- 作品展示: https://vane1981-2011.github.io/jiying/portfolio/
- ClawHub: https://clawhub.ai/vane1981/skills/jiying
- 复核报告: https://vane1981-2011.github.io/jiying/portfolio/稽影系列_参赛作品_复核报告.md

## 许可

Apache 2.0 · © 2026 Vane1981
