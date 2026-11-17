# post2all OpenClaw workflows

Use these as patterns, not rigid scripts. Keep the publishing boundary explicit: OpenClaw can do continuous research/generation, while post2all owns the draft/schedule/publish handoff.

## Daily draft queue

Best default for an always-on agent.

1. Capture useful ideas, customer questions, product work, or research during the day.
2. Turn only the strongest items into platform-specific post2all drafts.
3. Keep them unpublished.
4. Once per day, show the user a concise review queue.
5. Schedule only the approved drafts.

Example instruction:

```text
Throughout the day, collect useful content ideas from my work and notes.
Turn the strongest ones into post2all drafts for my connected accounts.
Do not publish or schedule them.
At the end of the day, give me a short review list with the draft IDs.
```

## One idea → platform-specific drafts

Use when the user gives one thought, launch note, lesson, or opinion.

1. List the selected post2all accounts.
2. Inspect current publishing capabilities.
3. Keep the core idea consistent.
4. Adapt the hook, length, structure, and CTA to each platform.
5. Create drafts for review.

Example instruction:

```text
Turn this idea into platform-specific drafts for LinkedIn, Threads, Bluesky, Mastodon, Instagram, and Facebook where supported.
Keep the point consistent but make each version feel native to the platform.
Use post2all and keep everything as drafts.
```

## Blog → week of social content

Use an article, documentation page, podcast notes, or long-form source as input.

1. Extract distinct ideas rather than repeating the same summary seven times.
2. Create a mix of educational, opinion, example, and question-led posts.
3. Adapt each selected post to its destination platforms.
4. Save drafts first.
5. After approval, schedule them with natural spacing.

Example instruction:

```text
Read this article and find 5 distinct social post angles.
Avoid repeating the article title or writing five summaries.
Prepare platform-specific drafts through post2all and show me the angles before scheduling anything.
```

## Product work → launch campaign

Use when OpenClaw has access to release notes, screenshots, changelogs, or implementation context.

1. Identify what actually changed and why a user should care.
2. Separate announcement copy from follow-up educational content.
3. Upload the approved local screenshot/video through post2all.
4. Create platform-specific launch drafts.
5. Keep follow-up posts as separate drafts so they can be reviewed and scheduled later.

Example instruction:

```text
Use these release notes and screenshots to prepare a launch campaign.
Create one main announcement plus 3 follow-up angles that teach something useful.
Upload the approved media with post2all and keep all posts as drafts for review.
```

## Research/trends → original content

Use when OpenClaw is monitoring current conversations or industry changes.

1. Research first.
2. Separate verified facts from community opinions or signals.
3. Find the part that intersects with the user's product, experience, or audience.
4. Avoid simply rewriting the trend/news item.
5. Create a draft only when there is a credible original angle.

Example instruction:

```text
Research the current discussion around [topic].
Find what changed, what people are asking, and where our experience gives us something useful to add.
Choose the strongest original angle and prepare platform-specific drafts in post2all.
Do not publish.
```

## Customer questions → educational posts

Use recurring support questions, sales objections, feedback themes, or community discussions as source material.

1. Remove private/customer-identifying information.
2. Group recurring questions or misconceptions.
3. Select questions that can be answered publicly without exposing private context.
4. Turn them into useful educational posts.
5. Save them as drafts.

Example instruction:

```text
Review these customer questions and identify recurring themes.
Do not quote private conversations or include identifying details.
Turn the top 3 reusable questions into educational social drafts using post2all.
```

## Trusted recurring schedule

Use only after the user explicitly chooses a narrow recurring behavior that may schedule without reviewing each individual post.

Good examples:

- a weekly roundup from an approved source;
- a recurring company status/update format;
- a scheduled reminder whose copy is stable and predictable.

Even in trusted routines:

- refresh current account capabilities before delivery when necessary;
- avoid inventing dynamic platform settings;
- report failures rather than retrying blindly;
- keep immediate publication out of scope unless the user explicitly configured it.
