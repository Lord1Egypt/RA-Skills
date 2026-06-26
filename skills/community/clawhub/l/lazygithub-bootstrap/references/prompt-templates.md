# Prompt Templates

## Universal prompt

Use this with any capable coding agent:

```text
Create or publish this project as a GitHub repository.

Requirements:
- Fill the repository README if it is missing or too empty.
- Fill the GitHub About section completely.
- Treat About as: description + homepage + topics.
- Do not stop after setting only description.
- Infer the description and 3-5 relevant topics from the codebase and README when possible.
- Topics are required unless you explicitly explain, with evidence from the project, why no topic is defensible.
- If topics are still empty at the end, treat the task as failed.
- Ask me only if a required value cannot be inferred safely.
- After creating/updating the repo, verify the final metadata.
- Your verification must show that repository topics are non-empty.

Preferred output:
- repo URL
- description used
- homepage used
- topics used
- verification result
```

## Codex-flavored prompt

```text
Create/publish this project to GitHub and make sure both the README and the full About box are populated.

About must include:
1. description
2. homepage if available
3. topics

Workflow:
- inspect the project first
- infer a one-sentence description
- infer 3-5 useful lowercase topics
- create or update the repo with gh
- verify the final metadata instead of assuming success

Hard requirements:
- do not leave topics empty
- if verification shows zero topics, continue working instead of claiming completion
- only finish once repository topics are present, or explicitly report a blocker with evidence
```

## Claude-flavored prompt

```text
Please publish this project to GitHub and complete the repository presentation, not just the remote creation.

Specifically:
- improve or create a minimal README if needed
- fill the About area fully
- interpret About as description, website/homepage, and topics
- choose 3-5 concrete topics based on the actual project
- verify the final repository metadata after the changes

Requirements:
- topics are mandatory unless you can justify their absence with project-specific evidence
- if final verification shows no topics, do not present the task as complete
- report the exact topics chosen in the final summary

If something essential is missing and cannot be inferred safely, ask one concise question.
```
