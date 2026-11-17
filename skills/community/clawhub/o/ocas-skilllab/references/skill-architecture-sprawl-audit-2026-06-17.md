# Skill Architecture Sprawl Audit — 2026-06-17

## User Directive
"you've been sprawling skills again... and creating skills when you should be creating functions inside of skills, do an audit of what needs to be merged"

## Core Principle
Skills should be **class-level umbrellas** — not narrow one-session-one-skill entries. When a new capability is needed, the first question is: "which existing skill should this be a function/subsection of?" Only create a new skill when no existing umbrella covers the class.

## Right Test for Consolidation
"Would a human maintainer write this as N separate skills, or as one skill with N labeled subsections?" If the latter, merge.

## Anti-Patterns to Avoid Going Forward

1. **Don't create a skill for a style rule.** Style guides belong as reference files inside the skill that handles the output.
2. **Don't create a skill for a single-channel integration.** Channel posting belongs as a module inside the communications skill.
3. **Don't create a skill for a prompt-engineering wrapper.** If all a skill does is format prompts for an existing tool, it's a reference file.
4. **Don't create a skill for a testing/simulation utility.** Testing belongs under operational skills.
5. **Don't create a skill that is only invoked by one other skill.** If it's only called by one parent, it's a sub-module.
6. **Before creating a new skill, check for an existing umbrella.** Add a subsection or reference file instead.