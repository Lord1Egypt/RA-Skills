# Troubleshooting

Use this file for symptom-driven diagnosis. Pair it with `references/integration.md` for setup issues and `references/patterns.md` for lifecycle mistakes.

## Camera Does Not Open Or The Page Says The Device Is Unsupported

Likely causes:

- host page is not on HTTPS and is not `http://localhost`
- real-device testing is happening on a LAN IP without HTTPS
- browser or WebView does not expose the required camera capability

Check:

1. current host origin
2. `error` details such as `isUserDeniedCamera`
3. `incompatibility` events

## No Useful Events Arrive Except `load` Or `error`

Likely causes:

- account or domain authorization limits process events
- the page never progressed because the scene id or collection id is wrong
- the host is relying on auto-open but the iframe was inserted after `DOMContentLoaded`

Check:

1. whether the host uses manual open or valid auto-open markup
2. whether the id format is correct
3. domain-authorization and watermark expectations

## Changing iframe Attributes Does Nothing

Cause:

- props are read only once during open

Fix:

1. close the current scene or collection
2. reopen with the new props

Do not expect `iframe.setAttribute('hide-start', '')` after open to change live behavior.

## `ready` Fires But `event.detail.api` Is Missing Or Not Usable

Likely causes:

- the page is a collection, not a scene
- the host expects collection runtime control from `ready.detail.api`

Fix:

- use scene pages when immediate runtime control is required
- for collections, use `sceneReady` when the inner scene changes

## Object Lookup Returns `null`

Likely causes:

- wrong object name
- lookup is too early
- the object belonged to a previous scene

Fix:

1. retry from `loadSceneEnd` instead of only `ready`
2. verify naming in the authored scene
3. stop reusing handles across scene switches, `clear()`, or `destroyObject()`

## Videos Or Audio-Like Media Do Not Autoplay

Likely causes:

- `hideStart` removed the user gesture that browsers expect
- playback is starting in a stricter iOS or app WebView environment

Fix:

1. restore the default start flow or add an explicit host-side start button
2. test playback on real target devices
3. avoid assuming desktop behavior will match mobile behavior

## Runtime Asset Creation Fails For URL Inputs

Likely cause:

- asset origin does not allow `https://www.kivicube.com` through CORS

Fix:

1. confirm `Access-Control-Allow-Origin: https://www.kivicube.com`
2. if CORS cannot be changed, fetch in the host and pass `ArrayBuffer`

## `dispatchTouchEvent()` Does Not Trigger Object Clicks

Likely causes:

- coordinates are in page space, not iframe-local space
- iframe is hidden or has zero size
- click target is disabled or blocked by other logic

Fix:

1. convert coordinates relative to the iframe rectangle
2. verify iframe visibility and size
3. check `setDisableClick()` state on the target object

## `switchCamera()` Fails

Likely causes:

- current scene type is `web3d`
- device only has one useful camera
- current page is not a scene page

Fix:

1. gate the control by scene type
2. show a fallback or disable the button on unsupported devices
3. use scene pages for camera-switch flows

## `skipCloudar()` Has No Effect

Likely causes:

- current scene is not `cloud-ar`
- the scene is already configured to skip scanning

Fix:

- use this only for documented cloud-recognition scenes and present it as a user action, not a universal default

## Photo Output Has Unexpected Watermark, Size, Or Crop

Likely causes:

- account or domain authorization still allows watermarks
- device DPR and runtime composition change the final resolution
- `web3d` and AR scenes produce different kinds of output

Fix:

1. verify authorization and watermark expectations
2. test on the real target devices
3. avoid hard-coding one expected output dimension

## Scene Reopen Causes Strange State Or Leaking Behavior

Likely causes:

- host skipped `destroyKivicubeScene()` or `destroyKivicubeCollection()`
- old event handlers and object handles are still referenced

Fix:

1. remove host listeners
2. destroy runtime-created objects
3. set iframe to `https://www.kivicube.com/lib/empty.html`
4. call the correct destroy method
5. reopen fresh
