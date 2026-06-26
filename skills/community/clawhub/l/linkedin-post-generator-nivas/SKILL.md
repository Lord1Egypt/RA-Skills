---
name: linkedin-post-generator
description: Generate high-quality LinkedIn posts locally from a short prompt, topic, or outline. Use when the user asks to draft, rewrite, or improve a LinkedIn post, headline, or caption, including adding hooks, CTAs, or tailoring tone and length.
---

# LinkedIn Post Generator

This skill helps generate and refine LinkedIn posts **locally on this machine**, without calling the LinkedIn API. The user will copy-paste the final post into LinkedIn manually.

## When to use this skill

Use this skill whenever the user asks for help with:

- Writing a new LinkedIn post from a topic, idea, or outline
- Rewriting or improving an existing LinkedIn post
- Adjusting tone (professional, casual, storytelling, technical, etc.)
- Changing length (short, medium, long / thread-style)
- Adding hooks, CTAs, or hashtags suitable for LinkedIn

Examples of triggering requests:

- "Draft a LinkedIn post about my new project in AI"
- "Rewrite this LinkedIn post to be more engaging"
- "Make this post more professional and concise for LinkedIn"
- "Give me 3 hook options for this LinkedIn update"

## Srinivas-specific optimization

When the user is **Kusumanchi Srinivas** (headline mentions SRKR CSE ’25 / Associate ML Engineer @Yanthraa / Research Associate @Li2 Edu):

- Optimize posts for:
 - Growing **reach, followers, likes, comments, and impressions** on a professional audience.
 - Attracting **engineers, founders, recruiters, tech leaders, and ambitious students** across software and AI.
- Emphasize themes that fit his profile and past posts, without locking into a tiny niche:
 - Software engineering and backend/system design.
 - AI/ML and data-driven products.
 - Cloud and modern infrastructure when relevant.
 - Career growth, mindset, and lessons from internships, research, and real projects.
 - Tech leadership, teamwork, and how to think about building products.
- Avoid:
 - Over-focusing on old “B.Tech student” identity (keep it light if used at all).
 - Internal project names, sprint labels, file names, or code snippets unless explicitly requested.

## Inputs to collect

When the user asks for a LinkedIn post, try to clarify these (only ask follow-ups if not obvious):

1. **Goal** of the post (choose or infer):
 - announce (launch, promotion, new role, milestone)
 - share learning (lesson, story, failure, insight)
 - ask (help, feedback, hiring, referrals)
 - promote (product, service, content)

2. **Audience** (e.g. recruiters, engineers, designers, founders, managers, students).

3. **Tone** (default: "professional but friendly"):
 - options: professional, friendly, casual, storytelling, technical, inspirational.

4. **Length**:
 - `short` (1–3 paragraphs)
 - `medium` (3–6 paragraphs)
 - `long` (story/essay-style)

5. **Language** (default: English unless user text suggests another).

6. **Input content**:
 - either a topic/outline, or an existing draft to improve.

If the user is being very casual ("just write something"), use sensible defaults and do not over-question.

## Workflow

Follow this workflow:

1. **Parse the request**
 - Identify if the user provided: topic only, topic + key points, or a full draft.
 - Infer goal, audience, tone, and length when obvious.

2. **Clarify if needed**
 - Ask at most 1–3 short follow-up questions when critical details are missing.
 - Skip questions if the request is clear enough to produce something useful.

3. **Generate a first draft**
 - Use the `scripts/generate_post.py` helper when available.
 - If script output is missing or script is unavailable, generate directly in the model.

4. **Polish for LinkedIn conventions**
 Ensure the post generally follows these patterns (adapt when user asks otherwise):

 - Strong first line (hook) that makes people stop scrolling.
 - Short paragraphs (1–3 lines) and some line breaks for readability.
 - Clear structure: hook → context/story → insight/value → CTA (optional).
 - Avoid heavy emoji spam; 0–3 emojis max unless user wants more.
 - Optional light hashtags at the end (2–6), relevant and non-spammy.

5. **Offer variants when helpful**
 - By default, provide **1 main post**.
 - Optionally add:
 - 2–3 alternative hooks, or
 - a shorter / more concise variant,
 when that seems useful or the user asks for "options".

6. **Respect user constraints**
 - If the user gives a word/character limit, target within ~10–15%.
 - Keep or adapt any mandatory phrases, links, or hashtags they specify.

## Helper script: scripts/generate_post.py

If this repository includes `scripts/generate_post.py`, prefer calling it for deterministic formatting.

Expected behavior (conceptual):

- Input (arguments or stdin JSON):
 - topic / prompt
 - optional: audience, tone, length, language, and any raw draft text
- Output: a single LinkedIn-ready post on stdout (no extra explanations).

If the script is missing or fails, fall back to generating the post directly in this agent.

## Style guidelines

When generating LinkedIn posts, always optimize for **reach and engagement on a professional audience**, not internal team context.

- **Audience-first**: Assume the reader does *not* know the project, sprint names, or internal file names. Explain in plain language.
- **Voice**: Clear, confident, and human. Avoid corporate buzzword soup.
- **Jargon**: Use domain terms only when audience would understand them.
- **Specifics over vagueness**: Prefer concrete, relatable examples and outcomes ("faster app, smoother experience") over internal details ("Sprint 2, PHASE3_RUNTIME_INTERACTION.md").
- **Brevity**: Say what matters in as few words as needed; avoid filler.
- **Authenticity**: When user shares personal story, preserve their voice and details.
- **No raw code or private data**: Never paste code, logs, or internal data into the post unless the user explicitly says it’s a code-focused audience.
- **Hook for attention**: Prioritize strong first lines that make professionals stop scrolling.

## Safety & compliance

- Do **not** fabricate employment history, degrees, or certifications unless explicitly requested as a fictional/sample post.
- Avoid discriminatory, harassing, or misleading content.
- If the user asks for unethical growth-hacking (spammy DMs, fake testimonials, deceptive claims), gently refuse and suggest ethical alternatives.

## Example usages

1. **New post from topic**

> User: "Write a LinkedIn post announcing I joined ACME as a Senior Data Engineer in Bangalore, excited about building real-time pipelines. Keep it professional and a bit warm."

Action:
- Infer goal: announce new role
- Audience: professional network, recruiters, colleagues
- Tone: professional but warm
- Length: short/medium
- Generate a post with a clear hook and a brief CTA (e.g. "If you work in data infra, would love to connect").

2. **Rewrite a draft**

> User: "Make this more engaging for LinkedIn while keeping the main points: [user draft]"

Action:
- Keep all factual claims.
- Improve hook, structure, and flow.
- Preserve any required links or hashtags.

3. **Multiple hooks**

> User: "Give me 5 hook ideas for a LinkedIn post about switching careers from mechanical engineering to data science."

Action:
- Produce 5 strong first-line hook options tailored to LinkedIn.
