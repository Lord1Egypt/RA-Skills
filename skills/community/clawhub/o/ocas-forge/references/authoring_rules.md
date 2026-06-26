# Forge Authoring Rules

## Core Rules
1. A skill must earn its existence — repeated, durable, worth maintaining
2. Every skill needs one sharp promise — "This skill exists to ______"
3. Routing comes first — description is routing logic, not branding
4. SKILL.md is the operational surface — not a tutorial or README
5. Match specificity to failure risk — exact where drift is costly
6. Add complexity only when justified — start minimal

## Responsibility Boundaries
Every new skill must verify it does not conflict with: Scout, Sift, Praxis, Dispatch, Corvus, Mentor, Elephas, Weave, Taste, Voyage, Look, Rally, Relay, Vesper, Forge, Fellow, Thread.

## Atomic Skill Principle
Skills perform one clear role. They may cooperate but must never depend on other skills.

## Required Structural Sections (System Skills)
Responsibility Boundary, Optional Skill Cooperation, Journal Outputs, Storage Layout (with ~/openclaw/ paths), Visibility, OKRs (universal + skill-specific).

## Storage Convention
All data under ~/openclaw/data/ocas-{skill}/ and journals under ~/openclaw/journals/ocas-{skill}/. No data inside skill packages.

## Journal Convention
Every run writes a journal. journal_spec_version: "1.3". journal_type in run_identity. Ref: spec-ocas-journal.md.

## Inter-Skill Interfaces
All inter-skill communication uses defined intake paths per spec-ocas-interfaces.md. No undocumented interfaces.
