# Personal Content DNA

An agent skill for turning real exploration, decisions and editorial feedback into a traceable personal content library, then practicing writing methods grounded in those materials.

## What it does

- Captures user choices, rejections, changed views, experiments and concrete aesthetic edits from explicitly scoped conversations and project records.
- Distinguishes user input, AI proposals, user decisions, AI execution and observed results.
- Maintains Markdown material cards, expression rules and a CSV index.
- Matches approved materials and reference methods to a writing brief.
- Records actual selection and revision feedback so trial methods can gradually become adopted practices, separately by genre.

The skill runs inside active agent sessions. It does not install background monitoring, scheduled capture, a dashboard, or automatic access to other conversations.

## Install

Clone this repository into your agent's skills directory under `personal-content-dna`. For Codex:

```bash
git clone https://github.com/0xcjl/personal-content-dna.git ~/.codex/skills/personal-content-dna
```

Use an empty destination. The core `SKILL.md`, `references/` and `assets/` are portable to compatible agents. `agents/openai.yaml` is optional Codex discovery metadata.

From ClawHub, after the registry release is available:

```bash
clawhub install @0xcjl/personal-content-dna
```

## Use

Capture after an exploration session:

> Use personal-content-dna to capture new decisions, rejection reasons, changed views and experiment results from this visible conversation and the files I specify. Save candidate cards in this project's personal library, merge the same event, and show the IDs, source scope and missing evidence.

Prepare writing inputs:

> Match approved, publicly allowed materials to this verified topic. Select a reference method, explain its fit, and put usable claims and attribution in the brief. Follow this project's post and article formats.

Save feedback:

> I selected version B because its comparison makes the tradeoff clearer. Save that reason and the concrete changes against the draft version. Keep the method as a trial unless I explicitly adopt it.

For cross-project capture, specify the source scope and one shared library destination. A public-use permission does not authorize publication or social account operations.

## Library and states

Library location: user-specified path, then project rules, then `reference/personal-dna/` in the current project. Store actual needed cards in `cards/`, methods in `style/`, and keep `index.csv` synchronized.

Material states: `candidate`, `approved`, `needs_review`, `historical`. Method states: `trial`, `adopted`, `retired`. Public-use states: `pending`, `allowed`, `restricted`.

Only `approved + allowed` personal materials enter routine writing. A public expression method may be practiced as `trial + allowed`. Preserve confirmation records and reuse existing authorization within its scope.

## Daily practice

At a work milestone or wrap-up, capture meaningful new events. After editing, save actual feedback. In a requested weekly review, reconcile duplicate events, changed views, useful gaps and method history. Do not invent cards to fill a daily quota or infer reasons from an unexplained selection.

## Pair with X Writing DNA

[x-writing-dna](https://github.com/0xcjl/x-writing-dna) can supply reference-author methods, separate genre profiles, supporting works and limitations. It is optional: supplied reference material or the user's own practice goal can also guide training. Preserve attribution rather than transferring another author's life facts to the user.

## Limits and privacy

Do not fabricate first-person experience, independent authorship, psychological motives, earnings or results. Generated drafts, repository ownership, publication and engagement cannot prove personal experience. Private/internal text and credentials stay out of ordinary candidate cards and Writer inputs. No personal library or third-party corpus is bundled in this repository.

## Attribution and license

The material-library concept was informed by [Nicolas Cole's The Right Way To Write With AI](https://artandbiz.substack.com/p/the-right-way-to-write-with-ai). This skill adds provenance, contribution boundaries, public-use scope, explicit states and feedback rules; it does not include the article text. This ClawHub edition uses MIT-0; the GitHub root edition uses MIT. See [LICENSE](LICENSE).
