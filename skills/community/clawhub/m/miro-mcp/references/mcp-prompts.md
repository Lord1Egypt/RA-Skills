# Miro MCP Tools & Prompts

This reference guide documents the 2 built-in prompts and 14 available tools in Miro MCP, with usage patterns and rate limit guidance.

## Built-in Prompts

Miro MCP provides two high-level prompts that combine multiple tools for common workflows.

### `code_create_from_board`

**Purpose:** Analyze a Miro board to understand project/feature requirements, then generate comprehensive documentation and implementation guidance.

**Workflow (two-phase):**
1. **Phase 1 - Analysis:** Agent explores board, identifies key documents, requirements, and design decisions
2. **Phase 2 - Generation:** Agent recommends document types, then generates specific documentation based on recommendations

**When to use:**
- You have a PRD or requirements on a Miro board
- You need implementation guidance, documentation, or code structure
- You want to convert visual designs into structured documentation

**Example:**
```
Analyze this board for product requirements and generate implementation guidance:
https://miro.com/app/board/uXjVGAeRkgI=/
```

### `code_explain_on_board`

**Purpose:** Transform code implementation into clear visual explanations by creating diagrams and documentation on a Miro board.

**Workflow:**
1. Agent analyzes provided code (from codebase, repository, or text)
2. Agent creates visual diagrams (architecture, data flow, component relationships)
3. Agent adds documentation to board explaining the code structure

**When to use:**
- You want to visualize existing code architecture
- You need to onboard team members with visual code documentation
- You're creating architecture documentation from a codebase

**Example:**
```
Explain my codebase at ~/dev/myapp by creating architecture diagrams on this board:
https://miro.com/app/board/uXjVGAeRkgI=/
```

## Tools Reference

Miro MCP provides 14 tools for reading, writing, and manipulating board content. Tools are organized by function.

### Discovery Tools

#### `board_list_items`
**Purpose:** List items on a board with pagination and filtering.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `item_type`: Filter by type (optional): frame, document, prototype, table, diagram, sticky, shape, image
- `parent_id`: Filter by parent container (optional)
- `limit`: Number of results (default 100)
- `cursor`: Pagination cursor for subsequent requests

**Returns:** List of board items with type, title, URL, parent container info

**Use cases:**
- Discover what's on a board before diving deeper
- List all documents, prototypes, or diagrams on a board
- Paginate through large boards efficiently

### Context Exploration Tools

#### `context_explore`
**Purpose:** Discover high-level items on a board (frames, documents, prototypes, tables, diagrams) with their URLs and titles.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID

**Returns:** High-level structure with frames, documents, prototypes, diagrams, tables and their metadata

**Use cases:**
- Get a quick overview of board structure
- Find specific item types quickly
- Understand board organization before detailed exploration

#### `context_get`
**Purpose:** Get text context from a specific board item.

**Uses AI Credits:** Yes ⚠️

**Parameters:**
- `board_id`: Miro board ID
- `item_id`: Item to read
- `item_type`: Type of item (document, prototype, frame, etc.)

**Returns:**
- **Documents:** HTML content with formatting preserved
- **Prototypes:** UI markup/structure of screens
- **Frames:** AI-summarized text of frame contents
- **Other items:** Text content where applicable

**Use cases:**
- Read full document content (PRDs, requirements, notes)
- Extract UI structure from prototype screens
- Summarize frame contents

**⚠️ Cost Warning:** This is the ONLY tool that uses Miro AI credits. Minimize parallel calls to this tool.

### Diagram Tools

#### `diagram_create`
**Purpose:** Create a new diagram on a Miro board from DSL (domain-specific language).

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `diagram_type`: flowchart, uml_class, uml_sequence, erd
- `dsl_text`: Diagram definition in DSL format
- `x`, `y`: Position on board (optional)
- `title`: Diagram title (optional)

**Returns:** Created diagram object with ID and URL

**Supported diagram types:**
- **Flowchart:** Decision trees, process flows
- **UML Class:** Entity relationships, class hierarchies
- **UML Sequence:** Actor interactions, message flows
- **ERD:** Database schema, table relationships

**Use cases:**
- Generate architecture diagrams from code analysis
- Visualize workflows and processes
- Document data models

**Example DSL (Flowchart):**
```
start
  -> decision: "User logged in?"
    -> yes -> action: "Show dashboard"
    -> no -> action: "Show login"
  -> end
```

#### `diagram_get_dsl`
**Purpose:** Get DSL format specification (syntax, rules, color guidelines, examples) for a diagram type.

**Uses AI Credits:** No

**Parameters:**
- `diagram_type`: flowchart, uml_class, uml_sequence, erd

**Returns:** DSL specification with syntax rules, color palette, styling options, and examples

**Use cases:**
- Before creating a diagram, fetch the DSL spec
- Understand diagram syntax and constraints
- Learn color and styling guidelines

### Document Tools

#### `doc_create`
**Purpose:** Create a new document on a Miro board.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `title`: Document title
- `content`: Markdown content (supports headings, bold, italic, lists, links)
- `x`, `y`: Position on board (optional)

