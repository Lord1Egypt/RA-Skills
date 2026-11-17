# Parts: what a system is made of

> **When to read**: a system is about to gain something other than text (a script, a dataset, a connection to a tool); you are taking stock of what the person already has; you must decide whether a part is worth adding; or a reader needs to know what a system's files are for.

**A system's core is natural language. The rest is whatever the system needs to act.**

| Part | What it is | Examples |
|---|---|---|
| **Core** | What the system is and understands, the practices it uses, how to use it, what every other part does | `SYSTEM.md` entries, understanding, practice records, watch conditions, the two records of understanding |
| **Code** | What it can execute | A script that refreshes data, an analysis notebook, a video project, a small tool |
| **Data** | What it knows in structured form | Source snapshots, timelines, tables, measured results |
| **Connections** | What it can reach | Skills, MCP servers, APIs, command-line tools, devices, collaborators |
| **Deliverables** | What it has produced | Pages, videos, documents, decks, share packs, in the person's workspace |

## How the parts relate

- **The core describes every other part.** For each script, dataset and connection, the core says what it is for, how to use it, what it needs and when it was last known to work. A part the core does not describe is invisible to the next reader, human or AI.
- **Parts appear when a real task needs them.** A system for a concept may be one file forever. Do not create `code/`, `data/` or `connections/` folders in advance. Structure follows content.
- **Natural language first.** Before writing code, ask whether a clear description would let a capable AI do the same thing next time. Code earns its place when the task must be repeated exactly, needs computation, or must run without an AI present.
- **The OpenXSys skill itself stays natural language.** Code belongs to the person's systems, never to the runtime.

## Code

- **Runs with the person's knowledge.** Say what a script does before it runs for the first time, and what it will read and write.
- **Stays inspectable.** Plain, readable source in the person's space. Nothing obfuscated, nothing fetched and executed unseen.
- **Says what it needs.** Runtime, inputs, credentials by reference (see below), expected output.
- **Is validated.** The core records what the code was run on and what happened. Code that has never run is a draft and is labelled as one.
- **Scheduling is the person's decision.** Code that runs repeatedly by itself is set up only after the person agrees, with how to stop it.

## Data

- **Carries its origin.** Where it came from, when it was captured, how it was processed. A table with no source is a liability.
- **Snapshots, not silent copies.** When a source may change, keep a dated snapshot and say so, and let the entry state as of when the understanding holds.
- **Measured results are data.** The results of a practice (before and after, with dates) are among the most valuable things a system holds: they are what lets a practice be judged by results.
- **Only what the person allowed.** Data from the person's own files and accounts is recorded only within what they permitted, and never includes secrets or sensitive personal information about them or about others.

## Connections

A connection is a reference to something the system can reach, with what it makes possible.

- **References, never secrets.** A connection names the tool, the account or the endpoint and says where the credential is kept by the person (an environment variable name, a password manager entry). It never contains the key, the token or the password. If you see a secret while working, do not write it anywhere in the system.
- **State what it makes possible.** "Connected to the analytics export: weekly retention can now be recomputed without manual download" is a connection. "Uses analytics" is not.
- **State its condition.** When it was last used successfully, and what it depends on.
- **Collaborators are connections too.** A person who reviews drafts or a team that owns a dataset can be recorded as a connection, limited to what the person themselves said and to what matters for the system. Contacting anyone is always the person's decision.

## Census: what the person already has

When a system opens, take stock of what is already available:

- the skills the host lists;
- skill folders such as `~/.claude/skills/` and `.agents/skills/`, and the project's own;
- MCP servers and the tools they expose;
- the host's built-in tools (search, browsing, code execution, image generation, sub-agents);
- runtimes that are present (Node.js, Python) and the bundled dependencies (see `deps/DEPENDENCIES.md`).

These become **connections** in the person's system. Use the person's own tools when they fit better than the bundled ones: a creator who already has a video pipeline should have their pipeline used, not replaced.

A census reads lists, names and descriptions. **It never reads secrets**: not credential files, not environment values, not tokens in configuration. If a configuration file mixes settings with secrets, read only what is needed to know that a tool exists.

Take the census quietly and report only what matters for this run: "you already have a slide skill installed, so the deck uses it" is useful; a full inventory is ritual. Record in the root system what was found, so it is not repeated every session; refresh it when something relevant changes.

## Deliverables

Deliverables live in the person's workspace, organized the way the person organizes things. The system points to them: where each is, what it shows, which understanding and sources it rests on, and its share pack if one was made. A deliverable the person edited by hand is theirs; the system records that their version is the reference.

## Judging whether to add a part

Add a part when the answer to one of these is yes:

- Will this be done again, and does doing it by hand cost real time or risk error?
- Does the understanding rest on data that will change, so that a refresh must be repeatable?
- Does a practice need something to run without an AI present?
- Would the next AI otherwise have to rebuild this from nothing?

When a part stops being used, remove it or mark it retired in the core. A system that accumulates dead scripts and stale tables has become harder to continue from, which is the opposite of what a system is for.
