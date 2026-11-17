---
name: "mochi-study-coach"
description: "Import question decks, retain attempts and review dates, summarize practice and export answer-hidden queues. Use for Study Coach and Mistake Review."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Study Coach and Mistake Review

## Prepare a sourced practice deck

Collect the learner's subject and source material. add stores topic, question, answer, source and the initial review date. import-csv accepts topic,question,answer,source with a per-row date or a default date on the request. Duplicate topic/question/source records are counted rather than added again. An invalid row prevents saving a partial batch. Use source-backed questions or label examples as exercises created for practice.

## Practice before revealing answers

due returns the date/topic review queue without stored answers or review history. Ask the learner to attempt a question first. show reveals one card's answer when needed. grade stores the actual response and feedback with a grade 0..3. Grades below 2 reset the stage; successful attempts extend the interval through the scripted sequence. The model explains the grade and the learner can correct it. A future due date is a ledger value, not a scheduled notification.

## Inspect progress and prepare the next session

stats reports card count, due count, recorded attempts, successful attempts and average recorded grade for the selected topic. These are practice records, not a standardized ability score. export creates review-plan.md and review-queue.csv for questions due on the selected date. Answers remain omitted unless includeAnswers:true is explicitly requested. Keep the saved queue and actual attempt history so a later session can continue from the same cards. Requested proactive review uses the host's separate scheduler.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-study-coach/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
