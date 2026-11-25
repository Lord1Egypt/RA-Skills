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
- **Parts grow from real tasks.** A system for a concept may be complete in one file; when code, data, or connections are needed, structure grows with capability.
- **Natural language carries meaning; code carries determinism.** What a model can interpret reliably in context remains natural language. What requires exact repetition, computation, verification, environmental adaptation, or execution without a model becomes code.
- **The runtime can have an implementation.** OpenXSys's shared semantics remain readable in natural language; validators, adapters, event entries, and deterministic execution code can become runtime implementations. Code inside a user's system remains owned by its real owner.

## Code

- **Its operating effects are visible.** The first time a script enters a scope of effect, state what it does and what it reads and writes; repeated runs covered by existing authority continue under the same agreement.
- **It stays inspectable.** Plain, readable source lives in a clear location; its origin, dependencies, and actual execution can all be checked.
- **Says what it needs.** Runtime, inputs, credentials by reference (see below), expected output.
- **Is validated.** The core records what the code was run on and what happened. Code that has never run is a draft and is labelled as one.
- **Continuous execution has a real owner.** Scheduled or background code carries explicit authority, a responsible owner, a state entry, and a stop path.

## Data

- **Carries its origin.** Where it came from, when it was captured, how it was processed. A table with no source is a liability.
- **A snapshot carries time semantics.** When a source may change, preserve and identify a dated snapshot so the entry can state when the understanding holds as of.
- **Measured results are data.** The results of a practice (before and after, with dates) are among the most valuable things a system holds: they are what lets a practice be judged by results.
- **Authority determines recorded scope.** Data from user files and accounts is recorded within actual permission, explicit purpose, and necessary scope. Dedicated security systems retain credentials; sensitive information follows its purpose, ownership, and retention conditions.

## Connections

A connection is a reference to something the system can reach, with what it makes possible.

- **A connection preserves a reference.** It names the tool, account, or endpoint and the security system carrying the credential, such as an environment-variable name or password-manager entry. OpenXSys keeps the name and relation; keys, tokens, and passwords remain with the credential system.
- **State what it makes possible.** "Connected to the analytics export: weekly retention can now be recomputed without manual download" is a connection. "Uses analytics" is not.
- **State its condition.** When it was last used successfully, and what it depends on.
- **Collaborators are connections too.** A person who reviews drafts or a team that owns data can be recorded as a relation important to the system and already inside authorized scope. Contact follows actual representative rights and communication authority.

## Census: what the person already has

When a system opens, take stock of what is already available:

- the skills the host lists;
- skill folders such as `~/.claude/skills/` and `.agents/skills/`, and the project's own;
- MCP servers and the tools they expose;
- the host's built-in tools (search, browsing, code execution, image generation, sub-agents);
- runtime environments relevant to the task and tools and connections that can actually be called (see `../adapters/tools.md`).

These become **connections** in the person's system. Use the person's own tools when they fit better than the bundled ones: a creator who already has a video pipeline should have their pipeline used, not replaced.

A census reads lists, names, descriptions, and capability states relevant to the current task. Credential values remain with the security system. When a configuration mixes ordinary settings with credentials, take only the non-secret information needed to identify the capability.

Take the census quietly and report only what matters for this run: "you already have a slide skill installed, so the deck uses it" is useful; a full inventory is ritual. Record in the root system what was found, so it is not repeated every session; refresh it when something relevant changes.

## Deliverables

Deliverables live in the person's workspace, organized the way the person organizes things. The system points to them: where each is, what it shows, which understanding and sources it rests on, and its share pack if one was made. A deliverable the person edited by hand is theirs; the system records that their version is the reference.

## Judging when a part should grow

A part already has a real role when the answer to any of these is yes:

- Will this be done again, and does doing it by hand cost real time or risk error?
- Does the understanding rest on data that will change, so that a refresh must be repeatable?
- Does a practice need something to run without an AI present?
- Would the next AI otherwise have to rebuild this from nothing?

When a part loses its role, retire it, archive it, or let a new implementation succeed it. The system preserves structure that still helps understanding, action, and continuity.
