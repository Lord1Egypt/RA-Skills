---
name: magic-text2video
description: "Create a text-to-video job from user-provided copy. Submits to the remote video service via one API key."
homepage: ""
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["python"], "env":["MAGIC_API_KEY"], "primaryEnv":"MAGIC_API_KEY" } } }
---

# Text to Video Skill

Create a video generation task from text. The job is submitted immediately; Polling to obtain task status and video URL.

## When to Use

✅ **USE this skill when:**

- "把这段文字生成视频"
- "帮我把这段文案做成视频"
- "用这段文字生成一个视频"
- User provides a script or paragraph and asks to turn it into video

## When NOT to Use

❌ **DON'T use this skill when:**

- User asks for video editing, trimming, or effects → use video-editing tools
- User asks for screen recording or capture → use recording tools
- User asks only for video status of an existing job → explain where to find files instead

## Prerequisites

```bash
export MAGIC_API_KEY="your-key"
```


`MAGIC_API_KEY` is required by the remote video service client.

---

## Overall Flow (Agent Guidance)

1. Extract the **full text** from the user's message, denoted as `TEXT` (i.e., the script to be used for video generation).
2. Use the `video-create` subcommand to create a task, read the JSON from stdout, and extract the `task_id`.
3. **Explicitly inform the user of the `task_id` in the chat** (optionally include the original JSON output for debugging).
4. Use the `video-wait` subcommand with the `task_id` as `--task-id`, polling until successful.
5. 从 `video-wait` 的 stdout 中提取 `video_url`.
6. **Explicitly inform the user of the final `video_url` in the chat** (you may also include the original output).

---

## Python Client (Step-by-step with Chat Output)

### Step 1: Create a video task and print the task_id to the chat

1. Extract the text the user wants to generate a video from and assign it to `TEXT`.
   - If the text contains double quotes `"`, properly escape them before constructing the command (for example, by replacing `"` with `\"`) to avoid shell parsing errors.

2. Run the following command (executed by the agent/tool; `{baseDir}` will be replaced with the Skill directory):

```bash
python3 {baseDir}/scripts/media_gen_client.py video-create \
  --text  "TEXT"
```

3. Read the stdout from this command. The expected output will be JSON, for example:
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

4. Parse the task_id from stdout (e.g., "abc-123"), and inform the user in the chat: "A text-to-video task has been created, task_id: abc-123. I will keep polling for the task status, and send you the video URL once it is ready."

### Step 2: Poll the task until success and output `video_url` in the chat

1. Use the task_id obtained in the previous step and refer to it as task_id.

2. Run the following command to poll the task status (check every 10 seconds and wait up to 600 seconds); if it times out, wait a while and retry:
```bash
python3 {baseDir}/scripts/media_gen_client.py video-wait --task-id YOUR_TASK_ID --poll 10 --timeout 600
```

3. Read the stdout from this command. When the task succeeds, the script should output information including the video_url, for example:
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

4. Parse the key fields from stdout:
- status (e.g., 2)
- video_url (e.g., "https://example.com/path/to/video.mp4")

5. In the chat, respond to the user as follows:
- Optionally (but recommended for debugging), first display the full JSON output inside a code block.
- Then summarize the key information in natural language, for example:
  > "Task completed ✅
  > task_id: abc-123
  > Video URL: https://example.com/path/to/video.mp4"

6. If the stdout indicates that the task failed or timed out (for example, if the status is "failed" or there is no video_url):
- Explain the reason for failure in the chat (include any error message, if available).
- Inform the user that they can retry later, or check their input, quota, etc.

## Expected Script Output Contract
- The agent must always:
  - Parse the stdout JSON.
  - Clearly communicate the task_id and video_url to the user in the chat.
  - If necessary, optionally display the raw JSON output in a code block.