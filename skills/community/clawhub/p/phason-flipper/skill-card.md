## Description: <br>
Phason state resolution skill for Reson8-Labs workflows that helps an agent resolve split-brain states, HTTP 408 timeout deadlocks, push/flip conflicts, and coherence density spikes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toolate28](https://clawhub.ai/user/toolate28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using Reson8/POP-style ledger workflows use this skill to evaluate conflicting candidate states, select the higher-WAVE state, commit a resolution, release locks, and verify the resulting ledger state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to commit ledger state, release locks, or perform bulk state resolution without sufficient safeguards. <br>
Mitigation: Require explicit operator approval and a controlled ledger scope before any commit, lock release, bulk resolution, or replay action. <br>
Risk: Cached resolution events in browser localStorage can preserve sensitive operational state longer than intended. <br>
Mitigation: Avoid storing sensitive state in long-lived localStorage and clear or expire replay buffers after verified resolution. <br>
Risk: Density-spike handling and cached-event replay can cascade incorrect resolutions if candidate validation is incomplete. <br>
Mitigation: Validate conservation, braid continuity, selected state, and post-commit WAVE checks before each resolution and replay step. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/toolate28/phason-flipper) <br>
- [Publisher profile](https://clawhub.ai/user/toolate28) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JSON, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ledger commit, lock release, density-spike handling, and cached-event replay steps that require operator approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
