# Saved state

Write work/state.json after every step and before every paid run. Never put keys,
tokens or approval links in it. Keep dollar amounts as decimal strings with six places.

```json
{
  "skill": "media-audio-edition",
  "version": 5,
  "status": "recording",
  "folder": "podcast/2026-10-14-why-we-killed-our-free-plan",
  "show": "Build Notes",
  "computer": {"ffmpeg": true, "loudness": true, "clip": true},
  "wallet": {"read_at": "2026-10-14T13:58:52+01:00", "available_usd": "4.120000", "daily_remaining_usd": null, "confirm_threshold_usd": "3.000000"},
  "post": {"title": "Why we killed our free plan", "author": "Ana Ruiz", "link": "https://example.com/free-plan", "words": 630},
  "choices": {"format": "conversation", "focus": null, "voices": {"host": {"name": "Eric", "voice_id": "cjVigY5qzO86Huf0OWal"}, "co_host": {"name": "Jessica", "voice_id": "cgSgspJ2msm6clMCkdW9"}}, "tool_id": "elevenlabs.eleven-v3", "clip": true},
  "passes": {"brief": "work/brief.md", "outline": "work/outline.md", "claims": "work/claims.md", "checked": "question by 0:12, a roadmap of three, an example, a doubt and a payoff in each point, a recap; longest sentence 22 words; every claim matched to the post in claims.md"},
  "script": {"sha256": "<fingerprint>", "characters": 4100, "turns": 52, "parts": [610, 1310, 640, 1540], "clip_part": 3},
  "music": {"tool_id": "elevenlabs.eleven-music-v2", "music_length_ms": 7000, "prompt": "A 5-second instrumental podcast intro sting, warm and curious, modern, no vocals, resolving cleanly by the fifth second.", "reused": false},
  "prices": {"source": "inspect", "read_at": "2026-10-14T13:58:40+01:00", "speech_per_1k": "0.140000", "minimum_per_request": "0.002500", "music_per_minute": "0.210000", "characters_per_request": 2000, "settled_share": "0.22"},
  "plan_usd": "0.598500", "typical_usd": "0.150780", "maximum_usd": "0.850000",
  "approval": {"at": "2026-10-14T14:02:11+01:00", "reply": "approve", "sha256": "<fingerprint>", "voices": ["cjVigY5qzO86Huf0OWal", "cgSgspJ2msm6clMCkdW9"], "tool_id": "elevenlabs.eleven-v3", "maximum_usd": "0.850000"},
  "voice_check": {"shared_at": "2026-10-14T14:02:40+01:00", "reply": "sounds right", "at": "2026-10-14T14:04:05+01:00"},
  "runs": [{"step": "part-1", "tool_id": "elevenlabs.eleven-v3", "idempotency_key": "<UUID; MCP or HTTP only>", "started_at": "2026-10-14T14:02:19+01:00", "run_id": "<run_id>", "status": "succeeded", "cost_final": "0.011088", "file": "work/part-01.mp3", "tail_db": "-47.3", "flagged": false}],
  "spent_usd": "0.011088",
  "updated_at": "2026-10-14T14:04:05+01:00"
}
```

`status` moves through "writing", "waiting for approval", "waiting for voice check",
"recording", "joining" and "done". Before approval, `approval` and `voice_check` are null
and `runs` is empty. Until the user answers the voice check, `voice_check` has no reply. A
re-take adds its own run with `"step": "part-1b"`, and the kept take is the one with
`"kept": true`. One voice: `voices` has only `host`. A reading has no `passes`.
