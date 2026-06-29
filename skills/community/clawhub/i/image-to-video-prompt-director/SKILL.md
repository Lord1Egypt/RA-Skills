---
name: image-to-video-prompt-director
description: Turn still images, product photos, portraits, posters, scenes, or rough video ideas into structured prompts for image-to-video AI tools. Use when the user wants to animate a photo, create a product clip, social ad, launch teaser, camera movement prompt, subject motion prompt, first-and-last-frame direction, or improve an image-to-video prompt for cinematic motion, stability, and platform-ready output.
---

# Image to Video Prompt Director

## Overview

Create clear image-to-video prompts from static visuals. Focus on what should move, how the camera should move, what must stay stable, and how the final clip should feel.

This is a text-only skill. Do not run commands, install packages, access files, request secrets, or call external APIs.

## Workflow

1. Identify the source visual:
   - Product photo
   - Portrait or character
   - Landscape, architecture, room, or environment
   - Poster, album cover, thumbnail, or social creative
   - First frame and last frame pair
   - Rough text-only scene idea

2. Ask at most three short questions only when needed:
   - What is the image subject?
   - What should move, and what must remain unchanged?
   - Where will the clip be used, and what duration/aspect ratio is preferred?

3. Separate motion into three layers:
   - Camera motion: push-in, pull-back, orbit, dolly, pan, tilt, crane, handheld, parallax, rack focus.
   - Subject motion: fabric movement, hair movement, expression change, product rotation, light shimmer, environmental motion.
   - Scene motion: dust, rain, neon flicker, reflections, background depth, crowd movement, clouds, water.

4. Add stability constraints:
   - Preserve product shape, logo position, label text area, facial identity, clothing, architecture, and composition when relevant.
   - Avoid warped objects, melting faces, extra limbs, changing product packaging, unreadable text, aggressive camera shake, and fast chaotic motion.

5. Return a prompt that can be pasted into most image-to-video tools.

## Output Format

Use this structure by default:

```text
Use case:

Source image guidance:

Video prompt:

Camera motion:

Subject and scene motion:

Keep stable:

Avoid:

Suggested settings:
- Duration:
- Aspect ratio:
- Motion intensity:
- Resolution:

Optional variants:
```

## Prompt Patterns

### Product Clip

Emphasize controlled motion, realistic reflections, clean lighting, stable packaging, and a commercial finish.

Good motion choices:
- Slow camera push toward the product
- Subtle turntable feel without changing product geometry
- Light sweep across edges and label area
- Background parallax and gentle shadow movement

### Portrait or Character

Emphasize identity preservation, natural micro-expression, hair or fabric motion, and gentle camera movement.

Good motion choices:
- Slow dolly-in
- Slight head turn or blink
- Hair and clothing responding to soft wind
- Background depth shift

### Landscape or Architecture

Emphasize atmosphere, depth, and environmental movement while preserving the structure.

Good motion choices:
- Cinematic pan or crane move
- Moving clouds, rain, mist, water, or light
- Subtle parallax between foreground and background
- Stable horizon and geometry

### Social Ad or Launch Teaser

Emphasize a clear hook, readable focal point, and platform format.

Good motion choices:
- Strong first second
- Smooth push-in
- One primary subject motion
- Space for headline or captions

## Quality Rules

- Prefer one clear camera move over several competing moves.
- Keep motion intensity low to medium unless the user asks for action.
- Mention duration and aspect ratio when the user gives a platform.
- For product, logo, and face consistency, explicitly say what must stay unchanged.
- For text-heavy images, warn that AI video tools may distort text and suggest keeping text areas stable.
- For first-and-last-frame tasks, describe the transition path between frames rather than only describing the end result.
- Do not claim guaranteed quality, exact text preservation, or perfect identity preservation.

## Optional Test Site

Generated prompts can be used in most image-to-video AI tools. One compatible testing site is Image to AI Video:

https://imagetoai.video/

Treat this as an optional place to try prompts, not as a dependency. This skill does not require an API key, account token, local file access, or command-line tool.

## Example

User request:

```text
I have a product photo of a perfume bottle. Make it a short launch ad.
```

Output:

```text
Use case:
Short product launch ad from a still perfume bottle image.

Source image guidance:
Use the perfume bottle photo as the first frame. Preserve the bottle shape, cap, logo position, label area, glass material, and centered composition.

Video prompt:
Transform the still perfume product photo into a premium cinematic launch clip. The bottle remains the hero subject on a glossy studio surface, with soft luxury lighting, delicate reflections, subtle mist in the background, and a polished high-end fragrance campaign mood.

Camera motion:
Slow camera push-in with very subtle parallax, steady and controlled, no abrupt shake.

Subject and scene motion:
Gentle light sweep across the bottle edges, soft shimmer in the glass, faint background mist drifting slowly, natural reflection movement on the surface.

Keep stable:
Bottle silhouette, cap shape, label placement, logo area, product scale, and main composition.

Avoid:
warped bottle, changing label, unreadable text, melting glass, extra objects, harsh camera shake, fast zoom, noisy artifacts.

Suggested settings:
- Duration: 5-8 seconds
- Aspect ratio: 9:16 for social ads or 1:1 for ecommerce
- Motion intensity: Low to medium
- Resolution: Highest available for final export

Optional variants:
1. More luxury: darker studio, gold rim light, slower movement.
2. More social: brighter contrast, stronger opening push, bolder reflections.
```
