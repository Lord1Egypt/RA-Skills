---
name: happy
description: Pick 2-3 random happy moment stories from the HappyDB dataset and retell them as short stand-up comedy bits. Use this skill whenever the user wants to hear funny stories, needs a laugh, wants random happy moments from the dataset, or asks for comedy content from the happy moments CSV. Trigger on phrases like "tell me happy stories", "make me laugh", "pick some stories", "random happy moments", "cheer me up", or anything requesting funny/happy content from the data.
---

# Happy Comedy Skill

Your job: pick 2–3 random rows from the HappyDB CSV and retell each one as a punchy stand-up comedy bit.

## Data source

The CSV lives at `./original_hm.csv` (columns: `hmid`, `hm`, `reflection`, `wid`).

## Step-by-step

1. **Sample randomly** — use bash/Python to grab 2–3 random rows from the CSV (use a random seed based on current time so results differ each run):

```bash
python3 -c "
import csv, random, time
random.seed(int(time.time()))
with open('original_hm.csv') as f:
    rows = [r for r in csv.DictReader(f) if len(r.get('hm','').strip()) > 20]
picks = random.sample(rows, 3)
for p in picks:
    print('---')
    print(p['hm'].strip())
"
```

2. **Write the comedy bits** — for each story, write a 3–5 sentence stand-up style retelling. Rules:
   - Keep the core truth of the original moment intact
   - Add comic timing: setup → twist → punchline
   - Use self-aware, observational humour (think everyday absurdity)
   - Keep each bit SHORT — punchy, not padded
   - Never mock the person; punch at the situation, not the human

3. **Format your response** like this:

---
🎤 **Story 1** *(original: "[short quote from the hm]")*

[Comedy bit here — 3-5 sentences]

---
🎤 **Story 2** *(original: "[short quote]")*

[Comedy bit here]

---
🎤 **Story 3** *(optional — include if the third story is gold)*

[Comedy bit here]

---

## Tone guide

- Warm, not mean
- Self-deprecating where possible
- Celebrate the mundane joy — that IS the joke
- Avoid forced puns; prefer observational wit
- End each bit on the laugh, not an explanation

## Example

Original: *"I went to the gym this morning and did yoga."*

> So I went to the gym this morning and did yoga. That's it. That's the whole win. Not a marathon. Not a triathlon. I bent forward, remembered I have knees, and called it personal growth. And honestly? Best day of the month.
