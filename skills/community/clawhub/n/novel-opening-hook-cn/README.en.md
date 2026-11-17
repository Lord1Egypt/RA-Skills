# Chinese Novel Opening Hook Rewrite

![Chinese novel opening hook rewrite](assets/promo-1600x900.png)

Rewrite a Chinese novel opening into fast-paced, suspense-led, and immersive versions while preserving characters and core events. Each version includes edit rationales tied to the original text, followed by one recommendation. Use it with a skill-capable assistant; no browser or additional API key is required.

## Quick start

Provide the opening plus non-negotiable facts. The skill returns fast-paced, suspense-led, and immersive versions; each has searchable edit rationales, followed by one recommended version. See [fixtures/success-input.json](fixtures/success-input.json). Missing opening text is rejected as shown in [fixtures/failure-input.json](fixtures/failure-input.json).

```bash
node scripts/self-test.mjs
```

It rewrites only the supplied opening. It does not write a whole novel, create an outline, or run a six-dimension review. Licensed under [MIT-0](LICENSE).

## License

Original editing instructions and examples, licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/novel-opening-hook-cn
```

Alternatively, copy this repository folder into your Agent’s skill directory, then invoke `$novel-opening-hook-cn` with your input.
