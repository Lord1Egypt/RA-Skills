---
name: organizing-edge-bookmarks
description: "Use when organizing Microsoft Edge bookmarks or favorites when persistence matters, when folder priorities like AI/investing/social are important, or when previous bookmark edits were reverted after restart or sync."
version: 1.0.2
license: MIT
homepage: https://github.com/XenoExia/edge-bookmarks-skills
metadata: { "openclaw": { "emoji": "📚", "os": ["darwin"] } }
---

# Organizing Edge Bookmarks

Treat the **live browser bookmark model** as the source of truth. The raw `Bookmarks` file is a fallback artifact, not the preferred write path.

## When to Use

✅ **USE this skill when:**

- The user wants Microsoft Edge bookmarks/favorites reorganized
- The result must survive reload or restart
- Previous bookmark edits were reverted, appended, or emptied after restart/sync
- The user wants priority folders such as `AI`, `Investing`, `Social`, `Tools`, `Resources`, or `Archive`

❌ **DON'T use this skill when:**

- The task is generic browser automation unrelated to bookmarks
- The user wants a plugin/extension instead of direct bookmark organization
- The target browser is not Microsoft Edge

## Core Principle

If a live-profile path exists, use it.

Avoid raw `Bookmarks` JSON edits by default because Edge can rebuild the visible tree from its live model and sync state.

This skill is for **local, same-machine execution only**. If the agent is not running on the same Mac as the target Edge profile, stop and switch to a manual checklist instead of inventing a remote control path.

## Runtime Preconditions

- Validated target: local macOS host with Microsoft Edge installed
- Use this skill only when an approved local control path has already been proven in the current session
- Acceptable proven control paths include:
  - a live browser bookmark API already verified against the visible tree
  - a local browser automation tool already present and authorized
  - a browser-native scripting path already demonstrated to work in this session
- If the control path is not already proven, do not infer one from this skill
- If the task would require undefined remote access, stop and switch to manual operator instructions

## Required Workflow

1. **Identify the exact target**
   - Confirm the exact Edge profile by name/path.
   - Confirm whether the scope is the bookmarks bar, other bookmarks, or both.
   - Confirm whether nested folders are in scope.
   - If profile or root scope is ambiguous, ask before moving anything.

2. **Turn the request into explicit buckets**
   - Convert vague priorities into named folders such as `AI`, `Investing`, `Social`, `Tools`, `Resources`, `Archive`.
   - Default assumption: `AI`, `Investing`, and `Social` are top-level priority folders unless the user says otherwise.
   - Use deterministic tie-breaks for multi-category bookmarks: primary purpose first, current user priority second, otherwise move to `Archive` or `Review`.

3. **Create a rollback point before mutation**
   - Capture a baseline snapshot/export of the live bookmark tree.
   - Record total bookmark count and target root counts.
   - Record a dry-run move plan or mutation ledger before the first write.
   - If a safe baseline cannot be captured, stop.

4. **Require explicit consent for intrusive actions**
   - Before quitting Edge, relaunching a profile, attaching to a live page, or running in-browser bookmark mutations, confirm the user explicitly approved those intrusive steps.
   - If the user did not approve browser restart or live profile control, downgrade to manual instructions.

5. **Do not start with raw file edits**
   - Do not use `Bookmarks` JSON as the primary path.
   - Do not mix file edits and UI/model edits in one pass.
   - If a prior file edit already rolled back, treat that as proof the path is unsafe.

6. **Prefer the live browser model**
   - Operate inside the real Edge profile if possible.
   - Enforce a single-writer rule: fully close other Edge instances/background writers before a controlled relaunch of the same profile.
   - If needed, capture current tabs, relaunch the same real profile in a controllable mode, and attach to it.
   - Prefer browser-native bookmark APIs such as `chrome.bookmarks`.
   - Select and move bookmarks by stable node IDs plus parent/root context, not by titles alone.
   - If the browser-native API is unavailable or does not match the visible bookmark state, stop treating it as authoritative.

7. **Use UI automation only as fallback**
   - `edge://favorites/` may expose weak accessibility structure.
   - If the UI is not semantically controllable, stop instead of guessing with destructive clicks.
   - If UI automation is used, reconcile the result against the live bookmark tree afterward.

8. **Verify persistence**
   - Inspect sync state before mutation; if sync state is unclear or the tree is still changing, wait or stop.
   - Re-read the live bookmark tree immediately after applying moves.
   - Compare the intended structure against the actual structure, not just counts.
   - Reload the favorites page and verify again.
   - Restart Edge normally, reopen the same profile, and verify again.
   - If sync is enabled, allow one sync reconciliation cycle and verify once more.

## Safety Rules

- Never delete on the first pass unless the user explicitly asks.
- Never assume browser restart or profile takeover permission just because the user asked for bookmark organization; intrusive control needs explicit approval.
- Prefer `Archive` or `Review` for uncertain items.
- Preserve counts unless deduplication is explicitly requested.
- Do not deduplicate, merge, or remove duplicates on the first pass.
- Do not rename bookmarks or folders on the first pass unless explicitly requested.
- Do not assume Apple Events JavaScript support is working just because a menu item exists.
- Do not assume a valid `Bookmarks` checksum means persistence is safe.
- Stop immediately on profile mismatch, unreadable bookmark tree, structural diff mismatch after apply, count mismatch after apply, or sync reversion.

## Credentials and Dependencies

- This skill does **not** require external API tokens or cloud credentials.
- It assumes access only to the user-approved local Edge profile and already-approved local automation tooling.
- If your intended path depends on a binary, extension, debugger port, or automation runtime that is not already present and verified, stop and document that dependency explicitly before proceeding.

## Common Mistakes

### Editing `Bookmarks` directly first

Why it fails:
- Edge may rebuild the visible tree from live model state or sync metadata.

Better:
- Use the live browser bookmark model first.

### Trusting `edge://favorites/` accessibility blindly

Why it fails:
- The page may not expose stable drag-and-drop controls.

Better:
- Probe control surfaces first and downgrade to manual instructions if the page is opaque.

### Treating sync as an afterthought

Why it fails:
- Correct in-session state can still be overwritten by restart or sync reconciliation.

Better:
- Inspect sync before mutation and verify again after restart and sync settlement.

### Moving by visible title only

Why it fails:
- Duplicate titles and repeated folder names can send items to the wrong place while counts still look correct.

Better:
- Move by bookmark node ID with root/path context and verify with an exact structural diff.

### Assuming an undefined automation toolchain

Why it fails:
- High-impact browser actions become unsafe when the skill implies capabilities that have not been proven on the current machine.

Better:
- Prove the local automation path first. If you cannot prove it in the current session, stop and fall back to manual operator instructions.

## Quick Reference

- Persistent bookmark reorganization → inspect profile/sync state, then prefer live bookmark model
- Prior file edit rolled back → do not retry raw file editing as the primary path
- Category cleanup → define deterministic top-level buckets first
- Uncertain bookmark → archive/review, do not delete
- Existing folders already exist → reuse or merge deliberately, do not create blind parallel folders

## Reference

- `references/edge-bookmarks-workflow.md`
