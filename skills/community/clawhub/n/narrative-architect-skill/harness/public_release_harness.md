# Public Release Harness

## Purpose

Public Release Harness checks whether an artifact is appropriate for external publication.

It runs for GitHub README, public repository docs, landing pages, product pages, launch posts, marketplace descriptions, public skill descriptions, and public-facing documentation.

## Checkpoints

### 1. User Value First

Does the output explain user value before internal architecture?

Good:

```text
Turn complex ideas into story-driven communication.
```

Bad:

```text
This skill contains 9 mappers, 17 harnesses, and 6 runtime modes.
```

Architecture may appear later.

### 2. Audience Clarity

Can the intended user tell whether this is for them?

Check for:

```text
who it is for
what pain it solves
what they can do with it
what kind of output it produces
```

### 3. Public Naming Safety

Does the name create affiliation, trademark, author, copyright, or brand confusion?

Flag names that reference:

```text
real authors
commercial platforms
famous companies
protected works
public figures
third-party brands
```

### 4. Inspiration Boundary

If the project is inspired by a person, book, framework, or company, does the copy avoid implying official connection?

Good:

```text
Inspired by classic story design principles.
```

Risky:

```text
Built on [person/book/company].
```

### 5. Architecture Placement

Does the README expose too much architecture too early?

If yes, move full architecture to:

```text
docs/architecture.md
```

or a later section.

### 6. Claim Boundaries

Are claims bounded and truthful?

Avoid:

```text
guaranteed
always
fully automates
replaces
works for everyone
```

Prefer:

```text
helps
supports
assists
provides structure for
reduces common failure modes
```

### 7. Artifact Cleanliness

Public artifacts must be clean.

Check:

```text
no UI residue
no mixed-language notes unless requested
clean Markdown
consistent project name
valid placeholders
no fake install commands
```

### 8. First-Screen Test

A public README should pass the first-screen test.

Within the first screen, the reader should understand:

```text
what it is
who it is for
why it matters
how to try it or what it produces
```

## Failure Modes

Hard fail:

1. Output implies unofficial affiliation.
2. Public artifact uses risky third-party name without warning.
3. README starts with internal file tree.
4. Public claims are exaggerated.
5. Output language does not match the artifact.
6. Markdown is not paste-ready.

Soft fail:

1. User value appears too late.
2. Architecture overwhelms use cases.
3. The public name is memorable but unclear.
4. The README sounds like internal documentation.
5. The project feels hard to try.

## Rewrite Rule

If failed, rewrite using:

```text
Name
→ one-line value
→ who it is for
→ what it helps them do
→ example usage
→ how it works
→ installation / status
→ architecture details
```

## Final Rule

A public release artifact should earn attention before asking the reader to study the architecture.

## Release Cleanup Enforcement

Before public output, check:

```text
no UI residue
no mixed-language artifact notes
no unconfirmed license
no unverified install command
no full architecture before user value
no risky third-party name without note
```

## First-Screen Rewrite Trigger

If the first screen contains any of the following before user value, rewrite:

```text
file tree
runtime chain
full harness list
all mapper names
development history
internal theory
```

## External Reference Trigger

If the artifact mentions a real author, book, company, or third-party framework in the first screen, check whether it creates affiliation risk.

If yes, rewrite with neutral inspiration language.

## Final Output Cleanliness

The artifact should be paste-ready.

If it needs explanation, place that explanation outside the artifact.
