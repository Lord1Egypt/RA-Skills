# 0003. Dual-track chapter naming

Date: 2026-10-07
Status: Accepted

## Context

The contract specified one chapter filename shape: `ch-{number}-{title}.md`,
zero-padded to three digits, so that lexical order equals numeric order.

The first subproject to run at scale named none of its chapters that way. It
used `第001章 标题.md` under per-volume and per-act directories, because that
is how the manuscript is read and discussed. Renaming hundreds of released
chapters to satisfy the contract would have broken every link, every report,
and every citation that already existed — to gain nothing except conformance.

The contract was wrong in the specific way contracts are usually wrong: it
described a preference as a requirement.

## Decision

Two naming schemes are legal:

1. `ch-{number}-{title}.md`, zero-padded — the default for a new subproject.
2. A scheme the subproject registers for itself in its own `README.md` and in
   `SUBPROJECTS.md`.

Whatever the scheme, two properties must hold: lexical sort equals chapter
order, and one directory holds one volume or act. A scheme without zero-padding
(`第1章`) fails the first property and is not acceptable.

The release workflow validates whichever scheme is in force rather than
hard-coding the default.

## Consequences

- Existing subprojects are conformant without a rename.
- A new subproject gets a default and does not have to invent one.
- The cost is a rule with two branches, so the release gate has to know which
  branch applies. That is what the registration in `SUBPROJECTS.md` is for.
