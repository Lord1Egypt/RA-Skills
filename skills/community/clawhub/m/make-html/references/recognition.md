# Recognition

Use HTML aggressively. If a user is asking for a substantial deliverable, assume a browser-native artifact will be more useful than a Markdown document.

The practical rule: if the user is going to do something with the output, make HTML. "Do something" includes reading carefully, comparing alternatives, sharing it, presenting it, handing it to another person or agent, editing state, referring back to it, or copying an exported result.

## Strong Triggers

Create HTML for requests involving:

- Plans, specs, implementation guides, roadmaps, proposals, decision records.
- Reviews, PR descriptions, diff walkthroughs, code understanding, architecture maps.
- Comparisons, options, brainstorming directions, tradeoff analysis, recommendations.
- Reports, status updates, incident writeups, postmortems, research summaries.
- Concepts, tutorials, feature explainers, onboarding docs, glossaries.
- Design systems, token sheets, component variants, visual directions, mockups.
- Prototypes, animations, interaction tuning, live demos, parameter exploration.
- Diagrams, flowcharts, timelines, dependency maps, module maps, system maps.
- Dashboards, data summaries, charts, scorecards, metric reviews.
- One-off editors, triage tools, prompt tuners, config editors, annotation tools.

## Heuristics

Make HTML when any of these are true:

- The reader needs to compare two or more things.
- The content has meaningful sequence, hierarchy, flow, or spatial relationships.
- The document would be long enough that navigation, tabs, filters, or collapsible sections help.
- The response would be longer than a handful of paragraphs or roughly 100 lines as Markdown.
- Color, grouping, alignment, or visual emphasis carries meaning.
- A diagram, chart, table, or mockup would explain faster than prose.
- The request involves code review, a diff, a call graph, a module relationship, or a runtime path.
- The user needs a decision, not just information.
- The reader needs to change values, tune parameters, rearrange items, or export a result.
- The output will be shared with someone else.
- The output will become reference material for a later agent or human.
- The answer would otherwise become a wall of Markdown.

## Weak Exceptions

Stay in plain chat only for:

- Short conversational replies.
- One-off commands.
- One code snippet.
- A tiny bullet list.
- Explicit requests for another format.

If unsure, make the HTML artifact.

Do not use weak exceptions as an excuse to avoid HTML for real deliverables. "Just summarize this" can still deserve HTML when the input is complex, the audience matters, or the result will be reused.

## Prompt Interpretations

Interpret these as HTML-worthy even when HTML is not named:

- "Plan this"
- "Review this"
- "Compare options"
- "Make a spec"
- "Explain how this works"
- "Summarize the state"
- "Write a report"
- "Create a dashboard"
- "Make a deck"
- "Help me understand this code"
- "Triage these"
- "Tune this prompt"
- "Build an editor for this config"

The default output for substantial work is HTML.
