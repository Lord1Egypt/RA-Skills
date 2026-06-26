# Module: Fixed Artifacts And Reusable Reader

Use this module for output stability and web reuse.

## Fixed Files

Every complete analysis must contain:

```text
analysis_bundle.json
paper_reading_report.md
paper_questions_for_code.md
paper_code_crosswalk.md
experiment_joint_reading.md
implementation_omissions.md
diagrams.md
modify_method_guide.md
validation_report.md
site/index.html
```

The web reader is a view over these artifacts. It is not the source of truth.

## Reader Rule

Do not rewrite `site/index.html`, `site/assets/app.js`, or `site/assets/styles.css` for one paper. If the page cannot display a generally useful field, update the reusable template in `assets/reader-template/`, rebuild, and validate.

Build with:

```bash
python scripts/build_static_reader.py <analysis_dir> --force
```

For final visual delivery when network access is available, install KaTeX fonts into the generated output:

```bash
python scripts/build_static_reader.py <analysis_dir> --force --install-katex-fonts
```

Do not bundle KaTeX `.ttf`, `.woff`, or `.woff2` files inside the skill package. ClawHub accepts text-only skill files; font binaries belong only in generated `site/vendor/katex/fonts/` outputs created at use time.

## Formula Rule

Formulas may be stored as fenced `math` blocks in Markdown or as `formula.math` in JSON, but the reader must render them with KaTeX. Normal visible page content must not show raw formula source such as `\frac`, `\lambda`, `\mathcal`, or `\tilde` when rendering succeeds.

## Validation

Run:

```bash
python scripts/validate_bundle.py <analysis_dir>/analysis_bundle.json
python scripts/check_outputs.py <analysis_dir>
python scripts/build_static_reader.py <analysis_dir> --force --install-katex-fonts
python scripts/check_reader.py <analysis_dir>
```

If validation fails, fix artifacts or the reusable template and rerun checks.
