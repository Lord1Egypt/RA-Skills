# Language Tutor Pro — Agent Skill

> Persistent, conversation-driven language learning with adaptive memory.
> No gamification. No flashcard drills. Just real conversation practice with a tutor that remembers everything.

## Trigger Phrases

Use this skill when the user says any of:
- "language lesson", "language practice", "practice [language]"
- "teach me [language]", "let's speak [language]"
- "vocab review", "vocabulary review", "spaced repetition"
- "grammar help", "grammar lesson"
- "conversation practice", "role play in [language]"
- "language tutor", "tutor session"
- "how's my [language]", "language progress", "learning stats"
- "situation practice", "ordering food in [language]", "job interview in [language]"

Do NOT use this skill for: translation requests (use a dictionary/translator), language identification, or one-off vocabulary lookups unrelated to active learning.

---

## 1. Overview

Language Tutor Pro turns the agent into a private language tutor with persistent memory. It tracks the learner's strengths, weaknesses, vocabulary, grammar mastery, and conversation history across every session. The tutor adapts difficulty in real time, corrects errors in context, and weaves spaced repetition into natural conversation — not disconnected drills.

### Supported Languages

Spanish, French, German, Italian, Portuguese, Japanese, Mandarin Chinese, Korean.

### CEFR Level Framework

All progress is tracked against the Common European Framework of Reference (CEFR):

- **A1 — Beginner:** Basic phrases, greetings, introductions, simple questions
- **A2 — Elementary:** Routine tasks, simple descriptions, basic past/future tense
- **B1 — Intermediate:** Main points on familiar topics, travel situations, opinions with reasons
- **B2 — Upper Intermediate:** Complex texts, fluent interaction, clear detailed writing
- **C1 — Advanced:** Implicit meaning, flexible language use, complex topics
- **C2 — Mastery:** Near-native fluency, nuanced expression, effortless understanding

---

## 2. Data Files

All learner data is stored in the skill's `data/` directory. The setup script creates this structure.

### 2.1 Learner Profile — `data/learner-profile.json`

```json
{
  "native_language": "English",
  "target_languages": [
    {
      "language": "Spanish",
      "current_level": "B1",
      "started": "2026-03-01",
      "goals": ["conversational fluency", "travel preparation"],
      "focus_areas": ["subjunctive mood", "colloquial expressions"],
      "session_preferences": {
        "default_duration_minutes": 20,
        "error_correction": "inline",
        "formality": "informal"
      }
    }
  ],
  "interests": ["cooking", "travel", "technology", "music"],
  "weak_spots": [],
  "total_sessions": 0,
  "current_streak_days": 0,
  "longest_streak_days": 0,
  "last_session_date": null
}
```

### 2.2 Vocabulary Ledger — `data/vocabulary.jsonl`

One JSON object per line. Each entry tracks a word/phrase through spaced repetition.

```jsonl
{"word":"conseguir","translation":"to get/obtain","language":"Spanish","context":"Necesito conseguir los boletos antes del viernes.","level":"B1","added":"2026-03-05","next_review":"2026-03-08","interval_days":3,"ease_factor":2.5,"correct_streak":2,"tags":["verb","irregular"]}
{"word":"sin embargo","translation":"however/nevertheless","language":"Spanish","context":"El restaurante estaba lleno; sin embargo, encontramos una mesa.","level":"B1","added":"2026-03-05","next_review":"2026-03-06","interval_days":1,"ease_factor":2.1,"correct_streak":0,"tags":["conjunction","formal"]}
```

**SRS Fields:**
- `next_review`: ISO date when word is due for review
- `interval_days`: Current interval (starts at 1, grows on success)
- `ease_factor`: SM-2 algorithm ease factor (starts at 2.5, adjusts per recall quality)
- `correct_streak`: Consecutive correct recalls (resets to 0 on failure)

### 2.3 Grammar Tracker — `data/grammar.jsonl`

```jsonl
{"rule":"ser_vs_estar","language":"Spanish","level":"A2","status":"learning","examples_seen":8,"errors":3,"last_error":"2026-03-04","last_practiced":"2026-03-05","notes":"Confuses estar with ser for temporary states. Reviewed with location examples."}
{"rule":"subjunctive_wishes","language":"Spanish","level":"B1","status":"introduced","examples_seen":2,"errors":1,"last_error":"2026-03-05","last_practiced":"2026-03-05","notes":"First exposure. Used quiero que + subjunctive. Got it wrong with esperar que."}
```

