## Description:

Analyzes static construction-site images for safety hazards and calls data collection or cross-verification endpoints only when the user explicitly asks for those workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqu108](https://clawhub.ai/user/chenqu108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to route construction-site image URLs to a configured hazard-analysis service and receive concise safety findings, structured results, or cross-verification when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends construction-site image URLs and related identifiers to a configured external HTTP service.

Mitigation: Use only a trusted lc_scene_http service, confirm that image URLs are appropriate to share, and keep usage limited to the disclosed construction-site image analysis workflows.

Risk: The skill depends on an auth profile containing API credentials and service configuration.

Mitigation: Store the API key only in the lc_scene_http:default auth profile, do not paste secrets into chat, and do not expose profile contents in outputs.

Risk: Hazard analysis results may be incomplete or uncertain if inputs are missing, the service fails, times out, or returns an unexpected structure.

Mitigation: Report those failures explicitly, avoid fabricating results, and avoid stating uncertain model conclusions as confirmed facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenqu108/skills/lc-scene-analysis-http)
- [Publisher Profile](https://clawhub.ai/user/chenqu108)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or JSON, depending on whether the user requests a concise summary, raw result, structured result, or cross-verification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve key service conclusions, avoid overstating uncertain findings, and report missing inputs, authentication problems, service errors, timeouts, or malformed responses instead of fabricating results.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
