# Voice Profile — How Ghostty Learns to Write Like You

Your voice profile lives at `ghostty/voice-profile.md` and is the core of Ghostty's ability to sound like you, not generic AI.

## What Gets Measured

### 1. Surface Metrics (easy to detect)
- **Average sentence length** — short=terse/urgent, long=thoughtful/deliberate
- **Paragraph length** — do you write in blocks or one-liners?
- **Punctuation style** — ellipses..., em dashes—, exclamation frequency!
- **Caps usage** — ALL CAPS for emphasis? Never?
- **Emoji frequency** — 😐 or none?

### 2. Structural Patterns
- **Greeting style** — "Hey", "Hi", "Hello", "Yo", "Dear"
- **Sign-off style** — "Cheers", "Thanks", "Best", "Kind regards", nothing
- **Opener patterns** — do you jump straight in or acknowledge first?
- **Question frequency** — do you ask a lot of questions?
- **Directness** — do you say "I want X" or "Would it be possible to X"?

### 3. Tone Indicators (harder to detect)
- **Confidence level** — assertive ("do this") vs. hedged ("maybe", "perhaps", "I think")
- **Warmth** — emotional language, exclamation, personal references
- **Formality register** — startup casual vs. corporate formal
- **Humor** — dry, sarcastic, none detectable?
- **Tone consistency** — same tone with everyone or different with different people?

### 4. Content Patterns
- **Topic avoidance** — what you never talk about
- **Pet phrases** — "no worries", "all good", "gotcha", "perfect"
- **Signature phrases** — things you always say at the end
- **Attention to detail** — do you proof, follow up, add caveats?

## Manual Voice Profile Template

Copy this to `ghostty/voice-profile.md`:

```markdown
# My Voice Profile

## Quick Summary
[TWO SENTENCES: how you sound to a stranger reading your emails]

## Greeting Style
[How you start emails/messages to: (a) friends, (b) colleagues, (c) clients, (d) authority figures]

## Sign-off Style
[Your sign-offs by context: casual, professional, close contacts]

## Typical Length
- Quick reply to friend: [X-Y sentences]
- Reply to colleague: [X-Y sentences]  
- Client/professional: [X-Y sentences]
- Difficult situation: [X-Y sentences]

## Tone Settings
- Confidence: [1-10, 10=always assertive]
- Warmth: [1-10, 10=very warm/expressive]
- Formality: [1-10, 10=very formal]
- Humor: [none / dry / light / frequent]

## Phrases I Use
- Filler/phatic: [e.g., "no worries", "all good", "hope you're well"]
- Agreement: [e.g., "perfect", "sounds good", "deal"]
- Disagreement: [e.g., "I see it differently", "not sure I agree", "hmm"]
- Closing: [e.g., "talk soon", "let me know", "solid"]

## Phrases I Never Use
[e.g., "Kind regards", "As per our conversation", "Please find attached"]

## Emoji Usage
[Frequency: never / occasional / frequent. Types you use: 🙏 💯 😂 etc.]

## What Makes My Replies Distinctive
[2-3 things that make your writing yours]
```

## Auto-Building from Samples

The `scripts/profile_builder.py` can analyze a folder of your sent emails or message exports and produce the profile above automatically.

**To use the profile builder:**
```bash
python3 scripts/profile_builder.py \
  --source ./my-sent-emails/ \
  --format eml \
  --output ghostty/voice-profile.md
```

**Supported formats:**
- `eml` — exported Gmail/Outlook .eml files
- `json` — WhatsApp/Telegram chat export
- `csv` — Slack message export
- `mbox` — Gmailmbox export

## Per-Person Overrides

Sometimes you write differently to different people. Ghostty supports per-person profiles:

```markdown
## Per-Person Overrides

### [boss-name]
More formal. Always use "Kind regards" sign-off. Max 3 sentences.

### [close-friend-name]  
All caps for emphasis OK. Emojis welcome. Can be rambling.

### [new-client-name]
Formal but warm. Confirm everything in writing.
```

Add a `ghostty/per-person/` directory with markdown files named `{person-name}.md` for overrides.
