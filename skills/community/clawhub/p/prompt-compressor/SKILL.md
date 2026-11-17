---
name: prompt-compressor
display_name: 提示/上下文压缩（Prompt Compressor）
display_name_en: "Prompt Compressor"
description: "当用户说『提示词太长/token烧太快』『上下文塞不下了』『把这段压缩一下还别丢重点』『长文档怎么塞进窗口』，或要压低 agent 每轮上下文成本时使用。基于「信息密度」裁剪：保留关键词密集/位置靠前的句子，删冗余/客套/复述，给出可运行脚本（提示压缩器，按密度+位置打分删句）。与 context-engineering 互补：context 管『放什么』，compressor 管『怎么压短』。理论根基：LGD 三律之收敛（删除冗余，单一有效信息）。触发词：提示压缩、prompt压缩、上下文压缩、压缩token、长文本精简、context压缩、省token、摘要进窗口、prompt shorten。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - 提示词/上下文太长，token 成本或窗口吃紧
  - 要把长文档压成能进窗口的精华
  - 想在不丢重点的前提下砍掉冗余句子
  - 搭 agent 时每轮上下文预算超标
tags: [提示压缩, prompt compressor, 上下文压缩, 省token, 长文本精简, 收敛]
slug: prompt-compressor
title: 提示/上下文压缩（Prompt Compressor）
copyright: SynomosAI
description_zh: "当用户说『提示词太长/token烧太快』『上下文塞不下了』『把这段压缩一下还别丢重点』『长文档怎么塞进窗口』，或要压低 agent 每轮上下文成本时使用。基于「信息密度」裁剪：保留关键词密集/位置靠前的句子，删冗余/客套/复述，给出可运行脚本（提示压缩器，按密度+位置打分删句）。与 context-engineering 互补：context 管『放什么』，compressor 管『怎么压短』。理论根基：LGD 三律之收敛（删除冗余，单一有效信息）。触发词：提示压缩、prompt压缩、上下文压缩、压缩token、长文本精简、context压缩、省token、摘要进窗口、prompt shorten。"
description_en: "Information-density based prompt and context compression: keep keyword-dense, front-positioned sentences and drop redundancy to cut per-turn token cost."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/compress_prompt.py
  runtime: python3
  call_pattern: args
input_schema:
  text:
    type: string
    description: "text"
    required: false
  file:
    type: string
    description: "file"
    required: false
  ratio:
    type: number
    description: "保留比例 0-1"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - prompt
  - compression
  - token
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- When the user detects capacity-limits scenarios such as "the prompt is too long", "tokens are burning too fast" or "the context won't fit".
- When you need to cut an agent's per-turn communication cost to fit the window-size limit or cost-control policy.
- When the input contains lots of redundancy, repetition or low information density and you must preserve core intent density.

### Usage
- Call the core script `compress_prompt.py` as the main logic carrier.
- Configure via command-line: `python compress_prompt.py --input "text-to-compress" --threshold 0.5`.
- For system integration, import the compiled module from `__pycache__` to ensure dependencies are ready.

### Workflow
1. Monitor the conversation flow / input features; spot trigger words ("compress", "save tokens") and context-overflow signals.
2. Sentence-split and tag the raw prompt; per the LGD convergence theory, keep keyword-dense and front-positioned sentences.
3. Run `compress_prompt.py` to auto-filter redundancy, pleasantries and repetitions.
4. Validate the output: core logic intact and no key instruction lost.
5. Return the trimmed prompt together with a runnable compression report.
6. Hand the final result to downstream agents or to the user for confirmation.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.1.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 当用户检测到「提示词太长」「token 烧太快」或「上下文塞不下了」等容量限制场景时。
- 需要降低 Agent 每轮沟通成本，以符合窗口大小限制或成本控制策略时。
- 针对输入中包含大量冗余、复述或低信息密度内容，需保持核心意图密度的情况。

### 用法
- 调用核心脚本 `compress_prompt.py`，作为技能执行的主要逻辑载体。
- 支持命令行参数配置：`python compress_prompt.py --input "待压缩文本" --threshold 0.5`。
- 若用于系统集成，读取 `__pycache__` 中的编译模块即可确保依赖环境就绪。

### 流程
1. 监测对话流或输入特征，识别触发词（如「压缩」「省 token」）及上下文溢出信号。
2. 对原始提示词进行分句与标记，依据 LGD 收敛理论筛选关键词密集及位置靠前的句子。
3. 执行 `compress_prompt.py` 脚本，自动过滤冗余、客套及重复信息片段。
4. 校验输出结果，确保核心逻辑完整性且未丢失关键指令内容。
5. 返回精简后的提示词，并生成对应的可运行压缩报告。
6. 将最终结果交付给后续 Agent 调用或用户确认。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
