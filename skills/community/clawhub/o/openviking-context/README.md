# OpenViking Context Database — OpenClaw Skill

L0/L1/L2 分层上下文加载，token 消耗降低 83-96%。

## 这个 Skill 做什么

基于字节跳动开源的 [OpenViking](https://github.com/volcengine/OpenViking) 上下文数据库，为 OpenClaw Agent 提供：

- **分层加载** — L0 摘要(~100 tokens) → L1 概览(~2k tokens) → L2 全文，按需逐层深入
- **语义检索** — 向量匹配 + 目录递归，精准定位相关上下文
- **会话记忆** — 自动提取长期记忆，Agent 越用越聪明
- **Token 追踪** — 每次操作实时展示节省了多少 token

## 安装

### 方式 1：从 ClawHub 安装

```bash
clawhub install openviking-context
```

### 方式 2：从源码安装

```bash
git clone https://github.com/guoweisheng/openviking-skill.git
cd openviking-skill
bash scripts/install-skill.sh
```

安装脚本自动检测本机 npm 安装 / Docker 安装路径。也可手动指定：

```bash
OPENCLAW_SKILLS_DIR=/your/path bash scripts/install-skill.sh
```

### 安装 OpenViking 依赖

```bash
bash scripts/install.sh      # 安装 openviking Python 包
bash scripts/setup-config.sh  # 交互式配置 API Key 和模型
openviking-server             # 启动服务
```

## 环境要求

| 依赖 | 版本 |
|---|---|
| Python | >= 3.10 |
| openviking (pip) | latest |
| OpenClaw | 2026.3+ |

需要配置一个模型提供商的 API Key（支持 OpenAI / 火山引擎 / NVIDIA NIM / LiteLLM）。

## 使用方式

在 OpenClaw 中直接对话即可触发，例如：

- "帮我用 openviking 搜索认证相关的文档"
- "查看 openviking 的 token 消耗统计"
- "把这个项目的文档导入 openviking"

也可以通过命令行使用：

```bash
# 添加资源
python3 scripts/viking.py add ./my-project-docs/

# 语义搜索（L0 摘要级别）
python3 scripts/viking.py search "用户认证"

# L1 概览
python3 scripts/viking.py overview viking://resources/auth-docs

# L2 全文（仅在需要时）
python3 scripts/viking.py read viking://resources/auth-docs/jwt-config.md

# 查看 token 消耗统计
python3 scripts/viking.py stats
```

## Token 节省效果

每次操作自动追踪并输出：

```
📊 会话累计 | 实际: 2,300 tokens | 全量: 48,000 tokens | 节省: 45,700 (95.2%)
```

`stats` 命令展示完整明细：

```
═══ Token 消耗统计 ═══
  ┌─────────────────────────────────────┐
  │  全量加载 (传统方式):     74,200 tokens │
  │  实际消耗 (分层加载):      5,380 tokens │
  │  节省 token 数量:        68,820 tokens │
  │  节省比例:                  92.8%        │
  └─────────────────────────────────────┘
```

## 目录结构

```
openviking-context/
├── SKILL.md                  # OpenClaw skill 入口
├── clawhub.json              # ClawHub 元数据
├── README.md                 # 本文件
└── scripts/
    ├── install-skill.sh      # 一键安装到 OpenClaw（本机/Docker）
    ├── install.sh            # 安装 OpenViking 依赖
    ├── setup-config.sh       # 交互式配置向导
    ├── viking.py             # CLI wrapper + token 追踪
    └── demo-token-compare.py # Token 对比演示
```

## 参考

- [OpenViking GitHub](https://github.com/volcengine/OpenViking)
- [OpenViking 官网](https://www.openviking.ai)
- [OpenClaw 技能文档](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub](https://clawhub.ai)
