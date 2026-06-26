---
name: blog-hexo
description: Draft and publish Hexo posts end-to-end (front matter + SEO polish + deploy)
metadata: { "openclaw": { "requires": { "bins": ["node", "npm", "npx", "hexo"] } } }
---

# blog-hexo Skill

Use this skill to manage the entire Hexo workflow:
- **Draft mode**: create or update Markdown with `published: false` front matter so it remains a draft.
- **Publish mode**: polish existing posts, ensure SEO best practices, and run the Hexo commands to deploy.

## Requirements
- Node.js + npm/npx installed locally (Hexo CLI depends on Node 18+).
- Hexo CLI available (`npx hexo ...`).
- Local access to the Hexo blog repository path (ask the user if it is not documented in memory).
- Git credentials or deployment tokens configured so `hexo deploy` can push to the hosting remote (e.g., GitHub Pages).
- Permission to read/write Markdown, config, and public folders within that repo.
- Optional: ability to preview locally requires `npx hexo clean && npx hexo generate`.

## Draft Mode
Use this skill whenever the user wants to draft a Hexo blog post that should **not** publish yet.

## Front Matter Template
Always start new drafts with this exact block (update values as needed):

```
---
title: ''
published: false
catalog: true
header-img: /img/article_header/article_header.png
date: YYYY-MM-DD HH:mm:ss
subtitle:
tags: []---
```

Notes:
- Keep `published: false` so `hexo generate` skips the draft.
- When picking tags, consult the preferred list (AI, OpenClaw, Agent, Technical, Life) unless the user specifies otherwise.
- Set `title` and `date` when drafting. Use the user’s timezone (default: America/Los_Angeles).
- Tags listed are the common ones; remove or add as appropriate for the post.

## Drafting Workflow

## Path Confirmation
- Before creating a file, check memory/reference notes for the blog path. If it isn’t specified, ask the user which local path to use.
1. Confirm the post topic, target keywords, audience, and tone.
2. Create the Markdown file under the confirmed blog path (ask if unknown).
3. Insert the front matter template above, filling in title/date/subtitle/tags as needed.
4. Write the draft content (introduction → body with H2/H3s → conclusion). Follow the user’s SEO preferences if provided.
5. Do **not** run `hexo deploy` unless the user explicitly wants to publish. If you run `hexo clean/generate` to preview locally, the `published: false` flag keeps the draft out of the public site.
- When ready to publish, remove `published: false` and continue with the Publish Mode checklist below for SEO polish + deployment.

## Reminders
- Preserve existing posts—only add or edit the target draft file.
- Mention in updates whether the draft is ready for review or needs more info.
- When ready to publish, remove `published: false` and follow Publish Mode (below) for SEO polish + deployment.

## Publish Mode

Before editing, confirm the repository path and ensure you have permission to modify it. If the path is not in memory, ask the user directly.

Before removing `published: false` or running `npx hexo deploy`, explicitly confirm with the user that they want the post to go live. If confirmation is not granted, stop after preparing the draft.

# SEO Writer

You write blog posts that rank on Google AND are worth reading. SEO without the soul-sucking keyword stuffing.

## Before Writing

Get from the user:
1. **Target keyword** — The main term they want to rank for
2. **Secondary keywords** — 3-5 related terms
3. **Search intent** — Informational, transactional, navigational, or commercial?
4. **Target audience** — Who's searching for this?
5. **Word count target** — Default: 1,500-2,000 words
6. **Tone** — Professional, casual, technical, etc.

## SEO Writing Framework

### Title (H1)
- Include target keyword, ideally near the front
- Under 60 characters (so it doesn't truncate in search results)
- Make it compelling — it's competing with 9 other results on the page
- Formats that work: "How to [X]", "[Number] Ways to [X]", "[X]: The Complete Guide"

### Meta Description
- 150-160 characters
- Include target keyword naturally
- Write it like ad copy — it's your pitch in search results
- Include a reason to click

### URL Slug
- Short, keyword-rich, lowercase, hyphens between words
- `/how-to-write-cold-emails` not `/how-to-write-the-best-cold-emails-that-get-replies-in-2024`

### Content Structure

**Introduction (100-150 words)**
- Hook the reader in the first sentence
- State what they'll learn
- Include target keyword in the first 100 words

**Body — Use H2 and H3 headers**
- Each H2 should target a secondary keyword or subtopic
- H3s break up long sections
- Aim for 300 words max per section before a new header
- Use bullet points and numbered lists (Google loves them, readers love them)

**Conclusion (100-150 words)**
- Summarize key takeaways
- Include a CTA (what should they do next?)
- Don't introduce new information

### Keyword Placement Rules

- **Target keyword appears in:** Title, first paragraph, one H2, conclusion, meta description
- **Keyword density:** 1-2% max. If it sounds forced, you've overdone it.
- **Use variations:** Synonyms, related phrases, natural language variations
- **LSI keywords:** Include semantically related terms throughout (Google understands context)

### Internal & External Links

- **Internal links:** Link to 2-3 other relevant pages on their site
- **External links:** Link to 2-3 authoritative sources (builds trust with Google)
- **Anchor text:** Descriptive, not "click here"

### Readability

- Short sentences. Vary length for rhythm.
- Short paragraphs (2-3 sentences max)
- Flesch reading ease: aim for 60+ (understandable by most adults)
- Use transition words
- Break up text with headers, lists, images (suggest image placements with alt text)

### Featured Snippet Optimization

For "how to" or "what is" queries:
- Include a concise definition or step-by-step list right after the relevant H2
- Use numbered lists for processes
- Use tables for comparisons
- Keep the snippet-target answer under 50 words


## Hexo Command Workflow

Whenever you modify or create a post in the user-specified blog repository, confirm the path (ask if unsure) and run:
1. `npx hexo clean`
2. `npx hexo generate`
3. `npx hexo deploy`

These commands rebuild the site and push to the configured remote using the user’s git credentials.

## Improving Existing Markdown

You don’t just draft from scratch—- If this is a brand-new article that should stay unpublished, use the `draft-hexo` skill first to create the draft with `published: false`, then hand it here when ready to polish/publish.
you often receive an existing Markdown article. When that happens:
- Preserve front matter (title, tags, dates).
- Read the current structure, then rewrite sections using the SEO framework above.
- Re-run the Hexo workflow afterwards so the live blog stays in sync.


## Rules
- Write for humans first, search engines second
- No keyword stuffing. Ever. Google is smarter than that.
- Every section should deliver value. No filler paragraphs to hit word count.
- Cite statistics and claims. "[Source]" placeholder is fine if you need to.
- Suggest where to add images, infographics, or embedded content.

## Credits
- Based on the original `ai-seo-writer` skill from ClawHub. Thanks to the original author for the SEO framework; Jessie customized it for Hexo publishing.
