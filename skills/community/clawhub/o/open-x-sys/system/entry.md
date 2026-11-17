# The entry: the one fixed convention

> **When to read**: you are about to write or rewrite a `SYSTEM.md`; you are judging whether an entry is good; you opened an entry written by the alpha; or a different AI will continue from this system.

Every system has one entry, `SYSTEM.md`, written in natural language and shared by the person and by AI. A person reads it as "my system". An AI reads it as "how to run this system". It is a natural-language program that can be run.

## What a reader must come away knowing

Whoever reads it, the person or an AI that has never heard of OpenXSys, should be able to answer:

- What is this system? For whom and for what purpose was it built, and where are its boundary and scale?
- What is its core understanding? The essence in one sentence, and the most important structures and mechanisms.
- How far does the understanding go? How reliable is it, as of when, and what is still unknown?
- What can it do now? Which practices does it use, with what results? What is it watching?
- What is it made of besides this file? Where are the code, the data, the connections and the deliverables, and what is each for?
- What does the person already understand about it, and where should the next explanation begin?
- What is most worth doing now? This is the choice left for the next run.
- How does one continue? An AI without OpenXSys installed must be able to carry on.

**This is a convention for continuity, not a content template.** These are questions a reader should be able to answer after reading. They are not headings to fill in. Writing them as eight sections with a paragraph each replaces understanding with a format. A good entry says the most important thing first, and the other answers sit where they belong. How much to write, in what order and with what structure follows the content: an entry for a concept may be twenty lines; an entry for a group of companies may be one page of judgment followed by several files. `system/shapes.md` shows how far apart entries can be.

**There is no template in these files, and you should not invent one.** A test: cover every name and look only at the structure. Can you still tell what kind of subject it is about and what kind of person it was built for? If not, it is a template.

## Three judgments for a good entry

- **It is understanding, not a record.** The reader learns how the subject is, not what was done in some conversation.
- **It explains itself.** It does not depend on this conversation or on OpenXSys vocabulary. An unfamiliar AI reading only this file knows what it is, how far to trust it and what to do next.
- **The person would want to read it.** It is in their language and starts from what they care about.

## The qualities of a good system

- **Same structure as the subject**, at the scale the person cares about.
- **For this person**: their concepts, starting from what they already understand, serving their purpose.
- **Answerable**: it can answer "why?", "then what?" and "what is the evidence?"
- **Honest**: fact, inference and guess are apart; there are sources and dates.
- **Self-describing**: any AI that reads the entry can understand and continue; the entry says what every other part of the system does.
- **Able to grow**: new understanding rewrites old; it can split, connect and simplify.
- **Connected to reality**: it points to deliverables, material, tools and actions.

## What 1.0 adds to an entry

Beyond the understanding itself, a 1.0 entry lets a reader find, when they exist:

- **the route** that produced the current understanding, so it can be swapped, extended or repeated;
- **practices in use**: each with its goal, why it fits, results so far and next review (the full record may be its own file; see `engines/practice.md`);
- **watch conditions**: the signal, the threshold and what it would mean;
- **the other parts**: code, data and connections, each with one line on what it is for and how to use it (see `system/parts.md`);
- **the second record**: what the person already understands about this subject.

None of these is a required section. An entry for a concept may have none of them. They appear when the system actually has them, written where a reader would look.

## Evidence in an entry

An entry is only as useful as it is trustworthy. Key claims carry their source and date, in the sentence or in a file the entry points to. State "as of" precisely where the subject allows it: for a codebase, the commit the understanding was checked against; for a company, the date of the latest filing read. What happened after that point is exactly what a returning system reports as changed.

## Opening an entry written by the alpha

Alpha entries are natural language and remain readable; nothing needs converting before use. The first time one is opened under 1.0, bring it up to date as part of the normal write-back: keep the understanding, restate figurative alpha terms in plain words, and add the items above only where the content supports them. Do not invent content to match the new expectations. Tell the person in one sentence that the entry was updated.

## Another AI, or no file system

A system is plain text: any AI that can read files can continue from the entry. This is why the entry must explain itself. On a host without a file system, the host's memory carries the entry, and a portable snapshot (the full text of the entry) lets the person bring it back.

## Two tests

- **Continuity**: delete the whole conversation and keep only the system files. Can a new AI do **clearly better** than from scratch?
- **Starting point**: on the second run, does the system start from what the person already understands, and not from the beginning?
