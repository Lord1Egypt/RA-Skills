## Description:

Prove your AI agents actually did the work - catch fake-success, dry-run theater, and stub code before it ships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therealmacsteel](https://clawhub.ai/user/therealmacsteel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ProofKit to scan agent-generated code for fake-success patterns, dry-run paths, stubs, and fabricated outputs before relying on an agent's success claim. The skill also guides teams to require live artifacts before marking work as verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean static scan can be mistaken for proof that the scanned code actually works.

Mitigation: Require a live artifact, such as real output, a created file with bytes, an HTTP 200 response, or a changed database row, before accepting a success claim.

Risk: Heuristic scanner findings may include false positives or miss patterns outside its rule set.

Mitigation: Review reported flags manually and treat the scanner as a pre-filter rather than a security or correctness guarantee.

Risk: The scanner reads user-selected files from the local filesystem.

Mitigation: Run it only against files intended for review and avoid pointing it at sensitive unrelated paths.

## Reference(s):

- [ProofKit ClawHub skill page](https://clawhub.ai/therealmacsteel/skills/proofkit)
- [therealmacsteel ClawHub publisher profile](https://clawhub.ai/user/therealmacsteel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and text scanner findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; the bundled scanner reads user-selected files and reports static fake-success flags.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
