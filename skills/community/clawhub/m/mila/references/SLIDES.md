# Slides Reference

Slide presentations store an array of slides, each rendered on a 960x540px canvas using free-form HTML.

## Slide object

Each slide in a presentation has these fields:

| Field | Type | Description |
|---|---|---|
| `html` | string | HTML content rendered on a 960x540px canvas |
| `background` | string | CSS background value (color, gradient, or image) |
| `notes` | string | Speaker notes (not displayed in presentation) |

The canvas is 960px wide and 540px tall. Design HTML to fit within these dimensions. Use absolute positioning or flexbox to place elements precisely. `<script>` tags are automatically stripped for security.

---

## List Slides

**REST API:**

```
GET /v1/slides
```

**Query parameters:**

| Param | Default | Description |
|---|---|---|
| `limit` | 50 | Results per page (1-100) |
| `offset` | 0 | Pagination offset |
| `sort` | `updated_at` | Sort field: `created_at`, `updated_at`, `last_edited_at`, `title` |
| `order` | `desc` | Sort order: `asc` or `desc` |
| `server_id` | *(all)* | Filter: omit for all, `personal` for personal files, or a server ID |

```bash
curl https://api.mila.gg/v1/slides \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `list_slides`

Parameters: `limit`, `offset`, `sort`, `order`, `server_id` (all optional).

The list response does not include slide `data` -- use the get endpoint for full slide content.

---

## Get Slide Presentation

**REST API:**

```
GET /v1/slides/:id
```

Returns the presentation including the `data` array with all slides.

```bash
curl https://api.mila.gg/v1/slides/pR7nW4kL2x \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `get_slide_presentation`

Parameters: `id` (required, string).

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "pR7nW4kL2x",
    "title": "Product Launch",
    "data": [
      {
        "html": "<div style=\"display:flex;align-items:center;justify-content:center;height:100%\"><h1 style=\"font-size:48px\">Welcome</h1></div>",
        "background": "#ffffff",
        "notes": "Opening slide"
      },
      {
        "html": "<div style=\"padding:60px\"><h2>Key Points</h2><ul><li>First</li><li>Second</li></ul></div>",
        "background": "#f8fafc",
        "notes": ""
      }
    ],
    "theme": "default",
    "aspectRatio": "16:9",
    "server_id": null,
    "created_at": "2026-02-26T...",
    "updated_at": "2026-02-26T..."
  }
}
```

---

## Create Slide Presentation

**REST API:**

```
POST /v1/slides
```

**Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | Yes | Presentation title |
| `data` | array | No | Array of slide objects |
| `theme` | string | No | Theme name (default: `"default"`) |
| `aspectRatio` | string | No | Aspect ratio (default: `"16:9"`) |
| `server_id` | string or null | No | Server to create in (null = personal files) |

```bash
curl -X POST https://api.mila.gg/v1/slides \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product Launch",
    "data": [
      {
        "html": "<div style=\"display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff\"><h1 style=\"font-size:52px;font-weight:700;margin:0\">Product Launch</h1><p style=\"font-size:24px;opacity:0.9;margin-top:16px\">Q3 2026</p></div>",
        "background": "#667eea",
        "notes": "Welcome everyone to the product launch presentation"
      },
      {
        "html": "<div style=\"padding:60px 80px\"><h2 style=\"font-size:36px;color:#1a1a1a;margin:0 0 32px 0\">What We Built</h2><div style=\"display:flex;gap:32px\"><div style=\"flex:1;padding:24px;background:#f0f4ff;border-radius:12px\"><h3 style=\"font-size:20px;color:#4f46e5;margin:0 0 8px 0\">Feature A</h3><p style=\"font-size:16px;color:#64748b;margin:0\">Description of feature A.</p></div><div style=\"flex:1;padding:24px;background:#f0fdf4;border-radius:12px\"><h3 style=\"font-size:20px;color:#16a34a;margin:0 0 8px 0\">Feature B</h3><p style=\"font-size:16px;color:#64748b;margin:0\">Description of feature B.</p></div></div></div>",
        "background": "#ffffff",
        "notes": "Cover the two main features"
      }
    ],
    "theme": "default",
    "aspectRatio": "16:9"
  }'
