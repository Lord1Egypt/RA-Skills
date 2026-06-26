## Description: <br>
NVEIL is an AI-powered data-processing and visualization toolkit for agents that plans joins, aggregations, pivots, resampling, geocoding, time-series analysis, feature engineering, 2D/3D charts, geospatial maps, volume rendering, and medical imaging remotely while executing work locally on the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pierrejacquet](https://clawhub.ai/user/pierrejacquet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agent users use this skill to transform, summarize, and visualize structured, geospatial, image, and volume data without hand-writing pandas, NumPy, Plotly, Matplotlib, VTK, or DeckGL code. The skill guides an agent to inspect data, invoke the NVEIL CLI or Python API, and return generated visualizations, reusable specs, or explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, column names, data types, and summary statistics may be sent to NVEIL's remote planning service. <br>
Mitigation: Use the skill only for datasets where sharing metadata is acceptable, and avoid auto-invocation for sensitive analysis unless the user explicitly agrees. <br>
Risk: The skill requires the sensitive credential NVEIL_API_KEY. <br>
Mitigation: Store the key in the environment or pass it at invocation time; do not commit or paste the key into shared files, logs, or prompts. <br>
Risk: Broad agent auto-invocation could route ordinary data-analysis requests through NVEIL unexpectedly. <br>
Mitigation: Use manual invocation or uninstall the skill when users do not want analysis metadata sent to the NVEIL planning service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pierrejacquet/nveil) <br>
- [NVEIL homepage](https://nveil.com) <br>
- [NVEIL documentation](https://docs.nveil.com) <br>
- [NVEIL API reference](https://docs.nveil.com/api-reference/) <br>
- [NVEIL PyPI package](https://pypi.org/project/nveil/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown instructions with CLI commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to produce HTML, PNG, and .nveil spec files through the NVEIL toolchain.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
