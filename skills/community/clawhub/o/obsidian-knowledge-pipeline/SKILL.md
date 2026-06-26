---
name: obsidian-knowledge-pipeline
description: 将URL文章自动抓取、分类、配图、编译入库Obsidian知识库的7步流水线技能，供Agent复用。
version: 1.0.0
author: openclaw
tags: [obsidian, knowledge-base, pipeline, url-to-wiki, auto-classify]
---

# Obsidian Knowledge Pipeline

## 概述

本技能实现从URL到Obsidian知识库节点的全自动处理流水线。任意Agent加载本技能后，即可按照标准化7步流程将网络文章转化为结构化的知识库节点，包含配图、分类、双向链接和知识图谱关系。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OBSIDIAN_VAULT_PATH` | `~/Documents/Obsidian Vault` | Obsidian Vault 根目录 |
| `DASHSCOPE_API_KEY` | _(无默认值)_ | Wan2.7 配图生成所需 API Key（可选，有则用Wan2.7脚本，无则用 image_generate 工具） |

## 快速参考

```
# 标准用法（Agent加载本skill后执行）
# 输入：一个或多个URL
# 输出：raw文章 + 配图 + 映射关系 + Wiki编译节点 + 知识图谱链接

# 关键路径
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
RAW_DIR="$VAULT/raw"
IMAGES_DIR="$RAW_DIR/images"
MAPPING_FILE="$IMAGES_DIR/关联关系.md"
WIKI_DIR="$VAULT/wiki/知识透视"
CLIPPINGS_DIR="$VAULT/Clippings"
```

## 7步流程总览

```
URL → ① 抓取 → ② 存raw/ → ③ 生成配图 → ④ 更新映射 → ⑤ 自动分类 → ⑥ Wiki编译 → ⑦ 知识图谱
```

| 步骤 | 说明 | 详细文档 |
|------|------|----------|
| ① 抓取内容 | web_fetch 优先，scrapling 回退 | [pipeline.md](pipeline.md#step-1) |
| ② 存入raw/ | 标准模板存储原文 | [pipeline.md](pipeline.md#step-2) |
| ③ 生成配图 | image_generate / Wan2.7 | [image-mapping.md](image-mapping.md) |
| ④ 更新映射 | 关联关系.md 标准条目 | [image-mapping.md](image-mapping.md) |
| ⑤ 自动分类 | 6大分类规则 | [classification.md](classification.md) |
| ⑥ Wiki编译 | 6要素结构化节点 | [classification.md](classification.md#wiki-编译标准) |
| ⑦ 知识图谱 | 双向链接建立 | [pipeline.md](pipeline.md#step-7) |

## 详细文档索引

- **[pipeline.md](pipeline.md)** — 完整7步处理流程详细说明
- **[classification.md](classification.md)** — 自动分类规则和Wiki编译标准
- **[image-mapping.md](image-mapping.md)** — 配图生成与映射规则

## 模板文件

- **[templates/raw-article.md](templates/raw-article.md)** — Raw 文章存储模板
- **[templates/wiki-node.md](templates/wiki-node.md)** — Wiki 节点编译模板
- **[templates/mapping-entry.md](templates/mapping-entry.md)** — 映射关系条目模板

## 禁止事项

- ❌ 禁止使用 `assets/` 目录存放配图，统一用 `raw/images/`
- ❌ 禁止硬编码 Vault 路径，必须通过 `$OBSIDIAN_VAULT_PATH` 环境变量
- ❌ 禁止硬编码 API Key，通过 `$DASHSCOPE_API_KEY` 环境变量引用
- ❌ 禁止跳过任何步骤，7步必须顺序执行
- ❌ 禁止在 Wiki 节点中省略6要素中的任何一个
- ❌ 禁止覆盖已有同名文件，遇到冲突时追加时间戳后缀
- ❌ 禁止在映射关系文件中使用非标准格式
- ❌ 禁止忽略 Clippings/ 目录的同步

## Clippings/ 同步流程

每次处理完文章后，需将编译结果同步到 Clippings/ 目录：

1. 在 `$CLIPPINGS_DIR` 下创建与 raw/ 同名的子目录结构
2. 将 Wiki 编译节点软链接或复制到对应位置
3. 确保 Clippings/ 中的 front matter 包含 `source_url` 字段

## 使用示例

```markdown
## Agent 调用流程

1. 读取本 SKILL.md，理解整体流程
2. 获取目标 URL
3. 按 pipeline.md 逐步执行
4. 使用 classification.md 进行分类和 Wiki 编译
5. 使用 image-mapping.md 处理配图
6. 各步骤使用 templates/ 中的标准模板
```
