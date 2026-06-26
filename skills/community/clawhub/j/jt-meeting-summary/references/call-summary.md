# Phone-call summary

Use for phone-call transcripts or AI速记通话 summaries.

## Speaker handling

1. Assign stable labels such as `发言人1(138****0001)` and `发言人2(139****0002)`.
2. In later topic summaries, refer to `发言人1` / `发言人2`; avoid repeatedly exposing phone numbers.
3. Mask the middle digits of phone numbers unless raw identifiers are explicitly required.

## Short-content handling

- Under 30 seconds with no concrete information: output `暂无`.
- Under 3 minutes: produce a compressed summary significantly shorter than the original.
- Under 1000 Chinese characters or total duration under 5 minutes: do not split into many topics.

## Output format

```markdown
#### 一、通话基本信息概述：
xx年xx月xx日，发言人1（手机号）与发言人2（手机号）就xxx等话题进行了一次通话，主要讨论了xxx。

#### 二、研讨嘉宾介绍：
- 发言人1（手机号）
- 发言人2（手机号）

#### 三、子话题及总结：
##### 话题1：xxx
**AI小结：**
...
**双方观点：**
**发言人1（角色）**：
- ...
**发言人2（角色）**：
- ...

#### 四、整体结论
- ...
```

## Content requirements

For each party, naturally summarize:

- role and core intent
- questions, attitude, demands, suggestions, commitments, or changed position
- agreements, disagreements, responsibilities, deadlines, and unresolved issues
- omit detailed treatment of small talk unless it affects meaning

Do not use mechanical labels like “角色分析/核心观点概括” inside each bullet; make the bullets read naturally.
