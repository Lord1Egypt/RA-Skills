## Description: <br>
當使用者貼上 Instagram 連結時，自動下載該貼文的所有高解析度圖片與影片。使用 Cobalt API 進行解析，支援多圖貼文，若為私人帳號會自動回報。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenleung1205](https://clawhub.ai/user/kenleung1205) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users provide an Instagram post URL so an agent can retrieve high-resolution images or videos, including carousel media, through the Cobalt API. The skill is intended for public or non-sensitive links and should not be used with Instagram credentials or cookies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Instagram URLs are shared with the third-party Cobalt API. <br>
Mitigation: Use the skill only for public or non-sensitive links and avoid providing Instagram credentials, cookies, or private-account content. <br>
Risk: Unusual user-provided URLs could be unsafe if inserted directly into a shell command. <br>
Mitigation: Validate that input is an Instagram URL and construct the curl request safely instead of blindly shell-interpolating raw user input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenleung1205/instagram-saver) <br>
- [Cobalt API endpoint](https://api.cobalt.tools/api/json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a curl request pattern and user-facing guidance for downloading media links returned by Cobalt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
