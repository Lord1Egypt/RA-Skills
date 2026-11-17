# Cliche Phrase Audit

## Aim

Catch phrases that readers now associate with machine-shaped prose, then replace
them with evidence that belongs to the current scene, argument, narrator, or source.

This is not a universal banned-word list. A phrase is a problem when it appears
without earned context, repeats across outputs, or substitutes for observation.

## Common Tell Families

### Chinese narrative and web fiction

- Fate inflation: "命运的齿轮", "一场风暴即将来临", "无人知道的是"
- Generic body cues & melodrama: "深邃的眼眸", "嘴角微微上扬", "眼中闪过一丝", "倒吸一口凉气", "瞳孔骤缩", "嘴角勾起一抹玩味", "周身散发威压"
- Emotion labels: "不禁感到一阵愤怒", "心中涌起复杂情绪"
- Empty atmosphere: "空气仿佛凝固", "时间在这一刻静止"
- Pseudo-intellectual flourishes: "最真实的底色", "写下最好的注脚", "激起微弱的回响", "在时间的褶皱里", "肌理", "锚点"
- Reasoning bleed-through: "究其原因", "归根结底", "从本质上剖析", "这背后折射出", "深层逻辑在于"
- Manufactured social media hype: "谁懂啊家人们", "狠狠共情", "治愈内耗", "直接封神", "闭眼入", "答应我"
- Cinematic setup bundles: exact clock + named place + colored light/weather + full
  outfit + generalized feeling before the first consequential action
- Vague self-interpretation: repeated "不知道为什么", "莫名", or "像是……又像是……"
  without a changed choice
-万能转场: "与此同时", "另一边", "很快", "下一秒" used without causal bridge

### English and general prose

- Inflated importance: "game-changing", "groundbreaking", "transformative", "beacon", "unleash", "foster"
- Stock abstractions: "realm", "tapestry", "journey", "landscape", "ecosystem", "nuanced", "intertwined", "bolster"
- Dead transitions: "moreover", "furthermore", "it is important to note", "a testament to the power of"
- Polished filler: "in today's fast-paced world", "unlock the potential", "let that sink in"

## Audit Steps

1. Scan for phrase families, not only exact words. Mark repeated gestures,
   repeated sentence openings, and repeated transition shapes.
2. Ask what the phrase is doing. Is it carrying plot, tone, proof, voice, or
   only decorating a blank spot?
3. Replace decorative phrases with one of:
   - a visible action
   - a specific object
   - a local sensory fact
   - a quoted or paraphrased source
   - a character-specific verbal habit
   - a causal bridge from the previous beat
4. Preserve a phrase only when it is intentional for parody, voice, genre
   convention, or character idiolect.
5. Send repeated contrast, comparison, and symmetrical sentence frames to
   `formulaic-structure-audit`. This module owns stock wording and phrase families,
   not sentence architecture.

## Repair Patterns

| Weak Pattern | Better Repair |
| --- | --- |
| Name the emotion | Show the action that leaks it |
| Announce fate | Put a small irreversible change on the page |
| Use stock body language | Tie the body cue to the character's current constraint |
| Add a grand transition | Carry over an object, sound, question, or pressure |
| Use abstract praise | Give one concrete proof detail |

## Output Check

When auditing, return:

```text
Cliche Phrase Audit
- Phrase: "..."
- Type: fate inflation / generic body cue / dead transition / abstract filler
- Why it reads machine-shaped:
- Keep or revise:
- Replacement direction:
```

Do not simply replace one cliche with another. If no concrete evidence exists,
ask for context or leave a plain sentence.
