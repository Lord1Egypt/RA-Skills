# Zoom Setup

## Server-to-Server OAuth App

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us)
2. **Develop** → **Build App** → **Server-to-Server OAuth**
3. Name it "Percept Meeting Sync"
4. Note your **Account ID**, **Client ID**, **Client Secret**
5. Add scopes:
   - `recording:read:list_recording_files:admin`
   - `recording:read:list_user_recordings:admin`
   - `user:read:list_users:admin`
6. Activate the app

## Environment Variables

```bash
export ZOOM_ACCOUNT_ID="your_account_id"
export ZOOM_CLIENT_ID="your_client_id"
export ZOOM_CLIENT_SECRET="your_client_secret"
```

## Batch Sync

```bash
# Import last 7 days of recordings with transcripts
percept zoom-sync --days 7

# Import a specific meeting
percept zoom-import <meeting_id>
```

Zoom must have cloud recording + audio transcript enabled in your account settings
(Settings → Recording → Cloud Recording → Audio Transcript).

## Webhook (Auto-Import)

For real-time import when recordings complete:

1. In your Zoom app, add **Event Subscriptions**
2. Endpoint URL: `https://your-host/zoom/webhook`
3. Subscribe to: `recording.completed`
4. Set `ZOOM_WEBHOOK_SECRET` to the verification token Zoom provides

```bash
export ZOOM_WEBHOOK_SECRET="your_webhook_secret"
percept zoom-serve --port 8902
```

## Local VTT Import

If you have downloaded VTT transcript files:

```bash
percept zoom-import /path/to/meeting.vtt --topic "Weekly Standup"
```

Supports standard WebVTT format with speaker labels.
