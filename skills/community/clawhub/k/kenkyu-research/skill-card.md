## Description:

Run multi-source research through the kenkyu API and return relevant source links and verbatim extracts to support a cited answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[george3d6](https://clawhub.ai/user/george3d6)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and other users ask an agent to investigate a question across multiple sources, review relevant extracts, and write a sourced answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and the account token are sent to kenkyu.dev; sensitive queries may disclose confidential or personal information.

Mitigation: Review the provider's data handling before use, keep the token private, and avoid sending secrets or sensitive queries unless authorized.

Risk: Research runs may consume paid account balance.

Mitigation: Check the account balance and choose an appropriate time limit before starting a run.

## Reference(s):

- [Kenkyu service](https://kenkyu.dev)
- [Kenkyu Research skill release](https://clawhub.ai/george3d6/skills/kenkyu-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answer with source links and relevant extracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent reviews returned source extracts and cites the links in its answer.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
