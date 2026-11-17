## Description:

Índices económicos argentinos y ajustes de montos para agentes (UVA, CER, ICL, inflación IPC, dólar histórico, días hábiles). Usar cuando el usuario pida actualizar un alquiler, ajustar un monto por inflación, convertir pesos a UVA, saber el valor de un índice en una fecha, el dólar de un día pasado o calcular un vencimiento en días hábiles. Servidor MCP remoto + REST; cobra por créditos prepagos con key de prueba gratis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torlettijoaquin](https://clawhub.ai/user/torlettijoaquin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve Argentine economic indicators and calculate indexed amounts, rental adjustments, historical exchange rates, and business-day deadlines.

### Deployment Geography for Use:

Argentina

## Known Risks and Mitigations:

Risk: Calculation amounts and dates are sent to an external provider using the API key, and usage consumes prepaid credits.

Mitigation: Send only necessary parameters, avoid names or full contracts, review the provider's privacy practices before sharing confidential details, and let the user control any payment.

Risk: Rental adjustment results may not match the governing contract terms.

Mitigation: Confirm the contract's index and adjustment interval with the user; present results as informational and defer to the contract clause.

## Reference(s):

- [Índices AR API](https://indices-ar-api-103907796853.us-east1.run.app)
- [MCP endpoint](https://indices-ar-api-103907796853.us-east1.run.app/mcp)
- [REST OpenAPI specification](https://indices-ar-api-103907796853.us-east1.run.app/openapi.json)
- [Remote skill instructions](https://indices-ar-api-103907796853.us-east1.run.app/skill.md)
- [Índices AR on ClawHub](https://clawhub.ai/torlettijoaquin/skills/indices-ar)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Structured economic values and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include the applicable data date; calls consume prepaid credits.]

## Skill Version(s):

0.1.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
