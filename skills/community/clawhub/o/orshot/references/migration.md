## Moving from another template render API

Swapping the API call is the easy part. Bring the templates over first, then change the call.

### 1. Bring the templates over

Check for an importer before rebuilding anything. Importers run in the Orshot dashboard (New Template dialog), not over MCP or REST, so the user does this step.

| Coming from | Path |
| --- | --- |
| Canva, Figma, Polotno | Importer. Guides: https://orshot.com/docs/importing-templates/index.md |
| Placid | Importer. https://orshot.com/docs/importing-templates/import-from-placid.md |
| Abyssale | Importer that reads designs with the user's Abyssale API key. https://orshot.com/docs/importing-templates/import-from-abyssale.md |
| Bannerbear, Templated | Importer for a template saved from their editor. Guides: https://orshot.com/migrate/from-bannerbear, https://orshot.com/migrate/from-templated |
| Creatomate and anything else | No importer. Rebuild the template, or the user requests a migration at https://orshot.com/migrate |

To rebuild, design it in the studio or with `orshot_create_template_design` (follow the `orshot-design` skill). Mark every layer that changes per render as a parameter with a clear `parameterId`.

### 2. Map the old field names

Other APIs key by layer name or fixed field names; Orshot keys by `parameterId`. Importers usually keep layer names as the keys, but read the real keys before mapping anything:

```
orshot_get_studio_template_modifications   (or GET /v1/studio/templates/:id)
```

Keep a lookup from old names to new keys in the user's code or automation.

### 3. Swap the call

`POST /v1/studio/render` with `Authorization: Bearer $ORSHOT_API_KEY`, `templateId` and a flat `modifications` object. Prefix every content key with `pageN@` on multi-page templates. Style overrides that other APIs put in per-layer objects become dot keys (`"title.fontSize"`). Request shape: https://orshot.com/docs/api-reference/render-from-studio-template.md

### 4. Sync or async

Many render APIs are submit then poll. An Orshot image or PDF render returns the result in the same response, so the polling code can go. Keep a job flow for long video renders (`response.mode: "async"`, https://orshot.com/docs/api-reference/async-render-start.md).

### 5. Check before cutting over

Render one real record through the new call and compare it with the old output. Read the response the way the docs describe it for the template's page count, then switch traffic.
