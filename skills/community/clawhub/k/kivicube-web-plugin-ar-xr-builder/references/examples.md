# Examples

Use this file when the user asks for copyable end-to-end examples. Each example is meant to be adapted, not pasted unchanged.

## Example 1: Branded AR Shell With Host-Owned Progress, Scan, And Photo UI

Best for copying:

- event wiring
- host-owned loading and scan UI
- custom photo button flow

```js
async function mountSceneShell() {
  const iframe = document.getElementById('sceneHost');
  const photoButton = document.getElementById('photoButton');
  const previewImg = document.getElementById('preview');

  let api = null;

  await kivicubeIframePlugin.openKivicubeScene(iframe, {
    sceneId: 'YOUR_32_CHAR_SCENE_ID',
    hideLogo: true,
    hideTitle: true,
    hideDownload: true,
    hideLoading: true,
    hideScan: true,
    hideTakePhoto: true,
  });

  iframe.addEventListener('ready', (event) => {
    api = event.detail.api;
    showLandingReady();
  });

  iframe.addEventListener('downloadAssetProgress', (event) => {
    setProgress(event.detail);
  });

  iframe.addEventListener('loadSceneStart', () => showLoading());
  iframe.addEventListener('loadSceneEnd', () => {
    hideLoading();
    showScanHint();
  });

  iframe.addEventListener('tracked', () => {
    hideScanHint();
    photoButton.disabled = false;
  });

  iframe.addEventListener('lostTrack', () => {
    showScanHint();
    photoButton.disabled = true;
  });

  iframe.addEventListener('error', (event) => {
    const detail = event.detail || {};
    if (detail.isUserDeniedCamera) showCameraGuide();
    else showToast(detail.message || 'Scene unavailable');
  });

  photoButton.addEventListener('click', async () => {
    if (!api) return;
    showPhotoLoading();
    try {
      previewImg.src = await api.takePhoto();
      openPreview();
    } finally {
      hidePhotoLoading();
    }
  });
}
```

## Example 2: Component Wrapper That Keeps DOM Mutation In The Host

Best for copying:

- React or Vue style mounting
- `modifyIframe=false`
- cleanup on unmount

```js
export async function mountKivicubeScene(iframe, sceneId) {
  const result = await kivicubeIframePlugin.openKivicubeScene(
    iframe,
    {
      sceneId,
      hideLogo: true,
      hideTitle: true,
    },
    false,
  );

  iframe.id = result.id;
  iframe.allow = result.allow;
  iframe.src = result.src;

  const onReady = (event) => {
    console.log('scene ready', event.detail.sceneInfo);
  };

  iframe.addEventListener('ready', onReady);

  return () => {
    iframe.removeEventListener('ready', onReady);
    iframe.src = 'https://www.kivicube.com/lib/empty.html';
    kivicubeIframePlugin.destroyKivicubeScene(iframe);
  };
}
```

## Example 3: Vue 3 Minimal Scene Component

Best for copying:

- `script setup`
- `ref` and lifecycle hooks
- simple scene open and cleanup

```vue
<template>
  <iframe ref="iframeRef" class="kivicube-frame" title="Kivicube scene" />
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';

const iframeRef = ref(null);
const sceneId = 'YOUR_32_CHAR_SCENE_ID';

function handleReady(event) {
  console.log('scene ready', event.detail.sceneInfo);
}

onMounted(async () => {
  const iframe = iframeRef.value;
  if (!iframe) return;

  await window.kivicubeIframePlugin.openKivicubeScene(iframe, {
    sceneId,
    hideLogo: true,
    hideTitle: true,
  });

  iframe.addEventListener('ready', handleReady);
});

onBeforeUnmount(() => {
  const iframe = iframeRef.value;
  if (!iframe) return;
  iframe.removeEventListener('ready', handleReady);
  iframe.src = 'https://www.kivicube.com/lib/empty.html';
  window.kivicubeIframePlugin.destroyKivicubeScene(iframe);
});
</script>

<style scoped>
.kivicube-frame {
  width: 100%;
  height: 60vh;
  border: none;
}
</style>
```

Note:

- Load `https://www.kivicube.com/lib/iframe-plugin.js` in the app shell or `index.html` before this component mounts.

## Example 4: React Minimal Scene Component

Best for copying:

- `useRef` and `useEffect`
- simple mount and unmount lifecycle
- event listener cleanup

```jsx
import { useEffect, useRef } from 'react';

export function KivicubeScene() {
  const iframeRef = useRef(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const handleReady = (event) => {
      console.log('scene ready', event.detail.sceneInfo);
    };

    let disposed = false;

    async function mountScene() {
      await window.kivicubeIframePlugin.openKivicubeScene(iframe, {
        sceneId: 'YOUR_32_CHAR_SCENE_ID',
        hideLogo: true,
        hideTitle: true,
      });

      if (!disposed) {
        iframe.addEventListener('ready', handleReady);
      }
    }

    mountScene().catch(console.error);

    return () => {
      disposed = true;
      iframe.removeEventListener('ready', handleReady);
      iframe.src = 'https://www.kivicube.com/lib/empty.html';
      window.kivicubeIframePlugin.destroyKivicubeScene(iframe);
    };
  }, []);

  return <iframe ref={iframeRef} title="Kivicube scene" style={{ width: '100%', height: '60vh', border: 0 }} />;
}
```

Note:

- Load `https://www.kivicube.com/lib/iframe-plugin.js` in the HTML shell before rendering this component.

## Example 5: Web3D Runtime Tuning For A Published Model Scene

Best for copying:

- `loadSceneEnd` as the mutation point
- model lookup
- light, env map, and tone mapping tuning

```js
async function mountWeb3dPolish() {
  const iframe = document.getElementById('sceneHost');
  let api;

  await kivicubeIframePlugin.openKivicubeScene(iframe, {
    sceneId: 'YOUR_WEB3D_SCENE_ID',
    hideBackground: true,
  });

  iframe.addEventListener('ready', (event) => {
    api = event.detail.api;
  });

  iframe.addEventListener('loadSceneEnd', async () => {
    const model = await api.getObject('product-main');
    if (!model) return;

    const envMap = await api.createEnvMapByHDR('/assets/studio.hdr');
    await api.useEnvMapForObj(model, envMap, 1);
    await api.setToneMapping(api.constants.aces_filmic, 1);
    await api.setAnisotropy(model, 8, 'map', true);

    const light =
      (await api.getDefaultDirectionalLightLeft()) ||
      (await api.getDefaultDirectionalLightRight());

    if (light) {
      await api.setLightColor(light, '#ffd27f');
      await api.setLightIntensity(light, 1.5);
    }
  });
}
```

Notes:

- Do not add `switchCamera()` to this example; it is not valid for `web3d`.
- If HDR assets come from another origin, remember the CORS requirement from `references/integration.md`.
