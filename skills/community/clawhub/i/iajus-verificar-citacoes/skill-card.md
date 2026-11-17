## Description:

Verifica uma a uma citações de decisões, precedentes e normas contra registros e fontes disponíveis. Use para checar existência, fidelidade e vigência; não use para pesquisar do zero.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaelob](https://clawhub.ai/user/rafaelob)

### License/Terms of Use:

MIT-0

## Use Case:

Advogados e equipes jurídicas usam a skill para conferir individualmente a existência, fidelidade e vigência de citações de decisões, precedentes e normas brasileiras com base nas fontes disponíveis. Ela não se destina a pesquisar o mérito jurídico do zero.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Termos de consulta filtrados são retidos por 90 dias, e consultas semânticas são encaminhadas a provedores de IA.

Mitigation: Não inclua dados confidenciais de clientes nas consultas e revise a política de privacidade IAJUS: https://iajus.com.br/privacidade.

Risk: Falhas, resultados parciais ou ausência de conteúdo suficiente podem deixar uma citação sem verificação conclusiva.

Mitigation: Trate esses casos como não verificáveis e confira a fonte oficial retornada antes de confiar no resultado.

## Reference(s):

- [Guia de pesquisa de jurisprudência](references/pesquisar-jurisprudencia/README.md)
- [Campos e confiança das fontes](references/pesquisar-jurisprudencia/references/campos-e-trust.md)
- [Ontologia OJBU](references/pesquisar-jurisprudencia/references/ontologia-ojbu.md)
- [Serviço MCP IAJUS](https://mcp.iajus.com.br/mcp)
- [Página da skill no ClawHub](https://clawhub.ai/rafaelob/skills/iajus-verificar-citacoes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Resumo em português com veredito por citação, fontes e eventuais limitações da verificação.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mantém separadas citações confirmadas, desatualizadas, não localizadas e não verificáveis; inclui links e dados da fonte quando disponíveis.]

## Skill Version(s):

3.0.19 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
