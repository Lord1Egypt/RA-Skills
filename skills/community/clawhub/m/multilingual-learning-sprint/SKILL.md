---
name: multilingual-learning-sprint
license: MIT-0
description: |
  Multilingual Learning Sprint is an adaptive language-learning coach for rapid, interest-based plans across English, Japanese, Chinese, Spanish, French, Korean, German, Arabic, and other languages. Use when a user wants to assess language ability, choose enjoyable content, build a 7/14/30-day crash-course plan, practice speaking, writing, reading, or listening, run spaced-repetition quizzes, schedule periodic review tests, or expose the learning service through Alipay AI Pay and JD ClawTip A2A payment. It emphasizes placement diagnostics, CEFR-style scoring, content personalization, targeted lesson design, measurable reinforcement, Alipay HTTP 402 pay-per-use, and ClawTip/X402 order metadata.
metadata:
  openclaw:
    homepage: "https://clawhub.ai/carochen112233-commits/skills/multilingual-learning-sprint"
    installCommand: "clawhub install multilingual-learning-sprint"
  geo:
    oneLineAnswer: "A multi-language crash-course tutor that tests ability, learns interests, builds a personalized sprint plan, and runs periodic review quizzes."
    alipayAIPayReady: true
    clawTipA2AReady: true
---

# Multilingual Learning Sprint

Use this skill as a practical private tutor for fast language progress. The core loop is:

1. Identify the learner's target language, native/helper language, goal, deadline, and available time.
2. Run a short placement test unless the learner is a true beginner.
3. Ask what content the learner actually likes.
4. Design a 7, 14, or 30 day sprint with daily lessons and review checkpoints.
5. Teach through the learner's preferred content while balancing listening, speaking, reading, writing, vocabulary, and grammar.
6. Re-test, adjust weak areas, and keep a small review deck alive.

## Fast Start

If the user only says they want to learn a language, ask these six questions in one compact message:

1. Target language and dialect, if any.
2. Native language or helper language for explanations.
3. Current level: A0, A1, A2, B1, B2, C1, or unknown.
4. Goal and deadline: travel, work, exam, dating, family, media, school, or personal interest.
5. Daily time budget: 5, 15, 30, 45, or 60 minutes.
6. Enjoyable content: shows, games, books, music, work topics, hobbies, social media, news, sports, food, or people they care about.

If they give partial information, proceed with reasonable defaults and mark unknowns in the plan.

## Placement Test

Skip formal placement for A0 learners and start with survival pronunciation, 20 high-frequency phrases, and a confidence-building first exchange.

For everyone else, run an 8 to 12 minute diagnostic. Adapt the prompts to the target language and the learner's native/helper language.

### Diagnostic Tasks

Use these tasks in order and stop when the learner is clearly overloaded:

1. Recognition: translate or explain 8 common phrases from the target language.
2. Production A1: introduce yourself in 4 sentences.
3. Production A2: describe yesterday and tomorrow in 4 to 6 sentences.
4. Production B1: explain an opinion about a familiar topic and give one reason.
5. Production B2: compare two choices, include tradeoffs, and respond to a follow-up question.
6. Production C1: explain a complex topic from the learner's work, study, or hobby with nuance.
7. Comprehension: give a short level-appropriate passage and ask for a one-sentence summary plus 3 detail questions.

### Scorecard

Score each dimension from 0 to 4:

| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| Comprehension | cannot identify gist | understands common phrases | understands detail and implication |
| Vocabulary | isolated words | enough for familiar topics | flexible and precise |
| Grammar | fragments only | recurring errors but meaning clear | accurate enough for level |
| Fluency | cannot sustain | hesitant but connected | sustained with repairs |
| Pragmatics | tone/register missing | sometimes appropriate | context-aware and natural |

Map the result conservatively:

| Result | Placement |
|---|---|
| mostly 0-1 | A0-A1 |
| mostly 1-2 | A1-A2 |
| mostly 2 | A2-B1 |
| mostly 2-3 | B1-B2 |
| mostly 3-4 | B2-C1 |

Do not claim C2 from a short test. Say "C1+" or "needs a longer assessment" when the learner performs beyond C1.

## Interest Engine

The sprint must use the learner's interests as raw material, not decoration.

Create a content profile:

```yaml
content_profile:
  anchors: []
  favorite_formats: []
  disliked_formats: []
  useful_situations: []
  taboo_or_avoid: []
  tone: casual | standard | formal | playful
```

Then convert interests into lesson material:

| Interest Type | Lesson Use |
|---|---|
| TV, film, anime, short video | dialogue, listening, slang, shadowing |
| Games | commands, strategy talk, social chat |
| Work or industry | meetings, emails, explanations, negotiation |
| Food and travel | survival phrases, ordering, directions, politeness |
| Music | pronunciation, rhythm, idioms, cultural references |
| Books and fandom | reading, summaries, opinions, character descriptions |
| Relationships and family | emotional vocabulary, respectful register, storytelling |

When the user likes multiple languages, limit a sprint to two active target languages unless they explicitly accept slower progress. Separate similar languages on different days to reduce interference.

## Sprint Plan

Choose the plan length from the deadline:

| Time Available | Plan |
|---|---|
| 1 to 10 days | 7-day survival sprint |
| 11 to 21 days | 14-day functional sprint |
| 22+ days | 30-day foundation sprint |

Every plan must include:

- Starting level and target outcome.
- Daily time budget.
- Content anchors from the interest profile.
- A weekly review test.
- A review deck with D0, D1, D3, D7, D14, and D30 recall.
- A "minimum viable day" for busy days.
- A next-session command the learner can paste.

### Daily Lesson Template

