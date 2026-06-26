# Glossary

Here is an overview of some of the terms we use to describe the PlayCanvas Engine and Tools.
## Animation {#animation}
An Animation is an [Asset](#asset) that contains keyframe data used to animate properties of [Entities](#entity) over time.
## Application {#application}
The `Application` class is the core container that manages all the essential systems and resources needed to run your PlayCanvas application.
* The `Scene` which includes the scene hierarchy and scene settings
* The `ComponentSystem`s that handle entity behavior
* Input devices (keyboard, mouse, touch and gamepad)
* Asset loading and management
* The main render loop and frame updates
* Audio context and 3D audio systems
The Application is accessible from any script function (`initialize`, `update` and so on) as `this.app` and provides the main interface for interacting with the engine's functionality.
## Asset {#asset}
An Asset is a unit of data that represents a resource used in your PlayCanvas application. Assets are typically imported from content creation applications (such as Blender, 3D Studio Max, or Photoshop) but can also be created directly in the editor.
* 3D models and animations
* Textures and materials
* Audio files and music
* Scripts and JSON data
* Fonts and UI elements
Assets are managed through the [Asset Pipeline](#asset-pipeline) and can be assigned to [Components](#component) to give [Entities](#entity) their appearance and behavior. Also see [Source Assets](#source-asset) and [Target Assets](#target-asset).
## Asset Pipeline {#asset-pipeline}
The asset pipeline is a process run on the PlayCanvas servers which converts an uploaded [Source Asset](#source-asset) e.g.
## Attribute {#attribute}
An attribute is a property of a [Component](#component). Attributes are represented in the PlayCanvas Editor interface via user interface controls (pickers, check boxes, sliders, etc).
## Collision {#collision}
Collision refers to the detection and response when two or more objects intersect in 3D space. PlayCanvas provides collision detection through the Collision component, which defines the shape used for collision detection, and the Rigidbody component, which handles the physics response.
## Component {#component}
Components describe the properties and functionality of an [Entity](#entity).
Components are added to Entities via the Component menu in the PlayCanvas Editor, or they can be added at runtime via their respective `ComponentSystem` object.
## Cubemap {#cubemap}
A Cubemap is a special type of [Texture](#texture) that consists of six square textures arranged to form a cube.
## DOM {#dom}
The DOM (Document Object Model) is a way of representing an HTML document.
## Entity {#entity}
An Entity is one of the building blocks of your application in the [PlayCanvas Engine](#playcanvas-engine).
All Entities have a position, rotation and scale. They have a parent node from which they inherit a transform, and they may have child nodes to which they supply their transform.
## Framework {#framework}
The Framework is the high-level abstraction layer built on top of the core PlayCanvas Engine that provides a game-development-focused interface.
* The Entity-Component System for organizing game objects
* Asset management and loading systems
* Input handling and device abstraction
* Audio management and 3D spatial audio
* Graphics pipeline management
* Integration with the PlayCanvas Editor for live-link functionality
The Framework simplifies common game development tasks and provides a structured approach to building interactive 3D applications. See the [API Reference](https://api.playcanvas.com) for more details.
## Gizmo {#gizmo}
A Gizmo is a control that can be dragged around with the mouse in order to edit the attributes of an Entity.
## Hierarchy {#hierarchy}
The Hierarchy is a panel in the [PlayCanvas Editor](#playcanvas-editor) that displays the tree structure of [Entities](#entity) in your [Scene](#scene).
## High Dynamic Range {#high-dynamic-range}
High Dynamic Range or HDR refers to color information that is outside of the usual 0-1 range. In the standard range, 0 is black and 1 is the brightest color that the display device can show.
## Inspector {#inspector}
The Inspector is a panel in the [PlayCanvas Editor](#playcanvas-editor) that displays the properties and [Components](#component) of the currently selected [Entity](#entity) or [Asset](#asset).
## Light {#light}
A Light is a [Component](#component) that illuminates the [Scene](#scene). PlayCanvas supports several types of lights including directional lights (like the sun), point lights (like light bulbs), and spot lights (like flashlights).
## Material {#material}
A Material is an [Asset](#asset) that defines how surfaces appear when rendered.
* **Albedo/Diffuse**: Base color and texture
* **Normal/Bump**: Surface detail and texture
* **Metalness**: How metallic the surface appears
* **Roughness**: How smooth or rough the surface is
* **Emission**: Self-illuminating properties
* **Opacity**: Transparency and alpha blending
Materials can reference [Texture](#texture) assets for detailed surface appearance and support both physically-based rendering (PBR) and traditional lighting models. In the [PlayCanvas Editor](#playcanvas-editor), materials can be edited by selecting them in the assets panel or by clicking on a material directly on a model in the 3D view.
## PlayCanvas Editor {#playcanvas-editor}
The PlayCanvas Editor is a visual editing tool which can be used by members of your development team to edit [Scenes](#scene).
## PlayCanvas Engine {#playcanvas-engine}
The PlayCanvas Engine is a JavaScript library which provides all the functionality you will need to create an interactive 3D application or game.
Programs created using the PlayCanvas Engine will run directly in a modern web browser with no need for third-party plugins.
## Project {#project}
A Project is a collection of [Scenes](#scene) and [Assets](#asset) that belongs to a single user.
## Rigidbody {#rigidbody}
A Rigidbody is a [Component](#component) that enables an [Entity](#entity) to participate in physics simulation.
## Scene {#scene}
A Scene is a collection of Entity data, Art data and Code data which can be loaded as a unit.
## Script {#script}
A Script is an [Asset](#asset). It is assigned to a Script [Component](#component) on an [Entity](#entity). Scripts are written in JavaScript. They have several predefined functions that can be overridden:
* `initialize` - called once on instantiation
* `postInitialize` - called once after all script `initialize` functions have been called
* `update` - called every frame
* `postUpdate` - called every frame after all script `update` functions have been called
* `swap` - called when a script is 'hot reloaded' (due to a save event in the Code Editor)
## Skybox {#skybox}
A Skybox is a background that surrounds the entire [Scene](#scene), typically used to create the illusion of distant scenery such as mountains, clouds, or stars.
## Source Asset {#source-asset}
A source asset is the original file that has been uploaded into PlayCanvas.
## Target Asset {#target-asset}
A target asset is a file that can be loaded into your game at runtime. It will be in a format ready to use in the Engine.
## Template {#template}
A Template is an [Asset](#asset) that contains a piece of an [Entity](#entity) hierarchy. It has a root Entity and can have any number of children.
## Texture {#texture}
A Texture is an [Asset](#asset). Typically, it contains image data that can be mapped onto 2D or 3D geometry.
## Transformation Matrix {#transformation-matrix}
A Transformation Matrix is a mathematical matrix that represents a set of linear transforms. In particular: translation, rotation and scale.
## Viewport {#viewport}
The Viewport is the 3D view panel in the [PlayCanvas Editor](#playcanvas-editor) where you can visually see and interact with your [Scene](#scene).