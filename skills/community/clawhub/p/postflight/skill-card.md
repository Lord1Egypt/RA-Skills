## Description:

Drafts X (Twitter) posts on a weighted pillar schedule, sends each draft to the authorized user for approval, and publishes only the ones they ship.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soos3d](https://clawhub.ai/user/soos3d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use Postflight to maintain an X posting workflow: drafting scheduled posts, preparing reply options, filing photos into a local library, and publishing only after authorized approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public X posts from approved pending drafts.

Mitigation: Require explicit approval from the configured authorized user before any publish action and keep X credentials or browser sessions under the user's control.

Risk: The release evidence flags local file-handling review needs around temporary files and photo ingestion.

Mitigation: Review the temp-file and photo-library path rules before use, and ingest photos only through the provided workflow that validates paths and strips location metadata.

Risk: The skill reads and writes local postflight-state data used for drafts, metrics, photos, and posting history.

Mitigation: Run it in the intended workspace, review state contents before deployment, and avoid storing credentials or tokens in state files.

## Reference(s):

- [ClawHub release: postflight](https://clawhub.ai/soos3d/skills/postflight)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text messages with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft and approval messages, reply options, local state updates, and publish commands gated by explicit authorized approval.]

## Skill Version(s):

1.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
