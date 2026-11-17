## Description:

Lunheng is an AI-assisted Chinese judgment drafting skill for syllogistic legal reasoning, judgment drafting and revision, citation checking, quality scoring, sentencing calculation, HTTP API service, batch processing, and case retrieval across 74 case types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawrencepage](https://clawhub.ai/user/lawrencepage)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals and developers use Lunheng to draft and review Chinese court judgment documents, validate legal citations, retrieve similar cases, score reasoning quality, and format outputs for professional legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles confidential case facts and API credentials.

Mitigation: Use an isolated virtual environment, dedicated low-privilege API keys, and redact personal or confidential data before processing.

Risk: Case text may be transmitted to a configured LLM API provider.

Mitigation: Verify LH_LLM_BASE_URL points to a trusted HTTPS endpoint or use an explicit local provider before using real cases.

Risk: The REST server can expose legal case workflows if bound beyond local access.

Mitigation: Keep the server on loopback and avoid exposing it to untrusted networks.

Risk: Generated legal drafts or citation checks may be incorrect or incomplete.

Mitigation: Require review by a qualified legal professional before use.

Risk: Process output and logs may contain case information.

Mitigation: Treat stderr, logs, and generated files as sensitive and apply appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lawrencepage/skills/lunheng)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Knowledge router](refs/knowledge_router.md)
- [Formatting standard](refs/formatting_standard.md)
- [IMA search workflow](refs/ima_search.md)
- [Evaluation framework](refs/eval_framework.md)
- [Shape-spirit corpus README](data/shape_spirit/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML files, text reports, JSON-compatible command inputs, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated legal documents under workspace/output and may transmit case text to the configured LLM API provider.]

## Skill Version(s):

3.0.5 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
