# Compaction Config — Field Reference

## reserveTokensFloor: 40000

This is headroom. The flush triggers at: `context window - reserveTokensFloor - softThresholdTokens`.

With 200K context and these values: `200,000 - 40,000 - 4,000 = 156,000 tokens` — that's when the flush fires.

The default is 20K. That's too tight. A single large tool output (file read, browser snapshot, API response) can jump past the threshold before the flush gets a chance to run, sending you into overflow recovery instead of the safe compaction path.

**40K is a good starting point.** Go higher if you regularly read large files or take browser snapshots. Go lower (30K) if your tool usage is lightweight and you want to maximize usable context.

## memoryFlush.enabled: true

Should be on by default in recent versions, but verify. When context crosses the soft threshold, OpenClaw injects a silent turn that prompts the agent to save important context to disk. The user never sees this turn. The `NO_REPLY` token in the prompt suppresses delivery.

## softThresholdTokens: 4000

How far before the `reserveTokensFloor` the flush triggers. Default 4000 is fine for most setups — gives a buffer for the flush turn itself.

## mode: "safeguard"

Safeguard mode prevents overflow recovery (the "bad path" where the context got so full the API rejected the request and everything gets compressed at once with no memory flush). Keep this.

## contextPruning: cache-ttl

Pruning trims old **tool results** in-memory, per-request only. It does NOT touch user/assistant messages. It's lossless — the on-disk transcript is unchanged. The `cache-ttl` mode prunes tool results older than the TTL (1h is a good default for most workflows).

Pruning is your friend. It reduces bloat without destroying conversation context. Compaction is the dangerous one.

## Two Compaction Paths

**Good path (maintenance compaction):**
1. Context nears threshold
2. Pre-compaction memory flush fires silently
3. Agent saves important context to disk
4. Compaction summarizes older history
5. Agent continues with summary + recent messages + everything from disk

**Bad path (overflow recovery):**
1. Context too big, API rejected the request
2. OpenClaw compresses everything at once to recover
3. No memory flush, no saving — maximum context loss

The entire point of `reserveTokensFloor: 40000` is to stay on the good path.

## What Compaction Destroys

Does NOT survive:
- Instructions embedded only in conversation
- Preferences and decisions given mid-session without being written to a file
- Images shared before compaction (by design)
- Tool results and their context
- Nuance and specificity (summaries are lossy)

Always survives:
- All workspace bootstrap files (SOUL.md, AGENTS.md, USER.md, MEMORY.md, TOOLS.md)
- Anything the agent wrote to disk before compaction
- File paths and IDs (preserved even in summarized parts)
- Daily memory logs (searchable via memory_search, not re-injected)
