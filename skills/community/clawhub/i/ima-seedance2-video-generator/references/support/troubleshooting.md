# TROUBLESHOOTING

## `unrecognized arguments: --reference-audio`

You are likely running an older copy of the skill or script. Update to the latest version of this repository. Current versions support:

- `--reference-image`
- `--reference-video`
- `--reference-audio`

## Media validation or verification fails before task creation

Current behavior:

- Images: preflight validation + compliance verification
- Videos: preflight validation + compliance verification
- Audio: preflight validation + compliance verification

Check:

1. The media URL is reachable
2. The file is not corrupted
3. The content complies with platform policy
4. Your API key is valid

## `401 Unauthorized`

Your API key is invalid or expired. Regenerate it here:

https://www.imaclaw.ai/imaclaw/apikey

## `4008 Insufficient points`

Your account does not have enough credits:

https://www.imaclaw.ai/imaclaw/subscription

## The skill generated visuals but did not preserve my uploaded narration MP3

That is expected unless the API explicitly supports final soundtrack preservation for uploaded audio. In the current documented boundary:

- uploaded audio can be used as reference conditioning
- `audio=true` can request generated ambient audio
- exact narration/music preservation may still require separate composition/post-processing

## IM / OpenClaw messages are out of order

Use:

```bash
IMA_STDOUT_MODE=events
```

and ensure the caller consumes JSON events instead of mixing them with manual progress narration.
