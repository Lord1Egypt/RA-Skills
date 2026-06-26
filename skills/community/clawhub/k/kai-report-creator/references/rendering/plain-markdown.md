# Plain Markdown Rendering

## Plain Markdown (default)

Convert using standard Markdown rules. Wrap each `##` section in:

    <section data-section="[heading text]" data-summary="[one sentence summary]">
      <h2 id="section-[slug]">[heading text]</h2>
      [section content]
    </section>

**`data-summary` must be plain text only** — write a short human-readable summary of the section in natural language. Never copy raw IR content (lists, prose, component bodies) into it. Especially never include `:::` directive syntax in `data-summary`.

For `###` headings: `<h3 id="section-[slug]">[heading text]</h3>`

`highlight-sentence` is a prose pattern, not an IR tag. If a paragraph deserves emphasized treatment, render it as prose upgraded to `<p class="highlight-sentence">...</p>`; do not invent `:::highlight-sentence`.

`lead-block`, `section-quote`, and `action-grid` are also prose/HTML patterns, not IR tags. Use them only when the surrounding prose clearly supports them.

- `lead-block` — decisive opening sentence that frames the section
- `section-quote` — strongest judgment sentence in a prose-heavy section
- `action-grid` — 2–5 implications, contrasts, or next actions that scan better as cards

For `narrative` reports, prefer `claim -> explanation -> scan anchor` over leaving every section as plain paragraphs.
If uncertain, stay with plain prose plus one callout/list/timeline rather than forcing a rhythm block.
