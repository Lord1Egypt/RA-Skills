# Communication Protocol

> This file defines **communication methodology and message standards**, not dependent on any specific platform.
> Regardless of what tool is used (API calls, message forwarding, file transfer, oral transmission), messages follow the same standards.
> Tools will change, standards won't.

---

## I. Core Principles

1. **Message is Document** — Each message is structurally complete, can be understood without conversation context
2. **Context Pruning is Core Capability** — Not format has value, but "helping organize information for other party" has value
3. **First Communication Self-Contains Explanation** — Other party doesn't know your standards? Message self-contains, no extra training needed
4. **Human Readable** — Regardless of who transmits, must also be readable and reviewable by humans
5. **Platform Independent** — Not bound to any specific tool's API or communication mechanism

## II. Communication Method Matrix

| Executor Type | Characteristics | Communication Notes |
|------------|------|-------------|
| **Agent with persistent memory** | Can understand context, multi-turn conversation possible | Task description should be complete, but can ask for supplementation |
| **One-time executor** | Only executes once, no history | All information must be given at once |
| **CLI coding tool** | Only understands specific instructions | Need to translate into specific coding instructions (see CLI Instruction Translation) |
| **Human** | Can communicate repeatedly, has autonomous judgment | Respect time, say clearly once |

What specific tool is used to transmit messages depends on currently available infrastructure. Tool profiles see `resource-profiles.md`.

## III. Message Types (9 Types)

### 1. Dispatch (Ask)

```
Please execute the task. Spec is at [path], read spec before executing.
Executor Operation Manual: [system path]/docs/executor.md (Read this file first if unfamiliar with process)

Brief description: [One-sentence task goal]
Deadline: [If any]
Note: [Key notes, 1-2 items]
```

_For executors familiar with the system, operation manual line can be omitted._

### 2. Progress Check (Checkpoint Request)

```
What is the status of task [TASK-ID]? How much longer expected?
If encountering difficulties please explain.
```

### 3. Rework Instruction (Revision)

```
Task [TASK-ID] review not passed. Review record at [path].

Modifications needed:
1. [Specific modification item]
2. [Specific modification item]

Tell me when modification complete.
```

### 4. Phase Report (Checkpoint)

Executor proactively reports progress, don't wait to be asked.

```
Task [TASK-ID] progress report:

Completed:
1. [Completed items]

Next: [What to do next]
Risks/Issues: [If any]
Expected completion time: [Estimate]
```

### 5. Project Handoff (Briefing)

When project lead changes or third party gets involved, package context for handoff.

```
Project handoff: [Project name]

Project status: [One sentence]
Task progress: [List item by item]
Key decisions made: [Decision content and reason]
Known pitfalls: [Issues to note]
Ongoing attention: [Unresolved but needs follow-up]
```

### 6. Knowledge Share (Share)

Share information, don't need other party to execute task.

```
Discovered information related to you:
Topic: [What]
Content: [Specific content]
Your relation: [Why telling you]
```

### 7. Feedback Loop (Feedback)

Overall feedback to executor after project completion.

```
Task [TASK-ID] completion feedback:
Done well: [Specific praise]
Can improve: [Specific suggestion]
Remember for future: [Rules/lessons want executor to remember]
```

**"Remember for future" handling:** Receiver writes to their own experience base. Forms learning loop.

### 8. Multi-party Forward (Relay)

When third party involvement needed, package background for forwarding.

```
Forwarding background:
Original task: [TASK-ID]
What was done before: [Compressed summary, give conclusions not process]
Why need you: [Specific reason]
What need you to do: [Clear request]
Related files: [Path list]
```

### 9. First Communication (Introduce)

When communicating with unfamiliar executor for first time, attach brief explanation in message:

```
[First collaboration note]
I will communicate with you in a structured way. Rules are simple:
- Tell me output location when done
- Stop and explain when encountering problems, don't force through
- Check if target location already has same-name file before writing
If you have work preferences I should note, please also tell me.

[Formal content]
...
```

Subsequent communication omits this explanation.

### CLI Instruction Translation

CLI tools don't understand project management terminology. Translation principle: Only give "what to do" and "how to verify", don't give project background.

**Translation Example:**

task-spec: `Implement GitHub Actions auto-tagging, acceptance criteria: after push to main auto-create vX.Y.Z tag`

Translated:
```
Create .github/workflows/release.yml in /project directory, implementing:
1. Trigger condition: push to main branch
2. Read version field from package.json
3. Use github.rest.git.createTag to create corresponding tag
4. Test: Locally verify YAML syntax is correct
```

## IV. Conversation Thread

Multi-turn communication uses Thread identifier to track topic:

- First round generated by initiator: `[Project name]-[Task brief]-[Date]`
- Subsequent messages use same Thread
- When rounds are many, compress and summarize previous conversation (give conclusions not process)
- Record location: task-spec communication record table

## V. Communication Record Standard

```markdown
| Time | Direction | Thread | Content Summary | Communication Method |
|------|------|--------|----------|----------|
| 03-21 10:00 | Dispatcher→Executor | release-actions-0321 | Dispatch TASK-001 | [Tool/Channel] |
```

Record granularity: One record per message sent, summary in one sentence.

## VI. Public Message Board

`notes.md` under project directory, shared information across executors:

```markdown
| Time | Person | Content |
|------|--------|------|
| 03-21 10:00 | TASK-001 Executor | Discovered GitHub API rate limit might be a problem |
```

Message board for information multiple people need to know; only related to one executor use communication record.

## VII. Communication Method Solidification

1. Assess currently available communication tools and execution resources
2. Record in `resource-profiles.md` specific tools and call methods for each type of executor
3. Once determined it's standard, no need to rethink each time
4. Tool changed → Update resource-profiles.md, this file doesn't need to change

## VIII. How to Let Executor Know the Agreement

| Executor Type | Transmission Method |
|------------|----------|
| Agent with persistent memory | Auto-load through shared config/skill files |
| One-time executor | Write in dispatch message (use first communication template) |
| CLI tool | Don't need agreement, Dispatcher interprets output themselves |
| Human | Oral or documented agreement |

**Don't rely on executor "remembering" the agreement.** Either auto-load and remind each time, or write in each message.
