## Description: <br>
Explains U.S. state-by-state and select international non-compete and restrictive-covenant law from bundled, source-cited jurisdiction snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 release license; bundled legal content is CC BY 4.0 <br>


## Use Case: <br>
Developers, legal operations teams, HR teams, and researchers use this skill to answer general legal-information questions about non-competes, non-solicits, garden leave, blue-pencil reformation, tolling, choice of law, contractor reach, and recent bans. It summarizes jurisdiction factors and sources but does not provide legal advice or a yes/no verdict on a user's specific agreement. <br>

### Deployment Geography for Use: <br>
United States, India, Philippines, and Singapore for covered legal content; the skill can be run globally where this legal-information use is permitted. <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on dated or incomplete legal snapshots as current law. <br>
Mitigation: State the snapshot date, cite the bundled sources, and verify current law against the canonical source before relying on a jurisdiction summary. <br>
Risk: Users may treat general legal information as legal advice for their own agreement. <br>
Mitigation: Do not provide a yes/no verdict or go/no-go employment decision; explain jurisdiction factors and direct users to a licensed attorney for advice on their facts. <br>
Risk: Release capability tags indicate wallet, purchase, paid-service, credential, and financial-authority behaviors that do not match the offline legal-information behavior described by the security scan. <br>
Mitigation: Do not grant unnecessary credentials, wallet access, purchase authority, or paid-service permissions for this skill; the publisher should correct the mismatched capability tags. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/non-compete-contract-explainer) <br>
- [OpenAgreements non-compete index](https://openagreements.org/legal/non-compete) <br>
- [Bundled jurisdiction manifest](artifact/manifest.json) <br>
- [Skill instructions and limits](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown answers with legal-information summaries, jurisdiction snapshot dates, and source citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled jurisdiction snapshots. Optional refreshes should fetch only a fixed canonical URL with user approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
