# OpenClaw + NovelAI

## Full User Manual

This manual is for people who use OpenClaw with NovelAI. It explains the first-time setup, how to give the agent instructions, what each feature does, and how to handle common situations.

This manual corresponds to the `openclaw-novelai` Skill and the `novelai-image-mcp==0.4.0` reference configuration.

## 1. What each part does

This is not a standalone chat application. Several parts work together:

| Part | Responsibility |
| --- | --- |
| OpenClaw | Receives your messages, calls the AI, reads/writes files, and connects external tools |
| `SKILL.md` | Tells the agent when to use each tool and how to apply safety and failure rules |
| NovelAI text model | Story continuation, rewriting, plot analysis, and text generation |
| NovelAI Image MCP | Text-to-image, img2img, inpainting, Vibe, Director, and other image operations |
| `project_state.py` | Manages story settings, memory, lorebook, style, and generation records |

After the Skill is available, you normally do not need to remember API requests. Describe what you want in natural language and let OpenClaw choose the appropriate capability.

## 2. First-time setup

### 2.1 Unpack the files

Extract the package to a stable directory, for example:

```text
D:\OpenClaw\openclaw-novelai\
```

The extracted directory should contain these files and folders at its root:

```text
SKILL.md
README.md
docs\
examples\
scripts\
tests\
```

Keep the `scripts` directory together with `SKILL.md`; the project-state helper is part of the workflow.

### 2.2 Prepare the software

The reference deployment needs:

- OpenClaw;
- Python 3.13;
- `uv` / `uvx`;
- an active NovelAI subscription;
- a NovelAI Persistent API Token.

The pinned `novelai-image-mcp==0.4.0` release requires Python 3.13–3.13.x. Python 3.12 is not a substitute for this MCP Server runtime.

### 2.3 Configure the Token

On Windows, configure the credential through the Environment Variables UI:

1. Open **Edit the system environment variables**;
2. click **Environment Variables**;
3. create a user variable:
   - name: `NOVELAI_TOKEN`
   - value: your NovelAI Persistent API Token
4. save the change and restart the terminal and OpenClaw Gateway.

Never send the Token to the agent in chat or write it into this manual, a prompt, command line, ordinary configuration file, log, or generation record. If a Token has appeared in a conversation, revoke it and create a replacement after testing.

### 2.4 Install the local Skill

Recent OpenClaw versions can install a Skill from an extracted local directory:

```powershell
openclaw skills install "D:\OpenClaw\openclaw-novelai" --as openclaw-novelai
```

Then inspect it:

```powershell
openclaw skills list
openclaw skills info openclaw-novelai
openclaw skills check
```

If the Skill is loaded through an extra skills directory instead, make sure the selected directory directly contains `SKILL.md`.

OpenClaw Skill CLI reference: <https://github.com/openclaw/openclaw/blob/main/docs/cli/skills.md>

### 2.5 Configure the text model and image MCP

The file:

```text
../examples/openclaw.config.example.json5
```

is a configuration skeleton. Ask the agent to merge the relevant fields into the existing OpenClaw configuration; do not overwrite unrelated channels, models, or permissions.

The important relationship looks like this:

```json5
models: {
  providers: {
    novelai: {
      baseUrl: "https://text.novelai.net/oa",
      api: "openai-completions",
      apiKey: "${NOVELAI_TOKEN}",
      models: [
        { id: "xialong-v1", name: "NovelAI Xialong", input: ["text"] },
        { id: "glm-4-6", name: "NovelAI GLM-4.6", input: ["text"] },
      ],
    },
  },
},
mcp: {
  servers: {
    "novelai-image": {
      command: "uvx",
      args: ["--from", "novelai-image-mcp==0.4.0", "novelai-image-mcp", "serve"],
      env: {
        NOVELAI_TOKEN: "${NOVELAI_TOKEN}",
      },
    },
  },
},
```

`apiKey` and `env.NOVELAI_TOKEN` are environment-variable references. Do not replace `${NOVELAI_TOKEN}` with a real value before committing or sharing the file. SecretRef behavior can vary by OpenClaw version, so use the current host documentation when selecting a secret provider.

