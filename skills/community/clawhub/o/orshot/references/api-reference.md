## API Reference

### 1. Render from Studio Template

Generate images/PDFs/videos from templates designed in Orshot Studio.

**POST** `https://api.orshot.com/v1/studio/render`

```js
await fetch("https://api.orshot.com/v1/studio/render", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer $ORSHOT_API_KEY",
  },
  body: JSON.stringify({
    templateId: 123, // Integer - your studio template ID
    modifications: {
      title: "Hello World",
      imageUrl: "https://example.com/photo.jpg",
      canvasBackgroundColor: "#eff2fa",
    },
    response: {
      type: "base64", // "base64" | "url" | "binary"
      format: "png", // "png" | "webp" | "jpg" | "pdf" | "mp4" | "webm" | "gif"
      scale: 1, // 1 = original size, 2 = double
      includePages: [1, 3], // optional – only for multi-page templates
      fileName: "my-render", // optional – custom filename (without extension)
    },
    pdfOptions: {
      // optional – only when format is "pdf"
      margin: "20px",
      rangeFrom: 1,
      rangeTo: 2,
      colorMode: "rgb", // "rgb" or "cmyk"
      dpi: 300,
    },
  }),
});
```

**Response (single page):**
```json
{
  "data": {
    "content": "data:image/png;base64,iVBORw0.....",
    "format": "png",
    "type": "base64",
    "responseTime": 325.22
  }
}
```

**Response (multi-page/carousel):**
```json
{
  "data": [
    { "page": 1, "content": "https://storage.orshot.com/.../image1.png" },
    { "page": 2, "content": "https://storage.orshot.com/.../image2.png" }
  ],
  "format": "png",
  "type": "url",
  "responseTime": 3166.01,
  "totalPages": 2,
  "renderedPages": 2
}
```

### 2. Render from Utility Template

Generate renders from Orshot's pre-built utility templates (e.g., website screenshots, tweet images).

**POST** `https://api.orshot.com/v1/generate/{renderType}`

- `renderType`: `images` or `pdfs`

```js
await fetch("https://api.orshot.com/v1/generate/images", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer $ORSHOT_API_KEY",
  },
  body: JSON.stringify({
    templateId: "website-screenshot", // String ID for utility templates
    response: {
      format: "png",
      type: "base64",
    },
    modifications: {
      websiteUrl: "https://example.com",
      fullCapture: false,
      delay: 500,
      width: 1200,
      height: 1000,
    },
  }),
});
```

### 3. Generate Signed URL

Create publicly accessible render URLs without exposing your API key.

**POST** `https://api.orshot.com/v1/signed-url/create`

```js
await fetch("https://api.orshot.com/v1/signed-url/create", {
  method: "POST",
  headers: {
    Authorization: "Bearer $ORSHOT_API_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    templateId: "website-screenshot",
    expiresAt: 1744550160505, // UNIX timestamp, or null for no expiry
    renderType: "images",
    modifications: {
      websiteUrl: "https://example.com",
    },
  }),
});
```

### 4. List Studio Templates

**GET** `https://api.orshot.com/v1/studio/templates/all?page=1&limit=10`

Response includes `data` array of templates and `pagination` object with `page`, `limit`, `total`, `totalPages`.

### 5. Get Studio Template

**GET** `https://api.orshot.com/v1/studio/templates/:templateId`

Returns the template metadata including available `modifications`.

### 6. Delete Studio Template

**DELETE** `https://api.orshot.com/v1/studio/templates/:templateId`

Not reversible. Confirm the template name and id with the user before calling it.

### 7. Duplicate Studio Template

**POST** `https://api.orshot.com/v1/studio/templates/:templateId/duplicate`

### 8. Get Profile & Workspaces

**GET** `https://api.orshot.com/v1/me`

Returns your profile and the workspaces your API key or OAuth token can access, including plan info and credit usage.

### 9. Brand Assets API

Brand assets are grouped by type, **images**, **colors**, **fonts**, **videos**, **audio**: each with its own routes under `/v1/brand-assets/{type}/…`.

#### Images
- **Get:** `GET https://api.orshot.com/v1/brand-assets/images/get`
- **Upload:** `POST https://api.orshot.com/v1/brand-assets/images/add`: `multipart/form-data` with a `file` field
- **Update tags:** `PATCH https://api.orshot.com/v1/brand-assets/images/update/:id`
- **Delete:** `DELETE https://api.orshot.com/v1/brand-assets/images/delete/:id`

