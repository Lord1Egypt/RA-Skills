## Description: <br>
Guides an agent through authorized OSINT workflows for building structured personal-profile reports from public information, with source mapping, confidence scoring, gap tracking, and compliance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavegeometry](https://clawhub.ai/user/wavegeometry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, auditors, researchers, and due-diligence reviewers use this skill for authorized digital-footprint assessments, privacy exposure reviews, and defensive social-engineering analysis. It should be used only with consent or another clear legal basis because it can assemble sensitive profiles about individuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to assemble detailed dossiers on people from minimal identifiers. <br>
Mitigation: Use it only for authorized privacy audits, defensive exposure assessments, lawful due diligence, or research with consent or another clear legal basis. <br>
Risk: Generated profiles may contain sensitive personal information and uncertain inferences. <br>
Mitigation: Minimize collection, label sources and confidence, review inferences before use, store results locally with appropriate access controls, and delete them when no longer needed. <br>
Risk: OSINT collection can cross legal, platform, or privacy boundaries if expanded beyond public and authorized sources. <br>
Mitigation: Respect applicable law, platform terms, robots.txt, and the skill's own prohibitions on private communications, credential material, social engineering, leaked databases, and minor-focused profiling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wavegeometry/skills/osint-personal-profiler) <br>
- [Publisher profile](https://clawhub.ai/user/wavegeometry) <br>
- [OSINT task catalog](references/osint-pp-catalog.md) <br>
- [OSINT methodology requirements](references/osint-pp-requirements.md) <br>
- [Output exemplars](references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown reports with tables, confidence labels, source lists, and gap summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain sensitive personal-profile information and should be minimized, protected, reviewed, and deleted when no longer needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
