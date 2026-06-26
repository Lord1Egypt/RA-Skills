# {{PROJECT_NAME}} Design Drafts

This directory contains design drafts produced during Phase 1 (RFC Specification) of the Platonic Coding workflow.

## Purpose

Design drafts capture the conceptual design before formalization into RFC specifications. They include:

- Problem space and goals
- Principles and constraints
- Conceptual interfaces and boundaries
- Key abstractions and terminology
- Design sketches and exploration

## Workflow

```
Design Draft (this directory)
        |
        v
RFC Specification (specs/)
        |
        v
Implementation Guide (docs/impl/)
        |
        v
Code
```

## Creating a New Draft

Use the **platonic-coding** skill starting at Phase 1:

```
Use platonic-coding workflow to start Phase 1 for a new feature.
```

Or create a draft manually -- any markdown file in this directory works.

## After a Draft is Complete

Once a draft captures the shared understanding, continue Phase 1 to formalize it into an RFC:

```
Use platonic-coding workflow to proceed with the draft at docs/drafts/<name>.md
```

This converts the draft into a formal RFC specification within Phase 1.
