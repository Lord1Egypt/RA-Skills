## Description: <br>
Create shareable HTML canvases through the gui.new API for visual outputs, live previews, and Mermaid diagrams by posting content and receiving a live URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanfeltus](https://clawhub.ai/user/dylanfeltus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish generated HTML, UI mockups, dashboards, forms, tables, or Mermaid diagrams as shareable gui.new links. It is useful when a user wants a live preview URL for visual or interactive output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML or Mermaid content is uploaded to a third-party hosted service and resulting canvas links may be publicly accessible until they expire. <br>
Mitigation: Do not send secrets, personal data, confidential business content, sensitive form inputs, or other private material to gui.new. <br>
Risk: An optional Pro API key may be used for extended expiry and higher limits. <br>
Mitigation: Protect the API key, avoid exposing it in shared canvases or logs, and use the free tier when elevated limits are not required. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/dylanfeltus/gui-new) <br>
- [gui.new documentation](https://gui.new/docs) <br>
- [gui.new llms.txt](https://gui.new/docs/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with bash commands, HTML or Mermaid examples, and returned gui.new URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include canvas IDs, edit tokens, expiry metadata, and public share links returned by gui.new.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
