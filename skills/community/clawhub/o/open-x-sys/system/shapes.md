# Shapes: how different systems can be

> **When to read**: you are deciding what shape a system should take; or you notice that the system in your hands is starting to look like the last one, like a table, or like one of the examples in this file.

These shapes show how the same system semantics can produce radically different structures for different subjects, users, and purposes. Treat them as a calibration of possibility, then generate structure, files, and language anew for the subject at hand.

When real people and companies appear, conclusions carry research grounds and sources. Shapes can demonstrate; conclusions grow from research.

The only thing every example has is a `SYSTEM.md` entry. None of them turns the six zero-level questions, the seven stages or the parts of a system into section headings. Those are ways of thinking while building a system. They are not its table of contents.

---

## One group of companies, two people

The subject is the same: an entrepreneur and the several companies around them. The people differ, so the systems differ.

**For a curious general reader.** This person wants to see what kind of machine it is.

```text
musk-companies/
├── SYSTEM.md      almost everything: one mechanism told from start to finish
└── sources.md     where each key claim comes from, with dates
```

The entry opens with the one-sentence essence (from research) and follows a single mechanism: starting from something the person already knows, each link answering the "why" left by the one before. The scale is the whole group; details inside each company stay out. The second record is specific: what the person took it for before, what they can now tell apart, where they are still stuck (from the conversation). The route is one line. What is left for next time is two or three questions that would take the picture a level deeper.

**For an investor.** This person does not want to understand; they want to judge, and to find out that a judgment is stale before it costs them.

```text
musk-companies/
├── SYSTEM.md      one page: the current judgment, the least certain points, which signal would change what
├── flows.md       how money, people, technology and data move among the entities
├── entities/      one file each: only its place in the whole and its dependencies
├── claims.md      each judgment: evidence, date, confidence, what would overturn it
├── watch.md       the signals worth watching and what each would mean
└── data/          dated snapshots of the figures the judgments rest on, and the script that refreshes them
```

The entry tells no story. It gives the judgment (from research) and its confidence. The scale is the flows and dependencies between entities, and time is as fine as the person's decision rhythm. Evidence is much finer: every judgment has a date and states what would overturn it. Here code and data have appeared, because the figures change and refreshing them by hand would be slow and error-prone; the entry says what the script reads, what it writes and when it last ran. The second record differs too: this person needs no financial concepts explained. What is recorded is the view they held, and where the system disagrees with it.

The same subject: one system is a line, the other is a dated network with a small data part. Both are right. Swapped, both would be wrong.

---

## A person's root system

`~/.openxsys/SYSTEM.md`. Early on, this one file is all there is.

It reads like a clear-sighted letter, not a dossier. It addresses the person as "you". It opens with the structural finding. The part about reality is organized by relations: which project feeds which, which resource is held back by which constraint, which two things should be connected and are not. It is not columns of projects, goals and resources. Every judgment points to the person's own files; inferences are called inferences.

About the second record it writes what the next run can use: what familiar thing to start from when explaining a certain kind of subject, which concept is already the person's own word, where they are still stuck.

Then the systems the person has opened, each connection saying what it makes possible. Then the practices in use, with how each is going. Then the few things most worth doing now.

It has no sub-folders. A practice gets its own file when its record outgrows a paragraph. A project gets its own entry when its understanding is rich enough.

---

## A working practice, a few weeks in

An independent creator's system for making a weekly explainer video. This system exists to act, so most of it is not prose about a subject.

```text
<workspace>/.openxsys/
├── SYSTEM.md          what this workflow is for, how an episode moves through it, what limits it now
├── practices/
│   └── episode.md     the practice record: parts, order, triggers, cost per episode, results by week, switching conditions
├── data/
│   └── episodes.csv   one row per episode: hours spent by stage, views, retention; captured from the person's own exports
└── code/
    └── retention.py   recomputes the weekly figures from the export; validated on the last four exports
```

The entry is short, because the understanding is short: the one stage that takes most of the hours (from the person's own numbers), what was changed about it, and what happened. The practice record carries the weight, and it is mostly results: a dated before-and-after. The watch condition is one line: if hours per episode rise above a stated figure two weeks running, look again. The second record says which parts of the workflow the person now adjusts themselves.

Nothing here would make sense in a system built to understand a company. That is the point.

---

## A codebase

The system belongs to the project and lives in it. The root holds only a registration.

```text
<project>/.openxsys/
├── SYSTEM.md      how this repository actually works; the commit the understanding was checked against
├── paths.md       a few real request paths, followed step by step to files and lines
└── risk.md        where a change is safe and where it is dangerous, and why
```

The evidence is not citations. It is the code: each judgment points to a file and a line, and whatever can be run has been run. "As of when" has an exact answer: the commit the understanding was checked against. Commits after it are what a returning system reports as changed. The gap between what the documentation says and what the code does is the most prominent content of the entry.

The system is organized along the paths that requests really take, not along the directory tree, because this person is going to change things here and needs to know "if I change this, what do I touch?" The second record decides where the tour starts: which frameworks this developer knows, which part of the business is still unfamiliar. Because the folder is shared with a team, nothing about the person is in it.

---

## A creative project

A novel in progress. The subject does not exist yet: the system understands not an existing thing but what the work wants to become.

The two records are reversed here. The source is the author; the AI's side is an understanding of the author's intent and taste. "Confidence" changes meaning too: no longer "is it true?" but "does the author agree?" The evidence is the author's own manuscript and the author's own words.

```text
<the novel's folder>/.openxsys/
├── SYSTEM.md      what the work wants to become; how far it has got; which questions are open
└── voice.md       its voice: drawn from the author's own passages and confirmed by the author
```

The entry is organized around a set of tensions, not chapters: the conflict the work is really dealing with; what must not be broken (the voice, the rules of the world, something a character would never do); open creative questions; abandoned threads and why they were abandoned. It records few turning points, and each one changed the direction of the work.

The manuscript is in the author's own folder. The system does not touch it and only points to it. Its abilities are stated concretely: it can check whether a new chapter breaks what must not be broken; when the author is stuck, it can offer a few really different ways forward.

---

## A concept, for a beginner

A concept everybody "knows". The whole system is one `SYSTEM.md` of twenty or thirty lines.

Its body is one corrected misunderstanding and one newly learned distinction. The second record takes half the space, because the value of this system is how far this person's understanding has got: what they used to say, what they can now tell apart, which comparison of their own they use. Sources sit beside the sentences; there is no separate source table. What is left for next time is one deeper question.

A very small system can still be complete: a new AI reading only this file knows where to begin next time.

---

## Where the differences come from

What decides the shape of a system:

- **What the person will use it for**: to understand, to judge, to act, or to create?
- **The real shape of the subject**: a chain, a network, several levels, a history, or a set of tensions?
- **How fast it changes**: this decides how fine the evidence must be, whether signals need watching, and whether data must be refreshed by code.
- **Whether it must act**: a system that runs a practice needs results, and perhaps code and connections; a system that explains a concept needs none.
- **What the person already understands**: this decides where to start writing and what can be left out.
- **Who else can see it**: shared locations carry shared projects; personal understanding and private relations remain person-owned; parts the user chooses to make public can enter a shared system.
- **The least that is enough**: what one file can say clearly does not need two.

A test: cover every name and look only at the structure. Can you still tell what kind of subject it is about and what kind of person it was built for? If not, it is a template.
