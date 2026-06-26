## Description: <br>
A Jupyter Notebook creation and editing skill for creating, appending, modifying, merging, exporting, indexing, tagging, and reordering .ipynb content with optional local image embedding and hash-based quiz cells. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIgamatrix](https://clawhub.ai/user/AIgamatrix) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, educators, and technical content authors use this skill to create or maintain Jupyter notebooks in smaller verified steps, including teaching notebooks, programming exercises, tutorials, and study notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper writes and modifies local notebook or script files, so an incorrect path or overwrite could affect important work. <br>
Mitigation: Confirm target paths before execution and keep backups of existing notebooks before using modification, merge, or export flows. <br>
Risk: Embedding local images copies their contents into the notebook as base64 data, increasing file size and potentially carrying sensitive local image content. <br>
Mitigation: Review image paths and contents before embedding, and compress or omit large or sensitive images. <br>
Risk: Hash-based quiz answers are suitable for teaching workflows but are not a high-security assessment mechanism. <br>
Mitigation: Use the quiz feature for low-stakes educational exercises and use a separate controlled assessment system for secure exams. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIgamatrix/notebook-builder) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [LICENSE.txt](artifact/LICENSE.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and local file outputs such as .ipynb and .py files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python helper functions to write notebook JSON, embed local images as base64 data, generate hash-based quiz cells, merge notebooks, and export code cells to scripts.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
