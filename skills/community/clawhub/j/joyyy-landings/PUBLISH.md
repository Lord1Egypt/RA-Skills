# Publish to ClawHub — checklist

So other agents (or their humans) actually install and use this.

## 0. Pre-publish verification (~10 min)

- [ ] Open https://vziatkov.github.io/neuro/landing-with-art-cards.html in incognito.
- [ ] **Core demos open, no 404:** Crash Engine, Dice Room, MMO Map, Crash Probability Explorer.
- [ ] All links from the landing work; pages load reasonably fast.
- [ ] Crash Probability Explorer runs (Start, charts, summary).

## 1. Before publish

- [ ] **Screenshots** — 3–5 PNG **1920×1080**: (1) Landing art cards, (2) Crash Engine, (3) Crash Probability Explorer, (4) MMO Map, (5) Dice Room. ClawHub reviewers prefer real UI, no placeholders. Save e.g. in `skills/joyyy-landings/screenshots/`.
- [ ] **Automated capture (optional):**
  ```bash
  cd skills/joyyy-landings
  pip install -r requirements-screenshots.txt
  playwright install chromium
  python3 capture_screenshots.py
  ```
  Then optionally build a 30s video from those screenshots:
  ```bash
  python3 make_demo_video.py
  ```
  Output: `screenshots/*.png` and `demo_30s.mp4`. Upload the video to YouTube/Vimeo and add URL to ClawHub.
- [ ] **Demo video** (optional but recommended) — **30–90 sec**, Loom / Screen Studio / OBS. Script: scroll landing → open Crash Engine → change RTP → open Probability Explorer. Or use `make_demo_video.py` output as draft.
- [ ] **Test** — All links open and load from incognito.

## 2. Account

- [ ] Sign up at https://clawhub.ai (or the URL from current OpenClaw docs).

## 3. Publish

From repo root:

```bash
clawhub publish ./skills/joyyy-landings \
  --slug joyyy-landings \
  --name "Interactive Prototypes — Human + AI" \
  --version 1.0.0 \
  --tags latest
```

If CLI uses a different path, point to the folder that contains `SKILL.md` and `clawhub.json`.

## 4. After publish

- [ ] Open the skill page on ClawHub. Add **demo URL** and **video URL** in the listing if the form has fields.
- [ ] Share the skill link: "Install: `/skills install @your-username/joyyy-landings`" or the one-line from the marketplace.

## 5. Distribution (skill alone won’t be found)

- [ ] **LinkedIn** — Post: "I built something unusual. Not a CV. A skill AI agents can call. Interactive prototypes: crash engines, probability simulators, procedural worlds, visual analytics. One link. Human + AI built." + link to landing.
- [ ] **GitHub** — README has an "AI-callable portfolio" block with link to landing and skill path.
- [ ] **HN / Twitter / AI communities** — "Show HN: AI-callable portfolio with interactive simulations" + landing link.

## 6. Next-level demo (optional)

Crash Probability Explorer can be turned into an **iGaming analytics tool**: house edge slider, bankroll sim, strategy comparison, histogram distribution — then the skill sells not just "portfolio" but "interactive systems engineer".

---

## Why agents will care

- **Clear outcome:** "One link for investors" — no guessing what they get.
- **No keys, no config:** Links only. Low friction.
- **Tags:** portfolio, human-ai, investor, games, analytics — discoverable.
- **Copy speaks to agents:** "Use when you need to show what we ship" — direct trigger for when to invoke the skill.

**One-line agent summary:** Returns landing URL for interactive prototypes (game engines, simulations, investor demos). Invoke on portfolio / demo / investor / "what do you offer" requests.
