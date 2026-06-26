---
name: kivicube-web-plugin-ar-xr-builder
description: Use when building, embedding, customizing, or troubleshooting AR/XR experiences with the Kivicube Web Plugin, including WebAR/Web3D H5 pages, landing pages, event pages, product showcases, sceneId or collectionId setup, Vue/React wrappers, SceneApi runtime control, camera, autoplay, permissions, CORS, and compatibility. Also match Chinese requests such as 开发AR体验、XR体验、WebAR活动页、H5落地页、营销页、3D展示页、接入Kivicube Web插件、扫码识别、云识别、拍照分享。
---

# Kivicube Web Plugin AR/XR Builder

Kivicube Web Plugin is an iframe-based integration layer for published scenes and collections used to build AR and XR experiences. The host page owns the iframe, page UI, and event listeners; Kivicube owns the inner experience and exposes a public runtime bridge through `iframe-plugin.js`. Use this skill from an external integrator's point of view: public script URL, public events, public open props, framework wrappers, and public `SceneApi`.

Common trigger phrases this skill should match well:

- build a WebAR H5 activity page or AR marketing page
- embed a Kivicube scene in a Vue 3 or React site
- create a branded AR landing page or event page
- build a Web3D product showcase or model viewer
- customize loading, scan, camera, or photo UI for Kivicube
- fix camera permission, autoplay, CORS, or compatibility issues in Kivicube Web

## Architecture Model

```text
Host page HTML/CSS/JS
  -> load https://www.kivicube.com/lib/iframe-plugin.js
  -> open a scene or collection into an <iframe>
  -> listen on the iframe for load/ready/progress/tracked/openUrl/error...
  -> for scene pages, read event.detail.api
  -> call async SceneApi methods across the iframe boundary
  -> Kivicube runtime updates objects, media, camera, and rendering
```

Key split:

- Plain `iframe` embed: fastest path, no plugin events, no runtime API.
- Plugin + scene: full host events plus `SceneApi`.
- Plugin + collection: open/close and process events work, but `ready.detail.api` is not a stable collection runtime API. If you need per-scene runtime hooks inside a collection, read `references/patterns.md` and `references/integration.md` for `sceneReady`.

## Common Task Map

| Task | Public entry point |
| --- | --- |
| Plain embed with no customization | direct iframe embed with a published scene or collection URL |
| Open a scene manually | `openKivicubeScene()` |
| Open a collection manually | `openKivicubeCollection()` |
| Auto-open before `DOMContentLoaded` | iframe `id` + `scene-id` or `collection-id` |
| Keep framework components in control of DOM attrs | `openKivicubeScene(..., false)` / `openKivicubeCollection(..., false)` |
| Start from Vue 3 or React | `references/examples.md` framework examples |
| React to loading or scan progress | iframe events: `downloadAssetProgress`, `loadSceneStart`, `tracked`, `lostTrack` |
| Get the runtime API | iframe `ready` event, then `event.detail.api` |
| Find or move an object | `getObject()`, `setPosition()`, `setRotation()`, `setScale()` |
| Add runtime content | `createImage()`, `createGltfModel()`, `createVideo()`, then `add()` |
| Clean up runtime objects | `remove()`, `destroyObject()`, `destroyKivicubeScene()` |
| Switch camera or take a photo | `switchCamera()`, `takePhoto()` |
| Forward host clicks into the scene | `dispatchTouchEvent()` |
| Skip cloud recognition | `skipCloudar()` |
| Diagnose permissions, autoplay, or CORS failures | `references/troubleshooting.md` |

## Mode Selection

- Use plain iframe embed when the user only needs to show a published scene or collection.
- Use the plugin when the host page needs custom UI, process events, runtime object changes, camera switching, or custom photo flows.
- Prefer scene pages over collection pages when the user needs `SceneApi` immediately; collection runtime control is narrower and event-driven.
- Prefer manual open when the host uses React, Vue, routing, or explicit mount/unmount logic. Prefer auto-open only for static pages with one obvious iframe.

## Key Conventions

- Treat `openKivicubeScene()` and `openKivicubeCollection()` as async. This matters most when `modifyIframe=false` is used in framework wrappers.
- HTML attributes are read once at open time. Changing `hide-start`, `scene-id`, or similar attrs later does nothing until the scene or collection is opened again.
- JS props override same-name HTML attrs.
- All `SceneApi` methods should be awaited.
- Scene objects are opaque handles, not raw `three.js` objects. Never mutate `handle.position` or similar fields directly.
- `loadSceneEnd` is usually the safest point for bulk object queries, runtime additions, and event registration that depend on scene content already existing.
- Always call `destroyKivicubeScene()` or `destroyKivicubeCollection()` before reusing the iframe for another scene or collection.
- `hideStart` is high risk for autoplay and permission flows. Prefer branded host UI that still preserves an explicit user gesture.
- Public Web scene types covered here are `image2d-tracking`, `cloud-ar`, and `web3d`. Do not present `face-ar`, `body-ar`, `landmark`, `plane`, `roam`, audio APIs, or custom animation APIs as part of the stable Web plugin surface.

## Minimal Path

```html
<script src="https://www.kivicube.com/lib/iframe-plugin.js"></script>
<iframe id="sceneHost" title="Kivicube scene"></iframe>
<script>
  async function main() {
    const iframe = document.getElementById('sceneHost');

    await kivicubeIframePlugin.openKivicubeScene(iframe, {
      sceneId: 'YOUR_32_CHAR_SCENE_ID',
    });

    iframe.addEventListener('ready', async (event) => {
      const api = event.detail.api;
      const obj = await api.getObject('rabbit');
      if (obj) await api.setObjectVisible(obj, true);
    });
  }

  main().catch(console.error);
</script>
```

Then branch by need:

- Installation, script URL, HTTPS, props, permissions, and deployment: `references/integration.md`
- Lifecycle, event choreography, host-owned UI, and cleanup: `references/patterns.md`
- Object lookup, transforms, creation, hierarchy, and destruction: `references/scene_objects_reference.md`
- Images, panorama, video, GIF, glTF, and animation control: `references/media_animation_reference.md`
- Rendering, lights, env map, camera, touch forwarding, photo, and cloud-skip: `references/rendering_camera_reference.md`
- Copyable end-to-end examples, including Vue 3 and React: `references/examples.md`
- Stable usage guidance and rollout advice: `references/best_practices.md`
- Symptom-driven debugging: `references/troubleshooting.md`

## API Scope

Treat the public Kivicube Web plugin surface as the source of truth:

- open or destroy a scene or collection through the global plugin object
- listen on the iframe for lifecycle, loading, recognition, URL, and error events
- read `event.detail.api` on scene pages and call async `SceneApi` methods
- keep answers limited to the stable Web plugin surface summarized in this skill and its references
