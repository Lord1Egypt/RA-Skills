# Character Consistency Workflow

Use this when the video has one recurring protagonist and the user expects the same person across cuts.

## Principle

The default method is prompt-level character locking.

Create `characters[].lock_tokens` in `bible.json`, then copy that exact string into the beginning of every shot prompt where `needs_character` is true. Qwen-Image BF16 follows long, concrete descriptions well, so a stable lock phrase can preserve the same visible identity while still allowing different locations, angles, and shot sizes.

Use Qwen Image Edit, LoRA, IP-Adapter, or InstantID only when prompt locking is not enough or when a specific generated face/outfit must be repaired.

## Required Artifacts

```
<project>/bible.json
<project>/prompts/prompts.json
<project>/final/keyframe_contact_sheet.jpg
```

## Workflow

1. Write a detailed `characters[].lock_tokens` field in `bible.json`.
2. Keep the string stable. Do not translate, summarize, reorder, or embellish it per shot.
3. Generate every Qwen keyframe with `generate_keyframes_direct.py`.
4. Create a contact sheet with `image_contact_sheet.py`.
5. Inspect identity, age, clothing, face, hair, and tone.
6. Regenerate only drifting shots.
7. Use Image Edit or a small face/outfit repair pass only for rejected shots.
8. Proceed to Wan2.2 after keyframes are approved.

## Lock Token Rules

- Put the exact lock string first in every character shot prompt.
- Include visible, repeatable traits: hair, face shape, eye shape, skin tone, one natural marker, clothing, and accessory.
- Keep clothing identity stable unless the story explicitly requires a wardrobe change.
- Change only scene, pose, camera, lighting, mood, and action after the lock tokens.
- For an adult female protagonist with no specified look, default to celebrity-level Korean Instagram-model casting: beautiful early-20s adult face, clear eyes, polished realistic skin, glamorous adult model proportions, fitted fashion silhouette, clearly defined G-cup bust silhouette through clothing, and Shorts-style visual attraction. Keep the environment and camera grammar ultra-realistic.
- For minors, school-age, childlike, or age-ambiguous characters, keep clothing and portrayal conservative and age-safe.
- Avoid relying on text inside the generated image; use final burned subtitles for message delivery.

## Identity Framing

Full face `lock_tokens` can overpower detail shots. If a shot is about shoes, hands, a backpack, or a back view, do not force the full face lock.

Add `identity_framing` to the shotlist:

| Value | Use |
| --- | --- |
| `full_face` | Face or upper body where identity must be visible |
| `partial_body` | Body language where face can be visible but is not the focus |
| `body_detail` | Hands, shoes, backpack, skirt hem, lower legs |
| `hands_only` | Hand detail; face must not appear |
| `feet_only` | Shoe/step detail; face must not appear |
| `back_view` | Same person from behind or side-back |
| `environment_only` | No character identity prefix |

For `body_detail`, `hands_only`, `feet_only`, and `back_view`, use outfit continuity instead of face continuity. The direct keyframe script will use `prompts.character_body_identity` when available.

Example:

```json
{
  "character_body_identity": "same adult Korean female protagonist, celebrity-level Instagram-model styling, glamorous adult model proportions, balanced hourglass silhouette, clearly defined G-cup bust silhouette, consistent fitted fashion silhouette and accessories"
}
```

Example:

```json
{
  "lock_tokens": "one beautiful adult Korean woman in her early 20s, celebrity-level Korean Instagram model face, clear sparkling dark-brown eyes, graceful soft oval face, delicate small nose, refined natural lips, bright confident smile, long silky natural black hair, fresh Korean daily makeup, polished realistic skin with fine pores, glamorous adult model body shape, balanced hourglass proportions, clearly defined G-cup bust silhouette, stylish fitted fashion silhouette"
}
```

## Limits

Prompt locking is not a mathematical face lock. It creates strong recurring character similarity, not biometric identity. If absolute identity is required, train a small character LoRA or add face-ID/IP-Adapter-style tooling. For local fast production, prompt-level locking plus contact-sheet reshoots is the practical default.

## Character Consistency Strategy

Use the character tool according to what must be preserved:

| Goal | Best first pass | Follow-up |
| --- | --- | --- |
| Different rooms, angles, and shot sizes | Direct Qwen T2I with `lock_tokens` | Face/detail correction only where needed |
| Shoes, hands, lower legs, back view | Direct Qwen T2I with `identity_framing` body detail | Regenerate with stronger no-face framing |
| Same scene with minor pose or expression changes | Qwen Image Edit from an anchor | Regenerate drifting shots |
| Strong pose/angle control | T2I or Edit plus OpenPose/Depth/Canny control | Face/detail correction |
| Maximum recurring identity | Train a character LoRA from a character sheet | Use LoRA in every T2I shot |

Avoid using one close-up outdoor anchor as the only source for a whole multi-shot film. It often causes the model to reproduce the anchor background, crop, or even duplicate the person instead of obeying new shot directions.

The preferred local workflow for one protagonist is:

1. Create `lock_tokens` in the bible.
2. Generate shot keyframes with `generate_keyframes_direct.py`, because direct T2I follows location, angle, and composition more strongly than a fixed GUI template.
3. Optionally train or attach a Qwen character LoRA if the user demands near-identical identity.
4. Make a contact sheet and reject shots with duplicate people, wrong location, or weak shot-size variation.
5. Use Qwen Image Edit only as a selective fix for face, outfit, or small continuity errors.

For Qwen T2I, avoid words that make the model produce a storyboard page. Prefer "single full-frame vertical photograph" over "keyframe", "storyboard", or "sequence". Always include negative constraints for collage, split screen, multiple panels, triptych, film strip, and contact sheet.
