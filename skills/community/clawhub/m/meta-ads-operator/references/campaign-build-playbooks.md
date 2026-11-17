# Campaign Build Playbooks

## Default build logic
1. Objetivo de negocio
2. Evento alvo
3. Arquitetura de campanha
4. Estrategia de budget
5. Audiencias
6. Criativos
7. Tracking
8. Review e `PAUSED`

## Scenario playbooks

### Validacao de oferta
- Estrutura enxuta
- ABO quando for importante forcar distribuicao por hipotese
- poucos conjuntos, mas testes claros

### Operacao perpetua
- simplifique estrutura
- priorize consolidacao de sinal
- CBO quando houver volume suficiente e varias teses concorrentes

### Lancamento
- separar captura, aquecimento, lembretes, remarketing e vendas
- buildar naming por fase do funil
- preparar criativos com antecedencia

### WhatsApp
- CTA e destino coerentes
- foco em conversa qualificada, nao so volume bruto
- preferir um app de mensagem por campanha

### E-commerce
- alinhar evento de compra e catalogo quando aplicavel
- isolar remarketing de quem viu produto, add to cart e checkout

### High ticket
- enfatizar qualidade, prova e etapas de qualificacao
- checar conexao com CRM e velocidade comercial

## UTM canonica
```text
utm_source=MetaAds&utm_medium={{adset.name}}|{{adset.id}}&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_term={{placement}}&utm_content={{ad.name}}|{{ad.id}}
```
