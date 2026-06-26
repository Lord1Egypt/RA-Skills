## Description: <br>
Investigative intelligence - document search, entity extraction, and relationship graphing for analyzing document corpuses and finding connections between people, organizations, and identifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aingestigate](https://clawhub.ai/user/aingestigate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investigators, analysts, and agents use this skill to search document corpuses, extract entities, trace relationship paths, retrieve source evidence, and upload new document sets for processing through a configured Ingestigate account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive investigative document corpuses through the user's configured Ingestigate account. <br>
Mitigation: Install only when Ingestigate is trusted with the relevant corpus, confirm upload and retention policies, and rely on organization-scoped permissions. <br>
Risk: Expired or mishandled access tokens can interrupt use or expose account access. <br>
Mitigation: Configure INGESTIGATE_TOKEN and INGESTIGATE_BASE_URL only through secure skill settings, avoid pasting secrets into chat, and regenerate the short-lived token when it expires. <br>
Risk: Advanced workflow guidance fetched from the provider may affect high-impact processing decisions. <br>
Mitigation: Review provider-fetched workflow or script guidance before allowing high-impact document processing. <br>


## Reference(s): <br>
- [Ingestigate](https://ingestigate.com) <br>
- [Agent Developer Guide](https://app1.ingestigate.com/api/agent/guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text with API-backed investigative findings and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should cite evidence returned by the Ingestigate API and note when corpus processing is incomplete.] <br>

## Skill Version(s): <br>
1.0.9 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
