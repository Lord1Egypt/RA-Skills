# Dialogue Subtext Rewrite for Fiction

Turn flat fiction dialogue into distinct character voices without changing supplied facts. Provide a dialogue excerpt, each character's immediate goal, and their relationship; receive a revised dialogue plus line-by-line subtext notes. Missing essentials are reported instead of invented.

![Promo](assets/promo-1600x900.png)

## Input and output

Use one chapter, scene, or short passage at a time (up to 100 table rows). Input needs speakers and lines, current goals, relationship, and non-negotiable facts or tone. Output includes revised dialogue, a surface-meaning/subtext/fact-preservation table, and a voice-difference check. Longer work should be split by scene.

```bash
npx skills add xxjrq/novel-dialogue-subtext-cn
```

See the [successful example](fixtures/success-example.md) and [missing-input example](fixtures/failure-missing-input.md). This is a Markdown-only skill: it does not use a browser, account, or automation.

## License and source note

The guidance and examples are original. The use case was checked against [story-skills / scene-craft](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/SKILL.md); no text or code was copied. Licensed under [MIT-0](LICENSE).
