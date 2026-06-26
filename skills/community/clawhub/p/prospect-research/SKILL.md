---
name: prospect-research
version: 0.1.0
description: >
  Builds a comprehensive pre-meeting intelligence brief on any company or prospect.
  Surfaces business context, decision-maker background, industry signals, and conversation angles.
  Use when: "research [company]", "prospect research", "tell me about [company]", "company profile",
  "pre-call prep", or any request for intel before a meeting, call, or outreach.
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# Prospect Research

Build a comprehensive intelligence brief on any company before a meeting, call, or outreach. The output should make you sound like you've known this company for months.

## Research Scope

### 1. Business Fundamentals
What does this company actually do? What do they sell, who do they sell to, and how do they fulfill? B2B, B2C, DTC, wholesale, or hybrid? Single location or multi-site? Key products, services, or platforms.

### 2. Company Trajectory
How is the business growing or changing? New product lines, geographic expansion, acquisitions, funding rounds, major partnerships, technology investments. Focus on the last 12 months; flag anything significant within 2 years.

### 3. Executive / Contact Background
Who is the target contact? Founder, hired exec, or family business? Professional history, how long at the company, other ventures. Public presence: LinkedIn activity, podcasts, interviews, press. What do they seem to care about based on what they post or say publicly?

### 4. Industry Signals
- Customer reviews mentioning pain points relevant to your offering
- Technology stack clues (platforms, integrations, tools they use)
- Job postings that signal growth areas or operational gaps
- Press or announcements about strategy shifts, partnerships, or new initiatives
- Competitive landscape: who are their alternatives, how do they position themselves?
- Seasonal patterns, growth indicators, revenue estimates if discoverable

### 5. Recent Activity (Last 90 Days Priority)
News mentions, press releases, social posts, website updates, blog content, third-party coverage. What's top of mind for this company or person right now?

## Research Standards
- **Verify before asserting.** If you can't confirm something, say so or skip it. Do not fill gaps with assumptions.
- **Cite or note sources** when useful, especially for key claims.
- **Stay on-topic.** If a rabbit hole doesn't connect back to business relevance, leave it out.
- **Quality over speed.** Accuracy matters more than a fast output.

## Output Format
Deliver a **narrative intelligence brief**: readable, not overly templated. Use light structure (headers are fine) but write in a way that flows. Target: something the user can read in 10 minutes and walk into a conversation fully prepared.

End with:
- **Fit Assessment:** Strong / Moderate / Weak, with one sentence on why
- **2-3 Conversation Angles:** Specific, natural openers tied to the prospect's actual situation. Not generic, not salesy.

## Tools
- Web search for company research and news
- Web fetch for website analysis, job boards, press
- Any available enrichment tools (Apollo, ZoomInfo, LinkedIn, etc.)

## Example Triggers
- "Research Hadrian before my call"
- "What do I need to know about this company?"
- "Prospect research on [company name]"
- "Pre-call prep for my meeting with [person] at [company]"
- "Tell me about [company] before I reach out"
