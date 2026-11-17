---
name: ima-kb-organizer
description: "IMA 知识库自动分类整理与 RAG 检索增强生成技能。扫描 IMA 知识库内容，按自定义规则自动分类，生成分类索引文档（Word + Markdown），支持定期自动整理，以及基于分类索引的精准 RAG 文档生成。当用户需要整理 IMA 知识库、定期分类知识库内容、使用 IMA 知识库资料辅助撰写文档、或设置知识库自动分类整理流程时触发此技能。关键词：IMA、知识库整理、分类索引、RAG、定期扫描、检索增强生成。"
agent_created: true
---

# IMA 知识库自动分类整理与 RAG 生成

## 概述

此技能解决 IMA 知识库"只进不出、无法分类整理"的痛点。IMA API 不支持删除、移动、建文件夹操作，本技能采用**逻辑分类**方案：用本地追踪文件记录每篇内容的分类归属，用 Word/Markdown 索引文档替代物理文件夹，通过 `fetch_media_content` 按需拉取全文实现 RAG 检索增强生成。

## 前置条件

- IMA 知识库 MCP 连接器已连接（`ima-mcp`）
- 已安装 python-docx（`pip install python-docx`）

## 核心工作流

### 工作流 1：首次设置

为用户搭建完整的知识库分类整理体系。

**步骤：**

1. **获取知识库列表**
   调用 `mcp__ima-mcp__get_knowledge_base_list`，参数 `{"params": [{"limit": 50, "type": "KBT_MINE_KB"}]}`，获取用户所有知识库。

2. **扫描知识库内容**
   对每个知识库调用 `mcp__ima-mcp__get_knowledge_list`，参数 `{"knowledge_base_id": "<KB_ID>", "limit": 50, "sort_type": "UPDATE_TS_DESC_SORT_TYPE"}`。如果 `is_end` 为 false，使用 `next_cursor` 翻页获取全部内容。

3. **与用户确认分类规则**
   根据扫描到的内容，与用户讨论确定分类方案。参考 `references/category_rules.md` 中的分类原则。通常 4-6 个分类为宜。

4. **创建配置文件**
   复制 `assets/config_template.json` 到项目工作区 `.workbuddy/ima-tracker/config.json`，填入：
   - 用户的知识库 ID 和名称
   - 输出目录（用户指定保存索引文档的路径）
   - 分类规则（名称、描述、关键词、排除词）
   - RAG 设置

5. **创建追踪文件**
   在 `.workbuddy/ima-tracker/tracker.json` 中创建基线数据，记录每篇内容的 `media_id`、`title`、`source`、`type`、`first_seen` 和所属分类。格式：
   ```json
   {
     "schema_version": "1.0",
     "last_scan_time": "ISO时间",
     "knowledge_bases": {
       "<KB_ID>": {
         "name": "知识库名称",
         "categories": {
           "分类名": {
             "description": "分类描述",
             "items": [
               {"media_id": "...", "title": "...", "source": "...", "type": "...", "first_seen": "..."}
             ]
           }
         }
       }
     }
   }
   ```

6. **生成索引文档**
   运行脚本：
   ```
   <python_path> <skill_dir>/scripts/generate_index_docs.py --config .workbuddy/ima-tracker/config.json
   ```
   将在配置的 `output_directory` 中生成每个分类的 Word 和 Markdown 索引文档。

7. **创建定期自动化任务**
   使用 `automation_update` 工具创建 recurring 自动化任务。自动化 prompt 应包含：
   - 读取 tracker.json 基线
   - 扫描知识库新增内容
   - 按分类规则分类
   - 更新 tracker.json
   - 运行 generate_index_docs.py 重新生成索引文档
   - 生成 Markdown 整理报告
   - 参考下方"自动化任务 prompt 模板"

### 工作流 2：定期扫描分类（自动化执行）

由自动化任务定期触发，处理用户新增到知识库的内容。

**步骤：**

