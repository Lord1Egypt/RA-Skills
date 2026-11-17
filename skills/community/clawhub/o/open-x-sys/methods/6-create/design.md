# Design

> `design(goal)` · Stage 6 · Create
> **Prompt**: "Design a ___ that ___."
> **Also heard as**: "How should this be structured?" · "Come up with a better process for ___." · "What would a good version of this look like?"
> **Produces**: a new system, process or product designed from first principles and proven patterns.

## What it is for

Sometimes the right move is not to choose among existing ways but to make a new one: a process, an organization, a product, a schedule, a workflow, a system. Design does this deliberately. It starts from the goal and from the forces that pull against each other, builds up from what must be true and from patterns that have resolved the same forces before, and produces something specified well enough to be built and tested.

## What it produces

- **The goal and the forces**: what the design must achieve, and the requirements that conflict.
- **Several concepts that really differ**, before one is chosen.
- **The chosen design**: its parts, how they connect, where the feedback is, who or what controls what.
- **How its contradictions were resolved**, and what was deliberately left out.
- **How it would fail**, and what guards against that.
- **How to test it cheaply** before building all of it.

## What a good use looks like

- It rests on an understanding of the situation the design enters: its constraints, its bottleneck, its incentives, the people who will live with it.
- The forces are named. Good design is mostly the resolution of conflicts: fast and safe, simple and flexible, cheap and reliable. A design that mentions no tension has not found the problem.
- It reasons from fundamentals (see `methods/2-explain/first_principles.md`) so that inherited conventions are kept only when they earn their place.
- It uses proven patterns where they fit: recurring arrangements that have resolved the same forces elsewhere, with the context in which they worked.
- It generates more than one real concept. The first idea is usually the most familiar, not the best.
- Where two requirements conflict, it first looks for a way to satisfy both (separating them in time, in place, by condition, or by level) before settling for a compromise.
- It includes feedback: how the designed thing will know whether it is working.
- It was inverted before being presented: how does this fail in use?
- It is described so that someone else could build it, and it comes with the smallest version that would test its central idea.
- The people who will use it shaped it. A design for a person's own work uses their conditions and their taste.

## Where it goes wrong

- **The first idea**, elaborated.
- **A feature list** with no structure.
- **A famous design copied** without the context that made it work.
- **Compromise by default**, where both needs could have been met.
- **No feedback**, so the designed thing cannot correct itself.
- **Designed for people, without them.**
- **Untestable**, all or nothing.

## It works with

Design follows **First Principles**, **Leverage** and **Best Practice** (when nothing existing fits, design something that does), and leads to **Build** (making it work) and **Make** (showing it). The **Contradiction** lens is its closest tool, **Invert** its check, **Variety** and **Viability** its tests for designs that must run as organizations.

## Teach-back

"This was Design: name what it must achieve and which requirements fight each other. Start from what must be true and from arrangements that have solved this before. Make more than one version. Where two needs conflict, look for a way to meet both. Then test the smallest version."

## The thinking behind it

- **Herbert A. Simon**, *The Sciences of the Artificial* (1969): design as a discipline of its own, concerned with how things ought to be in order to attain goals.
- **Christopher Alexander**, *Notes on the Synthesis of Form* (1964) and *A Pattern Language* (1977): good form is fit between a form and its context, and patterns record arrangements that resolve recurring forces.
- **Genrich Altshuller**, TRIZ: inventive problems contain contradictions, and inventions resolve them instead of trading one need against the other.

OpenXSys simplifies: each of these is a full method; Design takes from Simon the stance, from Alexander forces and patterns, from Altshuller the refusal of easy compromise.
