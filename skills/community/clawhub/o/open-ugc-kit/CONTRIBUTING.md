# Contributing

This kit stays useful if new scenes are specific and new masters stay short.

## Add an opening scene

1. Pick a format file in `prompts/`.
2. Use the next free ID (`U-26`, `S-26`, `F-26`, `Q-26`).
3. Follow the existing block: **title**, **hook line**, **still prompt**, **Seedance 2.5 prompt**.
4. The still must be one shot a phone could take. No multi-scene paragraphs.
5. The Seedance prompt follows `docs/seedance-2.5.md`: shot first, continuity, `[0-2s][2-6s][6-8s]`, `Audio:`, `No BGM`, `No subtitles`, 8s, 720×1280.
6. Keep product identity in brackets. Do not lock a scene to one brand.

Prefer editing `scripts/build_openings.py` and running `python3 scripts/build_openings.py` over hand-editing `prompts/*.md`.

## Add a master or workflow

Masters live in `docs/`. Workflows live in `workflows/`. Keep them copy-pasteable. Explain the order of operations, not the theory.

## Do not

- Paste prompts from paid packs
- Add on-screen text, logos, or watermark instructions
- Add cinematic language that fights UGC (anamorphic, drone, color grade, "cinematic lighting")
- Re-describe the still inside a Seedance I2V prompt
- Commit generated images or videos

## License

Contributions are accepted under CC BY 4.0.
