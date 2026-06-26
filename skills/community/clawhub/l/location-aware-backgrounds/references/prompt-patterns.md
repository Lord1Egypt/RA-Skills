# Location-Aware Background Prompt Patterns

## Background Plate Template

```text
{Aspect-ratio} background plate for a native app, dashboard, or product UI in {location}, on {date} at {local time}, with {weather} in {season}. Use only place and atmosphere details the user provided or explicitly asked to look up.
Visual style: {style direction from caller}. Medium: {caller medium or rendering language}. Rendering quality: crisp premium rendering.
Use a real city cue such as {local cue} only when it strengthens the composition. Keep it integrated into a layered city scene rather than isolated as the hero subject.
Compose as a calm UI background: broad clean negative space where the interface sits, a softly illuminated lower area if the UI needs grounding, a grounded foreground plane, and details pushed to the edges and distant horizon.
No characters, no text, no logos, no postcard framing, no dramatic camera angle, no busy foreground props, no washed-out haze, no giant block clouds, no floating island diorama.
```

## Portrait Variant

```text
Portrait background plate for an app or wallpaper, explicitly set in {location} during {time-of-day} with {weather}. Use only place and atmosphere details the user provided or explicitly asked to look up.
Visual style: {style direction from caller}. Rendering quality: polished, highly readable, crisp premium fidelity.
Use one real city cue such as {landmark or neighborhood cue} only if it helps the scene read as {location}; integrate it into the background or side depth rather than centering it as a monument.
Reserve the upper left and upper center as quiet low-detail space for UI, keep the lower center open and gently grounded, and build layered foreground, midground, and skyline or waterline depth.
No people, no text, no central monument, no sharp realism, no cluttered street scene, no washed-out lighting, no giant cloud slab, no floating platform.
```

## Landmark Strategy

Strong landmark types:

- skyline edge
- bridge silhouette
- harbor haze
- brownstone block
- park edge
- rooftop garden

Prefer these landmark treatments:

- distant
- partially obscured by cloud, fog, or blue-hour haze
- implied by silhouette rather than exact documentary detail

Avoid:

- front-and-center landmarks
- heavy tourism framing
- landmarks that consume the same visual area needed by the UI

## Safety Notes

- Treat location, time, weather, and screenshots as user-provided or explicitly approved inputs.
- Do not assume access to device state or local files unless the environment exposes them and the user asked for them.
- When a lookup is not approved, use only the provided inputs.

## Review Criteria

Choose winners that:

- keep the intended UI zone readable
- keep the center from becoming busy unless the caller wants a hero scene
- feel local without becoming literal
- match the caller's style direction
- can support repeated use without becoming visually tiring
