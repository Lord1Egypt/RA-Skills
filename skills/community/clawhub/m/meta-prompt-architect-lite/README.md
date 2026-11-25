# meta-prompt-architect-lite

Turn a plain-language task description into a minimal prompt template — extracts `{{variables}}`, detects output format, assembles a ROLE/TASK/INPUT/CONSTRAINTS/OUTPUT scaffold. Offline, zero deps, Node 18+.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill meta-prompt-architect-lite
```

## Run

```bash
node scripts/generate.js task.txt
echo "Summarize each meeting transcript into markdown for managers" | node scripts/generate.js -
```

## Full version

The full `meta-prompt-architect` skill ($9) detects tone/audience, adds edge-case and injection rules, and emits test-case stubs. Ask for it by slug.
