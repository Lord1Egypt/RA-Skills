---
name: knowledge-base-skill
version: 2.1.1
description: Multi-business knowledge base with image attachment + OCR support. Manage Q&A databases by business type, auto page splitting, and intelligent search.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "optional": ["tesseract-ocr", "pytesseract", "pillow"] },
        "install": [],
        "files":
          [
            "knowledge-base/kb-manager.py",
            "knowledge-base/image-manager.py",
            "knowledge-base/kb-image.sh",
          ],
      },
  }
---
# Knowledge Base Skill - 多业务知识库管理（支持图片 + OCR）

## 📖 功能概述

支持按业务类型分隔的问答知识库系统，每个业务独立存储、独立查询，自动分页，**支持图片附件 + OCR 文字提取**。

### 核心特性

| 特性 | 说明 |
|------|------|
| 🏢 **多业务支持** | 客服、产品、技术等独立数据库 |
| 📄 **自动分页** | 单文件达 500MB 自动创建新页 |
| 📸 **图片附件** | 保存截图，自动 OCR 提取文字 |
| 🔍 **智能搜索** | 匹配问题文本 + 图片 OCR 文字 |
| ⏳ **待回答管理** | 记录未回答问题，定期提醒 |
| 📊 **统计分析** | 业务统计、图片统计 |
| 📤 **导出功能** | 一键导出 Markdown 文档 |

---

## 🎯 触发词

当用户提到以下关键词时，进入知识库操作模式：

- `我想操作知识库`
- `我想操作业务知识库`
- `知识库`
- `knowledge base`
- `KB`
- `添加一个问题`
- `查询知识库`

---

## 🚀 交互流程

### 方式一：快捷命令（强烈推荐 ⭐）

用户直接使用快捷格式，无需多轮对话：

```
KB:<业务名> Q:<问题> A:<答案>              # 纯文字问答
KB:<业务名> Q:<问题> A:<答案> IMG:<路径>   # 带图片问答
KB:<业务名> <问题>                         # 查询问题
KB:<业务名> list                           # 查看统计
KB:list                                    # 列出所有业务
KB:img list [业务名]                       # 列出图片
KB:img stats                               # 图片统计
```

**示例：**
```
KB:客服 Q:如何退款 A:7 天内无理由退款
KB:技术 Q:登录报 502 错误 A: 检查 Nginx 配置 IMG:/tmp/error.png
KB:客服 退款流程是什么
KB:技术 list
KB:list
```

### 方式二：对话模式

#### 步骤 1：触发知识库操作

**用户**: `我想操作知识库` 或 `我想操作业务知识库`

**助理**: 
```
📚 已进入知识库操作模式

当前业务：
1. 客服 (120 问答)
2. 产品 (85 问答)
3. 技术 (200 问答)

请告诉我业务类型，或：
- 输入业务名称（如"客服"）
- 说"list"查看所有
- 说"new 业务名"创建新业务
- 或直接用快捷格式：KB:业务 Q:问题 A:答案
```

#### 步骤 2：选择业务

**用户**: `技术` 或 `切换到技术知识库`

**助理**:
```
✅ 已选择：技术知识库

当前操作模式：
- 添加问答：Q: 问题 A: 答案 [IMG:图片路径]
- 查询问题：直接发送问题
- 查看状态：list
- 图片管理：img list / img stats
- 切换业务：switch
- 退出：exit

当前业务：技术 | 已回答：200 条 | 待回答：5 条 | 图片：15 张
```

#### 步骤 3：执行操作

**添加问答（纯文字）**:
```
用户：Q: API 地址是什么 A: https://api.example.com
助理：✅ 问答已添加 (技术知识库)
```

**添加问答（带图片）**:
```
用户：Q: 登录报 502 错误 A: 检查 Nginx 配置 IMG:/tmp/error.png
助理：
📸 保存图片... ✅ 已保存：error.png (256 KB)
🔍 提取 OCR 文字：502 Bad Gateway nginx/1.18.0
✅ 问答已添加 (技术知识库)
📎 附件：1 张图片
```

**查询问题**:
```
用户：502 错误怎么办
助理：
🔍 找到匹配答案（相似度 0.95）：

Q: 登录报 502 错误
A: 检查 Nginx 配置

📎 相关图片：error.png
📝 图片文字：502 Bad Gateway nginx/1.18.0
```

---

## 📋 命令格式详解

