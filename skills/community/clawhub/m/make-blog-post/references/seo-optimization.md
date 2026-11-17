# SEO Optimization

Optimize the post for the way readers actually search for the problem it
solves. How far to take that depends on where the post lands, so settle the
destination first, then apply the matching level.

## Levels, relative to workspace context

| Level | Applies when | What to do |
|-------|--------------|------------|
| `full` | The post is going into a published blog or site (the `<blogSite>` form, or a workspace that builds to a public URL). | Apply every rule below. |
| `light` | The post is going only to the post store. | Apply title, description, slug, and tags. Skip internal linking and structured data. The post stays portable if it is published later. |
| `venue` | The post is going to a pseudo-blog venue such as a gist. | Apply title, description, slug, and opening paragraph at full strength. Skip the rest. See `pseudo-blog-venues.md`. |
| `internal` | The post is going into a documentation set. | Optimize for the reader searching the repository, not for a search engine: plain descriptive headings, terms that match the code's own identifiers, and a title that reads well in a file listing. Skip keyword phrasing that would look out of place in docs. |

With `seo-optimization` set to `auto`, pick the level from that table. With it
pinned, use the pinned level. With it set to `off`, skip this file entirely.

## Keywords come from the technology, not the project

The security and content rules in `SKILL.md` still hold. Derive search terms
from the generalized subject of the post: the language, runtime, library, and
task the code performs. **Never** use a project, client, organization,
repository, or internal product name as a keyword, tag, or slug, even when the
workspace is full of them.

Read the workspace for the technical vocabulary, not the proprietary
vocabulary:

- The language and runtime in use (e.g. `powershell`, `node`, `python`).
- The problem domain the code sits in (e.g. `file-io`, `date-time`,
  `string-utils`), which is usually the `<category>` already chosen.
- The terms the code's own API uses, where they are standard rather than
  invented for this project.

Choose one primary search phrase and at most two secondary phrases. Write the
phrase a reader would type, not the phrase the codebase uses internally.

## Title

- Lead with the primary phrase. A reader scanning results should see the
  problem in the first three or four words.
- Keep it under 60 characters so it is not truncated in results.
- State the task, not the cleverness. `Slugify Text in PowerShell` beats
  `A Neat Trick for Tidy URLs`.
- One `H1` per post, and it matches the title.

## Slug

- Lowercase, hyphenated, three to six words, derived from the primary phrase.
- No dates, no numbering, no stop words that carry no search weight.
- Match the file name so the file and the URL stay in step
  (`slugify-text.md` serves `/slugify-text`).
- When the workspace is a site with an established slug convention, follow the
  site.

## Headings and body

- Put the primary phrase in the first 100 words, once, in a sentence that would
  read the same without it.
- Use `H2` headings phrased the way readers search: what the code does, how to
  use it, what it returns, when not to use it.
- Use natural variants rather than repeating one phrase. Repetition past a
  couple of natural uses reads as padding and works against the post.
- Tag every code block with its language so it renders correctly and can be
  picked up as a code result.
- Give any image real alt text describing what it shows. Skip decorative images
  entirely.

## Tags and taxonomy

- When the workspace is a blog or site, reuse tags that site already uses. A
  new tag with one post behind it helps no one.
- Otherwise derive two to four tags from the category and the language.
- Keep tags lowercase and hyphenated, matching the `<category>` convention.

## Linking

- **Internal**: at `full` level, link to one or two existing posts in the same
  category when a genuine connection exists. No link is better than a forced
  one.
- **External**: link to the official documentation for any language feature or
  library the sample depends on. Do not link to private, internal, or
  authenticated URLs.
- Write descriptive link text. Never `click here`.

## Structured data

At `full` level, if the site already emits article metadata (JSON-LD,
OpenGraph, or equivalent), fill the fields it expects from the front matter
values rather than adding a separate block. Do not introduce a structured data
mechanism the site does not already have.
