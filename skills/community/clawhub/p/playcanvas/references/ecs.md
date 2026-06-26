# Entity Component System

PlayCanvas uses an **Entity Component System (ECS)** to organize and manage the objects in your application.
In this design pattern:
- **[Entities](https://api.playcanvas.com/engine/classes/Entity.html)** are containers — they hold components but have no behavior of their own.
- **[Components](https://api.playcanvas.com/engine/classes/Component.html)** add functionality or data to an Entity.
- **[Systems](https://api.playcanvas.com/engine/classes/ComponentSystem.html)** manage all instances of a given Component type.
This approach provides:
- **Flexibility** — you can mix and match components to build complex behaviors.
- **Modularity** — logic is encapsulated within components.
- **Performance** — systems process components in efficient batches.
## Components
A **[`Component`](https://api.playcanvas.com/engine/classes/Component.html)** adds data and behavior to an Entity.
## Examples
- [`CameraComponent`](https://api.playcanvas.com/engine/classes/CameraComponent.html)
- [`LightComponent`](https://api.playcanvas.com/engine/classes/LightComponent.html)
- [`RenderComponent`](https://api.playcanvas.com/engine/classes/RenderComponent.html)
- [`RigidBodyComponent`](https://api.playcanvas.com/engine/classes/RigidBodyComponent.html) & [`CollisionComponent`](https://api.playcanvas.com/engine/classes/CollisionComponent.html)
- [`ScriptComponent`](https://api.playcanvas.com/engine/classes/ScriptComponent.html)
## Adding a Component in code
```javascript
entity.addComponent('camera', {
    nearClip: 1,
    farClip: 100,
    fov: 55
});
```
See [`addComponent`](https://api.playcanvas.com/engine/classes/Entity.html#addcomponent).
## Accessing a Component
```javascript
const camera = entity.camera;
```
## Removing a Component
```javascript
entity.removeComponent('camera');
```
See [`removeComponent`](https://api.playcanvas.com/engine/classes/Entity.html#removecomponent).
## Enabling / Disabling Components
```javascript
entity.model.enabled = false;
```
See [`enabled`](https://api.playcanvas.com/engine/classes/Component.html#enabled).
## Hierarchy And Transformations
Entities can be arranged in a **parent-child hierarchy**. The `Entity` class inherits its transform capabilities from the [`GraphNode`](https://api.playcanvas.com/engine/classes/GraphNode.html) superclass.
## Key points
- **Transforms are relative** to the parent.
- **World transforms** are calculated by combining local transforms through the hierarchy.
- Moving a parent affects all its children.
## Example
```javascript
childEntity.setLocalPosition(1, 0, 0); // relative to parent
console.log(childEntity.getWorldPosition()); // global position
```
See [`setLocalPosition`](https://api.playcanvas.com/engine/classes/GraphNode.html#setlocalposition) and [`getWorldPosition`](https://api.playcanvas.com/engine/classes/GraphNode.html#getworldposition).
## Re-parenting
```javascript
newParent.addChild(childEntity);
```
## Scaling considerations
- Non-uniform scaling can cause visual or physics issues.
- Avoid scaling physics-enabled entities unless necessary.
## Searching The Hierarchy
## By Name
```javascript
const found = app.root.findByName("Player");
```
See [`findByName`](https://api.playcanvas.com/engine/classes/GraphNode.html#findbyname).
## By Tag
Tags are string labels you can assign to Entities ([`Tags`](https://api.playcanvas.com/engine/classes/Tags.html)).
```javascript
entity.tags.add("enemy");
const enemies = app.root.findByTag("enemy");
```
See [`tags`](https://api.playcanvas.com/engine/classes/Entity.html#tags) and [`findByTag`](https://api.playcanvas.com/engine/classes/Entity.html#findbytag).
## By Component
```javascript
const lights = app.root.findComponents("light");
```
See [`findComponents`](https://api.playcanvas.com/engine/classes/Entity.html#findcomponents).
## Recursion and Scope
- Searches can be started from any Entity, not just `app.root`.
- Searching from a smaller subtree is faster than searching the whole scene.
