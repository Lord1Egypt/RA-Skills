# OpenClaw + NovelAI

## Quick Start Guide

This guide focuses on everyday use and on how to describe tasks to the agent.

Think of OpenClaw as an assistant that can operate NovelAI: describe what you want in natural language, and it can choose the appropriate capability, read your story materials, generate text or images, and save the results.

For a plain-language explanation of what is free, what uses Anlas, and how the V5 Usage Limit works, see [Costs and Quotas](COSTS-AND-QUOTAS.md).

## The basic pattern

Tell the agent:

```text
What I want + which files/images to use + the desired result + whether to estimate the cost first
```

For example:

```text
Read chapter three, find scenes that would work as illustrations, and list a plan with estimated costs. Do not generate anything yet.
```

For image generation or editing, add:

```text
Tell me the model, image size, number of generations, and estimated cost first. Wait for my confirmation before executing.
```

## 1. Story writing

### Create a story project

```text
Create a story project named “The Frontier of Stars”.
```

Add the long-term setting:

```text
This is a near-future space adventure. The main characters are Lin Che and Gu Yao. The overall style should be restrained, cold, and hopeful. Treat these as the project's long-term settings.
```

### Save story settings

You can give the agent four types of information:

- worldbuilding, character facts, and established events;
- current plot progress;
- terms, locations, organizations, and background information;
- point of view, tone, and style.

Example:

```text
Organize the following information into the project's character and world settings. Do not overwrite existing settings until I confirm.
```

### Continue a chapter

```text
Read the project settings and chapter two for “The Frontier of Stars”, then write the opening of chapter three in third-person narration, about 1,000 words. Do not change established character relationships.
```

### Plan the plot

```text
Based on the current plot, propose three directions for chapter three. For each, describe the main conflict, the character's choice, and the ending hook. Do not draft the chapter yet.
```

### Rewrite text

```text
Make this passage more tense and visual without changing the event order, character personalities, or ending.
```

You can specify a style:

```text
Preserve the meaning and rewrite it in a restrained, cold science-fiction style.
```

### Check story continuity

```text
Check this chapter for timeline contradictions, character-setting conflicts, point-of-view jumps, and continuity problems. List issues and suggestions only; do not edit the file.
```

### Summarize a chapter

```text
Summarize chapter three: list the events, changes in character state, important foreshadowing, and unresolved questions.
```

### Update story memory

```text
Based on the confirmed contents of chapter three, draft an update for memory.md. Show it to me first and wait for confirmation before saving it.
```

For worldbuilding and character settings, use a “show first, save after confirmation” rule so that an agent's guess does not become an official fact.

## 2. Choosing a text model

### Xialong

Good for story continuation, narrative extension, and natural paragraph flow:

```text
Use Xialong, follow the project settings, and continue this passage.
```

### GLM-4.6

Useful for dialogue-heavy, analytical, or reasoning-oriented tasks. Ask for streaming output:

```text
Use GLM-4.6 with streaming output to analyze this plot problem.
```

If you are unsure:

```text
Choose the most suitable NovelAI text model for this task and explain why.
```

## 3. Text-to-image

Text-to-image means generating a new image from a written description.

```text
Generate an anime illustration of a moonlit harbor: night, thin fog, wooden boats, a distant lighthouse, blue moonlight, and cinematic composition. Use V5 at 512x768, generate one image, estimate the cost first, and wait for confirmation.
```

For a clearer image description, mention these in order:

1. subject: who or what is in the image;
2. appearance: hair, clothes, age, and materials;
3. action: what the subject is doing;
4. place and time: room, street, forest, morning, or night;
5. camera and composition: close-up, full body, overhead, or subject on the left;
6. mood and lighting: warm, oppressive, foggy, or backlit;
7. things to avoid: text, watermark, blur, or extra people.

Example:

```text
Generate a half-body illustration of a silver-haired girl at a rainy train station. She wears a dark blue trench coat and holds a transparent umbrella. Neon lights reflect on the ground. The mood is quiet and lonely. No text, no watermark, and no extra people.
```

## 4. Multiple characters

When a picture contains several people, describe each character and their position:

```text
Generate two characters standing on a rainy street:
the girl has silver hair and a blue coat and stands on the left;
the boy has black hair and a red scarf and stands on the right;
they face each other and their boundaries remain clear. Use V4.5 and estimate the cost first.
```

If the characters already exist in the project:

```text
Use the project settings for Lin Che and Gu Yao. Generate an illustration of their first meeting at the moonlit harbor. Lin Che is on the left and Gu Yao is on the right. Keep their clothes and hairstyles consistent.
```

## 5. Img2img

Img2img uses an existing image as the basis for a variation.

Send the image to the agent and say:

```text
Use this image for img2img. Preserve the face, pose, and main composition, and change the background to a rainy street. Keep the change moderate, output a new image, and do not overwrite the original.
```

Common uses:

- change the background;
- change clothes;
- change lighting or weather;
- try another visual style;
- keep the pose while changing the scene;
- create several variations of the same composition.

To keep the result close to the original:

```text
Stay as close to the original as possible and change only the background.
```

To permit a larger change:

```text
Allow a substantial redesign but preserve the character identity and overall composition.
```

If you want to specify a parameter:

```text
Use Strength 0.3 and keep the result close to the source.
```

## 6. Inpainting

Inpainting modifies only a selected part of an image. Send the source image and its mask together:

```text
Use this source image and mask.png. Repair only the right hand and keep all other areas as unchanged as possible. Use the V4.5 inpainting model and estimate the cost first.
```

White mask areas normally mean “redraw” and black areas mean “preserve”.

Typical uses:

- repair hands, faces, or eyes;
- change a small clothing detail;
- remove a small object;
- add a flower, weapon, or accessory in one place;
- repair a small part of the background.

