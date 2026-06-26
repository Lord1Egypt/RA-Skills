---
name: personality-analyzer
description: Analyze a person's personality traits based on their written text or chat messages. Use this skill whenever the user wants to understand someone's personality, character, communication style, or behavioral tendencies from text. Trigger when the user says things like "analyze this person's personality", "what kind of person wrote this", "tell me about this person based on their messages", "profile this person", "what does this text say about their character", or pastes messages/conversations and asks for a personality read. Also trigger when the user wants to understand communication patterns, emotional tendencies, or interpersonal styles inferred from written language.
version: 1.0.0
tags:
  - personality
  - psychology
  - text-analysis
  - character
  - communication
metadata:
  clawdbot:
    emoji: "🧠"
    files: []
---

# Personality Analyzer

Analyze a person's personality traits, communication style, and behavioral tendencies based on their written text.

## When to Activate

Activate this skill when:
- The user provides text, messages, or chat logs and asks for a personality reading
- The user wants to understand what someone's writing style reveals about them
- The user asks about communication patterns, emotional tendencies, or character traits
- The user provides a conversation excerpt and asks "what kind of person is this?"

---

## Analysis Framework

Perform a structured personality analysis across these five dimensions:

### 1. 🗣️ Communication Style
Examine HOW the person expresses themselves:
- **Directness**: Are they blunt and to-the-point, or do they hedge and soften?
- **Formality level**: Formal, casual, or code-switching between both?
- **Verbosity**: Concise and minimal, or elaborate and detailed?
- **Tone**: Warm, cold, neutral, enthusiastic, reserved?
- **Humor**: Do they use jokes, sarcasm, irony, wordplay?

### 2. 💡 Cognitive Patterns
Examine HOW the person thinks:
- **Logic vs. Emotion**: Do they lead with reasoning or feelings?
- **Big-picture vs. Detail-oriented**: Abstract/conceptual vs. specific/concrete?
- **Certainty**: Do they use definitive language or qualify everything?
- **Curiosity signals**: Do they ask questions, explore ideas, show intellectual interest?
- **Organization**: Is their thinking structured or stream-of-consciousness?

### 3. 🌡️ Emotional Tendencies
Read the emotional layer beneath the words:
- **Emotional expression**: Openly expressive or emotionally guarded?
- **Empathy signals**: Do they acknowledge others' feelings or stay self-focused?
- **Stress/anxiety indicators**: Urgency, over-explaining, excessive apologizing?
- **Confidence level**: Self-assured, uncertain, or seeking validation?
- **Emotional stability**: Consistent tone or noticeable mood shifts?

### 4. 🤝 Interpersonal Orientation
Assess how they relate to others:
- **Collaboration vs. Independence**: Do they involve others or prefer working solo?
- **Power dynamic awareness**: Do they position themselves above, equal to, or deferential toward others?
- **Trust signals**: Open and sharing, or guarded and vague?
- **Conflict style**: Avoidant, confrontational, diplomatic, or assertive?
- **Social awareness**: Do they seem attuned to how they're perceived?

### 5. 🎯 Values & Motivations
Infer what the person cares about:
- **Core priorities**: What do they keep returning to in their language?
- **Achievement orientation**: Goal-driven, process-driven, or people-driven?
- **Moral framing**: Do they invoke fairness, loyalty, authority, or other values?
- **What frustrates them**: Complaints and friction points reveal values in reverse

---

## Output Format

Structure the analysis as follows:

```
## Personality Analysis

### Quick Summary
[2-3 sentences capturing the overall personality impression]

### Communication Style
[Analysis with specific examples from the text]

### How They Think
[Cognitive style analysis with text evidence]

### Emotional World
[Emotional tendencies and what they suggest]

### How They Relate to Others
[Interpersonal style and social orientation]

### What They Value
[Core values and motivations inferred from language]

### Personality Type Snapshot
[Optional: Map to a recognizable framework if helpful, e.g., Big Five traits, MBTI-adjacent description — make clear these are approximations, not diagnoses]

### Important Caveats
[Note limitations: short text = lower confidence; text reflects a moment, not a whole person; cultural/contextual factors matter]
```

---

## Analysis Guidelines

**Do:**
- Anchor every claim to specific words, phrases, or patterns in the text
- Use probabilistic language ("suggests", "tends toward", "may indicate") — avoid stating certainties
- Note when evidence is thin or ambiguous
- Highlight both strengths and potential blind spots
- Consider alternative interpretations when the evidence is mixed

**Don't:**
- Make clinical diagnoses (no "this person has narcissistic personality disorder")
- Over-extrapolate from very short texts (< 3-4 sentences)
- Ignore context (a customer complaint vs. a love letter call for different readings)
- Project — only analyze what's actually in the text, not what you imagine
- Be unnecessarily harsh or reductive

**Text Length Calibration:**
- **< 50 words**: Give a brief impression only, emphasize high uncertainty
- **50–200 words**: Moderate analysis, note gaps
- **200+ words**: Full analysis with good confidence
- **Multiple messages over time**: Note patterns and any inconsistencies across messages

---

## Special Cases

### Multiple People in a Conversation
If the user provides a multi-party conversation:
- Analyze each participant separately
- Note the dynamic between them (power balance, emotional attunement, conflict patterns)

### Non-native Language Signals
If the text appears to be written by a non-native speaker:
- Focus on content and ideas rather than stylistic quirks that may be language artifacts
- Note this caveat explicitly

### Professional vs. Personal Text
- Professional text (emails, reports) is more constrained — read between the lines more carefully
- Personal text (chats, social posts) is more revealing — take it more at face value

---

## Example Invocation

**User**: "Can you analyze the personality of whoever wrote this?"

**Your response**: Follow the Output Format above. Lead with the Quick Summary, then go dimension by dimension. Close with the caveats section.

If the user hasn't provided text yet, ask: "Please share the text or messages you'd like me to analyze."
