# Codex 接入聚星逸 · OpenClaw Skill

> 安装 Codex → 接入聚星逸网关 → Agent 感知 Codex 工作

## 快速开始

```bash
# 1. 安装 Codex
bash scripts/install.sh

# 2. 配置聚星逸接入（交互式）
bash scripts/configure.sh

# 3. Agent 感知 Codex 工作
bash scripts/codex-context.sh
```

## 复用到其他 OpenClaw

本 skill **不硬编码任何用户私有信息**，其他 OpenClaw 实例可直接复用：

### 方式 1：直接复制

```bash
cp -r skills/codex-juxingyi-setup /目标路径/
cd /目标路径/codex-juxingyi-setup
bash scripts/install.sh
bash scripts/configure.sh
```

### 方式 2：自定义网关

如果用自建网关而非聚星逸：

```bash
export JUXINGYI_API_BASE="https://your-gateway.example.com/v1"
export JUXINGYI_API_KEY="your-api-key"
export JUXINGYI_MODEL="your-model"
bash scripts/configure.sh
```

### 方式 3：非交互式（CI/自动化）

```bash
JUXINGYI_API_KEY="fsk-xxx" JUXINGYI_MODEL="deepseek-v4-flash" \
  bash scripts/install.sh && \
  bash scripts/configure.sh
```

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `JUXINGYI_API_BASE` | `https://fireworks-simulator-api.huo15.com/v1` | 网关地址 |
| `JUXINGYI_API_KEY` | (交互输入) | API Key |
| `JUXINGYI_MODEL` | (交互选择) | 模型名 |
| `CODEX_HOME` | `~/.codex` | Codex 配置目录 |

## 依赖

- `bash` 4.0+
- `jq`（`brew install jq`）
- `curl`（macOS 自带）
- `npm`（安装 Codex CLI 用）

## 文件结构

```
codex-juxingyi-setup/
├── SKILL.md                  # Skill 定义（AI Agent 读取入口）
├── README.md                 # 本文档
├── scripts/
│   ├── install.sh            # 安装 Codex/ChatGPT
│   ├── configure.sh          # 配置聚星逸接入
│   ├── codex-status.sh       # 查看 Codex 当前状态
│   ├── codex-sessions.sh     # 列出/查看会话历史
│   └── codex-context.sh      # 聚合全部上下文
└── docs/
    └── design.md             # 设计文档
```

## Agent 感知能力

运行 `codex-context.sh` 后，Agent 可获得：

1. **配置信息**：当前模型、provider、网关地址
2. **安装状态**：ChatGPT 桌面版/Codex CLI 版本
3. **活跃项目**：Codex 正在操作的项目目录列表
4. **会话列表**：最近 N 条会话的标题、ID、时间
5. **会话内容摘要**：用户消息、Codex 回复、工具调用统计
6. **网关连通性**：当前网关是否可达
