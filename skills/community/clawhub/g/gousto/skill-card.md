## Description: <br>
Search and browse 9,000+ Gousto recipes. Get full ingredients and step-by-step cooking instructions via official API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhruvkelawala](https://clawhub.ai/user/dhruvkelawala) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to search Gousto recipes, refresh a local recipe cache, and retrieve ingredients and step-by-step cooking instructions for a selected recipe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Gousto's public API when refreshing the cache or fetching a recipe. <br>
Mitigation: Run it only in environments where outbound access to the Gousto API is acceptable and review network policy before deployment. <br>
Risk: The skill stores a local recipe cache in data/recipes.json. <br>
Mitigation: Treat the cache as local operational data and refresh or delete it according to the deployment's data handling policy. <br>
Risk: One note in the artifact mentions a vfjr.dev proxy even though the included scripts use the official Gousto API. <br>
Mitigation: Clarify or remove the stale proxy note before publication so users understand the actual network behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dhruvkelawala/gousto) <br>
- [Gousto recipe listing API](https://production-api.gousto.co.uk/cmsreadbroker/v1/recipes) <br>
- [Gousto single recipe API](https://production-api.gousto.co.uk/cmsreadbroker/v1/recipe/{slug}) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text search results and JSON recipe details from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; update-cache.sh stores a local recipe cache under data/recipes.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