### 快捷命令（推荐）

| 命令 | 说明 | 示例 |
|------|------|------|
| `KB:业务 Q:问题 A:答案` | 添加问答 | `KB:客服 Q:如何退款 A:7 天内可退款` |
| `KB:业务 Q:问题 A:答案 IMG:路径` | 添加带图片问答 | `KB:技术 Q:502 错误 A: 检查 Nginx IMG:/tmp/error.png` |
| `KB:业务 问题` | 查询问题 | `KB:客服 退款流程` |
| `KB:业务 list` | 查看业务统计 | `KB:技术 list` |
| `KB:list` | 列出所有业务 | `KB:list` |
| `KB:new 业务名` | 创建新业务 | `KB:new 财务` |
| `KB:export 业务名` | 导出文档 | `KB:export 客服` |
| `KB:img list [业务]` | 列出图片 | `KB:img list 技术` |
| `KB:img stats` | 图片统计 | `KB:img stats` |

### 自然语言命令

| 用户输入 | 助理行为 |
|---------|---------|
| `我想在客服知识库添加一个问题` | 提示用户提供问题和答案 |
| `Q: 如何退款 A: 7 天内可退款` | 添加到当前业务知识库 |
| `查询产品知识库中关于价格的问题` | 在产品知识库中搜索 |
| `帮我创建一个 HR 知识库` | 创建新业务 |
| `切换到技术知识库` | 切换当前业务 |
| `导出客服知识库` | 导出 Markdown 文档 |

---

## 🗂️ 目录结构

```
knowledge-base/
├── kb-manager.py              # 知识库核心管理器
├── image-manager.py           # 图片管理器 + OCR
├── kb-image.sh                # 图片命令行工具
├── businesses.json            # 业务索引
├── attachments/               # 图片附件目录
│   ├── 客服/
│   │   ├── a3f8b2c1.png
│   │   └── d9e4f5a6.jpg
│   ├── 产品/
│   └── 技术/
├── 客服/                      # 业务数据库目录
│   ├── qa-database.json
│   └── qa-database-page2.json
├── 产品/
└── 技术/
```

---

## 📸 图片处理流程

### 1. 保存图片

```python
# 自动保存到 attachments/业务名/
# 生成唯一文件名：{hash}.{ext}
# 返回文件信息：路径、大小、扩展名
```

### 2. OCR 提取文字

```python
# 自动尝试 OCR 引擎：
# 1. pytesseract (Python 库)
# 2. tesseract 命令行
# 3. 其他 OCR 服务
# 返回提取的文字内容
```

### 3. 存储到数据库

```json
{
  "question": "登录报 502 错误",
  "answer": "检查 Nginx 配置",
  "attachments": [
    {
      "filename": "a3f8b2c1.png",
      "type": "image",
      "path": "attachments/技术/a3f8b2c1.png",
      "ocr_text": "502 Bad Gateway nginx/1.18.0"
    }
  ]
}
```

### 4. 搜索时匹配

```python
# 同时搜索：
# 1. 问题文本相似度
# 2. 图片 OCR 文字相似度
# 返回最佳匹配 + 图片附件
```

---

## 🔍 搜索策略

### 优先级

1. **当前业务搜索** - 默认只在当前业务搜索
2. **跨业务搜索** - 如果当前业务无匹配，询问是否跨业务搜索
3. **图片 OCR 搜索** - 同时匹配图片中的文字

### 相似度阈值

| 相似度 | 行为 |
|--------|------|
| ≥ 0.9 | 直接返回，高置信度 |
| 0.7-0.9 | 返回并提示相似度 |
| 0.6-0.7 | 返回并建议确认 |
| < 0.6 | 视为无匹配，建议添加新问答 |

### 搜索结果格式

```json
{
  "question": "登录报 502 错误",
  "answer": "检查 Nginx 配置",
  "similarity": 0.95,
  "business": "技术",
  "page": 1,
  "attachments": [
    {
      "filename": "a3f8b2c1.png",
      "ocr_text": "502 Bad Gateway"
    }
  ]
}
```

---

## ⚙️ 配置选项

### 分页大小

```python
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
```

### 相似度阈值

```python
DEFAULT_THRESHOLD = 0.6  # 默认匹配阈值
```

### OCR 语言

```python
# 支持的语言包
lang='chi_sim+eng'  # 简体中文 + 英文
```

---

