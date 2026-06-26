## Description: <br>
Filter and match postdoctoral fellowship opportunities based on applicant nationality, years since PhD, and research field from a curated database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External postdoctoral applicants, advisors, and research administrators use this skill to screen fellowship options against nationality, years since PhD, and research area. It helps compare likely matches, deadlines, requirements, and caveats before checking official program sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fellowship deadlines, eligibility rules, and requirements may be stale or incomplete. <br>
Mitigation: Treat matches as preliminary and verify deadlines, nationality rules, years-since-PhD limits, and requirements on the official fellowship sites before relying on the output. <br>
Risk: Research-field filtering is limited and may not fully determine field fit. <br>
Mitigation: Manually confirm field fit against each fellowship's official scope and use the output as a shortlist rather than an eligibility determination. <br>


## Reference(s): <br>
- [Fellowship Database Reference](references/fellowships.md) <br>
- [NIH F32 Funding Opportunity](https://grants.nih.gov/grants/guide/pa-files/PA-23-271.html) <br>
- [NSF Postdoctoral Research Fellowships in Biology](https://www.nsf.gov/funding/pgm_summ.jsp?pims_id=503622) <br>
- [HFSP Postdoctoral Fellowships](https://www.hfsp.org/funding/hfsp-funding/postdoctoral-fellowships) <br>
- [EMBO Postdoctoral Fellowships](https://www.embo.org/funding/fellowships-awards-and-grants/postdoctoral-fellowships/) <br>
- [MSCA Postdoctoral Fellowships](https://marie-sklodowska-curie-actions.ec.europa.eu/actions/postdoctoral-fellowships) <br>
- [Schmidt Science Fellows](https://schmidtsciencefellows.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance or terminal text with matched fellowship names, deadlines, requirements, caveats, and next checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a built-in fellowship database and does not access live fellowship databases or real-time deadline updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
