## Description: <br>
Analyzes company websites to find content marketing gaps, qualify prospects, compare competitor content, score lead quality, and produce a personalized outreach angle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinoneliraz](https://clawhub.ai/user/yinoneliraz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales, marketing, and service-business operators use this skill to qualify a company from its domain before outreach by auditing website content, competitor visibility, fit, and budget signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-based prospect research can produce incomplete or outdated observations that affect lead scoring and outreach recommendations. <br>
Mitigation: Review the generated report, cited observations, score, and outreach angle before using them for sales decisions or contacting a prospect. <br>
Risk: PROSPECT_CONFIG.md may contain confidential pricing, strategy, target-customer, or service-positioning details that are used in generated analysis. <br>
Mitigation: Keep sensitive business information out of PROSPECT_CONFIG.md unless it is acceptable for the agent to use it in local lead-analysis files. <br>
Risk: Queue mode writes analysis files and can modify prospects/queue.md as prospects move through workflow states. <br>
Mitigation: Review workspace file changes before committing, sharing, or feeding the queue into downstream outreach workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yinoneliraz/prospect-analyzer) <br>
- [DriftMango SDR Kit](https://driftmango.com/sdr-kit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prospect reports with a short text summary and optional Markdown queue updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes prospects/[company-name]-analysis.md and may update prospects/queue.md when queue processing is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
