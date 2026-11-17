## Description:

Recommends movies from user mood, genre, actor, director, or year preferences, queries Douban ratings, and helps manage watched and want-to-watch lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

End users and agents use this skill to choose movies based on mood or genre, retrieve Douban movie information, and maintain local watched and want-to-watch lists. It is most useful for Chinese-language movie discovery workflows that can tolerate fallback recommendations when Douban lookup fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Movie searches may be sent to Douban during recommendation and rating lookups.

Mitigation: Avoid entering sensitive viewing preferences or private titles when network lookup is enabled.

Risk: Cache, watched-history, and wishlist JSON files may retain local viewing preferences.

Mitigation: Review or delete generated JSON files on shared machines or when retained movie history is not desired.

Risk: Watched and wishlist command parsing is incomplete and may save placeholder entries.

Mitigation: Review saved records after use and correct or remove placeholder entries before relying on the lists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/movie-recommender)
- [Douban Developers](https://developers.douban.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown-style Chinese text responses with movie lists, ratings, summaries, and locally stored JSON lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform network lookups to Douban, cache lookup results locally, and write watched or want-to-watch JSON records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
