# Live Model Metadata

The single source of truth for available models, parameter definitions, defaults, options, and field descriptions is:

`GET https://api.myreels.ai/api/v1/models/api`

Verified on March 18, 2026:

- currently accessible without `Authorization`
- currently does not require `VITE_API_KEY`

If your runtime can access this endpoint, prefer the live response over any static model list.

### Cost Display Rule

Use `estimatedCost` as the final user-facing cost field.

- display field: `estimatedCost`
- display unit: `points`

### Quick Request

```bash
curl -s "https://api.myreels.ai/api/v1/models/api"
```

### Minimal JavaScript Example

```typescript
const res = await fetch('https://api.myreels.ai/api/v1/models/api');
if (!res.ok) throw new Error(`Load models failed: HTTP ${res.status}`);

const payload = await res.json();
for (const item of payload?.data?.items ?? []) {
  console.log(item.modelName, item.name, item.tags, item.estimatedCost, 'points');
}
```

### Minimal Python Example

```python
import requests

r = requests.get("https://api.myreels.ai/api/v1/models/api")
r.raise_for_status()
for item in r.json().get("data", {}).get("items", []):
    print(
        item.get("modelName"),
        item.get("name"),
        item.get("tags"),
        item.get("estimatedCost"),
        "points",
    )
```

### Important Top-Level Fields

- `modelName`
  - the real identifier used in `POST /generation/:modelName`
- `name`
  - display name
- `tags`
  - capability tags such as `t2i`, `i2i`, `i2e`, `t2v`, `i2v`, `t2a`, `m2a`
- `description`
  - model-level description and usage notes
- `estimatedCost`
  - estimated display points
- `displayConfig.estimatedTime`
  - estimated generation time
- `estimatedPoints`
  - optional backend-provided points field; prefer `estimatedCost` for public display
- `userInputSchema`
  - full parameter schema for this model

### How To Read `userInputSchema`

Each entry in `userInputSchema` is a request parameter. These fields matter most:

- `type`
- `label`
- `description`
- `required`
- `default` / `defaultValue`
- `options`
- `min` / `max` / `step`
- `placeholder`

When mapping natural-language instructions to parameters, prioritize `label` and `description`.

Example:

- user says: "stronger motion"
- live schema may show:
  - `strength.label = "Motion Strength"` or an equivalent localized label
  - `strength.description` explains that larger values increase motion freedom

Without the live description, agents can easily map the request incorrectly.

### Recommended Selection Flow

1. Call `GET /api/v1/models/api`.
2. Filter models by `tags`.
3. Inspect `name`, `description`, `estimatedCost`, and `estimatedTime`.
4. Read `userInputSchema`.
5. Build the request body from `label`, `description`, `default`, and `options`.

### Polling Guidance

- image generation / image editing: every 10 seconds
- video generation: every 30 seconds to 1 minute

### Fallback

If your runtime cannot access `api.myreels.ai`, use the rest of the local reference docs only as a fallback. When live access is available, the live schema should take priority.
