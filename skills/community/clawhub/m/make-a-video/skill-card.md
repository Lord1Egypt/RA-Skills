## Description:

Make a complete video from a simple idea with Pexo; the hosted service handles scripting, shot selection, model selection, music, subtitles, final editing, and returns a publish-ready video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to ask an agent for a new video in plain language, optionally with uploaded media assets, and receive project updates and a final video URL from Pexo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected media, project metadata, generated assets, and account-credit checks may be sent to Pexo and may consume credits.

Mitigation: Send only content intended for Pexo processing, confirm credit expectations before starting production, and review project links and final asset URLs before sharing.

Risk: Changing PEXO_BASE_URL can redirect uploads, prompts, and authenticated requests to another endpoint.

Mitigation: Keep PEXO_BASE_URL fixed to https://pexo.ai unless the user intentionally trusts a different endpoint.

Risk: The local Pexo config contains API credentials and is sourced by the shell scripts.

Mitigation: Store ~/.pexo/config with restrictive permissions such as 600 and include only the expected PEXO_BASE_URL and PEXO_API_KEY values.

Risk: Server-resolved GitHub import provenance is unavailable for this release.

Mitigation: Prefer a pinned installer or reviewed release source before deployment.

## Reference(s):

- [Pexo](https://pexo.ai)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text guidance with shell commands, JSON script responses, project links, and final asset URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; prompts, uploads, project metadata, generated assets, and credit checks may be sent to Pexo.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
