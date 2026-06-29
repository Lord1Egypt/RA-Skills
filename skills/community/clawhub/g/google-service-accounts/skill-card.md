## Description: <br>
Read or write a user's Google Sheets, Docs, Drive, or Calendar from code via a Google service account - headless, no OAuth browser flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amiller](https://clawhub.ai/user/amiller) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to set up and use Google service accounts for headless access to explicitly shared Google Sheets, Docs, Drive files, and calendars. It is useful when an agent is handed service-account credentials or needs to guide a user through creating and sharing access for one. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runnable examples can modify Google files or calendars that have been shared with the service account. <br>
Mitigation: Use a dedicated test file first, grant Viewer or read-only access unless writes are required, and check the target document or calendar before running write examples. <br>
Risk: A credentials.json file or CREDS_JSON value gives the holder the service account's access to shared resources. <br>
Mitigation: Keep service-account credentials private, never commit or paste them into shared locations, and rotate or revoke exposed keys. <br>
Risk: Broad scopes or broad sharing can expose more Google data than the task needs. <br>
Mitigation: Request the least Google API scope needed, prefer .readonly scopes for read tasks, and share only the specific files or calendars required. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Runnable quickstart examples](quickstart.py) <br>
- [Google Cloud CLI installation](https://cloud.google.com/sdk/docs/install) <br>
- [ClawHub skill page](https://clawhub.ai/amiller/google-service-accounts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference credentials.json or CREDS_JSON supplied by the user; does not generate credentials itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
