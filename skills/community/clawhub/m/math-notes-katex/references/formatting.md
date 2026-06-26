# Input note format (UTF-8)

Store the input as a UTF-8 `.md`-like text file.

## Inline math

- Wrap variables/indices/short formulas in `$...$`
  - example: `Let $x$, then $x' = 2x$`
- Subscripts/superscripts: also inside `$...$`
  - example: `$x_i$, $a_{n+1}$, $x^2$`
- Avoid lookalike characters (typography confusables):
  - write `$u$` (Latin u), not `ν` (Greek nu)

## Display math

- Use a separate block between lines containing `$$`

Example:

$$
J[x] = \int_0^1 (x')^2\,dt
$$

## Escaping

- To print a literal `$` in text: `\$`

## Style

- Markdown headings (`#`, `##`, …) are NOT parsed; `#` will appear as a literal character
  - Use `--title="..."` for the main title
  - Use plain text section headers: `1) ...`, `Velocity continuity`, etc.
- Keep paragraphs short
- Lists can be plain line breaks (Markdown bullets are optional)
