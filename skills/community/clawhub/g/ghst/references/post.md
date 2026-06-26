# `ghst post`

Post management in Ghost.

## Usage
```bash
ghst post [options] [command]
```

## Commands
- `list [options]`: List posts.
- `get [options] [id]`: Get a post by id or slug.
- `create [options]`: Create a post.
- `update [options] [id]`: Update a post by id or slug.
- `delete [options] [id]`: Delete a post.
- `publish [options] <id>`: Publish a post.
- `schedule [options] <id>`: Schedule a post.
- `unschedule <id>`: Unschedule a post.
- `copy <id>`: Copy a post.
- `bulk [options]`: Run bulk post operations.

## Key Options (Common to most list/get commands)
- `--json`: Output as raw JSON.
- `--jq <query>`: Post-process JSON with a jq expression.
- `--limit <count>`: Limit the number of results.
- `--filter <query>`: Apply Ghost API filters.
- `--include <models>`: Include related models (e.g., `tags,authors`).
- `--fields <names>`: Specify which fields to return.

## Searching and Filtering

You can find a post by various attributes using the `ghst post list` command along with the `--filter` option. Ghost uses a query language called **NQL** (Nexa Query Language) for its API filters, meaning you can filter against almost any top-level attribute of the `post` object.

### Searching by Title

Here is how you can use NQL to search by title:

### 1. Partial Match (Contains)
If you know part of the title and want to search for any post containing that phrase, use the `~` (tilde) operator:

```bash
ghst post list --filter "title:~'My Awesome'"
```
*(This will match posts like "My Awesome Post", "Check out My Awesome new feature", etc.)*

### 2. Exact Match
If you want to find a post with a specific, exact title, omit the tilde:

```bash
ghst post list --filter "title:'My Exact Title'"
```

### 3. Combining Filters
You can also combine title searches with other filters like status. For example, to find a *published* post containing a specific word:

```bash
ghst post list --filter "title:~'Awesome'+status:published"
```

**Note:** If your title contains a single quote (`'`), you need to escape it (e.g., `title:~'It\'s a match'`) or just search for the words around the quote to keep things simple.

### Advanced Filtering Attributes

Here is a comprehensive list of the attributes you can use when constructing a `--filter` string for `ghst post list`:

### Core Identifiers
*   `id`: The internal Ghost ID of the post.
*   `uuid`: The globally unique identifier.
*   `slug`: The URL slug for the post.

### Standard Metadata
*   `title`: The title of the post (can use exact match `:` or partial match `:~`).
*   `status`: The current state of the post (`draft`, `published`, `scheduled`).
*   `visibility`: The access level (`public`, `members`, `paid`, `tiers`).
*   `featured`: Whether the post is marked as featured (`true` or `false`).
*   `email_only`: Whether the post is an email-only newsletter (`true` or `false`).

### Timestamps
*(These accept datetime strings, and you can use operators like `>`, `<`, `>=`, `<=`)*
*   `created_at`: When the post was created.
*   `updated_at`: When the post was last updated.
*   `published_at`: When the post was published.

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
*   `email_segment`: For posts sent via email, the target audience segment (e.g., `all`).

### Example Usage

Find a post by its exact slug:
```bash
ghst post list --filter "slug:'my-awesome-post'"
```

Find all posts that belong to the `news` tag and are `published`:
```bash
ghst post list --filter "tags.slug:news+status:published"
```

Find posts published after a certain date:
```bash
ghst post list --filter "published_at:>'2026-01-01 00:00:00'"
```
