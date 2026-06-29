---
name: md-to-rich-html
description: Turn Markdown files or folders into a polished, human-readable, self-contained HTML page by having the agent understand the document, choose an appropriate information design, generate custom HTML/CSS/JS, and validate the result. Prefer static validation; use browser-based visual checks only when the page complexity justifies it or the user asks.
metadata:
  version: "1.0.0"
  author: "441126098"
  tags:
    - markdown
    - html
    - documentation
    - technical-writing
    - visualization
  openclaw:
    homepage: https://github.com/441126098/md-to-rich-html
    emoji: "📄"
---

# Markdown to Rich HTML

Use this skill when the user wants to render, preview, publish, share, or make Markdown easier to read. It supports a single `.md` file or a folder of `.md` files.

This is an agent-first skill. The goal is not to mechanically convert Markdown tags into HTML tags. The goal is to read the source, infer the reader's task, and design a page that makes the content easier to scan, understand, compare, and use.

## Default Workflow

1. Inspect the input file or folder and read the Markdown content.
2. Determine the document's real reading purpose, such as a report, guide, interview pack, decision record, implementation plan, review, tutorial, knowledge note, changelog, or mixed document.
3. Identify local semantic blocks instead of relying only on document type:
   - executive summary, key takeaways, risks, decisions, action items
   - steps, timeline, roadmap, checklist, status, owners
   - Q&A, interview questions, prompts, answers, follow-ups
   - comparisons, trade-offs, pros/cons, options, matrices
   - metrics, counts, constraints, assumptions, warnings
   - code examples, API references, diagrams, tables, citations
4. Design an information structure for the page before writing HTML:
   - useful first viewport with title, context, summary, and document-specific signals
   - navigation or section map when the document is long
   - component choices that match the content, not just generic prose
   - responsive behavior for desktop and mobile
5. Generate a self-contained HTML file with inline CSS and JS.
6. Validate the HTML statically for complete structure, self-contained assets, valid links/anchors where practical, responsive CSS, and obvious accessibility issues.
7. Open a browser for visual inspection only when the user explicitly asks for preview/verification, the page has complex layout, JavaScript interaction, Mermaid, charts, or meaningful responsive behavior, or the agent changed an existing visual design.
8. Iterate if the result still looks like plain Markdown, has weak hierarchy, crowded spacing, broken wrapping, inaccessible contrast, or mobile layout issues.

## Design Rules

- Do not preserve Markdown structure mechanically when a better reading structure is obvious.
- Do not invent facts. Summaries, stats, badges, labels, and classifications must be derived from the source content or clearly phrased as structural labels.
- Prefer a small set of reusable human-reading components over document-type templates:
  - summary strip
  - stat grid
  - callout
  - comparison table or option matrix
  - timeline
  - step flow
  - collapsible Q&A
  - checklist panel
  - decision card
  - risk/action item list
  - code explanation block
  - diagram section
- Use visual hierarchy deliberately: typography, spacing, borders, muted backgrounds, accent colors, section labels, and stable component dimensions.
- Avoid generic landing pages. The first screen should expose the actual content.
- Keep the output portable as a single HTML file unless the user asks for external assets.
- If the Markdown contains Mermaid, either preserve and load Mermaid or convert the diagram to a readable fallback block.
- If the Markdown contains code, preserve syntax and context; add captions or explanation panels when helpful.
- If the content is short and plain, keep the design restrained. Do not over-design simple notes.

## Quality Bar

Before finishing, check the generated page against these questions:

- Can a reader understand the document's purpose within the first viewport?
- Are the most important points surfaced before the long body text?
- Are repeated structures, such as questions, options, tasks, or releases, rendered as components rather than paragraphs?
- Are dense tables, code, and diagrams readable on desktop and mobile?
- Does the page have enough hierarchy and contrast without becoming decorative noise?
- Does the output avoid the "Markdown with nicer CSS" problem?

Use static inspection as the default verification method. Browser screenshots and console checks are optional quality gates for complex pages, not a required step for every conversion.

## Maintenance

- Prefer improving this skill's guidance and quality bar before adding new detector code.
- Add helper scripts only when they provide narrow tooling, such as file collection, asset copying, HTML validation, or screenshot capture.
- Do not move the core design decision back into mechanical detector or template enumeration.
