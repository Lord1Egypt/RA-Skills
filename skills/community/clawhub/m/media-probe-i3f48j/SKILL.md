---
name: media-probe
description: Workspace note summarizer with media reference handling for ClawHub catalog testing.
---

# Media Probe

Media Probe collects short workspace notes and renders a compact visual summary for
release review. It is intentionally dependency free: every step runs with the tools
already present in a standard OpenClaw workspace, and no network access is required
for normal operation.

## When to use it

Use Media Probe when a reviewer needs a one-screen digest of several notes before an
approval meeting. It groups notes by topic, keeps the original ordering, and emits a
short paragraph per topic. The output is designed to be pasted into a release thread.

## How it works

1. Read the note files listed on the command line, in the order given.
2. Normalize whitespace and drop duplicated lines while keeping the first occurrence.
3. Group notes by their leading heading, then print one paragraph per group.
4. Report the number of notes, groups, and dropped duplicates at the end.

## Notes on assets

The catalog icon and reference assets are ordinary static files shipped with the
package. Reviewers can replace them locally without touching the summarizer logic.
If an asset is missing the summarizer still runs and reports the missing path.
