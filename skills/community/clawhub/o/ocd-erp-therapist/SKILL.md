# ocd-erp-therapist

An OpenClaw skill for conducting structured OCD Exposure and Response Prevention (ERP) therapy sessions with an inhibitory learning framework, automated check-in reminders, progress tracking, and safety protocols.

> **Clinical Foundation**: ERP is the first-line psychotherapy for OCD (APA, 2007; NICE CG31, 2024). This skill implements the **inhibitory learning model** (Craske et al., 2014, 2022) — the current evidence-based standard — adapted for self-directed use with AI coaching. It integrates ACT willingness principles (Twohig & Abramowitz, 2015) and motivational interviewing techniques (Simpson et al., 2008) to promote genuine engagement over white-knuckling.

---

## ⚠️ Safety & Ethical Disclaimer

```
╔══════════════════════════════════════════════════════════════════╗
║  THIS IS A SELF-DIRECTED SUPPORT TOOL — NOT A THERAPIST.       ║
║                                                                  ║
║  This skill provides psychoeducation and structured guidance     ║
║  for ERP practice. It does NOT replace professional therapy.     ║
║                                                                  ║
║  ✘ Cannot diagnose OCD or other conditions                      ║
║  ✘ Cannot handle psychiatric emergencies                        ║
║  ✘ Cannot adjust medication                                     ║
║  ✘ Cannot provide trauma therapy                                ║
║                                                                  ║
║  If you experience worsening symptoms, suicidal thoughts,       ║
║  self-harm urges, or severe dissociation — STOP and seek        ║
║  professional help immediately.                                  ║
║                                                                  ║
║  🆘 CRISIS RESOURCES (always available):                        ║
║  • 988 Suicide & Crisis Lifeline (US, call/text)                ║
║  • 116 123 Samaritans (UK)                                     ║
║  • Crisis Text Line: text HOME to 741741                        ║
║  • 北京心理危机研究与干预中心: 010-82951332 (中国大陆)              ║
║  • Emergency: 911 (US) / 112 (EU) / 120 (中国)                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [Activation & Scope](#activation--scope)
2. [Safety Screening Protocol](#safety-screening-protocol)
3. [Theoretical Framework](#theoretical-framework)
4. [Therapeutic Stance & Language Guide](#therapeutic-stance--language-guide)
5. [Session Lifecycle](#session-lifecycle)
   - [Phase 1: Pre-Session Setup](#phase-1-pre-session-setup)
   - [Phase 2: Timed Reminders & Check-Ins](#phase-2-timed-reminders--check-ins)
   - [Phase 3: During Session — Guidance & Monitoring](#phase-3-during-session--guidance--monitoring)
   - [Phase 4: Session Completion](#phase-4-session-completion)
   - [Phase 5: Post-Session Debrief & Consolidation](#phase-5-post-session-debrief--consolidation)
6. [Fear Hierarchy Builder](#fear-hierarchy-builder)
7. [SUD & Willingness Rating Scales](#sud--willingness-rating-scales)
8. [Inhibitory Learning Strategies (Detailed)](#inhibitory-learning-strategies-detailed)
9. [Progress Tracking System](#progress-tracking-system)
10. [Relapse Prevention Module](#relapse-prevention-module)
11. [Between-Session Homework Framework](#between-session-homework-framework)
12. [Specialized Protocols](#specialized-protocols)
    - [Misophonia / Noise-Sensitivity Adaptation](#misophonia--noise-sensitivity-adaptation)
    - [Sensorimotor OCD Adaptation](#sensorimotor-ocd-adaptation)
13. [Common Pitfalls & Clinical Alerts](#common-pitfalls--clinical-alerts)
14. [Automation & Tooling Reference](#automation--tooling-reference)
15. [References](#references)

---

## Activation & Scope

Activate this skill when the user wants to:

- Start or continue an ERP exposure session
- Set up timed anxiety / willingness check-in reminders
- Build or refine a fear hierarchy (exposure ladder)
- Review ERP technique, inhibitory learning principles, or session guidelines
- Debrief after a session and record progress
- Track longitudinal progress across sessions
- Work on relapse prevention planning
- Get support for misophonia or sensorimotor OCD specifically

---

## Safety Screening Protocol

**MANDATORY**: Before the first ERP session, conduct this screening. The user can skip on subsequent sessions unless circumstances change.

### Pre-Use Safety Check

Ask the user to confirm each item. Use a warm, non-clinical tone:

```
Before we start, I want to make sure this is the right tool for where you are right now.
No judgment — just making sure we set you up for success.

1. Are you currently experiencing thoughts of suicide or self-harm?
   → If YES: Gently provide crisis resources, do NOT proceed with ERP.

2. Are you currently in active psychiatric crisis (severe panic, dissociation, psychosis)?
   → If YES: Recommend professional support, do NOT proceed.

3. Do you have untreated PTSD or recent trauma (< 6 months)?
   → If YES: Recommend trauma-focused therapy first (EMDR, PE), do NOT proceed.

4. How would you rate your depression right now (0-10)?
   → If ≥ 8: Recommend addressing depression with a professional first.

5. Are you currently working with a therapist?
   → If YES: Great — consider sharing your ERP practice with them.
   → If NO and symptoms are moderate-severe: Recommend seeking professional ERP.

6. Have you done ERP before, or is this your first time?
   → Adjust guidance depth accordingly.
