---
name: obsidian-notesmd-cli
version: 1.0.0
description: Obsidian笔记命令行工具，支持笔记搜索、批量处理、统计分析、导出转换、标签管理等功能，直接操作本地Obsidian知识库。
metadata:
  author: bassshang
  category: productivity
  capabilities:
    - 全文搜索Obsidian笔记内容/标题
    - 统计知识库信息：笔记数量、总字数、标签统计、文件大小
    - 批量替换笔记内容
    - 导出笔记为Markdown/HTML/TXT格式
    - 提取双向链接关系、生成关系图谱数据
    - 批量管理笔记标签
    - 按日期/标签/关键词筛选笔记
---

# Obsidian Notesmd CLI 命令行工具

直接操作本地Obsidian知识库（Vault），无需打开Obsidian客户端即可完成批量操作、统计分析、内容搜索等功能。

## 核心功能
### 1. 笔记搜索
支持全文搜索、标题搜索、标签搜索、按日期范围筛选：
- 支持关键词高亮
- 支持正则表达式搜索
- 搜索结果按相关度排序

### 2. 知识库统计
自动生成知识库统计报告：
- 总笔记数量、总字数、总附件大小
- 标签数量、标签使用频率排名
- 近7/30/90天新增笔记数量
- 文件类型分布统计

### 3. 批量操作
- 批量替换所有笔记中的指定文本
- 批量给符合条件的笔记添加/删除标签
- 批量导出笔记到指定目录
- 批量清理空笔记、重复笔记

### 4. 链接管理
- 提取所有笔记的双向链接关系
- 检测孤立笔记（没有任何入链出链的笔记）
- 检测死链（指向不存在的笔记的链接）
- 导出链接关系数据用于生成关系图谱

## 使用方法
### 基础命令
```powershell
# 搜索笔记
obsidian-cli search "关键词" --vault "你的知识库路径"

# 生成知识库统计报告
obsidian-cli stats --vault "你的知识库路径"

# 批量替换内容
obsidian-cli replace "旧文本" "新文本" --vault "你的知识库路径"

# 导出所有笔记
obsidian-cli export --output "导出目录路径" --format markdown

# 检测死链
obsidian-cli check-links --vault "你的知识库路径"
```

### 常用参数
| 参数 | 说明 | 必填 |
|------|------|------|
| --vault | Obsidian知识库根目录路径 | ✅ |
| --output | 导出结果保存路径 | ❌ |
| --format | 导出格式：markdown/html/txt/json | 默认markdown |
| --case-sensitive | 搜索/替换是否区分大小写 | 默认不区分 |
| --regex | 是否启用正则表达式匹配 | 默认不启用 |
| --include-attachments | 导出时是否包含附件 | 默认不包含 |

## 示例
```powershell
# 统计我的知识库信息
obsidian-cli stats --vault "D:\我的知识库"

# 搜索所有包含"AI大模型"的笔记
obsidian-cli search "AI大模型" --vault "D:\我的知识库"

# 把所有笔记中的"GPT-4"替换为"GPT-4o"
obsidian-cli replace "GPT-4" "GPT-4o" --vault "D:\我的知识库" --case-sensitive

# 导出所有带"工作"标签的笔记
obsidian-cli export --vault "D:\我的知识库" --tag "工作" --output "D:\导出的工作笔记"
```