```

**MCP tool:** `create_slide_presentation`

Parameters: `title` (required), `data` (optional, array of slide objects), `theme` (optional), `aspectRatio` (optional), `server_id` (optional).

**Slide HTML tips:**

- Use inline styles (no external CSS).
- Use flexbox for centering: `display:flex;align-items:center;justify-content:center;height:100%`
- Use padding for content slides: `padding:60px 80px`
- Common font sizes: 48-52px for titles, 36px for section headings, 20-24px for body text, 16px for details.
- Use `background` field for solid colors, gradients (`linear-gradient(...)`), or images.

---

## Update Slide Presentation

**REST API:**

```
PUT /v1/slides/:id
```

**Body** (all fields optional):

| Field | Type | Description |
|---|---|---|
| `title` | string | New title |
| `data` | array | Full replacement array of slide objects |
| `theme` | string | New theme |
| `aspectRatio` | string | New aspect ratio |

Updating `data` replaces the entire slide array. To modify a single slide, first GET the presentation, update the specific slide in the array, then PUT the full array back. To add slides without replacing, use the append endpoint.

```bash
curl -X PUT https://api.mila.gg/v1/slides/pR7nW4kL2x \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Presentation Title"}'
```

**MCP tool:** `update_slide_presentation`

Parameters: `id` (required), `title` (optional), `data` (optional), `theme` (optional), `aspectRatio` (optional).

---

## Append Slides

**REST API:**

```
POST /v1/slides/:id/slides
```

Add one or more slides to an existing presentation without replacing the entire slide array.

**Body -- single slide:**

```json
{
  "slide": {
    "html": "<div style=\"display:flex;align-items:center;justify-content:center;height:100%\"><h1 style=\"font-size:48px\">Thank You</h1></div>",
    "background": "#1a1a2e",
    "notes": "Closing slide"
  }
}
```

**Body -- multiple slides:**

```json
{
  "slides": [
    {
      "html": "<div style=\"padding:60px\"><h2>Slide A</h2></div>",
      "background": "#ffffff",
      "notes": ""
    },
    {
      "html": "<div style=\"padding:60px\"><h2>Slide B</h2></div>",
      "background": "#f8fafc",
      "notes": ""
    }
  ]
}
```

**Body fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `slide` | object | One of `slide` or `slides` | A single slide object to append |
| `slides` | array | One of `slide` or `slides` | An array of slide objects to append |
| `position` | number | No | Insert at this 0-based index. Omit to append at the end. |

Each slide object must have an `html` field. `background` defaults to `"#ffffff"` and `notes` defaults to `""` if omitted.

```bash
# Append a slide at the end
curl -X POST https://api.mila.gg/v1/slides/pR7nW4kL2x/slides \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "slide": {
      "html": "<div style=\"display:flex;align-items:center;justify-content:center;height:100%\"><h1 style=\"font-size:48px\">Thank You</h1></div>",
      "background": "#1a1a2e",
      "notes": "Closing slide"
    }
  }'

# Insert a slide at position 1 (after the first slide)
curl -X POST https://api.mila.gg/v1/slides/pR7nW4kL2x/slides \
  -H "Authorization: Bearer mila_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "slide": {
      "html": "<div style=\"padding:60px\"><h2 style=\"font-size:36px\">Agenda</h2><ol style=\"font-size:24px\"><li>Introduction</li><li>Demo</li><li>Q&A</li></ol></div>",
      "background": "#ffffff",
      "notes": ""
    },
    "position": 1
  }'
```

**MCP tool:** `append_slides`

Parameters: `id` (required), `slides` (optional, array of slide objects), `slide` (optional, single slide object), `position` (optional, 0-based index).

The response returns the full updated presentation including all slides.

---

## Delete Slide Presentation

**REST API:**

```
DELETE /v1/slides/:id
```

Permanently deletes the presentation and all its slides.

```bash
curl -X DELETE https://api.mila.gg/v1/slides/pR7nW4kL2x \
  -H "Authorization: Bearer mila_sk_your_key_here"
```

**MCP tool:** `delete_slide_presentation`

Parameters: `id` (required).
