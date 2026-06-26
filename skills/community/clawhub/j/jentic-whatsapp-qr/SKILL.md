---
name: jentic-whatsapp-qr
description: Generate a clean WhatsApp pairing QR code PNG from a running OpenClaw agent and deliver it to the user via any channel. Use when a user asks to link WhatsApp, set up WhatsApp, or scan a WhatsApp QR code. Built by Jentic.
---

# WhatsApp Link

Captures the WhatsApp pairing QR, converts it to a clean PNG on disk, and sends it to the user.

⚠️ **The QR expires in ~60 seconds. Only generate it when the user is ready to scan immediately.**

⚠️ **The script takes ~25–28 seconds to run** (WhatsApp-controlled — this cannot be shortened). Tell the user upfront so they're not waiting in silence.

Tell the user: _"Have WhatsApp open, go to Settings → Linked Devices → Link a Device. It'll take about 30 seconds to generate — let me know when you're ready."_ Wait for their confirmation before proceeding.

## Steps

**1. Fire the script immediately — as your very first action after confirmation:**

```bash
python3 ./skills/jentic-whatsapp-qr/scripts/generate_qr.py /tmp/whatsapp_qr.png
```

> ⚡ **Do not fetch thread context, read other files, or do any other work before starting the script.** Every second of delay eats into the 60s QR window. Start the exec first, then do anything else while it runs.

- The script forks a background process to keep the session alive for ~55s
- It exits immediately once the PNG is written (stdout = file path, stderr = progress)
- Exit code 0 = success; exit code 1 = error (already linked, failed, etc.)

**2. Send the file to the user:**

```python
# Default (non-Mattermost, or Mattermost main channel):
# Use message tool:
# action: send
# media: "/tmp/whatsapp_qr.png"
# message: "Scan this in WhatsApp → Settings → Linked Devices → Link a Device. You have about 60 seconds!"
```

### Mattermost thread delivery

If you are in a **Mattermost thread** (inbound metadata has `topic_id` or `reply_to_id`), the `message` tool cannot post files into threads. Use the Mattermost API directly:

```bash
SHIRKA_TOKEN=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['env']['vars']['JENTIC_MM_SHIRKA_TOKEN'])")

# 1. Upload the file
FILE_ID=$(curl -s -X POST "https://mattermost.claw.jentic.ai/api/v4/files" \
  -H "Authorization: Bearer $SHIRKA_TOKEN" \
  -F "channel_id=CHANNEL_ID" \
  -F "files=@/tmp/whatsapp_qr.png;filename=whatsapp_qr.png" \
  | python3 -c "import json,sys; r=json.load(sys.stdin); print(r['file_infos'][0]['id'])")

# 2. Post into the thread
curl -s -X POST "https://mattermost.claw.jentic.ai/api/v4/posts" \
  -H "Authorization: Bearer $SHIRKA_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel_id\": \"CHANNEL_ID\",
    \"root_id\": \"TOPIC_ID\",
    \"message\": \"Scan this now — you have ~60 seconds. WhatsApp → Settings → Linked Devices → Link a Device 👇\",
    \"file_ids\": [\"$FILE_ID\"]
  }"
```

Replace `CHANNEL_ID` with the channel from inbound metadata and `TOPIC_ID` with `topic_id` (or `reply_to_id`).

**3. Tell the user:**

> "Scan that QR code in WhatsApp now — it expires in about 60 seconds. Once you've scanned it, WhatsApp will confirm the link. If it expires before you scan, just ask me to generate a new one."

## Notes

- `generate_qr.py` handles capture, filtering, and PNG conversion internally
- `qr_decode.py` is a standalone utility used by `generate_qr.py` — no need to call it directly
- Use `media: "/tmp/whatsapp_qr.png"` to send the file — **never pass base64 image data through context**
- If already linked, the script exits with code 1 and an error message — no QR needed
- Works on any channel (Mattermost, Signal, etc.) — `message` tool routes to current conversation
- **Set COLUMNS=120** is handled internally by the script
- **Interactive testing:** run the script manually and open the PNG to verify before distributing

## Interactive test (console)

```bash
# Run directly — stderr shows progress, stdout shows output path on success
python3 skills/jentic-whatsapp-qr/scripts/generate_qr.py /tmp/test_qr.png

# Then open/view the PNG to verify it's a proper square QR code
ls -lh /tmp/test_qr.png
```
