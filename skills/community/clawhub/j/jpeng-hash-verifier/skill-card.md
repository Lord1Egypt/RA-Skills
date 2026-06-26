## Description: <br>
Verify data integrity with hashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security operators use this skill to verify file or data integrity with hashes and automate checksum validation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HASH_API_KEY could be exposed if hardcoded, echoed, or included in logs. <br>
Mitigation: Store HASH_API_KEY in a protected environment or secret manager and avoid printing it in command output or logs. <br>
Risk: The skill may be invoked outside explicit file-integrity or digest-checking tasks. <br>
Mitigation: Use it only for requested hash or checksum verification workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-hash-verifier) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HASH_API_KEY configuration and returns verification results as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
