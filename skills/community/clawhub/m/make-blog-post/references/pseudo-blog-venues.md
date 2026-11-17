# Pseudo-Blog Venues

A pseudo-blog venue publishes a standalone readable post without being a blog:
there is no generator, no front matter, and no feed, but the result is a public
page that serves the same purpose. Common examples are a gist on GitHub, a
Discussions post, a wiki page, a snippet on a hosted git service, a standalone
page on a project site, or an entry in a notes repository.

Treat these as a valid destination. The post is built the same way and held to
the same security and content rules, but its shape changes.

## Shaping the post for a venue with no front matter

- **Never leave a front matter block at the top.** A venue that does not parse
  it renders the raw `title:` and `description:` lines as body text. Move those
  values into the post instead.
- **The title becomes the first heading**, or the venue's own title field where
  it has one.
- **The description becomes the opening line** of the body, or the venue's
  description field.
- **Tags have nowhere to live.** Drop them, or work the one or two that matter
  into the opening sentence as ordinary words.
- **Keep the archive copy intact.** The post store copy keeps its full front
  matter per the post file layout in `SKILL.md`. The venue copy is derived from
  it, so the metadata is never lost.

## Worked example: a gist post on GitHub

A gist has two pieces of discoverable text and no front matter at all.

| Piece | Carries | Rule |
|-------|---------|------|
| Gist description | The post description | The line readers see in listings and search results, so it holds the primary search phrase. One sentence, no project details. |
| File name | The slug, and syntax highlighting | `slugify-text.md` renders as Markdown and keeps the primary phrase in the URL. |
| File body | The post itself | Opens with an `H1` matching the title, then the walkthrough exactly as built. |

Keep it to one file. A gist with several files reads as a project, not a post.

### Archive copy vs. venue copy

The post store copy:

```
title: Slugify Text in PowerShell
description: Turn an arbitrary string into a URL-safe slug with one function.
slug: slugify-text
category: powershell
tags: powershell, string-utils
date: 2026-01-15
---
# Slugify Text in PowerShell
...
```

The gist copy derived from it, saved as `slugify-text.md`:

```markdown
# Slugify Text in PowerShell

Turn an arbitrary string into a URL-safe slug with one function.
...
```

The gist description field takes the same sentence as the `description` value.

## SEO for pseudo-blog venues

These pages are indexed but have no tag system, no internal link graph, and no
structured data. Apply the SEO rules selectively:

- **At full strength**: title, description, slug, and the primary phrase in the
  first 100 words. These are the only signals the venue carries.
- **Skipped**: tags, internal linking, and structured data. There is nothing to
  attach them to.
- **External links still apply.** Link to official documentation for anything
  the sample depends on.

## Publishing to a pseudo-blog venue

Writing the file is this skill's job. Uploading it is not.

1. Write the post to the post store under the chosen category, with full front
   matter.
2. Write the venue-shaped copy alongside it, named as the venue needs it.
3. Report both paths, and state the venue description and file name to use.
4. Stop there. Creating the gist, opening the discussion, or editing the wiki
   is a separate action and needs its own request from the user, exactly as
   committing and pushing do.

Before building a venue copy, check the post store for an existing post on the
same code that already went out to that venue. If one exists, skip.
