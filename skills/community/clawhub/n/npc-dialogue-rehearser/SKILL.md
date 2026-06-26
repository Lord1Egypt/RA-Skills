---
name: npc-dialogue-rehearser
description: Rehearse a real-world conversation by modeling likely counterpart styles such as busy, defensive, friendly, or authority-like NPCs. Generate a natural opening line, a short branching script, safer alternatives to risky phrases, and a calm closing line. Use when the user wants to ask for help, express a boundary, explain a need, or prepare for a mildly stressful conversation without becoming manipulative.
version: v1.0.0
tags: ttrpg, game-master, npc-design, roleplaying, creative-writing
---

# NPC Dialogue Rehearser

Chinese name: NPC 对话排练.

## Overview

Use this skill when the user wants to practice wording before a real conversation. It keeps the language natural, respects the relationship, and prepares a recovery line when the other person responds in an unexpected way.

## When to use

Use this skill when the user wants to:
- ask for help or accommodation
- express a boundary clearly
- explain a need without sounding vague
- prepare for a mildly tense conversation
- avoid freezing or overexplaining

### Example prompts
- "Help me rehearse how to ask for an extension"
- "Give me a natural script for setting a boundary"
- "What should I say if the other person gets defensive?"

## Inputs

Useful inputs include:
- scenario and counterpart
- goal or request
- taboo areas and worries
- preferred tone, such as gentle, firm, or brief

## Workflow

1. Clarify the real goal.
2. Choose the likely NPC styles.
3. Generate an opening line and branching short script.
4. Swap risky phrases for safer ones.
5. End with a calm closing line.

## Output

Return markdown with:
- dialogue objective
- opening line
- three-branch script
- risky phrase replacements
- closing line
- safety note for high-risk situations when relevant

## Limits

- This skill does not guarantee the real outcome.
- It should not be used for coercion, manipulation, or abusive dynamics.
- Serious legal, medical, violent, or power-abuse situations may require real-world support.

## Acceptance Criteria

- The language sounds natural.
- At least one branch handles an off-script response.
- The script protects the user’s goal without turning manipulative.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "Create a dialogue rehearsal for my innkeeper NPC: grumpy dwarf, speaks in short sentences, secretly a retired adventurer." | Character voice profile. Rehearsal script with 10 common player-trigger lines and the innkeeper's in-character responses. Includes "secret-reveal" triggers: if players ask about the scar on his arm or the locked chest behind the bar. |
| 2 | "The players just asked my villain something I did not prepare for: 'Why are you really doing this?' Improvise 3 responses that stay in character." | Three in-character responses at different depths: (1) surface lie, (2) half-truth deflection, (3) full-villain-monologue option. Each with dialogue, tone notes, and possible player follow-up prompts. |
| 3 | "Review my session notes. I feel like all my NPCs sound the same. Diagnose and fix." | Voice-diversity analysis: 8 NPCs, 6 use formal diction, 5 use similar sentence length. Recommends distinctive speech patterns: a nervous tic for the merchant, regional slang for the sailor, and abrupt interruptions for the impatient guard. |


### Scenario 2: 不知道怎么和陌生人开口
**User input:** "我在健身房/咖啡厅/行业会议上遇到想认识的人，但不知道怎么打招呼怎么开口。每次都是心跳加速最后什么也没说。怎么办？"
**Expected output:** 社交场景开口攻略——健身房场景：在器械休息时看着对方自然地问"你还有几组？""这个动作是练哪里的？"（80%的人会回答并反问）；咖啡厅场景：排队时看着对方点的东西说"你这个看起来不错，是什么？"或让对方推荐"你觉得这家什么最好喝？"；行业会议场景：等电梯/休息时的万能开场白"你好，我是XX公司的XX，你是做什么的？"然后问一个对方行业的问题；通用法则：问一个容易回答的开放式问题+认真听+跟着对方的话题聊。关键：不要想太多"要说什么"，开口说第一个句子最难但说出来了后面就顺了，被拒绝也没关系你不会再见到这个人。