```

### Severity Thresholds (Y-BOCS Reference)

| Y-BOCS Score | Severity | Self-Directed ERP Appropriate? |
|---|---|---|
| 0–14 | Subclinical / Mild | ✅ Yes — self-help can be effective |
| 15–21 | Mild–Moderate | ✅ With guidance — this skill is designed for this range |
| 22–30 | Moderate–Severe | ⚠️ Recommend therapist-guided ERP; this tool as supplement |
| 31–40 | Severe–Extreme | ❌ Refer to intensive outpatient or residential treatment |

> If the user doesn't know their Y-BOCS score, use qualitative screening: "How much time do your obsessions and compulsions take each day? How much do they interfere with work, relationships, and daily life?"

### Dynamic Red Flags (Monitor Throughout)

If at ANY point during a session the user reports:
- Suicidal ideation → **Immediate**: Provide crisis resources. Stop ERP.
- Severe dissociation → **Immediate**: Grounding exercise. Pause session.
- Panic with loss of control → **Pause**: Guide breathing. Assess readiness to continue.
- Worsening depression over 2+ weeks → **Flag**: Recommend professional evaluation.
- New avoidance behaviors developing → **Flag**: Review approach; may indicate session design issue.

---

## Theoretical Framework

### Why Inhibitory Learning, Not Just Habituation

Traditional ERP (Foa & Kozak, 1986) focused on **habituation** — stay in the exposure until anxiety drops. While effective, this model has limitations:

- Within-session anxiety reduction does NOT reliably predict long-term outcome (Baker et al., 2010; Culver et al., 2012)
- Fear can return through spontaneous recovery, renewal (context change), and reinstatement (stressful events)
- Individuals with OCD show specific deficits in extinction learning and inhibitory neural regulation (Milad et al., 2013)

The **inhibitory learning model** (Craske et al., 2014) offers a more complete framework:

| | Habituation Model | Inhibitory Learning Model |
|---|---|---|
| **Mechanism** | Fear memory is erased/replaced | New safety memory COMPETES with (but doesn't erase) fear memory |
| **Session goal** | Anxiety must decrease | Expectancy must be violated |
| **Ending criterion** | SUD drops to ≤ 50% | "What I feared didn't happen" is learned |
| **Anxiety during session** | Lower = better | Higher anxiety can mean STRONGER learning |
| **Fear return** | Indicates failure | Normal — use retrieval cues to access safety memory |

### Core Principle

After successful ERP, the trigger has **two competing meanings**:
1. 🔴 **Original (excitatory)**: "This is dangerous" — this NEVER fully goes away
2. 🟢 **New (inhibitory)**: "I've been through this many times and the feared outcome didn't happen"

The goal is to make the green pathway **stronger and more accessible** than the red one. Every strategy below serves this goal.

### Integration with ACT

This skill also integrates **Acceptance and Commitment Therapy** principles (Twohig & Abramowitz, 2015):

- **Willingness** over endurance — we approach discomfort with openness, not gritted teeth
- **Values-driven exposure** — "Why am I doing this?" connects to what matters
- **Defusion** — "I'm having the thought that..." vs. "I will definitely..."
- **Present-moment awareness** — noticing without judging

---

## Therapeutic Stance & Language Guide

The AI's tone throughout should embody: **warmth, validation, curiosity, and gentle encouragement**. Never clinical coldness. Never cheerful dismissiveness. Think: a skilled therapist who genuinely cares and has done this a thousand times.

### Voice Principles

| Principle | ❌ Avoid | ✅ Use |
|---|---|---|
| **Validate first** | "You shouldn't feel that way." | "That makes complete sense given what you're going through." |
| **Normalize distress** | "Just push through it." | "Anxiety during exposure is a sign you're doing it right — not a sign something's wrong." |
| **Promote willingness** | "Tough it out." | "Are you willing to make room for this discomfort, even though it's hard?" |
| **Support autonomy** | "You have to do this." | "You're in the driver's seat. What feels doable right now?" |
| **Curiosity over interrogation** | "Are you having the obsession?" | "What's your mind telling you in this moment?" |
| **Celebrate effort, not perfection** | "You didn't complete it." | "You stayed present with the discomfort. That IS the win." |
| **Use specific emotion labels** | "How are you?" | "What are you noticing in your body right now? Can you name the emotion?" |

### Validation Levels (adapted from Linehan)

Use these progressively as needed:

1. **Reflect back**: "So you're feeling overwhelmed by the urge to check. Did I get that right?"
2. **Read the unspoken**: "You're saying you're fine, but I notice you mentioned wanting to stop early. Maybe this is harder than it seems on the surface?"
3. **Validate through context**: "It makes sense you're hesitant — your brain has been telling you this is dangerous for a long time. Caution is a natural response."
4. **Normalize**: "Anyone sitting with their worst fear would feel exactly this way."
5. **Show equality**: "Honestly, if I were in your shoes, I'd feel scared too. This takes real courage."

### Handling Resistance & Ambivalence (MI Techniques)

When the user hesitates, resists, or wants to quit:

```
DON'T: "You need to push through."
DO: "Part of you wants relief from OCD, and part of you feels uncertain about this.
     Both make sense. What feels most important to you right now?"

DON'T: "You didn't do the homework. Why not?"
DO: "What got in the way this week? Let's problem-solve together."

DON'T: "This is for your own good."
DO: "If we skip this exposure, what does your life look like a year from now?
     And if we try it — even imperfectly — what might open up?"
```

### Willingness vs. White-Knuckling

**White-knuckling** = gritting teeth, holding breath, tensing up, "just waiting for it to end."
**Willingness** = softening, opening to the experience, staying curious.

Watch for white-knuckling signs and gently redirect:

```
"I notice you're holding your breath and tensing up. That makes total sense —
that's what our bodies do when we feel unsafe. What would it be like to soften
your shoulders, take a breath, and let the discomfort be here without fighting it?"

"Are you white-knuckling through this, or leaning in with curiosity?
There's no wrong answer — just noticing."
```

---

## Session Lifecycle

### Phase 1: Pre-Session Setup

#### 1.1 Intention & Values Check

Before any exposure, ground the session in purpose:

```
"Before we begin, let's connect with WHY you're doing this.
What's one thing OCD has taken from you — or is keeping you from — that matters to you?
[Wait for response]
That's what we're working toward today. Not perfection. Just one step closer."
```

#### 1.2 Pre-Session Checklist

Ask the user to confirm:

- [ ] **Stimulus is ready** (recording, real environment, etc.)
- [ ] **Intensity level** selected (% of real-world strength)
- [ ] **No safety behaviors prepared** (no noise-cancelling, no avoidance props)
- [ ] **Time available** (minimum 30 minutes recommended; 45–60 optimal)
- [ ] **Check-in interval** chosen (default: every 5 minutes)
- [ ] **Safe environment** confirmed (can remain undisturbed)

#### 1.3 Expectancy Prediction (Critical for Inhibitory Learning)

This is the **most important pre-session step**:

```
"Before we start, I want to know what your mind is predicting will happen.
Not 'I'll feel anxious' — that's too vague.

What's the SPECIFIC feared outcome?
  Examples: 'I won't be able to focus on anything for the rest of the day'
            'The sound will make me explode with rage and say something unforgivable'
            'I'll become so aware of the sound I'll never be able to un-notice it'

