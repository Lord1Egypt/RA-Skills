# Content Bank Guide

The content bank is the fuel for the entire pipeline. Write strong angles once; the
planner generates a week of cross-platform posts from them automatically.

## What Is an Angle?

An angle is a single perspective or story about your app — the raw material for one
day's worth of TikTok/YouTube videos, plus the X tweets and Facebook post that
accompany them.

A good angle has:
- A **hook** — one punchy sentence that stops the scroll
- **Texts** — 3–5 short lines that expand the hook into a video script
- A **caption** — the TikTok/YouTube caption with hashtags

## File Format

`content-bank.json` is a JSON array of angle objects:

```json
[
  {
    "id": "unique-kebab-id",
    "hook": "One punchy sentence that is the hook",
    "texts": [
      "Opening line — restate or escalate the hook",
      "The problem or insight (1-2 sentences)",
      "The turn or solution",
      "The close / mini-CTA"
    ],
    "caption": "TikTok/YouTube caption. Can include hashtags. #YourApp #IndieApp"
  }
]
```

The `id` must be unique. The planner uses it to track which angles have been posted
and will never repeat an angle until the bank is exhausted.

## Facebook Brand Content Bank

`fb-brand-content-bank.json` is a separate array for the longer-form Facebook posts
(Mon/Wed/Fri). Format:

```json
[
  {
    "id": "fb-unique-id",
    "pattern": "behind-the-scenes",
    "content": "Full post text here. Can be multi-paragraph.\n\nEngagement question at the end."
  }
]
```

Facebook posts don't come from the angle bank — they're independent. Write 10–20 to
start. The planner picks them in order.

## Writing Great Hooks

The hook is the most important part. It should:

- Start a story or raise a question mid-stream ("I spent 3 years doing this wrong")
- State a surprising fact or counter-intuitive truth
- Be relatable to your target user's daily frustration
- Be short enough to read in one breath

**Bad hook:** "Our app helps you be more productive."
**Good hook:** "I lost 4 hours last week looking for a note I took on my phone."

## Writing the Texts Array

Think of this as a 15–30 second video script:

1. **Line 1** — Restate or slightly escalate the hook
2. **Line 2** — The problem. Be specific. Use numbers if you can.
3. **Line 3** — The insight or turn. What changed?
4. **Line 4** — The close. Low-pressure. Can mention the app.

Each line should be 1–2 sentences. The planner uses these to generate X tweets
by pulling specific lines for different tweet patterns.

**Example:**

```json
{
  "id": "lost-notes-frustration",
  "hook": "I lost 4 hours last week looking for a note I took on my phone",
  "texts": [
    "I took a note during a meeting. A good one. Gone.",
    "Searched everywhere — notes app, photos, browser tabs. Nothing.",
    "Turns out I'd voice-noted it on my commute and never reviewed it.",
    "That was the moment I built a better system."
  ],
  "caption": "If you've ever lost a note you actually needed 😭 #ThoughtTrack #Productivity #DevLife"
}
```

## Angle Categories

A healthy bank has a mix of these categories. Aim for 3–4 angles per category
when starting out:

| Category | Description | Example hook |
|---|---|---|
| Pain point | The problem your app solves, without mentioning the app | "I missed a deadline because I forgot I'd written down the date" |
| Frustration | Specific everyday friction | "My notes app has 847 notes and I can't find any of them" |
| Discovery | The "aha moment" when someone found a better way | "I didn't realize how much time I was wasting until I tracked it" |
| Social proof | What users say (anonymized or paraphrased) | "Someone told me they use this during their commute every day" |
| Behind the scenes | Indie dev life, building in public | "I rewrote this feature 4 times before I got it right" |
| Tip / how-to | A concrete tip related to your app's domain | "3 things I do every Sunday that make my week less chaotic" |
| Myth buster | Counter-intuitive take | "Productivity apps don't make you productive — here's what actually does" |
| Relatable meme | Humor + recognition | "Me: I'll remember this later. Also me: I did not remember this." |

## How Many Angles Do You Need?

At 3 angles per day × 7 days = 21 angles per week.

- **Starting out:** Write 30 angles. That's ~6 weeks of content.
- **Maintenance:** Add 20–30 new angles every 4–5 weeks.
- **The planner alerts you** when angles run low.

## Keeping the Bank Healthy

### When to Refresh

Run the planner with `--dry-run` to see how many angles remain:

```bash
node scripts/weekly-planner.js --dry-run
```

The output shows: `Available: N unused angles (M total)`

When you have fewer than 21 unused angles (one week's worth), start writing new ones.

### How to Add Angles

Just append to `content-bank.json`. New angles get picked up on the next planner run.

### Recycling

The planner never repeats an angle until ALL angles have been used. Once all are
exhausted, reset `posting-history.json`:

```bash
echo '{"posted":[],"postedFbBrand":[],"lastApp":null}' > posting-history.json
```

Then run the planner again.

### Tracking Performance

After each week, check which angles drove the most engagement. Keep the
high-performers in your reference doc for writing new angles in the same vein.

## Tips for Indie App Devs

1. **Write from experience** — Your personal frustrations are your best hooks.
   Audiences respond to specific, authentic observations.

2. **One idea per angle** — Don't try to say everything. Each angle explores
   a single facet of the problem your app solves.

3. **Don't mention the app too early** — Build curiosity first. The app is the
   solution to the problem you've described — introduce it at the end, not the top.

4. **Vary the emotional tone** — Mix frustration, humor, discovery, and insight.
   A bank full of only "pain point" angles feels repetitive.

5. **Write in batches** — 30 angles in one sitting is easier than 3 angles every
   few days. Schedule a "content writing" block once a month.

6. **Use your App Store reviews** — User reviews are pre-written hooks. Paraphrase
   the common themes into angles.
