## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and collects public creator posts through Guaikei-powered Node.js command-line tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content creators, and analysts use this skill to gather structured public Xiaohongshu data for topic research, competitor monitoring, creator screening, trend analysis, and comment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guaikei API tokens, Xiaohongshu links, keywords, token-bearing requests, and retrieved records are sent to the Guaikei service.

Mitigation: Use a limited or disposable API token, avoid sensitive inputs, and confirm that sending the requested public-data lookup to Guaikei is acceptable for the user's environment.

Risk: API tokens are sent in URL query strings, which can be exposed through request logs or diagnostic traces.

Mitigation: Avoid sharing command output, process traces, network logs, or service logs that may contain token-bearing URLs; rotate the token if exposure is suspected.

Risk: Retrieved datasets are automatically saved locally as plaintext JSON logs.

Mitigation: Restrict access to the logs directory, avoid storing sensitive retrieved data, and delete saved outputs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search)
- [Guaikei service website](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include request metadata and may be saved as plaintext JSON logs; calls require GUAIKEI_API_TOKEN and support result limits up to 10000 where applicable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
