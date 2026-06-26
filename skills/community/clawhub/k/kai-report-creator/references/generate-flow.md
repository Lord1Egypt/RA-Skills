# Generate Flow

Steps for `--generate` mode:

1. Read IR input only. With no file given, extract exactly one valid IR block from context. Treat this as IR from context, not chat history. If zero or multiple are present, stop and ask for an explicit file or single IR block. Never render the surrounding conversation.
2. Load reference files minimally but reliably; load only the references that materially help the current render path. Standard HTML shell generation always loads the shell entry plus all `references/html-shell/*.md`; component rules load by IR inventory via `references/rendering-rules.md`.
3. Parse frontmatter and resolve `lang`, `theme`, `report_class: mixed` default, `archetype`, date display, chart mode, TOC, animation, template, and theme overrides.
4. Run guard validation before rendering:
   - Use `scripts/guard_validate.py` with IR text from file or extracted context.
   - If fatal metadata is missing, stop and report the error.
   - If a block is invalid, apply its `auto_downgrade_target` (`kpi -> callout`, `chart -> table`, `timeline -> list`, `diagram -> callout`) and mention the downgrade.
5. Render components using `references/rendering-rules.md`, `references/design-quality.md`, and the path-specific `references/rendering/*.md` files selected from the IR.
6. Build the standard shell from `references/html-shell-template.md` plus all `references/html-shell/*.md`; follow Shell metadata, version/theme metadata, export completeness, and the duplicate-date guard.
7. Compute and embed `<meta name="ir-hash" content="sha256:[ir-hash]">` from the exact IR text, not the file path.
8. Assemble CSS through `references/theme-css.md`: theme before-marker, shared CSS, theme post-shared override, TOC/shell CSS, frontmatter overrides.
Steps 9-12 (quality gates) are defined in SKILL.md and always run after these setup steps.
