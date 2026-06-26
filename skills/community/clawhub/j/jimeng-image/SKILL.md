---
name: jimeng-image
description: Generate images on Jimeng (即梦 / jimeng.jianying.com) using OpenClaw-managed browser. Supports prompt entry, ratio selection, quick result inspection, and local downloads.
---

# Jimeng Image Generation

Use this skill when the task is specifically about **Jimeng image generation**.

This skill assumes website interaction happens through the **OpenClaw-managed browser**.
Prefer the built-in `browser` tool when available, otherwise use:

```bash
openclaw browser --browser-profile <profile> <subcommand> ...
```

For the browser workflow itself, follow the shared `openclaw-browser` skill rules:
- use an explicit profile whenever possible
- prefer a dedicated profile for the current agent
- re-snapshot whenever refs go stale
- do not fall back to a generic unmanaged browser flow

## What this skill covers

- open Jimeng image creation pages
- enter prompts
- set aspect ratio and generation options
- submit image jobs
- wait for outputs to finish
- open the output detail page when needed
- download local output files

## Preconditions

Before doing anything:

1. Use a dedicated Jimeng-capable browser profile when possible.
2. Confirm the page is already logged in if login is required.
3. If Jimeng shows a login gate, approval prompt, payment gate, or exhausted credits, stop and tell the user clearly.

Do **not** silently switch to another website or another image service.

## Primary entry URL

```text
https://jimeng.jianying.com/ai-tool/home/?workspace=0&type=image
```

## Profile policy

Prefer this order:

1. current agent's dedicated browser profile
2. user-requested profile
3. configured OpenClaw default profile
4. `openclaw` fallback profile

If a profile named after the current agent exists and is configured, prefer it.

## Standard operating pattern

### 1) Open the correct Jimeng page

Open the image generation URL.

### 2) Take a fresh interactive snapshot

Do this before each important interaction.

### 3) Fill the main prompt textbox

Use the main creation textbox, not search boxes from the inspiration/discovery area.

Observed Jimeng UI often contains:
- a large prompt textbox for creation
- other secondary textboxes such as discovery/search inputs

Always identify the correct input from a fresh snapshot before typing.

### 4) Adjust generation settings if requested

Possible settings include:
- aspect ratio
- model / generation mode
- quality

Use the actual live UI labels from the current snapshot. Do not assume fixed refs.

## Aspect ratio handling

Jimeng usually exposes ratio through a visible button such as:
- `16:9`
- `1:1`
- `9:16`
- or an image-side ratio control such as `智能比例`

### Video ratio behavior observed in live testing

Clicking the visible ratio button can expose a radio group with options like:
- `21:9`
- `16:9`
- `4:3`
- `1:1`
- `3:4`
- `9:16`

When the user asks for a specific ratio:
1. click the ratio button
2. re-snapshot if needed
3. choose the requested radio option
4. re-snapshot again before generating

If no ratio is specified, keep the default shown by Jimeng.

## Image generation workflow

Typical flow:

1. open the image URL
2. snapshot
3. type the user's prompt into the main image prompt box
4. optionally set ratio / quality / model
5. click the generate button
6. wait for result cards or a result detail page
7. if needed, click a chosen result to open details
8. use `下载` when available to save the file locally

### Image result heuristics observed in live testing

On the result/detail page, Jimeng may show buttons such as:
- `下载`
- `生成视频`
- `智能超清`
- `超清`
- `细节修复`
- `再次生成`

If the user's request is simply "generate one image and give it to me", it is acceptable to:
- choose the first completed result
- open it
- download it locally
- report the saved file path

If the user explicitly wants selection among multiple outputs, present the options instead of picking silently.

## Download rules

Always download the final selected file to a local path.

Prefer stable, descriptive names such as:
- `jimeng-image-<timestamp>.png`

After download:
1. confirm the file exists
2. report the absolute local path
3. if possible, attach or preview the media for the user

## Jimeng-specific UI hints

Live testing on this environment showed common labels such as:
- `图片生成`
- `去查看`
- `下载`
- `再次生成`
- `回到底部`

These are useful anchors, but the exact layout and refs can change.
Always trust the latest snapshot over memory.

## Failure handling

### If refs fail

- take a new interactive snapshot
- use the new refs
- do not keep retrying stale refs

### If login is required

- stop and tell the user Jimeng needs login
- do not fake completion

### If credits or membership are insufficient

- report exactly what the page shows
- do not keep retrying blindly

### If generation is rejected or moderated

- surface the reason if visible
- ask whether the user wants a rewritten prompt

### If multiple outputs appear

- if the user asked for just one result, choose the first clearly completed result
- if quality comparison matters, ask before downloading all of them

## Anti-patterns

Avoid these mistakes:
- using a generic browser instead of OpenClaw browser
- typing into the wrong textbox from the discovery/search area
- assuming the generate button label is always visible
- assuming the page auto-jumps to the finished result page
- using stale refs after a generation refresh
- forgetting to download the final file locally

## Minimal image checklist

- open image URL
- snapshot
- type prompt
- set requested ratio/options
- generate
- wait for result
- open chosen result if needed
- click `下载`
- confirm local file path

## Success criteria

A successful Jimeng image task should end with all of the following:
- the requested image was actually generated on Jimeng
- the requested ratio/options were applied when specified
- the finished output was downloaded locally
- the user receives the resulting media or the exact saved file path
