## Description:

JF camera recording playback skill for retrieving cloud and local recording lists, playback URLs, and download links for JF devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query JF device cloud or local recording history and obtain playback or download URLs for historical video review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can send camera identifiers, authentication material, recording metadata, and playback URL requests to the host named by JF_ENDPOINT.

Mitigation: Keep JF_ENDPOINT unset or set it only to an official JF host, and do not run the skill where another user or process can control environment variables.

Risk: Printed playback and download URLs can grant temporary access to camera recordings.

Mitigation: Treat playback and download URLs as temporary secrets and avoid sharing logs or terminal output that contains them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jftech-open-pro-video-record)
- [JF Open Platform](https://open.jftech.com/)
- [JF API documentation](https://docs.jftech.com/)
- [Cloud video list API documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=66142b2ca13c418d84085772a627d650)
- [Cloud playback URL API documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672)
- [Local recording API documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=4b1516da5763439a9bc7175d7ac7d246)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text and optional JSON from Python command-line scripts, including recording lists, status summaries, and playback or download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive camera recording metadata and temporary playback or download URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