**Status progression:** `introduced` → `learning` → `practiced` → `mastered`

### 2.4 Session Log — `data/sessions.jsonl`

```jsonl
{"id":"s_20260305_1","date":"2026-03-05","language":"Spanish","type":"conversation","duration_minutes":18,"topic":"weekend plans","level":"B1","new_vocab":4,"errors_corrected":3,"grammar_points":["subjunctive_wishes","preterite_vs_imperfect"],"notes":"Good fluency on familiar topics. Struggled with subjunctive after esperar. Introduced 4 new food-related verbs."}
```

### 2.5 Conversation History — `data/conversations/`

Full conversation transcripts stored as markdown files: `data/conversations/YYYY-MM-DD-{session_id}.md`

---

## 3. Session Types

### 3.1 Free Conversation

**Trigger:** "Let's practice [language]", "free conversation", "let's chat in [language]"

**Procedure:**

1. Read `data/learner-profile.json` for current level, interests, and weak spots.
2. Read `data/vocabulary.jsonl` for words due for review (where `next_review <= today`).
3. Read `data/grammar.jsonl` for grammar rules in `learning` or `practiced` status.
4. Select a conversation topic based on:
   - Learner's stated interests
   - Current level appropriateness
   - Opportunities to practice weak grammar points
   - Natural integration of review vocabulary
5. Begin the conversation in the target language at the learner's level.
6. Use the **Conversation Engine** rules (Section 4).
7. After the session, run the **Post-Session Protocol** (Section 7).

**Level-Appropriate Conversation Guidelines:**

| Level | Sentence Complexity | Vocab Range | Topics |
|-------|-------------------|-------------|--------|
| A1 | Simple present, basic questions | ~500 most common | Self, family, daily routine, weather |
| A2 | Past tense, basic future, comparisons | ~1000 | Shopping, directions, hobbies, food |
| B1 | Multiple tenses, opinions, conditionals | ~2000 | Travel, work, current events, culture |
| B2 | Complex clauses, idioms, nuance | ~4000 | Abstract topics, debates, professional |
| C1 | Native-speed, implicit meaning, humor | ~8000 | Any topic, nuanced discussion |
| C2 | Full native register including slang | ~15000+ | Any topic at native complexity |

### 3.2 Guided Lesson

**Trigger:** "Teach me [grammar topic]", "lesson on [topic]", "I want to learn [grammar point]"

**Procedure:**

1. Identify the target grammar point or vocabulary theme.
2. Check `data/grammar.jsonl` — has the learner encountered this before?
3. Begin with a brief contextual explanation (2-3 sentences max, in the native language).
4. Provide 2-3 clear examples in the target language with translations.
5. Transition into a short conversation that requires the grammar point.
6. Correct errors using the **Grammar Correction Protocol** (Section 5).
7. After 5-8 exchanges using the rule, summarize what was practiced.
8. Update `data/grammar.jsonl` with the session's results.

**Grammar points by level (examples):**

- **A1:** Articles, gender, basic verb conjugation, greetings, numbers
- **A2:** Past tense, prepositions, comparatives, possessives, question formation
- **B1:** Subjunctive (basic), conditional, relative clauses, reported speech
- **B2:** Subjunctive (advanced), passive voice, idiomatic expressions, register shifting
- **C1:** Nuanced tense distinctions, literary constructions, regional variations
- **C2:** Stylistic choices, rhetorical devices, dialect awareness

### 3.3 Vocab Review (Spaced Repetition)

**Trigger:** "Vocab review", "review my words", "spaced repetition session", or run `scripts/vocab-review.sh`

**Procedure:**

1. Read `data/vocabulary.jsonl` and filter entries where `next_review <= today`.
2. Sort by: overdue items first, then by lowest `ease_factor` (hardest words first).
3. For each word due (target: 10-20 words per session):
   a. Present a natural sentence in the target language using the word — but **replace the target word with a blank**.
   b. The sentence should be different from the original `context` to test genuine recall.
   c. After the learner responds:
      - **Correct:** Increase interval. `interval_days = interval_days * ease_factor`. Bump `ease_factor` by 0.1 (max 3.0). Increment `correct_streak`.
      - **Incorrect:** Reset `interval_days` to 1. Decrease `ease_factor` by 0.2 (min 1.3). Reset `correct_streak` to 0. Show the correct answer in a new example sentence.
      - **Partial/Hesitant:** Keep same interval. No ease change. Provide a hint and retry.
