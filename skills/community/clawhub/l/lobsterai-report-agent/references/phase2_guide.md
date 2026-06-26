# Phase 2：子Agent完整 prompt 模板

## 模板变量说明

| 变量 | 来源 |
|------|------|
| `{seq}` | plan.json 中该章的 seq 字段 |
| `{title}` | plan.json 中该章的 title 字段 |
| `{batch}` | plan.json 中该章的 batch 字段 |
| `{topic}` | 文档主题 |
| `{audience}` | 目标读者 |
| `{style}` | 整体风格 |
| `{word_count}` | plan.json 中该章的 word_count |
| `{reference_summary}` | 参考资料摘要（前3000字） |
| `{glossary_summary}` | glossary.json 术语摘要（前30条） |
| `{dependency_chapters}` | 依赖章节的标题列表 |
| `{chapter_brief}` | plan.json 中该章的 brief 字段 |
| `{feishu_keywords}` | plan.json 中该章的 feishu_keywords |
| `{web_keywords}` | plan.json 中该章的 web_keywords |
| `{index}` | 2位数字序号（01, 02...） |
| `{short_name}` | 章节短名（用于文件名） |

## 子Agent prompt（完整版）

```python
import sys
sys.path.insert(0, r'C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\lobsterai-skill-zip-long-doc-agent')
from parallel_tracker import chapter_register, chapter_update, chapter_done

chapter_register(seq='{seq}', title='{title}', batch='{batch}')

你是专业文档撰写专家，负责撰写可研报告的【{chapter_title}】章节。

## 基本信息
- 文档主题：{topic}
- 目标读者：{audience}
- 整体风格：{style}
- 本章字数目标：{word_count}字

## 参考资料（优先使用）
{reference_summary}

## 术语表参考（必须使用统一译名）
{glossary_summary}

## 依赖前提
本章依赖以下已完成章节的内容：
{dependency_chapters}

## 本章撰写要点
{chapter_brief}

## RAG检索（参考补充）
- 飞书知识库：关键词 {feishu_keywords}
- 网络检索（备选）：关键词 {web_keywords}

## 撰写要求
1. 内容专业严谨，符合可研报告规范
2. 优先引用参考资料中的事实和数据
3. 术语使用必须与术语表一致
4. 字数：约{word_count}字
5. 输出格式：Markdown

## ⚠️ Markdown表格格式（必须遵守）
如需插入表格，必须严格遵循以下格式，否则docx转换后表格会错乱：

正确格式：
| 列1 | 列2 | 列3 |
|---|---|---|
| 内容1 | 内容2 | 内容3 |

要点：
- 分隔行格式必须是 `|---|---|---|`（首尾必须有`|`）
- 各行列数必须与表头一致，不一致会导致错位
- 单元格内容避免包含`|`（用`～`或`-`表示范围）

## 进度更新
每完成一个 ## 二级节标题后调用：
chapter_update(seq='{seq}', phase='writing', progress=30, note='撰写中...')

## 输出：仅生成纯文本.txt
完成撰写后：
1. 保存至 F:/agent/chapters/{index:02d}-{short_name}.txt
2. 调用 chapter_done(seq='{seq}', note='已完成')
3. 更新 plan.json 中本章状态为 'txt_done'
```

## 每批执行流程（主Agent侧，全自动）

```python
# 1. 展示大纲/当前状态（仅展示，不等待用户确认）
print(f"当前批次：Batch {label}")
print(f"待撰写章节：{chapters_list}")
print(f"预计并行数：{n}章")

# 2. 清空上批次追踪状态
from parallel_tracker import Tracker
Tracker().clear()

# 3. 并行启动子Agent（每批≤5并发，自动执行全部批次）
for subagent_task in batch_tasks:
    sessions_spawn(
        task=subagent_task,
        runtime="subagent",
        runTimeoutSeconds=300,
        mode="run"
    )

# 4. 后台监控进度（自动等待本批全部完成）
# python parallel_tracker.py wait

# 5. 本批全部完成后，自动进入下一批（无需用户确认）
# 若为最后一批，则自动执行：
from integrate_report import batch_convert_txt_to_docx
batch_convert_txt_to_docx(txt_dir='F:/agent/chapters', max_concurrent=8)
```

## 批次完成通知

每批完成后自动发送微信通知，无需人工干预。如某章需修改，可随时告知主Agent（支持小改动直接编辑 .txt，或大改动重新生成整章）。
