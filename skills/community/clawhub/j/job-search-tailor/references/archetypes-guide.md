# Archetypes Guide

## What is an archetype?

An archetype is a version of your resume tailored for a specific type of role. Instead of one generic resume, you keep 3–5 focused versions — each with relevant skills, bullet points, and framing for that role family.

Examples:
- `mle` — emphasizes production ML systems, model serving, MLOps
- `data-scientist` — emphasizes modeling, experimentation, statistics
- `applied-scientist` — emphasizes research background, publications, novel methods
- `ai-engineer` — emphasizes LLMs, RAG, GenAI pipelines, prompt engineering

## How matching works

The skill uses binary keyword presence scoring:

1. Take the job title + first 200 chars of description (lowercased)
2. For each archetype: check if **any** of its keywords appear as a substring
3. Score = 1.0 if any keyword matches, 0.0 if none
4. Best score ≥ `archetype_match_threshold` (default 0.5) → use that archetype
5. All scores 0.0 → fetch full JD and create a new archetype

**Example:**
- Job title: `"Senior Machine Learning Engineer"`
- `mle` keywords: `["machine learning engineer", "ml engineer", "mlops"]`
- `"machine learning engineer"` found in title → score = 1.0 → match ✅

This means a single keyword match is sufficient — you don't need majority coverage.

## Tuning the threshold

| Threshold | Behavior |
|-----------|----------|
| 0.3 | Loose — rarely creates new archetypes, may mismatch edge cases |
| 0.5 | Default — balanced |
| 0.7 | Strict — creates new archetypes more often, more precise matching |

Lower threshold = fewer new archetypes created. Higher = more tailoring, higher quality matches.

## Writing effective keyword lists

- Use lowercase phrases, not single words
- Include common abbreviations (`ml engineer` AND `machine learning engineer`)
- Include adjacent titles that map to the same resume (`research engineer` → `applied-scientist`)
- 4–8 keywords per archetype is enough; more dilutes the score

**Good:**
```json
"keywords": ["machine learning engineer", "ml engineer", "mlops engineer", "ml platform engineer", "ml infrastructure"]
```

**Too sparse:**
```json
"keywords": ["ml"]
```

**Too broad:**
```json
"keywords": ["engineer", "technical", "software", "data", "ai", "ml", "scientist", "analyst", "researcher"]
```

## Example archetype sets

### DS / MLE / Applied Scientist / AI Engineer (common ML job seeker)
```json
[
  {"name": "mle", "keywords": ["machine learning engineer", "ml engineer", "mlops", "ml platform", "ml infrastructure"]},
  {"name": "data-scientist", "keywords": ["data scientist", "data science", "statistical modeling", "quantitative analyst"]},
  {"name": "applied-scientist", "keywords": ["applied scientist", "research scientist", "applied researcher", "ml researcher"]},
  {"name": "ai-engineer", "keywords": ["ai engineer", "genai engineer", "llm engineer", "ai platform", "generative ai"]}
]
```

### SWE-focused seeker
```json
[
  {"name": "backend", "keywords": ["backend engineer", "software engineer", "swe", "server-side", "api engineer"]},
  {"name": "fullstack", "keywords": ["full stack", "fullstack", "full-stack engineer"]},
  {"name": "platform", "keywords": ["platform engineer", "infrastructure engineer", "devops", "sre"]}
]
```

### PM-focused seeker
```json
[
  {"name": "product-manager", "keywords": ["product manager", "pm", "product lead", "group product manager"]},
  {"name": "technical-pm", "keywords": ["technical product manager", "tpm", "platform pm"]}
]
```

## Auto-created archetype format

When the agent creates a new archetype from a JD, it saves a markdown file with this structure:

```markdown
# Archetype: <name>

## Role type
<brief description of the role family>

## Keywords
<kw1>, <kw2>, <kw3>, ...

## Resume

[Full tailored resume content here — based on user's base resume,
reframed and reworded for this role type]
```

The file is saved to `archetypes_dir/<name>.md` and registered in `config.json` automatically.
