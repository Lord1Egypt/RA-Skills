# YouTube policy and originality gates

Status: checked against YouTube policy coverage and help text in Nov 2026. Policies change; before a channel plan depends on this, have the user read the current YouTube Partner Program policies in YouTube Help.

## What the rules target (verified)

- **Inauthentic content**: mass-produced or repetitive content, template-like videos, image slideshows, templated storylines, near-identical videos with minimal variation. Applies to the whole channel, not one video. It can make a channel ineligible for monetization.
- **Reused content**: compilations or re-uploads without significant commentary, modification or original value.
- **Clarification effective 16 Jul 2026** (reported summary, three groups): generic or repetitive content; unsatisfying or off-putting content, including unrelated AI clips stitched together; AI personas presenting as experts on sensitive topics (health, legal, finance, politics).
- It is not a ban on AI tools, stock footage or synthetic voices. The sources checked said nothing specific about voiceover or about a disclosure duty for narration alone; the "altered or synthetic content" label in YouTube Studio has its own criteria, so the user must read it and decide.

## What this means for this skill

A stock-clip video with a synthetic voice is acceptable only when the video itself adds value: research, analysis, a point of view, structure, examples, original graphics, the user's own footage or voice. The scripts can lint some surface signs (no angle, repeated sentences, repeated openings), but they cannot judge originality. A human must.

## Originality gates (all must be true before publishing)

1. **Angle.** One sentence in `project.json` saying what this video offers that the top results do not. If it cannot be written, do not make the video.
2. **Sources.** Facts come from named sources listed in `sources` and in the description. No invented numbers, quotes or events.
3. **Commentary.** Narration analyses, compares, explains or argues; it does not just read a Wikipedia summary aloud.
4. **Visual relevance.** Each shot matches the sentence. No unrelated filler clips; mix in maps, charts, text cards, diagrams, screenshots with permission, or the user's own footage.
5. **Variation across the channel.** Different structures, hooks and lengths between videos; no identical template every time. The user should not publish dozens of videos a week made by this pipeline.
6. **Human pass.** The user watches the full video, fixes errors and approves. Record it in `review.human_checked`.
7. **Own voice option.** Offer the user's own recording (`voice.engine: own`) as the higher-trust path, especially for opinion or expertise content.

## Sensitive topics

Health, legal, finance, politics and news: do not present a synthetic voice or avatar as a doctor, lawyer, advisor or journalist. Cite primary sources on screen, state that this is general information, avoid individualized advice, and prefer a human narrator. `project.py validate` warns when `topic_category` is one of these and the voice is synthetic.

## Disclosure and honesty

- Put a plain line in `youtube.disclosure` when narration is synthetic (for example "Narration is AI-generated"), and decide the Studio "altered or synthetic content" setting with the user.
- Do not use thumbnails or titles that promise something the video does not deliver.
- Do not imply that stock footage shows the real event it illustrates; say "stock footage" or "illustrative" where it could mislead (news, historical claims).
