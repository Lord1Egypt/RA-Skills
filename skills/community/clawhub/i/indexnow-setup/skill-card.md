## Description: <br>
Set up IndexNow for any website to enable real-time URL submission to Bing, Yandex, Seznam, and other search engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuyangtusenpo](https://clawhub.ai/user/tuyangtusenpo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to configure IndexNow for websites, publish an IndexNow key file, add a Node.js URL submission script, and integrate submissions into deploy or content-update workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submission script can send sitemap URLs for the configured SITE_URL to the IndexNow endpoint. <br>
Mitigation: Run it only for websites you control and confirm SITE_URL points to the intended production host. <br>
Risk: IndexNow requires a public key file, so an incorrectly placed or unexpected key file can cause setup failures or confusion. <br>
Mitigation: Verify the key file is intentionally public at the documented URL and contains only the IndexNow key. <br>
Risk: A sitemap may include staging, admin, private, or otherwise unintended URLs. <br>
Mitigation: Review the sitemap before submission and remove URLs that should not be sent to search engines. <br>


## Reference(s): <br>
- [IndexNow API endpoint](https://api.indexnow.org/IndexNow) <br>
- [Bing Webmaster Tools](https://www.bing.com/webmasters) <br>
- [ClawHub skill page](https://clawhub.ai/tuyangtusenpo/indexnow-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline JSON, bash commands, and a JavaScript submission script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for generating an IndexNow key, publishing the key file, reading sitemap URLs, and submitting them to the IndexNow endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
