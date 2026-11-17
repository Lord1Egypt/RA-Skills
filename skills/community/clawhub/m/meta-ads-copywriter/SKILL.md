---
name: meta-ads-copywriter
version: 1.1.0
description: "Motor autônomo de redação direta e criativos visuais de alta conversão para Meta Ads via Habilis MCP Gateway (https://xvix.com.br). Gera variações AIDA/PAS e publica criativos."
triggers:
  - criar copy
  - escrever anuncio
  - copy meta ads
  - copywriter
  - substituir anuncio
  - texto para anuncio
  - gerar criativo
---

# ✍️ Meta Ads Copywriter & Creative Engine Skill

## 🚀 Onboarding & Setup Rápido (Primeiro Uso)

Ao executar a skill pela primeira vez:
1. Exibir checklist visual de status `[OK]` / `[PENDENTE]`.
2. Obtenha seu token de acesso MCP Habilis no portal de desenvolvedores: [https://xvix.com.br](https://xvix.com.br).
3. Assegure que as variáveis de ambiente locais estejam configuradas:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export META_ACCESS_TOKEN="EAA..." # Token do anunciante na ponta
   export META_AD_ACCOUNT_ID="act_..." # ID da conta de anúncios
   ```
4. Conecte o Habilis MCP no Hermes / OpenClaw / Claude Desktop (`config.yaml`):
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```

---

## 🛠️ Ferramentas MCP Utilizadas (Habilis Gateway)

Esta skill opera exclusivamente através das ferramentas fornecidas pelo **Habilis MCP Gateway**:
- `mcp__meta_ads__upload_image`: Faz upload de imagens e criativos renderizados para a biblioteca da conta.
- `mcp__meta_ads__create_ad_creative`: Registra criativos dinâmicos ou de imagem única com headline, copy e CTA.
- `mcp__meta_ads__update_ad`: Atualiza o criativo de anúncios existentes ou substitui variações pausadas.

---

## 🎯 FRAMEWORKS DE COPY DE ALTA CONVERSÃO

### 1. Modelo AIDA (Atenção, Interesse, Desejo, Ação)
- **Gancho (Atenção):** Pergunta provocativa ou quebra de padrão direta na dor do público (Primeiras 2 linhas).
- **Interesse:** Estatística impactante, caso de uso ou prova de eficiência.
- **Desejo:** Apresentação da transformação gerada pela oferta com gatilho de escassez/urgência.
- **Chamada de Ação (CTA):** Chamada clara e imperativa para a ação principal (Click-to-WhatsApp, Checkout ou Lead Form).

### 2. Modelo PAS (Problema, Agitação, Solução)
- **Problema:** Identificação cirúrgica da principal fricção enfrentada pelo cliente.
- **Agitação:** Consequências e custo financeiro/operacional de postergar a solução.
- **Solução:** Como a oferta resolve a dor de forma imediata e sem fricção.

### 3. Modelo Gancho + Prova + Oferta Irresistível
- **Gancho:** Contraste direto (ex: "Por que gastar horas fazendo X se você pode automatizar em 3 cliques?").
- **Prova:** Diferenciais técnicos, velocidade de implementação ou garantia.
- **Oferta:** Proposta de valor com risco zero (teste gratuito ou bônus de entrada).

---

## ⚡ FLUXO DE EXECUÇÃO AUTÔNOMA

1. **Diagnóstico do Briefing:** O agente analisa o nicho, público-alvo, URL de destino e proposta de valor fornecidos.
2. **Geração de Variações:** Redige 3 variações de copy aplicando ângulos distintos (Técnico/Direto, Comparativo/Preço, Transformacional/Benefício).
3. **Parametrização de UTMs:** Inclui parâmetros rastreáveis em todas as URLs:
   - `utm_source=meta_ads`
   - `utm_medium=feed` (ou `stories`/`reels`)
   - `utm_campaign={{campaign.name}}`
   - `utm_content=Ad01_{angulo}`
4. **Publicação via MCP:** Invoca `mcp__meta_ads__create_ad_creative` através do gateway Habilis (`https://xvix.com.br/api/mcp`) para subir o criativo aprovado.
