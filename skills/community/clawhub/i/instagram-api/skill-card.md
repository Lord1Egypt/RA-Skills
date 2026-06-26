## Description: <br>
Post to Instagram Feed, Story, Reels, Carousel, and Threads using the official Meta Graph API, with Imgur used for media hosting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifeissea](https://clawhub.ai/user/lifeissea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and social publishing operators use this skill to publish approved local media and captions to Instagram and Threads through shell scripts backed by Meta APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Threads posting script runs undeclared local code before publishing to a social account. <br>
Mitigation: Avoid the Threads script until the hardcoded local clean_md.py dependency is removed, bundled, or replaced with reviewed code. <br>
Risk: Local media uploaded through the Instagram scripts is also sent to Imgur as a public URL. <br>
Mitigation: Use only final approved media and captions, and do not upload sensitive or private media through these scripts. <br>
Risk: Posting tokens can publish content to connected Instagram or Threads accounts. <br>
Mitigation: Use least-privileged posting tokens and review all media and captions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lifeissea/instagram-api) <br>
- [Meta for Developers](https://developers.facebook.com/) <br>
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>
- [Imgur client registration](https://api.imgur.com/oauth2/addclient) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Text] <br>
**Output Format:** [Shell commands with text logs and returned media or post identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Meta, Threads, and Imgur environment variables; uploads local media to Imgur to obtain public media URLs for publishing.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
