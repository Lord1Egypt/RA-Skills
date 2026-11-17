## Description:

Use when developer needs to install, use, or look up components from @pointcloud/pcloud-components npm package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank17008](https://clawhub.ai/user/frank17008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to install and apply the @pointcloud/pcloud-components React library, look up component APIs, and generate usage patterns for enterprise web interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing npm packages or using CDN assets can introduce supply-chain exposure.

Mitigation: Pin package versions, keep a lockfile, review the npm package before use, and avoid production CDN usage unless assets are self-hosted or protected with integrity checks.

Risk: Using incompatible React or Ant Design versions can cause integration failures.

Mitigation: Use the documented peer dependencies and verify compatibility with React 18 and Ant Design 4.x before adopting generated examples.

Risk: Some component documentation and sample UI text is in Chinese, which can lead to misunderstanding during implementation.

Mitigation: Review translated labels, validation messages, and component descriptions before using generated code in user-facing interfaces.

## Reference(s):

- [pcloud-components online documentation](https://frank17008.github.io/pcloud-components)
- [Component index](references/components-index.md)
- [Common patterns](references/patterns.md)
- [Create component guide](references/create-component.md)
- [Ant Design Form API](https://4x-ant-design.antgroup.com/components/form-cn/#API)
- [Ant Design ConfigProvider API](https://4x-ant-design.antgroup.com/components/config-provider-cn/#API)
- [wordcloud2.js documentation](https://github.com/timdream/wordcloud2.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSX/TSX examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include package installation commands, peer dependency notes, import examples, component props, and usage patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