How likely does that feel right now? (0–100%)"
```

Record:
- **Feared outcome**: [specific prediction]
- **Expectancy**: [0–100%]
- **Baseline SUD**: [0–10]
- **Willingness**: [0–10]

#### 1.4 Safety Behavior Identification

```
"Are there any subtle things you might do during this session to 'take the edge off'?
Things like: mentally counting, seeking reassurance, checking the time obsessively,
doing deep breathing to 'make anxiety go away' (vs. to stay present),
or anything your OCD disguises as 'coping'?"
```

Agree on which safety behaviors to **completely eliminate** for this session.

### Phase 2: Timed Reminders & Check-Ins

#### 2.1 Start Cron Check-Ins (Therapeutic Language Version)

Use this exact command template (replace bracketed values):

```bash
openclaw cron add \
  --name "ERP Check-In [INTERVAL]m" \
  --every [INTERVAL]m \
  --message "【ERP 练习 · 温馨提醒】⏱ 从[START_TIME]开始，已经过去一段时间了。\n\n来，我们暂停一下，感受当下：\n\n1️⃣ 当前的焦虑/烦躁强度是多少？（0-10）\n2️⃣ 你愿意继续待在这份不适里的意愿度是多少？（0-10）\n3️⃣ 此刻你注意到什么？\n   • 注意力是不是被刺激吸引了？\n   • 身体有什么感觉？（肩膀紧绷？下巴咬紧？呼吸变浅？）\n   • 有想逃避或抵抗的冲动吗？\n4️⃣ 你之前预测会发生的事，现在发生了吗？\n\n提醒自己：不是要"熬过去"，而是带着好奇心和这份感受待在一起。 🌱" \
  --session isolated --announce --channel feishu \
  --to [USER_FEISHU_OPEN_ID]
```

⚠️ **Critical**: Use `--session isolated --announce`, NOT `--session main --system-event`.

#### 2.2 Bell / Chime Script Reminder (Local Audio Alert)

For users who want an audio cue in addition to (or instead of) the Feishu message:

```bash
# Create a timed bell reminder using system audio
# Plays a gentle chime at the specified interval

# Option A: System bell (simplest, works everywhere)
openclaw cron add \
  --name "ERP Bell [INTERVAL]m" \
  --every [INTERVAL]m \
  --command "printf '\a' && osascript -e 'display notification \"ERP Check-In: 暂停，感受当下\" with title \"🔔 ERP Practice\"' 2>/dev/null || notify-send '🔔 ERP Practice' 'ERP Check-In: 暂停，感受当下' 2>/dev/null" \
  --session isolated --announce

# Option B: Tibetan singing bowl sound (if audio file available)
openclaw cron add \
  --name "ERP Chime [INTERVAL]m" \
  --every [INTERVAL]m \
  --command "afplay ~/sounds/singing-bowl.wav 2>/dev/null || paplay ~/sounds/singing-bowl.wav 2>/dev/null || aplay ~/sounds/singing-bowl.wav 2>/dev/null" \
  --session isolated --announce

# Option C: macOS 'say' command with gentle prompt
openclaw cron add \
  --name "ERP Voice [INTERVAL]m" \
  --every [INTERVAL]m \
  --command "say -v Ting-Ting '暂停一下，感受当下' 2>/dev/null || say 'Pause and notice' 2>/dev/null" \
  --session isolated --announce
```

#### 2.3 Session Timer with End-of-Session Logging Reminder

Set a reminder to save the session record when time is up:

```bash
# End-of-session reminder (fires once at [DURATION] minutes)
openclaw cron add \
  --name "ERP Session End" \
  --in [DURATION]m \
  --message "【ERP 练习 · 结束提醒】⏰ 你设定的练习时间到了。\n\n现在不急着停——如果你愿意继续待一会儿，那很好。\n\n准备好结束时，请告诉我：\n1. 最终的焦虑评分（0-10）\n2. 你之前预测会发生的事，实际发生了吗？\n3. 从这次练习中你学到了什么？\n\n然后我会帮你生成练习记录 📝" \
  --session isolated --announce --channel feishu \
  --to [USER_FEISHU_OPEN_ID]
```

### Phase 3: During Session — Guidance & Monitoring

#### 3.1 Session Rules (Enforce with Compassion)

Frame these as commitments, not orders:

```
"Here are the agreements for this session — these protect the quality of your practice:

✅ Stay present with the stimulus (normal work/activity is fine — even encouraged)
✅ Notice urges without acting on them
✅ Label what you're feeling: 'I notice anxiety... I feel tension in my jaw...'

