## Description: <br>
Use when developer needs to install, use, or look up components from @pointcloud/pcloud-components npm package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank17008](https://clawhub.ai/user/frank17008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install @pointcloud/pcloud-components, choose suitable React business components, and generate usage guidance or example code for Ant Design-based applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unintended or unpinned third-party package can introduce dependency risk. <br>
Mitigation: Confirm the @pointcloud/pcloud-components package identity before installation and pin dependency versions with a lockfile. <br>
Risk: Production CDN or iconfont script URLs can load code or assets outside the application's reviewed supply chain. <br>
Mitigation: Avoid production CDN or iconfont script URLs unless the source is trusted, or self-host reviewed assets. <br>
Risk: React or Ant Design version mismatch can cause integration failures. <br>
Mitigation: Use the documented peer dependencies: React 18 and Ant Design 4.x-compatible packages. <br>


## Reference(s): <br>
- [pcloud-components online documentation](https://frank17008.github.io/pcloud-components) <br>
- [Component index](references/components-index.md) <br>
- [Common patterns](references/patterns.md) <br>
- [Create component guide](references/create-component.md) <br>
- [DForm component documentation](references/docs/DForm.md) <br>
- [DTable component documentation](references/docs/DTable.md) <br>
- [CRUD component documentation](references/docs/CRUD.md) <br>
- [Ant Design Form instance documentation](https://4x-ant-design.antgroup.com/components/form-cn/#FormInstance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, JSX, TSX, and HTML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package installation commands, peer dependency guidance, component API references, and React usage examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
