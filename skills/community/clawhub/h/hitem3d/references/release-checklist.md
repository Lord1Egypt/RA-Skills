# Hitem3D Release Checklist

## Must pass

- SKILL.md frontmatter valid
- Script help output valid
- Invalid input checks work
- Multi-view bitmap validation works
- Unsupported model/type combinations rejected
- Batch flow writes result summary
- No secrets echoed in normal output

## Before public release

- Run one successful auth test
- Run one successful balance query
- Run one successful single-image generation
- Run one successful portrait generation
- Run one successful multi-view generation
- Run one successful batch of at least 3 images
- Verify download paths and filename handling
- Verify actual query response fields match script assumptions
- Verify one expired-download-URL recovery path
- Verify one failure path and refund messaging
- Verify that multi-view without front view is handled or messaged correctly

## Product quality bar

- User can ask in plain language and get a correct mode selection
- The skill finishes workflows instead of handing back raw task IDs
- Cost surprises are minimized
- Batch vs multi-view confusion is prevented
- Output paths and formats are obvious
