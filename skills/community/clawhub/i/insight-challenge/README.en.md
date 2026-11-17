# insight-challenge

A skill for **adversarial verification** of findings from code reviews, static analysis, or security scans: independently check whether each finding actually holds, and produce one of three verdicts — overturned / weakened / confirmed — so that no one wastes effort fixing phantom issues.

## Directory Layout

```
insight-challenge/
├── SKILL.md                       # Chinese main doc (entry point: input format,
│                                    # four-phase flow, output template, error codes)
├── SKILL.en.md                    # English main doc
├── README.md                      # Chinese navigation & usage
├── README.en.md                   # This file
├── specs/
│   ├── challenge-protocol.md      # Challenge protocol: five strategies & decision tree
│   ├── challenge-protocol.en.md
│   ├── verdict-schema.md          # Verdict schema: fields & value constraints
│   └── verdict-schema.en.md
├── scripts/
│   └── validate-verdict.mjs       # Zero-dependency verdict validator (fail-closed)
└── tests/fixtures/
    ├── verdict-good.json          # Known-good fixture (must PASSED)
    └── verdict-bad.json            # Known-bad fixture (must be rejected with codes)
```

Note: the source repo also contains `LICENSE` (stripped by the publish packaging; repo only).

## Dependencies

Node.js ≥ 18 only; the validator has zero third-party dependencies — nothing to install.

## Running the Validator

Three input modes:

```bash
# 1. Validate a JSON file (single verdict, batch verdicts object, or top-level array)
node scripts/validate-verdict.mjs verdict.json

# 2. Read from stdin
cat verdict.json | node scripts/validate-verdict.mjs -

# 3. Validate a markdown report (extracts embedded ```json verdict blocks)
node scripts/validate-verdict.mjs report.md
```

Failures report error codes (IC-V00..V13) pinpointing each problem; unmet evidence expectations emit IC-W01..W03 warnings (they do not change the exit code); exit 0 means pass.

## Running the Tests

```bash
node scripts/validate-verdict.mjs tests/fixtures/verdict-good.json   # expect: PASSED
node scripts/validate-verdict.mjs tests/fixtures/verdict-bad.json    # expect: exit 1 with error codes IC-V01-V06, V09, and V11-V13
```

The repo-root `.github/workflows/ci.yml` (not part of this skill's distributed package) runs both assertions plus stdin/markdown mode gates on every push.

## Documentation Guide

| Want to know | Read |
|--------------|------|
| How to invoke the skill, inputs and outputs | SKILL.en.md |
| Five challenge strategies and the decision tree | specs/challenge-protocol.en.md |
| Verdict fields and validation rules | specs/verdict-schema.en.md |
| Validator usage | This file + `node scripts/validate-verdict.mjs` (no args prints Usage) |
