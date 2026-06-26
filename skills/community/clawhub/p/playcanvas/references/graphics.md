# Graphics

PlayCanvas incorporates an advanced graphics engine that delivers high-performance 3D rendering on the web. The engine provides both [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API) and [WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) support, ensuring compatibility across all modern browsers while offering cutting-edge graphics capabilities.
## Graphics Engine Backends
The PlayCanvas engine supports multiple graphics backends:
* **WebGPU (Beta)** - Next-generation graphics API with reduced driver overhead and compute shader support
* **WebGL 2.0** - Mature and [widely supported](https://caniuse.com/webgl2) across all browsers and devices
* **Null** - For running the engine in headless environments such as Node.
## Key Rendering Features
### Physically Based Rendering (PBR)
* Comprehensive PBR support via metallic/roughness and specular/glossiness workflows
* Energy conservation and physically accurate lighting models
* Support for clearcoat, anisotropy, sheen, and transmission materials
### Advanced Lighting
* **Clustered lighting system** - Efficient handling of hundreds of dynamic lights
* **Directional, point, and spot lights** with configurable shadows and cookies
* **Area lights** - Rectangle, disk, and sphere-shaped light sources for realistic lighting
* **Image-based lighting (IBL)** with HDR environment maps
* **Runtime lightmap generation** for static lighting optimization
### High Dynamic Range (HDR) Rendering
* **Linear workflow** with automatic gamma correction
* **HDR display output** support on compatible devices
* **Advanced tone mapping** operators including ACES, Neutral, and Linear
* **CameraFrame system** for comprehensive post-processing pipeline
### Modern Rendering Pipeline
* **Render passes architecture** enabling advanced effects
* **Multiple render targets (MRT)** support
* **Depth pre-pass** and **temporal anti-aliasing (TAA)**
* **Hardware instancing** for efficient rendering of repeated geometry
* **Static and dynamic batching** to reduce draw calls
### Post-Processing Effects
The CameraFrame system provides a full suite of post-processing effects:
* **HDR Bloom** with physically accurate light bleeding
* **Screen Space Ambient Occlusion (SSAO)**
* **Depth of Field (DoF)** with bokeh effects
* **Temporal Anti-Aliasing (TAA)** for smooth edges
* **Vignette, sepia, brightness/contrast** and color grading
### Advanced Rendering Techniques
* **3D Gaussian Splatting** for photorealistic scene reconstruction
* **Hardware-accelerated particles** for special effects
* **Mesh skinning and morphing** for character animation
* **Procedural geometry generation** with optimized primitives
* **Texture compression** courtesy of Basis Universal
### Custom Shaders
* **Flexible shader system** supporting both GLSL (WebGL) and WGSL (WebGPU)
* **Automatic shader generation** with chunk-based composition
* **Preprocessor support** for shader variants and includes
* **WebGPU compute shaders** for GPU-accelerated computation
The graphics engine is continuously updated to leverage the latest web standards and hardware capabilities, ensuring PlayCanvas applications deliver exceptional visual quality and performance across all platforms.
## Cameras
# Cameras
Cameras are responsible for rendering a scene to the screen. You need at least one camera in your scene to see anything. When you create a new scene in PlayCanvas, it is automatically populated with a single camera (along with a directional light).
## Creating a Camera
In the Editor's 3D View, an unselected camera is represented with the following icon:
To create a new camera, simply create a new entity and add a camera component to it. For convenience, the Editor menu has an item that does this in a single step.
## Orthographic vs Perspective Projection
Cameras can have one of two types of projection: orthographic or perspective. Orthographic cameras define a parallel projection and are often used for 2D or isometric games.
More commonly used is the perspective projection. It more closely mimics how our eyes or cameras work.
## Controlling the Viewport
By default, a camera will render to the full width and height of its render target. However, there are circumstances where you might want to change this behavior. For example, perhaps you are writing a game that has a local multiplayer mode that requires split-screen rendering to show each player's viewpoint.
For 2-player horizontal split screen, you would create two cameras and configure their viewports as follows:
And for vertical split screen, you would configure the viewports as follows:
## Camera Properties
Key camera component properties include:
- **Projection**: Orthographic or Perspective
- **Field of View (FOV)**: The viewing angle (perspective only)
- **Near/Far Clip**: Near and far clipping planes
- **Priority**: Rendering order when multiple cameras exist
- **Clear Color**: Background color when nothing is rendered
- **Clear Depth**: Whether to clear the depth buffer
- **Render Target**: Optional render texture target
- **Layers**: Which render layers to include
- **Culling Mask**: Which entities to render
## Multiple Cameras
You can have multiple cameras in a scene. Common use cases include:
- Split-screen multiplayer
- Minimap rendering
- Picture-in-picture views
- Post-processing effects
- UI camera for overlays
## Lighting
# Lighting
Lighting a scene is the process of calculating the color or shading of a pixel render to the screen based on the material properties of the surface and the light sources that are applied to that material.
In PlayCanvas, lighting can be broadly divided up into two basic categories: dynamic lights and lightmaps.
## Dynamic Lights
Lighting calculations that are performed at runtime are classed as dynamic. Every frame the engine calculates the amount of light falling on a surface from the type, position and properties of Light Entities and uses this to color the material.
### Light Component Types
- **Directional Light**: Simulates light from a far-away source (like the sun). All rays are parallel.
- **Point Light**: Emits light in all directions from a single point. Has a range.
- **Spot Light**: Emits light in a cone shape from a point. Has range, inner and outer cone angles.
### Light Properties
- **Color**: The color of the light
- **Intensity**: How bright the light is
- **Range**: Maximum distance the light reaches (point and spot only)
- **Inner/Outer Cone Angle**: Defines the cone shape (spot only)
- **Cast Shadows**: Whether the light casts shadows
- **Shadow Resolution**: Quality of shadow maps
- **Shadow Distance**: Maximum distance for shadow rendering
## Lightmaps
For lights and geometry that does not move, it is often preferable to determine the lighting information in advance. This information is then saved into lightmap textures which are applied to the surface materials. This method has a very low runtime cost at the expense of having static lighting which can not change and pre-computation times.
There are two methods of creating lightmaps:
### External Lightmap Generation
Many 3D creation tools have lightmap generation included or available as an add-on, including 3DS Max, Maya and Blender. These tools generally generate lightmap textures which can be uploaded as regular assets and added to the Lightmap slot in the standard Physical Material.
### PlayCanvas Runtime Lightmap Generation
The PlayCanvas Engine has built in lightmap generation. This can be used to generate lightmaps automatically just before your game runs. With this method you can use the standard light components, make changes and preview your scene directly in the Editor.
## Shadow Mapping
PlayCanvas uses shadow mapping for dynamic shadow rendering. Key considerations:
- Only directional, spot, and point lights can cast shadows
- Shadow maps have a resolution setting (higher = better quality, more memory)
- Soft shadows use PCF (Percentage Closer Filtering)
- Cascade shadow maps are available for directional lights to improve quality over distance
## Light Baking
Runtime lightmap baking in PlayCanvas:
1. Set up lights with the "Bake" property enabled
2. Mark static geometry as "Lightmapped"
3. Bake lighting via the Editor or programmatically
4. Lightmaps are automatically applied at runtime
## Lighting Lights
## Light Types
| Type | Description | Example |
|------|-------------|---------|
| **Directional** | Light traveling in a single direction — like the Sun | Sunlight |
| **Omni** | Emits in all directions — like a candle | Light bulb |
| **Spot** | Constrained to a cone shape | Flashlight |
## Light Shapes
| Shape | Description | Cost |
|-------|-------------|------|
| **Punctual** | Infinitesimally small point (default, cheapest) | Low |
| **Rectangle** | Flat 4-sided with width and height | Higher |
| **Disk** | Round and flat with radius | Higher |
| **Sphere** | Ball-shaped with radius | Higher |
## Use Cases
| Shape/Type | Punctual | Rectangle | Disk | Sphere |
|------------|----------|-----------|------|--------|
| Directional | Sun | ❌ | Sun/Moon | Sun/Moon |
| Omni | Bulb | ❌ | ❌ | Round bulb |
| Spot | Torch | TV screen | Shaded bulb | Shaded round bulb |
## Materials
# Physical Materials
To use Physically Based Rendering (PBR) in PlayCanvas you need to understand how the Physical Material is configured and what effect altering various parameters will have.
## Image Based Lighting (IBL)
Physical Materials with an HDR Prefiltered CubeMap look great! PBR relies on environment lighting for realistic reflections. Without a cubemap, materials won't look like the samples.
## Workflows: Metalness vs Specular
PBR offers two equivalent workflows:
### Metalness Workflow
Involves setting a metalness value or map determining which areas are metal (1) or non-metal (0). Usually binary — values between 0 and 1 are rare.
## Core Material Properties
### Diffuse (Albedo / Base Color)
The base color of the material (RGB). Should avoid including lighting detail (shadows/highlights).
Reference values:
| Material | RGB |
|----------|-----|
| Gold     | (1.000, 0.766, 0.336) / [255, 195, 86] |
| Silver   | (0.972, 0.960, 0.915) / [248, 245, 233] |
| Copper   | (0.955, 0.637, 0.538) / [244, 162, 137] |
### Metalness
A single value 0-1 determining if a material is metal (1) or non-metal (0). Can also be a map. Should almost always be 0 or 1.
### Glossiness
Used in both workflows. Defines how smooth the surface is. Affects reflection sharpness and specular highlight breadth. Value 0-100 or a map.
## Additional Properties
- **Ambient Occlusion**: Shadow detail in crevices
- **Emissive**: Self-illuminating color
- **Opacity**: Transparency (0-1)
- **Normal Map**: Surface detail without geometry
- **Height Map**: Parallax/displacement mapping
- **Clear Coat**: Simulates coated surfaces (car paint, etc.)
- **Sheen**: Soft rim-like lighting for fabrics
- **Specular**: For specular workflow — color/intensity of reflections
## The Core Triad
Diffuse, Metalness, and Glossiness are the three core properties of the physical material system. Mastering these three gives you control over most material appearances.
## Shaders
# Shaders
When you import your 3D models into PlayCanvas, by default, they will use the Physical Material. This is a versatile material type that can cover a lot of your rendering needs.
However, you will often want to perform special effects or special cases for your materials. To do this you will need to write a custom shader using ShaderMaterial.
## Creating a ShaderMaterial
```javascript
const shaderDesc = {
    uniqueName: 'MyShader',
    vertexGLSL: `
        // write your vertex shader source code in GLSL language
    `,
    fragmentGLSL: `
        // write your fragment shader source code in GLSL language
    `,
    vertexWGSL: `
        // write your vertex shader source code in WGSL language
    `,
    fragmentWGSL: `
        // write your fragment shader source code in WGSL language
    `,
    attributes: {
        aPosition: pc.SEMANTIC_POSITION,
        aUv0: pc.SEMANTIC_TEXCOORD0
    }
};
const material = new pc.ShaderMaterial(shaderDesc);
```
The shader source code can be written in GLSL (WebGL2/WebGPU) or WGSL (WebGPU only), or both.
## Preprocessor
Before the shader is used, a preprocessing step is applied supporting C-like directives: `#define`, `#if`, `#else`, `#endif`, and `#include`.
### Material Shader Defines
Set per-material defines for dynamic customization:
```javascript
material.setDefine('USE_TEXTURE', true);
material.setDefine('FIRETYPE', 'RED');
```
Results in: `#define USE_TEXTURE` and `#define FIRETYPE RED`
### Shader Pass Defines
Built-in engine defines:
- `#define FORWARD_PASS` — normal forward pass
- `#define SHADOW_PASS` — shadow rendering
- `#define PICK_PASS` — picking (instance IDs)
- `#define DEPTH_PICK_PASS` — picker depth support
Custom passes via `CameraComponent.setShaderPass('custom')` generate `#define CUSTOM_PASS`.
## Shader Includes (Chunks)
### Vertex Shader Includes
```glsl
#include "transformCoreVS"  // model/view/projection matrices, skinning, morphing
#include "normalCoreVS"     // normal matrix, local normal
```
These provide:
- `getModelMatrix()`, `getLocalPosition()`
- `getNormalMatrix()`, `getLocalNormal()`
- Automatic skinning and morphing support
### Fragment Shader Includes
```glsl
#include "gammaPS"          // Gamma correction
#include "tonemappingPS"    // Tone mapping
#include "fogPS"            // Fog effects
```
Usage pattern:
```glsl
vec3 colorLinear = ...;
vec3 fogged = addFog(colorLinear);
vec3 toneMapped = toneMap(fogged);
gl_FragColor.rgb = gammaCorrectOutput(toneMapped);
```
## Debugging Shaders
To inspect generated shaders:
```javascript
pc.Tracing.set(pc.TRACEID_SHADER_ALLOC, true);
```
Each created shader will be logged in the browser console with its full source code.
## Particles
PlayCanvas provides comprehensive support for creating and editing particle systems.
## What is a Particle System?
A particle system is a simulation that manages many independently moving particles. They can be used to approximate a huge number of effects such as rain, snow, smoke, fire and so on.
Note that particles are not physically simulated. They do not interact or collide with each other. They will pass through surfaces in your scene.
## Creating a Particle System
In the Editor's 3D View, an unselected particle system is represented with the following icon:
To create a new particle system, simply create a new entity and add a particle system component to it. For convenience, the Editor menu has an item that does this in a single step:
A newly created particle system with the default settings looks like this:
To configure the particle system via the particle system component interface, consult the reference [here](/user-manual/editor/scenes/components/particlesystem).
## Triggering a Particle System in Script
Sometimes, you might want a particle system to play in response to some event or at a particular time. For example, an explosion should play when a missile reaches its target. To do this, ensure that the Autoplay option is disabled for your particle system. Then, attach a script component to your particle system entity. The following two lines will start (or restart) a particle system:
```javascript
this.entity.particlesystem.reset();
this.entity.particlesystem.play();
```
## Soft Particles
Soft particles are particles that are faded out near their intersections with scene geometry. If soft particles are enabled by using [`depthSoftening`](https://api.playcanvas.com/engine/classes/ParticleSystemComponent.html#depthsoftening), the camera which renders the particles needs to have a [Depth Map](/user-manual/graphics/cameras/depth-layer) rendering enabled.
## Layers
Layers customize the render loop. Use them to: modify mesh render order, set cameras to render only certain meshes, control which lights affect which meshes.
## Rendering Order (3 factors)
### 1. Camera Priority
Cameras with lower priority values render first. Each camera has a layer list controlling which layers it renders.
### 2. Layer Composition
`this.app.scene.layers` determines sub-layer order. Sub-layers (not layers) are ordered — e.g., all opaque first, then transparent.
### 3. Sort Modes
| Mode | Description |
|------|-------------|
| `MATERIALMESH` | (Opaque default) Minimize material/mesh switching |
| `BACK2FRONT` | (Transparent default) Properly blend semi-transparent objects |
| `FRONT2BACK` | May improve performance via reduced overdraw |
| `MANUAL` | (UI/2D default) Sorted by `MeshInstance.drawOrder` |
| `NONE` | No sorting — render in add order |
## Default Layers
| Layer | Purpose |
|-------|---------|
| World (Opaque) | Most opaque component meshes |
| Depth (Opaque) | Capture color/depth buffer |
| Skybox (Opaque) | Skybox (after World to reduce overdraw) |
| World (Transparent) | Transparent component meshes |
| Immediate (Opaque/Transparent) | `app.renderLine()` etc. |
| UI (Transparent) | Element components |
## Custom Layers
Create in Settings → LAYERS panel. Assign components to layers via the `layers` property on Model, Element, Sprite, and Particle System components. Cameras and Lights also use `layers` to control what they render/light.
**Recommended:** Each mesh-rendering entity on exactly one layer (World, Terrain, Buildings, Characters). Additional cameras for picture-in-picture, split screen, or render-to-texture.
## Advanced Batching
Batching combines multiple mesh instances into a single mesh to render in one GPU draw call. Assign Model, Sprite, and Element components to batch groups to reduce draw calls.
## Batch Groups
Created in Project Settings → Batch Groups. Properties:
| Property | Description |
|----------|-------------|
| **Name** | Identifier, retrievable at runtime |
| **Dynamic** | If enabled, objects can move/rotate/scale. Static uses less runtime resources. |
| **Max AABB Size** | Maximum bounding box side length. Larger = fewer draw calls but worse culling. |
## Combining Rules
Mesh instances in a single batch must:
- Share the same Batch Group ID
- Share the same material
- Share the same shader parameters
- Be within the Max AABB Size bounding box
- Be in the same layer
- Have ≤ 65,535 vertices per batch
- Dynamic batches have max 1,024 movable instances (hardware dependent)
## Triggering Re-batching
```javascript
element.textureAsset = this.hoverAsset;
if (element.batchGroupId)
    this.app.batcher.markGroupDirty(element.batchGroupId);
```
## Terminology
- **Batch Group** — Named group defining how meshes combine. Components are assigned to it.
- **Batch** — Runtime object: the combined mesh instances rendered in one draw call.
- **Batch Manager** — Programmatic API for creating/updating batches.
