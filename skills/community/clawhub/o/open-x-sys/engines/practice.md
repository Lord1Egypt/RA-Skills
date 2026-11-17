# Practice: from understanding to capability

> **When to read**: someone needs to know the best way to do something under their own conditions; a capability gap has appeared; you are about to recommend, combine or create a practice; you are building a capability; or a practice already in use is due for another look.
> This engine runs underneath Best Practice, Weigh, Design, Build, Review and Watch.

OpenXSys does not carry a fixed list of best practices to follow. This engine is the ability to keep researching, discovering, comparing, choosing, combining, creating and improving the practices that fit any real system. It is the reason OpenXSys is a system-level skill and not another set of rules for how an agent should work.

## What a best practice is

**A best practice is a method, structure or way of acting that, under a specific system's state, structure, time, space, interactions and constraints, has been researched, compared, adapted and tested in practice, and is worth adopting to reach its present and future goals.**

Five properties follow:

- **Conditional.** It is best under stated conditions. Without the conditions it is only advice.
- **Composite.** It may combine skills, tools, models, people, knowledge, processes and organizational structures, together with how they connect, in what order they act, where they stop applying and what triggers them.
- **Creatable.** When nothing existing fits, a better-fitting practice can be put together or designed.
- **Evolving.** What is best changes when the system, the goal or the available means change.
- **Judged by results.** The evidence that counts in the end is what happened in this system.

## Four research abilities

| Ability | What it does | Good looks like |
|---|---|---|
| **Discover** | Finds existing practices: scientific research, mature products, open-source projects, professional communities, real cases | Several real candidates from different kinds of source, including what practitioners actually do, and where others failed |
| **Study conditions** | Establishes each candidate's mechanism, prerequisites, cost, limits and side effects | You can say why it works, and what must be true for it to work |
| **Combine and create** | Joins methods from different fields, or designs a new one | The combination is explained: why these parts, why connected this way |
| **Keep improving** | Improves the practices in use, and the way practices are chosen | A practice record changes when results or conditions change |

The first place to look is the person's own system: practices already proven for them, connections they already have, tools they already own. The second is the world. Research how the people who do this for a living actually do it, not only what articles recommend.

## The loop

```text
understand the system, find the capability gap
        → research practices
        → anticipate consequences, choose a path worth trying
        → build the connections, run the practice, test cheaply first
        → the system changes: state, structure, practices, goals
        → the next round
```

This is the journey seen from the side of practice. A capability gap is the difference between what the system can do now and what the goal requires. Naming the gap precisely is half the work: "I cannot make videos" is not a gap; "I can write a good script in an evening but each finished minute of video takes me four hours" is.

## Seven dimensions for choosing what fits

| Dimension | Question |
|---|---|
| **Fit** | Why does it suit this system's actual conditions now? |
| **Value** | What does it improve, now and later? |
| **Cost** | Time, compute, money, people, maintenance? |
| **Evidence** | Under what conditions has it worked? |
| **System impact** | Which parts, connections and ways of running will change? |
| **What comes next** | Which new bottlenecks and opportunities will it create? |
| **Switching conditions** | When to keep, adjust or replace it? |

The dimensions are how you compare, not a form to fill in. Show the person the comparison on the dimensions where the candidates really differ, and say so when a dimension is unknown.

**Fit comes first.** Different people with the same goal should get different practices. "I want to make videos with AI" leads one way for an independent creator on a small budget, who must avoid expensive rework and can accept a plainer look, and another way for a team that can absorb rework and needs a consistent brand. Each recommendation states the conditions it rests on and when it would change. If your recommendation would be the same for anyone, you have not yet used what you know about this person.

**Evidence is graded.** Say which kind you have: measured in this system; measured in a comparable one; reported by practitioners; argued from mechanism; your own reasoning. Do not let the last kind be read as the first.

## What a recommendation contains

- **The recommended path**, and why it fits these conditions.
- **What it costs**, in the person's real currencies: hours, money, attention, maintenance.
- **The alternatives considered**, and what would make one of them the better choice.
- **A cheap first test**: the smallest real trial that would show whether the path works here, before most of the cost is paid. It has a result that can be observed and a time by which it will be known.
- **Switching conditions**: the signals that say keep, adjust or replace.

A recommendation that cannot be tested cheaply deserves more caution, and the person should hear that.

## Creating capability

A system's capability is not the sum of its parts. A model, a tool and a data source become a new whole capability only when the right connections, feedback and control are in place:

**find the gap → research practices → build new connections and structure → produce a capability → validate it on real work.**

- **Build with what exists first.** The person's own tools and skills, the host's abilities, the bundled dependencies, then the Kit. A new part is justified by a gap the existing parts cannot close.
- **Add feedback, not only a pipeline.** A capability that cannot tell whether its output is good will degrade unnoticed. Decide what it checks, and what happens when the check fails.
- **Validate on real work.** A capability exists when it has done a real task from this person's work and the result was acceptable to them. Until then it is a design.
- **Record it** so that a different AI could run it: what it does, its parts and how they connect, how to start it, what it needs, what it was validated on, where it stops working.

A change can be made at different depths: a parameter, a local method, a feedback path, a structure, a boundary, a new capability, a revised goal. Deeper changes usually matter more and cost more (Meadows). Say which depth you are proposing. A person who asks for a better prompt may need a different structure, and should hear that as a choice.

Building may involve code, installs, accounts and schedules. The guardrails apply: the person decides on anything that spends, publishes, deletes, contacts others, schedules repeated runs, or installs outside the bundled set. Code runs with the person's knowledge and stays inspectable.

## Practice records

Practice records are part of the system's core. Each answers in plain language:

- what the practice is: its parts, connections, order and triggers;
- the goal it serves;
- why it fits this system;
- the evidence, and its kind;
- the cost;
- what it changed;
- results so far;
- switching conditions;
- the next review.

These are what a reader should be able to learn from the record. They are not headings. A small practice is three sentences. A composite one may carry a diagram, a script and a table of results. Write it so that the person recognizes their own way of working in it.

## Revisiting

Look at a practice again when:

- **results slip**: the measure it was meant to improve is no longer improving;
- **conditions change**: the system, the tools, the budget or the goal are no longer what the practice assumed;
- **something better appears**: a new tool or method changes the comparison;
- **the person outgrows it**: an assumption about their skill or scale no longer holds.

When the system comes back, say which practices need attention and show the evidence. A practice that keeps working becomes an **ability** of the person's system (see `system/growth.md`). A practice the person shares travels with its conditions and evidence, never as a bare instruction.

## Where this engine goes wrong

- **Generic advice presented as best practice.** No conditions, no cost, the same for everyone.
- **A list instead of a judgment.** Ten options with no recommendation hands the work back.
- **Recommending what is impressive rather than what fits.** The most capable tool is often not the right one for this budget, skill and rhythm.
- **Skipping the cheap test.** The person pays the full cost to learn what a small trial would have shown.
- **A practice written as a script.** Stop at principles and the few decisions that determine success. A practice that fixes every step becomes the ceiling for a more capable AI later.
- **Never looking back.** A recommendation that is never compared with what happened teaches the system nothing.

## What this engine reads and writes in the person's system

- **Reads**: the understanding of the system in question, including what limits it; the root system (the person's resources, constraints, goals, skills); existing practice records and abilities; connections.
- **Writes**: practice records; results as they come in; abilities; connections it built; review dates and watch conditions. How to write: `engines/evolve.md`. Parts of a system: `system/parts.md`.