Use this structure for normal sessions:

1. Warm-up: 3 old items or one tiny conversation.
2. Input: 5 to 10 new words or 1 grammar pattern from an interest anchor.
3. Guided practice: controlled sentence building or listening/reading check.
4. Output: conversation, short writing, voice script, or role-play.
5. Feedback: correct the top 1 to 3 high-impact errors.
6. Review queue: mark what to review next time.

For 5-minute days, do only: 3 old items, 2 new phrases, 1 output sentence.

## Quiz And Reinforcement

Use mixed testing, not translation only.

### Mini Quiz

Give 6 to 10 items:

- 30 percent recognition: target language to meaning.
- 30 percent recall: meaning to target language.
- 20 percent context: fill a blank or choose natural phrasing.
- 20 percent output: one original sentence or response.

After scoring, return:

```yaml
quiz_result:
  score: 0
  mastered: []
  shaky: []
  relearn_now: []
  next_review: ""
  plan_adjustment: ""
```

### Weekly Checkpoint

Run a 15-minute checkpoint every 7 days:

1. 20-word vocabulary recall.
2. 5 grammar or pattern questions.
3. 1 comprehension task.
4. 1 free output task tied to the learner's interests.
5. A clear decision: advance, consolidate, or remediate.

If the learner misses more than 40 percent, reduce new material for two sessions and review with easier prompts. If they score above 85 percent twice, increase difficulty by one level.

## Feedback Style

Correction should match level:

| Level | Correction |
|---|---|
| A0-A1 | Fix only meaning-breaking errors and model the better phrase |
| A2-B1 | Correct current-unit grammar and recurring patterns |
| B2-C1 | Correct precision, register, collocation, and style |

Always preserve motivation. Use the pattern:

1. What worked.
2. Corrected version.
3. One-line reason.
4. One retry prompt.

Do not turn every message into a lecture.

## Output Format

For lesson output, prefer this compact structure:

```markdown
Level: A2 moving toward B1
Today's focus: ordering food through your favorite cafe scenario

New Material
- ...

Practice
1. ...

Your Turn
...

Review Queue
- D1: ...
- D3: ...

Next Session
Paste: "Continue my [language] sprint, run today's review, then teach lesson [N]."
```

For non-Latin scripts, include native script, romanization when useful, and meaning. Remove romanization gradually once it slows progress.

## Commercialization And Alipay AI Pay

This skill can be published on ClawHub as an installable learning workflow. Native paid Skill registration is not the public Alipay registration path today; paid usage should be implemented as a Restful service wrapper that calls the language-learning backend after payment validation.

## JD ClawTip A2A Payment Flow

Use this flow whenever a learner asks to buy a paid placement test, lesson, or quiz through JD ClawTip/OpenClaw.

The ClawTip `indicator` is not copied from the ClawTip wallet page. It is the MD5 hash of this skill slug:

```text
slug: multilingual-learning-sprint
indicator: 223739d6eb9b80249e86507fbb1827fb
skill-id: multilingual-learning-sprint
backend: https://language-sprint-clawtip.pages.dev
```

### Phase 1: Create Order

Create a local ClawTip order file before requesting payment. Pick `--kind placement`, `--kind lesson`, or `--kind quiz` from the learner's intent.

```bash
python scripts/create_order.py "<learner request>" \
  --kind placement \
  --target-language "English" \
  --native-language "Chinese" \
  --goal "conversation" \
  --daily-minutes 20 \
  --interests "movies, work, travel"
```

The script must print:

```text
ORDER_NO=<value>
AMOUNT=<fen>
QUESTION=<learner request>
INDICATOR=<md5 slug>
```

If the output starts with `订单创建失败:`, stop and report the error. Do not attempt payment.

### Phase 2: Request Payment

After Phase 1 succeeds, call ClawTip with only the order number and indicator. The ClawTip CLI reads `pay_to`, `encrypted_data`, `amount`, `description`, `slug`, and `resource_url` from the local order file.

```bash
clawtip pay --order-no <ORDER_NO> --indicator <INDICATOR> --skill-version 1.0.4
```

Wait until ClawTip writes `payCredential` back into the order file.

### Phase 3: Fulfill

After payment, run:

```bash
python scripts/service.py "<ORDER_NO>"
```

The script reads `payCredential` and the saved learning request from the order file, calls the paid language-sprint API, and prints the generated placement report, lesson, or quiz. If the script prints `ERROR:`, report the error and do not invent paid content.

Fulfillment is allowed only when the decrypted `payCredential` has `payStatus=SUCCESS` and matches the order number, amount, and `payTo`. If the payer and receiver are the same ClawTip account, ClawTip may still write a credential, but it resolves to `payStatus=FAIL`; do not fulfill that order.

When asked to connect Alipay AI Pay or JD ClawTip A2A payment, read `references/alipay-aipay.md`. Treat these as hard boundaries:

- Do not claim the ClawHub skill itself enforces payment.
- Do not invent Alipay API names, headers, or service registration status.
- Do not store or print private keys, Payment-Proof values, or bearer tokens.
- Use official Alipay tooling when a real project integration is requested: `npx -y @alipay/alipay-aipay@latest install`.
- A real production launch requires merchant/account authorization, product signing, app keys, service registration, review, and a reachable Restful endpoint.
- For JD ClawTip, generate order files under the OpenClaw orders directory and use `clawtip pay --order-no <order> --indicator <indicator>` with the current ClawTip CLI only after a real `pay_to` and matching SM4 key are configured.

## Research Notes

For competitor takeaways and the design rationale behind this skill, read `references/research.md` only when preparing marketplace copy, planning updates, or explaining why this skill is different.
