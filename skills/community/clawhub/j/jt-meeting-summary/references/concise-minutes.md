# Concise minutes Markdown

Use for readable meeting minutes, “简约纪要”, or general meeting-summary requests.

## Output format

```markdown
#### 一、会议基本信息概述：
xx年xx月xx日，xxx、xxx等人进行了一场主题为xxx的会议，就xxx、xxx等议题进行了充分讨论。

#### 二、研讨嘉宾介绍：
- 发言人1
- 发言人2

#### 三、研讨话题及总结：
##### 话题1：xxx
**AI小结：**
...
**嘉宾观点：**
- **发言人1**：
  - ...
  - ...
- **发言人2**：
  - ...

#### 四、整体结论
- ...
- ...
- ...
```

## Topic segmentation

- Topic titles should be precise and no more than 15 Chinese characters when possible.
- Each topic should correspond to a coherent discussion segment.
- Separate different discussion contents; merge repeated or highly similar content.
- For short transcripts, avoid excessive topic splitting.

## AI summary requirements

For each topic, write a 100–200 Chinese character summary when enough content exists:

- Use `总-分` or `总-分-总` structure.
- Start with the topic's main point.
- Include core claims, key evidence, decisions, and action direction.
- Extract concrete slogans, policy directions, or action principles only if present.
- Do not use generic phrases like “某观点强调了...”; explain the actual content.

## Speaker views

For every substantive speaker:

- Preserve the original speaker name/id exactly.
- Summarize that speaker's own views only.
- Include problems, attitude, doubts, suggestions, outlook, key evidence, consensus/conflict, and decisions where applicable.
- Use different wording for different speakers; avoid reusable generic templates.
- Do not quote or paraphrase at unnecessary length.

## Overall conclusion

- Summarize each topic's conclusion in at least one sentence.
- Merge repeated conclusions across topics.
- Include consensus, disagreement, remaining risks, and next actions.
