## Description: <br>
Generates a static legal and support site for app store compliance and Cloudflare Pages deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chentuan7963-afk](https://clawhub.ai/user/chentuan7963-afk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and app publishers use this skill to generate a static site containing privacy, terms, support, and data deletion pages for app distribution workflows. The generated content should be reviewed before deployment as legal or compliance material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated legal pages may be incomplete or placeholder-like despite compliance-oriented claims. <br>
Mitigation: Review and revise the generated pages with qualified legal or compliance stakeholders before deployment. <br>
Risk: User-supplied values may be embedded into deployable HTML without sufficient escaping. <br>
Mitigation: Escape or validate all generated HTML content before publishing the site. <br>
Risk: The skill writes to ./dist/index.html and may overwrite existing generated content. <br>
Mitigation: Run it in a clean workspace or back up the dist directory before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chentuan7963-afk/legal-site-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/chentuan7963-afk) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Configuration] <br>
**Output Format:** [Static HTML files in a dist directory plus status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires appName, companyName, and contactEmail inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
