## Description: <br>
Controls and prints text, barcodes, and QR codes on the Gprinter GP-C200V ESC/POS thermal printer via Node.js or command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yardfarmer](https://clawhub.ai/user/yardfarmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to build ESC/POS print commands and run Node.js or CLI printing workflows for GP-C200V or compatible receipt printers, including Chinese text, QR codes, and barcodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Print jobs may be sent to the wrong network device if the printer host or port is misconfigured. <br>
Mitigation: Verify the configured printer IP and port before running the CLI or reusable Node.js helper. <br>
Risk: The optional localhost HTTP bridge can expose printing behavior if it is run in an environment the user does not trust. <br>
Mitigation: Use direct TCP printing by default and run the bridge only when browser-based printing is intentionally required. <br>
Risk: The --file option prints the contents of the provided path. <br>
Mitigation: Avoid passing sensitive files and review file contents before printing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yardfarmer/gprinter) <br>
- [ESC/POS Protocol Reference](esc-pos-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ESC/POS byte arrays, printer host and port settings, and file paths supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
