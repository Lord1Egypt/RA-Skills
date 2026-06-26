## Description: <br>
The nervous system for sovereign AI entities — cross-pillar checks, LLM trust profiles, coherence detection, and signal routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to set up and operate NSE Orchestrator, which coordinates identity, wallet, calendar, relationship, and alignment pillars for cross-pillar checks, LLM trust scoring, coherence detection, and signal routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through identity, wallet, profile, calendar, memory, social, and alignment workflows that may affect sensitive accounts or real value. <br>
Mitigation: Use a test identity and limited wallet first, and require explicit user confirmation before payments, public profile updates, calendar changes, or persistent memory writes. <br>
Risk: Private Nostr keys, seed phrases, passphrases, wallet credentials, or API tokens may be exposed if pasted into chat or routed through the wrong tool. <br>
Mitigation: Never paste nsec values or seed phrases into chat; keep secrets in the relevant pillar package or environment, and review agent output before execution. <br>
Risk: The release depends on an external Python package and optional pillar packages outside the skill artifact. <br>
Mitigation: Install only from trusted package sources, review dependency provenance before use, and start with the minimum required pillars. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/nse-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/vveerrgg) <br>
- [Project homepage](https://github.com/HumanjavaEnterprises/nse-orchestrator.app.OC-python.src) <br>
- [PyPI package](https://pypi.org/project/nse-orchestrator/) <br>
- [NSE project site](https://nse.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes status checks, setup flows, package installation commands, and operational guardrails for agent use.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
