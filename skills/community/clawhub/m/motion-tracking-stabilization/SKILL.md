---
name: motion-tracking-stabilization
description: "Stabilize shaky video (non-destructive stabilizer (smoothed camera path, border-hiding zoom, rolling-shutter correction)), solve 3D camera tracker anchors, track 2D regions/points with rotation and scale, and attach graphics or props to moving hands and objects."
version: 1.0.3
author: brajendrak00068
license: MIT
---

# Motion Tracking, 3D Camera Solve, and Warp Stabilization

Track 2D regions and points with rotation and scale, attach graphics to hands or live track nulls, solve 3D camera movement for perspective scene anchors, and run non-destructive warp stabilization.

## Setup

This skill calls the Levea (livecore.ai) editing service, which requires a Levea account and API key.

1. Sign up and generate an API key at https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=motion-tracking-stabilization
2. Provide the key to the tool you use:
   - OpenClaw plugin `openclaw-ai-video-editor` (ClawHub): set `apiKey` in the plugin config.
   - MCP server `levea-mcp-server` (npm): set `LEVEA_API_KEY` in the MCP server config. `LEVEA_API_URL` is optional and defaults to `https://api.livecore.ai`.
3. Describe the edit you want in plain language; the tool returns a project ID and, after export, an MP4 URL.

## When to use

- Pinning callouts, labels, arrows, or stickers to moving objects, faces, or hands in video footage.
- Replacing flat screens, signs, or walls using planar tracking and perspective corner-pinning.
- Placing text or graphics into 3D space on floors, walls, or tables with true perspective and parallax using a monocular 3D camera solve.
- Smoothing shaky handheld or vehicle footage using non-destructive warp stabilization.

## Tool interface

Use the registered `ai-video-editor` (OpenClaw plugin) or `autonomous_edit` (MCP server) tool, or call `search_skills` / `load_skill` + `execute_action` / `execute_batch` for direct canonical control.

### Tool parameters

<!-- edit-contract:start (generated from contract/edit-contract.json — edit that file, then run node scripts/sync-contract.mjs) -->
- `prompt` (string, required): Description of the video edit to perform, in the user's own words.
- `project_id` (string, optional): Project identifier returned by a prior call; reuse it for every follow-up edit on the same video.
- `video_url` (string, optional): Public source video URL when starting a new project.
- `assets` (array, optional): Input media (video, image, audio) as public HTTP/HTTPS URLs.
- `scene` (object, optional): Existing scene/timeline state to continue editing (advanced).
- `captionTemplatePreset` (string, optional): Caption template id to apply: a builtin slug (e.g. `hormozi`, `viral-pop`, `karaoke`) or a saved template id. With the MCP server, `list_caption_templates` lists the exact ids; elsewhere, name the look in the prompt.
- `captionTemplateMode` (string, optional): How to apply `captionTemplatePreset`: one of `add`, `recreate`, `style`, `translate`, `clear`, `remove_fillers`.
- `requirePlanApproval` (boolean, optional): When `true`, pause after planning and return `workingMemory` for the user to approve.
- `workingMemory` (object, optional): State returned by a paused plan-approval call; send it back to resume.
- `editedPlan` (object, optional): The user's edited version of a plan returned by an approval pause.
- `planDecision` (string, optional): Set to `"approve"` to approve the plan from an approval pause; resend it with that response's `workingMemory`.
- `attachedImages` (array, optional): Reference image URLs for planning (style, branding).
- `style_reference_url` (string, optional): A reference video whose editing style the result should match (pacing, captions, framing, zooms, transitions, grade).
- `skills` (array, optional): Your own saved skills (save_skill) to apply to this edit, as "user/<slug>" ids. Skills saved with apply: always are applied to every edit without being named.
- `flaggedIssues` (array, optional): Specific problems the user flagged that this run must fix.
- `brandId` (string, optional): Brand kit to apply to this call.
- `projectBrandId` (string, optional): Default brand kit for the project; persists across calls.
- `core_only` (boolean, optional): Return only rendering-essential scene fields (smaller responses).
<!-- edit-contract:end -->

### Example tool input

```json
{
  "prompt": "Stabilize the shaky handheld clip without re-encoding, pin a price tag label onto the car with rotation and scale follow, and anchor a 3D title onto the floor plane as the camera moves.",
  "project_id": "project_example_01"
}
```

## Capabilities

- 2D Region & Point Tracking: feature-region tracking that measures position, in-plane rotation, and scale with per-frame confidence and occlusion recovery.
- Live Track Parenting: After Effects null-style parenting with pixel or bounding-box-relative offsets, scale follow, and rotation follow that survive later trims, splits, and speed changes.
- Hand & Palm Attachment: keypoint-based palm tracking that follows the hand, scales with depth, and hides while out of view.
- Planar & 3D Camera Tracking: 4-corner perspective pinning for screen replacement, and monocular 3D camera solve for world-anchored 3D layers.
- Non-Destructive Warp Stabilizer: camera-path smoothing with max-scale relaxation and border-hiding auto-scale.

## Response fields

- `success` (boolean): True when the edit and verification passed.
- `status` (string): One of `completed`, `waiting`, `awaiting_approval`, or `failed`.
- `projectId` (string): Active project identifier for subsequent edits.
- `projectRevision` (number): Committed project revision number.
- `videoUrl` (string, optional): Rendered MP4 download URL when export completes.
- `verificationReport` (object): `status` is `verified`, `rejected`, `unverified`, or `not_applicable`, with each failed check and what repair tried.
- `qualityNotes` (array, optional): Advisory notes about the result.
- `jobId` (string, optional): Async render job identifier for status polling via `check_job_status`.
