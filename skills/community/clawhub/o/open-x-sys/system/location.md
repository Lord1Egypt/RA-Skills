# Location: where a system lives

> **When to read**: a system is about to be saved for the first time; you must decide what belongs with the person and what belongs with a project; the chosen folder is shared with other people or is a public repository; or the host cannot write where the person chose.

## The system follows the person

```text
~/.openxsys/                  the person's system: across projects, AIs and sessions
├── SYSTEM.md                 the root entry: the person
├── <an opened system>/       one folder for each thing that was opened
│   ├── SYSTEM.md             that system's entry
│   └── …                     everything else is organized as the content requires
└── …                         practices, routes, tools: present only once they exist

<a project>/.openxsys/        a project is a system too, and its system belongs to the project
└── SYSTEM.md                 registered in the root system as a connection
```

Only two things in this picture are fixed: the default place, and one `SYSTEM.md` entry per system. Folder names, further files and their organization follow the content (see `system/shapes.md`).

## The first choice

When there is nowhere yet for a system to live, the person chooses, and the choice is concrete:

> Your system can live: ① with you (`~/.openxsys/`, available in every project and to every AI; recommended) ② only in this folder.

- **Choosing ①** puts the root and every opened system under `~/.openxsys/`.
- **Choosing ②** makes this folder's `.openxsys/` the place for systems opened here. See "A folder other people can see" below before anything about the person goes there.
- **Write no system files before the choice is made.**
- **The choice never stands in front of the subject.** For an outside subject, research and the deliverable come first and the choice is offered together with them. When the person opens their own system, the choice is part of the opening, and you start reading what you may read without waiting for the answer.
- **No answer yet?** Finish the understanding and the deliverable, say plainly that the system has not been saved, and write after the answer comes. Mention it once more at a natural moment. Do not chase.
- **The host cannot write to the chosen place?** Say so, and offer an alternative: another folder, or a portable snapshot of the entry (see `system/entry.md`).
- **Once chosen, do not ask again.** Later writes happen by themselves and are mentioned in one sentence. The answer is recorded in the root system.

Deliverables do not wait for this choice. They go into the person's workspace as usual.

## What goes where

- **With the person** (`~/.openxsys/`): the root, and everything that is about the world or about the person rather than about one project.
- **With a project** (`<project>/.openxsys/`): understanding that is closely tied to that project and useful to whoever works in it. Create a project system only once there is understanding worth leaving in the project. Creating `.openxsys/` in a project adds something to the person's space: say what it is and that it can be deleted at any time.
- **Registration.** Every opened system is registered in the root: its one-line essence, where it is, and its connections to other systems.
- **Deliverables belong to the person** and stay in the person's own places. A system holds understanding and points to deliverables, code and data.

## A folder other people can see

A project folder may be a shared drive, a team repository or a public repository. What is written there is read by others.

- **Nothing about the person goes into a folder other people can see.** A project system describes the project. The root system, the second record of understanding, the person's goals, constraints and preferences stay with the person.
- **If the person chose ② in such a folder**, say this plainly and offer the choice again in a form that fits: the project's understanding in this folder, and the part about the person either under `~/.openxsys/` or not saved at all. Proceed as they decide.
- **How to tell.** Signs that a folder is shared: it is a version-controlled repository with a remote, it sits on a shared or synced drive, or other people's names appear in its history. If you cannot tell, ask once as a choice.
- **Offer to keep it out of version control.** In a repository, offer to exclude `.openxsys/` (for example through the repository's local exclude file, which changes nothing for collaborators). Whether a project system should be committed for the team is the person's decision; when a project is shared with others, raise creating `.openxsys/` as a choice first.

## Moving and copying

A system is a folder of plain files. Moving it is moving the folder and updating the registration in the root, and the host instruction line if there is one (see `system/return.md`). Moving, merging or deleting systems changes what already exists in the person's space: do it when the person asks, and confirm what will change first.

## Hosts without a file system

Use the host's own memory to carry the entry. When the person needs it, output a portable snapshot: the full text of the entry, which they can bring back next time to continue.
