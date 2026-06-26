## Description: <br>
Intent-alignment orchestration for OpenClaw agent teams across diverse host environments where work must stay anchored to user goals while allowing flexible execution across coding, multi-phase delivery, multi-agent coordination, and evolving requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent-team operators use this skill to keep multi-phase coding, repository, tracker, and multi-agent work aligned to user goals. It structures intent capture, ambiguity handling, phase planning, realignment, adapter selection, and verification gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run local tools and inspect repository files, including workspaces that contain secrets or production credentials. <br>
Mitigation: Review commands before allowing execution, run in the narrowest required workspace, and avoid exposing secrets or production credentials to the agent. <br>
Risk: Repository, GitHub, or tracker adapters may require read or write authorization for files, issues, pull requests, or task records. <br>
Mitigation: Grant least-privilege access, prefer read-only or local-hub fallback when write access is unnecessary, and confirm authorization paths before write operations. <br>
Risk: Ambiguous goals or changing requirements can cause work to drift from user intent during multi-phase execution. <br>
Mitigation: Use the intent quality gate, strictness mode, pre-execution clarification gate, and realignment protocol before continuing impacted phases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscraters/intent-align) <br>
- [Core Contract](references/core-contract.md) <br>
- [Alignment Hub Schema](references/alignment-hub-template.md) <br>
- [Realignment Protocol](references/realignment-protocol.md) <br>
- [Verification Gates](references/verification-gates.md) <br>
- [Capability Taxonomy](references/capability-taxonomy.md) <br>
- [GitHub Adapter](references/adapters/github.md) <br>
- [Local Repository Adapter](references/adapters/local-repo.md) <br>
- [Tracker Adapter](references/adapters/tracker-generic.md) <br>
- [Adapter Template](references/adapters/adapter-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML schemas, Mermaid diagrams, checklists, structured reports, and inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce alignment hub files, phase plans, adapter specs, verification evidence, clarification prompts, and final alignment reports.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
