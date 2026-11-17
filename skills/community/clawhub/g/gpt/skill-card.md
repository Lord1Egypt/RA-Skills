## Description:

Generate GPT API request payloads. Use when building chat completions, embeddings, fine-tuning data, or estimating API costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare GPT API payloads, embedding requests, fine-tuning JSONL, batch request files, format conversions, and rough API cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cost estimator can execute local commands when unsafe numeric arguments are supplied.

Mitigation: Do not pass untrusted or agent-supplied values to the cost command until the AWK injection issue is fixed; review numeric arguments before running it.

Risk: Generated embedding, batch, and fine-tuning files may be used for external API uploads.

Mitigation: Exclude secrets, private records, and confidential datasets unless that use is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/gpt)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON, JSONL, CSV, and plain-text cost tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands write to stdout by default and can write generated artifacts to a file when an output option is supplied.]

## Skill Version(s):

3.4.1 (source: server release metadata; artifact frontmatter lists 3.4.0 and script header lists 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
