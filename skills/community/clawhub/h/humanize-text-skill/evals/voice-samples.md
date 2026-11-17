# Voice Samples

> This file covers the addition layer unique to `humanize-text-skill`. Given a text and a target voice, the engine should produce a reasonable drift score and actionable pull suggestions.

The subtraction-layer evaluation lives in [benchmark.md](./benchmark.md). This file focuses on `voice.drift` and `voice.suggestions`, which are the capabilities the parent projects explicitly stopped short of and `humanize-text-skill` adds.

## Evaluation dimensions

Each sample is judged on three axes:

1. **Drift realism**: does the drift score reflect the actual distance between the text and the target voice?
2. **Suggestion actionability**: are the suggestions concrete about where and how to revise, rather than generic?
3. **Fidelity safety**: do the voice-pull suggestions avoid protected spans such as numbers, commands, and terms?

---

## VS-01 | en | formal text → casual target

Original:

> Furthermore, it is worth noting that the aforementioned architectural decision necessitates a comprehensive reconsideration of the underlying infrastructure across multiple interconnected subsystems simultaneously.

Target voice: `casual`

Expected:

- drift `>= 40` because a long formal sentence is far from casual
- at least one split suggestion because sentence length `15+` is well above the target of `12`
- either a CV suggestion or a connector suggestion

---

## VS-02 | zh | formal long sentence -> casual target

Original:

> 值得注意的是，本次架构决策需要对底层基础设施进行全面重新考量。此外，实施策略要求在多个相互关联的子系统中保持细致的注意力。

Target voice: `casual`

Expected:

- drift `>= 40`
- the split suggestion should include a Chinese break position
- connector suggestions should use Chinese connectors such as `其实`, `不过`, or `反正`, not English ones

---

## VS-03 | en | clean low-AI text → blunt target

Original:

> I fixed the bug yesterday afternoon. The tests pass now. Will ship tomorrow morning.

Target voice: `blunt`

Expected:

- low `score` because the text already passes subtraction-layer cleanup
- nonzero drift as an independent dimension, since a blunt target may still want shorter and sharper phrasing

This case validates the **three-dimension contract**: `score`, `fidelity`, and `voice.drift` are independent.

---

## VS-04 | en | custom voice calibrated from sample

Author sample:

> Rolled back the auth thing. Cookie scope was wrong. Shipped it. Moving on.

Text to rewrite:

> The authentication refactor has been reverted due to complications, and we are currently investigating the root cause of the session invalidation issue that has been affecting a subset of our user base.

Target voice: `custom`, calibrated from the sample above

Expected:

- target fingerprint: short sentences (mean around 5 words), low CV, and first-person tendency
- high drift because the input is long, passive, and not first-person
- split suggestions should point at the longest sentences

---

## VS-05 | zh | technical status text -> should not be dragged by voice

Original (contains protected spans):

> 今天把连接池上限从 20 调到 100，504 先压下来了。后面再观察 24 小时，如果错误率还在 0.1% 以下就全量。

Target voice: `casual`

Expected:

- low `score` because technical status text should not be misread as AI-heavy
- drift may be `> 0`, but voice suggestions must not touch protected spans such as `20/100/504/24/0.1%`
- suggestions should focus on rhythm only, not numbers or commands

This case checks that the addition layer still respects the fidelity gate.