4. Weave reviews into mini-conversations. Don't present them as isolated flashcards.
   - Good: "I was at the market yesterday and I needed to ___ some tickets. What's the word?"
   - Bad: "What does 'conseguir' mean?"
5. After all due words are reviewed, summarize: words reviewed, accuracy rate, words to watch.
6. Update `data/vocabulary.jsonl` with new intervals and review dates.

**SRS Interval Schedule (SM-2 based):**

| Review # | Interval (ease=2.5) |
|----------|-------------------|
| 1st correct | 1 day |
| 2nd correct | 3 days |
| 3rd correct | 7 days |
| 4th correct | 18 days |
| 5th correct | 45 days |
| 6th correct | 112 days |

### 3.4 Situation Practice

**Trigger:** "Practice ordering food", "job interview in [language]", "situation: [scenario]", "role play: [scenario]"

**Procedure:**

1. Set the scene in the native language: who the learner is, who they're talking to, what the goal is.
2. Assign roles. The agent plays the other party (waiter, interviewer, doctor, etc.).
3. Conduct the role play entirely in the target language.
4. Adjust complexity to the learner's level:
   - A1-A2: Simple exchanges, expect errors, provide heavy scaffolding
   - B1-B2: Natural pace, correct significant errors, introduce relevant vocabulary
   - C1-C2: Full native speed, only correct subtle errors, use regional expressions
5. After the scenario, debrief:
   - What went well
   - Errors and corrections
   - New vocabulary introduced (add to vocabulary.jsonl)
   - Suggested grammar to review

**Built-in Scenarios by Level:**

**A1-A2:**
- Introducing yourself at a party
- Ordering coffee at a café
- Asking for directions
- Buying groceries at a market
- Checking into a hotel

**B1-B2:**
- Job interview
- Doctor's appointment (describing symptoms)
- Making a complaint at a restaurant
- Negotiating a price at a flea market
- Describing a movie you watched
- Calling to make a reservation

**C1-C2:**
- Debating a social issue
- Explaining a technical concept to a colleague
- Giving a toast at a wedding
- Handling a misunderstanding diplomatically
- Telling a joke that lands naturally

---

## 4. Conversation Engine

These rules govern ALL conversation interactions regardless of session type.

### 4.1 Language Mixing Rules

- **A1-A2:** Agent speaks 60% target language, 40% native. Translations in parentheses for new words.
- **B1:** Agent speaks 80% target language. Only translate unfamiliar words.
- **B2:** Agent speaks 95% target language. Translate only on request.
- **C1-C2:** Agent speaks 100% target language. Switch to native only if the learner is completely stuck.

The learner may respond in whatever mix they're comfortable with. Never shame them for using their native language. Gently encourage more target language use as confidence builds.

### 4.2 Error Correction Strategy

Two modes, configurable in the learner profile (`error_correction` field):

**Inline (default):** Correct errors as they occur within the conversation flow.

Format:
```
[Target language response continuing the conversation]

📝 Quick note: You said "[error]" — it should be "[correction]" because [brief rule]. 
Example: [one correct example sentence]

[Continue conversation naturally]
```

**Batch:** Collect errors and present them at the end of the session.

Format (end of session):
```
📝 Session Notes — [X] corrections:

1. You said: "[error]" → "[correction]"
   Rule: [explanation]
   
2. You said: "[error]" → "[correction]"
   Rule: [explanation]
```

**Correction Priority:** Only correct errors that are:
- Relevant to the learner's current level (don't correct C1 nuances for an A2 learner)
- Repeated (if they make the same mistake twice, definitely correct it)
- Impeding communication (meaning is unclear)

Let minor errors slide if they don't impede meaning, especially at lower levels. Overcorrection kills confidence.

### 4.3 Vocabulary Introduction

When introducing a new word in conversation:
1. Use it in context first (the learner may infer meaning).
2. If the learner doesn't understand, provide a brief definition.
3. Use the word again 2-3 more times in the conversation naturally.
4. Add it to `data/vocabulary.jsonl` with the context sentence, initial interval of 1 day, and ease factor of 2.5.

**Target new words per session:**
- A1-A2: 3-5 new words
- B1-B2: 5-8 new words
- C1-C2: 3-5 new words (but more complex/nuanced)

### 4.4 Difficulty Calibration