Be specific about the selected area:

```text
Turn only the masked area into a small blue flower held naturally in the character's hand. Do not change the arm or background.
```

## 7. Vibe Transfer

Vibe Transfer uses the overall style, colors, and atmosphere of a reference image to guide another image. It does not necessarily copy the people or composition.

```text
Use this reference image for its visual style and color atmosphere, then generate a small cabin in a moonlit forest. Do not copy the people in the reference. Use V4.5 and estimate the cost first.
```

To make the reference stronger:

```text
Make the reference style more influential while preserving the new scene's subject and composition.
```

To keep it subtle:

```text
Only borrow a little of the reference's colors and lighting; do not change the new scene's subject.
```

Vibe is mainly suitable for V4/V4.5. If you choose V5, ask the agent to confirm that the active tool supports this reference mode.

## 8. Character reference images

If the active tool provides character-reference support:

```text
Use this character reference to keep the face, hairstyle, and clothing consistent. Generate a full-body image of her at a snowy mountain station. The background and action may change.
```

To preserve the visual style too:

```text
Reference both the character's appearance and the original visual style, but do not copy the original composition.
```

The difference is:

- character reference: preserve who the person is;
- Vibe Transfer: borrow what the image feels like.

## 9. Tag suggestions

If you do not know how to write NovelAI tags:

```text
I want an image with silver hair, a rainy night, a blue uniform, and harbor lights. Use NovelAI tag suggestions to expand the prompt, explain what each group does, and do not generate the image yet.
```

After reviewing the prompt:

```text
Use the confirmed tags to generate one 512x768 image, and estimate the cost first.
```

## 10. Director tools

Director applies a specific transformation to an existing image. Send the image and describe the operation.

### Line art

```text
Convert this image into clean black-and-white line art. Keep the original and save the result as a new image.
```

### Sketch

```text
Convert this image into a pencil-sketch style and keep the original.
```

### Background removal

```text
Remove the background, keep the person as the main subject, and output a transparent-background image. Do not overwrite the original.
```

### Declutter

```text
Remove clutter and unwanted visual interference while preserving the person and composition as much as possible.
```

### Colorize

```text
Colorize this line drawing: silver hair, dark blue clothes, and warm yellow background light. Keep both the line drawing and the original.
```

### Emotion

```text
Make the person look happy and relaxed while preserving the facial features and composition.
```

## 11. ControlNet annotation

ControlNet annotations are auxiliary images that provide structural guidance for later generation; they are not ordinary enhancement images.

```text
Create a fake_scribble ControlNet annotation from this image and keep the original.
```

You can also ask for advice first:

```text
Which ControlNet annotation would best preserve the pose in this image? Explain first and do not execute anything yet.
```

## 12. Upscaling and enhancement

### Dedicated upscaling

```text
Upscale this image 2x with the dedicated upscaler. Check that the current upscale tool is available and tell me the estimated cost first.
```

Dedicated upscaling is different from regeneration: it is intended to preserve the original pixels and details more closely.

### Higher-resolution img2img enhancement

```text
Use img2img to enhance this image at a higher resolution. Preserve the composition and character as much as possible, do not overwrite the original, and state clearly that this is regeneration rather than pixel-preserving dedicated upscaling.
```

## 13. Account and cost checks

Query the account:

```text
Query my NovelAI subscription status and account information only. Do not generate an image.
```

Estimate a cost:

```text
Estimate the approximate Anlas cost of one V5 image at 512x768 and 8 steps. Estimate only; do not generate.
```

For a batch:

```text
I want five illustrations for chapter three. List each scene, model, dimensions, number of generations, and estimated total cost. Wait for my confirmation before starting.
```

## 14. Complete chapter-illustration workflow

Use two requests instead of asking for a batch immediately.

First plan:

```text
Read chapter three and the project character settings. Find the most suitable scenes for illustrations. For each scene, list the characters, location, action, composition, recommended model, and estimated cost. Do not generate anything yet.
```

Then execute:

```text
Generate the first two approved scenes. Generate one image at a time. Before each request, tell me the model, dimensions, steps, and estimated cost. Save each result as a new file and record the prompt, seed, and output path.
```

## 15. Save and organize results

After each generation:

```text
Save the image as a new project asset without overwriting the original. Record the model, prompt, negative prompt, seed, dimensions, and generation type.
```

Organize chapter assets:

```text
Mark the images just generated as chapter-three scene images, and list each filename with its corresponding scene.
```

Review records:

```text
List the latest images in this project with their models and prompts. Do not display any secret information.
```

## 16. Useful instruction templates

### Writing only

```text
Read the current story-project settings and continue this passage. Preserve the established character personalities and narrative style, then list the new plot facts introduced.
```

### One image

```text
Generate an illustration of [subject] doing [action] at [location] in [style]. The mood is [mood]. Use [model] at [dimensions]. Estimate the cost first and wait for confirmation.
```

### Modify an image

```text
Use this image and change [what to change] into [target effect]. Preserve [what must remain]. Output a new image and do not overwrite the original.
```

### Plan first

```text
Analyze the request and provide a plan, model, parameters, estimated cost, and tradeoffs. Do not perform any operation that may incur a charge.
```

### Conservative operation

```text
Keep every original file. Ask before generating. Perform one operation at a time. After completion, report the output file and parameters used.
```

## 17. Remember these three things

1. You can describe tasks in plain language; you do not need to remember API or tool names.
2. Text-to-image, img2img, inpainting, and Director operations may consume Anlas, so ask for an estimate and confirmation before batch work.
3. Say “preserve the original, save a new file, and record the parameters” when you want results that are easy to reproduce and manage.
