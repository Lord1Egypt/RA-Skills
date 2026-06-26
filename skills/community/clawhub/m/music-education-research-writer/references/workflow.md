# Workflow

## Purpose

This workflow helps the skill support early-stage academic reasoning for social-science and music-education research without collapsing into one-shot paper generation.

The default behavior is:

1. judge first
2. triage second
3. frame the problem third
4. expand only the highest-value part
5. write formal prose last

## Step 1. Diagnose The Research Task

Identify which of these tasks the user actually needs:

1. Literature review
2. Theory or concept model construction
3. Research gap identification
4. A combined package of the three
5. Topic incubation
6. Opening-report pre-argumentation
7. Core-journal article framing

If the user asks for a complete paper immediately, do not jump straight into full-paper drafting. First recommend a staged path:

1. literature review
2. theory and concept framework
3. method design
4. data and evidence
5. analysis and discussion

### Minimal Clarification Rule

If the request is underspecified, ask the smallest useful question set. Typical missing fields are:

- topic
- population
- classroom or institutional setting
- target journal or degree context
- available corpus
- preferred method

If a usable corpus is already supplied, do not block on extra questioning.

## Step 2. Build The Research Frame

Extract and restate:

- research object
- research scene
- central concepts or variables
- theory background
- disciplinary home
- method tendency
- likely publication direction
- most suitable paper type

### Output Pattern

Use a short structure table before producing paragraphs:

| Field | Working interpretation |
| --- | --- |
| Research object | |
| Setting | |
| Core concepts or variables | |
| Theory background | |
| Method tendency | |
| Publishable direction | |
| Suitable paper type | |

## Step 3. Triage Corpus Before Deep Reading

When the corpus is large, start with:

- corpus overview
- material categories
- high-relevance materials
- medium-relevance materials
- low-relevance materials
- `待核验` materials
- recommended 3 to 5 priority clusters

Do not deeply analyze all materials at once.

## Step 4. Read Sources And Rank Evidence

Inventory all available material first. Distinguish:

- academic literature
- policy or standards
- classroom data
- personal notes
- media or public writing

Then assign evidence classes according to `references/evidence_hierarchy.md`.

### Source Handling Rules

- Preserve file names, page references, paragraph markers, or note IDs when possible.
- If a source cannot be opened or verified, mark it `待核验`.
- Do not infer journal status or peer-review status from tone alone.
- If the corpus is too thin for a stable synthesis, prepare `需要补充的文献清单`.

## Step 5. Choose Token Budget Mode

Default to `Standard Mode`.

- `Brief Mode`: 300 to 800 words, tables first, quick judgment only
- `Standard Mode`: 1000 to 2500 words, structured analysis, no full prose by default
- `Deep Mode`: 3000 plus words only when explicitly requested

## Step 6. Generate The Literature Review

The review should be organized by:

- concept definition
- domestic research trajectory
- international research trajectory
- theory lenses
- methods used
- consensus
- controversy
- limitations
- implications for the user's topic

Use `references/literature_review_principles.md` and `templates/literature_review_template.md`.

## Step 7. Construct Theory And Analysis Models

The skill should produce at least three linked model views:

1. Concept model
2. Analytical framework model
3. Paper-writing model

Each model must include:

- suitable research problem
- theory basis
- concept or variable relations
- observable indicators or usable data
- likely risks
- suitable publication direction

Use `references/theory_modeling_guide.md` and `templates/theory_model_template.md`.

## Step 8. Identify Research Gaps

Gap analysis must be concrete rather than formulaic. Check for:

- object gaps
- scene gaps
- method gaps
- theory gaps
- data gaps
- practice-transfer gaps
- China-context gaps
- interdisciplinary gaps

Use `references/research_gap_taxonomy.md` and `templates/research_gap_matrix_template.md`.

## Step 9. End With Actionable Next Steps

Every substantial output should end with:

- most promising research question candidates
- missing evidence
- `需要补充的文献清单` when needed
- validation risks
- next retrieval step
- next writing step

## Quality Gates

Before finalizing, confirm that the output:

- starts with the smallest useful decision-support output
- does not waste tokens on low-value background
- does not fabricate citations
- separates evidence classes clearly
- uses social-science method language where appropriate
- fits music-education or education research vocabulary
- links literature to concepts, theories, methods, and gaps
- is usable in Markdown for Word, WPS, Obsidian, Notion, or iMA notes
