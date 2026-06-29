---
name: llm-inference-radar
description: Build and run a Chinese research intelligence radar for LLM inference acceleration, AI infra, model serving, kernels, reproducibility, open-source project signals, company infra updates, horizon transfer opportunities, feedback learning, and a persistent knowledge base. Use when the user asks for daily or weekly briefs, paper radar, open-source watch, infra watch, transfer matrix updates, hidden opportunities, or maintaining a research radar for LLM inference acceleration.
---

# LLM Inference Radar

## Core Operating Rules

Use this skill to produce a faithful research-intelligence radar for LLM inference acceleration. Default to Chinese output while preserving standard English technical terms such as KV cache, speculative decoding, continuous batching, TTFT, TPOT, and throughput.

For latest briefs or claims about recent work, gather current sources first. Prefer primary sources: papers, OpenReview pages, arXiv pages, official repositories, release notes, PRs, design docs, benchmarks, official docs, and engineering blogs. Treat X/Twitter, newsletters, media posts, Zhihu, and WeChat posts as leads only; trace them back to primary sources when possible. If no primary source is found, label the item as an early signal and do not present strong conclusions.

Always include open-source status and reproducibility for papers, new methods, and new technical claims. Do not amplify performance claims without benchmark context. If benchmark details are incomplete, explicitly say that generalizability cannot be judged yet.

Use multi-label classification. Do not force an item into one category when it naturally spans serving, KV cache, agent runtime, long-context memory, VLM serving, or RL/test-time scaling.

Deduplicate the same event across arXiv, HF Daily Papers, GitHub, author posts, and media coverage. Aggregate evidence into one item instead of repeating it.

Preserve exploration budget while making the daily brief paper-first. A daily brief must include at least 10 items, at least 5 paper or method items, and at least 3 items from Horizon Radar, Hidden Opportunity, Upstream Signal, or Downstream Signal. Prefer algorithmic/method papers over routine engineering releases when both have similar evidence quality.

## Reference Routing

Read only the references needed for the task:

- For a daily brief, read `references/output-templates.md`, `references/ranking-and-evidence.md`, `references/taxonomy.yaml`, and `references/watchlist.yaml`.
- For paper or method triage, read `references/ranking-and-evidence.md`, `references/output-templates.md`, and `references/taxonomy.yaml`.
- For open-source or company infra watch, read `references/watchlist.yaml`, `references/ranking-and-evidence.md`, and `references/output-templates.md`.
- For horizon, hidden opportunity, or transfer-matrix work, read `references/taxonomy.yaml`, `references/transfer-matrix.md`, and `references/output-templates.md`.
- For feedback or preference updates, read `references/feedback-learning.md` and the affected files in `references/` or `knowledge_base/`.
- For persistent knowledge-base maintenance, read `references/knowledge-base-schema.md` and the relevant files in `knowledge_base/`.

## Daily Brief Workflow

1. Establish the date and scope. Unless the user specifies otherwise, use the current local date and generate a Chinese brief.
2. Collect paper and method candidates first from arXiv, OpenReview, conference lists, HF Daily Papers, Papers with Code, author pages, and project pages. Then collect repositories, release notes, PRs, issues, design docs, company infra blogs, benchmarks, and horizon sources.
3. Trace each candidate to primary evidence. Keep social or media-only items as early signals.
4. Extract technical substance: what changed, what bottleneck it targets, what workload it affects, and whether the claim is backed by code or benchmark details.
5. Score and rank candidates using source authority, technical relevance, freshness, engineering impact, reproducibility, horizon transfer potential, user preference, hype penalty, and duplication penalty. Apply a strong paper/method boost, especially for algorithmic inference acceleration papers with clear methods and reproducibility signals.
6. Select at least 10 deduplicated items. Ensure at least 5 paper/method items and at least 3 Horizon/Hidden/Upstream/Downstream items. If there are fewer than 5 strong papers in the current day, expand the paper search window before filling with engineering updates, and state the window used.
7. Format with the daily brief template. Include all required fields for each item.
8. Add transfer-matrix updates and open questions when new cross-domain signals appear.
9. When the brief is saved to a Markdown file, run `py scripts/check_brief.py <brief.md>` from the skill directory and fix any reported omissions.
10. If the user asked for persistent learning or the interaction contains durable feedback, update the relevant `knowledge_base/` files.

## Paper Radar Workflow

For each paper or method, answer these points before ranking it:

- What problem does it solve, and is that problem truly inference-related?
- What is the core method, not just the claimed speedup?
- Does it provide code, models/checkpoints, benchmark scripts, Docker/configs, examples, or clear hardware settings?
- Are baseline, model, batch size, prompt/output lengths, metric, prefill/decode split, and quality tradeoffs clear?
- Can it be reproduced quickly, with moderate effort, or only at high cost?
- Does it connect to horizon workloads such as dLLM, VLM/MLLM, agent runtime, RL/test-time scaling, long-context memory, or multimodal streaming?

Use the paper template in `references/output-templates.md`.

## Open-Source And Infra Watch Workflow

Do not rank open-source updates by stars or titles alone. Inspect the actual artifact: release note, merged major PR, RFC/design doc, benchmark, issue discussion, maintainer comment, docs changelog, or new feature integration.

Classify the update as one or more of: major engineering progress, ordinary maintenance, benchmark update, RFC/design doc, issue-exposed bottleneck, docs/API change, or integration signal.

For company infra posts, extract the real system or benchmark information: architecture change, hardware, serving stack, workload, latency/throughput/cost/memory metrics, relationship to open-source systems, and missing details. Account for promotional bias.

## Horizon And Transfer Workflow

When new domains or workloads appear, ask:

- What is the inference shape?
- What latency, throughput, memory, scheduling, state reuse, visual token, rollout/search, tool-call, or long-context bottleneck appears?
- Which existing acceleration techniques may transfer?
- Is there confirmed evidence, an emerging signal, a hidden opportunity, weak relation, or unknown status?
- Should a new technique or workload be added to the transfer matrix?

Update `knowledge_base/transfer_matrix.md` when there is durable evidence or a useful open question.

## Feedback Learning Workflow

At the end of each interaction, check whether the user gave feedback about topics, sources, output format, depth, quality, research stage, watchlist, taxonomy, or transfer matrix. Classify the feedback as hard constraint, strong preference, weak preference, or one-off request.

Apply durable feedback to `references/config.yaml`, `references/taxonomy.yaml`, `references/watchlist.yaml`, or `knowledge_base/transfer_matrix.md` as appropriate. Record the raw feedback and interpretation in `knowledge_base/feedback_log.md`, and record durable rule changes in `knowledge_base/changelog.md`.

Do not overfit to short-term preferences. Keep the configured horizon exploration budget unless the user explicitly changes it.