If a sandbox is enabled, MCP tools may also need to be allowed:

```json5
tools: {
  sandbox: {
    tools: {
      alsoAllow: ["bundle-mcp"],
    },
  },
},
```

### 2.6 Check the MCP connection

After restarting the OpenClaw Gateway, run or ask the agent to run:

```powershell
openclaw mcp doctor novelai-image --probe
openclaw mcp probe novelai-image --json
```

The server should expose tools similar to:

```text
generate_image
image_to_image
inpaint
upscale_image
director_tool
annotate_image
suggest_tags
encode_vibe
get_subscription
get_user_data
estimate_anlas_cost
```

The host may display names with a server prefix such as `novelai-image__generate_image`; that is normal.

OpenClaw MCP reference: <https://github.com/openclaw/openclaw/blob/main/docs/tools/mcp.md>

## 3. First conversation

Do not start with a large batch of images. Send this first:

```text
Please check whether the openclaw-novelai Skill is loaded and list the available NovelAI text models and image MCP tools. Only inspect the connection and tool catalog; do not generate an image. Confirm that NOVELAI_TOKEN is read from the secure host environment, but do not display its value.
```

Then perform a no-generation account check:

```text
Query my NovelAI subscription status and estimate the approximate cost of one 512x768 image at 8 steps. Do not generate an image yet.
```

If the agent can list the tools, query the account, and provide an estimate, the basic workflow is ready.

## 4. Story projects

### Create a project

```text
Create a story project named “The Frontier of Stars” and use this project directory for all future chapters.
```

The Skill uses `project_state.py` to create a structure like:

```text
novelai-projects/
└─ The Frontier of Stars/
   ├─ canon.md
   ├─ memory.md
   ├─ lorebook.md
   ├─ style.md
   ├─ chapters/
   ├─ images/
   └─ metadata\generations/
```

The files are used for:

- `canon.md`: worldbuilding, character facts, and other facts that must not change casually;
- `memory.md`: current plot summary and state;
- `lorebook.md`: terms, locations, organizations, and background information;
- `style.md`: point of view, tone, pacing, and formatting;
- `chapters/`: chapter drafts;
- `images/`: chapter illustrations and edited images;
- `metadata/generations/`: model, seed, prompt, and other generation records.

### Continue a chapter

```text
Read the canon, memory, lorebook, and style for “The Frontier of Stars”, then continue chapter three. Use third-person narration, write 800 words, and do not change established character facts.
```

### Plan the plot first

```text
Read chapter two and the project context. Propose three directions for chapter three, including the conflict, character change, and ending hook for each. Do not draft the chapter yet.
```

### Rewrite and review

```text
Check chapter three for character contradictions, timeline problems, point-of-view jumps, and continuity errors. List issues and suggestions only; do not edit the file.
```

```text
Make this passage more tense and visual while preserving all plot facts, character relationships, and the ending.
```

### Update story memory

```text
Summarize chapter three and draft an update for memory.md. Show me the draft first and wait for confirmation before saving it.
```

Use a “show first, save after confirmation” rule for `canon.md` and `memory.md`. This prevents a guess from becoming an official story fact.

## 5. Image workflows

### General guidance

Before each image operation, specify as many of these as possible:

- model;
- image dimensions;
- steps and sample count;
- positive prompt;
- negative prompt;
- reference-image settings;
- whether to estimate Anlas first;
- whether the result must be saved as a new file.

If you have not chosen parameters, ask for a proposal instead of allowing an automatic batch.

Common models:

| Use | Model ID |
| --- | --- |
| V5 text-to-image | `nai-diffusion-5-full` |
| V4.5 text-to-image and img2img | `nai-diffusion-4-5-full` |
| V4.5 inpainting | `nai-diffusion-4-5-full-inpainting` |

512x768 is a low-cost test size. Dimensions normally need to be multiples of 64.

### Text-to-image

