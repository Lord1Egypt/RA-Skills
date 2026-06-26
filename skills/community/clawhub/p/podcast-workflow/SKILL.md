---
name: podcast-workflow
description: Full podcast post-production pipeline. Give it a transcript or audio URL and it produces show notes, chapter markers, social media clips, SEO title/description, and a newsletter summary — all in one shot. Use when the user mentions podcast, episode, transcript, show notes, chapters, or timestamps.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins:
        - curl
---

# Podcast Workflow

## When to use this skill

Use this skill when the user:
- Pastes a podcast transcript or provides an audio/video URL
- Asks for show notes, chapter markers, or timestamps
- Wants social media posts from a podcast episode
- Needs a newsletter summary of an episode
- Says anything like "process my podcast", "episode notes", "clip this"

Do NOT use this skill for general writing tasks unrelated to podcasts.

## What you produce

Run all steps below in sequence. Deliver everything in a single structured response.

---

## Step 1 — Ingest content

**If the user pastes a transcript:**
- Use the text directly. Note approximate word count.
- Estimate total episode duration: assume ~130 words per minute of spoken audio.

**If the user provides a URL (YouTube, Spotify, RSS, etc.):**
- Use `curl` to fetch the page and extract any available transcript or description.
- If no transcript is available, tell the user: "No transcript found at this URL. Please paste the transcript text directly."

**If the user provides neither:**
- Ask: "Please paste your episode transcript or share a URL to the episode."

---

## Step 2 — Show notes

Write professional show notes in this exact format:

```
## [Episode Title — infer from content if not given]

[2–3 sentence hook that captures the core insight of the episode. Write for someone who hasn't listened yet.]

### What we cover
- [Key topic 1]
- [Key topic 2]
- [Key topic 3]
- [Key topic 4]
- [Key topic 5]

### Key takeaways
[3–5 bullet points with the most actionable or surprising insights from the episode]

### Guest / Host
[Name and one-line description if mentioned in transcript. Skip if solo episode with no guest info.]

### Resources mentioned
[List any books, tools, websites, or people mentioned in the transcript. Format: Name — brief description. Skip section if none found.]
```

Rules:
- Write in present tense ("In this episode, [Host] explains...")
- No filler phrases like "fascinating", "incredible", "game-changing"
- Keep the hook under 60 words
- Total show notes: 200–400 words

---

## Step 3 — Chapter markers

Generate timestamp-based chapters suitable for YouTube, Spotify, and podcast players.

Format each line as:
```
00:00 Introduction
[MM:SS] [Chapter title — max 50 characters]
```

Rules:
- Estimate timestamps based on content position in transcript (use the ~130 wpm estimate)
- Minimum 4 chapters, maximum 12
- Chapter titles must describe the content, not just label it (e.g. "Why cold outreach fails" not "Topic 2")
- First chapter always starts at 00:00
- Last chapter should be a clear conclusion/outro

---

## Step 4 — Social media clips

Write 3 social posts, each optimized for a different platform:

**LinkedIn post:**
- 150–250 words
- Professional tone, insight-first
- End with a reflective question to drive comments
- No hashtags in body — add 3 relevant ones at the end on their own line

**X (Twitter) thread:**
- 5–7 tweets
- Tweet 1: hook (under 280 chars, must stand alone)
- Tweets 2–6: one insight per tweet, concrete and specific
- Final tweet: call to action (link to episode or subscribe)
- Number each tweet: 1/ 2/ etc.

**Instagram caption:**
- 100–180 words
- Conversational, personal tone
- 5–8 hashtags at the end

---

## Step 5 — SEO metadata

Provide:

```
Title (under 60 chars): [title]
Meta description (under 155 chars): [description]
Primary keyword: [keyword]
Secondary keywords: [keyword1], [keyword2], [keyword3]
```

Rules:
- Title must include the primary keyword naturally
- Meta description must include a benefit or outcome
- Keywords should reflect what someone would search to find this episode

---

## Step 6 — Newsletter summary

Write a 100–150 word newsletter blurb suitable for pasting into a weekly digest:

```
**[Episode title]**

[2-sentence summary of what the episode covers]

[1 key insight or quote from the episode]

[1-sentence reason why subscribers should listen]

🎧 [Listen / Watch] → [leave placeholder: INSERT_LINK]
```

---

## Output format

Deliver all 5 outputs in order, each under a clear H2 heading:

1. `## Show notes`
2. `## Chapter markers`
3. `## Social media`
4. `## SEO metadata`
5. `## Newsletter`

Separate each section with a horizontal rule (`---`).

After all sections, add:

```
---
✅ Podcast workflow complete. All assets ready to publish.
Want me to adjust tone, length, or regenerate any section?
```

---

## Error handling

- **Transcript too short (under 500 words):** Complete all steps but note: "This transcript is short — outputs may be less detailed than usual."
- **Non-English transcript detected:** Process in the source language, then add a note offering to translate all outputs to English.
- **No clear topic or guest:** Infer from context. Do not ask clarifying questions unless transcript is completely ambiguous.
- **Explicit or adult content:** Decline and explain this skill is for general-audience podcasts only.

---

## Version history

- 1.0.0 — Initial release. Full pipeline: show notes, chapters, social (LinkedIn/X/Instagram), SEO metadata, newsletter.
