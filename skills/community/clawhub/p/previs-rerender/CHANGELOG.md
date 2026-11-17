# Changelog

All notable changes to the **previs-rerender** skill. Versioning follows SemVer.

## 1.0.0 — first measured previs-to-finish workflow

Initial release. It separates structure-preserving rerender from continuation,
delegates paid execution to `ofox-video-core`, requires a publicly reachable
video URL, and records the shipped client's `frame_images` /
`input_references` conflict as a tool boundary rather than a claim about the
direct API. It also leaves a mixed `image_url` + `video_url`
`input_references` request out of v1 because that distinct shape is untested,
not because the core rejects it.

The workflow is backed by two Seedance 2.5 jobs at 4 seconds / 480p on
`byteplus`: one preserved four compositions, four motion directions and three
hard boundaries; the other began at the source's final state and continued
into new space without replaying the earlier layouts. Both dry-run estimates
matched the 56-cent bills. A video data URI was rejected before job creation,
so the skill requires a web URL and calls out temporary-URL lifetime risk.
