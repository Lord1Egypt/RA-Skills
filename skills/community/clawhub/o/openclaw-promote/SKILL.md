# Promote — Content Distribution Skill

You have access to tools for publishing content across multiple channels. When the user asks you to promote a project, product, or article, follow these guidelines.

## General approach

1. **Ask for context first** — What is the project? Who is the target audience? What's the URL? What's the key value proposition?
2. **Tailor content per platform** — Each platform has a different audience and culture. Never cross-post identical text.
3. **Start with drafts** — Use `publishStatus: "draft"` or `published: false` where available so the user can review before going live.
4. **Publish in batches** — Don't post everywhere simultaneously. Stagger across hours/days for better reach.

## Platform-specific writing guidelines

### Hacker News (`publish_hackernews`)
- **Audience:** Developers, founders, tech enthusiasts. Very skeptical of marketing.
- **Tone:** Matter-of-fact, technical. Zero superlatives or buzzwords.
- **Title:** State what it is, not why it's great. "Show HN: X — a Y that does Z" works well.
- **Don't:** Use exclamation marks, claim to be "revolutionary", or sound like a press release.
- **Do:** Focus on the technical approach, what problem it solves, what's novel.
- **Timing:** Weekday mornings US Eastern (9-11 AM ET) for best visibility.

### Reddit (`publish_reddit`)
- **Audience:** Varies by subreddit. Research the community first.
- **Tone:** Authentic, conversational. Write like a community member, not a marketer.
- **Subreddits to consider:** r/programming, r/webdev, r/selfhosted, r/opensource, r/sideproject, r/InternetIsBeautiful — pick based on the project.
- **Don't:** Sound promotional. Reddit users will downvote anything that feels like an ad.
- **Do:** Share your story, what you learned, ask for feedback. "I built X because Y" works well.

### Medium (`publish_medium`)
- **Audience:** General tech readers, professionals looking to learn.
- **Tone:** Educational, storytelling. Start with a hook.
- **Format:** Use headers, code blocks, and images. Long-form (800-2000 words) performs best.
- **Don't:** Write thin content. Medium readers expect depth.
- **Do:** Tell the story behind the project. What problem, what approach, what you learned.

### Dev.to (`publish_devto`)
- **Audience:** Developers. More welcoming and beginner-friendly than HN.
- **Tone:** Friendly, tutorial-style. Technical but approachable.
- **Format:** Markdown with code samples. Can be shorter than Medium.
- **Tags:** Use popular, relevant tags (max 4). Check trending tags on Dev.to.
- **Do:** Include setup instructions, code examples, architecture decisions.

### Hashnode (`publish_hashnode`)
- **Audience:** Developers, similar to Dev.to but smaller community.
- **Tone:** Technical blog post style.
- **Format:** Markdown, similar to Dev.to content.
- **Do:** Cross-post your Dev.to or Medium content (with canonical URL).

### Twitter/X (`publish_twitter`)
- **Audience:** Broad tech audience. Founders, developers, designers.
- **Tone:** Punchy, concise. Every word counts in 280 characters.
- **Format:** Lead with the hook. Use line breaks for readability.
- **Don't:** Use hashtags excessively. One or two max.
- **Do:** Include the URL. Mention relevant accounts. Use "I just shipped X" or "Built X to solve Y" patterns.

### Bluesky (`publish_bluesky`)
- **Audience:** Tech-savvy early adopters, many ex-Twitter users.
- **Tone:** Similar to Twitter but slightly more conversational.
- **Format:** 300 character limit. URLs are auto-linked.
- **Do:** The community is receptive to open-source and indie projects.

### Mastodon (`publish_mastodon`)
- **Audience:** Privacy-conscious, open-source advocates.
- **Tone:** Community-oriented. Less "hustle culture" than Twitter.
- **Format:** 500 character limit on most instances.
- **Do:** Emphasize open-source aspects, privacy features, self-hosting options.
- **Don't:** Sound too corporate or growth-hacky.

### LinkedIn (`publish_linkedin`)
- **Audience:** Professionals, B2B buyers, recruiters.
- **Tone:** Professional but personal. "I learned" and "We built" narratives work.
- **Format:** Short paragraphs with line breaks. Include article link when relevant.
- **Don't:** Write corporate-speak. LinkedIn engagement favors authentic personal stories.
- **Do:** Frame it as a professional journey or industry insight.

### Product Hunt (`publish_producthunt`)
- **Audience:** Early adopters, product enthusiasts, investors.
- **Format:** Tagline (60 chars), description, maker comment, screenshots.
- **Maker comment:** Tell the personal story. Why you built it, for whom, what's next.
- **Do:** Prepare screenshots/GIF. Launch at 12:01 AM PT. Rally your network.

## Workflow example

When the user says "promote byoky":

1. Ask about target audience and key messages if not clear
2. Generate platform-specific content for each configured channel
3. Present all drafts to the user for review
4. Publish to channels one by one after approval
5. Report back with links to all published posts
