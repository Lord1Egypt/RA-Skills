# Patterns

Use this file for cross-module workflows: event timing, host-owned UI, runtime object lifecycle, and scene or collection choreography.

## Pattern 1: Host-Owned State Machine

When the host hides Kivicube's default download, loading, scan, or photo UI, it needs its own state machine. A practical sequence for scene pages is:

```text
load
-> ready
-> downloadAssetStart / downloadAssetProgress / downloadAssetEnd
-> loadSceneStart / loadSceneEnd
-> sceneStart
-> tracked / lostTrack (recognition flows only)
```

Recommended ownership:

- `downloadAssetProgress`: progress bar
- `loadSceneStart` / `loadSceneEnd`: loading mask
- `tracked` / `lostTrack`: scan hints
- `sceneStart`: "experience started" marker for analytics and host UI changes
- `openUrl`: custom confirmation or routing when `disableOpenUrl` is enabled

## Pattern 2: Landing Page Without Breaking User Gesture

If the host wants a branded landing page:

1. Hide logo and title with props.
2. Keep the Kivicube start flow unless the team has tested autoplay carefully.
3. Use `downloadAssetEnd` or `ready` to transition host UI.
4. Let the user explicitly start the experience, even if the host UI is custom.

Do not default to `hideStart` unless:

- The scene is effectively `web3d`, or
- There is no important audio or video autoplay requirement.

## Pattern 3: Safe Runtime Mutation Window

`ready` gives the host `event.detail.api`, but scene content may still be loading. Use this split:

- Use `ready` to store `api`, `sceneInfo`, or bind host buttons.
- Use `loadSceneEnd` for `getObject()`, `getAllObject()`, bulk visibility changes, event registration on existing objects, and runtime additions that depend on the base scene already being there.

This reduces races where the API exists but the target object has not finished loading.

## Pattern 4: Runtime Object Lifecycle

For dynamically created objects:

```text
createXxx()
-> add() or addChild()
-> update with setPosition/setScale/...
-> remove() for temporary disappearance
-> destroyObject() when the handle will never be reused
```

Rules:

- `createXxx()` usually does not make the object visible by itself.
- `remove()` hides without freeing underlying resources.
- `destroyObject()` frees resources and invalidates the handle.
- `clear()` destroys every object in the scene and should be treated as a last-resort reset.

Keep a host-owned list of runtime-created handles if the page needs to clean them up before route changes or scene switches.

## Pattern 5: Switching Scenes In One Iframe

When reusing one iframe for several scene ids:

1. Unbind host listeners or object callbacks that point at the old scene state.
2. Remove or destroy runtime-created objects from the old scene.
3. Point the iframe to `https://www.kivicube.com/lib/empty.html`.
4. Call `destroyKivicubeScene(iframe)`.
5. Open the next scene.

Never reuse old `SceneObjectHandle` values after `destroyKivicubeScene()`, `destroyObject()`, or `clear()`.

## Pattern 6: Collection Pages

Collection pages differ from scene pages:

- `openKivicubeCollection()` and `destroyKivicubeCollection()` work as expected.
- `ready.detail.collectionInfo` is useful.
- `ready.detail.api` is not the stable collection-level API to design around.
- Use collection-only `sceneReady` when the host needs scene-level data or runtime hooks as the collection switches between internal scenes.

Choose scene pages instead of collection pages when the requirement is "open once, then control runtime content immediately."

## Pattern 7: Object Events And Cleanup

Use iframe events for process-level flow. Use `api.on()` / `api.off()` for runtime object events.

Typical structure:

```js
let api;
let currentModel;

iframe.addEventListener('ready', (event) => {
  api = event.detail.api;
});

iframe.addEventListener('loadSceneEnd', async () => {
  currentModel = await api.getObject('rabbit');
  if (!currentModel) return;
  await api.on('click', handleModelClick, currentModel);
});

function handleModelClick(payload) {
  console.log(payload);
}
```

On teardown:

- Call `api.off()` with the same callback when possible.
- Then destroy runtime objects.
- Then destroy the scene or collection.

## Pattern 8: Overlay UI And Click Forwarding

If the host overlays transparent UI above the iframe, clicks may stop reaching the inner scene. Use `dispatchTouchEvent()` only when the overlay truly needs to intercept clicks first.

Rules:

- Pass iframe-local coordinates, not arbitrary page coordinates.
- The iframe must be visible and have non-zero size.
- Pair click forwarding with normal object event listeners such as `api.on('click', ...)`.

Prefer leaving critical 3D interaction areas uncovered when possible; click forwarding is for the hard cases, not the default architecture.
