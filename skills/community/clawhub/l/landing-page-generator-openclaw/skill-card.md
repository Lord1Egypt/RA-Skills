## Description: <br>
Generate high-converting, mobile-responsive landing pages from a brief for landing pages, sales pages, or marketing pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanwyngaard](https://clawhub.ai/user/seanwyngaard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and marketing teams use this skill to turn a product or service brief into a static landing page and client-facing customization guide. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares Bash access even though normal use should only read a brief and write static landing-page files. <br>
Mitigation: Review any unexpected shell command before allowing it, and expect normal output to be limited to output/landing-page/index.html and output/landing-page/README.md. <br>
Risk: Generated marketing copy, testimonials, forms, and deployment notes may include placeholders or claims that are not ready for publication. <br>
Mitigation: Review the generated HTML and README before deployment, replace placeholder content, verify claims, and connect forms to the intended service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanwyngaard/landing-page-generator-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Self-contained HTML/CSS, Markdown README, and concise Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/landing-page/index.html and output/landing-page/README.md; generated pages avoid external JavaScript and image dependencies except Google Fonts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