1. 读取 `.workbuddy/ima-tracker/tracker.json`，记录所有已知 `media_id`
2. 调用 `mcp__ima-mcp__get_knowledge_list` 扫描每个知识库
3. 比对找出新增内容（`media_id` 不在追踪文件中的）
4. 按分类规则（标题 + 简介 + 来源）对新增内容分类
   - 如需更高精度，可调用 `mcp__ima-mcp__fetch_media_content` 获取内容摘要辅助分类
5. 将新增内容写入 tracker.json 对应分类
6. 更新 `last_scan_time`
7. 运行 `generate_index_docs.py` 重新生成索引文档
8. 生成整理报告到 `.workbuddy/ima-tracker/reports/report-YYYY-MM-DD.md`

### 工作流 3：RAG 文档生成

用户撰写文档时，基于分类索引从 IMA 拉取全文生成。

**步骤：**

1. 用户指定要使用的分类（如"用 AI+体育 分类的资料帮我写..."）
2. 读取 `.workbuddy/ima-tracker/tracker.json` 获取该分类下所有 `media_id`
3. 选择 RAG 模式（参考 `references/rag_workflow.md`）：
   - **搜索优先**（推荐，资料多时）：用 `mcp__ima-mcp__search_knowledge` 搜索主题关键词，取 top 3-5 相关条目
   - **全量拉取**（资料少时，≤5篇）：逐篇调用 `mcp__ima-mcp__fetch_media_content` 拉全文
4. 检查本地缓存（`.workbuddy/ima-tracker/content_cache/`），已有缓存直接读取
5. 以拉取的全文作为上下文生成文档
6. 在生成的文档中标注每段内容的来源资料

## 自动化任务 prompt 模板

创建自动化任务时，将以下内容填入 prompt（替换尖括号中的内容）：

```
你是 IMA 知识库整理助手。执行以下步骤完成本周扫描分类整理。

## 配置
- 配置文件：<WORKSPACE>/.workbuddy/ima-tracker/config.json
- 追踪文件：<WORKSPACE>/.workbuddy/ima-tracker/tracker.json
- 报告目录：<WORKSPACE>/.workbuddy/ima-tracker/reports/
- Python 路径：<PYTHON_PATH>
- 脚本路径：<SKILL_DIR>/scripts/generate_index_docs.py

## 步骤
1. 读取 tracker.json，记录所有已知 media_id
2. 读取 config.json 获取知识库 ID 列表
3. 对每个知识库调用 mcp__ima-mcp__get_knowledge_list 扫描全部内容
4. 比对找出新增内容（media_id 不在 tracker 中）
5. 按 config.json 中的分类规则对新增内容分类
6. 将新增内容写入 tracker.json，更新 last_scan_time
7. 运行 generate_index_docs.py 重新生成索引文档
8. 生成 Markdown 整理报告（含新增内容标题、来源、分类结果）
9. 简要汇报扫描结果

## 注意
- 无新增内容也要更新 last_scan_time 和重新生成文档
- tracker.json 格式必须正确
- 始终使用简体中文
```

## 关键资源

### scripts/
- `generate_index_docs.py` — 分类索引文档生成器，读取 config.json 和 tracker.json，生成 Word + Markdown 索引文档并复制到用户指定目录。用法：`python generate_index_docs.py --config <config.json>`

### references/
- `ima_api_reference.md` — IMA MCP 工具完整能力说明和 API 限制
- `category_rules.md` — 分类规则定义指南（MECE 原则、颗粒度、多标签、配置格式）
- `rag_workflow.md` — RAG 检索增强生成工作流（搜索优先 vs 全量拉取、缓存策略、质量保障）

### assets/
- `config_template.json` — 配置文件模板，包含知识库 ID、输出目录、分类规则、RAG 设置

## 注意事项

- IMA API **不支持**删除、移动、建文件夹、打标签操作，所有整理通过逻辑分类实现
- 用户只需将新资料丢入知识库根目录（作为"收件箱"），自动化任务负责分类和更新索引
- 索引文档生成后自动复制到用户在 config.json 中指定的 `output_directory`
- 如分类规则需要调整，修改 config.json 后重新全量扫描分类即可
- `fetch_media_content` 拉取的全文建议缓存到本地，避免重复 API 调用
