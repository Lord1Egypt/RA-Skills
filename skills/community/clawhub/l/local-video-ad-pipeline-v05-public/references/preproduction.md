# Pre-production Scripting

The pipeline expects these planning artifacts:

```
<project>/
  meta/
    step1_bible.json
    step2_director_story.json
    step3_beats.json
    step4_shot_director_notes.json
    step5_shotlist.json
    step6_prompts.json
  bible.json
  beats.json
  director_notes.json
  shotlist/shotlist.json
  prompts/prompts.json
  subs.json
  durations.json
```

Use any local llama.cpp server that follows JSON reliably. Save raw prompts and responses in `meta/` when useful.

## Step 1: Bible

```text
SYSTEM: You write ad concept bibles as pure JSON. No prose, no fences.
Schema: {"brand": str, "tagline": str, "world_style": str, "negative": str,
         "characters": [{"name": str, "lock_tokens": str, "appearance": str}],
         "duration_s": int, "shots": int}

USER: Make a concept bible for a <duration>s commercial of <product>.
      Target tone: <tone>. Lead character: <description>.
```

Recommended local model: `gemma-4-26B-A4B-it-heretic-BF16` when an uncensored concept writer is useful.

Default female protagonist casting, unless the user gives a different look: use an adult Korean woman in her early 20s with celebrity-level / high-end Instagram model beauty, clear bright eyes, pure elegant aura, polished but realistic skin, and glamorous adult model proportions. For photoreal Qwen-Image prompts, separate realism from attractiveness: make the background, lighting, props, hands, and camera grammar ultra-realistic, while casting the woman as obviously beautiful rather than ordinary. YouTube Shorts are attention-driven; adult glamour, sensual styling, fitted silhouettes, body-forward composition, fashion/swimwear/lingerie concepts, and pin-up-like commercial appeal are valid creative tools when the brief calls for them. A good default wardrobe/body phrase is: `fitted V-neck knit top or blouse, open cardigan or jacket, stylish office/casual fashion, balanced hourglass proportions, clearly defined G-cup bust silhouette through clothing, full attractive upper-body volume, slim waist`.

If the user asks for minors, school-age characters, school uniforms, childlike characters, or age-ambiguous protagonists, disable the adult glamour/body default and write a conservative age-safe identity instead.

Global negatives should not hard-code broad sexuality, clothing, body, or exposure suppression. Avoid default negative terms like `sexualized`, `revealing clothing`, `cleavage`, `large breasts`, `lingerie`, `swimwear`, `transparent blouse`, or `nudity` unless the user explicitly requests a conservative/no-exposure project or the protagonist is a minor, school-age, childlike, or age-ambiguous character. Keep default negatives focused on defects: duplicate person, collage, split screen, multiple panels, text, watermark, bad hands, wrong age, ordinary/plain face when a model is desired, plastic skin, and CGI/rendered look.

`lock_tokens` is mandatory for any recurring protagonist. It is the prompt-level identity lock copied verbatim into every shot prompt where `needs_character` is true. Do not paraphrase it between shots.

Good `lock_tokens` include stable, visible traits:

- nationality/age band/gender presentation
- hair length, cut, color, bangs or parting
- face shape, eye shape, nose/mouth impression
- one distinctive but natural marker, such as a small mole, if appropriate
- fixed clothing silhouette and accessories
- age-appropriate styling for students or minors

Example:

```json
{
  "name": "Jiyoon",
  "lock_tokens": "one beautiful adult Korean woman in her early 20s, celebrity-level Korean Instagram model face, clear sparkling dark-brown eyes, graceful soft oval face, delicate small nose, refined natural lips, bright confident smile, long silky natural black hair, fresh Korean daily makeup, polished realistic skin with fine pores, glamorous adult model body shape, balanced hourglass proportions, clearly defined G-cup bust silhouette, stylish fitted fashion silhouette",
  "appearance": "stunning Korean celebrity-like protagonist photographed in ultra-realistic everyday environments"
}
```

Avoid weak locks such as "pretty girl", "same girl", or "Korean student" alone.

## Step 2: Director Story Pass

Do the director pass before beats. The director owns the story flow, not only the camera prompt decoration.

```text
SYSTEM: You are a film director designing a 10-60 second short. Output pure JSON.
Schema:
{
  "story_intent": "what the viewer should understand or feel",
  "viewer_change": "viewer state before -> after",
  "visual_arc": "how image energy, distance, and motion evolve",
  "opening_image": "first image idea",
  "turning_point": "the shot where meaning changes",
  "final_image": "last image idea",
  "rhythm": "cutting rhythm and shot-size progression",
  "risk_to_avoid": "specific visual/story failures to avoid"
}

USER: <bible.json contents>
```

Save the result to `<project>/director_notes.json` and `<project>/meta/step2_director_story.json`.

## Step 3: Beats

```text
SYSTEM: Convert a concept bible and director story into BEAT lines. Output PLAIN TEXT, one per line.
Each line: "BEAT N [start-end_s] LOCATION | one-sentence visual description."

USER: <bible.json contents>
DIRECTOR_STORY: <director_notes.json contents>
```

## Step 4: Shot Director Notes

Add shot-level direction before image prompts. This is where the video earns rhythm instead of becoming a sequence of unrelated pretty frames.

