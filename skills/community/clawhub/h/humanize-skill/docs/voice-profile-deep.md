# Voice profile: deep matching

The base profile in `SKILL.md` covers surface signals — sentence length, paragraph shape, diction, punctuation, openings. This document goes one level deeper: **how a person thinks on the page**. Surface features are easy to mimic. The deeper fingerprint is what makes a rewrite actually read like the user.

Use this when samples are present and the user explicitly wants stronger voice matching. Do not invent a "voice" when none is in evidence. The natural default voice is fine for most rewrites.

## Why deep matching matters

A user with a 12-word-average sentence who swears in casual posts is not the same writer as one with the same sentence length who is decorous in the same register. The first person uses "fucking" as emphasis; the second uses "remarkably". Same length, different voice.

Surface features (length, punctuation, paragraph shape) tell you the rhythm. Deep features (stance, abstraction, hedging, repair, perspective) tell you the *person*. Both are needed.

## Beyond surface: the deep signals

### 1. Abstract vs concrete tendency

Some writers anchor everything in specifics. They say "in our 12-week pilot with 40 students". Others prefer abstraction. They say "early results suggest".

- **Concrete default**: numbers, dates, names, places, sensory detail, named people.
- **Abstract default**: trends, principles, frameworks, general statements.

How to detect it:

- Do the sample sentences contain numbers, names, or specific verbs (saw, ran, broke, fixed)?
- Or do they contain general verbs (suggest, indicate, demonstrate, highlight)?

How to apply it:

- Match the user's tendency. If they are concrete, do not float up to abstraction to sound "more professional". If they are abstract, do not over-specify with invented numbers.

### 2. Conclusion-first vs setup-first ordering

Some writers lead with the bottom line. "The new model is wrong. Here's why." Others build to it. "We ran three tests, each showed the same issue, which leads me to conclude the model is wrong."

- **Conclusion-first**: thesis in the first sentence. Argument follows.
- **Setup-first**: argument unfolds. Thesis lands late or implicit.

How to apply it:

- Read the first sentence of three or four sample paragraphs. Does the writer state the conclusion, or build to it?
- Match that. Do not impose thesis-first structure on a writer who builds. Do not stretch a thesis-first writer into long preambles.

### 3. Stance and opinion strength

Writers differ in how strongly they commit to claims.

- **Strong stance**: "This is the right call." "I disagree." "We should ship."
- **Soft stance**: "One approach is..." "Some teams prefer..." "It depends."
- **Hedged stance**: "Maybe we should consider..." "I am not sure, but..."

How to apply it:

- If the user is strong, the rewrite can be strong. Do not flatten into mushy "perhaps" language.
- If the user hedges, preserve that. Do not promote their hedges into commitments.

### 4. Repair and self-correction in prose

Real writers leave traces of thinking on the page. AI usually does not.

- **Repair visible**: "I thought X, but Y." "On reflection, ..." "Actually, that was wrong — the right number is..."
- **Repair hidden**: clean, considered prose with no visible mid-thought corrections.

Some surfaces call for clean prose (legal, formal, reference). Others (essays, newsletters, posts) make space for repair.

How to apply it:

- If the sample has visible repair, allow a small amount in the rewrite. The user feels seen when their quirks survive.
- Do not invent repair where the user writes clean prose.

### 5. Perspective: "I", "we", "you", or impersonal

Voice profile is also about who is doing the seeing.

- **First person singular ("I")**: personal essays, opinion posts, individual work.
- **First person plural ("we")**: team, company, group posts.
- **Second person ("you")**: instructional, direct, sometimes salesy.
- **Impersonal**: reference, encyclopedic, formal report.

How to apply it:

- Pick the perspective the user uses, then keep it consistent. A voice profile that flips between "I" and "we" within a rewrite is jarring.

### 6. Hedging vs commitment per claim type

The same writer often hedges differently for different kinds of claim.

- For facts: confident when cited, hedged when not.
- For predictions: hedged by default.
- For opinions: committed or explicitly framed as opinion.
- For personal experience: confident and specific.

How to apply it:

- A good voice profile is *internally consistent*. A writer who is confident about facts and soft about predictions reads differently from a writer who is soft about facts and confident about predictions.
- Match the pattern, not just the average hedge level.

### 7. Domain vocabulary and register

Writers carry the vocabulary of their domain. A software engineer writes about "API rate limits". A lawyer writes about "indemnification clauses". A teacher writes about "formative assessment".

How to apply it:

- Keep the domain vocabulary. A lawyer's voice is not improved by replacing "indemnification" with "legal protection".
- Do not over-translate. Match the register the user actually uses.

### 8. Code-switching and bilingual habits

Some users switch between languages in their natural writing. A bilingual writer who writes "this is a really 麻烦 issue" is doing something AI will not reproduce by default.

How to apply it:

- Preserve natural code-switching. Do not normalize it into monolingual prose.
- Add a note in the profile that the user code-switches, so the host agent does not "fix" it.

### 9. Tolerance for imperfection

A real voice profile is not perfectly consistent. The user has a tell that breaks the rule.

- Maybe they always use Oxford commas except in lists of three.
- Maybe they swear in the second paragraph of long posts.
- Maybe they always start with "Look," or "OK," or "So,".

How to apply it:

- Capture at least one of these in the profile. It is the signature. Without it, the rewrite is generic.
- Do not over-apply the signature, though. A writer who swears once per post is not made more human by swearing in every paragraph.

### 10. Tolerance for opinion, humor, and self-disclosure

Writers differ in how much of themselves they put on the page.

- **Personal**: opinions, feelings, biographical detail, opinions about people.
- **Reserved**: stays on the topic, avoids personal aside.
- **Mixed**: shares when relevant, holds back otherwise.

How to apply it:

- If the user is personal, allow some personality. If reserved, hold back.
- Never *invent* personal disclosure. A user who never says "I" should not be made to say it just to "humanize" the prose.

## Building the deep profile

A short workflow:

1. Read 3-5 samples, at least 300 words total.
2. For each of the 10 axes above, note the user's tendency.
3. Keep the notes compact. One short phrase per axis is enough.
4. Use the notes as a constraint, not a script. The rewrite should *feel* like the user, not be checked against every axis.

Compact profile example:

```json
{
  "user": "casey",
  "samples": ["samples/posts/casey-2024.jsonl", "samples/email.txt"],
  "word_count": 2400,
  "surface": {
    "avg_sentence_words": 14.0,
    "paragraph_style": "short",
    "punctuation": { ".": 95, ",": 38, "?": 6 }
  },
  "deep": {
    "concrete_vs_abstract": "concrete, names projects and dates",
    "conclusion_ordering": "setup-first, lands the point in the last sentence",
    "stance": "strong, takes a position",
    "repair_visible": "sometimes, especially in long posts",
    "perspective": "we for team, I for personal",
    "hedge_pattern": "confident on facts, hedged on predictions",
    "domain_vocab": "infra/SRE, comfortable with technical shorthand",
    "code_switching": "none observed",
    "imperfection_tells": "starts some posts with 'OK,'",
    "personality": "dry humor, no swearing"
  }
}
```

## What deep matching is not

- It is not a license to inject personality. If the user is dry, the rewrite is dry.
- It is not a way to make the text "feel" more like the user by adding slang, emojis, or random rhythm.
- It is not guaranteed to fool any specific detector. It is the right way to write like the user; that is its own reward.

The goal is a rewrite the user can read and feel *yes, this is how I would have said it*. That feeling is the test. If it is missing, the profile is incomplete or the surface signals are dominating.
