---
name: litmus
description: >-
  Check whether an eval suite can fail. Use when someone asks if their plugin
  or skill evals are any good, wants a mutation score for a `claude plugin eval`
  suite, suspects a grader always passes, or wants to know which parts of a
  skill their evals do not cover.
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/litmus
    requires:
      bins: [python3]
---

# litmus

litmus mutation-tests eval suites. It breaks the skill on purpose and checks
that the evals go red. It runs through the `litmus` command (on PATH inside
Claude Code when this plugin is enabled, or `python3 -m litmus.cli`).

Start with the free checks. They never call a model:

1. `litmus vacuity <plugin-dir>`: graders that provably cannot fail, and cases
   a do-nothing run would pass.
2. `litmus audit <plugin-dir>/evals/results/*/aggregate-result.json`: cases
   that stayed green with the plugin removed, from runs the user already has.
3. `litmus mutate <plugin-dir> --dry-run`: the mutants and the cost estimate.

Only run `litmus mutate ... --yes` when the user asked for a real run and
accepted the estimate. It runs `claude plugin eval` once per mutant on their
credential. Pass the same `--allow-tools` the suite needs, and a
`--max-cost-usd` ceiling.

When you report:

- Give the mutation score with killed, survived and inconclusive counts.
  INCONCLUSIVE is never a kill; say why each one was inconclusive.
- List every surviving mutant with its description: each is a part of the
  skill no eval checks. Some survivors are equivalent mutants (the line did
  not matter); say so when it is plausible, do not hide them.
- List VACUOUS graders and NULL_GREEN cases first; they are certain.
- Suggest the smallest grader change that would kill a survivor, for example
  a regex on the final message for the rule the mutant removed.

Exit codes: 0 pass, 1 the suite failed the bar (vacuous grader, null-green
case, or score below `--min-score`), 2 litmus could not evaluate. On 2, show
the `litmus: error:` line and fix the cause.
