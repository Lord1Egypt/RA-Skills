# Pipeline Templates — Built-in POP Pipelines

## 1. Idea to Publish

**Trigger:** `/pop idea-to-publish "Your idea title"`
**Purpose:** Take a raw idea from spark to published document.

```json
{
  "pipeline": "idea-to-publish",
  "steps": [
    {
      "id": "spark",
      "action": "create_note",
      "params": {
        "title": "$INPUT.title",
        "content": "$INPUT.description",
        "folder": "Pipeline/Sparks",
        "tags": ["spark", "pipeline"]
      }
    },
    {
      "id": "expand",
      "action": "ai_expand",
      "params": {
        "note_id": "$spark.output.id",
        "prompt": "Expand this idea into a structured outline with: introduction, key arguments, evidence needed, conclusion. Maintain the original voice."
      }
    },
    {
      "id": "visual",
      "action": "generate_figure",
      "params": {
        "note_id": "$expand.output.id",
        "style": "publication",
        "format": "svg"
      }
    },
    {
      "id": "verify",
      "action": "wave_check",
      "params": {
        "content": "$expand.output.content"
      }
    },
    {
      "id": "assemble",
      "action": "merge_notes",
      "params": {
        "ids": ["$spark.output.id", "$expand.output.id"],
        "title": "DRAFT: $INPUT.title"
      }
    },
    {
      "id": "export",
      "action": "export_pdf",
      "params": {
        "note_id": "$assemble.output.id",
        "template": "academic"
      }
    }
  ],
  "coherence_threshold": 0.85
}
```

**Expected duration:** 2-5 minutes
**Output:** PDF in vault + ATOM trail entry

## 2. Research Digest

**Trigger:** `/pop research-digest "topic"`
**Purpose:** Fetch, summarize, and organize research on a topic.

```json
{
  "pipeline": "research-digest",
  "steps": [
    {
      "id": "fetch",
      "action": "search_vault",
      "params": {
        "query": "$INPUT.topic",
        "limit": 20
      }
    },
    {
      "id": "summarize",
      "action": "ai_expand",
      "params": {
        "note_id": "$fetch.output.results[0].id",
        "prompt": "Summarize the key findings across all related notes on: $INPUT.topic. Identify themes, contradictions, and gaps."
      }
    },
    {
      "id": "score",
      "action": "wave_check",
      "params": {
        "content": "$summarize.output.content"
      }
    },
    {
      "id": "tag",
      "action": "tag_note",
      "params": {
        "note_id": "$summarize.output.id",
        "tags": ["digest", "research", "$INPUT.topic"]
      }
    },
    {
      "id": "canvas",
      "action": "create_note",
      "params": {
        "title": "Research Digest: $INPUT.topic",
        "content": "$summarize.output.content",
        "folder": "Pipeline/Digests"
      }
    }
  ],
  "coherence_threshold": 0.80
}
```

**Expected duration:** 1-3 minutes
**Output:** Tagged digest note in vault

## 3. Quantum Circuit

**Trigger:** `/pop quantum-circuit "circuit name"`
**Purpose:** Generate, verify, and export a quantum circuit as Minecraft redstone.

```json
{
  "pipeline": "quantum-circuit",
  "steps": [
    {
      "id": "generate",
      "action": "create_note",
      "params": {
        "title": "Circuit: $INPUT.name",
        "content": "Quantum circuit specification for conservation law verification.\nCircuit: $INPUT.name\nConstraint: ALPHA + OMEGA = 15",
        "folder": "Pipeline/Circuits"
      }
    },
    {
      "id": "verify",
      "action": "wave_check",
      "params": {
        "content": "$generate.output.content"
      }
    },
    {
      "id": "export_mcf",
      "action": "ai_expand",
      "params": {
        "note_id": "$generate.output.id",
        "prompt": "Convert this circuit specification to Minecraft .mcfunction format. Use setblock commands for redstone components. Ensure conservation law is enforced: input signal strength + output signal strength = 15."
      }
    },
    {
      "id": "place",
      "action": "create_note",
      "params": {
        "title": "MCFunction: $INPUT.name",
        "content": "$export_mcf.output.content",
        "folder": "Pipeline/MCFunctions",
        "tags": ["mcfunction", "quantum", "conservation"]
      }
    }
  ],
  "coherence_threshold": 0.90
}
```

**Expected duration:** 1-2 minutes
**Output:** .mcfunction-formatted note ready for Minecraft export

## 5. Resonance Cascade

**Trigger:** `/pop resonance-cascade "scientific concept"`
**Purpose:** Generate a blog post about a scientific concept, create a visual representation, and then publish the blog post to a hypothetical platform with ATOM authentication.

```json
{
  "pipeline": "resonance-cascade",
  "description": "Generate a blog post about a scientific concept, create a visual representation, and publish it to a platform with ATOM authentication.",
  "steps": [
    {
      "id": "research",
      "action": "search_vault",
      "params": {
        "query": "$INPUT.concept",
        "limit": 30
      }
    },
    {
      "id": "summarize",
      "action": "ai_expand",
      "params": {
        "note_id": "$research.output.results[0].id",
        "prompt": "Summarize the key findings across all related notes on: $INPUT.concept. Identify the core principles and potential applications."
      }
    },
    {
      "id": "visualize",
      "action": "generate_figure",
      "params": {
        "note_id": "$summarize.output.id",
        "style": "scientific",
        "format": "svg"
      }
    },
    {
      "id": "draft",
      "action": "ai_expand",
      "params": {
        "note_id": "$summarize.output.id",
        "prompt": "Write a blog post based on the summary and the generated figure. Use a catchy title and engaging language. Target audience: general public with some scientific background."
      }
    },
    {
      "id": "wave_check",
      "action": "wave_check",
      "params": {
        "content": "$draft.output.content"
      }
    },
    {
      "id": "publish",
      "action": "create_note",
      "params": {
        "title": "Published: $INPUT.concept",
        "content": "$draft.output.content",
        "folder": "Published",
        "tags": ["blog", "science", "$INPUT.concept"]
      }
    }
  ],
  "coherence_threshold": 0.88
}
```

**Expected duration:** 3-7 minutes
**Output:** Blog post note in the vault
**Purpose:** Full academic paper generation pipeline.

```json
{
  "pipeline": "paper-draft",
  "steps": [
    {
      "id": "rag",
      "action": "search_vault",
      "params": {
        "query": "$INPUT.title",
        "limit": 50
      }
    },
    {
      "id": "outline",
      "action": "ai_expand",
      "params": {
        "note_id": "$rag.output.results[0].id",
        "prompt": "Create an academic paper outline for: $INPUT.title\nSections: Abstract, Introduction, Related Work, Methodology, Results, Discussion, Conclusion\nUse the search results as source material."
      }
    },
    {
      "id": "draft",
      "action": "ai_expand",
      "params": {
        "note_id": "$outline.output.id",
        "prompt": "Write the full paper draft following the outline. Include citations in [Author, Year] format. Target 4000-6000 words."
      }
    },
    {
      "id": "figures",
      "action": "generate_figure",
      "params": {
        "note_id": "$draft.output.id",
        "style": "academic",
        "format": "svg"
      }
    },
    {
      "id": "verify",
      "action": "wave_check",
      "params": {
        "content": "$draft.output.content"
      }
    },
    {
      "id": "export",
      "action": "export_pdf",
      "params": {
        "note_id": "$draft.output.id",
        "template": "arxiv"
      }
    }
  ],
  "coherence_threshold": 0.85
}
```

**Expected duration:** 5-15 minutes
**Output:** PDF paper with figures, ready for arXiv submission
