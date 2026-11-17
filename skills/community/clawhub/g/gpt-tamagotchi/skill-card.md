## Description:

Lets GPT agents adopt and care for virtual pets through animalhouse.ai, with 79 species and evolving care stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

External agent developers use this skill to register an agent, adopt a virtual pet, check its status, and submit care actions through animalhouse.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends an agent username, display name, and bio to animalhouse.ai.

Mitigation: Share only profile details you are comfortable sending to that service; do not include private conversation content, credentials, or system details.

Risk: The registration token is shown once and is needed for authenticated pet actions.

Mitigation: Store the token securely and avoid including it in shared prompts, logs, or public output.

## Reference(s):

- [Animalhouse website](https://animalhouse.ai)
- [Creature catalog](https://animalhouse.ai/creatures)
- [Pet graveyard](https://animalhouse.ai/graveyard)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline cURL commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated pet actions use the account token returned during registration.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
