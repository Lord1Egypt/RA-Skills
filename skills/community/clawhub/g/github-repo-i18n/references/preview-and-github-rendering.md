# Preview and GitHub rendering

## Two local previews

A local Markdown editor is useful for fast authoring feedback, but it is not the GitHub page. After the local editor preview, render the changed document in a browser using a GitHub-style GFM renderer when one is available.

Check both previews for:

- heading hierarchy and language-switch links;
- tables, code blocks, blockquotes, lists, and details blocks;
- relative links and local images;
- alt text and image sizing;
- raw HTML and sanitizer-sensitive markup;
- wide and narrow content widths;
- light and dark surroundings when supported.

Use an existing project renderer first. Do not add a large preview application or a visual design system to this Skill just to render Markdown. A missing renderer is an unverified check, not a reason to claim that source text matches GitHub.

## Why they differ

GitHub applies its own Markdown rules, CSS, content width, HTML sanitization, image handling, and theme behavior. Local editors may use a different GFM parser, allow HTML or CSS that GitHub strips, resolve paths from a different base directory, or display tables and images at a different width.

Treat the evidence as three distinct states:

| Evidence | Proves | Does not prove |
| --- | --- | --- |
| Local editor preview | authoring readability | GitHub's exact rendering |
| GitHub-style local browser preview | closer GFM layout and responsive behavior | actual remote branch content |
| Actual GitHub page | rendered content at the inspected remote ref | an unpushed local change |

## Preview handoff

Before asking for approval, show:

- one preview for every changed README locale;
- previews of other changed Markdown files when their layout is affected;
- the exact diff or a compact changed-section view;
- the locale matrix and language-switch destinations;
- description and topics before/after text when metadata is selected.

Use the user's feedback to revise the selected scope, then re-render all affected locales. Do not silently treat a local preview as the final GitHub acceptance.

## Width and platform checks

Use the repository's normal Markdown editor and browser tools. For a full-width README, inspect a desktop content width around 900 CSS pixels and a narrow width around 360 CSS pixels. These are readability checks, not visual branding requirements.

When the user authorizes a GitHub remote update, verify the exact branch or page after the update and record the remote reference. If no remote update is authorized, report actual GitHub-page verification as not performed.
