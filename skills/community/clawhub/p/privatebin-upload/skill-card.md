## Description: <br>
Upload content to a PrivateBin instance and return a shareable link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KafCoppelia](https://clawhub.ai/user/KafCoppelia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, employees, and external users use this skill to upload identified text, code, reports, or files to a configured PrivateBin instance and receive a shareable paste URL with optional expiry, password protection, or burn-after-reading settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded content is shared through an external PrivateBin instance. <br>
Mitigation: Confirm the exact destination host and the exact content or file before upload. <br>
Risk: Sensitive, regulated, proprietary, or private material may be exposed if uploaded unintentionally. <br>
Mitigation: Avoid uploading such material unless sharing is intentional; use short expiry, password protection, or burn-after-reading for sensitive-but-shareable content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/KafCoppelia/privatebin-upload) <br>
- [PrivateBin](https://privatebin.info/) <br>
- [privatebin CLI](https://github.com/gearnode/privatebin) <br>
- [privatebin CLI releases](https://github.com/gearnode/privatebin/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with paste URL, expiry details, optional password information, and inline shell commands when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PrivateBin CLI JSON response fields such as paste_url, expire, and password when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
