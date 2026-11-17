---
name: store-media
description: >-
  Put screenshots, app preview videos, and creative assets (product page
  headers, search results art, in-app event cards) on an iOS app's App Store
  pages through Apple's App Asset Library, via MetaRun: upload each file
  once, place it on the listing, custom product pages, in-app events, or
  product page tests, order it, verify it. Trigger phrases: "upload these
  screenshots", "add an app preview", "iPhone Duo screenshots", "product page
  header", "event card image", "asset library", "swap screenshot 3", "put
  the new screenshots on the store".
metadata:
  openclaw:
    homepage: https://metarun.dev/agents
    primaryEnv: METARUN_TOKEN
    envVars:
      - name: METARUN_TOKEN
        required: false
        description: MetaRun personal access token (Settings, MCP). Not needed after `npx metarun login`, which stores it in ~/.metarun/config.json.
    requires:
      anyBins:
        - npx
---

# Store media: upload once, place anywhere

You are managing App Store media through MetaRun. Apple's App Asset Library
(App Store Connect API 4.5.1) replaced per-surface screenshot sets: a file is
uploaded ONCE into the app's library, then a placement puts it in one slot of
one surface. The same file can back many placements.

## Ground rules

- Tools run over MetaRun's MCP server or `npx metarun run <tool> '<json>'`.
  Fetch any schema you have not used this session: `npx metarun tools
  <tool-name> --json`. Never invent parameters.
- **Placement groups are runtime ids, never guesses.** Device families
  (`IPHONE_DUO_PROFILE`, a 6.9-inch iPhone group, an iPad group...) come from
  `apple_get_asset_catalog`, and Apple adds new ones without an API change.
- Every write is a preview/apply pair with a `confirmToken`. Show the user
  what each preview returned before applying.
- A category is fixed at upload: `APP_SCREENSHOTS_AND_PREVIEWS` for
  screenshots and app previews, `CREATIVE_ASSETS` for headers, search
  results and event art. Pick it from where the file will go.

## The mission

### 1. Learn the rules for the target slot

- `apple_list_apps` -> resolve the bundle id.
- `apple_get_asset_catalog` (narrow it with `surface` and `placementType`)
  -> which placement types the surface takes, each group's exact pixel
  sizes, formats, video duration/frame rate/audio rules, and the per-group
  limit (an App Store version holds 10 screenshots, 3 previews, 1 header).
- `apple_list_asset_surfaces` -> the editable version, custom product pages,
  in-app events, and product page test treatments, each with its
  localization ids and whether its parent is editable. Placements can only
  change while the parent is editable; a version needs to be in Prepare for
  Submission (create one with the release tools if the user agrees).

### 2. Upload

- The file needs an https URL. For a file on the user's machine (an image
  or a video up to 500 MB): `studio_create_media_upload` (its content type
  and byte size) -> run the returned `curl` to PUT the bytes ->
  `studio_finalize_media_upload` -> pass its `sourceUrl` on. The bytes go
  straight to storage, never through the conversation.
- `apple_preview_upload_library_asset` -> checks the file's real type and,
  for images, its pixel size against the catalog. Then
  `apple_apply_upload_library_asset`; its `createdId` is the asset id.
- Videos are judged only after processing: read the result back with
  `apple_get_library_asset` (state `PREPARE_FOR_SUBMISSION` = ready, `FAILED`
  carries Apple's reason) before placing. A video's still frame can be set
  later with `apple_preview_update_library_asset` (`previewFrameTimeCode`).

### 3. Place and order

- `apple_preview_place_library_asset` with the asset, `placementType`,
  `placementGroup`, and the surface (`localizationId`, or just `locale` for
  the editable version) -> `apple_apply_place_library_asset`.
- Apple appends: after placing several, set the order with
  `apple_preview_reorder_asset_placements` (every placement in the slot, in
  order; ids from `apple_list_asset_placements`) ->
  `apple_apply_reorder_asset_placements`. In-app event slots hold one asset
  and do not reorder.
- To change one image in place ("swap screenshot 3"):
  `apple_preview_replace_asset_placement` ->
  `apple_apply_replace_asset_placement`. Placements are immutable; this op
  removes, re-creates, and restores the position for you.

### 4. Clean up when asked

- Take something off a surface: `apple_preview_remove_asset_placement` ->
  `apple_apply_remove_asset_placement` (the file stays in the library).
- Delete a file: `apple_preview_delete_library_asset` ->
  `apple_apply_delete_library_asset`. Apple refuses to delete a placed
  asset; set `removePlacements` only when the user agreed to lose them.
- Rename or archive (approved assets only):
  `apple_preview_update_library_asset` -> `apple_apply_update_library_asset`.

### 5. Verify and report

- `apple_list_asset_placements` for each surface and language you touched:
  name what each slot now shows, in order, and each placement's state.
- `apple_get_asset_library` lists everything in the library with its state
  and how many placements use it.
- Placements travel through App Review with their parent: say so if the
  version still needs submitting.

## Beyond this mission

Classic screenshot sets (`apple_list_screenshots` and its upload/delete/
reorder pairs) still work for plain screenshots; the library is required
for app preview videos, creative assets, and iPhone Duo. Discover the rest
with `npx metarun tools <filter>`.
