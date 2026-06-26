---
name: my_stock_tradeagents_rebuild_skill
description: 当且仅当用户明确提出“重新构建tradeagents”或类似高度相关指令时触发。主要功能为在 ~/TradingAgents 目录下重新创建并激活 Python 虚拟环境，安装包及依赖，最后总结修改并推送到远程仓库。
---

# my_stock_tradeagents_rebuild_skill (重建 TradingAgents 环境技能)

## 核心规则与触发条件
- **触发条件**：只有当用户明确说出“重新构建tradeagents”或类似明确的指令时才触发该技能。
- **环境要求**：所有的操作必须在 `~/TradingAgents` 目录空间下执行。

## 工作流程

### 1. 切换工作空间
强制要求所有操作都在 `~/TradingAgents` 目录下进行。
```bash
cd ~/TradingAgents
```

### 2. 重建 Python 虚拟环境
为了保证环境纯净，如果 `venv` 目录已存在，则删除并重新创建。
```bash
# 删除旧环境
rm -rf venv

# 创建新环境 (使用系统 python3.13)
python3.13 -m venv venv

# 激活环境
source venv/bin/activate
```

### 3. 安装依赖与包
使用虚拟环境内的 pip 安装当前目录下的包以及所有依赖。
```bash
./venv/bin/pip install --upgrade pip
./venv/bin/pip install .
```

### 4. 总结代码修改并推送到远程
分析当前空间（`~/TradingAgents`）内文件的修改情况，提交变更并推送到远程 Git 仓库：
```bash
git add .
git commit -m "Auto-commit: 重新构建 TradingAgents 环境并更新相关文件"
BRANCH_NAME="feature/rebuild-$(date +%Y%m%d%H%M%S)"
git checkout -b $BRANCH_NAME
git push origin $BRANCH_NAME
```
