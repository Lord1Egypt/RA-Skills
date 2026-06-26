## Description: <br>
Deploy local HTML/frontend files to PostMe (dele.fun) and get a live URL <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[del-zhenwu](https://clawhub.ai/user/del-zhenwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish a local HTML file or frontend project folder to PostMe and return a shareable live URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploading a project root can publish .env files, secrets, private assets, or proprietary source that should not be shared. <br>
Mitigation: Deploy only a reviewed public build folder or single HTML file. <br>
Risk: The PostMe API key can be exposed if it is stored in uploaded files or pasted into public content. <br>
Mitigation: Keep POSTME_API_KEY in an environment variable or secret store and exclude secrets from the deployment target. <br>
Risk: Changing the upload endpoint can send files and credentials to an untrusted service. <br>
Mitigation: Use the default PostMe endpoint unless the replacement POSTME_API_URL is specifically trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/del-zhenwu/postme-deploy) <br>
- [Publisher Profile](https://clawhub.ai/user/del-zhenwu) <br>
- [PostMe](https://www.dele.fun) <br>
- [PostMe API Keys](https://www.dele.fun/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and string deployment status with a live URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PostMe API key and the Python requests library.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
