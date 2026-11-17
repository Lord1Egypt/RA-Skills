# Setup and compatibility

Run helpers from the installed skill directory, replacing `<project-root>` with the intended project. Inspect existing documents before choosing a profile. A detector result describes conventional files, not the quality or completeness of the project's governance.

```sh
python scripts/detect_governance_state.py --root <project-root> --format json
python scripts/bootstrap_project.py --root <project-root> --profile lightweight --dry-run --format json
python scripts/adapt_governance.py --root <project-root> --profile lightweight --dry-run --format json
```

Use `bootstrap_project.py` for requested new scaffolding and `adapt_governance.py` when preserving and mapping existing structures. Remove `--dry-run` to perform the authorized setup. Both preserve existing files. `--project-name` controls the template title. Existing projects may need a targeted manual addition instead of any profile.

The default changed from `layered` to `lightweight` in 1.1.0. Pass `--profile layered` to retain the previous structure. `memory-only` does not create AGENTS.md, README.md, or code.md. The adapter adds a compatibility map and initialization marker only if absent; it does not rewrite an existing marker or migrate existing content. Review reported conflicts and maintain necessary links in the project's existing navigation as part of the requested adaptation.

Templates use `{{PROJECT_NAME}}`, `{{DATE}}`, and `{{DATE_COMPACT}}` placeholders. Generated draft sections need project-specific facts; they are not evidence that setup, validation, or memory import has happened. Keep existing conventions instead of imposing the example filenames on unrelated projects.

Template source directories use `_learnings` so registries that exclude hidden paths include them. Both setup helpers render that directory as `.learnings` in the target project; existing project paths are unchanged.
