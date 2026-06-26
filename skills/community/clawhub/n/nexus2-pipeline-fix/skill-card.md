## Description: <br>
Fixes JSON serialization of pandas Timestamps and ensures fresh fixture ingestion for accurate Nexus2 sports predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tktk-ai](https://clawhub.ai/user/tktk-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining Nexus2 sports prediction pipelines use this skill to apply and verify fixes for pandas Timestamp serialization failures and stale fixture ingestion that can cause phantom predictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying patched pipeline files directly to a production Nexus2 installation could introduce incompatible behavior or replace local changes. <br>
Mitigation: Obtain the patched files from a trusted source, review the diff against the installed Nexus2 version, back up the originals, and test the prediction pipeline in staging before production use. <br>
Risk: Prediction output may still be misleading if fixture data or bookmaker sources are stale, malformed, or unavailable. <br>
Mitigation: Verify prediction output against live SportyBet or SofaScore fixtures after applying the fix. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tktk-ai/nexus2-pipeline-fix) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline file paths and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No bundled code or automatic execution; users must obtain and review the referenced patched files before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
