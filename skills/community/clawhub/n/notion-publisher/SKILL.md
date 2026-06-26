---
name: notion-publisher
description: Publish articles to Notion using cached local copies of the target database's default Notion template when available. Use this skill when the user types /notion-publisher, asks to publish an article to Notion, create a Notion article page, draft a post into a Notion database, use an existing Notion article template, refresh the local template cache, or infer article metadata such as slug, summary, tags, category, status, cover, and template before creating a Notion page.
---

# Notion Publisher Skill

## Trigger

Use this skill when the user types `/notion-publisher` or asks to publish, draft, or create an article page in a Notion database.

## Shared Config Path

`~/.notion_publish/notion-publisher-config.json`

Only store reusable publishing preferences:

```json
{
  "default_status": "Draft",
  "template_strategy": "ask_each_time"
}
```

Do not store database IDs, data source IDs, tags, category choices, cover choices, article content, Notion tokens, or private workspace URLs in the config file. Ask for the target database every time.

## Detect Platform

Before choosing a runtime, detect whether the current client is OpenClaw by running:

```bash
which openclaw 2>/dev/null && echo "PLATFORM=openclaw" || echo "PLATFORM=other"
```

If `PLATFORM=openclaw`, assume Notion MCP is not available and prefer the bundled CLI runtime. If `PLATFORM=other`, use MCP when available and fall back to the CLI runtime when MCP is missing.

## Notion Runtime Options

This skill supports MCP clients and command-only clients such as OpenClaw.

Preferred order:
1. If Notion MCP tools are available, use MCP.
2. If MCP is not available but shell commands are available, use the bundled CLI runtime:
   `scripts/notion_publisher.py`
3. If neither MCP nor shell command execution is available, generate the article Markdown and ask the user to publish it manually.

The CLI runtime uses the official Notion API and requires `NOTION_TOKEN` in the environment or in:

```text
~/.notion_publish/.env
```

Example:

```text
NOTION_TOKEN=secret_xxx
```

The target Notion database must be shared with that Notion integration.

To get a Notion token:
1. Open Notion's integrations/creator dashboard.
2. Create a new internal integration in the target workspace.
3. Open the integration's Configuration tab and copy the Internal Integration Secret.
4. Enable the capabilities needed for publishing, including read content, update content, and insert content.
5. Share the target Notion database or parent page with the integration through the Content access tab or Notion's Add connection menu.
6. Save the secret locally in `~/.notion_publish/.env` as `NOTION_TOKEN=secret_xxx`. Never commit it to a repository.

### MCP Tool Names

Use whichever Notion MCP tools are available in the current client.

Codex tool names:
- `mcp__notion__notion_search`
- `mcp__notion__notion_fetch`
- `mcp__notion__notion_create_pages`
- `mcp__notion__notion_update_page`

Claude Code / Claude plugin tool names:
- `mcp__plugin_Notion_notion__notion-search` or `notion-search`
- `notion-fetch`
- `notion-create-pages`
- `notion-update-page`

If no Notion MCP tools are available, do not stop automatically. Use the CLI runtime if shell commands are available.

CLI examples:

```bash
python3 scripts/notion_publisher.py publish \
  --database-id "NOTION_DATABASE_ID_OR_URL" \
  --title "Article title" \
  --body-file article.md \
  --status Draft \
  --type Post
```

The CLI also accepts a Notion data source directly:

```bash
python3 scripts/notion_publisher.py publish \
  --data-source-id "collection://DATA_SOURCE_ID" \
  --title "Article title" \
  --body-file article.md
```

If both `--database-id` and `--data-source-id` are omitted, the CLI asks the user for a Notion database/data source ID or URL. By default, it does not save database IDs. Use `--save-database` only if the user explicitly wants the database remembered as a local prompt default.

CLI update examples:

```bash
python3 scripts/notion_publisher.py update \
  --page-id "NOTION_PAGE_ID_OR_URL" \
  --mode replace \
  --body-file article.md \
  --summary "Updated summary"
```

```bash
python3 scripts/notion_publisher.py update \
  --page-id "NOTION_PAGE_ID_OR_URL" \
  --mode append \
  --body-file appendix.md
```

CLI search example:

