# Assets

Assets are the building blocks of your PlayCanvas application. They represent all the external resources your application needs, such as 3D models, textures, audio files, and scripts.
## Assets vs Resources
In PlayCanvas, there's an important distinction between **Assets** and **Resources**:
- **Asset** - A record in the asset registry that contains metadata about a resource, including its name, type, tags, and a reference to the underlying resource data. Assets are managed by the [`AssetRegistry`](asset-registry).
- **Resource** - The actual runtime data that gets loaded into memory and used by the engine. For example, a texture asset's resource is the actual image data that can be applied to materials.
When you load an asset, PlayCanvas downloads and parses the underlying file to create the resource. The asset object then holds a reference to this resource via its `resource` property.
```javascript
const asset = this.app.assets.find('my-texture');
asset.ready((asset) => {
    const texture = asset.resource; // The actual Texture object
});
this.app.assets.load(asset);
```
## Asset Lifecycle
Assets go through several stages during the lifetime of your application:
1. **Registry** - Assets are registered in the [`AssetRegistry`](asset-registry), making them discoverable by ID, name, or tags
2. **Loading** - Asset data is downloaded from the server
3. **Ready** - The resource is parsed and available for use
4. **Unloading** - Resources can be unloaded to free memory
For details on controlling when assets load, see [Preloading](preloading) and [Loading and Unloading](loading-unloading).
## Supported Formats
PlayCanvas supports a wide variety of file formats for different asset types. See [Supported Formats](supported-formats) for a complete list.
## Working with Assets
### In the Editor
If you're using the PlayCanvas Editor, see the [Editor Assets Guide](/user-manual/editor/assets/) for information on:
- Importing and organizing assets
- Configuring asset properties
- Using the Asset Store
### Programmatically
For working with assets in code:
- **[Asset Registry](asset-registry)** - Find and manage assets at runtime
- **[Preloading](preloading)** - Control which assets load before your app starts
- **[Loading and Unloading](loading-unloading)** - Dynamically load assets during runtime
## Finding Assets
Looking for 3D models, textures, or audio for your project? See [Finding Assets](finding) for a list of asset marketplaces and resources.
## Asset Registry
The [`AssetRegistry`](https://api.playcanvas.com/engine/classes/AssetRegistry.html) is the central system for managing assets in PlayCanvas. It maintains a collection of all assets available to your application and provides methods to find, load, and manage them.
## Accessing the Registry
The asset registry is available via the application object:
```javascript
const assets = this.app.assets;
```
## Finding Assets
### By ID
Every asset has a unique numeric ID. This is the most reliable way to reference an asset:
```javascript
const asset = this.app.assets.get(123456);
```
### By Name
Find an asset by its name. Returns the first matching asset:
```javascript
const asset = this.app.assets.find('My Texture');
```
Find all assets with a given name:
```javascript
const assets = this.app.assets.findAll('Enemy');
```
### By Tag
Assets can be tagged for easy grouping. Find all assets with a specific tag:
```javascript
const levelAssets = this.app.assets.findByTag('level-1');
```
Find assets matching multiple tags (AND logic):
```javascript
// Assets tagged with BOTH 'level-1' AND 'enemy'
const enemies = this.app.assets.findByTag('level-1', 'enemy');
```
Find assets matching any of several tags (OR logic):
```javascript
// Assets tagged with 'level-1' OR 'level-2'
const assets = this.app.assets.findByTag(['level-1', 'level-2']);
```
## Asset Events
The registry emits events when assets are added, removed, or loaded:
### Registry Events
```javascript
// Asset added to registry
this.app.assets.on('add', (asset) => {
    console.log('Asset added:', asset.name);
});
// Asset removed from registry
this.app.assets.on('remove', (asset) => {
    console.log('Asset removed:', asset.name);
});
// Asset loaded
this.app.assets.on('load', (asset) => {
    console.log('Asset loaded:', asset.name);
});
// Asset failed to load
this.app.assets.on('error', (err, asset) => {
    console.error('Failed to load:', asset.name, err);
});
```
### Individual Asset Events
You can also listen for events on specific assets:
```javascript
const asset = this.app.assets.find('My Texture');
// Called when the asset's resource is ready
asset.on('load', (asset) => {
    console.log('Texture loaded:', asset.resource);
});
// Called if loading fails
asset.on('error', (err, asset) => {
    console.error('Failed:', err);
});
// Called when the asset is removed from the registry
asset.on('remove', (asset) => {
    console.log('Asset removed');
});
// Called when any property changes
asset.on('change', (asset, property, newValue, oldValue) => {
    console.log(`${property} changed from ${oldValue} to ${newValue}`);
});
```
### Using ready()
The `ready()` method is a convenient way to execute code when an asset is loaded. If the asset is already loaded, the callback fires immediately:
```javascript
const asset = this.app.assets.find('My Texture');
asset.ready((asset) => {
    // Asset is guaranteed to be loaded here
    const texture = asset.resource;
    material.diffuseMap = texture;
});
// Make sure to trigger loading if not already loaded
this.app.assets.load(asset);
```
## Adding Assets at Runtime
You can create and add new assets to the registry at runtime:
```javascript
const asset = new pc.Asset('New Texture', 'texture', {
    url: 'path/to/texture.png'
});
this.app.assets.add(asset);
this.app.assets.load(asset);
```