# Component Rendering Rules

Entry point for IR component rendering in late-context-safe generation. Keep this file small: load it first to parse directives and choose the exact child references needed for the current IR.

## CRITICAL: IR Directive Parsing — Never Let `:::` Leak Into Output

**Before emitting any HTML, do a mental pass to ensure zero `:::` sequences appear in the final output.** Any `:::` in the output means an IR directive was not converted — this is a bug.

### Block Detection Rules

A `:::` directive block has this structure:

    :::tag [param=value ...]
    [content — can be multiple lines, YAML, or a Markdown list]
    :::

**The closing `:::` is ALWAYS on its own line.** Parse the IR line by line:
1. When you see a line starting with `:::tag`, begin collecting the block body.
2. Collect all lines until you hit a line that is exactly `:::` (the closing marker).
3. Convert the entire block (opening tag + body + closing `:::`) to HTML per the child reference for that tag.
4. Never output the `:::tag`, params, closing `:::`, or any part of the directive syntax as text.

**Single-line `:::` format also exists** (generated when the block body is short):

    :::list style=ordered 1. Item A 2. Item B :::

When the opening and closing `:::` appear on the same line, treat everything between the tag/params and the trailing `:::` as the block body, split on the item separators (numbered or bullet items).

**Compatibility only:** Do not generate new single-line blocks as the primary format. They are accepted only to keep older IR renderable.

**NEVER pass `:::` lines through to HTML as `<p>` tags or any other text node.** If in doubt: parse it as a block, not as prose.

## IR Validity Taxonomy

Use these labels consistently when reasoning about IR failures:

- `invalid_syntax` — the body cannot be deterministically parsed into the component contract.
- `invalid_semantics` — the structure parses, but the component is still the wrong choice for the content.
- `contract_conflict` — repository docs disagree about the same contract.
- `auto_downgrade_target` — the safer component to emit instead.

## Component Selection Guard

- narrative reports should not force KPI blocks when the source has no short numeric values; use prose, `:::callout`, `:::timeline`, or `:::list` instead.
- charts must never be decorative. Use `:::chart` only when the source has chartable data and a valid schema; otherwise downgrade to `table` or `callout`.
- Timelines must represent real chronological order. Parallel principles, categories, or features belong in lists/prose, not `:::timeline`.
- Diagrams must explain structure or flow that prose cannot scan clearly. If the diagram type would misrepresent the content, downgrade to `callout` or `list`.
- Badges are optional visual enhancements, not a first-class IR tag.

## Child Reference Routing

| IR content | Load |
| --- | --- |
| Plain Markdown sections/prose | `references/rendering/plain-markdown.md` |
| `:::kpi` | `references/rendering/kpi.md` |
| `:::chart` | `references/rendering/chart.md` |
| `:::table` or `:::list` | `references/rendering/table-list.md` |
| `:::timeline` or `:::diagram` | `references/rendering/timeline-diagram.md` |
| `:::image`, `:::code`, `:::callout`, or custom blocks | `references/rendering/media-code-callout.md` |

Load only the child files required by the IR inventory. Keep this entry file visible in every component-rendering path so raw directive parsing and component selection red lines are never lost.
