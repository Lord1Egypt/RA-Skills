## Description: <br>
Atomic node skill to search google contacts. Loops internally until successful. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents or developers use this skill to search Google Contacts from JSON input through a configured Composio and gog connection, returning contact search results for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a Composio API key and an external gog tool to access Google Contacts data. <br>
Mitigation: Confirm that the gog binary and connected Composio account are trusted, grant only the Google Contacts access needed for search, and keep COMPOSIO_API_KEY secret. <br>
Risk: The skill loops internally until successful, which can continue longer than expected when failures persist. <br>
Mitigation: Monitor execution and stop the workflow if retries continue after failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-contacts-search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls] <br>
**Output Format:** [JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JSON input object and returns the contact search result array.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
