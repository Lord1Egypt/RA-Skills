# Extending to new languages (beyond CN/EN)

Goal: add language support without breaking quality.

## 1) Add language_id + native conventions
For each new language L:
- language_id: e.g., es, fr, ja
- politeness system (tu/vous, keigo, honorifics)
- typical sentence rhythm and paragraphing
- common “AI tells” in that language (often translationese)

## 2) Add per-scenario micro-templates
For each scenario S1–S9, add:
- 2–3 short templates in L
- 10–20 phrase bank entries (greetings, asks, softeners)

## 3) Build a small few-shot pack
- 10–30 human samples per scenario (start with S1, S3, S2)
- 3–8 few-shot pairs per scenario

## 4) Add evaluation
- native speaker review, or
- blinded A/B preference test

## 5) Avoid translationese
If user provides English facts but wants Japanese output, do not translate literally. Re-express in native patterns for that scenario.