## 🛠️ 命令行工具

### 知识库管理

```bash
cd knowledge-base

# 业务管理
python3 kb-manager.py business list              # 列出所有业务
python3 kb-manager.py business new 客服          # 创建新业务
python3 kb-manager.py business delete 客服       # 删除业务

# 问答操作
python3 kb-manager.py add 客服 "如何退款" "7 天内可退款"
python3 kb-manager.py search 客服 "退款流程"
python3 kb-manager.py stats 客服                 # 详细统计
python3 kb-manager.py export 客服                # 导出文档
```

### 图片管理

```bash
# 保存图片并添加问答
./kb-image.sh add 技术 "502 错误" "检查 Nginx" "/tmp/error.png"

# OCR 提取
./kb-image.sh ocr "/tmp/screenshot.png"

# 列出图片
./kb-image.sh list 技术

# 图片统计
./kb-image.sh stats
```

---

## 📊 统计信息

### 业务统计

```bash
KB:技术 list
```

输出：
```
业务：技术
已回答：200 条
待回答：5 条
页数：1 页
```

### 图片统计

```bash
KB:img stats
```

输出：
```json
{
  "total_images": 25,
  "total_size_mb": 12.5,
  "businesses": {
    "客服": {"images": 10, "size_kb": 5120},
    "技术": {"images": 8, "size_kb": 4096},
    "产品": {"images": 5, "size_kb": 2560}
  }
}
```

---

## 💡 最佳实践

### 1. 业务命名

- ✅ 简洁：2-4 个字（客服、产品、技术）
- ❌ 过长：客户服务知识库、产品信息知识库

### 2. 问题标准化

- ✅ 包含关键词：`502 错误`、`退款流程`、`API 地址`
- ❌ 模糊表述：`这个怎么办`、`那个问题`

### 3. 图片处理

- ✅ 清晰截图，文字可读
- ✅ 有意义文件名：`login-502-error.png`
- ✅ 大小 < 5MB
- ❌ 敏感信息未脱敏

### 4. 定期维护

- 每周导出备份：`KB:export 业务名`
- 清理待回答问题
- 检查图片统计

---

## ⚠️ 依赖安装

### 必需

- Python 3.x
- 基础 Python 库（json, os, hashlib 等）

### 可选（推荐）

**OCR 引擎 - 用于自动提取图片文字：**

```bash
# Python 库
pip install pytesseract pillow

# 系统包（Ubuntu/Debian）
apt install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng

# macOS
brew install tesseract tesseract-lang
```

**检查 OCR 状态：**
```bash
./kb-image.sh ocr /path/to/test.png
```

---

## 🎯 使用场景

### 场景 1：客服 FAQ

**问题**：新客服不知道如何处理各种客户咨询

**解决**：
1. 创建 `客服` 业务
2. 添加常见问题：`KB:客服 Q:如何退款 A:7 天内可退款`
3. 新客服查询时自动回答

### 场景 2：技术支持（带截图）

**问题**：用户发送错误截图咨询，同样问题重复出现

**解决**：
1. 保存错误截图：`KB:技术 Q:502 错误 A: 检查 Nginx IMG:/tmp/error.png`
2. OCR 自动提取文字
3. 下次查询时返回答案 + 截图

### 场景 3：产品文档

**问题**：产品规格经常变更，文档更新不及时

**解决**：
1. 创建 `产品` 业务
2. 每次更新后添加：`KB:产品 Q:iPhone 15 规格 A:...IMG:specs.png`
3. 查询时自动匹配最新规格

---

## 📖 相关文档

- [README.md](../../knowledge-base/README.md) - 完整文档
- [QUICKSTART.md](../../knowledge-base/QUICKSTART.md) - 快速开始
- [IMAGE_GUIDE.md](../../knowledge-base/IMAGE_GUIDE.md) - 图片支持详解
- [EXAMPLES.md](../../knowledge-base/EXAMPLES.md) - 使用示例
- [SUMMARY.md](../../knowledge-base/SUMMARY.md) - 功能总结

---

## 📝 版本历史

- **v2.1** (2026-03-15) - 图片附件支持、OCR 文字提取、图片搜索
- **v2.0** (2026-03-15) - 多业务支持、快捷命令格式
- **v1.0** (2026-03-15) - 初始版本

---

**Skill 位置**: `skills/knowledge-base-skill/`
**数据位置**: `knowledge-base/`
