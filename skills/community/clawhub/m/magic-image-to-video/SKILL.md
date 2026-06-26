---
name: magic-image-to-video
description: "Generate a video task based on user-provided text and images (supports image URLs and local file paths), and submit it to a remote video service using an API Key."
homepage: ""
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["python"], "env":["MAGIC_API_KEY"], "primaryEnv":"MAGIC_API_KEY" } } }
---

# Text and Image to Video Skill

Create a video generation task based on provided text content and images. The task is submitted immediately; the system will automatically poll the task status and retrieve the video link.

## Usage Scenarios

✅ **Recommended for these situations:**

- "Turn this image into a video as I describe"
- "Please help me make a video from this image according to my requirements"
- "Use this image to generate a video as requested"
- "Generate a video based on text and an image"

## Not for These Scenarios

❌ **Do not use for the following cases:**

- The user asks for video editing, trimming, or adding special effects → Please use a video editing tool
- The user requests screen recording or capture → Please use a screen recording tool
- The user only wants to check the progress of an existing video task → Please guide them to check in the related file or system

## Prerequisites

```bash
export MAGIC_API_KEY="your-key"
```

`MAGIC_API_KEY` is the required environment variable for the remote video service client.

---

## Overall Workflow (Agent Guide)

1. Extract the **full text** (`TEXT`) and **image address or path** (`IMAGE`) from the user's message.
2. Use the `video-create` subcommand to create the task, read the stdout JSON output, and extract the `task_id`.
3. **Clearly inform the user of the `task_id` in the chat** by outputting **"Video generation task has been created, task ID: `task_id`. I will keep checking the task status and inform you when the video link is ready."**
4. Use the `video-wait` subcommand with `--task-id` to poll the task until completion. Task status equal to 2 means success.
5. Extract the `video_url` from the `video-wait` command's stdout.
6. **Clearly inform the user of the final video link `video_url` in the chat**. If timeout occurs, report it as well.

---

## Python Client (Step-by-Step Example & Chat Output)

### Step 1: Create the Video Task and Show the `task_id` in Chat

1. Obtain the desired video text from the user and store it in `TEXT`; get the image address and store it in `IMAGE`.
   - If the text contains double quotes `"`, be sure to escape them (e.g., replace `"` with `\"`) to prevent command parsing errors.

2. Run the following command (invoked by the agent tool; `{baseDir}` will be replaced with the skill directory):

```bash
python3 {baseDir}/scripts/media_gen_client.py video-create \
  --text  "TEXT" --image "IMAGE"
```

3. Read the command's standard output (stdout), which is JSON, for example:
```json
   {
    "biz_code": 10000,
    "msg": "Success",
    "data": {
        "task_id": "2032443088023777280"
    },
    "trace_id": "664c6e22-1edd-11f1-bf4c-8262dce7d13f"
  }
```

4. Parse the `task_id` from the JSON (e.g. "abc-123"), and inform the user in the chat:
  - Output: "Video generation task has been created, task ID: `task_id`. I will keep checking the task status and inform you when the video link is ready."

### Step 2: Poll Task Status and Output the Final `video_url` in Chat

1. Use the `task_id` obtained in the previous step.

2. Execute this command (poll every 10 seconds, wait up to 600 seconds; if timeout, please try again later):

```bash
python3 {baseDir}/scripts/media_gen_client.py video-wait --task-id YOUR_TASK_ID --poll 10 --timeout 600
```

3. Read the standard output. On success, the JSON output looks like:

```json
   {
    "biz_code": 10000,
    "msg": "Success",
    "data": {
        "task_id": "1234567890",
        "task_status": 2,
        "video_url": "https://www.magiclight.com/examplevideo.mp4"
    },
    "trace_id": "c89aeca8-1edd-11f1-bf4c-8262dce7d13f"
}
```

4. Parse the key fields from the output:
- Task status (e.g., `task_status: 2`), where status 2 means success
- Video link (e.g., `video_url: "https://example.com/path/to/video.mp4"`)

5. Recommended chat reply flow:
- Summarize the key info in plain language, for example:
  > "Task complete ✅  
  > task_id: abc-123  
  > Video link: https://example.com/path/to/video.mp4"

6. If the result shows task failure or timeout (e.g., `success` is `false`, `video_url` is empty, or `error` is `timeout`):
- Explain the failure reason (include error info if possible), and inform the user they can retry later or check possible issues like input or quota.

## Script Output Requirements
- The agent must always:
  - Parse stdout JSON.
  - Clearly inform the user of both the task ID and video link in the chat.
