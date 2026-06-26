# Integration

Use this file for installation, iframe setup, open props, platform constraints, and deployment details. Do not use it for runtime object workflows or long troubleshooting trees.

## Choose The Embed Mode

Use plain iframe embed when the user only wants to show published content:

```html
<iframe
  src="https://www.kivicube.com/scenes/<sceneId>"
  allow="xr-spatial-tracking;camera;microphone;autoplay;fullscreen;gyroscope;accelerometer"
  frameborder="0"
></iframe>
```

Use the plugin when the host page needs any of the following:

- Hide or replace Kivicube landing, loading, scan, or photo UI
- Listen for `ready`, download progress, tracking, `openUrl`, or compatibility failures
- Call `SceneApi` to inspect or mutate runtime content
- Build custom camera-switching or photo flows

Load the public script:

```html
<script src="https://www.kivicube.com/lib/iframe-plugin.js"></script>
```

## Host Environment Requirements

- The host page must run on HTTPS, or on `http://localhost` during local development.
- Mobile testing on `192.168.x.x`, `10.x.x.x`, or `172.16-31.x.x` without HTTPS is a common camera failure case.
- If the host uses CSP, allow `https://www.kivicube.com` in at least `frame-src`, and in `script-src` if the host loads the official script directly.
- The plugin writes the iframe `allow` permissions automatically. Do not strip or overwrite them.

## Open A Scene Or Collection

Manual scene open:

```js
async function mountScene() {
  const iframe = document.getElementById('sceneHost');

  await kivicubeIframePlugin.openKivicubeScene(iframe, {
    sceneId: 'YOUR_32_CHAR_SCENE_ID',
    hideLogo: true,
    hideTitle: true,
    cameraPosition: 'back',
  });
}
```

Manual collection open:

```js
async function mountCollection(iframe) {
  await kivicubeIframePlugin.openKivicubeCollection(iframe, {
    collectionId: 'YOUR_6_CHAR_COLLECTION_ID',
    hideGyroscopePermission: true,
  });
}
```

Important differences:

- `sceneId` is 32 chars; `collectionId` is 6 chars.
- Collection-only open prop: `hideGyroscopePermission`.
- `ready.detail.api` is documented for scenes, not for collection-level runtime control.

## Auto-Open Rules

The plugin auto-opens only when the iframe already exists before `DOMContentLoaded` and uses the expected id:

- Scene auto-open: `<iframe id="kivicubeScene" scene-id="...">`
- Collection auto-open: `<iframe id="kivicubeCollection" collection-id="...">`

Prefer manual open for SPAs, route transitions, or reusable components.

## Props And Attribute Rules

- HTML form: use kebab-case such as `hide-start`, `hide-logo`, `scene-id`.
- JS form: use camelCase such as `hideStart`, `hideLogo`, `sceneId`.
- JS props override same-name HTML attrs.
- Props are read once when opening. Reopen to apply changes.

High-risk props worth calling out explicitly:

- `hideStart`: can reduce autoplay and camera permission success because it removes an important user gesture.
- `hideScan`: only hide it if the host will render its own scan guidance for `image2d-tracking` or `cloud-ar`.
- `hideBackground`: mainly useful for `web3d`.
- `disableOpenUrl`: prevents the inner page from opening URLs directly, but the host can still handle the `openUrl` event.

The important host-facing props are summarized in this skill: `sceneId`, `collectionId`, `hideLogo`, `hideTitle`, `hideDownload`, `cameraPosition`, `hideLoading`, `hideScan`, `hideTakePhoto`, `hideBackground`, `hideStart`, `disableOpenUrl`, and collection-only `hideGyroscopePermission`.

## Scene Types And Platform Notes

Documented Web types:

- `image2d-tracking`: image-recognition flow with `tracked` and `lostTrack`
- `cloud-ar`: cloud recognition, optional `skipCloudar()`
- `web3d`: no camera recognition flow, works on desktop, `switchCamera()` does not apply

Important platform behaviors:

- iOS iframe hosts do not reliably support gyroscope authorization flows. Prefer disabling gyroscope-dependent content where possible.
- `web3d` does not depend on the device camera and is the most predictable mode on desktop.
- Keep answers scoped to the stable public Web plugin surface, especially `image2d-tracking`, `cloud-ar`, and `web3d`.

## Permissions And Media

The host should listen to:

- `error` for `isUserDeniedCamera` and `isUserDeniedGyroscope`
- `incompatibility` for device or browser capability failures

Example:

```js
iframe.addEventListener('error', (event) => {
  const detail = event.detail || {};
  if (detail.isUserDeniedCamera) showCameraGuide();
  else if (detail.isUserDeniedGyroscope) showGyroscopeGuide();
  else showToast(detail.message || 'Kivicube unavailable');
});

iframe.addEventListener('incompatibility', () => {
  showUnsupportedDialog();
});
```

Remember that media autoplay can still fail even if camera permission succeeds, especially after `hideStart`.

## Framework Wrapper Pattern

When React, Vue, or similar code wants to keep DOM attributes under component control, call open with `modifyIframe=false` and then apply the returned attrs yourself:

```js
const result = await kivicubeIframePlugin.openKivicubeScene(
  iframe,
  { sceneId, hideLogo: true },
  false,
);

iframe.id = result.id;
iframe.allow = result.allow;
iframe.src = result.src;
```

Treat the open call as async. That keeps wrapper logic correct even when the plugin prepares protocol state before returning.

## Runtime Asset Loading And CORS

If the host passes URLs into `createImage()`, `createGltfModel()`, `createVideo()`, `createPanorama()`, or `createEnvMapByHDR()`, the asset origin must allow:

```text
Access-Control-Allow-Origin: https://www.kivicube.com
```

If that is not possible, download the file in the host and pass `ArrayBuffer` instead. Use URL form for large videos unless auth or CORS requires host-side fetches.

## Local Development And Deployment

Recommended flow:

1. Build the host page on `http://localhost` for layout, event wiring, and UI iteration.
2. Move to an HTTPS test domain for real-device validation.
3. Verify iPhone Safari, Android Chrome, and any target in-app WebView before launch.

Deployment checklist:

1. Host page is reachable via HTTPS.
2. Scene or collection ids are correct.
3. Kivicube script and iframe are allowed by CSP.
4. Event listeners and error fallbacks are wired.
5. Runtime asset origins allow CORS from `https://www.kivicube.com`.
6. Watermark and domain-authorization expectations are understood.
