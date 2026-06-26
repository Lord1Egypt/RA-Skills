## Description: <br>
Browse MongoDB Atlas Admin API specifications and execute operations when Atlas credentials are provided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finishy1995](https://clawhub.ai/user/finishy1995) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect MongoDB Atlas Admin API categories, endpoint definitions, and schemas, and to run Atlas API calls when service account credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate the MongoDB Atlas Admin API when service account credentials are present. <br>
Mitigation: Use a least-privilege Atlas service account and install only where Atlas administration through an agent is intended. <br>
Risk: POST, PUT, PATCH, and DELETE requests can change or delete Atlas resources. <br>
Mitigation: Require dry-run previews for state-changing calls and approve --yes only after checking the exact method, endpoint, and JSON body. <br>
Risk: A custom ATLAS_API_BASE_URL changes the endpoint receiving credentials and API requests. <br>
Mitigation: Leave ATLAS_API_BASE_URL unset unless the endpoint is trusted. <br>


## Reference(s): <br>
- [MongoDB Atlas Admin API documentation](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/) <br>
- [ClawHub skill page](https://clawhub.ai/finishy1995/mongodb-atlas-admin) <br>
- [Publisher profile](https://clawhub.ai/user/finishy1995) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown or JSON returned through command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live MongoDB Atlas API requests when ATLAS_CLIENT_ID and ATLAS_CLIENT_SECRET are set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
