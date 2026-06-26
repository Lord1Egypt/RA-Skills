# Routing Map

Use this hub only to route into the right public skill.

## Skill Map

- `ppt-maker`
  Use for PPT, keynote, proposal deck, investor deck, training deck, sales deck, project report, and presentation work.

- `social-account-ops`
  Use for Xiaohongshu, X, and Douyin account diagnosis, operating plans, post writing, iteration, and managed account work.

- `promo-video-maker`
  Use for promo videos, explainers, launch videos, teasers, ad scripts, beat sheets, shot lists, and editor handoff packs.

## Routing Priority

When a request could fit more than one skill:

1. Choose the main output format first.
2. Route to the skill that owns that output.
3. Only pull adjacent skills if they improve the result materially.

Examples:
- PPT introducing a product launch: start with `ppt-maker`.
- Social campaign that also needs a launch trailer: start with `social-account-ops` if the core problem is account operation, otherwise start with `promo-video-maker`.
- Video storyboard for a deck presentation: start with `promo-video-maker`.
