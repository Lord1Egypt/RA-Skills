## Description: <br>
Collects invoices and receipts from Gmail, downloads PDF attachments or screenshots email bodies when PDFs are unavailable, and sends a summary email with attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mintannn](https://clawhub.ai/user/mintannn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People managing billing or bookkeeping use this skill to gather invoice and receipt emails from Gmail for a date range and forward a summary with attachments to a chosen recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Gmail invoice and receipt content and can automatically send a summary email with attachments. <br>
Mitigation: Use only with a Gmail account and destination you explicitly control, and verify the configured queries, date range, recipient, and attachments before each run. <br>
Risk: The screenshot path renders email HTML in Puppeteer with the browser sandbox disabled. <br>
Mitigation: Run the screenshot workflow in an isolated environment or modify it to disable JavaScript and outbound network requests before rendering email HTML. <br>
Risk: The installation examples download gogcli release artifacts from the network. <br>
Mitigation: Prefer checksum-verified installs or package-manager installation before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mintannn/invoice-collector) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [gogcli Linux release archive](https://github.com/steipete/gogcli/releases/latest/download/gogcli_linux_amd64.tar.gz) <br>
- [gogcli checksums](https://github.com/steipete/gogcli/releases/latest/download/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with bash, JSON configuration, and Node.js command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary invoice files or screenshots and send email attachments through Gmail when executed by the user.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