```text
Generate an anime illustration of a moonlit harbor: night, thin fog, wooden boats, a distant lighthouse, cinematic composition, and blue moonlight. Use V5 at 512x768 with 8 steps. Estimate the cost first and wait for confirmation. Save the result as a new file and record the model, seed, and prompt.
```

The corresponding tool is `generate_image`.

### Multiple characters

```text
Generate two characters standing on a rainy street: a silver-haired girl in a blue coat on the left, and a black-haired boy with a red scarf on the right. Use V4.5 and keep the two character positions distinct. Estimate the cost first.
```

The agent should use character prompts and positions instead of mixing both characters into one undifferentiated prompt.

### Img2img

Upload the image to OpenClaw or provide a path the agent can access:

```text
Use this image for img2img. Keep the face and main composition, change the background to a rainy street, use Strength 0.3, do not overwrite the original, and save the result as a new file.
```

Lower Strength normally keeps more of the original; higher Strength permits larger changes.

### Inpainting

You need a source image and a mask:

```text
Use this source image and mask.png. Redraw only the right hand and keep all unmasked areas as unchanged as possible. Use the V4.5 inpainting model and tell me the estimated cost first.
```

The corresponding tool is `inpaint`. In the usual black-and-white convention, white areas are redrawn and black areas are preserved; follow the actual tool signature if it documents a different convention.

### Vibe Transfer

```text
Use style.png to extract the overall visual style, then generate a small cabin in a moonlit forest. Do not copy the people or composition from the reference. Use V4.5 and estimate the cost first.
```

The workflow is `encode_vibe` followed by `generate_image`. Vibe is mainly suitable for V4/V4.5; ask the agent to verify support before using it with V5.

### Tag suggestions

```text
I want an image with silver hair, a rainy night, a blue uniform, and harbor lights. Use NovelAI tag suggestions to expand the prompt, show me the final prompt, and do not generate the image yet.
```

The corresponding tool is `suggest_tags`.

### Director tools

```text
Convert this image into clean line art. Keep the original and save the result as a new file.
```

```text
Remove the background from this image without overwriting the original.
```

```text
Colorize this line drawing with silver hair, dark blue clothes, and warm yellow background light. Keep both the line drawing and the original.
```

```text
Make the person in the image look happy and relaxed while preserving the facial features and composition.
```

The Director types are:

- `lineart`: line art;
- `sketch`: sketch;
- `bg-removal`: background removal;
- `declutter`: remove clutter and visual interference;
- `colorize`: colorize an image;
- `emotion`: change the character's emotion.

The corresponding tool is `director_tool`.

### ControlNet annotation

```text
Create a fake_scribble ControlNet annotation from this image and keep the original.
```

The corresponding tool is `annotate_image`. It creates a structural control image; it is not a general enhancement or upscaling tool.

### Upscaling and enhancement

The intended request for a dedicated upscaler is:

```text
Upscale this image by 2x using the dedicated upscaler. Check that the current upscale tool is available and tell me the estimated cost first.
```

The dedicated `/ai/upscale` route returned 404 during the reference test, so do not assume `upscale_image` is available. A different fallback is:

```text
Use img2img at a larger resolution to enhance this image while preserving the composition and characters. State clearly that this is regeneration, not pixel-preserving dedicated upscaling.
```

## 6. Chapter illustration workflow

Ask for planning first:

```text
Read chapter three and the character settings for “The Frontier of Stars”. Find the best scenes for illustrations. For each scene, list the time, location, characters, action, composition, recommended model, and estimated cost. Do not generate anything yet.
```

After confirming the plan:

```text
Generate the first two approved scenes. Generate one image at a time; before each request, report the model, dimensions, steps, and estimated cost. Save every result as a new file and record the prompt, negative prompt, seed, and output path.
```

This is safer and usually produces more consistent results than asking for ten images in one sentence.

## 7. Generation records and files

After a generation, you can say:

```text
Save the image as a new project asset without overwriting the original. Record the model, prompt, negative prompt, seed, dimensions, generation type, and output path. Do not store any Token or Authorization value.
```

A useful record contains:

