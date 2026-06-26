---
name: imagetovideoai-motion-brief-planner
description: Plan image-to-video briefs for Image to Video AI. Use when a user wants to turn a still image, product visual, concept art, or campaign asset into a clear motion brief with scene direction, camera movement, style notes, prompt variants, and QA checks for short AI video generation.
---

# Image to Video AI Motion Brief Planner

Use this skill to prepare practical image-to-video briefs for Image to Video AI.
Image to Video AI helps creators, marketers, designers, and product teams turn still images into short motion-rich videos: https://imagetovideoai.pro/

## Workflow

1. Identify the source asset:
   - Product image
   - Portrait
   - Concept art
   - Marketing visual
   - Social media creative
   - Ecommerce image
   - Storyboard frame
2. Define the intended output:
   - Product promo
   - Ad concept
   - Social clip
   - Landing page hero video
   - Storytelling shot
   - Before-and-after transformation
   - Cinematic motion test
3. Capture constraints:
   - Aspect ratio
   - Video duration
   - Target platform
   - Desired mood
   - Motion intensity
   - Camera movement
   - Brand or product details that must stay stable
4. Draft the motion brief:
   - Main subject
   - Scene setting
   - Camera direction
   - Subject motion
   - Background motion
   - Lighting and atmosphere
   - Style references
   - Negative constraints
5. Create 2-4 prompt variants:
   - Conservative motion
   - Cinematic motion
   - Social ad motion
   - Product showcase motion
6. Add QA checks:
   - Product shape remains consistent
   - Text and logos are not distorted
   - Motion does not conflict with the original image
   - Camera movement supports the message
   - Output fits the intended platform

## Output Format

Use this structure by default:

```markdown
## Assumptions

## Motion Goal

## Image-to-Video Brief

## Prompt Variants

## Negative Prompt / Constraints

## QA Checklist
```

## Quality Rules

- Keep the brief specific enough to guide video generation, but not so rigid that it blocks creative motion.
- Prefer natural, plausible motion over excessive effects.
- Preserve key product and brand details when the source image contains commercial assets.
- Avoid promising exact model behavior unless the user has tested it.
- If the input image has text, logos, faces, hands, or fine product details, flag those as areas to review carefully after generation.
