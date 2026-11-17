# The Open UGC Kit

A free, open prompt system for turning any product into a realistic AI UGC video. Written for **Seedance 2.5**.

Still first. Then an 8-second image-to-video clip. Same path every time.

Run the clip on **[ezugc.ai](https://ezugc.ai)** — Seedance 2.5, 9:16, no extra setup.

**License:** [CC BY 4.0](LICENSE) — use it, remix it, sell client work with it. Credit the kit.

---

## Prompt count

**209 copy-paste prompts**

| Count | What |
|---:|---|
| 100 | First-frame stills (25 × 4 formats) |
| 100 | Matching Seedance 2.5 I2V prompts (one per still) |
| 4 | Format masters (invent a new still in a format) |
| 4 | Seedance 2.5 animation masters |
| 1 | Clone-any-viral-ad master ([Ad Spy](https://app.ezugc.ai/dashboard/ad-spy)) |

Plus 4 start-to-finish workflows and 100 hook lines for captions (not generation prompts).

---

## What you get

| # | Piece | What it does |
|---|---|---|
| 01 | [Seedance 2.5](docs/seedance-2.5.md) | Settings, five-layer brief, I2V vs T2V |
| 02 | [Clone any viral ad](docs/clone-viral-scene.md) | Pull a winner from [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy). Remake it with your product. |
| 03 | [100 openings](prompts/) | Still + Seedance 2.5 prompt across unboxing, street interview, face-cam, Q&A |
| 04 | [4 format masters](docs/format-masters.md) | Unlimited new stills in those four formats |
| 05 | [4 animation masters](docs/animation-masters.md) | Seedance 2.5 I2V for each format |
| 06 | [4 workflows](workflows/) | Unboxing, street interview, Q&A, and clone from Ad Spy |
| 07 | [How to use](docs/how-to-use.md) | Blank screen to finished clip |

Optimized for Seedance 2.5 (`bytedance:seedance@2.5`): 8s, 720×1280 (9:16), native audio, first frame = still. Stills still work as first frames for other I2V models if you need them.

---

## The four formats

**Unboxing** — package lands, hands go in, product comes out.

**Street interview** — a stranger reacts on the sidewalk.

**Face-cam review** — talking to the front camera.

**Q&A / who sells more** — two people, one question, comments.

---

## Quick start

1. Read [How to use](docs/how-to-use.md) and [Seedance 2.5](docs/seedance-2.5.md) once.
2. Fill the [brackets](docs/how-to-use.md#brackets).
3. Pick an opening from [`prompts/`](prompts/) **or** run a [format master](docs/format-masters.md).
4. Generate the still at 9:16.
5. Run Seedance 2.5 I2V on [ezugc.ai](https://ezugc.ai) with that scene's Seedance prompt (or the matching [animation master](docs/animation-masters.md)): **8s · 720×1280 · audio on · first frame = still**.

To remake a live winner, open [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy) and follow [clone any viral ad](docs/clone-viral-scene.md).

---

## Who this is for

- Creators making UGC for brands
- Operators who need ads without a shoot
- Anyone whose AI video still looks like AI

---

## Design rules

- Phone camera, 9:16, handheld micro-shake
- Real skin, real rooms, real light — no beauty filter, no studio grade
- Product is physically in the frame
- No on-screen text (caption later)
- Brackets for `[PRODUCT]`, `[PACKAGING]`, `[CREATOR]`
- Seedance motion prompts: shot first, then continuity, timed action, light, `Audio:` — do not re-describe the still

---

## Agent skill

```bash
npx skills add team-listnr/open-ugc-kit
```

The agent fills brackets, picks a format, and emits a still prompt plus a Seedance 2.5 I2V prompt. To clone a live ad, it uses [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy). Generate the video on [ezugc.ai](https://ezugc.ai).

There was no Seedance 2.5 UGC format skill on [skills.sh](https://skills.sh) (existing hits are API routers or generic UGC marketing). This repo is that skill.

---

## FAQ

**Do I need to edit?** No. Generate a still, run Seedance 2.5, caption in-app.

**What tools?** A photoreal image model + Seedance 2.5. The intended path is [ezugc.ai](https://ezugc.ai). Other I2V models can take the stills; motion prompts are Seedance-shaped.

**Will this work for my product?** If it can sit in a hand, a box, or a sink, yes. Services and software still work in face-cam and Q&A.

**Is this a subscription?** No. Clone it. It is CC BY 4.0.

**How fast?** One still + one 8s clip. About 10 minutes the first time.

**Does it only work with Seedance 2.5?** Motion prompts are written for Seedance 2.5. The stills are model-agnostic first frames.

**Can I clone a live ad?** Yes. Open [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy), screenshot the opening, then use [clone any viral ad](docs/clone-viral-scene.md).

**Is there a video walkthrough?** Not yet. [How to use](docs/how-to-use.md) is the walkthrough.

## Contributing

New scenes, tighter masters, and real before/after examples are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

From [EzUGC](https://ezugc.ai). Original prompts. Not a paid prompt pack.
