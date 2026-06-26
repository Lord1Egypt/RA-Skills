---
name: mem0-memory-setup
description: >-
  为 Hermes Agent 配置 Mem0 外部记忆层。涵盖 pip install、npm CLI 安装、
  Agent Mode 注册、Hermes 集成、账号认领、验证、和国内网络/特殊 shell 的排错。
  使用场景：用户问"怎么给 Hermes 加记忆"、"装一下 mem0"、"配置外部记忆"、
  "memory provider"、"让 Hermes 记住我"。
---

# Mem0 记忆层配置指南

Mem0（"mem-zero"）是开源的 AI Agent 记忆层（Apache 2.0）。Hermes 内置 8 种记忆 provider，其中 Mem0 支持服务端自动事实提取 + 语义搜索 + 实体提权，一行命令接入。

**官方文档:** https://docs.mem0.ai
**Hermes 集成文档:** https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
**GitHub:** https://github.com/mem0ai/mem0

## 触发条件

- 用户说"配置记忆"、"装 mem0"、"memory provider"、"让 Hermes 记住我"
- `hermes memory status` 显示 provider 为 `built-in only`
- 需要跨会话持久记忆的场景

## 完整配置流程

### Step 1: 安装 Python 包

```bash
pip install mem0ai
```

**中国用户（镜像加速）：**

```bash
pip install mem0ai -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Step 1b: 验证 Python 库已正确安装

```bash
python3 -c "from mem0 import Memory; print('Mem0 lib OK')"
# → Mem0 lib OK
```

### Step 2: 安装 Mem0 CLI（获取 API Key）

Mem0 CLI (`@mem0/cli`) 用于注册 Agent Mode 账号和获取 API Key：

```bash
npm install -g @mem0/cli
```

**如果报 EACCES（权限错误）：**

npm 默认 prefix 是 `/usr`，普通用户没有写入权限。**不要用 sudo**，改为用户目录：

```bash
# 检查当前 prefix
npm config get prefix   # 很可能返回 /usr

# 设为用户目录（只需一次，永久生效）
npm config set prefix ~/.npm-global

