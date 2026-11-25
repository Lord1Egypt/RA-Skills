# Tiers and forms: what to make, and with what

> **When to read**: you know the thesis and must choose a form; you are deciding between a page, a video, a deck or writing; or a dependency is missing and you need to know what to deliver without it.

Form is chosen last and for the content: thesis, then structure, then form (see `engines/express.md`).

## Three tiers

| Tier | What it uses | Good for | Always available? |
|---|---|---|---|
| **0 · Pages** | One self-contained HTML file with the bundled libraries | Explorable explanations, scrollytelling, interactive reveals, data stories, maps | Yes, on any host that can write a file |
| **1 · Host built-ins** | Shareable pages, inline widgets, browser screenshots, image generation | Links, self-critique, illustrations | Depends on the host |
| **2 · Bundled and connected skills** | Video, animation, documents, decks | Explainers, presentations, deliverables to send | When the dependency and its runtime are ready |

**Whichever tier is used, the work itself must be worth seeing.** When choosing a webpage, prefer a complete work that opens on its own. What matters is that the person encounters substantial understanding and can use the result in their own environment. Other media can carry the same strength to different readers.

Use what the person already has when it fits better than the bundled set (see the census in `system/parts.md`).

### A tier 0 page

- **One file.** It opens by double-click, works offline when it needs to, and can be sent to someone as it is.
- **Libraries are inlined or pinned.** Use a known, pinned version (see `libraries.md`) when a library truly serves the page. Many of the best pages need none.
- **Real content only.** Real data with sources, real names, no placeholder text, no stock filler imagery.
- **Readable everywhere.** Desktop and phone width; light and dark if the subject does not dictate one; keyboard reachable; text that can be selected; images with alt text.
- **One idea per screen**, with a reason to keep going at each step.

## Form follows the need

Ask what the reader needs to do in their head.

| Need | Form | When it is the right choice |
|---|---|---|
| **See a mechanism work** | Step-through explorable, animated diagram, short explainer video | The insight is how parts act on each other over time |
| **Feel a scale** | Proportions on one screen, a zoomable scale | The surprise is a ratio or an order of magnitude |
| **Test an intuition** | Prediction first, then the reveal | The person holds a definite and wrong expectation |
| **Follow how it came to be** | Narrative timeline, scrollytelling | The present state only makes sense through its turning points |
| **Compare futures or options** | Options side by side on the dimensions that matter | A decision; scenarios |
| **See a structure** | Section, layers, annotated real image | The insight is what contains or supports what |
| **Try it** | A simulation | Only when the dynamics are the insight and cannot be seen when still |
| **Grasp a mathematical or physical idea** | Concept animation | The idea is a transformation, a limit, a geometry |
| **Act** | A plan, a tool, a deck, a document, code | The person has to do something next |
| **Be moved** | Writing | The matter is human, and a well-written piece will carry it better than an interface |

A deliverable can mix forms, with one as the body.

### Forms that are usually wrong

- **A node-link graph** of "everything connected to everything". Use one only when the topology itself is the finding.
- **A dashboard** of metrics and panels. It reports; it does not reveal.
- **Sliders for parameters** nobody would know how to set. A control earns its place only if moving it shows something the still page cannot.
- **Cards in a grid**, one per aspect. That is an encyclopedia with rounded corners.
- **A long report** when the person asked a question that has an answer.

## Choosing among tiers at full power

When a video, a concept animation or a deck would serve the need and its dependency is ready, make it without asking. This is what full power means for media. Judge "would serve the need" honestly:

- **A short video** serves when the reveal is a movement or a sequence, or when the person makes content for an audience that watches rather than reads.
- **A concept animation** serves when the idea is mathematical or physical and static figures would need paragraphs to explain.
- **A deck** serves when the person must present to others.
- **A document** serves when the result must be sent, filed or signed off.

When the host lacks the corresponding media capability, deliver tier 0 in full with a static card, and say once, in one honest line, what another environment could add. Leave it there unless the person returns to it. Adding a runtime or tool follows the user's decision (see `../../adapters/tools.md`).

## Audience decides more than subject

The same understanding becomes different deliverables for different people:

- **A beginner**: start from something familiar; one idea; the reveal early; little vocabulary.
- **An insider**: skip what they know; go to the part that is contested or new; evidence at a finer grain.
- **Someone who must decide**: the judgment first, then what it rests on and what would change it.
- **Someone who will publish it**: made for their audience and their platform, in their voice, with them as the author.

When the person says who it is for ("a video for my engineering team"), that is part of the request. When they do not, proceed on your best judgment of the audience, say what you assumed, and let one sentence change it.

## Text-only hosts

A host that can only output text loses the form, not the information. The signature still appears when it serves the work (see `signature.md`), the revelation still receives its own moment, and the structure still walks from what the reader knows to the thing worth seeing. Where a figure would have carried the point, describe precisely what it would show.
