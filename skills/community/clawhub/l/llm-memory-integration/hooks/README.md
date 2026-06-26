# Hooks 说明

本目录包含生命周期钩子，用于在安装时自动配置私有内容。

## 钩子列表

| 钩子 | 触发时机 | 功能 |
|------|---------|------|
| `bootstrap-extra-files.py` | postinstall | 将本地私有配置链接到工作区 |

## 安全说明

- ✅ **无网络访问**：钩子不执行任何网络操作
- ✅ **无敏感信息**：钩子只读取环境变量，不包含任何密钥或地址
- ✅ **无远程拉取**：钩子只操作本地文件系统
- ✅ **用户可控**：用户完全控制私有目录的位置和内容

## 使用方法

### 1. 准备私有配置目录

```bash
mkdir -p ~/my-private-config
# 将你的私有文件放入此目录
```

### 2. 设置环境变量

```bash
# 临时设置（当前会话）
export CNB_PRIVATE_WORKSPACE="~/my-private-config"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export CNB_PRIVATE_WORKSPACE="$HOME/my-private-config"' >> ~/.bashrc
```

### 3. 安装技能

```bash
clawhub install llm-memory-integration
```

安装后，钩子会自动将 `CNB_PRIVATE_WORKSPACE` 目录下的文件链接到技能工作区。

## 私有目录结构示例

```
~/my-private-config/
├── AGENTS.md          # 自定义 Agent 规则
├── TOOLS.md           # 自定义工具配置
├── MEMORY.md          # 私有记忆文件
└── config/            # 自定义配置目录
    └── llm_config.json
```

## 禁用钩子

如果不需要私有配置，可以跳过钩子：

```bash
clawhub install llm-memory-integration --no-hooks
```