```bash
python3 scripts/notion_publisher.py search \
  --data-source-id "collection://DATA_SOURCE_ID" \
  --query "keyword" \
  --limit 10
```

CLI search returns JSON rows with `id`, `title`, `status`, `type`, `category`, `slug`, `date`, and `url`.

Important search behavior:
- MCP search is semantic workspace/data-source search.
- CLI search uses Notion API data source query plus local keyword filtering over title, summary, slug, status, type, category, and tags.
- Use CLI search when OpenClaw needs a page ID before calling `update`.

## Workflow

### 1. Check Config

Read:

```bash
cat ~/.notion_publish/notion-publisher-config.json 2>/dev/null
```

If the file does not exist, create it immediately:

```bash
mkdir -p ~/.notion_publish
cat > ~/.notion_publish/notion-publisher-config.json <<'EOF'
{
  "default_status": "Draft",
  "template_strategy": "ask_each_time"
}
EOF
```

Then continue. During the article confirmation step, show `default_status` and `template_strategy` to the user and let them override values for that article.

Do not save cover preferences. Cover is selected every time.

### 2. Ask for Target Database Every Time

Always ask the user to choose a target database. Do not reuse a cached database.

Offer these input modes:

```text
Please choose a target Notion database:

1. Paste a Notion database URL
2. Enter a database ID
3. Enter keywords to search
4. Press Enter to search for likely article databases
```

After the user chooses, fetch the database schema with the current environment's Notion fetch tool. Read the data source ID, writable properties, select/multi-select options, and available Notion database templates.

In CLI mode, pass the database ID or URL to `scripts/notion_publisher.py`. If the user does not provide one, let the CLI prompt for it. Do not save the database unless the user explicitly chooses `--save-database`.

### 3. Use Cached Default Templates First

Before fetching a Notion template page, read:

`templates/notion-defaults/catalog.md`

If a local cached template matches the target database or template ID, use the local Markdown file as the article structure source.

Fetch the Notion template page only when:
- There is no matching local cache.
- The user explicitly asks to refresh, sync, or re-read the Notion template.

When refreshing, update the cache file under `templates/notion-defaults/` and update `cached_at`. Do not include private database IDs or workspace names if the skill will be shared publicly.

When using a cached or bundled template, preserve its visual structure:
- Keep emoji in headings and callouts.
- Keep callout colors, quote blocks, toggles, dividers, and section order unless the user asks to simplify.
- Replace placeholder headings with meaningful article-specific headings. Prefer neutral numbering such as `一、...` and `二、...`; avoid generic subheadings like `观点一` or `观点二`.
- Do not flatten the template into plain paragraphs.

### 4. Collect Article Basics

Ask:

```text
Title:
Body: paste content, type "generate", or leave blank to draft later.
```

Infer and show a confirmation block:

```text
slug:
summary:
category:
tags:
status:
cover:
inline images:
template strategy:
```

Rules:
- Use the database's real schema. Do not invent property names.
- Pick categories and tags only from existing database options unless the user explicitly asks to create or change schema.
- Use `default_status` from the shared config as the suggested status, but show it for confirmation each time.
- Generate `slug` as English kebab-case.
- Keep `summary` to one or two concise sentences.

### 5. Ask for Cover Every Time

Cover is not saved in config. Always ask:

```text
Choose cover:

1. Search a recommended cover by article topic
2. Search with custom keywords
3. Custom image URL
4. No cover
```

Cover search rules:
- Infer the article topic from the title, summary, tags, and body.
- For technical articles, prefer real nebula, deep-space, telescope, satellite, or astronomy images. NASA, ESA, Hubble, and Webb official image sources are good defaults.
- For AI, LLM, agent, code, infrastructure, or developer-tool articles, default to astronomy/deep-space covers unless the user asks for another style.
- For essays, reflections, product thinking, culture, history, or other non-technical articles, prefer well-known public-domain or museum collection artworks by major artists when they fit the article mood or theme.
- For non-technical articles, search for a real image that matches the article's actual subject instead of using a generic decoration.
- Use the current environment's available web/image search capability when search is requested or when recommending a cover.
- Prefer stable direct image URLs from official sites, open-license sources, or pages that are appropriate to cite.
- Prefer simple direct `.jpg`, `.jpeg`, `.png`, or `.webp` URLs. Avoid URLs with complex crop/query parameters when a clean direct image URL is available.
- Do not use guessed Notion built-in Gallery cover URLs. Notion's UI Gallery covers are not exposed as stable public URLs through the current Notion MCP flow.
- For artwork covers, prefer museum/open-access image sources such as Art Institute of Chicago IIIF, Cleveland Museum of Art Open Access, The Met Open Access, or Rijksmuseum public-domain images.
- Do not hotlink random Google Images thumbnails, unstable CDN thumbnails, or images that are unrelated to the article.
- Show the recommended cover URL and short source note to the user, then ask for confirmation before creating or updating the Notion page.
- If the confirmed cover does not appear in Notion, retry with a simpler stable direct image URL.

