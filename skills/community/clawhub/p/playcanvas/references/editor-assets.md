# Editor Assets

## Assets
The PlayCanvas Editor provides a complete asset management system for your project. This section covers how to work with assets in the Editor, including importing, organizing, and configuring them.
## Overview
Assets in the Editor are managed through the Assets Panel, which provides a visual interface for:
- Organizing assets into folders
- Uploading new assets via drag-and-drop
- Searching and filtering assets
- Inspecting and editing asset properties
- Copying assets between projects
When you upload a file, the Editor runs it through the import pipeline to convert and optimize it for use in your application. The resulting asset can then be configured using the appropriate asset inspector.

### Uploading & Importing
Drag and drop asset files into the Asset Panel. A progress bar appears; when it disappears, the asset is ready. **File size limit:** 340MB. Re-upload the same filename to update an existing asset.
**Migrating from JSON to GLB:** For projects created before Oct 14, 2020: Project Settings → Asset Tasks → tick **Convert to GLB**, reimport files, replace JSON asset references with new GLB assets.
### Asset Store
Click **ASSET STORE** in the Assets Panel to browse free assets (3D models, fonts, scripts, sky boxes, textures).
| Store | Description |
|-------|-------------|
| **PLAYCANVAS** | Curated by PlayCanvas: 3D models, fonts, scripts, sky boxes, templates, textures |
| **SKETCHFAB** | 3D models curated by Sketchfab |
| **MY ASSETS** | Assets you've imported (closed beta) |
## Assets Asset Panel
The Assets Panel manages all of the Assets that are available in your project. From here, you can create, upload, delete, inspect and edit any Asset.
## Folder Hierarchy
The folder panel organizes assets into a tree of folders.
- **Create folder:** Add Asset (+) → Folder, or right-click → New Asset > Folder
- **Rename:** Double-click folder, edit Name in Inspector
- **Delete:** Double-click folder → Delete, or right-click → Delete
- **Reorganize:** Drag-and-drop folders into each other
## Creating and Uploading Assets
- **Upload:** Drag files from your file system into the Assets Panel
- **Create:** Use the Add Asset (+) icon for certain asset types
- **Delete:** Select assets, click Delete Asset icon
## Inspecting Assets
Select any asset's thumbnail to see its details in the Inspector.
## Filtering and Searching
**Filter dropdown:** Filter by asset type.
**Search box:** Global search with these capabilities:
- **ID search** — Type an asset ID to find it exactly
- **RegExp** — Start with `*` then write regex (e.g., `*.*` for all)
- **Tags** — Search in brackets: `[level-1]` (OR), `[[level-1, monster]]` (AND), `[[level-1, monster], [level-2, monster]]` (compound)
## Drag and Drop
- Drag assets between folders (multi-select with Ctrl+A)
- Drag to Inspector slots (component attributes, script attributes)
- Drag models into Viewport → creates new entity with model component
- Drag materials onto meshes in Viewport → preview/swaps material
- Drag cubemaps onto Viewport background → sets scene skybox
## Copy and Paste Between Projects
Select → right-click Copy (or Ctrl/Cmd+C), then right-click Paste (or Ctrl/Cmd+V) in target project. Dependencies are copied automatically. Hold Shift when pasting to keep folder structure.
## Checking References
A small dot on a thumbnail indicates no detected references. Right-click → References to see where an asset is used.
## Assets Import Pipeline
Some assets are uploaded in source format and need to be converted into a "target" format before they can be used in a game at runtime. This process is called Importing. For example, a 3D model can be uploaded as an FBX file, but must be converted into a PlayCanvas compatible model file.
Some assets don't need to be imported (e.g., PNG images can be used as textures immediately).
## Asset Tasks
When a source asset is uploaded, PlayCanvas starts an Asset Task to perform the import process on the server. Various options are available to tune import pipeline behavior.
**Search related assets:** When re-uploading a source file:
- Enabled → updates target assets regardless of location
- Disabled → only looks for target assets in the same folder as the source
**Assets default to preload:** New assets auto-set to preload (except JavaScript scripts, which always preload).
## Texture Import Settings
- **Texture POT (Power of Two)** — Converts non-power-of-two textures to nearest POT resolution
- **Create Atlases** — Images imported as texture atlas instead of normal texture (useful for spritesheets/UI)
## Model Import Settings
- **Preserve material mappings** — Try to preserve material assignments on reimport
- **Overwrite Models** — Whether to overwrite target model on reimport (default: yes)
- **Overwrite Animations** — Whether to overwrite animations on reimport (default: yes)
- **Overwrite Materials** — Whether to overwrite materials on reimport (default: no)
- **Overwrite Textures** — Whether to overwrite textures on reimport (default: yes)
- **Convert to GLB** — Import models/animations as GLB instead of deprecated JSON (default: yes)
- **Import Hierarchy** — Creates a template with full model hierarchy as entities
- **Mesh Compression** — Compress mesh data (Draco) to reduce GLB size
- **Create FBX Folder** — Creates a folder for imported assets (render, template, materials)
## Animation Import Settings
Refer to the Animation inspector documentation for animation-specific import details.
## Assets Inspectors
When you select an asset in the Assets Panel, its properties display in the Inspector. Each asset type has configurable properties.
## Common Properties
| Property | Description |
|----------|-------------|
| ID | Unique identifier (use in scripts) |
| Name | Editable display name |
| Tags | Organization and runtime filtering |
| Type | Asset type (read-only) |
| Exclude | Exclude from publish (dev-only assets) |
| Preload | Load at startup vs async/manual |
| Size | File size (read-only) |
| Source | Source asset reference (read-only) |
| Created | Creation date/time (read-only) |
## Script Asset Properties
| Property | Description |
|----------|-------------|
| Loading Order | Manage script load sequence |
| Loading Type | Asset (default), Before Engine, After Engine |
## Asset Store Assets
Store-imported assets show: License (with link), Author (with profile link).
## All Asset Types
| Type | Source Extensions | Runtime | Description |
|------|-------------------|---------|-------------|
| animation | .glb, .fbx | .glb | Animation keyframe data |
| audio | .mp3, .wav, .ogg | .mp3, .wav, .ogg | Sound data |
| binary | .bin | .bin | Binary data |
| bundle | Editor | .tar | Bundled assets |
| css | .css | .css | Stylesheets |
| cubemap | .png, .jpg, .webp, .avif | same | Environment lighting |
| font | .ttf, .woff | .json, .png | Font data |
| gsplat | .ply | .ply | 3D Gaussian Splat |
| html | .html | .html | HTML documents |
| json | .json | .json | JSON documents |
| material | .glb, .fbx | None | Material definitions |
| render | .glb, .fbx | .glb | 3D mesh data |
| script | .js, .mjs | .js, .mjs | Scripts |
| shader | .glsl, .vert, .frag | same | Custom shaders |
| sprite | Editor | None | 2D images |
| template | .glb | None | Entity hierarchy templates |
| text | .txt | .txt | Text documents |
| texture-atlas | .png, .jpg, .webp, .avif | same | Sprite sheet |
| texture | .png, .jpg, .webp, .avif | same | Image data |
| wasm | .wasm | .wasm | WebAssembly modules |
