# Core File Rules

Use these rules when deciding whether a file should appear in Obsidian graph support notes.

## Core files

Include:

- Business materials: `.md`, `.docx`, `.doc`, `.pptx`, `.ppt`, `.xlsx`, `.xls`, `.pdf`, `.txt`, `.csv`, `.json`, `.yaml`, `.yml`.
- Code project core files: README files, manifests, requirements, project configs, source files, tests, scripts, templates, command/rule files, and agent/config files.
- Existing Markdown notes that are already meaningful user-authored material.

## Non-core files

Exclude:

- Dependency directories: `node_modules`, `.venv`, `venv`, `env`.
- Tool/cache directories: `.git`, `.obsidian`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `__pycache__`, `.cache`.
- Build/runtime output: `dist`, `build`, `.next`, `.nuxt`, logs, temporary files.
- Model or training output: `models`, `autogluon_result`, `ag_exp_*`, pickle/model binaries.
- Static vendor/resource bundles that are not authored knowledge material.
- Temporary Office lock files beginning with `~$`.

## Discovery defaults

By default, the script discovers:

- Business roots: top-level, non-excluded directories that contain business-material extensions such as Word, PowerPoint, Excel, PDF, TXT, or CSV.
- Project roots: non-excluded directories up to three levels below the vault root containing `pyproject.toml`, `package.json`, `requirements.txt`, `project.config.json`, `manifest.json`, `AGENTS.md`, `README.md`, or `config.yaml`.
- Root-level Markdown files within two path segments are treated as workspace notes.

Override discovery with `--business-root` or `--project-root` on `scan` and `refresh` when the default is wrong.
