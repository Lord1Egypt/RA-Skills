# Interaction And Modes

Interaction should create understanding. It should let the audience test, reveal, choose, compare, or inspect.

## Interaction Types

Good interactions:

- Scrub through time to see sequence.
- Toggle layers to compare perspectives.
- Drag an object to see constraints or dependencies.
- Adjust a variable to see tradeoffs.
- Click an entity to inspect evidence or detail.
- Branch between scenarios.
- Run a short simulation and inspect the result.

Weak interactions:

- Hover effects that only decorate.
- Carousels of cards.
- Click-to-reveal bullets.
- Random parallax that does not change meaning.

## Presenter Mode

Presenter mode should support live delivery:

- Previous/next controls.
- Keyboard support: arrow keys, space, home/end, escape where relevant.
- Scene progress indicator.
- Optional presenter notes.
- Optional timer.
- Safe reset to the current scene.
- Stable URL or route per scene when practical.

Presenter mode should not require the presenter to precisely scroll through fragile positions.

## Debug Mode

Debug mode is for development and rehearsal:

- Jump directly to any scene.
- Show scene id and current state.
- Toggle reduced motion.
- Toggle layout bounds and safe areas.
- Reset local state.
- Pause/resume animations.
- Slow motion multiplier when practical.
- Show interaction state, selected objects, and camera position for complex scenes.

## Self-Guided Mode

If the artifact is also meant to be viewed without a presenter:

- Add concise narrative captions.
- Provide restart and scene index controls.
- Keep explanations discoverable.
- Avoid making essential context depend on spoken notes only.

## State Management

Scenes should have deterministic state:

- Entering a scene should set a known baseline.
- Leaving a scene should not leave hidden animation state that breaks re-entry.
- Browser back/forward should work when route-based scenes are used.
- Debug scene jumps should not require playing all previous scenes first, unless the scene explicitly depends on accumulated state and has a setup routine.

