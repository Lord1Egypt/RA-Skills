# Blocks — Reading and Building Page Content

Page content is a tree of blocks, fetched separately from the page and one level at a time. Everything here applies equally to a database row's body and a plain page.

**Contents:** [Read One Level](#read-one-level) · [Reading a Whole Page](#reading-a-whole-page) · [Append Children](#append-children) · [Block Payloads](#block-payloads) · [Container Blocks](#container-blocks) · [Update a Block](#update-a-block) · [Delete a Block](#delete-a-block) · [Unsupported and Read-Only Blocks](#unsupported-and-read-only-blocks) · [Markdown Conversion](#markdown-conversion)

## Read One Level

```bash
curl 'https://api.notion.com/v1/blocks/BLOCK_OR_PAGE_ID/children?page_size=100' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

A page id is a block id — the page is the root of its own tree. The response returns direct children only, paginated at 100.

## Reading a Whole Page

There is no "give me the page as text" endpoint. The full read is a recursion:

1. Fetch children of the page, looping `has_more` (`pagination.md`).
2. For each block with `"has_children": true`, fetch its children too.
3. Repeat until nothing has children.

Cost: **one request per container, per 100 children**. A 300-block page with 20 toggles is roughly 3 + 20 = 23 requests, ≈8s at 3 req/s. A whole-workspace export is a job, not a call (`bulk.md`).

Depth-first with a queue and a visited set. Synced blocks can point at content elsewhere; following them without a visited set is how an export loops forever.

## Append Children

```bash
curl -X PATCH 'https://api.notion.com/v1/blocks/PARENT_ID/children' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "heading_2", "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "Findings"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Body text."}}]}}
    ]
  }'
```

- Appends to the end. To insert elsewhere, pass `after` with the id of the block to insert behind — otherwise rebuilding order means deleting and re-appending.
- **100 children per call is the batch that always works.** Chunk longer lists and keep the order across chunks by appending sequentially, never in parallel — concurrent appends to one parent interleave.
- Nesting in a single request is limited to two levels. Build deeper trees by appending to the child ids the response returns.
- The response contains the created blocks with their ids — capture them if anything downstream needs to address the content.
- 500 KB total request body (SKILL.md Limits). A "payload too large" on an append is usually one code block carrying a whole file.

## Block Payloads

```json
{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Text"}}]}}
{"type": "heading_1", "heading_1": {"rich_text": [...], "is_toggleable": false}}
{"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [...]}}
{"type": "numbered_list_item", "numbered_list_item": {"rich_text": [...]}}
{"type": "to_do", "to_do": {"rich_text": [...], "checked": false}}
{"type": "toggle", "toggle": {"rich_text": [...]}}
{"type": "code", "code": {"rich_text": [...], "language": "python", "caption": []}}
{"type": "quote", "quote": {"rich_text": [...]}}
{"type": "callout", "callout": {"rich_text": [...], "icon": {"type": "emoji", "emoji": "💡"}}}
{"type": "divider", "divider": {}}
{"type": "bookmark", "bookmark": {"url": "https://example.com"}}
{"type": "equation", "equation": {"expression": "e^{i\\pi}+1=0"}}
{"type": "image", "image": {"type": "external", "external": {"url": "https://…"}}}
```

Also `heading_2`/`heading_3`, `embed`, `video`, `file`, `pdf`, `link_to_page`, `table_of_contents`, `breadcrumb`, `child_page`, `child_database`.

- Every text-bearing block takes a **rich text array**, subject to the 2,000-character-per-object cap (`properties.md`).
- `code.language` must be one Notion recognizes; an unknown language is a `validation_error`, not a fallback to plain.
- List items are flat blocks — indentation is parent/child, not a property. Nested bullets are children of the bullet above.
- Numbered lists renumber themselves in the UI; the API has no ordinal to set.

## Container Blocks

| Block | Constraint that bites |
|---|---|
| `table` | Must be created with `table_width`, `has_column_header`, and its `table_row` children in the same request. Width is fixed at creation — adding a column later means rebuilding the table |
| `table_row` | `cells` is an array of rich text **arrays**, one per column, and its length must equal `table_width` exactly |
| `column_list` | Requires at least two `column` children, each with its own content, all in one request. A lone column is rejected |
| `synced_block` | The original has `synced_from: null`; a copy references the original's id. Editing a copy edits the original |
| `toggle`, `callout`, `quote` | Accept children; content nested under them needs a second call unless included in the create |
| `child_page` / `child_database` | Read-only markers. Create the page or database through its own endpoint, not by appending this block |

## Update a Block

```bash
curl -X PATCH 'https://api.notion.com/v1/blocks/BLOCK_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"paragraph": {"rich_text": [{"type": "text", "text": {"content": "Updated"}}]}}'
```

- Replaces the block's content wholesale; there is no partial edit of a rich text array.
- A block cannot change type. Turning a paragraph into a heading is delete + append (and the new block gets a new id).
- Setting `"archived": true` on a block trashes it like a page.

## Delete a Block

```bash
curl -X DELETE 'https://api.notion.com/v1/blocks/BLOCK_ID' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

Moves the block **and every descendant** to the trash. Deleting a container silently takes its subtree; state the child count before running it under `write_mode: confirm-writes`.

## Unsupported and Read-Only Blocks

Some block types render in Notion but come back as `"type": "unsupported"` with no content, and cannot be created through the API. An export or duplication that hits them loses that content with no error.

- Count them during a read and report the count. "The copy is missing three embeds" is a fact the user needs before they trust the copy.
- Link previews and some third-party embeds are the usual offenders; plain `embed` and `bookmark` are creatable.

## Markdown Conversion

Converting markdown to blocks is the most-rewritten piece of code in this domain. The parts that are always wrong the first time:

- Inline formatting is `annotations` on rich text objects, not markup inside `content` — writing `**bold**` produces literal asterisks.
- Links are `text.link.url`, not markdown syntax.
- Nested lists are child blocks, so a two-level list is two requests unless it fits in the create's two-level nesting allowance.
- Fenced code needs the language mapped to Notion's list; unmapped languages must fall back to `plain text` deliberately.
- Tables need width declared up front and rows padded to it.
- Long paragraphs need chunking at 2,000 characters at a word boundary you choose.

**When a conversion or a page skeleton is worth reusing**, save it to `~/Clawic/data/notion-api-integration/artifacts/template-<what>.md` with the payload and the block-type mapping it assumes, and add its `## Boxes` line in the same turn.