Do not use plain-color or mostly solid-color covers by default. Avoid gradient covers unless the user explicitly asks for a simple gradient.

Preferred cover source strategy:
1. Technical / AI / LLM / coding articles:
   - Search NASA, ESA, Hubble, or Webb official image pages.
   - Use direct official image URLs only. Prefer clean `.jpg`, `.jpeg`, `.png`, or `.webp` URLs.
   - Avoid temporary signed URLs, heavily cropped URLs, and arbitrary CDN thumbnails.
2. Art / reflection / essay / product-thinking articles:
   - Prefer Art Institute of Chicago first because it has stable IIIF URLs.
   - Search the API for public-domain artworks with `image_id`, then build:
     `https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg`
   - Good search query shape:
     `https://api.artic.edu/api/v1/artworks/search?q={keywords}&query[term][is_public_domain]=true&fields=id,title,artist_display,image_id,is_public_domain`
3. Alternate artwork sources:
   - The Met Open Access: use the object API's `primaryImage` or `primaryImageSmall` JPEG URL when `isPublicDomain` is true.
   - Rijksmuseum: use IIIF URLs like `https://iiif.micr.io/{id}/full/max/0/default.png` when an image id is available.
   - Cleveland Museum of Art Open Access: use API-provided image URLs when available.
4. Final validation before using a cover:
   - The URL must be a direct image URL or a documented IIIF image URL.
   - The image should visually match the article topic or mood.
   - Do not reuse the same cover for multiple newly generated articles in the same batch unless the user asks.
   - Show title/source/URL to the user when practical, then use the confirmed URL as the Notion page `cover`.

### 6. Ask for Inline Images

Ask whether to insert images inside the article body:

```text
Insert inline images?

1. No inline images
2. Search by article title and summary
3. Search by custom keywords
4. Use custom image URL
```

If the user chooses search:
- Generate 2-4 image search keywords from the title, summary, and article topic.
- Use the current environment's available web/image search capability.
- Prefer stable image URLs from official sites, open-license sources, or pages that are appropriate to cite.
- Avoid hotlinking random copyrighted images from Google Images or unstable CDN thumbnails.
- Show candidate URLs to the user and ask for confirmation before inserting.

When generating a complete article body, include at least one relevant inline image unless the user explicitly chooses "No inline images".
- Place the first inline image after the opening callout or intro paragraph.
- Put inline images on their own line with `<empty-block/>` before and after the image block so Notion App has the best chance of rendering them as native image blocks, not plain Markdown text.
- The page cover does not count as an inline image.
- In batch publishing mode, do not stop for each image if the user has already asked to publish everything; choose stable, relevant image URLs using the cover source strategy above and avoid reusing the same image across the batch.
- For technical / AI / LLM / coding articles, inline images may use the same source families as covers: NASA, ESA, Hubble, Webb, or stable astronomy image URLs. Prefer official NASA/ESA/Webb asset URLs over Wikimedia when the user wants the image to show inside Notion App.
- For non-technical or reflection articles, prefer museum/open-access artwork URLs.
- After updating an existing page, fetch the page and verify the image line is present. If Notion App still shows the image Markdown as text while the frontend renders it, explain that the current MCP update path may have written text that the frontend parses but Notion App does not convert into a native image block; retry with a simpler official direct image URL and explicit surrounding `<empty-block/>` blocks.

Insert confirmed images with Notion-flavored Markdown:

