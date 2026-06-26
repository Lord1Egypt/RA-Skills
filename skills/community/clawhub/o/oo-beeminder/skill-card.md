## Description: <br>
Beeminder helps agents read, create, update, and delete Beeminder data through an OOMOL-connected connector instead of calling the Beeminder API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Beeminder from an agent session, including reading users, goals, and datapoints and performing confirmed write or delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Beeminder datapoints, changing user goal data. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write-tagged actions. <br>
Risk: The skill can delete Beeminder datapoints. <br>
Mitigation: Get explicit approval for the target datapoint before running destructive actions. <br>
Risk: The skill requires a connected external account and sensitive credentials managed outside the artifact. <br>
Mitigation: Only grant Beeminder/OOMOL access when it matches the user's requested task and rely on the connector rather than exposing raw tokens. <br>


## Reference(s): <br>
- [ClawHub Beeminder skill page](https://clawhub.ai/oomol/oo-beeminder) <br>
- [Beeminder homepage](https://www.beeminder.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions can return JSON data and execution metadata from the OOMOL connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
