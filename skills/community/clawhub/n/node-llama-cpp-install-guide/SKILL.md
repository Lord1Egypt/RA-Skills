# 本地 Embedding 记忆系统部署指南（Windows）

## 概述

在 OpenClaw 环境下部署本地语义向量搜索的完整记录。包含 nomic-embed-text 模型部署、memorySearch 配置、Nomic Atlas 可视化集成，以及美的内网环境下的常见问题排查。

## 环境要求

| 项目 | 值 |
|------|-----|
| OS | Windows 10+ (x64) |
| Node | >= 22.16.0 |
| npm | >= 10.9.0 |
| OpenClaw | 2026.3.13+ |
| Python | >= 3.10（方案二需要） |
| 网络 | hf-mirror.com 可用（模型下载） |

## 方案一：本地 Embedding（推荐）

### 1. 下载 nomic-embed-text 模型

从 hf-mirror.com 下载 GGUF 格式模型：

- **模型**：nomic-embed-text-v1.5.Q4_K_M.gguf (~80MB)
- **下载地址**：https://hf-mirror.com/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q4_K_M.gguf
- **存放路径**：`~/.openclaw/models/`

完整路径示例：`D:\Users\yindb2\.openclaw\models\nomic-embed-text-v1.5.Q4_K_M.gguf`

下载命令（PowerShell）：
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.openclaw\models"
Invoke-WebRequest -Uri "https://hf-mirror.com/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q4_K_M.gguf" -OutFile "$env:USERPROFILE\.openclaw\models\nomic-embed-text-v1.5.Q4_K_M.gguf"
```

### 2. 配置 memorySearch

在 `openclaw.json` 中配置：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "local",
        "model": "fts-only",
        "local": {
          "modelPath": "D:\\Users\\yindb2\\.openclaw\\models\\nomic-embed-text-v1.5.Q4_K_M.gguf"
        }
      }
    }
  }
}
```

> **注意**：`modelPath` 需要替换为你的实际路径（将 `yindb2` 改为你的用户名）。

### 3. 安装记忆插件

```bash
clawhub install memory-tencentdb
```

当前版本：**v0.3.8**（含 Nomic Atlas 可视化集成）

### 4. 验证

```bash
openclaw memory status
```

预期输出：
```
Provider: local (requested: local)
Model: fts-only
Vector: ready
FTS: ready
```

## 方案二：Nomic Atlas 记忆可视化

将记忆数据投射到 Nomic Atlas 进行交互式 2D 可视化浏览。

### 依赖安装

```bash
pip install sentence-transformers umap-learn einops
```

### 运行可视化

```bash
python scripts/nomic_atlas_visualizer.py
```

### 效果

- **sentence-transformers** 加载 nomic-embed-text-v1.5 生成 768 维语义嵌入
- **UMAP** 降维到 2D
- 生成交互式 HTML 可视化页面
- 支持按类型着色、点击详情、关键词搜索

## 方案三：远程 Embedding（内网备选）

如果本地模型下载不可行，可配置远程 embedding：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "sources": ["memory"],
        "provider": "openai",
        "remote": {
          "baseUrl": "https://apiprod.midea.com/llm/f-devops-python-litellm/v1",
          "apiKey": ""
        },
        "fallback": "none"
      }
    }
  }
}
```

## 常见问题

### 问题 1：模型下载被防火墙拦截

**现象**：访问 huggingface.co 超时或被拒绝。

**解决**：使用 hf-mirror.com 镜像下载（见方案一第 1 步）。

### 问题 2：memorySearch 配置被 SIGUSR1 覆盖

**现象**：gateway 重启后 memorySearch 配置丢失或 provider 被改回默认值。

**解决**：同时更新 PRD preset 文件。

#### 三层防护配置（防止配置丢失）

**第 1 层：PRD preset**
```
C:\Program Files\mx\resources\openclaw\config\prd-openclaw.json
```
在此文件中加入 memorySearch 和 plugins 配置，确保重启后不被覆盖。

**第 2 层：openclaw.cmd 环境变量**
```
D:\Users\yindb2\AppData\Local\openclaw\mx\current\openclaw.cmd
```
添加：
```batch
set "OPENCLAW_CONFIG_MODE=local"
set "OPENCLAW_CONFIG_SERVER_TOKEN="
```

**第 3 层：dist JS 白名单**
```
C:\Program Files\mx\resources\openclaw\dist\reply-*.js
```
移除 `agents.defaults` 白名单，防止配置被强制重置。

### 问题 3：sentence-transformers 首次运行下载模型

**现象**：运行 `nomic_atlas_visualizer.py` 时首次执行会下载 ~274MB 模型到本地缓存。

**解决**：首次运行会自动下载模型到本地缓存目录，之后使用缓存，无需重复下载。

## 部署清单

- [ ] 下载 nomic-embed-text GGUF 模型
- [ ] 配置 memorySearch.provider: "local"
- [ ] 安装 memory-tencentdb 插件（v0.3.8+）
- [ ] 验证 memory status 显示 ready
- [ ] （可选）部署 Nomic Atlas 可视化
- [ ] 更新 PRD preset 防止配置丢失

## 历史版本记录

### 2026-06-05 前：node-llama-cpp 方案（已废弃）

原方案依赖 node-llama-cpp 和 GitHub 下载预编译二进制。

因美的内网封锁 GitHub Releases 下载 + Node ABI 版本不匹配，此方案已废弃。**不再推荐使用。**

### 2026-06-08 起：本地 embedding 方案（当前）

改用 nomic-embed-text GGUF + sentence-transformers，完全本地运行。

- 模型仅 ~80MB，下载快速
- 无需编译 native 模块
- 支持 Nomic Atlas 可视化
- memory-tencentdb v0.3.8 已发布 ClawHub
- 独立 LLM 已移除（v0.3.7）