```markdown
<empty-block/>
![Caption](https://example.com/image.jpg)
<empty-block/>
```

Place images near the relevant section. Do not insert images that are unrelated, low quality, broken, or likely to violate usage rights.

### 7. Choose Template Strategy

Use `template_strategy` from config as the default suggestion:
- `ask_each_time`: ask every time.
- `use_cached_notion_template`: default to creating with the Notion template ID.
- `generate_from_cached_template`: default to generating complete content from the cached local template.

Still let the user override.

Show:

```text
Choose template strategy:

1. Use the Notion database template to create a page
2. Generate complete content from the cached local template
3. Use a bundled fallback template
4. No template
```

Important:
- If using `template_id`, do not pass `content`.
- If generating complete content, do not pass `template_id`; read the local template and pass `content`.
- Remove all unreplaced placeholders before creating the page.
- Preserve rich Notion-flavored Markdown styling from the selected template, including emoji headings, callouts, toggles, quotes, and empty-block spacing.

### 8. Fallback Templates

If no database template cache exists, read `templates/catalog.md` and offer:

1. Clean Essay
2. Technical Deep Dive
3. Product Update
4. Knowledge Note
5. Minimal Blog
6. No Template

### 9. Create Page

If using MCP, call the current environment's Notion create pages tool with:

```json
{
  "parent": { "type": "data_source_id", "data_source_id": "..." },
  "pages": [{
    "properties": {},
    "cover": "optional cover URL",
    "template_id": "only when using a Notion database template",
    "content": "only when writing generated Markdown content"
  }]
}
```

Use expanded date property fields such as `date:date:start` and `date:date:is_datetime` when required by the schema.

If using CLI mode, create or save the generated article as Markdown and run:

```bash
python3 scripts/notion_publisher.py publish \
  --database-id "NOTION_DATABASE_ID_OR_URL" \
  --title "Article title" \
  --body-file article.md \
  --status Draft \
  --type Post \
  --category "LLM" \
  --tags "LLM,工具" \
  --slug "article-slug" \
  --summary "Short summary" \
  --date "2025-06-12" \
  --cover "https://example.com/cover.jpg"
```

CLI mode writes inline images as native Notion `image` blocks through the official API. This is preferred when the user needs images to render inside Notion App, not only in a frontend that parses Markdown.

### 10. Update Page When Needed

If a page was created from a Notion database template and the user later wants to replace or insert article content, call the current environment's Notion update page tool with `replace_content` or targeted content updates.

In CLI mode, use `scripts/notion_publisher.py update`.

Supported update modes:
- `--mode replace`: delete/archive existing child blocks, then append the new article blocks. This matches MCP `replace_content`.
- `--mode append`: keep existing child blocks and append the new blocks at the end.

The CLI update command can also update page properties and cover:

```bash
python3 scripts/notion_publisher.py update \
  --page-id "NOTION_PAGE_ID_OR_URL" \
  --mode replace \
  --body-file article.md \
  --status Published \
  --type Post \
  --category "LLM" \
  --tags "LLM,工具" \
  --slug "article-slug" \
  --summary "Short summary" \
  --date "2025-06-12" \
  --cover "https://example.com/cover.jpg"
```

CLI update mode writes inline images as native Notion `image` blocks and should be preferred in OpenClaw when the user needs images to render inside Notion App.

### 11. Search Pages When Needed

If using MCP, search through the target data source with the current environment's Notion search tool, then fetch candidate pages and inspect properties before updating.

If using CLI mode, run:

```bash
python3 scripts/notion_publisher.py search \
  --data-source-id "collection://DATA_SOURCE_ID" \
  --query "keyword" \
  --status Draft \
  --limit 25
```

Use the returned `id` as `--page-id` for `scripts/notion_publisher.py update`.

## Reset

When the user says `/notion-publisher reset`, delete:

`~/.notion_publish/notion-publisher-config.json`

Then re-run the initial config flow. Do not delete template caches unless the user explicitly asks.

## Safety

- Do not publish pages as `Published` unless the user confirms.
- Do not store Notion tokens, workspace URLs, private database IDs, page IDs, or article drafts in the shared config.
- Do not commit private cached templates to public repositories.
- If creating an open-source package, include only generic example templates and example config files.
