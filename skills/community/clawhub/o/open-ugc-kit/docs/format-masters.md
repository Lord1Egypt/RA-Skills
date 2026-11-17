# Format master prompts

Use these when the 100 openings are not the right room, person, or hook. Paste a master into a text model with your brackets. It returns one still prompt in the same style as `prompts/`.

Give the model:

- `[PRODUCT]`, `[PACKAGING]`, `[CREATOR]`
- Audience (who this is for)
- One benefit you can stand behind
- Optional: city, season, price point, one objection

Ask for **one** still prompt, 9:16, ready to paste into an image model. Then animate in Seedance 2.5 with the matching master in [animation-masters.md](animation-masters.md).

Still rules for Seedance I2V: leave space around hands and product (they need room to move). Do not crop a hero packshot. Do not add on-screen text. Prefer a moment *before* the product is fully revealed.

---

## 1. Unboxing master

```
Write one photoreal UGC still prompt (9:16, phone camera) of [CREATOR] at the exact moment they start opening [PACKAGING] to get to [PRODUCT].

The still is the hook: hands on the package, product not fully revealed yet, or just peeking.

Rules:
- Real apartment or real car, not a studio. Show one messy human detail (mail pile, coffee, laundry).
- Window light or overhead indoor light. No rim light, no beauty dish.
- Product and packaging must match the descriptions exactly. No invented logos.
- Camera is a phone, slightly above the package or at chest height. Handheld feel.
- Expression is unposed: concentrating, slightly excited, or mid-talk.
- No on-screen text, watermark, or caption.
- End the prompt with: real skin texture, visible pores, slight noise, no beauty filter, no extra fingers.

Also output a 6-word [HOOK_LINE] they might be saying, separately, so I can caption later.
```

---

## 2. Street interview master

```
Write one photoreal UGC still prompt (9:16, phone camera) of a sidewalk interview about [PRODUCT].

Two people: a holder (we see a hand or shoulder of the interviewer) and [CREATOR] as the interviewee, mid-reaction, holding or looking at [PRODUCT].

Rules:
- Real street, campus, mall corridor, or park path. Include a background that is busy but readable (bikes, storefront, other pedestrians out of focus).
- Daylight, overcast or sun with a hard shadow. Not golden-hour cinema.
- Interviewee is not a model pose. Weight on one leg, maybe a tote bag, maybe AirPods in one ear.
- Product is in someone's hands, label readable if the real label is simple, otherwise three-quarter angle.
- Shot from the interviewer's phone, arm's length, slight wide-angle distortion.
- No lavalier packs, no film crew, no clapper, no on-screen text.
- End with: candid documentary still, real skin, no beauty filter.

Also output the interviewer's question (under 10 words) and a 5–8 word reply for later captions.
```

---

## 3. Face-cam review master

```
Write one photoreal UGC still prompt (9:16, front camera) of [CREATOR] talking to the phone about [PRODUCT].

This is a story-time / review opening, not a studio talking head.

Rules:
- Front camera, held in one hand or propped. The other hand holds [PRODUCT] or has just set it down in frame.
- Location is a bathroom, bedroom, parked car, or kitchen — somewhere people actually film.
- Catch them mid-sentence. Mouth slightly open is fine. Eyes at the lens.
- Lighting is the room they are in (mirror lights, car window, desk lamp). Uneven is good.
- Skin is real. Flyaways, under-eye texture, no smooth filter.
- Background is a real room, slightly messy.
- No ring light visible unless it would honestly be there. No on-screen text.
- End with: iPhone selfie still, natural color, slight grain.

Also output a [HOOK_LINE] under 8 words for later captions.
```

---

## 4. Q&A / who sells more master

```
Write one photoreal UGC still prompt (9:16, phone camera) for a "who would you buy from" or "who sells more" beat about [PRODUCT].

Two people in one frame, or one person holding the phone toward a second person. They have just been asked a question. The still is the reaction, not the question.

Rules:
- Casual indoor or sidewalk. Friends, not hosts.
- [PRODUCT] is visible — in a hand, on a table between them, or being passed.
- Body language disagrees a little (one leaning in, one squinting at the label). That tension is the hook.
- Phone camera, slightly wide, both faces readable.
- Real clothes, real hair, no matching outfits unless they would match in life.
- No lower-thirds, no vs graphic, no on-screen text. We will caption later.
- End with: candid UGC photo, real skin, no beauty filter.

Also output the question (under 12 words) and two short opposing replies for later captions.
```
