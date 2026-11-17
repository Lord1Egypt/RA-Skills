## Description:

Retrieves public Xiaohongshu note comments, commenter information, and interaction data, with related commands for keyword search, note detail retrieval, and creator post monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, marketers, content teams, and data analysts use this skill to collect public Xiaohongshu comments and related public content signals for audience feedback analysis, trend research, competitor monitoring, and KOL screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public description emphasizes comment collection, but the artifact also supports keyword search, note detail retrieval, and creator post collection.

Mitigation: Review the selected command before execution and limit use to the specific Xiaohongshu public-data task the user requested.

Risk: Keywords, Xiaohongshu links, and the Guaikei API token are sent to guaikei.com.

Mitigation: Use a low-privilege, rotatable token and avoid sensitive links or keywords unless this third-party data flow is acceptable.

Risk: Returned results may be saved locally in the artifact's logs directory.

Mitigation: Apply local retention controls, review log contents before sharing, and delete logs that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comment-data)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, json]

**Output Format:** [JSON command results with concise text guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0 or newer and a GUAIKEI_API_TOKEN; successful runs may write returned data to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
