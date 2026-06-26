# Media And Animation Reference

Use this file when the user is working with images, panorama, GIFs, video, glTF models, or animation playback.

## Choose The Media Type

- `createImage()`: 2D image planes, posters, badges, clickable overlays
- `createPanorama()`: 360 background content, especially for `web3d`
- `createAnimatedImage()`: GIF-like decorative or lightweight feedback loops
- `createVideo()`: standard video planes
- `createAlphaVideo()`: transparency encoded in the video asset
- `createKeyingVideo()`: green-screen or blue-screen style chroma key
- `createGltfModel()`: 3D models and model animation

All of them return object handles and usually need `add()` before they become visible.

## URL vs ArrayBuffer

All documented creation methods accept either a URL or binary data. Pick based on tradeoff:

- URL: preferred for large assets, especially video
- `ArrayBuffer`: preferred when the host must attach auth, avoid CORS problems, or fetch from its own pipeline first

If using URL, the origin must allow `https://www.kivicube.com` via CORS.

## Images And Panorama

Relevant APIs:

- `createImage()`
- `createPanorama()`

Important notes:

- Panorama uses a `segments` parameter; `64` is a practical default and larger values are rarely necessary.
- Panorama does not support click events.
- Images and panorama still use normal transform APIs such as `setPosition()` and `setScale()`.
- Supported image inputs here are standard JPEG, PNG, and GIF-style assets. Prefer sRGB images for predictable output.

## Animated Images

Animated image APIs:

- `getAnimatedImagePaused()`
- `playAnimatedImage(loopCount?)`
- `pauseAnimatedImage()`
- `stopAnimatedImage()`

Documented events:

- `play`
- `pause`
- `ended`
- `loop`

Usage guidance:

- Use GIFs for simple decorative loops or short feedback effects.
- If the user needs better transparency, more precise seeking, or stronger performance control, steer them toward video or glTF animation instead.

## Videos

Video creation APIs:

- `createVideo()`
- `createAlphaVideo()`
- `createKeyingVideo(input, config?)`

Video playback APIs:

- `getVideoDuration()`
- `getVideoPaused()`
- `getVideoCurrentTime()`
- `setVideoCurrentTime()`
- `getVideoLoop()`
- `setVideoLoop()`
- `playVideo()`
- `pauseVideo()`
- `stopVideo()`
- `playbackVideo()`

Keying-video config points worth remembering:

- `color`
- `similarity`
- `smoothness`
- `spill`

Operational advice:

- Browser autoplay restrictions still apply because this is Web media inside an iframe.
- `hideStart` makes autoplay more fragile.
- Use real-device regression tests for video-heavy experiences before launch.

## glTF Models And Animation

Model APIs:

- `createGltfModel()`
- `getAnimationNames()`
- `animationIsRunning()`
- `isAnimationLoop()`
- `getAnimationIsRunningNames()`
- `playAnimation()`
- `pauseAnimation()`
- `stopAnimation()`
- `playbackAnimation()`

Model animation options worth remembering:

- `name`
- `loop`
- `repeat`
- `repeatMode`
- `timeScale`
- `weight`
- `clampWhenFinished`
- `resetLoopCount`

Important semantics:

- glTF models are usually object trees, not one mesh. Use `getChildren()` or `getChildByProperty()` when the host needs an internal node.
- Model, video, and animated-image playback all share the same general event names (`play`, `pause`, `ended`, `replay`) but payload fields vary by object type.
- Keep answers scoped to model-embedded animation and the documented animation controls above.

## Media Event Strategy

Use media object events when the host needs analytics or UI feedback tied to the asset rather than to the page:

- Video ended -> show replay CTA
- GIF play or loop -> sync other UI motion
- Model animation ended -> unlock next step in the host flow

Bind with `api.on()` and unbind before destroying the scene or the asset handle.

## High-Frequency API Coverage

This file owns the primary explanation for these documented APIs:

- `createImage`
- `createAnimatedImage`
- `createGltfModel`
- `createVideo`
- `createAlphaVideo`
- `createKeyingVideo`
- `createPanorama`
- `getAnimatedImagePaused`
- `playAnimatedImage`
- `pauseAnimatedImage`
- `stopAnimatedImage`
- `getVideoDuration`
- `getVideoPaused`
- `getVideoCurrentTime`
- `setVideoCurrentTime`
- `getVideoLoop`
- `setVideoLoop`
- `playVideo`
- `pauseVideo`
- `stopVideo`
- `playbackVideo`
- `getAnimationNames`
- `animationIsRunning`
- `isAnimationLoop`
- `getAnimationIsRunningNames`
- `playAnimation`
- `pauseAnimation`
- `stopAnimation`
- `playbackAnimation`

Pair this file with `references/scene_objects_reference.md` for transforms and lifetime, and with `references/rendering_camera_reference.md` for env maps, light, and tone mapping that often accompany models.
