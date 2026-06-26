## Description: <br>
傳送定位點或 Google Maps 網址，查詢附近台灣停車場即時空位，附 Apple Maps / Google Maps 一鍵導航連結。支援 Telegram、LINE、iMessage。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harperbot](https://clawhub.ai/user/Harperbot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to send a location or Google Maps URL and receive nearby Taiwan parking options with current availability, distance, address, and navigation links. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: The bundled updater can replace installed skill code from an unpinned GitHub branch. <br>
Mitigation: Remove or avoid running update.sh unless the repository is trusted and the updated code has been reviewed. <br>
Risk: Location coordinates or map URLs may be sent to external services while resolving locations and navigation links. <br>
Mitigation: Use raw coordinates when possible, avoid untrusted short links, and only share locations appropriate for the intended channel. <br>
Risk: TDX credentials are required for API access. <br>
Mitigation: Use dedicated TDX credentials and rotate them if the skill environment or logs may have exposed secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Harperbot/openclaw-parking-query) <br>
- [TDX transport data platform](https://tdx.transportdata.tw) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with parking availability, addresses, distances, and map navigation URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to five nearby parking results; realtime mode includes current availability and future mode omits realtime occupancy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script version comment) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
