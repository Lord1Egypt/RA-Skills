# Character Knowledge-State Ledger

Track who knows each story fact, when they first learned it, and where they use it too early. Supply scenes in story order, fact IDs, and non-empty quoted evidence of a character experiencing, being told, inferring, or using a fact. The result is a character-by-fact matrix with first-known scene, certain/guess/unknown state, and early-use findings. Inference alone means guess; no character evidence means unknown. Missing scene order or all evidence triggers a request for more material. Reader knowledge is never treated as character knowledge.

```bash
npx skills add xxjrq/novel-knowledge-state-ledger-cn
node scripts/self-test.mjs
```

The skill covers up to 10 characters, 30 facts, and 20 scenes. It tracks information propagation only; it does not critique narrative viewpoint or plan foreshadowing. Missing scene order or evidence triggers a request for the missing material; unsupported facts remain `unknown`.

See the copyable [success input](fixtures/success-input.json), [success output](fixtures/success-output.json), and [missing-material response](fixtures/failure-output.md). The self-test executes both the valid ledger and an invalid, incomplete input.

Source use was limited to checking the purpose of [story-skills revision continuity](https://github.com/danjdewhurst/story-skills/blob/main/skills/revision-continuity/SKILL.md); all repository prose, process, and examples are original. Licensed under [MIT-0](LICENSE).
