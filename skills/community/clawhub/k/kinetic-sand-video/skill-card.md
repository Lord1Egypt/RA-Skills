## Description:

Generate vertical kinetic and magic sand satisfying shorts through WeryAI, using text prompts or public HTTPS sand-shape images to create slicing, mold-release, collapse, or pouring motion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to generate short vertical kinetic-sand ASMR videos from a brief or public HTTPS image, with prompt expansion and parameter checks before submitting WeryAI jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the documented quoted shell command pattern with untrusted prompt text can turn prompt content into shell syntax.

Mitigation: Invoke the Node script with structured arguments, stdin, or another non-shell mechanism rather than interpolating JSON into a quoted shell command.

Risk: The skill requires WERYAI_API_KEY and submits requests to external WeryAI API hosts.

Mitigation: Use it only in an environment where the API key is intentionally available, keep the key out of skill packages and logs, and run generation in an isolated or short-lived environment when higher assurance is needed.

Risk: Successful wait runs consume paid WeryAI credits and repeated runs create new paid tasks.

Mitigation: Confirm parameters before submission, use dry-run or status checks where appropriate, and avoid automatic retries that submit new generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/kinetic-sand-video)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI model registry API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with command snippets and JSON API results that include generated video URLs or failure details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and paid WeryAI credits; image inputs must be public HTTPS URLs.]

## Skill Version(s):

0.1.1 (source: ClawHub server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
