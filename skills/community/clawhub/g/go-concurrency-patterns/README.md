# Go Concurrency Patterns

Production Go concurrency patterns — goroutines, channels, sync primitives, context, worker pools, pipelines, and graceful shutdown. Use when building concurrent Go applications or debugging race conditions.

## What's Inside

- Concurrency Primitives — goroutines, channels, select, sync.Mutex, sync.WaitGroup, context.Context, errgroup.Group
- Worker Pool pattern with context cancellation
- Fan-Out / Fan-In Pipeline pattern
- errgroup with Cancellation and concurrency limits
- Bounded Concurrency (Semaphore) — `semaphore.Weighted` and channel-based semaphore
- Graceful Shutdown pattern with signal handling
- Concurrent Map — `sync.Map` and ShardedMap for different workloads
- Select Patterns — timeout, non-blocking send/receive, priority select
- Race Detection — `go test -race`, `go build -race`
- Best Practices and common pitfalls

## When to Use

- Building concurrent Go applications
- Implementing worker pools and pipelines
- Managing goroutine lifecycles and cancellation
- Debugging race conditions
- Implementing graceful shutdown

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/backend/go-concurrency
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/backend/go-concurrency .cursor/skills/go-concurrency
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/backend/go-concurrency ~/.cursor/skills/go-concurrency
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/backend/go-concurrency .claude/skills/go-concurrency
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/backend/go-concurrency ~/.claude/skills/go-concurrency
```

---

Part of the [Backend](..) skill category.
