## Description: <br>
Capture, search, verify, export, import, and synthesize Methodological Yield Reports (MYRs) for OODA-based intelligence compounding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordangreenhall](https://clawhub.ai/user/jordangreenhall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent maintainers use MYR to install and operate a node, store and search OODA-cycle yield, verify and sign reports, sync with peers, and produce weekly or cross-node syntheses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends a one-line curl-to-bash install path. <br>
Mitigation: Review the repository and installer before use, or use the manual install path with a pinned revision. <br>
Risk: The skill can start a persistent HTTP server for peer synchronization. <br>
Mitigation: Run the server only on a trusted network and verify reachability, authentication, and peer trust before syncing. <br>
Risk: Peer approval and auto-approval can expose data to unintended peers if trust is misconfigured. <br>
Mitigation: Keep auto-approval disabled unless the environment is controlled, verify peer fingerprints out of band, and confirm which reports are marked shareable. <br>


## Reference(s): <br>
- [MYR ClawHub skill page](https://clawhub.ai/jordangreenhall/myr) <br>
- [jordangreenhall ClawHub publisher profile](https://clawhub.ai/user/jordangreenhall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, SQL, and XML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Required output includes the action performed, affected artifact IDs, verification result, and next recommended step.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
