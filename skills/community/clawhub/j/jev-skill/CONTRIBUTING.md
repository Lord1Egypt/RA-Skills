# Contributing

Thanks for helping make typed model decisions more reliable.

## Before opening a pull request

Run the dependency-free checks:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/jev_harness.py
python3 /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Keep changes provider-neutral when possible. Do not add API keys, customer
state, private golden sets, or generated reports. New provider behavior should
include a local fake-server test and should preserve strict response
validation, bounded retries, and privacy-safe reporting.

For evaluation changes, document which metric or failure slice changed and
include representative, adversarial, boundary, or metamorphic cases when
appropriate. Confidence and consensus are signals for review, not proof of
correctness.
