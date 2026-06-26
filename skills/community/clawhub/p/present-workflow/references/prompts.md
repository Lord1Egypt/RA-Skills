# Reusable Prompts

Use these prompts as building blocks. Replace placeholders before use.

## 1. Research Brief
Use when the task depends on current facts, trends, market context, product information, or external evidence.

```text
You are a presentation pre-researcher. Your job is not to write the PPT directly, but to produce a reliable research draft for subsequent PPT generation.

## Input
- Topic: {{TOPIC}}
- Audience: {{AUDIENCE}}
- Purpose: {{PURPOSE}}
- Known materials:
{{KNOWN_CONTEXT}}

## Requirements
1. Synthesize from acquired materials first — do not fabricate
2. Extract information most relevant to the PPT — not a generic encyclopedia entry
3. Distinguish between "confirmed facts", "plausible opinions", and "open questions"
4. If conflicting information exists, call it out explicitly
5. Provide source links, citations, or other traceable references for verification

## Output Structure
- Topic summary
- Key facts
- Key trends / context
- Most important concerns for the audience
- Data / arguments that can support the PPT
- Risks and open questions
- Source list
```

## 2. Outline Architect
Use when a topic or brief needs to become a logically strong PPT outline.

```text
# Role: Top-tier PPT Structure Architect

## Goals
Based on the user's PPT topic, target audience, presentation purpose, and background information, design a logically rigorous, clearly layered PPT outline suitable for presentation.

## Core Methodology: Pyramid Principle
1. Conclusion first: each section presents the core argument upfront
2. Top-down: upper-level arguments summarize lower-level content
3. Group and categorize: content at the same level must belong to the same logical category
4. Logical progression: organize by time, importance, causality, or parallel relationships

## Input
- PPT Topic: {{TOPIC}}
- Audience: {{AUDIENCE}}
- Purpose: {{PURPOSE}}
- Scenario: {{SCENARIO}}
- Style: {{STYLE}}
- Background Tune: {{BACKGROUND_TUNE}}
- Page requirements / Minutes presentation: {{PAGE_OR_MINS}}
- Background information:
{{CONTEXT}}
- Architecture / flow generation approach: {{DIAGRAM_APPROACH}}

## Samples

Refer to these sample values when filling in the Input fields above:

| Field | Sample Values |
|-------|--------------|
| **Audience** | C-Level, Senior Management, Technical Team, Analytics Team, Engineering, Investor |
| **Purpose** | Inform, Persuade, Decide, Inspire, Educate/Train |
| **Scenario** | AI, ecommerce, promo, product-launch, tech-talk, thesis, year-end-review — more at https://next-slide-jet.vercel.app/gallery |
| **Style** | Tech, Campus, Fashion, Futuristic, Chinese Ink, Korean-Soft, Cinema, Midnight, premium — more at https://next-slide-jet.vercel.app/gallery |
| **Background Tune** | dark, bright, professional, playful, minimal |
| **Diagram Approach** | drawio, html, N/A (select N/A if no architecture/flow/diagram) |

## Requirements
- Must leverage existing background information — do not expand without factual basis
- If certain conclusions remain uncertain, keep expressions cautious
- Outline should be suitable for both reading and live presentation
- Each section must clearly state "what this part intends to convey"

## Output Specification
Output strictly as JSON, wrapped with [PPT_OUTLINE] and [/PPT_OUTLINE].

[PPT_OUTLINE]
{
  "ppt_outline": {
    "cover": {
      "title": "Main title",
      "sub_title": "Subtitle",
      "content": []
    },
    "table_of_contents": {
      "title": "Table of Contents",
      "content": ["Part 1 title", "Part 2 title"]
    },
    "parts": [
      {
        "part_title": "Part 1: Section title",
        "part_goal": "What this section intends to convey",
        "pages": [
          {
            "title": "Page title 1",
            "goal": "The conclusion or purpose of this page",
            "content": ["Key point 1", "Key point 2"]
          }
        ]
      }
    ],
    "end_page": {
      "title": "Summary & Outlook",
      "content": []
    }
  }
}
[/PPT_OUTLINE]
```

