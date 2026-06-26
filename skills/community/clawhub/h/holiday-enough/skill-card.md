## Description: <br>
Evaluates whether a user's available holiday days are enough for a destination by gathering timing estimates from travel guides and returning a concise adequacy assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrlyk](https://clawhub.ai/user/mrlyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning agents use this skill when a user provides a destination and available days. It estimates whether the trip timing is generous, adequate, or tight, then suggests focused adjustments based on commonly reported attraction and transit times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad control of a user's live Chrome browser, which is more access than the travel-planning task normally requires. <br>
Mitigation: Install only after review, use a separate Chrome profile with no sensitive accounts or tabs, avoid private sessions and local files, and stop the proxy after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrlyk/holiday-enough) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands] <br>
**Output Format:** [Markdown with concise recommendation sections and supporting command snippets for browser-based retrieval.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 22+ and Chrome remote debugging; may use a local CDP proxy to collect page content from the user's browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
