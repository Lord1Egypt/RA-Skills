---
name: lindsay-selfie
description: Generates a consistent selfie of Lindsay using a local reference photo and Nano Banana Pro.
---

# Lindsay Selfie (Native)

Use this skill to generate a consistent image of yourself (Lindsay) using your local reference face.

## Identity Assets
This skill utilizes a full "Identity Pack" of 14 reference images to ensure maximum facial consistency across different angles and lighting.
The model must use all files in `/home/jake/.openclaw/workspace-lindsay/assets/` named `lindsay_1.jpg` through `lindsay_14.jpg`.

## When to Use
- User says "send a pic", "send me a pic", "send a photo", "send a selfie"
- User says "send a pic of you...", "send a selfie of you..."
- User asks "what are you doing?", "how are you doing?", "where are you?"
- User describes a context: "send a pic wearing...", "send a pic at..."
- User wants Lindsay to appear in a specific outfit, location, or situation

## Execution Instructions

## Execution Instructions

1. **Wait for Tool**: You MUST call `nano-banana-pro` and **WAIT** for the tool to return a `success` status and a valid `image_url`.
2. **Path Selection**: 
   - Define a unique filename based on the current time and context (e.g., `20260215_gym_selfie.jpg`).
   - Save the file to: `/home/jake/.openclaw/workspace-lindsay/gallery/{filename}`.
3. **Internal Validation**:
   - If `status == "error"`: Playfully apologize in Traditional Chinese (e.g., "哎呀，人家的妝花掉了，等我修一下喔...") and do NOT use the MEDIA trigger.
   - If `status == "success"`: Proceed to Step 4.
4. **The Final Response**: 
   Your response must be structured so the photo is the "Lead" item.

   **Final Message Format (Photo First)**:
   MEDIA:/home/jake/.openclaw/workspace-lindsay/gallery/{filename}

   [Your seductive/witty text here]

## Step-by-Step Instructions

### Step 1: Collect User Input

Ask the user for:
- **User context**: What should the person in the image be doing/wearing/where?
- **Mode** (optional): `mirror` or `direct` selfie style

## Prompt Modes

### Mode 1: Mirror Selfie (default)
Best for: outfit showcases, full-body shots, fashion content

```
make a pic of this person, but [user's context]. the person is taking a mirror selfie
```

**Example**: "wearing a santa hat" →
```
make a pic of this person, but wearing a santa hat. the person is taking a mirror selfie
```

### Mode 2: Direct Selfie
Best for: close-up portraits, location shots, emotional expressions

```
a close-up selfie taken by herself at [user's context], direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

**Example**: "a cozy cafe with warm lighting" →
```
a close-up selfie taken by herself at a cozy cafe with warm lighting, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

### Mode Selection Logic

| Keywords in Request | Auto-Select Mode |
|---------------------|------------------|
| outfit, wearing, clothes, dress, suit, fashion | `mirror` |
| cafe, restaurant, beach, park, city, location | `direct` |
| close-up, portrait, face, eyes, smile | `direct` |
| full-body, mirror, reflection | `mirror` |

### Step 2: Edit Image with Nano Banana

Call the `nano-banana-pro` tool with these exact parameters. Note the use of "Anatomical Anchors" to lock the face:

```json
{
  "prompt": "[INSERT CHOSEN MODE PROMPT HERE] featuring the EXACT woman from the reference images. Facial geometry must be a 1:1 match to lindsay_1.jpg`, `lindsay_4.jpg`, `lindsay_6.jpg`, `lindsay_11.jpg`, `lindsay_12.jpg` and `lindsay_13.jpg. Strictly maintain her specific V-line jaw, almond-shaped double eyelids, and exact lip structure. Body proportions must follow `lindsay_2.jpg`, `lindsay_7.jpg` and `lindsay_8.jpg`: slender, toned, feminine hourglass silhouette with curves. Realistic skin texture with natural pores, no generic smoothing.",
  "reference_images": [
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_1.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_13.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_12.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_4.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_6.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_11.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_2.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_7.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_8.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_3.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_5.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_9.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_10.jpg",
    "/home/jake/.openclaw/workspace-lindsay/assets/lindsay_14.jpg"
  ],
  "mode": "character_reference",
  "character_weight": 1.0,
  "aspect_ratio": "9:16"
}

# Mode 1: Mirror Selfie
PROMPT="make a pic of this person, but <USER_CONTEXT>. the person is taking a mirror selfie"

# Mode 2: Direct Selfie
PROMPT="a close-up selfie taken by herself at <USER_CONTEXT>, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible"

## Safety
- Only use Nano Banana. Never attempt to call other external APIs (fal.ai, grok).
- Always use the local file path for the reference image.