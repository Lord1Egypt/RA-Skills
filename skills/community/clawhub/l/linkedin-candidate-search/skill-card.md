## Description:

Automates LinkedIn candidate search through Chrome DevTools, using Google and LinkedIn search results to collect profiles, avoid duplicate scans, and summarize candidates against role and experience criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sourcers, and hiring teams use this skill to search for LinkedIn candidates by role and location, save profile summaries, and classify matches using hard and soft screening criteria. It is intended for agent-assisted sourcing workflows where the user controls browser access and reviews saved candidate data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to duplicate browser credential or session files and expose them through a persistent Chrome debugging session.

Mitigation: Use a dedicated browser profile, log in manually only for the intended account, restrict DevTools access, close the debugging browser when finished, and delete temporary profile and saved candidate data that is no longer needed.

Risk: The skill stores candidate profile data locally after visiting LinkedIn profiles.

Mitigation: Store only data needed for the sourcing workflow, review saved files before sharing, and remove candidate data that is no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianjunye/skills/linkedin-candidate-search)
- [Publisher profile](https://clawhub.ai/user/qianjunye)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown summaries, candidate profile files, browser automation scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves candidate profiles under linkedin-save role directories and reports A/B/C match levels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
