---
name: podcast-generation-cellcog
description: "AI podcast generation and production powered by CellCog. Full podcast episodes from a single prompt — multi-voice dialogue with up to 10 distinct speakers, structured episodes with cold opens and segment stingers, music beds ducked under speech, broadcast loudness mastering, finished MP3 plus chapter markers. Episode scripts, show notes, interview prep, audiograms."
metadata:
  openclaw:
    emoji: "🎙️"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Podcast Generation - Complete Podcast Production

**A great podcast needs three things: compelling content, natural-sounding voices, and polished production.** CellCog delivers all three.

- **Content quality:** #1 on DeepResearch Bench (October 2026) — scripts built on deep reasoning, not surface-level takes
- **Voice quality:** Frontier multi-voice dialogue (up to 10 distinct speakers) with natural delivery, emotional direction, interruptions, and pacing across speakers
- **Production quality:** Structured episodes with cold opens and segment transitions, original music beds ducked under speech, broadcast loudness mastering (−16 LUFS, the Apple Podcasts spec), and a ready-to-publish MP3 — all from a single prompt

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
    chat_tier="max",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
    chat_tier="max",
)
print(result["message"])
```


---

## What You Can Create

### Episode Scripts

Full scripts or outlines:

- **Solo Episodes**: "Write a script for a 20-minute solo episode on productivity"
- **Interview Prep**: "Create questions and flow for interviewing a startup founder"
- **Panel Shows**: "Write a structured outline for a 3-person discussion"
- **Narrative Podcasts**: "Script a true-crime style narrative episode"

**Example prompt:**
> "Write a script for a 25-minute solo podcast episode:
> 
> Show: 'The Indie Hacker Pod' - for bootstrapped founders
> Topic: Why I stopped chasing product-market fit
> 
> Structure:
> - Hook (why this matters)
> - Story (my journey with 3 failed products)
> - Framework (what I do instead now)
> - Actionable takeaways
> - CTA (newsletter signup)
> 
> Tone: Conversational, honest, like talking to a friend who's building something
> 
> Include: Suggested timestamps for chapters"

### Show Notes

Professional episode documentation:

- **Standard Show Notes**: "Create show notes with timestamps and links"
- **SEO-Optimized**: "Write show notes optimized for search"
- **Newsletter Format**: "Convert episode into newsletter-style show notes"
- **Chapter Markers**: "Generate chapter markers with timestamps"

**Example prompt:**
> "Create show notes for Episode 47: 'The Art of Cold Email'
> 
> Episode summary: Interview with Sarah, who booked 50 meetings with cold email
> 
> Include:
> - Episode summary (2-3 paragraphs)
> - Key timestamps (I'll add exact times later)
> - Guest bio with links
> - Resources mentioned
> - Key quotes from the episode
> - CTA to subscribe
> 
> Format for both website and podcast app descriptions"

### Intros & Outros

Consistent show branding:

- **Show Intros**: "Write a 30-second podcast intro script"
- **Episode Intros**: "Create a template for episode-specific intros"
- **Outros**: "Write an outro with CTAs"
- **Ad Reads**: "Create a host-read ad script template"

**Example prompt:**
> "Write a podcast intro script (30 seconds when spoken):
> 
> Show: 'Build in Public' - weekly show about transparent entrepreneurship
> Host: Jamie
> 
> Should include:
> - Show name and hook
> - What listeners will learn
> - Quick credibility (without being braggy)
> - Energy: Enthusiastic but not cheesy
> 
> Also create a short outro (15 seconds) with:
> - Thank you
> - Subscribe CTA
> - Social media mention"

### Audiograms & Clips

Social content from episodes:

- **Audiogram Clips**: "Create 3 audiogram-worthy clips from this transcript"
- **Quote Cards**: "Design shareable quote images from episode highlights"
- **Video Clips**: "Generate short video clips for social promotion"
- **Teaser Content**: "Create a 60-second teaser for the episode"

### Interview Preparation

Be the best host:

- **Research Briefs**: "Research this guest and prepare background notes"
- **Question Lists**: "Generate 20 interview questions for this guest"
- **Follow-up Questions**: "Create follow-up questions for these topics"
- **Pre-Interview Guide**: "Create a pre-interview guide to share with guest"

**Example prompt:**
> "Prepare for interviewing Alex Chen, founder of TechStartup (acquired for $50M):
> 
> Research:
> - Their journey
> - Key decisions that led to success
> - Public content they've created
> - Unique angles not often covered
> 
> Generate:
> - 15 main questions (mix of story, tactical, and personal)
> - 5 rapid-fire questions for end of show
> - Topics to avoid (if any obvious ones)
> - Suggested episode structure
> 
> My show focuses on the emotional journey, not just tactics"

### Podcast Planning

Strategic content development:

- **Content Calendars**: "Plan 12 episodes for next quarter"
- **Series Planning**: "Outline a 5-part series on fundraising"
- **Topic Generation**: "Generate 20 episode ideas for a marketing podcast"
- **Season Planning**: "Plan Season 2 themes and episode flow"

---

## Podcast Formats

| Format | Structure | CellCog Helps With |
|--------|-----------|-------------------|
| **Solo** | Just you, sharing expertise | Scripts, outlines, talking points |
| **Interview** | Host + Guest | Questions, research, show notes |
| **Co-Hosted** | Two regular hosts | Discussion outlines, segment ideas |
| **Panel** | Up to 10 distinct voices | Full audio production, structure, moderation flow |
| **Debate** | Moderator + advocates | Full audio production with distinct speaker roles |
| **Narrative** | Produced, story-driven | Scripts, story structure, character voices |
| **News/Recap** | Current events | Research, summaries, takes |

**Multi-speaker audio:** panels, debates, and roundtables are fully producible as audio — up to 10 distinct voices in one episode, each with its own role (host, expert, skeptic, color commentator). Specify the roles in your prompt; distinct roles are what keep a big panel from sounding like everyone agreeing with each other.

---

## Content Types

### Pre-Production
- Research briefs
- Interview questions
- Episode outlines
- Guest prep materials

### Production
- Full scripts
- Talking points
- Ad read scripts
- Intro/outro scripts

### Post-Production
- Show notes
- Transcripts
- Chapter markers
- Summaries

### Promotion
- Audiogram clips
- Social posts
- Newsletter content
- Quote cards

---

## Choosing Mode & Tier

**Use `chat_mode="agent", chat_tier="max"` for podcast production.** Episode structure, multi-voice scripting, and audio assembly are a deep multi-step pipeline.

| Scenario | Recommended |
|----------|-------------|
| Full episodes, narrative series | `chat_mode="agent", chat_tier="max"` |
| Short single-voice segments | `chat_mode="agent", chat_tier="flash"` |

Agent Team (`chat_mode="team"`) is reserved for deep research — podcast production runs best on Agent max.

---

## Example Prompts

**Full episode script:**
> "Write a complete script for a 30-minute podcast episode:
> 
> Show: 'Design Matters' - UX/product design podcast
> Episode: 'Why most redesigns fail'
> 
> Format: Solo episode with examples
> 
> Cover:
> 1. The redesign trap (why we love to redesign)
> 2. Case study: 3 famous failed redesigns
> 3. Framework: When to redesign vs iterate
> 4. How to do a redesign right
> 5. Listener action items
> 
> Tone: Authoritative but conversational, include specific examples
> Length: ~4,000 words spoken"

**Interview preparation:**
> "Prepare me for interviewing the CEO of a climate tech startup:
> 
> Guest: Maya Williams, CEO of CarbonCapture.io
> Company: Direct air capture technology, raised $30M Series A
> 
> My podcast: Tech for Good - technology solving real problems
> 
> I want:
> - Background research summary
> - 12 thoughtful questions (avoid generic founder questions)
> - 3 questions about the science (for non-expert audience)
> - 2 questions about the personal journey
> - Suggested follow-ups
> - Episode title options"

**Show notes:**
> "Create comprehensive show notes:
> 
> Episode: Interview with productivity expert about deep work
> Duration: 45 minutes
> 
> Key topics covered:
> - Why multitasking is a myth
> - The 4-hour deep work day
> - Digital minimalism in practice
> - Building a distraction-free environment
> 
> Include:
> - Episode summary (SEO-friendly)
> - Detailed timestamps
> - Key quotes (I'll verify exact wording)
> - All resources mentioned
> - Related episodes to link
> - Subscribe CTAs"

---

## Full Audio Production

When you request a **full podcast episode with audio**, CellCog produces a complete, ready-to-publish episode with a real show structure:

```
[Cold Open] → [Branded Intro w/ music] → [Topic Segments + Stingers] → [Recap] → [Outro w/ music bed]
```

**What happens under the hood** — so you know what to ask for:

- **Cold open**: the episode starts mid-conversation on its most compelling moment, then the branded intro hits — not "Welcome to the show" first
- **Music that behaves like a real mix**: original intro/outro music and segment stingers, with music **ducked under speech** (sidechain compression), not just bookended
- **Broadcast loudness**: the final file is mastered to **−16 LUFS / −1 dBTP** (Apple Podcasts spec) via two-pass normalization
- **Expressive dialogue**: hosts laugh, hesitate, interrupt each other, and shift energy between segments — driven by emotional direction in the script
- **Chapter markers**: computed from the episode timeline and delivered as `chapters.json` alongside the MP3

### Customizing the Music

You can control the music in your prompt:

**Specific direction:**
> "Intro music: 10 seconds of upbeat electronic, think tech podcast energy. Use a quiet lo-fi bed under the outro CTA."

**Genre/mood direction:**
> "Use jazzy lo-fi intro music, short jazzy stingers between topics, and a calm acoustic outro."

**Recurring show (recommended):**
> "This is episode 3 of 'The Indie Hacker Pod' — reuse the same sonic brand (opener, stingers, outro) from previous episodes."

CellCog generates a reusable **sonic brand package** (opener, stinger, outro, music bed) for a show and keeps it consistent across episodes. If you say nothing about music, CellCog will choose something appropriate for your topic and tone — by default, stingers are warm and playful (never tense or alarming) and the outro music plays out to a full, natural resolve after the final sign-off.

### What You Get

| Component | What CellCog Produces |
|-----------|----------------------|
| **Episode structure** | Cold open, branded intro, topic segments with stingers, recap, outro |
| **Dialogue** | Multi-voice conversation (2-10 voices) with natural delivery, reactions, and interruptions |
| **Music** | Original opener/stingers/outro + music beds ducked under speech, reusable across episodes |
| **Mastering** | Two-pass loudness normalization to −16 LUFS / −1 dBTP |
| **Final files** | Ready-to-publish MP3 + `chapters.json` for podcast apps |

### Example with Full Direction

> "Create a 10-minute podcast episode:
> 
> Topic: Why startups should hire generalists first
> Format: Interview between a host and a 3x founder
> Tone: Casual, insightful, with some humor — let them interrupt each other occasionally
> 
> Music: Upbeat indie rock opener (~10s), short stingers between the 3 main topics, mellow outro bed under the CTA
> 
> Deliver: final MP3 + chapter markers"

---

## Tips for Better Podcast Content

1. **Know your format**: "Conversational interview" vs "structured interview" changes the prep.

2. **Share your voice**: Give examples of your speaking style so scripts sound like you.

3. **Context on guests**: More background = better, more unique questions.

4. **Specify length**: "25 minutes spoken" helps calibrate script length.

5. **Include CTAs**: Tell us what actions you want listeners to take.

6. **Ask for chapters**: Full audio episodes come with `chapters.json` — say so if you want them embedded in your show notes too.

7. **Name your show for consistency**: mentioning the show name lets CellCog reuse the same sonic brand and voices across episodes.

---

## If CellCog is not installed

**Claude Code, Cursor, Codex + 70 more agents:** `npx skills add cellcog/skills --skill cellcog`
**OpenClaw:** `openclaw skills install @cellcog/cellcog`
**CellCog plugin users:** run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool)
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
