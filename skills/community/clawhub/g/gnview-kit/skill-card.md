## Description:

Gnview Kit helps agents analyze Douyin video data, user profiles, and trends, then sync structured results and document links to Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnview](https://clawhub.ai/user/gnview)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect and normalize Douyin video metadata, coordinate related analysis/download skills, and write results into Feishu Bitable with associated cloud document links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write records and document links to a configured Feishu Bitable.

Mitigation: Verify the Feishu base and table configuration points to the intended workspace before use.

Risk: The workflow may rely on API credentials and related downloader or extraction services.

Mitigation: Keep API keys in environment variables and confirm related skill configuration before processing data.

Risk: The workflow may download video files during analysis.

Mitigation: Use an approved download location and review storage expectations before running batch jobs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration values and structured field specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write records and document links to a configured Feishu Bitable and may coordinate video downloads through related skills.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
