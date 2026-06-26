# Scene Objects Reference

Use this file when the question is about object handles, transforms, hierarchy, visibility, or object lifetime. Do not use it for video or animation semantics unless they depend on object handles.

## Core Mental Model

All scene objects are opaque handles:

```ts
interface SceneObjectHandle {
  id: number;
}
```

The handle is only a token that must be passed back into `SceneApi`. Never treat it as a raw `Object3D`.

## Lookup And Basic Properties

Primary lookup APIs:

- `getObject(name)`
- `getAllObject()`
- `getChildren(target)`
- `getChildByProperty(target, property, value)`

High-value property APIs:

- `getObjectName()` / `setObjectName()`
- `getObjectVisible()` / `setObjectVisible()`
- `getRenderOrder()` / `setRenderOrder()`
- `getDisableClick()` / `setDisableClick()`
- `getSize()`
- `lookAt()`

Guidance:

- Prefer meaningful object names in scene authoring so the host can use `getObject(name)` instead of brittle tree traversal.
- Use `getSize()` for layout or scale heuristics, not for exact authored dimensions.
- Use `setDisableClick()` when host UI or tutorial states should temporarily suppress interaction.

## Transform APIs

Transforms operate on authored or runtime-created objects:

- `getPosition()` / `setPosition()`
- `getRotation()` / `setRotation()`
- `getQuaternion()` / `setQuaternion()`
- `getScale()` / `setScale()`
- `lookAt()`

Important semantics:

- Rotation values are radians, not degrees.
- Use either Euler rotation or quaternion workflows consistently for one object.
- `setPosition()` and friends are the public write path; direct property mutation is not supported.

## Hierarchy And Lifetime

Hierarchy and lifetime APIs:

- `addChild()` / `removeChild()`
- `add()` / `remove()`
- `destroyObject()`
- `clear()`

Interpret them carefully:

- `add()` inserts a created object into the scene tree.
- `addChild(parent, child)` inserts under a parent; if the parent is already in the scene tree, the child does not need a separate `add()`.
- `remove()` detaches without destroying.
- `destroyObject()` detaches and frees resources.
- `clear()` destroys every object in the current scene and invalidates all stored handles.

Use `remove()` for temporary hiding or regrouping. Use `destroyObject()` only when the host will never reuse that handle.

## Runtime Creation APIs

Creation APIs from this file's perspective:

- `createGroup()`
- `createAmbientLight()`
- `createDirectionalLight()`

Creation APIs covered in other references:

- Images and panorama: `references/media_animation_reference.md`
- GIF, video, glTF animation: `references/media_animation_reference.md`
- Env map and rendering helpers: `references/rendering_camera_reference.md`

## Groups And Parenting

`createGroup()` is the simplest way to build host-owned hierarchy at runtime:

- Use it to move several objects together.
- Use it to make one object follow another.
- Use it to assemble a simple layout when the scene editor could not encode the final structure.

A common sequence:

```js
const group = await api.createGroup();
const image = await api.createImage(buffer);

await api.add(group);
await api.addChild(group, image);
await api.setPosition(group, 0, 1, 0);
```

## Object Events

General event APIs:

- `on(eventName, callback, target?)`
- `off(eventName, callback, target?)`

Event-name rules that matter most:

- Without `target`, only `objectClick` is supported.
- With `target`, documented events include `click`, `play`, `pause`, `ended`, `replay`, and object-specific media variants.

Click behavior notes:

- Click events bubble up the object tree.
- Because of the async bridge, there is no documented stop-propagation mechanism.
- `event.target` is the object whose listener is running; payloads may also include the more specific clicked child object.

## High-Frequency API Coverage

This file owns the primary explanation for these documented APIs:

- `getObject`
- `getAllObject`
- `getObjectName`
- `setObjectName`
- `getObjectVisible`
- `setObjectVisible`
- `getRenderOrder`
- `setRenderOrder`
- `getDisableClick`
- `setDisableClick`
- `getSize`
- `lookAt`
- `addChild`
- `removeChild`
- `getChildren`
- `getChildByProperty`
- `add`
- `remove`
- `destroyObject`
- `clear`
- `getPosition`
- `setPosition`
- `getRotation`
- `setRotation`
- `getQuaternion`
- `setQuaternion`
- `getScale`
- `setScale`
- `createGroup`

All of these methods are async and operate on opaque scene-object handles.
