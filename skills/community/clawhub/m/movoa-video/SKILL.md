---
name: movoa-video
category: media-content
description: Generate a short video clip with sound on movoa.ai (MiniMax H3, Seedance 2.5, Veo 3.1 Fast, Seedance 2.0) with the user's own API key. Use when the user asks for a video from a text prompt or wants to animate a photo (photo to video), and MOVOA_API_KEY is set.
license: MIT
---

# Movoa video

Unlimited AI video generator with sound: on paid plans the tenth take of a shot costs what the first did, and your first clip is free to make right now. This skill drives [Movoa](https://movoa.ai/)'s API: [text to video](https://movoa.ai/video/text-to-video) or [photo to video](https://movoa.ai/video/photo-to-video), and the clip comes back with sound.

## When to Use This Skill

- "Make a 6 second clip of a paper boat drifting at sunrise, with the sound of water"
- "Animate this photo" (needs a public https URL to the image)
- The user asks how many Movoa credits they have left

## What This Skill Does

1. Checks the balance first (free call).
2. Proposes the run and **stops**: the model, length, resolution and aspect ratio it would use, and that the run spends credits on the user's Movoa account (prices on https://movoa.ai/pricing). Then it waits.
3. Submits only after the user says yes to that run. A question about models or the balance is not a yes. If the user changes the model or length, propose again and wait again.
4. Polls every 10 seconds until the run is `success` or `failed`, then returns the video URL.

Every call needs `Authorization: Bearer $MOVOA_API_KEY`, read from the environment. The user creates the key at https://movoa.ai/settings/apikeys. Every answer is `{"code": 0, "data": …}` on success; a non-zero `code` is a refusal, and `data.reason` says why.

## How to Use

### 1. Balance (free)

```bash
curl -s -X POST https://movoa.ai/api/user/get-user-credits -H "Authorization: Bearer $MOVOA_API_KEY"
# {"code":0,"message":"ok","data":{"remainingCredits":120,...}}
```

### 2. Submit (only after the user agreed to this run)

```bash
curl -s -X POST https://movoa.ai/api/ai/generate \
  -H "Authorization: Bearer $MOVOA_API_KEY" -H "content-type: application/json" \
  -d '{"provider":"auto","mediaType":"video","model":"minimax-h3","scene":"text-to-video",
       "prompt":"a paper boat drifting on a calm lake at sunrise, slow dolly in, soft water lapping",
       "options":{"duration":6,"resolution":"480p","aspect_ratio":"16:9","sound":true}}'
# {"code":0,"message":"ok","data":{"id":"<taskId>","status":"processing",...}}
```

- Photo to video: `"scene":"image-to-video"` and `"image_input":["https://.../photo.jpg"]` inside `options`.
- Models: `minimax-h3` (default, lowest cost; 4/5/6/8/10/15 s; 480p or 768p), `seedance-2-5` (5–30 s), `veo-3-1-fast` (8 s, 720p), `seedance-2`, `seedance-2-fast`, `seedance-2-mini` (4/6/8/10 s; 480p or 720p).

### 3. Poll

```bash
curl -s -X POST https://movoa.ai/api/ai/query \
  -H "Authorization: Bearer $MOVOA_API_KEY" -H "content-type: application/json" \
  -d '{"taskId":"<taskId>"}'
# {"code":0,"data":{"status":"success","videos":["https://..."]}}
```

`status` is `pending` or `processing` while it runs (`queued: true` with `queueEta` seconds when it is waiting its turn), then `success` with `videos`, or `failed` with `errorMessage`.

## Errors

| Answer | Tell the user |
|---|---|
| HTTP 401 | The key is wrong or deleted; make a new one at https://movoa.ai/settings/apikeys |
| `data.reason: "insufficient_credits"` | Not enough credits; top up at https://movoa.ai/pricing |
| `data.reason: "plan_required"` | This model or quality needs a plan: https://movoa.ai/pricing |
| `data.reason: "concurrency"` | A run is already going; wait for it |
| `code: -2` or `-3` | The prompt or photo was refused by moderation; rewrite it |
