## Description: <br>
List and snapshot retrieval for webcams, especially foto-webcam.eu, including current snapshot JPG retrieval from a favorites list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixweb](https://clawhub.ai/user/unixweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to list saved webcams, fetch current public webcam snapshots by ID or URL, and send selected images through a configured OpenClaw or Telegram channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public webcam image URLs and can send retrieved images through a configured Telegram channel. <br>
Mitigation: Review the favorites list before use, avoid private or internal URLs, and confirm the Telegram target is the intended chat. <br>
Risk: Adding or changing favorites can redirect snapshot retrieval to an unintended image source. <br>
Mitigation: Keep favorites limited to approved public webcam pages or direct JPG URLs and review changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unixweb/photo-webcam) <br>
- [foto-webcam.eu webcam source](https://www.foto-webcam.eu/webcam/zugspitze/) <br>
- [Favorites list](docs/webcams/favorites-muenchen.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, JSON, Shell commands, API calls] <br>
**Output Format:** [Plain text captions and lists, JPG snapshot files, JSON script status, and OpenClaw message-send commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits multi-webcam requests to six images and sends each image separately.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
