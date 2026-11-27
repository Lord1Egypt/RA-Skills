---
name: mintrim
description: >-
  Restate only the last message in its original wording: cut filler, repetition,
  and empty talk, order kept points logically without polishing, and return the
  cleaned text.
disable-model-invocation: true
license: Apache-2.0
metadata:
  language: en
  translation_of: mintrim-cn
  version: "0.1.0"
---

Restate only the user's last message in its original wording: cut filler, repetition, and empty talk, put the kept points in logical order without polishing or adding anything, and return just the cleaned text.

## Check

- Keep every claim, name, number, and constraint; shorten by cutting words, never swapping in smoother phrasing.
- Leave earlier messages untouched; if the last message is already clean, return it unchanged.
- Reply with the restatement alone—no commentary, tone shifts, or added formatting.
