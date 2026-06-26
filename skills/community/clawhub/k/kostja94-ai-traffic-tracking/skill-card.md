## Description: <br>
Guides agents in helping users track AI-driven search traffic in Google Analytics 4 and Google Search Console. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, analytics, and SEO practitioners use this skill to configure GA4 and GSC views that separate AI referral and AI search traffic from broader organic, referral, or direct traffic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex and channel-group changes could misclassify traffic if applied without checking the site's actual AI referral sources. <br>
Mitigation: Review and adapt the regex against observed GA4 sources before saving reports or channel groups. <br>
Risk: Analytics configuration changes could be made in the wrong GA4 property. <br>
Mitigation: Confirm the intended GA4 property before applying report, channel-group, or library changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown guidance with regex and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or API calls; guidance should be adapted to the user's observed AI referral sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
