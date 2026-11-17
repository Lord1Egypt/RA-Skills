# Contributing

Thank you for improving Advanced Human Writing & AI Humanizer.

## Rules And Tests

- Add a deterministic rule only when it has a concrete, user-visible editing purpose.
- Give every rule a stable ID, category, severity, repair direction, allow-list behavior,
  positive fixture, and a plausible negative fixture.
- Do not describe a pattern score as proof of AI authorship. Rules identify editing leads.
- Gate genre-specific rules so fiction, news, academic, legal, and technical writing do
  not inherit one another's constraints.
- Preserve token budgets: optional or specialized modules must not silently enter quick
  generation or unrelated document types.

Run the full suite before opening a pull request:

```powershell
python -m unittest discover -s tests -v
python -m build
```

## Documentation

Update the English and Chinese README material for user-facing commands. Keep examples
generic and evidence-led; do not publish private manuscript material in fixtures or issues.

## Pre-commit

Teams can install the repository hook with:

```powershell
pre-commit install --hook-type pre-commit
```

The hook checks Markdown-like text and fails only once the transparent pattern score
reaches its configured threshold. Use allow-lists for intentional motifs or house style.
