## Migrating from Another Template-Render API

The API-call swap is the easy part. The real work is recreating the design, because another platform's template JSON cannot be imported:

1. **Recreate the template in Orshot Studio** (or via `POST /v1/studio/templates/create`). Rebuild the layout, then mark every dynamic layer parameterizable with a clear `parameterId`.
2. **Map old field names → Orshot `parameterId`s.** Other APIs key by layer name or by fixed keys such as `image_url`; Orshot keys by `parameterId`. Keep a lookup from old names to new ones.
3. **Swap the API call**: `Authorization: Bearer $ORSHOT_API_KEY` + `POST /v1/studio/render` with `modifications` as a flat object (page-prefixed keys for multi-page templates).
4. **Handle sync vs async.** Many render APIs are submit-then-poll; Orshot image and PDF renders return synchronously, so delete the polling/webhook code and read `data.content` from the response. Long video renders use async render jobs (see above).
5. **Style overrides** that other APIs put in per-layer objects become dot-notation keys here (`"title.fontSize": "48px"`).
6. **Verify the response shape**: single page is an object, multi-page is an array (Common Gotchas #7): before cutting traffic over.

Render URLs on Orshot persist; do not add expiry handling unless you delete renders yourself.

