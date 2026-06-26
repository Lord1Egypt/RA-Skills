---
name: layered-memory-sys
slug: layered-memory-sys
description: "分层记忆系统 v2.4.1 — 6层架构的智能记忆管理。支持分层TTL管理、梦境模式（自动巩固/归档/遗忘/合并）、TF-IDF搜索、导入导出、全功能管理面板（搜索/批量操作/编辑/梦境触发）、自动备份、Docker一键部署。适用于AI Agent需要长期记忆、分层管理、自动遗忘和知识提取的场景。触发词：记忆、分层、梦境、导入导出、归档、备份"
---

# layered-memory-sys

分层记忆系统 — 6层架构的智能记忆管理，灵感来自人类记忆机制。

## 核心特性

### 🧠 6层记忆架构
- **核心层** (永久) → MEMORY.md，永久存储的核心记忆
- **沉淀层** (90天) → 重要决策、项目经验
- **关注层** (30天) → 反复讨论的话题
- **活跃层** (7天) → 正在进行的任务
- **闪存层** (3天) → 临时查询、一次性问答
- **Session** (实时) → 当前对话上下文

### ⚡ 核心功能
- 📊 **分层 TTL 管理** — 自动升级/归档/遗忘
- 💤 **梦境模式** — 巩固、归档、遗忘、合并（定时执行）
- 🔍 **TF-IDF 搜索** — 中文关键词搜索（支持召回机制）
- 📈 **全功能管理面板** — 记忆管理、搜索、批量操作、导入导出
- 📥 **记忆导入导出** — JSON 格式，支持 skip/overwrite/append 模式
- 🐳 **Docker 一键部署** — 记忆面板 + API + 定时备份
- ⚙️ **路径配置化** — 支持环境变量和配置文件
- 🤖 **自动写入检测** — 从对话中识别值得记住的内容

### 🆕 v2.4.1 修复
- **梦境去重修复** 🐛 — 修复点击「运行梦境」按钮时自动重复生成记忆的 bug
  - 添加 `processed_messages` 表追踪已处理消息
  - 消息级精确去重（sessionId + 内容hash）
  - 对话摘要去重（session 文件列表 key）
  - 语义相似度去重升级（0.8 → 0.85）

### 🆕 v2.4.0 新增
- **📥 导入导出** — JSON 格式导出/导入，支持 skip/overwrite/append 三种冲突模式
- **🎛️ 全功能管理面板** — 搜索、层级筛选、标签云、详情编辑、批量操作（切换层级/归档/删除）
- **🗂️ 自动备份** — 定时备份 SQLite + JSON，自动清理过期备份
- **🐳 Docker 一键部署** — Docker Compose 三容器（API + Nginx面板 + 备份服务），`install.sh` 支持 Docker/原生双模式
- **🖱️ 批量操作** — 全选、批量切换记忆层级、批量归档/删除
- **📤 导出菜单** — `GET /api/export` 按层级/类型/状态过滤导出
- **📥 导入菜单** — `POST /api/import` 支持三种冲突处理模式

### 🔒 v2.3.0 新增
- **图遍历搜索** — 基于记忆关联图的广度/深度优先搜索
- **Hebbian 学习** — 记忆关联强度动态调整
- **矛盾检测** — 自动识别和标记矛盾记忆
- **自动提取** — 从对话内容自动提取关键信息
- **云端同步可选** — 按需启用/禁用同步

### 🔒 v2.2.0 新增
- **进程锁** — 防止多进程并发冲突
- **批量事务** — 提升大量操作性能
- **合并摘要** — 相似记忆自动合并摘要
- **锁定层级** — 防止重要记忆被误删
- **提醒重试** — 提醒发送失败自动重试
- **日志分级** — DEBUG/INFO/WARN/ERROR 分级日志

## 快速开始

### 安装依赖
```bash
cd skills/layered-memory-sys
npm install
```

### 测试
```bash
node scripts/test-v2.mjs
```

### 梦境模式
```bash
node scripts/dream-cycle.mjs
```

### 统计面板
```bash
node scripts/stats-panel.mjs
```

### Docker 一键部署（推荐 🚀）
```bash
cd skills/layered-memory-sys
bash install.sh
```
自动部署 API 服务、Nginx 面板（含记忆管理 UI）、定时备份→ `http://localhost/memory`

### 原生模式启动 API 服务
```bash
cd skills/layered-memory-sys
node scripts/start-api.mjs
```
启动后访问：
- API: `http://localhost:3456/api/...`
- 记忆面板: `http://localhost:3456/{memory.html}（需配 Nginx）`

### 备份命令
```bash
node scripts/backup.mjs --dir ./backups --keep 30
```

## API 文档

### 记忆 CRUD
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/memories` | 列出所有记忆 |
| GET | `/api/memories/:id` | 获取单条记忆 |
| POST | `/api/memories` | 创建记忆 |
| PATCH | `/api/memories/:id` | 更新记忆（部分字段） |
| DELETE | `/api/memories/:id` | 删除记忆 |

### 搜索
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/search` | 关键词搜索 `{query, limit}` |
| POST | `/api/search/tfidf` | TF-IDF 搜索 |

### 梦境 & 提醒
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/dream/run` | 手动触发梦境 |
| GET | `/api/dream/logs` | 梦境日志 |
| GET | `/api/dream/stats` | 梦境统计 |
| GET | `/api/reminders` | 获取提醒列表 |
| POST | `/api/reminders` | 创建提醒 |

### 统计 & 导入导出 🆕 v2.4.0  |  梦境去重 🐛 v2.4.1
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats` | 统计总览（层级分布、标签云、即将过期） |
| GET | `/api/export?status=all` | 导出所有记忆（JSON 数组） |
| GET | `/api/export/download?status=all` | 导出为可下载 JSON 文件 |
| POST | `/api/import` | 导入记忆 `{memories, mode:"skip|overwrite|append"}` |

## 使用方式

### 记忆层级规则

| 层级 | TTL | 说明 |
|------|-----|------|
| flash | 3天 | 临时查询、一次性问答 |
| active | 7天 | 正在进行的任务 |
| attention | 30天 | 反复讨论的话题 |
| settled | 90天 | 重要经验、决策记录 |

### 升级规则
- 同一话题被召回 ≥3 次 → flash → active
- 多天连续被召回 → active → attention
- 召回 ≥10 次 → attention → settled
- 用户说"记住这个" → 直接进沉淀层

### 锁定层级
可通过配置锁定特定层级，防止被归档或遗忘。

## 配置

支持环境变量 + 配置文件 (`memory/config.json`) + 默认值三级覆盖：

| 环境变量 | 说明 |
|---------|------|
| MEMORY_DIR | 记忆数据目录 |
| SESSION_DIR | Session 日志目录 |

## 依赖

| 依赖 | 用途 | 必需 |
|------|------|------|
| sql.js | SQLite WASM 存储 | ✅ |
| nodejieba | 中文分词 | 推荐 |
| ws | WebSocket | 可选 |

## 版本历史

- **v2.4.0** 🎉 — 导入导出/全功能管理面板/自动备份/Docker一键部署/批量操作
- **v2.3.0** — 图遍历搜索/Hebbian学习/矛盾检测/自动提取/云端同步可选
- **v2.2.0** — 进程锁/批量事务/合并摘要/锁定层级/提醒重试/日志分级
- **v2.0.1** — 6层架构/中文分词/时间衰减/REST+WebSocket接口
- **v2.0.0** — 初始版本
