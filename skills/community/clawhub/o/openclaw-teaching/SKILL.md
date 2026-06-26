---
name: openclaw-teaching
description: "OpenClaw 知识教学技能 - 用于持续更新和管理 OpenClaw 平台知识，支持将知识内容导出为 PPT 或 Word 文档。适用场景：OpenClaw 平台使用教程、技能开发指南、最佳实践分享、知识库维护与更新。"
license: MIT
version: 1.0.0
author: OpenClaw Team
---

# OpenClaw 知识教学技能

## 概述

本技能是一个专门用于 OpenClaw 平台知识管理和教学的工具。它能够：
- 持续更新和维护 OpenClaw 知识库
- 将知识内容导出为专业的 PPT 演示文稿
- 将知识内容导出为 Word 文档
- 支持知识分类和版本管理

## 核心能力

### 1. 知识库管理
- **知识收集**: 从多种来源收集 OpenClaw 相关知识
- **知识分类**: 按主题、难度、类型进行分类
- **版本控制**: 跟踪知识的更新历史
- **知识检索**: 快速查找特定知识点

### 2. 文档生成
- **PPT 生成**: 创建专业的教学演示文稿
- **Word 文档**: 生成详细的教学文档
- **自定义模板**: 支持自定义文档样式和格式

### 3. 内容更新
- **增量更新**: 支持添加新知识点
- **批量更新**: 批量导入知识内容
- **自动同步**: 与官方文档保持同步

## 使用指南

### 快速开始

当用户需要 OpenClaw 相关知识教学时，按以下流程操作：

1. **识别需求**: 确定用户需要的知识类型（入门教程、进阶指南、API 文档等）
2. **检索知识**: 从知识库中检索相关内容
3. **生成文档**: 根据用户需求生成 PPT 或 Word 文档

### 知识库结构

知识库位于 `KNOWLEDGE_BASE.md`，包含以下主要章节：

```
1. OpenClaw 平台概述
2. 快速入门指南
3. 技能开发教程
4. API 参考文档
5. 最佳实践
6. 常见问题解答
7. 更新日志
```

### 文档生成命令

#### 生成 PPT 演示文稿

```bash
python scripts/generate_docs.py ppt \
    --topic "技能开发入门" \
    --output "/home/z/my-project/download/openclaw_tutorial.pptx" \
    --template "modern"
```

#### 生成 Word 文档

```bash
python scripts/generate_docs.py docx \
    --topic "OpenClaw 完整教程" \
    --output "/home/z/my-project/download/openclaw_guide.docx" \
    --include-toc
```

#### 更新知识库

```bash
python scripts/update_knowledge.py \
    --action add \
    --category "技能开发" \
    --title "新技能创建流程" \
    --content "..."
```

## 知识更新流程

### 1. 收集新知识
- 从官方文档获取最新信息
- 收集用户反馈和常见问题
- 整理最佳实践案例

### 2. 验证和整理
- 验证知识的准确性
- 按分类整理内容
- 添加示例代码和截图

### 3. 更新知识库
- 运行更新脚本添加新知识
- 更新版本号和更新日志
- 生成新的文档版本

## 文档模板说明

### PPT 模板类型
- `modern`: 现代简约风格（默认）
- `professional`: 专业商务风格
- `creative`: 创意活泼风格

### Word 文档选项
- `--include-toc`: 包含目录
- `--include-cover`: 包含封面
- `--style`: 文档样式（academic/business/tutorial）

## 输出目录

所有生成的文档默认保存到：
```
/home/z/my-project/download/
```

## 注意事项

1. **知识准确性**: 更新知识前务必验证内容的准确性
2. **版本管理**: 重要更新后记得更新版本号
3. **文档格式**: 生成的文档遵循 OpenClaw 官方文档规范
4. **编码规范**: 所有脚本使用 UTF-8 编码，支持中文内容

## 依赖说明

本技能依赖以下组件：
- Python 3.8+
- python-pptx（PPT 生成）
- python-docx（Word 文档生成）
- markdown（Markdown 解析）

## 更新历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2024-01-01 | 初始版本发布 |

---

**技能路径**: `{project_path}/skills/openclaw-teaching`
**知识库文件**: `{Skill Location}/KNOWLEDGE_BASE.md`
