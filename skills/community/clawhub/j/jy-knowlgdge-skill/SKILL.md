---
name: jy-knowledge-skill
description: 智能知识库文件处理与数据集自动生成系统。上传文件后自动评估知识价值，LLM智能分类归档，通过EasyDataset生成微调数据集。使用场景：(1) 用户上传文档需要判断是否值得生成知识数据集，(2) 批量处理DOCX/PDF/Excel/图片文件转为知识库，(3) 从本地知识库搜索答案结合对话回复，(4) 部署和初始化知识库环境，(5) 管理知识库分类体系和数据集。
metadata: {"clawdbot":{"emoji":"📚","requires":{"anyBins":["python","docker"]},"os":["win32","linux","darwin"]}}
---

# JY_Knowledge_Skill

基于 LLM 的智能知识库文件处理系统，实现从**文件上传 → 价值判断 → 自动分类 → 数据集生成 → 分类归档 → 知识检索**的全流程自动化。通过 EasyDataset + MongoDB 双引擎驱动。

## When to Use

- 用户上传了文档文件（.docx/.pdf/.xlsx/.md/.txt），需要判断是否值得制作知识库数据集
- 批量处理文档目录，自动生成 Alpaca 格式的微调训练数据集
- 对话中用户提问涉及已入库的知识领域，需要从知识库检索相关内容辅助回答
- 部署知识库服务到服务器，需要环境检测、Docker 部署、一键安装
- 管理知识库分类体系，查看某分类下的数据集数量和描述

## Quick Reference

```bash
# 环境检测（首次使用必须执行）
python tools/check_env.py

# 测试所有连接（LLM/EasyDataset/MongoDB/视觉模型）
python main.py -t

# 处理单个文件（自动价值评估 + 数据集生成）
python main.py -f <文件路径> -y

# 批量处理目录
python main.py -d <目录路径> -y

# 知识库总览
python main.py --overview
# → /焊接材料: 286 datasets, 收录焊接电极、焊丝、焊条...
# → /工程技术: 0 datasets (新建分类)

# 搜索知识库（返回仅 answer 文本，≤45000字）
python main.py -q "焊丝 技术要求"
# → **重型装备集团焊丝采购选型评估简报**...
# → ---
# → **依据国家标准规范**...

# 问题诊断
python tools/diagnose.py
```

## Prerequisites

| 组件 | 检测命令 | 缺失时行为 |
|------|----------|------------|
| Python 3.10+ | `python --version` | 告知用户安装，等确认 |
| pip 依赖 | `python tools/check_env.py` | 列出缺失库，询问是否允许 `pip install` |
| Docker | `docker --version` | 告知安装方式，等确认 |
| EasyDataset (:1717) | `curl localhost:1717/api/projects` | 询问是否允许 `docker pull + run` |
| MongoDB (:27017) | `python tools/check_env.py` | 同上 |
| config.json | 自动检测 | **不存在时逐项询问**用户 LLM/视觉模型/路径信息 |

> 📖 完整冷启动流程（7 Phase 逐项部署 + 用户话术模板）见 `docs/cold_start.md`

## Core Workflow

### 文件处理管线

```
用户上传文件
  → [Step 1] 预处理（DOCX/PDF/图片 → 纯文本 Markdown，视觉 LLM 替换内嵌图片）
  → [Step 2] 价值评估（LLM 打分，< 0.4 跳过，>= 0.4 继续）
  → [Step 3] 智能分类（LLM 匹配 MongoDB 分类树，自动创建新分类 + GA 判断）
  → [Step 4] 参数确认（分类路径、GA 设置、语言）
  → [Step 5-6] EasyDataset 管线（分割 → GA对 → 问题生成 → 答案生成，最多3次重试）
  → [Step 7] 去重 + COT移除 + 本地 JSON 导出
  → [Step 8] MongoDB 入库（ds_{分类slug} 集合）
```

### 知识检索协议

```
用户提问涉及已有分类
  → python main.py --overview     # 确认分类存在
  → python main.py -q "关键词"    # 搜索 ds_* 集合
  → 仅返回 answer（---分隔）+ 45000字截断
  → 作为知识凭证融入回答
```

## 依赖服务

