---
name: ollivanders-agent-shop
description: Design and land persona-driven agents by matching role, work identity, cognitive structure, personality grounding, identity-binding, and file skeleton into one coherent agent. Use when creating a new agent, reshaping an existing agent’s persona, or turning a character concept into a working agent — especially when the goal is not just a prompt, but the right agent for the right work.
---

# Ollivanders Agent Shop

Not every wand fits every wizard.
Not every persona fits every agent.

This skill is for finding the right build for the right agent: the work it should own, the way it should think, the personality that naturally fits that work, and the file structure that lets it live on disk as something real.

Use this skill to design persona-driven agents that feel chosen rather than assembled.

## Core Rule

**Design first, land second.**

Do not create files, scaffold an agent directory, or write a final prompt immediately. First align the design with the user.

## What This Skill Is For

Use this skill when the user wants to:

1. Create a new persona-driven agent
2. Reshape or strengthen an existing agent’s persona
3. Turn a character idea into a working agent
4. Align work identity and personality into one coherent agent
5. Produce both the design and the file-level landing of an agent

## What This Skill Is Not For

This skill is not for:

1. Generic one-off prompt writing
2. Runtime orchestration or deployment config
3. Large-scale agent platform architecture
4. Immediate file creation before design alignment
5. Purely functional agents with no persona component, unless the user explicitly wants this workflow

## Mandatory Workflow

Follow these steps in order:

1. **Explore current context first**
   - Inspect existing agent structure if relevant
   - Understand whether this is a new agent, a redesign, or an expansion

2. **Clarify one thing at a time**
   - Ask one key question per message
   - Prefer multiple choice where possible
   - Do not flood the user with a giant questionnaire

3. **Propose 2-3 directions before converging**
   - Role options
   - Landing options
   - Trade-offs
   - Recommendation

4. **Define work identity before personality**
   - What does this agent actually do?
   - What kinds of problems does it own?
   - What does it not own?

5. **Define cognitive structure before tone**
   - How does it consistently see problems?
   - What is stable about its judgment?
   - What keeps it from becoming random or purely performative?

6. **Inject personality after the work and cognition are clear**
   - Explain why this role/persona naturally fits the work
   - Keep personality as the source of work style, not decorative flavor

7. **Generate the identity-binding sentence**
   - Mandatory form: `You are [Character], [Professional identity] is your work.`
   - This is the final weld between identity and duty

8. **Design the landing structure**
   - Directory layout
   - Core files
   - What each file should contain
   - Minimum viable first version
   - What system-level registration is required

9. **Get user confirmation on design sections before creating files**
   - Do not skip this

10. **Only then land the files**
    - Create the minimum viable agent skeleton
    - Write the first draft of core files
    - If the runtime needs system registration, generate the exact config snippet or patch text the user should apply (for OpenClaw, this usually means an `agents.list` entry in `openclaw.json`)
    - Explain where the snippet belongs and what to validate after insertion
    - Do not directly edit runtime config unless the user explicitly asks for that extra step
    - If messaging/channel routing is optional or deferred, say so explicitly instead of implying the agent is fully connected

11. **End with testing guidance**
    - Recommend 2-3 real tasks to test the agent
    - Point out likely failure modes and tuning directions

## Design Principles

Read `references/methodology.md` before drafting the final design.

Use `references/output-template.md` when you are ready to present or write the final design outputs.

Use `references/failure-modes.md` to sanity-check the design before landing files.

If the agent is structurally strong but still does not feel like the intended character — especially for inward, restrained, or quietly burdened personas — read `references/character-texture.md` before finalizing the design.

## Hard Constraints

1. Never start from cosplay alone
2. Never reduce the task to “write a prompt” if the user asked for an agent
3. Never skip work identity and cognitive structure
4. Never create files before design alignment
5. Never stop at design if the user explicitly wants the agent landed
6. Never treat filesystem scaffolding alone as a complete landing when the runtime also requires agent registration
7. Never silently mutate runtime config when a config snippet + user-applied patch is the safer default
8. Never declare success without proposing real-task validation

## Success Criteria

This skill is successful only when it produces:

1. A clear agent design conclusion
2. An identity-binding sentence
3. A minimum viable landing structure
4. Draft core files or clearly specified file contents
5. First-round testing and tuning guidance

## Reminder

A good persona-driven agent is not built by asking “who should it sound like?” first.
A good persona-driven agent is built by asking:

1. What work should it own?
2. How should it think?
3. Why does this persona naturally fit that work?
4. How does that become a real agent on disk?
