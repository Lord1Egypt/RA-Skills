# meta-prompt-architect-lite

Turn a plain-language task description into a minimal prompt template — extracts `{{variables}}`, detects output format, assembles a ROLE/TASK/INPUT/CONSTRAINTS/OUTPUT scaffold. Offline, zero deps, Node 18+.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill meta-prompt-architect-lite
```

## Run

```bash
node scripts/generate.mjs task.txt
echo "Summarize each meeting transcript into markdown for managers" | node scripts/generate.mjs -
```

## Full version

The paid version detects tone/audience, adds edge-case and injection rules, and emits test-case stubs:

- SkillHQ: https://skillhq.dev/skills/sone94/meta-prompt-architect
- Agensi: https://agensi.io/skills/meta-prompt-architect
