# Wiki Patterns Reference

Use this file for concrete templates and operational patterns when working on a markdown knowledge wiki.

## Recommended source summary template

```markdown
# Source: <title>

## Summary
2-6 sentence summary of the source.

## Key takeaways
- Point one
- Point two
- Point three

## Entities and concepts
- [[Entity A]]
- [[Concept B]]

## Claims
- Claim with enough specificity to be checked later

## Open questions
- Question one

## Related wiki pages
- [[Topic Page]]

## Provenance
- Author:
- Date:
- URL or local path:
```
```

## Recommended topic page template

```markdown
# <Topic>

## Summary
Short synthesis.

## Current understanding
- Durable point
- Durable point

## Important nuances
- Caveat or ambiguity

## Timeline or developments
- Date: event

## Open questions
- Unknown or disputed point

## Related
- [[Related Page]]

## Sources
- [[Source: Example]]
```
```

## Contradiction handling pattern

When two sources disagree, do not silently merge them into one narrative.

Use a section like:

```markdown
## Tensions and contradictions
- Source A claims X
- Source B claims Y
- Current best interpretation: Z
- Confidence: low | medium | high
```
```

If the contradiction is important and recurring, create a dedicated analysis page.

## Page creation heuristics

Create a page when:
- the concept/entity appears in multiple sources
- the page can become a hub for links
- the content is substantial enough to deserve its own summary

Do not create a page when:
- the term is mentioned only once and is not central
- the resulting page would contain only one weak bullet
- the information fits naturally into an existing page

## Index organization patterns

Common groupings for `index.md`:

```markdown
# Index

## Topics
- [[Topic A]] - one line

## Concepts
- [[Concept A]] - one line

## Entities
- [[Entity A]] - one line

## Analyses
- [[Analysis A]] - one line

## Sources
- [[Source: Example]] - one line
```
```

Keep descriptions compact. Prefer one useful line over verbose summaries.

## Log entry pattern

```markdown
## [YYYY-MM-DD] ingest | <title>
- Created: [[Source: Title]]
- Updated: [[Topic A]], [[Entity B]]
- Notes: contradiction with [[Older Source]] on <claim>
```
```

For a query:

```markdown
## [YYYY-MM-DD] query | <question>
- Read: [[Topic A]], [[Analysis B]]
- Created: [[Analysis: <short title>]]
```
```

## Query filing heuristic

Save a query result back into the wiki when it has any of these qualities:
- cross-source synthesis that would be expensive to redo
- comparison between multiple entities or approaches
- a new framing or insight that changes how related pages should read
- a decision memo the user may revisit

Do not save trivial one-off answers.

## Minimal schema document template

```markdown
# Wiki Schema

## Purpose
Describe what this wiki is for.

## Folder layout
Describe top-level directories.

## Page types
- topic
- concept
- entity
- analysis
- source

## Naming rules
State canonical naming conventions.

## Citation rules
Describe how pages cite sources and related pages.

## Update workflow
Describe ingest, query, and lint workflows.
```
```

## Human factors

Optimize for a human browsing the wiki later.

Prefer:
- short summaries near the top
- sections with stable names
- explicit related pages
- visible uncertainty

Avoid:
- giant walls of generated prose
- excessive metadata
- duplicate pages with overlapping scope
- hiding evidence behind polished summaries
