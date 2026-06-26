## Description: <br>
Kaggle API integration with managed authentication for accessing datasets, models, competitions, and kernels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to search, download, and interact with Kaggle resources through Maton-managed authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Maton brokering Kaggle requests and handling authentication. <br>
Mitigation: Install only if you trust Maton for this workflow and connect only the Kaggle account intended for agent use. <br>
Risk: MATON_API_KEY grants access to Maton-managed Kaggle operations. <br>
Mitigation: Store MATON_API_KEY securely, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>
Risk: Deleting a connection can remove access needed by later Kaggle operations. <br>
Mitigation: Verify the connection id before using delete examples or automating connection cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/kaggle-api) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton](https://maton.ai) <br>
- [Kaggle API documentation](https://www.kaggle.com/docs/api) <br>
- [Kaggle datasets](https://www.kaggle.com/datasets) <br>
- [Kaggle models](https://www.kaggle.com/models) <br>
- [Kaggle competitions](https://www.kaggle.com/competitions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for live Kaggle operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
