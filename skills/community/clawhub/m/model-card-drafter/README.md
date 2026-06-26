# model-card-drafter

**Domain:** MLOps  
**Skill:** `model-card-drafter`  
**Version:** 0.1.0

## What It Does

Converts a model description, training details, and evaluation results into a structured Model Card — the standard responsible-AI artifact for documenting a machine-learning or AI model's intended use, performance characteristics, limitations, and ethical risks.

Produces a **DRAFT** Model Card aligned to:
- Google's Model Cards specification (Mitchell et al., 2019)
- EU AI Act technical documentation requirements (Annex IV for high-risk AI systems)
- Responsible AI Institute and Partnership on AI documentation standards

## When to Use

Use this skill when an ML engineer, data scientist, MLOps practitioner, or responsible-AI lead needs to:

- Draft a Model Card for a newly trained or fine-tuned model before deployment
- Produce model documentation required by internal AI governance policy
- Prepare technical documentation for EU AI Act Annex IV compliance
- Document a model for publication (e.g., Hugging Face Model Hub, academic paper supplement)
- Create an audit trail for a model used in a regulated domain (healthcare, finance, employment, criminal justice)

## Scope and Boundaries

**This skill covers:**
- Model identification and version information
- Intended use and out-of-scope use documentation
- Training data description and known biases
- Evaluation data and performance metrics (overall and disaggregated)
- Ethical considerations including sensitive attributes and potential harms
- Limitations, failure modes, and deployment recommendations
- Reviewer sign-off block

**This skill does not:**
- Train, evaluate, or modify a model
- Conduct bias audits or run evaluation pipelines
- File documents with regulators
- Guarantee regulatory compliance — the DRAFT requires governance and legal review

## Output

A structured Markdown Model Card labeled **DRAFT**, with all documentation gaps flagged for resolution before publication or regulatory use.

## Example Use Cases

- An ML team at a health-tech startup needs to document a readmission-risk classifier before deploying it in a hospital EHR
- A government AI team must produce Annex IV technical documentation for an EU AI Act high-risk system
- A data science team is publishing a new NLP model to Hugging Face and needs a model card for the model page
- A financial services firm needs an audit-ready model card for a credit-scoring model

## Feedback & Contributions

Have feedback or a use case this skill doesn't cover? Open an issue at:  
https://github.com/archlab-space/Open-Skill-Hub/issues
