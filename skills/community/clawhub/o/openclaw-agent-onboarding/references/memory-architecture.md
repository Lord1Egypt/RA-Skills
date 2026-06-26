# HOT/WARM/COLD Memory Architecture

## HOT

File: `MEMORY.md`

Purpose: small, permanent, high-frequency context.

Recommended max: 150 lines.

Include:

```text
core rules, user preferences, current priority projects, safety boundaries, memory index links
```

Do not include:

```text
long logs, temporary tasks, raw docs, full reports, outdated rules
```

## WARM

Directory:

```text
memory/projects/
memory/domains/
memory/people/
memory/preferences/
```

Include project details, domain knowledge, people/contact context, preferences, durable background.

## COLD

Directory:

```text
memory/archive/
memory/logs/
memory/raw/
```

Include historical logs, raw material, old decisions, long reports, low-frequency references.

## Required structure

```text
memory/
├── index.md
├── projects/
├── domains/
├── people/
├── preferences/
├── decisions.md
├── gotchas.md
├── archive/
├── logs/
└── raw/
```

## Write policy

1. Decide if it is worth remembering.
2. Temporary info never enters HOT.
3. Long content goes WARM/COLD.
4. Conflicting memory is flagged, not overwritten.
5. Outdated rules move to archive.
6. Every durable memory includes date/source when possible.
7. Important WARM/COLD files are indexed in `memory/index.md`.
