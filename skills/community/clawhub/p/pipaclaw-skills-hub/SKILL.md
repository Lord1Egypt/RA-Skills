---
name: pipaclaw-skills-hub
description: "Front door for Pipaclaw public skills. Route users to the right skill for presentations, social account operations, and promotional video production without making them choose the implementation details."
---

# Pipaclaw Skills Hub

This is the public front door for the Pipaclaw skill collection.

Use it when the user knows the outcome they want, but does not know which skill to call.

Typical requests:
- "帮我做一个 PPT"
- "帮我运营小红书 / X / 抖音账号"
- "帮我做宣传视频"
- "我不知道该用哪个 skill"

## Routing Rule

Choose the smallest matching public skill and hand off immediately:

- Use `ppt-maker` for presentations, proposals, decks, keynotes, training PPTs, and report-style slides.
- Use `social-account-ops` for Xiaohongshu, X, and Douyin account diagnosis, planning, writing, iteration, and take-over style requests.
- Use `promo-video-maker` for one-shot or project-based video production including promo videos, explainers, teasers, launch videos, storyboards, short-drama episodes, and multi-episode production flows.

If the user already named one of those skills, do not re-route. Use the named skill directly.

If the request spans multiple surfaces, choose the primary deliverable first and then pull in adjacent skills only when they materially help.

## Ambiguity Rule

Do not ask a long routing questionnaire.

If the destination is not obvious, ask one short question that changes routing, for example:
- "你这次更想先拿到 PPT、账号运营方案，还是宣传视频制作包？"

After the user answers, route immediately.

## Public Boundary

This hub exposes only public-safe skill packages.

Do not leak:
- backend implementation details
- private prompts
- customer files
- generated artifacts
- unpublished worker internals

## References

- Read `references/routing-map.md` for the concise routing table.