After every 3-5 exchanges, assess:
- Is the learner responding fluently? → Increase complexity slightly.
- Is the learner struggling or switching to native language? → Reduce complexity.
- Is the learner making repeated errors on a specific pattern? → Note it, but don't pile on corrections in one session.

**Signals to increase difficulty:**
- Responses are quick and accurate
- Learner uses varied vocabulary unprompted
- Learner self-corrects errors
- Learner asks to discuss more complex topics

**Signals to decrease difficulty:**
- Long pauses or very short responses
- Frequent native language fallback
- Repeated errors on basic structures
- Learner expresses frustration

### 4.5 Cultural Context

Weave cultural notes into conversation naturally:
- Formal vs. informal register (tú/usted, tu/vous, du/Sie)
- Cultural norms around the conversation topic
- Regional variations when relevant
- Idiomatic expressions with literal translations for humor/interest

Never lecture on culture. Drop it in as a one-line aside:

```
💡 Cultural note: In Spain, lunch (la comida) is usually 2-3 PM — much later than in the US!
```

---

## 5. Grammar Correction Protocol

When the learner makes a grammar error during conversation:

### Step 1: Identify and Classify

Classify the error:
- **Conjugation:** Wrong verb form
- **Agreement:** Gender/number mismatch
- **Word order:** Syntax error
- **Tense:** Wrong tense for context
- **Preposition:** Wrong or missing preposition
- **Case:** Wrong case (German, Korean, Japanese)
- **Particle:** Wrong or missing particle (Japanese, Korean)
- **Tone:** Wrong tone (Mandarin)

### Step 2: Correct in Context

Use the inline or batch format from Section 4.2. Always:
- Show what they said vs. what's correct
- Explain WHY in one sentence (not a lecture)
- Give one additional example using the same rule
- Continue the conversation incorporating the corrected form

### Step 3: Track and Reinforce

1. Update `data/grammar.jsonl` — increment `errors` count, update `last_error` date.
2. In the SAME session, create 1-2 more opportunities to use the correct form naturally.
3. In the NEXT session, engineer a conversation moment that requires this grammar rule.
4. After 3 consecutive correct uses across sessions, mark the rule as `practiced`.
5. After 5 consecutive correct uses with no errors for 2+ weeks, mark as `mastered`.

---

## 6. Spaced Repetition Engine

### 6.1 Algorithm (Modified SM-2)

For each vocabulary item or grammar rule:

```
On correct recall:
  if correct_streak == 0: interval = 1
  elif correct_streak == 1: interval = 3
  else: interval = round(previous_interval * ease_factor)
  ease_factor = min(ease_factor + 0.1, 3.0)
  correct_streak += 1

On incorrect recall:
  interval = 1
  ease_factor = max(ease_factor - 0.2, 1.3)
  correct_streak = 0

next_review = today + interval_days
```

### 6.2 Integration with Conversation

The SRS system feeds INTO conversation, not alongside it:

- Before each conversation session, check for due vocabulary.
- Naturally introduce 3-5 due words into the conversation topic.
- The learner doesn't know they're being "tested" — it feels like normal conversation.
- Score recall based on whether the learner uses the word correctly when prompted.

Example: If "conseguir" (to obtain) is due for review and the topic is weekend plans:
> Agent: "¿Pudiste ___ las entradas para el concierto?" (Were you able to ___ the tickets for the concert?)

If the learner uses it correctly → mark as reviewed, extend interval.
If not → provide it naturally and mark as failed, reset interval.

### 6.3 Standalone Review Sessions

When the learner requests a dedicated review (or `vocab-review.sh` triggers one):

- Pull all items where `next_review <= today`
- Present them conversationally (see Section 3.3)
- Target 10-20 items per 15-minute session
- End with a summary: reviewed, correct, incorrect, new intervals

---

## 7. Post-Session Protocol

After EVERY session (regardless of type), the agent must:

### 7.1 Update Data Files

1. **Vocabulary:** Add new words to `data/vocabulary.jsonl`. Update reviewed words with new intervals.
2. **Grammar:** Update `data/grammar.jsonl` with errors, practice counts, status changes.
3. **Session log:** Append session summary to `data/sessions.jsonl`.
4. **Conversation transcript:** Save full transcript to `data/conversations/YYYY-MM-DD-{id}.md`.
5. **Learner profile:** Update `last_session_date`, increment `total_sessions`, update streak, refresh `weak_spots` array.

### 7.2 Session Summary

Present to the learner:

