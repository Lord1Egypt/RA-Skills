## Description: <br>
Print text, images, and QR codes to a wireless Bluetooth thermal printer from a MacOS device. Use `inkjet print` for output, `inkjet scan` to discover printers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronchartier](https://clawhub.ai/user/aaronchartier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to print receipts, labels, worksheets, images, QR codes, and logs through the InkJet CLI on macOS with Bluetooth thermal printers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the external InkJet CLI introduces dependency trust risk. <br>
Mitigation: Verify that the `inkjet` pip package or Homebrew tap is trusted before installation. <br>
Risk: Printed text, files, images, QR codes, and streamed content may expose private information physically. <br>
Mitigation: Print only content that is acceptable to disclose on paper and review QR code payloads before printing. <br>
Risk: Saved printer configuration can route output to the wrong printer or use unintended formatting. <br>
Mitigation: Review local and global InkJet configuration files before printing in shared or multi-printer environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaronchartier/inkjet) <br>
- [Publisher profile](https://clawhub.ai/user/aaronchartier) <br>
- [InkJet homepage](https://github.com/AaronChartier/inkjet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for an installed `inkjet` CLI connected to Bluetooth thermal printer hardware.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
