# Scenes & Templates

## Scenes
A Scene is the foundation of your PlayCanvas application. It defines the 3D world that users will experience, containing all the entities, components and settings that make up your game or interactive experience.
## What's in a Scene?
Every scene contains:
- **Entities** — The objects in your scene, organized in a hierarchy. Entities can represent characters, props, lights, cameras or any other element.
- **Components** — The building blocks that give entities their behavior and appearance. Components handle rendering, physics, audio, user interface and more.
- **Scene Settings** — Global properties that affect the entire scene, such as physics gravity, ambient lighting, fog and skybox.
## Topics
| Topic | Description |
|-------|-------------|
| **Managing Scenes** | Create, open, duplicate and delete scenes in your project. |
| **Components** | Learn about the different component types you can add to entities. |
| **Loading Scenes** | Load scenes dynamically at runtime in your application. |
## Scenes Components
A component encapsulates functionality that can be added to or removed from entities. For example, a component might enable an entity to play sound, render a 3D model or run a script.
Components can be added via the Editor or the Engine API. Properties are shown in the Inspector.
## Component Inspector
Each component panel has:
- **Collapse/Expand** — Arrow toggle
- **Component Icon** — Identifies type
- **Enable Toggle** — Disabled components don't run or render
- **Help** — Opens documentation
- **Actions Menu (cog)** — Copy, Paste, Delete options
## Component Types
| Component | Description |
|-----------|-------------|
| **Anim** | State graph and animations on an entity hierarchy |
| **Audio Listener** | Location of the listener for 3D audio |
| **Button** | User interface button |
| **Camera** | Renders the scene from entity location |
| **Collision** | Assigns a collision volume |
| **Element** | UI text or image element |
| **GSplat** | Renders 3D Gaussian Splat |
| **Layout Child** | Overrides Layout Group properties |
| **Layout Group** | Auto-positions child UI elements |
| **Light** | Dynamic light source |
| **Particle System** | Particle effects |
| **Rigid Body** | Adds entity to physics simulation |
| **Render** | Renders primitive or asset |
| **Screen** | UI area and rendering |
| **Script** | Runs JavaScript for custom behavior |
| **Scrollbar** | Scrolling control for Scroll View |
| **Scroll View** | Scrollable UI area |
| **Sound** | Plays audio assets |
| **Sprite** | Renders 2D graphics |
### Deprecated Components
| Component | Description |
|-----------|-------------|
| **Animation** (deprecated) | Animations on model component entity |
| **Model** (deprecated) | Renders 3D model — use Render component instead |
## Scenes Managing Scenes
The Scenes dialog manages all scenes in your project.
## Opening the Dialog
- **Menu:** Click PlayCanvas logo (top-left) → Scenes
- **Scene Name:** Click the current scene name in the viewport toolbar
## Dialog Overview
- **Filter** — Search scenes by name
- **Scene List** — Alphabetical, showing name and last modified date
- **Current Scene** — Highlighted with selectable (copyable) name
## Actions
| Action | Description |
|--------|-------------|
| **Open Scene** | Click any scene in the list |
| **Create** | Click + ADD NEW SCENE → enter name → Enter |
| **Duplicate** | Dropdown → Duplicate Scene (auto-named with increment) |
| **Delete** | Dropdown → Delete Scene (permanent after confirmation) |
| **Item History** | Dropdown → version control history |
| **Open in New Tab** | Dropdown → opens scene in new browser tab |
## Scenes Loading Scenes
This page covers how to load scenes programmatically. Two main approaches: changing scenes completely and loading additively.
## Changing Scenes Completely
Most common approach — each scene is a self-contained part of the game (title screen, level 1, level 2, etc).
```javascript
this.app.scenes.changeScene('Some Scene Name');
```
If scene data is not already loaded, this function:
1. Makes an async network request for scene data
2. Destroys all children from the application root
3. Calls `loadSceneSettings` (now synchronous)
4. Calls `loadSceneHierarchy` (now synchronous)
With callback:
```javascript
this.app.scenes.changeScene('Some Scene Name', (err, loadedSceneRootEntity) => {
    if (err) console.error(err);
});
```
**Preload for instant switching:** Call `loadSceneData` ahead of time to avoid async network delay.
## Loading Scenes Additively
Load multiple scene hierarchies without destroying the old one. Common uses: splitting large worlds, global managers.
```javascript
const sceneItem = this.app.scenes.find('Some Scene Name');
this.app.scenes.loadSceneHierarchy(sceneItem, (err, loadedSceneRootEntity) => {
    if (err) console.error(err);
});
```
⚠️ Multiple instances of the same scene **cannot** be loaded at once (GUID conflicts). Use Templates for multiple instances.
## Destroying Old Scenes
**Approach 1 — Destroy first (blank screen gap):**
```javascript
const rootChildren = this.app.root.children;
while(rootChildren.length > 0) rootChildren[0].destroy();
this.app.scenes.loadSceneHierarchy(sceneItem, callback);
```
**Approach 2 — Destroy old after new loads (both in memory briefly):**
```javascript
this.app.scenes.loadSceneHierarchy(sceneItem, (err, root) => {
    oldSceneRootEntity.destroy();
});
```
## Managing Assets Across Scenes
Assets and scenes are separate — load them separately. **Recommended:** Tag assets with scene name, load tagged assets first, then load the scene.
## Templates
Templates (prefabs) speed up development with reusable Entity hierarchies. Changes to a Template Asset propagate to all instances.
## Creating Templates
Right-click an Entity → **Template → New Template**. Creates a Template Asset; the entity becomes an instance.
## Adding to Scene
Drag-and-drop a Template Asset into the scene, or right-click → **Template → Add Instance** and select the Template Asset.
## Overrides
Changes to a Template instance generate overrides:
| Type | Description |
|------|-------------|
| **Field override** | A field value differs from the Template Asset |
| **New Entity** | Entity added to the instance, not in Template |
| **Deleted Entity** | Entity removed from the instance |
- **Apply:** Hover colored label → APPLY, or Apply All / Template → Apply To Template
- **Revert:** Click REVERT on individual fields, or Revert All
## Runtime Instantiation
```javascript
const templateAsset = this.app.assets.get(templateAssetId);
const instance = templateAsset.resource.instantiate();
this.app.root.addChild(instance);
```
