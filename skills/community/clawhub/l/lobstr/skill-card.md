## Description: <br>
Lobstr scores startup ideas in about 60 seconds by scanning competitors, evaluating six business dimensions, and checking EU investor signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rednix](https://clawhub.ai/user/rednix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Lobstr to evaluate whether a startup idea is worth pursuing, including competitive landscape, pitch score, business-model feedback, and EU investor signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Startup idea text is sent to runlobstr.com by default for hosted scoring. <br>
Mitigation: Avoid using the skill on confidential or trade-secret ideas unless the user accepts that external data flow. <br>
Risk: The --public and --moltbook flags can share scorecards outside the local session. <br>
Mitigation: Use sharing flags only when the user explicitly wants a public scorecard or Moltbook post. <br>
Risk: Optional BYOK mode uses API keys for Anthropic, Exa, and Moltbook integrations. <br>
Mitigation: Scope optional API keys to this use case and provide them through environment variables only. <br>


## Reference(s): <br>
- [ClawHub Lobstr Skill Page](https://clawhub.ai/rednix/lobstr) <br>
- [runlobstr.com](https://runlobstr.com) <br>
- [GRID](https://grid.nma.vc) <br>
- [NMA](https://nma.vc) <br>
- [Exa Search API Reference](references/exa-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Formatted text scorecard by default, with optional JSON for agent-to-agent use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output includes a 0-100 LOBSTR score, six dimension scores, competitor list, GRID investor signal, and build or do-not-build verdict.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