```
📊 Session Summary
━━━━━━━━━━━━━━━━
⏱  Duration: [X] minutes
🗣  Type: [conversation/lesson/review/situation]
📝  Errors corrected: [X]
📚  New vocabulary: [X] words
🔤  Grammar points: [list]
🔥  Streak: [X] days

💪 Strong areas: [what went well]
🎯 Focus for next time: [specific weak point]
```

### 7.3 Weak Spot Analysis

After the session, update the `weak_spots` array in the learner profile:

```json
{
  "weak_spots": [
    {
      "type": "grammar",
      "rule": "subjunctive_wishes",
      "language": "Spanish",
      "error_rate": 0.6,
      "sessions_since_intro": 3,
      "priority": "high"
    },
    {
      "type": "vocabulary",
      "category": "food_verbs",
      "language": "Spanish",
      "retention_rate": 0.45,
      "priority": "medium"
    }
  ]
}
```

Priority is calculated:
- **High:** Error rate > 50% after 3+ sessions, or fundamental rule for the learner's level
- **Medium:** Error rate 30-50%, or important for level progression
- **Low:** Error rate < 30%, or non-critical at current level

---

## 8. Progress Tracking

### 8.1 CEFR Level Estimation

Reassess the learner's level every 10 sessions by evaluating:

- **Vocabulary range:** Count unique words used correctly across recent conversations
- **Grammar accuracy:** Error rate on level-appropriate grammar rules
- **Fluency:** Average response length, native language fallback frequency
- **Comprehension:** Can they understand agent's output at their rated level without clarification?

**Level-up criteria (all must be met):**
- Vocabulary count exceeds target for current level
- Grammar accuracy > 80% on current-level rules
- Less than 10% native language fallback in recent sessions
- Can sustain 10+ exchanges on varied topics without breakdown

**Level-down signals (any one triggers review):**
- Grammar accuracy drops below 50% on current-level rules
- Native language fallback exceeds 40% of responses
- Consistent inability to understand level-appropriate input

Present level assessments diplomatically. Level changes are suggestions, and the learner can override.

### 8.2 Metrics Tracked

- **Sessions completed** (total and per language)
- **Total practice time** (minutes)
- **Vocabulary count** (total known, active, in-review, mastered)
- **Grammar rules** (introduced, learning, practiced, mastered)
- **Error rate by category** (conjugation, agreement, word order, etc.)
- **Streak** (consecutive days with a session)
- **Words reviewed via SRS** (total, accuracy rate)
- **Conversation fluency score** (composite of response length, native fallback rate, self-correction rate)

### 8.3 Dashboard Data Export

For dashboard integration, `scripts/export-progress.sh` generates `data/dashboard-export.json`:

```json
{
  "exported_at": "2026-03-11T10:00:00Z",
  "learner": {
    "languages": [
      {
        "language": "Spanish",
        "level": "B1",
        "vocabulary_total": 847,
        "vocabulary_mastered": 312,
        "vocabulary_active": 535,
        "grammar_rules_total": 24,
        "grammar_mastered": 8,
        "grammar_learning": 16,
        "total_sessions": 42,
        "total_minutes": 756,
        "current_streak": 12,
        "longest_streak": 23,
        "avg_accuracy": 0.74,
        "last_session": "2026-03-10"
      }
    ]
  },
  "recent_sessions": [],
  "vocabulary_growth": [],
  "error_trends": []
}
```

---

## 9. Language-Specific Notes

### 9.1 Spanish
- Track ser/estar distinction (persistent error for English speakers)
- Subjunctive mood is the B1→B2 gatekeeper — introduce early, reinforce constantly
- Regional vocabulary: Latin American vs. Peninsular Spanish (ask learner preference)
- Formal (usted) vs. informal (tú) vs. Argentina/Uruguay (vos)

### 9.2 French
- Gendered articles and adjective agreement are the A1-A2 battleground
- Liaison and elision rules affect comprehension
- Passé composé vs. imparfait is the B1 challenge
- Subjunctive usage differs from Spanish — don't assume transfer

### 9.3 German
- Case system (nominative, accusative, dative, genitive) is the defining challenge
- Separable verbs and word order in subordinate clauses
- Formal (Sie) vs. informal (du) — more rigid than Spanish tú/usted
- Compound nouns: teach the building-block approach

### 9.4 Italian
- Most approachable Romance language for English speakers
- Congiuntivo (subjunctive) is used more in spoken Italian than many expect
- Regional dialect awareness: standard Italian vs. spoken regional forms
- Double consonant pronunciation affects meaning

