## Description: <br>
Automates uploading a Chinese-language title and long-form article to moccard.com, selecting a card style, generating cards, and downloading the resulting image ZIP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moccard](https://clawhub.ai/user/moccard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and operators can use this skill to turn long Chinese articles into styled card images through MocCard automation and retrieve the generated ZIP archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup download path can forward browser cookies to a configurable server. <br>
Mitigation: Review or remove the backup endpoint before use, restrict it to a trusted fixed server, and avoid forwarding browser cookies. <br>
Risk: The automation may delete matching ZIP files from the user's Downloads folder while trying to monitor downloads. <br>
Mitigation: Run it in an isolated download directory or add an explicit confirmation step before deleting files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moccard/moccard-zh) <br>
- [MocCard website](https://www.moccard.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Terminal output with a ZIP download URL environment-style line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns MEMOLE_DOWNLOAD_URL when the image ZIP is downloaded successfully.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
