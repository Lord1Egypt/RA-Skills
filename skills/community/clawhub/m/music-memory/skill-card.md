## Description:

Music Memory helps agents store and recall music practice recordings, chord progressions, technique work, and lesson notes with BlueColumn-backed musical context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External music learners, coaches, and agent users can use this skill to log practice recordings, lesson notes, musical context, and quick observations, then recall progress and recurring technique issues. It is suited to practice journaling, student coaching, and session planning workflows that rely on remembered musical details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Practice recordings, transcripts, lesson notes, and coaching observations may be stored by an external BlueColumn cloud service.

Mitigation: Use the skill only when users understand the service's retention and deletion options, and avoid student names or sensitive personal details unless consent is in place.

Risk: The skill relies on a BlueColumn API key for authenticated requests.

Mitigation: Store the API key as a secret, avoid placing it in shared prompts or logs, and rotate it if exposure is suspected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends practice content to BlueColumn's cloud service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
