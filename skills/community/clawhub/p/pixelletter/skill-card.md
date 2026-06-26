## Description: <br>
Send letters, PDFs, postcards, faxes, registered mail, or query account credit through the PixelLetter HTTPS interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bone187](https://clawhub.ai/user/bone187) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent prepare, test, and submit PixelLetter letter, PDF, fax, registered-mail, and account-credit requests through the PixelLetter HTTPS API. It is most useful for automated correspondence workflows where real dispatch is gated by explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production sends can dispatch real postal mail or faxes and incur PixelLetter charges. <br>
Mitigation: Default to dry-run or test mode and require explicit confirmation of the recipient, document or text, options, and dispatch intent before using production mode. <br>
Risk: PixelLetter account credentials could be exposed through logs, commits, screenshots, or shared examples. <br>
Mitigation: Use environment variables or secret injection, avoid storing credentials in skill files, and do not include credentials in logs or shared artifacts. <br>
Risk: A PixelLetter success code means the request was accepted by the API, not that physical delivery is complete. <br>
Mitigation: Treat code 100 as acceptance only and rely on PixelLetter's later email confirmation for final send status. <br>


## Reference(s): <br>
- [PixelLetter HTTPS API Notes](references/api.md) <br>
- [PixelLetter](https://www.pixelletter.de) <br>
- [PixelLetter XML Endpoint](https://www.pixelletter.de/xml/index.php) <br>
- [PixelLetter Error Messages](https://www.pixelletter.de/docs/error_messages.php) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled CLI returns sanitized XML for dry-runs and JSON summaries for API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Real dispatch requires PixelLetter credentials, account credit, production mode, explicit confirmation, and PIXELLETTER_ALLOW_REAL_SEND=true.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
