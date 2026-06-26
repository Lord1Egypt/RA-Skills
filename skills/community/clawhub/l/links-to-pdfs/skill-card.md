## Description: <br>
Scrape documents from Notion, DocSend, direct PDFs, and other web sources into local PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisling-dev](https://clawhub.ai/user/chrisling-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to download, archive, or convert authorized web documents into local PDF files, including protected documents that require an authentication workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install an unreviewed global browser-automation package that may handle credentials and saved sessions. <br>
Mitigation: Review the package before installing, pin the package version where possible, and clear saved profiles or stop the daemon after use. <br>
Risk: Fallback scraping can send page HTML to a third-party LLM for analysis. <br>
Mitigation: Avoid confidential or sensitive pages unless that analysis is approved for the data involved. <br>
Risk: Automatic handling of protected document flows, including agreement checkboxes, may create authorization or compliance concerns. <br>
Mitigation: Use the skill only for documents you are authorized to access and do not automate agreement or NDA steps without explicit authorization. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local PDF file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return blocked job IDs and required credential field names when authentication is needed.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
