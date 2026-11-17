## Description:

Fetches public Xiaohongshu keyword search results, note details, comments, and creator posts as structured data for downstream analysis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content creators, marketing teams, and analysts use this skill to collect public Xiaohongshu search, note, comment, and creator-post data before summarizing trends, competitors, KOL activity, or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and GUAIKEI_API_TOKEN values to guaikei.com.

Mitigation: Use it only where that data sharing is approved, keep the API token out of shared logs and prompts, and rotate the token if it is exposed.

Risk: Collected comments, profile data, research topics, and xsec_token URLs may be saved to plaintext log files.

Mitigation: Run the skill in a private workspace, review log contents before sharing, and delete or protect logs after use.

Risk: The skill depends on a third-party API service and may fail, rate limit, or return unavailable data.

Mitigation: Handle empty or error responses as non-authoritative, retry later for transient service failures, and avoid fabricating results when collection fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-hot-notes)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with command examples; CLI commands return structured JSON and may write plaintext logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and Node.js 16.14.0+; each data collection command can request up to 10000 public items.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