**Returns:** Created document object with ID and URL

**Markdown support:**
- Headings (# ## ###)
- Bold (**text**)
- Italic (*text*)
- Lists (- or *)
- Links ([text](url))

**Use cases:**
- Create implementation guides from code analysis
- Document design decisions
- Generate meeting notes or requirements

#### `doc_get`
**Purpose:** Read the markdown content and metadata of an existing document.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `doc_id`: Document ID

**Returns:** Document markdown content, version info, metadata

**Use cases:**
- Extract requirements from PRD documents
- Read design documentation
- Track document versions

#### `doc_update`
**Purpose:** Edit content in an existing document using find-and-replace.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `doc_id`: Document ID
- `find`: Text to find
- `replace`: Replacement text
- `replace_all`: true/false (false = first occurrence only)

**Returns:** Updated document with change summary

**Use cases:**
- Update requirements based on feedback
- Correct documentation errors
- Append new information to existing docs

### Table Tools

#### `table_create`
**Purpose:** Create a new table on a Miro board.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `title`: Table title
- `columns`: Array of column definitions with `name`, `type` (text or select)
- `x`, `y`: Position on board (optional)

**Returns:** Created table object with ID and URL

**Column types:**
- **text:** Free-form text input
- **select:** Predefined options dropdown

**Use cases:**
- Create requirement matrices
- Build task lists or checklists
- Organize data on board

#### `table_list_rows`
**Purpose:** Get rows from a Miro table with column metadata and filtering.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `table_id`: Table ID
- `column`: Column to filter by (optional)
- `value`: Value to match (optional)
- `limit`: Number of rows (default 100)
- `cursor`: Pagination cursor

**Returns:** Table rows with column values, column definitions

**Use cases:**
- Read task lists or checklists from board
- Extract data from organized tables
- Filter and retrieve specific rows

#### `table_sync_rows`
**Purpose:** Add new rows or update existing rows in a table using key-based upsert matching.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `table_id`: Table ID
- `rows`: Array of row objects with column values
- `key_column`: Column to use for upsert matching

**Returns:** Summary of added/updated rows

**Upsert logic:**
- If row with `key_column` value exists → update it
- If row doesn't exist → add new row

**Use cases:**
- Bulk update task statuses
- Sync data from external sources
- Update tracking tables

### Image Tools

#### `image_get_url`
**Purpose:** Get the download URL for an image item on a board.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `image_id`: Image item ID

**Returns:** Download URL for the image

**Use cases:**
- Download board images for processing
- Share image URLs externally

#### `image_get_data`
**Purpose:** Retrieve the actual binary image data (base64-encoded) for an image item.

**Uses AI Credits:** No

**Parameters:**
- `board_id`: Miro board ID
- `image_id`: Image item ID

**Returns:** Base64-encoded image data

**Use cases:**
- Embed images in generated documents
- Process images programmatically
- Analyze board mockups

## Rate Limits

### Standard API Rate Limits
- Apply **per user** across all tool calls
- Based on API request count, data volume, time windows
- Returns **429 Too Many Requests** if exceeded

### Tool-Specific Limits
Some tools have stricter limits:

| Tool | Limit | Notes |
|------|-------|-------|
| `context_get` | Strictest | Uses AI credits, most restrictive |
| Other tools | Standard | Share standard API rate limit |

Limits are subject to change; check Miro documentation for latest values.

### Managing Rate Limits

**Best practices:**
1. **Minimize `context_get` calls** — Only read items you need
2. **Batch operations** — Use `table_sync_rows` instead of individual row updates
3. **Implement backoff** — Exponential backoff when rate-limited (retry after 60+ seconds)
4. **Cache results** — Store frequently accessed board content locally when possible
5. **Reduce parallelization** — Avoid parallel `context_get` calls

**If rate-limited:**
- Wait 60+ seconds before retrying
- Implement exponential backoff (1s, 2s, 4s, 8s...)
- Reduce frequency of parallel operations
- Contact Miro Developer Discord for guidance on limits

## Workflow Examples

### Example 1: Analyze Board + Generate Docs

```
1. Use context_explore to discover board structure
2. Use context_get to read key documents (PRD, design)
3. Use doc_create to generate implementation guide
4. Use diagram_create to generate architecture diagram
```

### Example 2: Update Task List from Feedback

```
1. Use table_list_rows to fetch all tasks
2. Analyze and determine updates needed
3. Use table_sync_rows to bulk update task statuses
4. Use doc_create to document decisions
```

### Example 3: Visualize Code as Diagrams

```
1. Use code_explain_on_board prompt
2. Agent uses diagram_get_dsl to understand syntax
3. Agent uses diagram_create to generate UML diagrams
4. Agent uses doc_create to add code explanations
```

## Next Steps

- **Setup for your client:** See [references/ai-coding-tools.md](ai-coding-tools.md)
- **Workflow patterns:** See [references/best-practices.md](best-practices.md)
- **API details:** See [references/rest-api-essentials.md](rest-api-essentials.md)
