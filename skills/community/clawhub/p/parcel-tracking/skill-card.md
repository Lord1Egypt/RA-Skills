## Description: <br>
Automatically detects parcel carriers through the Track123 API and returns parcel tracking status, with optional postal-code support for more detailed lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dany9328](https://clawhub.ai/user/dany9328) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and support agents use this skill to check parcel status from a tracking number, optionally adding a postal code for a more specific Track123 lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends tracking numbers and optional postal codes to Track123. <br>
Mitigation: Install and use it only when users are comfortable sharing those parcel details with Track123, and provide the TRACK123_API_SECRET through environment configuration. <br>
Risk: The artifact includes a bundled Python virtual environment that is not necessary for understanding or running the skill logic. <br>
Mitigation: Prefer installing dependencies from requirements.txt in a fresh environment and review the artifact before deployment. <br>


## Reference(s): <br>
- [Parcel Tracking on ClawHub](https://clawhub.ai/dany9328/parcel-tracking) <br>
- [Track123 API endpoint](https://api.track123.com/gateway/open-api/tk/v2) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown] <br>
**Output Format:** [JSON containing status fields and a Markdown tracking summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRACK123_API_SECRET and sends the tracking number, plus optional postal code, to Track123.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