| 服务 | 地址 | 用途 |
|------|------|------|
| EasyDataset | `http://localhost:1717` | 文本/图片数据集生成引擎（Docker） |
| MongoDB | `mongodb://localhost:27017` | 分类体系 + ds_* 数据集存储（Docker） |
| LLM API | 用户配置 | 价值评估 + 智能分类 + GA判断 |
| 视觉 LLM API | 用户配置 | 文档图片识别 + 表格截图解析 |

## Examples

### 处理一个 DOCX 文件

```bash
python main.py -f D:/docs/焊接标准.docx -y
```
```
# Expected output:
[INIT] 系统初始化完成
============================================================
  Processing: 焊接标准.docx
  Size: 472,334 bytes | MD5: a4db4db0...
============================================================

[Step 1] 文件预处理...
  预处理完成 → .../processed/a4db4db0.md
  Markdown 长度: 42756 字符

[Step 2] 价值评估 (LLM)...
  价值评分: 0.92 | 有价值: True
  理由: 内容为国家技术标准，信息密度高...

[Step 3] 智能分类 (LLM + MongoDB)...
  匹配分类: /焊接材料 (置信度: 1.00)

[Step 6] EasyDataset 数据集生成...
  [1] 项目已创建: JYKG_xxx_1753000000
  [4] 文件分割完成
  [5] 问题生成完成
  [6] 答案生成完成 (184/184)
  [7] 已确认 184 条数据集
  [8] 导出完成，共 184 条数据集

[OK] 数据集导出路径: .../datasets/焊接材料/焊接标准.docx/焊接标准.docx_alpaca.json
```

### 低价值文件跳过

```bash
python main.py -f D:/docs/会议纪要.txt -y
```
```
[Step 2] 价值评估 (LLM)...
  价值评分: 0.25 | 有价值: False
  [跳过] 文件价值不足 (阈值: 0.4)
```

### 环境检测

```bash
python tools/check_env.py
```
```
# Expected output (healthy):
✅ Python 3.13.12
✅ requests (HTTP API 调用)
✅ pymongo (MongoDB 驱动)
...
✅ 配置文件: config.json
✅ Docker 运行时
✅ EasyDataset API
✅ MongoDB 容器
============================================================
所有检测通过 ✅  可以执行: python main.py -t
```

## Config Setup

首次使用需生成 `config.json`，由 Model 分批询问用户后写入（不自动生成空配置）：

```json
{
  "llm": {
    "base_url": "http://your-llm-host:port/v1",
    "api_key": "your-api-key-here",
    "model": "your-model-name",
    "vision_model": "your-vision-model",
    "vision_concurrency_limit": 10
  },
  "easy_dataset": { "base_url": "http://localhost:1717" },
  "mongo": { "uri": "mongodb://localhost:27017", "database": "knowledge_skill" },
  "output": {
    "processed_dir": "./processed",
    "datasets_dir": "./datasets",
    "uploads_dir": "./uploads"
  },
  "dataset_generation": {
    "task_timeout_minutes": 720,
    "include_ga_pairs": true
  },
  "file_filter": { "value_threshold": 0.4 }
}
```

## Common Operations

### 环境问题诊断

```bash
# 快速环境检测
python tools/check_env.py
# → 列出所有缺失的依赖和服务

# 深度诊断（含日志和容器状态）
python tools/diagnose.py --full
# → MongoDB 连接状态 + EasyDataset API 可达性 + 最近日志
```

### 知识库管理

```bash
# 查看所有分类及数据集数量
python main.py --overview
# → /焊接材料: 286 datasets, 收录焊接电极、焊丝...

# 搜索知识（纯 answer 文本，不包含 question）
python main.py -q "焊丝 分类 标准"
# → **重型装备集团焊丝采购选型评估简报**...
# → ---
# → **依据国家标准规范，气体保护电弧焊**...
```

### 测试连接

```bash
python main.py -t
# Expected:
# ✅ LLM 服务: 连接成功 ✓
# ✅ 视觉模型: 连接成功 ✓
# ✅ EasyDataset: 连接成功 ✓
# ✅ MongoDB: 连接成功 ✓
```

## 辅助文档

详细内容按需查阅，避免占用主上下文：