# 重新安装
npm install -g @mem0/cli
```

> **重要：保持 prefix 为 `~/.npm-global`，不要改回 `/usr`。** 这条设定对所有 npm 全局包（mmx-cli、@mem0/cli 等）都生效，改完后所有 `npm install -g` 都不再需要 sudo。永久解决 EACCES 问题。

#### PATH 问题（fish / zsh 等非 bash shell）

CLI 装在 `~/.npm-global/bin/mem0`。bash 通过 `.bashrc` 加 PATH：

```bash
export PATH="$HOME/.npm-global/bin:$PATH"
```

**fish shell（通过 `.bashrc` 启动 fish）：** 如果 `.bashrc` 中有上面这行，fish 会继承继承过来的 PATH。验证用：

```fish
type mem0
# → mem0 is /home/po/.npm-global/bin/mem0
```

如果找不到，在 `~/.config/fish/config.fish` 添加：

```fish
fish_add_path ~/.npm-global/bin
```

### Step 3: Agent Mode 注册（无邮箱）

AI Agent 可以直接注册，无需人类邮箱：

```bash
mem0 init --agent --agent-caller hermes
```

说明：
- `--agent-caller hermes` — 告诉 Mem0 这是 Hermes Agent
- 注册后在 `~/.mem0/config.json` 保存 API Key
- 此账号**未认领**，30 天内可认领到人类邮箱

### Step 4: 读取 API Key

```bash
python3 -c "import json; print(json.load(open('/home/po/.mem0/config.json'))['platform']['api_key'])"
```

或直接查看：`cat ~/.mem0/config.json`

### Step 5: 配置 Hermes

写入 API Key 到 `.env`：

```bash
MEM0_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.mem0/config.json'))['platform']['api_key'])")
echo "export MEM0_API_KEY=$MEM0_KEY" >> ~/.hermes/.env
```

设置 provider：

```bash
hermes config set memory.provider mem0
```

### Step 6: 验证

```bash
hermes memory status
# → Plugin: installed ✓
# → Status: available ✓
# → Provider: mem0 ← active
```

### Step 7: 测试写入和检索

```bash
mem0 add "Test memory: user prefers concise responses"
mem0 search "prefers concise"
# → Found 1 memories:
# → User prefers concise responses in conversations
# → Score: 0.34
```

### Step 8: 账号认领（可选但推荐）

让人类用户认领 Agent 账号，获得 Web 面板和管理权限：

```bash
mem0 init --email <your-email>
# 输入邮箱验证码即可
# API Key 不变，所有记忆数据保留
```

认领后可在 [app.mem0.ai](https://app.mem0.ai) 查看记忆数据和管理面板。

## Hermes 集成后行为

| 时机 | 行为 |
|------|------|
| 每轮对话前 | Mem0 预取相关记忆注入 system prompt（零延迟，后台完成） |
| 每轮回复后 | Mem0 自动提取事实并存储（后台线程，不阻塞对话） |
| 会话结束时 | 服务端处理存储优化和去重 |
| Circuit breaker | 连续 5 次失败后暂停 2 分钟，Agent 继续工作不受影响 |

### 可用工具

启用 Mem0 后，Hermes 额外获得 3 个工具（自动调用，无需手动触发）：

| 工具 | 功能 |
|------|------|
| `mem0_profile` | 获取所有已存储的用户记忆 |
| `mem0_search` | 语义搜索（支持 rerank + top_k 过滤） |
| `mem0_conclude` | 手动存储一条事实（不走服务端提取） |

## 内置记忆 vs Mem0

内置记忆（memory/user 工具）始终并行运行，不受影响：

```
内置记忆:   MEMORY.md + USER.md 文件 → 2 个分区，各 2200 字符上限
Mem0:       云端语义向量库 → 无大小限制，支持语义搜索 + 自动提取
```

两者互补：内置记忆存**静态事实**（项目路径、设备参数、偏好），Mem0 存**动态学习**（用户习惯、工作模式、历史偏好变化）。

## 已知问题与排错

### 1. 国内网络

- **pip install 超时**: 用清华镜像 `-i https://pypi.tuna.tsinghua.edu.cn/simple`
- **npm install 正常**: npm 镜像通常够快
- **Mem0 Cloud API (api.mem0.ai) 延迟**: 国内访问约 0.5-1.5s 延迟，Hermes 用后台预取 + 缓存屏蔽了感知延迟
- **自托管选项**: Mem0 支持 Docker 自部署，见 [Self-hosted docs](https://docs.mem0.ai/open-source/overview)

### 2. `mem0` 命令找不到

```bash
# 检查安装位置
ls ~/.npm-global/bin/mem0
ls /usr/lib/node_modules/.bin/mem0

# 加 PATH
export PATH="$HOME/.npm-global/bin:$PATH"
```

### 3. Hermes memory status 显示 not available

检查以下 env var 是否已设置：

```bash
grep MEM0_API_KEY ~/.hermes/.env
```

### 4. npm 全局安装报 EACCES

npm 默认 prefix 为 `/usr`，普通用户无写入权限。解法：

```bash
npm config set prefix ~/.npm-global
# 之后安装无需 sudo
```

### 5. fish shell 下 which 找不到

fish 没有 `which` 命令。用内置的 `type` 代替：

```fish
type mem0
# → mem0 is /home/po/.npm-global/bin/mem0
```

### 6. 写入记忆时被安全模块拦截

向 `memory` 工具写入 `.env` 路径、API Key 明文等敏感信息会触发安全模式 `hermes_env` 导致写入被拒绝。不要在 memory 条目中包含 `.env`、`api_key`、`token`、`secret` 等字样的路径或值。

解法：将敏感配置步骤写在 SKILL.md 中（不注入 system prompt），只在 memory 中记录无风险的事实（如 "Mem0 已配置"、"provider: mem0" 等摘要）。
