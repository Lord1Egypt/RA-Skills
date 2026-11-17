# Project memory file design

Use five small files with non-overlapping responsibilities:

| File | Source of truth |
| --- | --- |
| `docs/README.md` | Documentation map and maintenance rules |
| `docs/PROJECT.md` | Current product, architecture, modules, interfaces, data, and limits |
| `docs/DEVELOPMENT.md` | Repeatable setup, test, build, deploy, and delivery commands |
| `docs/PROGRESS.md` | Append-only dated history and verification evidence |
| `docs/DECISIONS.md` | Durable choices, alternatives, and reasons |

Initialization procedure:

1. Inspect the repository tree, manifests, routes, migrations, tests, CI, and deployment files.
2. Write only supported facts. Use `unknown`, `not yet verified`, or `requires environment` instead of inventing details.
3. Avoid copying the same paragraph into several files; link to the authoritative file.
4. Preserve existing documents and migrate only when the user explicitly requests restructuring.
5. Add a first progress entry describing initialization and anything not verified.