#### Colors
- **Get:** `GET https://api.orshot.com/v1/brand-assets/colors/get`
- **Add:** `POST https://api.orshot.com/v1/brand-assets/colors/add`: body `{ type: "hex" | "gradient", value, tags? }`
- **Update tags:** `PATCH https://api.orshot.com/v1/brand-assets/colors/update/:id`
- **Delete:** `DELETE https://api.orshot.com/v1/brand-assets/colors/delete/:id`

#### Fonts / Videos / Audio
Same shape, swap the type segment (`fonts`, `videos`, `audio`):
- **Get:** `GET /v1/brand-assets/{type}/get`
- **Upload:** `POST /v1/brand-assets/{type}/add` (`multipart/form-data`, `file` field)
- **Update tags:** `PATCH /v1/brand-assets/{type}/update/:id`
- **Delete:** `DELETE /v1/brand-assets/{type}/delete/:id`

#### Search
- **Search assets:** `GET https://api.orshot.com/v1/brand-assets/search`

Use an uploaded asset in a render by passing its hosted URL as an image/video modification value.

The `delete` routes remove the asset for the whole workspace and cannot be undone. Name the asset and ask before deleting.

### 10. Enterprise API Endpoints

These endpoints require an Enterprise plan.

#### Create Studio Template
**POST** `https://api.orshot.com/v1/studio/templates/create`

```js
{
  name: "Product Banner",        // required, max 255 chars
  description: "Banner template", // optional
  canvas_width: 1200,             // required, 1-5000
  canvas_height: 628,             // required, 1-5000
  pages_data: [...]               // optional - array of page objects with elements
}
```

#### Bulk Create Studio Templates
**POST** `https://api.orshot.com/v1/studio/templates/bulk-create`
Create multiple templates at once via CSV or JSON.

#### Update Template
**PATCH** `https://api.orshot.com/v1/studio/templates/:templateId`
Update template name and description.

#### Update Template Modifications
**PATCH** `https://api.orshot.com/v1/studio/templates/:templateId/update-modifications`
Update text and image content in template layers.

#### Generate Template Variants
**POST** `https://api.orshot.com/v1/studio/templates/:templateId/generate-variants`
Generate multiple size variants of a template using AI.

### 11. Dynamic URLs

Generate images directly from URL parameters:

```
https://api.orshot.com/v1/studio/dynamic-url/my-image?title=Hello%20World&title.fontSize=48px&title.color=%23ff0000
```
URL-encode special characters (e.g., `#` → `%23`).

### 12. Template Folders & Sharing

Organize studio templates into folders and share them:

- **List folders:** `GET https://api.orshot.com/v1/studio/folders`
- **Create folder:** `POST https://api.orshot.com/v1/studio/folders`
- **Update folder:** `PATCH https://api.orshot.com/v1/studio/folders/:folderId`
- **Delete folder:** `DELETE https://api.orshot.com/v1/studio/folders/:folderId`
- **Move template into folder:** `PATCH https://api.orshot.com/v1/studio/templates/:templateId/folder`
- **Get template sharing:** `GET https://api.orshot.com/v1/studio/templates/:templateId/share`
- **Update template sharing:** `POST https://api.orshot.com/v1/studio/templates/:templateId/share`

### 13. Workflows API

Workflows automate multi-step pipelines (trigger → fetch data → render → publish/deliver). Available to first-party clients (like the Orshot MCP server) and Enterprise workspaces.

- **List workflows:** `GET https://api.orshot.com/v1/workflows`
- **Create workflow:** `POST https://api.orshot.com/v1/workflows`
- **Get workflow:** `GET https://api.orshot.com/v1/workflows/:id`
- **Update workflow:** `PATCH https://api.orshot.com/v1/workflows/:id`
- **Delete workflow:** `DELETE https://api.orshot.com/v1/workflows/:id` (confirm first; not reversible)
- **Run workflow:** `POST https://api.orshot.com/v1/workflows/:id/run` (a run spends credits and can deliver or post; confirm with the user first)
- **List runs:** `GET https://api.orshot.com/v1/workflows/:id/runs`
- **Get a run:** `GET https://api.orshot.com/v1/workflows/:id/runs/:runId`
- **Validate a workflow:** `POST https://api.orshot.com/v1/workflows/validate`
- **List available nodes:** `GET https://api.orshot.com/v1/workflows/nodes`
- **Get/update sharing:** `GET` / `POST https://api.orshot.com/v1/workflows/:id/share`