- timestamp;
- tool name;
- model;
- positive and negative prompts;
- dimensions, steps, and seed;
- reference-image paths and strengths;
- output path;
- whether the result was txt2img, img2img, inpainting, or a Director result.

Keep originals, edited results, and intermediate outputs in separate files.

## 8. Costs and confirmation

See [Costs and Quotas](COSTS-AND-QUOTAS.md) for the detailed Anlas and Opus/V5 rules. In short, text generation, account queries, cost estimates, tag suggestions, and local project records do not consume NovelAI Anlas. Image-producing operations may be free only under the active Opus conditions described in that document.

These operations require a cost check before execution:

- text-to-image;
- img2img;
- inpainting;
- Vibe encoding and use;
- Director tools;
- dedicated upscaling;
- high resolutions and multiple samples.

V5 free generations consume a separate rechargeable Usage Limit even when the estimated Anlas cost is zero. Do not treat the current approximate daily refill rate as a fixed daily quota.

Use this wording for cautious operation:

```text
Estimate the cost first and show the model, dimensions, steps, sample count, and estimated Anlas. Do not generate until I confirm.
```

Start with one single, low-cost image before trying a batch or a high-resolution request. Check the estimate rather than assuming that a UI size label is free.

## 9. Common problems

### The agent cannot find the Skill

Check that the extracted directory directly contains `SKILL.md` and that the Skill is installed for the active Agent rather than merely sitting in a download folder.

### The MCP tool list is empty

Check `uvx`, Python 3.13, the Gateway's environment, the Gateway restart, and the sandbox MCP allowlist. Ask the agent to inspect the output of `openclaw mcp doctor novelai-image --probe`.

### HTTP 401

The Token is missing, expired, invalid, or was not passed to the MCP Server. Never send it in chat; check the host-managed credential source.

### HTTP 402

The subscription or Anlas balance is insufficient. Do not retry automatically; query the account and estimate the operation first.

### HTTP 400

The model, image, mask, dimensions, or parameters may be invalid. Ask for the active tool signature and a redacted error field.

### HTTP 429

The account may be rate- or concurrency-limited. Stop parallel generation and wait before making one small retry.

### GLM-4.6 returns 200 but no text

The reference test found that GLM-4.6 streaming chat works while a non-streaming request may return HTTP 200 with empty text. Ask OpenClaw to use streaming or switch to Xialong.

### Dedicated upscaling returns 404

The current `/ai/upscale` route may be unavailable. Do not retry indefinitely; use larger-resolution img2img or a local upscaler and describe the difference.

## 10. Recommended first-run instruction

Give the agent the package and this message:

```text
Please unpack and read README.md, SKILL.md, docs/FULL-USER-MANUAL.md, docs/QUICK-START.md, docs/COSTS-AND-QUOTAS.md, and COMPATIBILITY.md.

First inspect the current OpenClaw, Python, uv, uvx, Skill search path, and MCP configuration. Do not install anything, modify configuration, or generate an image immediately. Do not ask for, print, or record the value of NOVELAI_TOKEN; only check whether it is available through the secure host environment.

List:
1. the installed OpenClaw version;
2. the Python and uvx versions;
3. whether the Skill is loaded;
4. whether the NovelAI text provider is configured;
5. whether NovelAI Image MCP passes doctor/probe;
6. any missing dependency or permission.

First show the planned actions and risks and wait for confirmation before installing or changing anything. After configuration, begin with MCP tool discovery and an account query rather than a batch generation.
```

## 11. References

- OpenClaw Skill CLI: <https://github.com/openclaw/openclaw/blob/main/docs/cli/skills.md>
- OpenClaw MCP: <https://github.com/openclaw/openclaw/blob/main/docs/tools/mcp.md>
- NovelAI Image MCP: <https://github.com/xinvxueyuan/NovelAI-Image-MCP>
- NovelAI image models: <https://docs.novelai.net/en/image/models/>
- NovelAI text models: <https://docs.novelai.net/en/text/models/>
- NovelAI Persistent API Token: <https://docs.novelai.net/en/text/usersettings/account/>