| 文件 | 何时查阅 |
|------|----------|
| `docs/cold_start.md` | 全新服务器、环境缺失、首次部署 |
| `docs/skill_architecture.md` | 完整管线流程、文件结构、配置模板 |
| `docs/easydataset_deploy.md` | EasyDataset + MongoDB Docker 部署指南 |
| `docs/easydataset_api.md` | EasyDataset 130+ API 端点完整参考 |
| `docs/troubleshooting.md` | 20种常见错误的诊断与修复命令 |

## Troubleshooting

常见问题快速定位和修复：

```bash
# 全局诊断
python tools/diagnose.py --full
# Expected output:
# Python: 3.13.12
# OK 配置文件: 配置正常
# --- MongoDB ---
#    状态: running
#    Docker 容器运行中: knowledge-mongo   Up 3 hours
#    MongoDB 直接连接成功
#    数据库 knowledge_skill 存在
#    数据集集合: 1 个
# --- EasyDataset ---
#    状态: running
#    EasyDataset API 正常 (返回 892 bytes)
```

### ModuleNotFoundError

```bash
# 检测缺失的依赖
python tools/check_env.py
# → ❌ fitz   PDF 转图片（PyMuPDF）
# →    pip install pymupdf>=1.24.0

pip install -r requirements.txt
```

### EasyDataset 连接失败

```bash
# 确认容器状态
docker ps | grep easy-dataset
# → (空) — 容器未运行

# 启动容器
docker pull ghcr.io/conardli/easy-dataset:latest
docker run -d --name easy-dataset --restart unless-stopped -p 1717:3000 ghcr.io/conardli/easy-dataset:latest

# 验证
sleep 5 && curl -s http://localhost:1717/api/projects
# → [] (正常返回)
```

### MongoDB 连接失败

```bash
# 确认容器状态
docker ps | grep knowledge-mongo
# → (空) — 容器未运行

docker pull mongo:7
docker run -d --name knowledge-mongo --restart unless-stopped -p 27017:27017 mongo:7
```

### config.json 不存在

```bash
# Model 不应自动生成，而应分批询问用户：
# 1. LLM API 地址 + API Key + 模型名称
# 2. 视觉模型 API 地址 + API Key + 模型名称
# 3. 存储路径（datasets/ processed/ uploads/）

# 拿到信息后写入 config.json，路径由用户指定
```

### Task Polling 超时

```bash
# 默认超时 720 分钟，在 config.json 的 task_timeout_minutes 调整
# 查看 EasyDataset 日志确认任务仍在运行
docker logs easy-dataset --tail 20
# → Starting answer generation for project y13KUDTvB5lI
# → Processed: 180/453, succeeded: 180, failed: 0
```

## Tips

- `tools/check_env.py` 是一键检测利器，Model 在每次会话开始都应先跑这个脚本确认环境
- EasyDataset task 响应是 `{code: 0, data: {...}}` 格式，记得解包 `data` 字段读取 `status`
- 问题/答案生成默认超时 12 小时（720 分钟），在大文件（500+ chunk）场景下无需调整
- GA 增强由 LLM 在分类时自主判断，适合标准/规范/教材等多角色解读文档，无需手动开关
- Python 脚本输出可能有 GBK 编码问题（Windows），已在 main.py + tools 中加了 UTF-8 修复
- MongoDB slug 使用 MD5 确定性哈希（不是 Python `hash()`），跨进程/重启保持一致
- 项目名使用完整 Unix 时间戳保证唯一：`JYKG_<文件名>_<timestamp>`，不会碰撞
- EasyDataset 领域树构建走 `domain_tree_action="keep"` 跳过 LLM 调用，避免非标准 JSON 输出兼容问题
- `requirements.txt` 已包含 `Pillow`，冷启动时别忘了 `pip install -r requirements.txt`
- 视觉 LLM 并发上限 20，默认 10，由 `config.json` → `vision_concurrency_limit` 控制

## Hard Constraints

- 视觉 LLM 并发上限 20（默认 10），不可超过
- 知识检索 answer 拼接总字数 ≤ 45000，超出的在句号处截断并标记 `...[已截断]`
- COT 字段**彻底删除**（`ds.pop('cot', None)`），最终数据集仅有 question/answer/questionLabel/chunkName
- 问题/答案生成最多重试 3 次，失败则跳过不影响整体
- Model 执行任何动态操作（部署、安装、改配置、删文件）前必须**先告知用户并获取确认**
