## Description:

Cria sites institucionais profissionais em React, Vite, TypeScript e Tailwind CSS 4 a partir de logos, imagens, apresentacoes, PDFs e identidade visual fornecidos pelo cliente.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guedes-xtent](https://clawhub.ai/user/guedes-xtent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and site-building agents use this skill to transform client visual materials and product content into institutional sites, landing pages, product pages, or one-page React websites in Portuguese or English. It guides project setup, content inventory, component selection, performance optimization, accessibility basics, SEO basics, and delivery checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect project-material folders and create or modify generated site files.

Mitigation: Run it only against a clearly chosen materials or project folder, then review generated files before use.

Risk: The workflow may install npm dependencies and incorporate third-party UI components or external assets.

Mitigation: Review dependency additions, 21st.dev retrievals, stock images, and external assets before shipping a generated site.

Risk: The bundled password-confirmation component is unsafe for real passwords or secrets.

Mitigation: Do not use that component with real credentials; remove it or replace it with a production-grade authentication flow.

## Reference(s):

- [Component Templates](artifact/references/components.md)
- [CSS Patterns & Visual Guidelines](artifact/references/patterns.md)
- [21st.dev component prompts API](https://21st.dev/api/prompts)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with React, TypeScript, Tailwind CSS, and shell command snippets; generated projects are Vite React files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create site files, install npm dependencies, adapt component templates, and propose image, font, SEO, accessibility, and build optimizations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
