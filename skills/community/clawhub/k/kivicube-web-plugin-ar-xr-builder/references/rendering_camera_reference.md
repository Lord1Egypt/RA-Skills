# Rendering And Camera Reference

Use this file when the question is about lights, rendering state, environment maps, tone mapping, camera parameters, custom photo flows, click forwarding, or cloud-scan skipping.

## Rendering-State APIs

Documented rendering-state APIs:

- `setEnableMask()`
- `setDisableMask()`
- `setGLState(target, prop, value, recursive?)`
- `setAnisotropy(target, num, mapType?, recursive?)`
- `setObjectAlpha(target, type, cutOff)`
- `setToneMapping(toneMapping, toneMappingExposure?)`
- `createEnvMapByHDR()`
- `useEnvMapForObj(target, envMap, intensity?)`

Public `api.constants` tone-mapping values:

- `no`
- `linear`
- `reinhard`
- `cineon`
- `aces_filmic`

Guidance:

- Use `setGLState()` sparingly; frequent low-level render overrides usually mean the asset should be authored differently upstream.
- `setObjectAlpha()` is for transparency or clipping behavior, not for general visibility toggling.
- Start tone-mapping tuning only after light and env-map choices are stable.
- Apply env maps selectively to model-like objects instead of blindly to the whole scene.

## Light APIs

Light APIs:

- `getDefaultAmbientLight()`
- `getDefaultDirectionalLightLeft()`
- `getDefaultDirectionalLightRight()`
- `getDirectionalLightTarget()`
- `getLightColor()`
- `setLightColor()`
- `getLightIntensity()`
- `setLightIntensity()`
- `createAmbientLight()`
- `createDirectionalLight()`

Recommended strategy:

- Prefer adjusting default lights first.
- Add new lights only when necessary.
- Tune lights together with env maps and tone mapping for PBR models.

## Camera APIs

Camera APIs:

- `getDefaultCamera()`
- `getCameraFov()` / `setCameraFov()`
- `getCameraAspect()` / `setCameraAspect()`
- `getCameraNear()` / `setCameraNear()`
- `getCameraFar()` / `setCameraFar()`
- `updateCameraProjectionMatrix()`
- `getCameraWorldDirection()`

Important distinction:

- These APIs control the scene camera, not the device hardware camera itself.
- After changing projection values, call `updateCameraProjectionMatrix()`.

## Switch Camera

Hardware-facing camera control:

- `switchCamera(position?)`

Use it only for camera-dependent scene types:

- `switchCamera()` is not valid for `web3d`
- collection runtime does not document this as a supported collection-level capability

Show a short loading state while switching, because device media streams can reopen.

## Photo, Touch Forwarding, And Cloud Skip

Interaction APIs:

- `takePhoto()`
- `dispatchTouchEvent(x, y)`
- `skipCloudar()`

Key semantics:

- `takePhoto()` returns a `data:image/png;base64,...` URL
- AR photo output usually composites camera + 3D scene
- `web3d` photo output is mostly the rendered content itself
- `dispatchTouchEvent()` expects iframe-local coordinates
- `skipCloudar()` only makes sense for `cloud-ar`

Recommended uses:

- `takePhoto()`: branded photo flows, download or preview overlays
- `dispatchTouchEvent()`: host overlays that intentionally intercept clicks first
- `skipCloudar()`: explicit "skip scan" buttons or controlled fallback flows

## Screen-Fixed 3D vs Host HTML

One practical 3D HUD pattern:

1. `getDefaultCamera()`
2. `addChild(camera, obj)`
3. position the child in camera space
4. optionally disable depth testing or depth writes

Use that only when the content truly needs to remain a 3D object. For text, buttons, forms, and precise responsive layout, prefer normal host HTML/CSS above the iframe.

## High-Frequency API Coverage

This file owns the primary explanation for these documented APIs:

- `createEnvMapByHDR`
- `setEnableMask`
- `setDisableMask`
- `setGLState`
- `setAnisotropy`
- `setObjectAlpha`
- `useEnvMapForObj`
- `setToneMapping`
- `getDefaultAmbientLight`
- `getDefaultDirectionalLightLeft`
- `getDefaultDirectionalLightRight`
- `getDirectionalLightTarget`
- `getLightColor`
- `setLightColor`
- `getLightIntensity`
- `setLightIntensity`
- `createAmbientLight`
- `createDirectionalLight`
- `getDefaultCamera`
- `getCameraFov`
- `setCameraFov`
- `getCameraAspect`
- `setCameraAspect`
- `getCameraNear`
- `setCameraNear`
- `getCameraFar`
- `setCameraFar`
- `updateCameraProjectionMatrix`
- `getCameraWorldDirection`
- `switchCamera`
- `takePhoto`
- `dispatchTouchEvent`
- `skipCloudar`

All of these methods are async and should be treated as cross-iframe runtime calls.
