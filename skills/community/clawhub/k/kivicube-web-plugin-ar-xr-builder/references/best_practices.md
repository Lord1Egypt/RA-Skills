# Best Practices

Use this file for stable guidance, not for API signatures.

## Start With The Smallest Working Integration

- Begin with plain iframe or the plugin with only `sceneId` or `collectionId`.
- Add custom props one by one.
- Move to `SceneApi` only after process events are already working.

This keeps permission, autoplay, and scene-id problems separate from runtime-API problems.

## Preserve User Gesture When Possible

- Prefer keeping the default start flow, or recreate it with an explicit host-side button.
- Treat `hideStart` as an opt-in tradeoff, not a styling tweak.
- Test media-heavy experiences on real mobile devices before launch.

## Keep Host UI In HTML, Not In 3D, Unless It Must Be 3D

Prefer normal host HTML/CSS for:

- buttons
- text
- form controls
- analytics-heavy overlays
- responsive layout

Use screen-fixed 3D objects only when the content must remain part of the rendered scene.

## Favor Named Scene Objects Over Tree Guessing

- Give important authored objects stable names.
- Use `getObject(name)` first.
- Use `getChildByProperty()` only when the host truly needs internal nodes.

This makes runtime patches less brittle across scene edits.

## Be Deliberate About Runtime Asset Transport

- Use URL inputs for large media, especially video.
- Use `ArrayBuffer` when auth, signed URLs, or CORS policy make host-side fetches safer.
- Confirm the final asset origin allows `https://www.kivicube.com` before relying on URL mode.

## Manage Runtime Object Lifetime Explicitly

- Track host-created handles in one place.
- Use `remove()` for temporary disappearance.
- Use `destroyObject()` when the handle will not return.
- Avoid `clear()` unless the host truly wants a hard reset of the whole scene.

## Tune Rendering In Layers

For model-heavy `web3d` or polished AR scenes:

1. fix the model and authored content
2. adjust default lights
3. add or tune env map
4. choose tone mapping
5. only then tweak lower-level render state like opacity or depth behavior

This keeps rendering changes understandable and avoids chasing problems in the wrong layer.

## Prefer Default Lights Before Adding New Ones

- adjust default ambient or directional lights first
- add new lights only when needed

More runtime lights mean more complexity and more performance cost.

## Treat `loadSceneEnd` As The Main Runtime Hook

Use `ready` to capture `api`. Use `loadSceneEnd` for:

- object lookup
- event binding on existing objects
- runtime object insertion
- visual tuning

This is usually more robust than doing heavy scene work immediately at `ready`.

## Validate On Real Targets

Always test:

- iPhone Safari or the target iOS container
- Android Chrome or the target Android container
- any in-app WebView the product depends on

Desktop browser success is not enough evidence for a WebAR launch.

## Be Honest About What Is Not Public Yet

Audio APIs, custom animation APIs, and several scene-type families are outside the stable Web plugin surface here. Do not fill gaps with guesswork or internal implementation details when answering external users.
