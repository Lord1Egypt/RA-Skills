# `ghst page`

Page management in Ghost.

## Usage
```bash
ghst page [options] [command]
```

## Commands
- `list [options]`: List pages.
- `get [options] [id]`: Get a page by id or slug.
- `create [options]`: Create a page.
- `update [options] [id]`: Update a page by id or slug.
- `delete [options] <id>`: Delete a page.
- `copy <id>`: Copy a page.
- `bulk [options]`: Run bulk page operations.

## Key Options
- `--json`: Output as raw JSON.
- `--jq <query>`: Process JSON with jq.
- `--limit <count>`: Limit results.
- `--filter <query>`: filter results.

## Searching and Filtering

You can find a page by various attributes using the `ghst page list` command along with the `--filter` option. Ghost uses a query language called **NQL** (Nexa Query Language) for its API filters, meaning you can filter against almost any top-level attribute of the `page` object.

### Searching by Title

Here is how you can use NQL to search by title:

### 1. Partial Match (Contains)
If you know part of the title and want to search for any page containing that phrase, use the `~` (tilde) operator:

```bash
ghst page list --filter "title:~'My Awesome'"
```
*(This will match pages like "My Awesome Page", "Check out My Awesome new feature", etc.)*

### 2. Exact Match
If you want to find a page with a specific, exact title, omit the tilde:

```bash
ghst page list --filter "title:'My Exact Title'"
```

### 3. Combining Filters
You can also combine title searches with other filters like status. For example, to find a *published* page containing a specific word:

```bash
ghst page list --filter "title:~'Awesome'+status:published"
```

**Note:** If your title contains a single quote (`'`), you need to escape it (e.g., `title:~'It\'s a match'`) or just search for the words around the quote to keep things simple.

### Advanced Filtering Attributes

Here is a comprehensive list of the attributes you can use when constructing a `--filter` string for `ghst page list`:

### Core Identifiers
*   `id`: The internal Ghost ID of the page.
*   `uuid`: The globally unique identifier.
*   `slug`: The URL slug for the page.

### Standard Metadata
*   `title`: The title of the page (can use exact match `:` or partial match `:~`).
*   `status`: The current state of the page (`draft`, `published`, `scheduled`).
*   `visibility`: The access level (`public`, `members`, `paid`, `tiers`).
*   `featured`: Whether the page is marked as featured (`true` or `false`).
*   `email_only`: Whether the page is an email-only newsletter (`true` or `false`).

### Timestamps
*(These accept datetime strings, and you can use operators like `>`, `<`, `>=`, `<=`)*
*   `created_at`: When the page was created.
*   `updated_at`: When the page was last updated.
*   `published_at`: When the page was published.

### Relational Attributes
*(You can filter on nested relationships using dot notation)*
*   `primary_author.slug` / `authors.slug`: Filter by specific authors.
*   `primary_tag.slug` / `tags.slug`: Filter by specific tags.

### Content & Snippets
*   `custom_excerpt`: The custom excerpt text.
*   `meta_title` / `meta_description`: Search-engine specific overrides.
*   `og_title` / `og_description`: Open Graph (Facebook/social) overrides.
*   `twitter_title` / `twitter_description`: Twitter/X specific overrides.
*   `custom_template`: The name of the custom Handlebars template in the theme.
*   `email_segment`: For pages sent via email, the target audience segment (e.g., `all`).

### Example Usage

Find a page by its exact slug:
```bash
ghst page list --filter "slug:'about-us'"
```

Find all pages that belong to the `news` tag and are `published`:
```bash
ghst page list --filter "tags.slug:news+status:published"
```

Find all draft pages created by a specific author:
```bash
ghst page list --filter "primary_author.slug:jane+status:draft"
```

Find pages published after a certain date:
```bash
ghst page list --filter "published_at:>'2026-01-01 00:00:00'"
```
