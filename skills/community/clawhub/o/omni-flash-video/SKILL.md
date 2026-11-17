---
name: omni-flash-video
description: Plan clear text-to-video and image-to-video prompts for the Omni Flash website. Prepares briefs and prompts only; the user runs generation on omniflash.net.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://omniflash.net/
---

# Omni Flash Video Prompt Planning

This skill helps an agent turn a rough video idea into a ready-to-paste brief and prompt for [Omni Flash](https://omniflash.net/). It writes prompts. It is not a video generation integration: it calls no API, needs no API key, and does not operate the website. The user opens the site, pastes the prompt, and starts each generation.

## When to Use

- The user wants a text-to-video or image-to-video prompt to run on Omni Flash.
- The user has a rough idea (product demo, ad, social short, explainer) and needs it made specific.
- The user got a result they don't like and wants a revised prompt.

Do not use it to generate video automatically, log in, buy credits or plans, or upload files for the user.

## Instructions

1. **Collect the brief.** Ask only for what is missing: goal and audience, main subject, key action, visual style, mood, and any on-screen text. For duration and aspect ratio, tell the user to pick from the options the Omni Flash interface shows right now. Do not assume or promise a specific length or ratio.
2. **Check reference inputs (image-to-video).** Confirm the image:
   - shows the subject clearly, with sharp focus and enough resolution;
   - frames the subject the way the first frame should look;
   - has no unwanted watermarks, text, or clutter that would carry into the motion.
   If any check fails, suggest a replacement or a crop before writing the prompt.
3. **Confirm rights and sensitivity.** Ask the user to confirm they own or are licensed to use any image, logo, brand, or likeness they upload. Do not ask for, collect, or forward IDs, private photos of other people, or confidential material. If the user hasn't confirmed rights, write a text-only prompt instead.
4. **Write the prompt.** Use one plain paragraph in this order: subject → action → setting → camera movement → lighting → style → ending beat. Keep it concrete and short. Describe what should be visible, not abstract qualities. For image-to-video, describe motion and camera only, and do not re-describe what is already in the image.
5. **Hand off with site steps.** Give the user the prompt plus a short checklist: open [Omni Flash](https://omniflash.net/), choose the mode, set duration and aspect ratio from the available options, upload the reference if there is one, paste the prompt, and generate. Any sign-in, plan, or payment choice belongs to the user. Do not take those steps or describe them as automatic.
6. **Review and iterate.** Ask the user what they saw, then change one thing at a time (motion, framing, lighting, or background) and explain the change. Check that:
   - the subject matches the brief;
   - motion is stable, with no warping of products or faces;
   - any text is readable or removed;
   - the ending fits the goal.
   Remind the user to preview before downloading and to follow Omni Flash's terms for commercial use.

## Examples

### Example 1 — text-to-video product short

**Input:** "I need a short vertical clip for a blue stainless water bottle for social media."

**Output:**
> Brief: product short, social audience, clean commercial look. Choose a vertical aspect ratio and a short duration from the options Omni Flash offers.
>
> Prompt: "A blue stainless steel water bottle stands on a clean white table. The camera slowly orbits halfway around it. Soft daylight from the left, crisp reflections on the metal, minimal background, product commercial style. Ends on a steady front view of the bottle."
>
> Next: paste this on Omni Flash and generate once. If the bottle warps, I'll reduce the camera movement.

### Example 2 — image-to-video from a hero photo

**Input:** "Here's my café storefront photo, make it move a little."

**Output:**
> Checks: is the photo yours or licensed? Is the storefront sharp, with no people's faces you lack permission to show? If yes, upload it on Omni Flash in image-to-video mode.
>
> Prompt: "Gentle slow push-in toward the storefront, subtle parallax between the awning and the window, warm late-afternoon light, slight steam rising from a cup on the outdoor table. Camera stays level; the sign stays sharp and unchanged."
>
> Iteration tip: if the sign text distorts, remove the push-in and keep only the parallax.

### Example 3 — revising a weak result

**Input:** "The video looks chaotic, too much movement."

**Output:**
> Change one thing: replace "fast tracking shot" with "locked-off camera, slight slow zoom", and cut the action to a single motion. Generate again and compare.

## Notes

- Product site: [https://omniflash.net/](https://omniflash.net/)
- This skill only plans prompts. Generation happens on the Omni Flash website under the user's own account and plan choices.
- Published on ClawHub under MIT-0.