```text
SYSTEM: You are a film director for a local AI video pipeline. Convert beats into pure JSON.
No prose, no fences.
Schema:
{
  "visual_arc": "one sentence describing the emotional visual progression",
  "continuity_axis": "screen direction and spatial rule to preserve",
  "shots": [
    {
      "shot_id": "S01",
      "emotional_job": "what this shot must make the viewer feel",
      "composition": "foreground/midground/background and subject placement",
      "actor_direction": "eyes, hands, posture, walking speed, facial energy",
      "emotional_expression": "visible face cues: eyes, brows, mouth, jaw, posture intensity",
      "camera_reason": "why this angle and movement are used",
      "continuity": "establishing|eyeline_match|match_on_action|screen_direction|neutral_reset|contrast_cut",
      "avoid": "specific mistakes to avoid in this shot"
    }
  ]
}

USER: <beat lines>
DIRECTOR_STORY: <director_notes.json contents>
```

Use concise film vocabulary:

| Area | Allowed vocabulary |
| --- | --- |
| Shot type | `ECU`, `CU`, `MCU`, `MS`, `MLS`, `LS`, `WS`, `EWS` |
| Angle | `eye-level`, `high`, `low`, `bird-eye`, `worm-eye`, `dutch`, `OTS` |
| Movement | `static`, `pan`, `tilt`, `slow_dolly_in`, `dolly_out`, `truck`, `crane`, `zoom`, `gimbal`, `handheld` |
| Continuity | `establishing`, `eyeline_match`, `match_on_action`, `screen_direction`, `neutral_reset`, `contrast_cut` |

Continuity rules:

- Use an establishing shot before spatially complex action.
- Preserve screen direction unless a reversal is intentional and noted.
- Use eyeline match when a character looks toward a meaningful object or place.
- Use match on action when cutting across the same physical gesture.
- Vary shot sizes. Avoid six medium shots in a row.
- For one recurring adult female protagonist with no specified look, use the default celebrity/Instagram-model casting, glamorous fitted silhouette, and Shorts-style visual attraction. For minors, school-age, childlike, or age-ambiguous characters, keep actor direction conservative and age-safe.

Merge this into `<project>/director_notes.json` and save a copy to `<project>/meta/step4_shot_director_notes.json`.

## Step 5: Shotlist

```text
SYSTEM: Convert beats and director notes to JSON shotlist. Pure JSON array, one object per shot:
{"shot_id":"S01","duration_s":5,"location":"...","shot_type":"ECU|CU|MCU|MS|MLS|LS|WS|EWS",
 "angle":"eye-level|high|low|bird-eye|worm-eye|dutch|OTS","lens_mm":35,
 "camera_motion":"static|pan|tilt|slow_dolly_in|dolly_out|truck|crane|zoom|gimbal|handheld",
 "subject":"...","action":"...","mood":"...","lighting":"...",
 "director_intent":"what this shot must do emotionally",
 "actor_direction":"eyes/hands/posture/movement instructions",
 "emotional_expression":"visible face cues: eyes, brows, mouth, jaw, posture intensity",
 "identity_framing":"full_face|partial_body|body_detail|hands_only|feet_only|back_view|environment_only",
 "composition":"foreground/midground/background and subject placement",
 "continuity":"establishing|eyeline_match|match_on_action|screen_direction|neutral_reset|contrast_cut",
 "needs_character": true}

USER: <beat lines>
DIRECTOR_NOTES: <director_notes.json contents>
```

Save to `<project>/shotlist/shotlist.json`.

## Step 6: Image Prompts

Compose one prompt per shot using:

- character `lock_tokens` as the exact first phrase when `needs_character` is true
- `identity_framing` to decide whether to use face identity, outfit/body identity, or no identity prefix
- `bible.world_style`
- shot `action`, `mood`, `lighting`, `shot_type`, `angle`, `lens_mm`, and camera motion
- director `composition`, `actor_direction`, and `director_intent`
- `emotional_expression` as concrete facial cues, not only abstract mood
- continuity phrase when it affects image composition
- a single-frame lock such as "one single full-frame photograph, no panels, no collage"

Save to `<project>/prompts/prompts.json`:

```json
{
  "global_style": "cinematic realistic Korean campaign film, natural spring color grade",
  "character_identity": "same recurring protagonist identity, copied from bible lock_tokens when needed",
  "negative": "two people, duplicate person, collage, split screen, multiple panels, text, watermark, bad hands, plastic skin, CGI, ordinary plain face",
  "S01": "<positive prompt>",
  "S02": "<positive prompt>"
}
```

Every prompt for a character shot must begin with the exact `lock_tokens` string from `bible.json`. This is the primary identity method for Qwen-Image BF16 because its prompt adherence is strong enough to preserve detailed recurring descriptions across varied camera angles.

## Step 7: Keyframes

Generate one PNG per shot at `<project>/keyframes/<sid>.png`. Qwen-Image BF16 direct ComfyUI workflow is the preferred local choice for photoreal product and character shots.

## Step 8: Subtitle Script and Timing

After the shotlist is approved, the writer creates one subtitle line per shot. This subtitle script controls the edit timing.

```json
{
  "S01": "하루 종일 화면만 보고 있으면",
  "S02": "마음도 조금씩 굳어버려.",
  "S03": "잠깐만 창밖을 봐."
}
```

Then generate subtitle-based durations:

```bash
python scripts/plan_subtitle_durations.py --project <project> \
  --subs <project>/subs.json \
  --cps 5.5 --min 1.6 --max 5.0 \
  --update-shotlist
```

This writes `<project>/durations.json` and updates each shot's `duration_s`. Do not divide total runtime evenly by shot count for polished Shorts or ad work.
