# App Embedding Quickref (Jira Cloud, ADF)

This quick reference explains generic patterns to embed app-relevant data into Jira issue descriptions or comments via REST API v3 (ADF), plus a concrete example for a Mermaid-diagram app.

---

## 1) Generic: how to embed app data into Jira text bodies

### 1.1 Where apps typically read data from
Most Jira apps integrate via one or more of these carriers:
1. issue description (ADF)
2. issue comments (ADF)
3. custom fields (text or textarea; textarea is often ADF)
4. issue entity properties (structured JSON, not normally visible in the UI)
5. attachments (files referenced from description/comments or consumed directly by the app)

If your integration goal is “put structured data somewhere apps can parse”, ADF code blocks are the most universal option for descriptions and comments.

---

### 1.2 Recommended pattern: marker + ADF codeBlock
Embed a stable marker line so parsers and humans can find the payload reliably.

Recommended human-readable pattern:
- paragraph: short label + identifier
- code block: the payload (JSON, YAML, Mermaid, etc.)

#### ADF snippet: marker paragraph + JSON code block
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "APPDATA: my-app-key v1 (do not edit marker)" }
      ]
    },
    {
      "type": "codeBlock",
      "attrs": { "language": "json" },
      "content": [
        {
          "type": "text",
          "text": "{\n  \"schema\": 1,\n  \"feature\": \"triage\",\n  \"settings\": { \"mode\": \"auto\" }\n}\n"
        }
      ]
    }
  ]
}
```

Notes:
- Keep the marker line consistent, for example `APPDATA: <appKey> v<schema>`.
- Put the entire machine-readable payload into the `codeBlock`.
- Avoid inline JSON inside paragraphs.

---

### 1.3 Common ADF carriers you will use often
- `paragraph` for headings and labels
- `codeBlock` for machine-readable payloads
- `panel` or `expand` when you want to hide details but keep them in the document
- `inlineCard` for smart-link style references to an external artifact

#### ADF snippet: inlineCard to an external artifact
```json
{
  "type": "inlineCard",
  "attrs": { "url": "https://example.invalid/artifacts/123" }
}
```

---

### 1.4 Plain text to ADF rules for openClaw automation
When the user provides plain text but you need reliable formatting:
- convert plain text into ADF
- convert multiple paragraphs into multiple `paragraph` nodes
- convert machine-readable payloads into a `codeBlock`
- do not assume Markdown will render as intended in Jira rich-text fields

---

### 1.5 Alternative pattern: issue entity properties
If you need structured JSON that should not clutter the description or comments, store it via:
- `PUT /rest/api/3/issue/{issueKey}/properties/{propertyKey}`

Pros:
- clean UI
- structured JSON

Cons:
- not visible unless the app reads it or you surface it elsewhere

Use this when:
- you control the consuming automation or app, or
- the vendor documents a specific property key contract

---

## 2) Concrete example: ContentCraft — Mermaid Diagrams for Jira

### 2.1 UI-oriented usage
This kind of app is commonly used by:
- opening an issue
- enabling the Diagrams panel
- creating or editing Mermaid diagrams in that panel

If you want diagrams rendered by the app, the polished rendering often happens in the app UI, not in the raw Jira description or comment.

---

### 2.2 openClaw-friendly approach: keep Mermaid source in the issue body
Even if the app renders diagrams in a panel, it is useful to keep Mermaid source in the issue description or a comment as a portable source of truth.

Recommended embedding pattern:
- paragraph marker: `DIAGRAM: mermaid (ContentCraft)`
- code block with language `mermaid`

#### ADF payload: comment body containing Mermaid source
Use this as the `body` for:
- `POST /rest/api/3/issue/{issueKey}/comment`

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "DIAGRAM: mermaid (ContentCraft) — edit in Diagrams panel or update this block" }
      ]
    },
    {
      "type": "codeBlock",
      "attrs": { "language": "mermaid" },
      "content": [
        {
          "type": "text",
          "text": "graph TD\n  A[User] --> B[Jira Issue]\n  B --> C[Diagrams Panel]\n  C --> D[Rendered SVG]\n"
        }
      ]
    }
  ]
}
```

Why this helps:
- humans can read and edit Mermaid quickly
- the source remains searchable in Jira
- the diagram source stays close to ticket discussion

---

### 2.3 Practical two-track workflow
1. openClaw writes or updates Mermaid source in the description or a comment as ADF `codeBlock` with `language=mermaid`
2. the team uses the app’s Diagrams panel to render, inspect, and present the diagram

---

### 2.4 Mermaid usage guidance
- use standard Mermaid syntax
- keep diagrams small and composable
- prefer multiple focused diagrams instead of one oversized graph

---

## 3) Recommended helper routine for the skill
It is useful to add one plain-text-to-ADF helper routine to the skill so agents consistently generate:
- paragraph nodes for human text
- codeBlock nodes for payloads
- stable markers for app-owned content blocks
