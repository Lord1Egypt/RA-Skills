# Novel Blurb Variants (Chinese)

![Novel Blurb Variants promotion](assets/promo-1600x900.png)

Turn a real story synopsis into reader-facing Chinese book copy: three distinct positioning options that respect spoiler boundaries, plus one concise selling line.

Built for Chinese-speaking shop owners, novelists, and social-media creators. It produces book blurbs only—not cover design, video storyboards, or submission synopses.

## Input and output

Provide real information for all three fields:

- **Story synopsis**: protagonist, starting point, central conflict, relationships or choices, and what may be publicly revealed.
- **Genre**: for example mystery, romance, historical fiction, science fiction, or healing/growth.
- **Spoiler boundaries**: identities, twists, endings, deaths, relationships, or clues that must remain undisclosed; write “none” if there are no restrictions.

The skill delivers three 120–220 Chinese-character blurbs—character/emotion, conflict/genre, and theme/atmosphere—plus an 18–36-character spoiler-safe selling line.

## Use

Invoke `$novel-blurb-variants-cn` and provide the three fields. If one is missing, the skill identifies the missing field instead of inventing story facts. [`fixtures/success.json`](fixtures/success.json) includes an `expected_output` contract for all three blurbs, the selling line, and spoiler boundaries. [`fixtures/failure-missing-type.json`](fixtures/failure-missing-type.json) includes the expected error for the isolated missing-genre case.

## Self-test

From this repository root:

```sh
sh scripts/self-test.sh
```

The test verifies packaging structure, metadata, PNG dimensions, and fixture contracts; it does not claim to generate real copy. Quality, factual fidelity, and spoiler handling still require reviewing model output against each fixture's expected conditions.

## Source and license

The limited public-use reference and attribution are in [sources/attribution.md](sources/attribution.md). This repository is released under the [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/novel-blurb-variants-cn
```

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the input fixtures.
