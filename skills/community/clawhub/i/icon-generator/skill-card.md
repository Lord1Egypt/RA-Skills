## Description: <br>
Icon Generator helps agents create app icons, favicons, logos, and brand marks for iOS, Android, and web outputs in multiple sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and external users can use this skill to generate local icon and logo assets for apps, websites, favicons, and brand marks across common platform sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Pillow from pip without a pinned version, which can reduce supply-chain reproducibility. <br>
Mitigation: Use an isolated virtual environment and pin Pillow to a reviewed version when reproducible builds matter. <br>
Risk: Generated icons become user-facing app, website, or brand assets. <br>
Mitigation: Review generated icons for brand fit, legibility, and platform requirements before publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobewin/icon-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/tobewin) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python code and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports multi-size icons for iOS, Android, and web when run locally with Pillow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
