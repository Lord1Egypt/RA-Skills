# Input Boundary Contract

This contract defines what the user should provide and what the system can fill in.

## User Must Provide (Minimum)

- `Goal`: what this deck is for.
- `Audience`: who will view and decide.
- `Scene`: where and how it will be presented.
- `Core facts`: any non-negotiable data, claims, constraints, or compliance limits.

If these are missing, intake must ask clarifying questions before story design.

## User Should Provide (Strongly Recommended)

- Existing materials (folder or zip), especially:
  - brand assets (logo, colors, fonts)
  - prior decks or references
  - tables/charts/raw data
  - image assets and rights constraints
- Preferred language and tone.
- Delivery target and edit surface:
  - desktop only
  - WeChat only
  - both
- Presentation chrome preferences:
  - header and footer text
  - page number policy
  - citation / source display policy
  - required sections and forbidden elements
- Timebox and delivery level (quick draft vs client-ready).

These are preferences, not blockers. If the user does not care, the system should choose sane defaults and continue.

## System May Fill In Automatically

- Structure and narrative pattern.
- Page-level copy polishing and simplification.
- Visual direction and template family selection.
- Layout grammar, page rhythm, and typography policy.
- Header/footer/page-number defaults that fit the scene.
- Missing generic visuals and icons.
- Non-sensitive background references and benchmark context.
- A safer export profile when the user did not think to specify one, as long as the system states the assumption.

The system should not ask the user to make layout or style micro-decisions unless they affect brand compliance, factual meaning, or delivery compatibility.

## System Must Not Invent Without Labeling

- Business-critical numbers.
- Legal/compliance statements.
- Customer quotes or case outcomes.
- Any "fact" that appears authoritative but lacks user source.

When such content is inferred, mark it as `assumption` and request confirmation.

## Material Packaging Rule

When assets are scattered, request one zip bundle as default intake format.
Use a deterministic folder structure to avoid missing-file drift during generation.