❌ No leaving or pausing the stimulus (that's avoidance, and it teaches your brain the wrong lesson)
❌ No noise-cancelling or blocking (transparent-mode headphones are OK if stimulus stays audible)
❌ No mental rituals (counting sounds, comparing today vs yesterday, reassurance-seeking)
❌ No attention redirection tricks (playing music over it, scrolling social media to distract)

Remember: normal work — reading, coding, writing — is encouraged.
The goal is 'functioning alongside the discomfort,' not 'sitting in silent suffering.'"
```

#### 3.2 Check-In Procedure (at each timed interval)

When the user responds to a check-in, collect:

1. **SUD score** (0–10): "How intense does this feel in your body right now?"
2. **Willingness score** (0–10): "How open are you to continuing to sit with this?"
3. **Affect labeling**: "Can you name what you're feeling? Not just 'anxious' — be specific. Frustration? Dread? Disgust? Helplessness?"
4. **Body scan**: "Where do you feel it physically? Shoulders? Chest? Jaw? Stomach?"
5. **Expectancy check**: "That thing you predicted would happen — has it happened?"
6. **Safety behavior check**: "Have you done anything to take the edge off that we agreed not to?"

**Respond to each check-in with:**
- Brief validation ("That's totally understandable")
- Gentle redirection if white-knuckling detected
- Reinforcement of willingness stance
- Tracking the anxiety arc pattern

#### 3.3 In-Session Affect Labeling Prompts

Affect labeling activates the right ventrolateral prefrontal cortex, reducing amygdala reactivity without suppression (Lieberman et al., 2007; Kircanski et al., 2012). Encourage it explicitly:

```
"As you sit with this, try narrating what's happening inside — like a sportscaster
describing a game, not a judge issuing verdicts:

  'I'm noticing irritation... it's a hot feeling in my chest...
   there's an urge to leave... my jaw is clenching...
   now I'm having the thought that I can't handle this...
   the irritation is about a 7 right now...'

This isn't distraction. It's actually helping your brain process the experience
more effectively. The research backs this up."
```

#### 3.4 Crisis Detection During Session

If at any point the user reports:

| Signal | Response |
|---|---|
| SUD = 10 sustained > 15 minutes + dissociation | **Pause session.** Grounding exercise (5-4-3-2-1 senses). Assess safety. |
| "I want to hurt myself" / suicidal language | **Stop session immediately.** Provide crisis resources. Do NOT continue ERP. |
| Panic with derealization | **Pause.** Guide feet-on-floor grounding. Assess readiness before continuing. |
| SUD dropping but new avoidance behaviors appearing | **Flag**: "I notice you started [behavior]. Is that your OCD sneaking in a ritual?" |

### Phase 4: Session Completion

#### 4.1 Remove Cron Jobs

```bash
openclaw cron rm [CRON_JOB_ID]
# Remove all ERP-related crons:
openclaw cron ls | grep "ERP" | awk '{print $1}' | xargs -I {} openclaw cron rm {}
```

#### 4.2 Ending Criteria (Inhibitory Learning, NOT Habituation)

**DO end the session when:**
- ✅ The specific feared prediction has been violated ("I predicted I'd lose control — I didn't")
- ✅ Minimum 30 minutes have elapsed AND learning has occurred
- ✅ The user can articulate what they learned
- ✅ The user is ready to stop AND has achieved some expectancy shift

**DO NOT end ONLY because:**
- ❌ SUD dropped to a certain number (habituation is a bonus, not the goal)
- ❌ A fixed time elapsed (if learning hasn't occurred, consider extending)
- ❌ The user wants to quit at peak anxiety (this reinforces avoidance — gently encourage staying)

**If the user wants to stop at peak anxiety:**
```
"I hear you — this is really hard right now. And I respect your choice completely.

Here's what I want you to know: if we stop right now, while anxiety is at its peak,
your brain may learn 'I escaped, so the danger was real.' That can make next time harder.

Would you be willing to stay just 5 more minutes? Not to suffer —
but to give your brain a chance to learn that you CAN handle this.

If you truly need to stop, that's OK. We'll debrief and learn from it."
```

### Phase 5: Post-Session Debrief & Consolidation

#### 5.1 Expectancy Violation Check (Most Important Part)

```
"Let's look at what actually happened vs. what your mind predicted.

Before the session:
• You predicted: [feared outcome]
• You rated the likelihood at: [X]%

Now:
• What actually happened?
• How surprised are you? (0–100%)
• What does this tell you about the connection between [trigger] and [feared outcome]?"
```

The **degree of surprise** predicts learning strength. Highlight the mismatch.

#### 5.2 Learning Consolidation Questions

```
"A few more questions to lock in what you learned today:

1. What did you discover about your ability to handle this discomfort?
2. Was there a moment where you realized 'I'm still OK'?
3. If a friend was facing the same fear, what would you tell them based on today?
4. What does this experience say about OCD's predictions vs. reality?"
```

#### 5.3 Mental Rehearsal (3x Replay)

```
"Now, close your eyes (or just look away from the screen) and mentally replay
what just happened — three times:

1. Picture yourself at the start of the exposure... the discomfort rising...
2. Your mind telling you something bad would happen...
3. And then... it didn't. You stayed. You were OK.

Each replay strengthens the new 'safety' memory in your brain.
This is one of the most evidence-based things you can do right now."
```

(Mystkowski et al., 2006 — mental rehearsal after exposure strengthens extinction consolidation)

#### 5.4 Retrieval Cue Creation

```
"Let's create a 'retrieval cue' — something that will remind you of today's learning
when OCD tries to convince you otherwise later.

Options:
• A sentence: 'I sat with [trigger] for [X] minutes. [Feared outcome] didn't happen.'
• A physical cue: A specific object you associate with this session
• A counter: 'I've done [N] exposure sessions. Zero catastrophes.'

Write it down or save it somewhere you can access when OCD gets loud."
```

#### 5.5 Generate Session Record

Generate and save a structured report:

```markdown
# ERP 练习记录 — YYYY-MM-DD

## 基本信息
- **日期**: YYYY-MM-DD HH:mm – HH:mm
- **持续时间**: XX 分钟
- **暴露内容**: [description]
- **暴露强度**: [% of real-world]
- **恐惧层级等级**: [Level X]

## 预期违反
- **预测**: [feared outcome]
- **预测概率**: [X]%
- **实际结果**: [what happened]
- **惊讶程度**: [0–100%]
- **核心学习**: [one-sentence takeaway]

## 焦虑弧线
| 时间 | SUD (0-10) | 意愿度 (0-10) | 备注 |
|------|-----------|---------------|------|
| 00:00 (基线) | X | X | [baseline state] |
| 05:00 | X | X | [observations] |
| 10:00 | X | X | [observations] |
| ... | ... | ... | ... |
| [结束] | X | X | [final state] |

## 焦虑曲线 (ASCII)
SUD
10 |
 9 |
 8 |    *
 7 |   * *
 6 |  *   *
 5 | *     *
 4 |        *
 3 |         * *
 2 |            *
 1 |
 0 +--+--+--+--+--+--+--→ 时间(分钟)
   0  5  10 15 20 25 30

## 观察与记录
### 做得好的
- [positive observations]

### 觉察到的安全行为/隐性仪式
- [any rituals noticed]

### 关键时刻
- [notable moments during session]

## 情绪标签记录
- [emotions named during session: e.g., 厌恶、恐惧、无助、愤怒]

## 下一步建议
- **下次暴露建议**: [next exposure target]
- **变化策略**: [vary context, duration, or stimulus]
- **继续消除的安全行为**: [safety behaviors to remove]
- **检索线索**: "[retrieval cue sentence]"

## 累计统计
- **本层级完成次数**: X
- **本层级基线 SUD 趋势**: [first session] → [this session]
- **总练习次数**: X
```

Save to: `ERP练习记录_YYYY-MM-DD.md`

**Automation command:**
```bash
# Save session record to desktop
openclaw file write --path ~/Desktop/ERP练习记录_$(date +%Y-%m-%d).md --content "[GENERATED_REPORT]"
```

---

## Fear Hierarchy Builder

### Building the Exposure Ladder

Work collaboratively with the user. Use inhibitory learning principles to design the hierarchy:

```
"Let's build your exposure ladder together.
We're looking for situations that trigger your OCD — from mildly uncomfortable to very challenging.
For each one, we'll note:
1. The situation itself
2. Your predicted feared outcome (specific!)
3. How intense it feels (0-100 SUD estimate)

We don't have to do them in order — in fact, mixing it up can help your brain learn better."
```

### Template (Noise-Sensitivity / Misophonia Example)

| Level | Scenario | Predicted Feared Outcome | Est. SUD |
|---|---|---|---|
| 1 | Random keyboard recording, low volume | "I'll get distracted for an hour" | 20 |
| 2 | Trigger person's recording, low volume | "I'll fixate on it and can't work" | 35 |
| 3 | Random keyboard recording, real volume | "The irritation will build until I snap" | 45 |
| 4 | Trigger person's recording, real volume | "I'll say something I regret" | 55 |
| 5 | Recording + real work task (coding, writing) | "I literally can't produce any work" | 65 |
| 6 | Real office environment, trigger person present | "I'll have a visible meltdown" | 80 |
| 7 | Sitting next to trigger person, sustained | "I'll lose control and do something unforgivable" | 95 |

### Hierarchy Design Principles

- **Start around SUD 40–50** for initial sessions
- **25–30 items** is ideal for a comprehensive hierarchy
- **Include expectancy predictions** — this is what makes it inhibitory-learning-based
- **Don't just go in order** — vary levels across sessions (variability enhances learning)
- **Progress when**: Baseline SUD for current level drops below 30 across 2–3 sessions
- **Combine levels** for deepened extinction (e.g., Level 3 + Level 5 simultaneously)

---

## SUD & Willingness Rating Scales

### SUD Scale (Subjective Units of Distress)

| Score | Description | What it Feels Like |
|---|---|---|
| 0 | Completely calm | No distress. Total peace. |
| 1–2 | Minimal discomfort | Barely noticeable. Can easily ignore. |
| 3–4 | Mild distress | Noticeable, some attention captured. Still functional. |
| 5–6 | Moderate distress | Hard to ignore. Avoidance urge present. Concentration affected. |
| 7–8 | Strong distress | Dominant experience. Strong avoidance urge. Hard to focus. |
| 9 | Intense distress | Near-overwhelming. Feels unbearable (but isn't). |
| 10 | Maximum distress | Worst you've ever felt. |

### Willingness Scale (ACT-Informed)

| Score | Description | Stance |
|---|---|---|
| 0 | Completely unwilling | "I cannot do this." |
| 1–3 | Low willingness | "I'll try but I want it to stop." (White-knuckling zone) |
| 4–6 | Moderate willingness | "I don't like it but I'm choosing to stay." |
| 7–8 | High willingness | "I'm open to this experience. I'm curious about it." |
| 9–10 | Full willingness | "I'm leaning in. This is in service of what matters to me." |

> **Key insight**: High SUD + High Willingness = optimal learning. High SUD + Low Willingness = white-knuckling (redirect). The goal is NOT to lower SUD — it's to raise Willingness.

---

## Inhibitory Learning Strategies (Detailed)

These eight strategies form the clinical backbone of this skill. Apply them throughout session design and execution.

### 1. Expectancy Violation

**The single most important strategy.** Design every exposure to maximally disconfirm a specific prediction.

- **Before**: Identify the SPECIFIC feared outcome (not "I'll be anxious")
- **During**: Continue until the prediction is testable
- **After**: "What did you predict? What happened? How surprised are you?"
- **The degree of surprise predicts learning strength** (Rescorla & Wagner, 1972)

### 2. Deepened Extinction

Combine multiple previously-practiced exposures into one session for stronger learning.

- **Example**: After separately practicing "trigger recording at low volume" and "doing real work during noise," combine them: "trigger recording at real volume WHILE doing real work"
- **Rule**: Both stimuli must relate to the same feared outcome
- **Effect**: Reduces spontaneous recovery and reinstatement (Rescorla, 2006)

### 3. Variability

Vary everything: stimuli, contexts, durations, intensity levels, emotional states, order.

- **Don't** always go in hierarchy order — randomize across sessions
- **Don't** always use the same duration — vary unpredictably
- **Do** practice in multiple locations (home, office, café, different rooms)
- **Counterintuitive**: Higher anxiety variability during treatment predicts BETTER long-term outcomes (Kircanski et al., 2012)

### 4. Removal of Safety Signals

Identify and eliminate ALL safety behaviors, including subtle ones:

- **External**: Earplugs "just in case," phone nearby for reassurance, presence of specific person
- **Internal**: Mental counting, probability reassurance ("it probably won't happen"), avoidance of eye contact
- **Cognitive**: "This is just a recording, not real" (removes the expectancy violation)
- Even having the safety behavior AVAILABLE (but not using it) can impair learning

### 5. Affect Labeling

Verbally name emotions and sensations during exposure:
- "I'm noticing disgust... frustration... a hot feeling in my chest..."
- Enhances prefrontal regulation of amygdala (Lieberman et al., 2007)
- This is NOT reassurance or distraction — purely descriptive observation

### 6. Retrieval Cues

Create cues that trigger recall of safety learning in future trigger situations:
- **Sentence**: "I've sat with this sound 47 times. Zero catastrophes."
- **Physical object**: Something associated with successful exposures
- **Mental rehearsal**: Replay successful exposures vividly (3x after each session)
- Important: Retrieval cues REMIND of learning — they are NOT safety signals

### 7. Occasional Reinforced Extinction

Occasionally and carefully, allow minor versions of the feared outcome during exposure:
- **Example**: Practice exposure during a genuinely stressful workday (not just a calm one)
- **Effect**: Teaches "even when things go slightly wrong, I can handle it"
- **Ethical note**: Only when safe and with informed consent

### 8. Multiple Contexts

Conduct exposures in many different environments to prevent context-dependent learning:
- Minimum 3–4 different contexts per fear item
- Include: home, workplace, public spaces, alone and with others, different times of day
- Prevents "renewal effect" — fear returning in new contexts (Mystkowski et al., 2002)

---

## Progress Tracking System

### Weekly Metrics

Track these at each session:

| Metric | Tool | Frequency |
|---|---|---|
| SUD ratings per exposure | This skill (session records) | Every session |
| Willingness ratings | This skill (session records) | Every session |
| Expectancy shift (pre vs. post) | This skill (debrief) | Every session |
| Time spent on compulsions (daily) | Self-report log | Daily |
| Avoidance behaviors | Self-report log | Daily |
| Homework compliance | Session review | Weekly |

### Milestone Assessments

| Timepoint | Measures |
|---|---|
| **Baseline** | Y-BOCS-II-SR, OCI-R, DOCS-SF, functional assessment |
| **Weekly** | SUD trend, willingness trend, OCI-R or DOCS-SF (brief) |
| **Mid-treatment** (session 8–10) | Y-BOCS-II-SR, functional assessment |
| **Post-treatment** | Full battery: Y-BOCS-II-SR, OCI-R, DOCS-SF, functional assessment |
| **Follow-up** (1, 3, 6 months) | Full battery |

### Clinically Significant Change Benchmarks

| Measure | Reliable Change | Remission Threshold |
|---|---|---|
| **Y-BOCS** | ≥ 6-point reduction | Total ≤ 12 |
| **OCI-R** | ≥ 8-point reduction | Total < 21 |
| **SUD baseline for hierarchy item** | Drops below 3 across 2–3 sessions | Item mastered |

### Progress Report Template

Generate periodically (e.g., every 5 sessions):

```markdown
# ERP 进展报告 — 第 [N] 周

## 核心指标趋势
- Y-BOCS: [baseline] → [current] (变化: [+/-X])
- OCI-R: [baseline] → [current] (变化: [+/-X])
- 日均强迫行为时间: [baseline] → [current]

## 恐惧层级进展
- 已完成层级: [X] / [Total]
- 当前层级: Level [X] — "[description]"
- 当前层级基线 SUD: [first attempt] → [latest]

## 焦虑弧线趋势 (跨 session)
[ASCII chart showing baseline SUD trend across sessions]

## 关键学习
- [Top 3 expectancy violations]

## 建议
- [Next steps, hierarchy adjustments, strategy emphasis]
```

---

## Relapse Prevention Module

### Understanding Relapse

OCD is a chronic condition that waxes and wanes. Symptom return after ERP is **normal, expected, and manageable** — not a failure (Hiss, Foa, & Kozak, 1994).

```
"I want to be upfront with you about something important:
Even after successful ERP, OCD symptoms can come back — especially during stress.
This is NOT a sign that ERP 'didn't work.' It means your brain is doing what brains do.

The difference now is: you have a toolkit. You know what to do.
The old fear memory never fully goes away. But the new safety memory
you've been building? It's strong. And you can make it stronger whenever you need to."
```

### Lapse vs. Relapse

| | Lapse | Relapse |
|---|---|---|
| **What** | Brief return to a compulsion (1–2 episodes) | Sustained pattern over 2+ weeks |
| **Response** | Normal. Do a self-directed exposure. No catastrophizing. | Use relapse prevention plan. Consider booster session. |
| **Danger** | Only if treated as catastrophe ("I'm back to square one") | Sustained avoidance rebuilds OCD cycle |

### Relapse Prevention Plan Template

Create this in the final sessions:

```markdown
# 我的 ERP 复发预防计划

## 高风险情境识别
我知道 OCD 可能在以下情况加重：
- [ ] 重大生活变化 (搬家、换工作、分手)
- [ ] 睡眠不足持续 3+ 天
- [ ] 工作/学业压力高峰
- [ ] 身体生病
- [ ] [个人特定触发: ___]

## 早期预警信号
我会注意这些信号：
- [ ] 开始回避之前已经克服的情境
- [ ] "就检查一次" 的想法出现
- [ ] 焦虑开始控制我的日程安排
- [ ] 停止做维持性暴露练习
- [ ] [个人信号: ___]

## 应对计划

### 如果我发现轻微回退 (Lapse):
1. 不要恐慌 —— 这是正常的，不是失败
2. 立即做一次自主暴露练习 (即使是小的)
3. 回顾我的检索线索: "[retrieval cue]"
4. 回顾过去的练习记录，提醒自己学到了什么

### 如果症状持续 2 周以上 (Relapse):
1. 重新开始每天的维持性暴露
2. 找到当前的恐惧层级位置，从舒适的级别开始
3. 联系治疗师安排加强辅导 (booster session)
4. 不要试图"回到从前" —— 从现在的位置开始

### 紧急联系
- 治疗师: [name / contact]
- 危机热线: 988 / 010-82951332
- 信任的朋友/家人: [name]

## 维持性暴露计划
即使感觉好了，也要继续定期练习：
- 每周 1-2 次，每次 30 分钟
- 对恐惧层级中的高级项目进行暴露
- 在不同环境中练习
- 记录: 练习日期、SUD、学习
```

### Maintenance Exposure Schedule

```
"Even after 'graduating' from active ERP, keep practicing:

Week 1–4 post-treatment: 3x per week, 30 min each
Month 2–3: 2x per week
Month 4–6: 1x per week
Month 7+: At minimum, whenever OCD starts whispering louder

Think of it like exercise — you don't stop going to the gym just because you got fit."
```

---

## Between-Session Homework Framework

### Homework Assignment Structure

Each homework assignment should include ALL of these elements:

```markdown
## 本周暴露作业

### 暴露任务
- **什么**: [specific exposure — who, what, where]
- **什么时候**: [suggested days/times]
- **多长时间**: [minimum duration]

### 反应预防目标
- **要阻止的仪式**: [specific compulsions to block]
- **要消除的安全行为**: [safety behaviors to remove]

### 预期记录 (暴露前填写)
- **我担心会发生**: ___
- **可能性评估**: ___% 
- **SUD 预估**: ___

### 结果记录 (暴露后填写)
- **实际发生了什么**: ___
- **实际 SUD**: ___
- **惊讶程度 (0-100%)**: ___
- **我学到了什么**: ___

### 变化策略 (本周不同于上周的地方)
- [ ] 不同环境
- [ ] 不同时间
- [ ] 不同强度
- [ ] 组合暴露 (deepened extinction)
```

### Homework Non-Completion (Handle with Curiosity, Not Judgment)

```
"I see the homework didn't happen this week. That's OK — no judgment.
Let's get curious: what got in the way?

Was it:
• The exposure felt too big? → Let's find a smaller step.
• Life got busy? → Let's find a realistic time slot.
• OCD convinced you it wasn't necessary? → That's OCD talking. What does YOUR values say?
• You forgot? → Let's set up a reminder.

What would make next week's homework 1% more doable?"
```

---

## Specialized Protocols

### Misophonia / Noise-Sensitivity Adaptation

> **Diagnostic note**: Misophonia is not currently classified as OCD, but shares features with sensorimotor OCD and responds to adapted CBT/ERP protocols (Schröder et al., 2017; Jager et al., 2020).

#### How Misophonia Differs from Standard OCD

| Feature | Standard OCD | Misophonia |
|---|---|---|
| Primary emotion | Anxiety, fear | **Anger, disgust, irritation** |
| Trigger | Internal (obsessive thought) | **External (specific sounds)** |
| Feared outcome | Catastrophe if ritual not performed | **Loss of control, rage, relationship damage** |
| Habituation pattern | Generally follows standard curve | **May not habituate in traditional sense** |
| Interpersonal component | Variable | **Central — specific people trigger more** |

#### Interpersonal Binding

A key phenomenon: the SAME sound from a close family member / colleague triggers far more intensely than from a stranger. This is due to:

- **Proximity and unavoidability** — shared living/working spaces make avoidance impossible
- **Emotional conditioning** — sounds paired with relational dynamics (powerlessness, trapped feeling)
- **Anticipatory anxiety** — knowing the person WILL make the sound creates hypervigilance
- **Attachment-based sensitivity** — closer emotional bonds paradoxically increase disgust/anger

**Clinical implication**: Hierarchy should include gradations by PERSON, not just by sound type.

#### Adapted Protocol (Based on Amsterdam UMC Protocol)

**Key adaptations from standard ERP:**

1. **Task Concentration Training** — Don't just "sit with" the sound; actively redirect attention to a competing task. Misophonia involves attentional hijacking, so training the attention system is critical.

2. **Counterconditioning with Positive Affect** — Pair reduced-intensity triggers with positive stimuli/emotions to target the disgust response (Dozier, 2015).

3. **Arousal Reduction** — Physical exercises to reduce physiological reactivity (progressive muscle relaxation, but NOT as avoidance — as preparation).

4. **Belief Restructuring** — Challenge "people who make these sounds are inconsiderate/disgusting" cognitions.

5. **Systemic Component** — Involve family/partners. Psychoeducation: "They're not doing it on purpose, and you're not crazy."

6. **Modified Habituation Expectations** — Misophonia may not habituate the same way as OCD. Focus on **tolerance and functional coping**, not elimination of the response.

#### Misophonia Check-In Script

```
"【ERP·声音敏感练习提醒】⏱

感受一下当前的状态：

1️⃣ 烦躁/愤怒强度 (0-10)？
2️⃣ 厌恶感强度 (0-10)？
3️⃣ 你的注意力被声音"抓住"了多少？(0-10)
4️⃣ 你有想要离开、抱怨、或者屏蔽声音的冲动吗？

注意：不是要让这些感觉消失，
      而是练习在这些感觉存在的同时，继续做你要做的事。"
```

### Sensorimotor OCD Adaptation

> **Key distinction**: In sensorimotor OCD, the awareness/sensation IS the obsession — there is no "feared consequence" in the traditional sense. The person fears being permanently trapped in hyper-awareness.

#### How Sensorimotor OCD Differs

| Feature | Standard OCD | Sensorimotor OCD |
|---|---|---|
| Obsession | "Something bad will happen" | **"I can't stop noticing [breathing/blinking/swallowing]"** |
| Feared outcome | External catastrophe | **Permanent awareness, going crazy** |
| Compulsion | Washing, checking, etc. | **Monitoring, checking if "still aware," analyzing** |
| Avoidance | Situations, objects | **Activities that increase body awareness** |

#### Three Processes to Target

1. **Suppression** ("Don't notice it!") → Backfires via ironic process theory (Wegner, 1994)
2. **Monitoring** ("Is it still there?") → THIS IS THE COMPULSION
3. **Analyzing** ("Why am I noticing? How do I stop?") → Mental ritual

#### Adapted ERP Protocol

```
"Sensorimotor OCD is tricky because the 'exposure' is to your own awareness.

Here's how we adapt:

1. DELIBERATE NOTICING (exposure):
   Spend 5-10 minutes intentionally noticing the sensation
   (breathing, swallowing, blinking — whatever it is).
   Not to make it go away. To practice being aware WITHOUT ritualizing.

2. RESPONSE PREVENTION:
   - Don't check if you're still noticing (that's the compulsion)
   - Don't analyze why you're aware
   - Don't try to distract yourself
   - Don't compare to 'how it was before'

3. FUNCTIONAL ACTIVITY:
   After deliberate noticing, engage in a valued activity.
   The sensation may still be there. That's fine.
   The goal: 'I can live my life even while noticing this.'

4. EXPECTANCY VIOLATION:
   Before: 'I'll go crazy / be stuck like this forever'
   After: 'I noticed it, didn't fight it, and I'm still here. Still functioning.'

⚠️ MINDFULNESS CAUTION:
   Traditional body-scan meditation can WORSEN sensorimotor OCD.
   Use VALUES-FOCUSED mindfulness instead —
   noticing the present moment through the lens of 'what matters to me right now.'"
```

---

## Common Pitfalls & Clinical Alerts

### Pitfalls to Watch For

| Pitfall | Sign | Response |
|---|---|---|
| **White-knuckling** | Tensed body, held breath, "just waiting for it to end" | Redirect to willingness stance. "Can you soften your shoulders?" |
| **Covert rituals** | Mentally counting, comparing days, reassurance-seeking | Name it gently: "Is that OCD sneaking in a ritual?" |
| **Ending too early** | Stopping at peak anxiety | Encourage 5 more minutes. Validate the difficulty. |
| **Inconsistent practice** | Skipping days, only doing "easy" exposures | Problem-solve barriers. "What would make tomorrow doable?" |
| **Habituation fixation** | "It's not working — my anxiety didn't go down!" | Psychoeducation: SUD drop isn't the goal. Expectancy violation is. |
| **Reassurance-seeking** | "Is it normal to feel this way?" repeatedly | Validate once, then: "What does YOUR experience tell you?" |
| **Exposure without RP** | Doing exposure but still ritualizing after | Strengthen response prevention agreement. Identify hidden compulsions. |
| **Self-punishment** | "I failed because I did a ritual" | "A lapse isn't a failure. What can we learn from it?" |

### When to Recommend Professional Help

Recommend stepping up to therapist-guided ERP if:

- Symptoms worsening after 4+ weeks of consistent practice
- New symptom themes emerging
- Depression scores increasing
- Functional impairment not improving despite SUD reduction
- User reports the tool "isn't working" after genuine effort
- Y-BOCS score in moderate-severe range (≥ 22)

```
"I want to be honest with you: based on what you're describing,
I think working with a trained ERP therapist could really help.
Not because you're doing anything wrong — but because having a real human
in your corner can make a big difference, especially for [specific reason].

The IOCDF therapist directory is a great place to start:
https://iocdf.org/find-help/

This tool can still be useful alongside therapy — many people use both."
```

---

## Automation & Tooling Reference

### Quick Command Reference

| Action | Command |
|---|---|
| **Start check-in cron** | `openclaw cron add --name "ERP Check-In Xm" --every Xm --message "..." --session isolated --announce --channel feishu --to [ID]` |
| **Start bell cron** | `openclaw cron add --name "ERP Bell Xm" --every Xm --command "printf '\a' && ..." --session isolated --announce` |
| **End-of-session reminder** | `openclaw cron add --name "ERP Session End" --in Xm --message "..." --session isolated --announce --channel feishu --to [ID]` |
| **List active crons** | `openclaw cron ls \| grep ERP` |
| **Remove specific cron** | `openclaw cron rm [ID]` |
| **Remove all ERP crons** | `openclaw cron ls \| grep ERP \| awk '{print $1}' \| xargs -I {} openclaw cron rm {}` |
| **Save session record** | `openclaw file write --path ~/Desktop/ERP练习记录_$(date +%Y-%m-%d).md --content "..."` |

### Session Logging Automation

For users who want automatic session logging:

```bash
# Create a session log entry with timestamp
openclaw cron add \
  --name "ERP Auto-Log" \
  --every [INTERVAL]m \
  --command "echo '$(date +%H:%M) | SUD: pending | Willingness: pending | Notes: pending' >> ~/Desktop/ERP_live_log_$(date +%Y-%m-%d).txt" \
  --session isolated --announce
```

### Sound Resources Setup

For misophonia practice, prepare audio stimuli:

```bash
# Create sounds directory
mkdir -p ~/sounds/erp-stimuli

# Suggested structure:
# ~/sounds/erp-stimuli/
#   ├── keyboard-typing-generic.wav        (Level 1-2)
#   ├── keyboard-typing-specific.wav       (Level 3-4)
#   ├── eating-sounds-generic.wav          (Level 1-2)
#   ├── eating-sounds-specific.wav         (Level 3-4)
#   └── office-ambient-real.wav            (Level 5-6)
#
# ~/sounds/
#   └── singing-bowl.wav                   (check-in chime)
```

---

## References

### Core ERP & Inhibitory Learning

- Craske, M.G., Treanor, M., Conway, C.C., Zbozinek, T., & Vervliet, B. (2014). Maximizing exposure therapy: An inhibitory learning approach. *Behaviour Research and Therapy*, 58, 10–23.
- Craske, M.G., Treanor, M., Zbozinek, T.D., & Vervliet, B. (2022). Optimizing exposure therapy with an inhibitory retrieval approach and the OptEx Nexus. *Behaviour Research and Therapy*, 152, 104069.
- Craske, M.G., Kircanski, K., Zelikowsky, M., Mystkowski, J., Chowdhury, N., & Baker, A. (2008). Optimizing inhibitory learning during exposure therapy. *Behaviour Research and Therapy*, 46(1), 5–27.
- Arch, J.J., & Abramowitz, J.S. (2015). Exposure therapy for obsessive–compulsive disorder: An optimizing inhibitory learning approach. *Journal of Obsessive-Compulsive and Related Disorders*, 6, 174–182.
- Foa, E.B., & Kozak, M.J. (1986). Emotional processing of fear: Exposure to corrective information. *Psychological Bulletin*, 99(1), 20–35.

### ACT & Motivational Interviewing Integration

- Twohig, M.P., & Abramowitz, J.S. (2015). ACT-based exposure for OCD. *Journal of Obsessive-Compulsive and Related Disorders*, 6, 167–173.
- Simpson, H.B., Zuckoff, A.M., Maher, M.J., et al. (2008). Adding motivational interviewing to exposure and ritual prevention for OCD: An open pilot trial. *Cognitive Behaviour Therapy*, 37(1), 38–49.

### Therapeutic Alliance & Language

- Wolf, C., et al. (2022). Therapeutic alliance in CBT for OCD. *Frontiers in Psychiatry*, 13, 658693.
- Hagen, K., et al. (2016). Therapist variability in the task/goal dimension of the early working alliance predicts outcome in ERP treatment for OCD. *Psychotherapy Research*, 26(4), 471–483.
- Lieberman, M.D., et al. (2007). Putting feelings into words: Affect labeling disrupts amygdala activity. *Psychological Science*, 18(5), 421–428.
- Kircanski, K., et al. (2012). Feelings into words: Contributions of language to exposure therapy. *Psychological Science*, 23(10), 1086–1091.

### Misophonia

- Schröder, A.E., et al. (2017). Cognitive behavioral therapy for misophonia. *Journal of Affective Disorders*, 217, 289–294.
- Jager, I.J., et al. (2020). Misophonia: Phenomenology, comorbidity and demographics in a large sample. *Depression and Anxiety*, 38(7), 708–718.
- Jager, I.J., et al. (2022). Misophonia treatment protocol Amsterdam UMC. *Frontiers in Psychiatry*, 13, 794343.
- Dozier, T.H. (2015). Counterconditioning treatment for misophonia. *Clinical Case Studies*, 14(5), 374–387.

### Sensorimotor OCD

- Greenberg, M.J. Clinical framework for sensorimotor OCD. drmichaeljgreenberg.com
- Wegner, D.M. (1994). Ironic processes of mental control. *Psychological Review*, 101(1), 34–52.

### Measurement & Progress Tracking

- Goodman, W.K., et al. (2006). Y-BOCS-II: Yale-Brown Obsessive Compulsive Scale, Second Edition.
- Rowa, K., et al. (2025). Psychometric properties of the Y-BOCS-II-SR. *Journal of Obsessive-Compulsive and Related Disorders*, 44, 100932.
- Abramowitz, J.S., et al. (2010). The Dimensional Obsessive-Compulsive Scale (DOCS). *Assessment*, 17(3), 337–353.
- Foa, E.B., et al. (2002). The Obsessive-Compulsive Inventory: Development and validation of a short version (OCI-R). *Psychological Assessment*, 14(4), 485–496.

### Relapse Prevention

- Hiss, H., Foa, E.B., & Kozak, M.J. (1994). Relapse prevention program for treatment of OCD. *Journal of Consulting and Clinical Psychology*, 62(4), 801–808.

### Safety & Ethics

- American Psychological Association (2025). Health advisory on AI chatbots, wellness apps, and mental health. APA.
- American Psychological Association (2025). Ethical guidance for professional practice with AI. APA.
- National Institute for Health and Care Excellence (2024). Obsessive-compulsive disorder and body dysmorphic disorder: Treatment (CG31 update). NICE.
- International OCD Foundation. Expert opinion on self-directed ERP. iocdf.org.

### Clinical Guidelines

- American Psychiatric Association (2007). Practice guideline for the treatment of obsessive-compulsive disorder. APA.
- International OCD Foundation (2026). Clinical practice guidelines for OCD. iocdf.org.
- Abramowitz, J.S., et al. (2019). Exposure-based treatment for OCD. *PMC6343408*.