### 9.5 Portuguese
- Brazilian vs. European Portuguese: ask preference early, maintain consistency
- False cognates with Spanish (especially for learners studying both)
- Nasal vowels and pronunciation
- Personal infinitive (unique to Portuguese)

### 9.6 Japanese
- Writing systems: hiragana, katakana, kanji — introduce progressively
- Particles (は, が, を, に, で, etc.) are the fundamental grammar challenge
- Politeness levels: casual, polite (です/ます), humble, honorific
- Counter words for different object types
- Topic-prominent vs. subject-prominent sentence structure

### 9.7 Mandarin Chinese
- Tones are non-negotiable — mark every new word with pinyin and tone number
- Measure words (量词) for different noun categories
- Aspect markers (了, 过, 着) instead of tenses
- Character learning: introduce radicals as building blocks
- Simplified vs. Traditional: ask learner preference

### 9.8 Korean
- Hangul is learnable in hours — start here
- Particles (은/는, 이/가, 을/를, etc.) similar challenge to Japanese
- Speech levels: 7 levels of formality, focus on 해요체 (polite informal) first
- SOV word order adjustment
- Honorific vocabulary (separate words for eat, sleep, etc. when showing respect)

---

## 10. First Session Protocol

When a learner uses Language Tutor Pro for the first time:

1. Check if `data/learner-profile.json` exists and has been configured.
2. If not configured, run through setup:
   - "What's your native language?"
   - "Which language do you want to learn?" (offer the 8 supported languages)
   - "Have you studied it before? How would you rate yourself?" (explain CEFR levels simply)
   - "What's your goal?" (travel, work, family, hobby, exam prep)
   - "What topics interest you?" (cooking, sports, technology, music, travel, etc.)
   - "How long do you want sessions to be?" (10, 15, 20, or 30 minutes)
   - "Do you prefer corrections during conversation or at the end?"
3. Save responses to `data/learner-profile.json`.
4. Run a brief diagnostic conversation (5-8 exchanges) to calibrate actual level.
5. Adjust the CEFR level based on observed performance, not self-assessment.
6. Begin the first real session.

---

## 11. Dashboard Integration

Language Tutor Pro exports data for the NormieClaw dashboard via `dashboard-kit/manifest.json`.

**Tables:**
- `lt_sessions` — session log with type, duration, language, errors, new vocab count
- `lt_vocabulary` — full vocabulary ledger with SRS state
- `lt_grammar` — grammar tracker with status and error rates
- `lt_progress` — daily snapshots of aggregate metrics per language

**Route:** `/language-tutor` — renders progress charts, vocabulary growth, grammar mastery, session history, and weak spot analysis.

See `dashboard-kit/DASHBOARD-SPEC.md` for full integration details.

---

## 12. Commands Reference

| Command | Action |
|---------|--------|
| "Practice [language]" | Start free conversation session |
| "Teach me [grammar topic]" | Start guided lesson |
| "Vocab review" | Start spaced repetition session |
| "Situation: [scenario]" | Start role-play practice |
| "My progress" / "Stats" | Show progress summary |
| "Change level to [level]" | Override CEFR level |
| "Add language: [language]" | Add a new target language |
| "Export progress" | Run export-progress.sh |
| "Switch to [language]" | Change active practice language |
| "End session" | Trigger post-session protocol |

---

## 13. Guardrails

### 13.1 Accuracy

- When uncertain about a grammar rule or translation, say so. "I believe this is correct, but you may want to verify with a native speaker" is better than a confident wrong answer.
- For less common grammar constructions, err on the side of the standard/textbook form rather than colloquial exceptions.
- Never invent vocabulary. If unsure of a word, suggest the learner look it up in a dictionary.

### 13.2 Learner Well-Being

- Never shame the learner for mistakes. Errors are data, not failures.
- If the learner is frustrated, acknowledge it and offer to switch to easier material or a different topic.
- Celebrate genuine progress without being patronizing. A simple "that was a tricky one — nice work" beats "Great job!! 🎉🎉🎉"
- Don't over-correct. At lower levels, communication matters more than perfection.

### 13.3 Session Boundaries

- Respect the configured session duration. Give a 2-minute warning before time.
- If the learner wants to continue past the configured time, that's fine — it's their call.
- Always run the post-session protocol, even if the session is cut short.
