# Phase 2: Sub-Agent Full Prompt Template

## Template Variable Descriptions

| Variable | Source |
|----------|--------|
| `{seq}` | seq field of this chapter in plan.json |
| `{title}` | title field of this chapter in plan.json |
| `{batch}` | batch field of this chapter in plan.json |
| `{topic}` | Document topic |
| `{audience}` | Target audience |
| `{style}` | Overall style |
| `{word_count}` | word_count field of this chapter in plan.json |
| `{reference_summary}` | Reference material summary (first 3000 characters) |
| `{glossary_summary}` | Glossary summary (first 30 entries) |
| `{dependency_chapters}` | Title list of dependent chapters |
| `{chapter_brief}` | brief field of this chapter in plan.json |
| `{feishu_keywords}` | feishu_keywords from plan.json |
| `{web_keywords}` | web_keywords from plan.json |
| `{index}` | 2-digit sequential number (01, 02...) |
| `{short_name}` | Chapter short name (used in filenames) |

## Sub-Agent Prompt (Full Version)

```python
import sys
sys.path.insert(0, r'C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\long-doc-agent')
from parallel_tracker import chapter_register, chapter_update, chapter_done

chapter_register(seq='{seq}', title='{title}', batch='{batch}')

You are a professional document writing expert, responsible for writing the 【{chapter_title}】 chapter of the feasibility report.

## Basic Information
- Document Topic: {topic}
- Target Audience: {audience}
- Overall Style: {style}
- This Chapter's Word Target: {word_count} words

## Reference Materials (Priority Use)
{reference_summary}

## Glossary Reference (Must Use Consistent Terminology)
{glossary_summary}

## Dependencies
This chapter depends on the following completed chapters:
{dependency_chapters}

## This Chapter's Writing Points
{chapter_brief}

## RAG Search (Supplementary Reference)
- Feishu Knowledge Base: keywords {feishu_keywords}
- Web Search (backup): keywords {web_keywords}

## Writing Requirements
1. Content must be professional and rigorous, conforming to feasibility report standards
2. Prioritize citing facts and data from reference materials
3. Terminology usage must be consistent with the glossary
4. Word count: approximately {word_count} words
5. Output format: Markdown

## ⚠️ Markdown Table Format (Must Follow)
When inserting tables, you MUST strictly follow this format, otherwise tables will be distorted in docx conversion:

Correct format:
| Col1 | Col2 | Col3 |
|---|---|---|
| Content1 | Content2 | Content3 |

Key points:
- Separator row format must be `|---|---|---|` (leading/trailing `|` required)
- All rows must have the same column count as the header — mismatch causes column displacement
- Cell content should avoid containing `|` (use `～` or `-` for ranges)

## Progress Update
After completing each ## H2 section heading, call:
chapter_update(seq='{seq}', phase='writing', progress=30, note='Writing in progress...')

## Output: Generate Plain Text .txt Only
After completing the writing:
1. Save to F:/agent/chapters/{index:02d}-{short_name}.txt
2. Call chapter_done(seq='{seq}', note='Completed')
3. Update this chapter's status to 'txt_done' in plan.json
```

## Per-Batch Execution Flow (Main Agent Side, Fully Automatic)

```python
# 1. Display outline/current status (display only, no user confirmation)
print(f"Current batch: Batch {label}")
print(f"Chapters to write: {chapters_list}")
print(f"Estimated parallelism: {n} chapters")

# 2. Clear previous batch tracking state
from parallel_tracker import Tracker
Tracker().clear()

# 3. Parallel launch sub-agents (≤5 per batch, automatically execute all batches)
for subagent_task in batch_tasks:
    sessions_spawn(
        task=subagent_task,
        runtime="subagent",
        runTimeoutSeconds=300,
        mode="run"
    )

# 4. Monitor progress in background (automatically wait for this batch to complete)
# python parallel_tracker.py wait

# 5. After this batch completes, automatically proceed to next batch (no user confirmation)
# If this is the last batch, automatically execute:
from integrate_report import batch_convert_txt_to_docx
batch_convert_txt_to_docx(txt_dir='F:/agent/chapters', max_concurrent=8)
```

## Batch Completion Notification

WeChat notification is automatically sent after each batch completes, no manual intervention needed. If any chapter needs modification, you can notify the main agent at any time (supports small changes via direct .txt editing, or large changes via full chapter regeneration).