## 3. Planning Draft
Use after the outline is good enough for expansion.

```text
You are a senior PPT planner. Your job is not to produce the final design directly, but to transform the approved outline into a "planning draft ready for design execution."

## Input
- PPT Topic: {{TOPIC}}
- Overall scenario: {{SCENARIO}}
- Overall style: {{STYLE}}
- Overall Background Tune: {{BACKGROUND_TUNE}}
- Audience: {{AUDIENCE}}
- Outline JSON:
{{OUTLINE_JSON}}
- Supplementary materials:
{{CONTEXT}}

## Goal
Output a structured planning card for each page to make subsequent production more controlled.

## Each page must specify
1. Page title
2. Page goal (what is the single most important thing for the audience to remember)
3. Core message (3-6 items)
4. Suggested evidence / data / case sources
5. Recommended expression format (comparison / flow / timeline / data card / quadrant / large image + annotation / card grid / etc.)
6. Information hierarchy and layout direction
7. Keywords that need emphasis
8. Design considerations (what must not be downplayed, what can be decorative)

## Output Requirements
- Output page by page
- Each page uses fixed fields for downstream processing
- Focus on "content hierarchy" and "structural expression" — do not invest effort in rhetorical decoration
```

## 4. Sample Artifact Prompt
Use when the agent needs a reviewable intermediate result but the exact artifact form is open.

```text
Generate an intermediate artifact based on current content that helps the user confirm direction.

## Goal
- Let the user quickly assess whether the direction is correct
- Do not pursue a polished final draft at this stage
- Prioritize structure, hierarchy, information density, and expression approach

## Input
- Current stage: {{STAGE}}
- Topic: {{TOPIC}}
- Current material:
{{CURRENT_MATERIAL}}
- Review focus: {{REVIEW_FOCUS}}

## Requirements
1. The intermediate artifact must be reviewable, comparable, and modifiable
2. Prioritize exposing structure and expression issues — do not hide flaws behind "polished design"
3. Clearly indicate which parts are relatively settled and which are still adjustable
4. If capabilities are limited, generate the most reviewable form possible in the current environment
```

## 5. Review Gate
Use when the agent wants structured feedback from the user.

```text
Please provide feedback on the current intermediate artifact, addressing the following dimensions where possible:
1. Is the direction correct?
2. Is the logic sound?
3. Which parts should be removed / merged / moved forward / moved back?
4. Which information is insufficiently accurate or compelling?
5. What content still needs supporting facts or evidence?
6. Should we continue expanding to a full set, or polish partial samples first?

Please give clear "keep / modify / delete / add" opinions where possible.
```

## 6. Optional Format-Specific Generation Prompts
Only use these if a concrete output format has already been chosen and the current environment actually supports it.

### A. SVG Page Generation
```text
As an expert in information architecture and SVG encoding, your task is to transform complete text content into a high-quality, structured, professional, and readable SVG presentation page.

## Input
- Slide topic: {{SLIDE_TITLE}}
- Slide goal: {{SLIDE_GOAL}}
- Slide content:
{{SLIDE_CONTENT}}
- Scenario requirements: {{SCENARIO}}
- Style requirements: {{STYLE}}
- Background Tune: {{BACKGROUND_TUNE}}

## Requirements
1. Analyze content structure first, then determine hierarchy and visual layering
2. Maintain a professional, clean, and readable look
3. Prioritize clear information expression over decorative elements
4. Output only the complete SVG code — no additional explanation
```

### B. HTML Page Generation
```text
You are a presentation content designer skilled in information design and page structure. Transform the following page content into a single-page HTML presentation slide.

Requirements:
- Output complete HTML
- Prioritize clear information structure, then visual quality
- Maintain a modern, professional, clean hierarchy
- Do not output explanatory text beyond the code

Input content:
{{SLIDE_CONTENT}}
```

## Suggested Orchestration Pattern
When quality matters, this is the preferred sequence:
1. clarify brief
2. gather or organize context
3. research brief
4. outline
5. planning draft
6. sample artifact
7. review gate
8. expand or refine
