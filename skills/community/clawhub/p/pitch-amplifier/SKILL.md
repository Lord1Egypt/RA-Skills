---
name: pitch-amplifier
description: Turn a vague reporting clue, observation, or topic hunch into a deeper news pitch by extracting entities, retrieving 1-2 hop context from a city knowledge graph, and generating an editor-style planning memo. Use when the user says things like “这个选题怎么做深”, “帮我放大这个线索”, “这个观察能不能做成深度报道”, or needs angles, contradictions, interview targets, and structural context behind a local topic.
---

# Pitch Amplifier

Use the bundled script to turn a rough clue into a deeper reporting plan.

## Workflow

1. Normalize the user's clue into graph-query keywords.
2. Retrieve nearby issues, institutions, and relation chains from the graph.
3. Generate an editor-style pitch memo with:
   - 图谱关联洞察
   - 破局角度
   - 建议采访清单
4. If the graph has weak coverage, say so clearly and treat it as a reporting gap instead of pretending certainty.

## Use the script

Primary script:
- `scripts/skill_pitch_amplifier.py`

Typical usage:

```bash
python3 scripts/skill_pitch_amplifier.py "最近园博园挺热闹，但我感觉大型活动越来越多，周边交通和承载压力可能会越来越大，这个选题能怎么做深？"
```

Interactive mode:

```bash
python3 scripts/skill_pitch_amplifier.py
```

## Constraints

- Prefer graph-grounded output over generic feature writing.
- Do not hard-code one topic template across all topics.
- When graph recall is weak, explicitly mark the topic as a graph blind spot.
- Keep interview lists specific to the detected issue cluster: transport, ecology, governance, operations, market, etc.

## Topic routing rule

Infer the dominant issue family from graph context before generating the memo:
- Transport / crowding / parking / carrying capacity
- Ecology / wetland / habitat / environmental protection
- Cultural tourism / event operations / post-event sustainability
- Governance / multi-department coordination / responsibility structure
- Market / business survival / operator pressure

If multiple families appear, keep 2-3 strongest ones and organize the memo around tension between them.
