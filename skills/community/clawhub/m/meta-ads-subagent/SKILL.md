---
name: meta-ads-subagent
description: Subagente autônomo especialista em Meta Ads. Cria campanhas completas via MCP (Super Prompt), gera criativos com IA, monitora métricas (CPA/ROAS/CTR), executa otimizações, pausa anúncios ruins e alerta via Papi. Suporta multi-contas de anúncios.
triggers:
  - meta ads
  - facebook ads
  - otimizar tráfego
  - criar campanha meta
  - pausar anuncio ruim
  - cpa alto
  - relatório de tráfego
---

# Meta Ads Subagent Skill
**Desenvolvido por / Créditos:** Rafa Martins (rafacpti@gmail.com)

---

## 🚀 Onboarding & Setup Rápido (Primeiro Uso)

Ao executar a skill pela primeira vez ou ao configurar um novo ambiente:

### 📋 Checklist de Credenciais & Acesso
- [ ] **1. Habilis MCP Token (Obrigatório)**:
  - Obtenha seu token de acesso no portal de desenvolvedores: [https://xvix.com.br](https://xvix.com.br).
  - Defina: `export HABILIS_API_KEY="hab_live_..."`
- [ ] **2. Meta Ads Access Token (Cliente)**:
  - Token de usuário do sistema ou Graph API com escopo `ads_management` (reside estritamente no seu ambiente local).
  - Defina: `export META_ACCESS_TOKEN="EAA..."`
- [ ] **3. ID da Conta de Anúncios (`META_AD_ACCOUNT_ID`)**:
  - Formato: `act_<NUMERO_DA_CONTA>` (ex: `act_1234567890`).

### 🩺 Autodiagnóstico de Conectividade (Doctor)
```bash
hermes run "mcp_meta_ads_get_ad_account(ad_account_id='act_...')"
```

---

## 🛡️ Protocolo de Auditoria Contínua & Rotina de Cron Job

Nas auditorias periódicas e rotinas de monitoramento autônomo (via Cron ou sob demanda), o agente deve executar o seguinte checklist de governança integrada:

1. **Auditoria Financeira & Spend Cap:**
   - Obter `amount_spent`, `spend_cap` e `balance` da conta de anúncios.
   - Calcular a margem restante de teto de gastos (`spend_cap - amount_spent`).
   - Se a margem restante for menor que R$ 50,00 ou o saldo estiver baixo, emitir **Alerta Financeiro Crítico** destacando a necessidade de recarga no Billing Hub antes que a veiculação seja pausada pelo Meta.

2. **Validação de Destinos & Integridade de Landing Pages:**
   - Extrair as URLs de destino (`link_data` / `video_data`) de todos os criativos e anúncios ativos.
   - Testar o status HTTP de cada URL (garantindo retorno `200 OK` e ausência de erros 404/500 ou quebras de UTM).
   - Pausar imediatamente anúncios com destino quebrado.

3. **Governança de Performance & Stop-Loss:**
   - Avaliar CTR, CPC, LPVs e CPA dos anúncios ativos nos últimos 7 dias.
   - Aplicar a regra de stop-loss: pausar criativos cujo CPA exceda +30% da meta de custo por conversão/resultado.

4. **Triagem Inbound & Integração CRM (GHL/PAPI):**
   - Verificar mensagens não respondidas e leads inbound.
   - Categorizar contatos em:
     * 🚨 **Suporte Técnico / Bloqueio Operacional** (ex: falhas de licença/instância - prioridade máxima).
     * 🏥 **Lead Quente / Oportunidade Nichada** (solicitações de IA/soluções com intenção de compra).
     * 💼 **Follow-up Comercial** (negociações em andamento).
     * 🚫 **Spam / Broadcasts Terceiros** (descarte).

5. **Formatação do Relatório Executivo (Telegram/Canal):**
   - Estruturar em Markdown limpo, conciso e com emojis informativos.
   - Respeitar rigorosamente o limite de **3.000 caracteres** para entrega em mensagem única no Telegram.

---

## 🚀 Protocolo de Onboarding Interativo & Setup Guiado (First-Run Rule)

> 💡 **DIRETRIZ OBRIGATÓRIA PARA A IA / ASSISTENTE:**
> Ao iniciar o uso desta skill ou se as credenciais do Meta Ads estiverem ausentes no ambiente local:
> 1. **NÃO trave a conversa com erros de autenticação da Graph API.**
> 2. **Inicie imediatamente um diálogo de Onboarding Intuitivo, amigável e guiado.**
> 3. **Solicite os dados essenciais**, explicando passo a passo onde o usuário os encontra na Meta.
> 4. **Execute uma validação automática da conta (Health Check)** usando a tool `mcp_meta_ads_get_ad_account` para confirmar que o token está ativo e o ID da conta é válido.

### 📋 Checklist de Informações do Meta Ads

1. **`META_ACCESS_TOKEN` / Token do Sistema** *(Obrigatório)*:
   - *O que é:* Token de Usuário do Sistema ou de Acesso de Longa Duração da Graph API com permissões `ads_management`, `ads_read`, `pages_show_list`.
   - *Onde obter:* Meta Business Suite ➡️ Configurações do Negócio ➡️ Usuários do Sistema ➡️ Gerar Token.

2. **`META_AD_ACCOUNT_ID`** *(Obrigatório)*:
   - *O que é:* ID da Conta de Anúncios no formato `act_1234567890` (ou apenas os números).
   - *Onde obter:* No Gerenciador de Anúncios da Meta ou na URL do Ads Manager.

3. **`META_PAGE_ID`** *(Necessário para criação de anúncios)*:
   - *O que é:* ID da Página do Facebook anunciante.
   - *Onde obter:* Na Página do Facebook ➡️ Sobre ➡️ Informações da Página (ID numérico).

4. **`META_PIXEL_ID`** *(Para campanhas de Vendas/Conversão)*:
   - *O que é:* ID do Pixel/Dataset da Meta.
   - *Onde obter:* Gerenciador de Eventos ➡️ Configurações do Conjunto de Dados.

### 💬 Modelo de Mensagem de Boas-Vindas & Onboarding:

```text
👋 Olá! Bem-vindo ao Gestor Autônomo de Meta Ads!
Para começarmos a gerenciar suas campanhas, criativos e otimizações, só preciso que você me informe 2 dados básicos da sua conta Meta:

1️⃣ Seu Token de Acesso da Meta (`META_ACCESS_TOKEN`)
2️⃣ O ID da sua Conta de Anúncios (`META_AD_ACCOUNT_ID`, ex: `act_327126129438619`)

👉 Como prefere configurar?
• Pode colar os dados diretamente aqui no chat que eu salvo e valido para você.
• Ou você pode salvar no seu arquivo `.env` local (`/root/.hermes/metaads/.env`).
```

### ✅ Validação em Tempo Real (Health Check):
Assim que o cliente fornecer as informações, chame `mcp_meta_ads_get_ad_account(ad_account_id=...)`:
- **Se OK:** *"✅ Conta Meta Ads validada com sucesso! [Nome da Conta] está ativa (Moeda: BRL/USD). Deseja criar uma campanha nova, auditar os anúncios existentes ou gerar criativos?"*
- **Se Erro:** *"⚠️ Houve uma falha ao conectar na conta com esse token. Verifique se o token expirou ou se possui a permissão ads_management no Business Manager."*

---

- **Playbook de Auditoria & Stop-Loss:** Ver `references/audit_playbook.md` para rotina detalhada de checagem de saldo, integridade de LPs e métricas de leilão.
- **Padrão de Nomenclatura Start Company (3 Níveis):** Ver `references/naming_conventions_and_briefing_standards.md` para taxonomia oficial de campanhas (`[TAG] {NUM} [{OBJ}] {ESTR}_{ORÇ}_[{OFERTA}] – {DATA}`), conjuntos (`{CAMP}.{SUB}_[{POS}]_({GENERO}_{IDADE})_{INTERESSES}_{GEO}_{DATA}`) e anúncios (`{CAMP}.{SUB}.{NUM_ANUNCIO}_{CRIATIVO}_{DATA}`), além da metodologia de teste isolado 10x10.
- **Habilis SaaS Gateway & Zero-Storage:** Ver `references/habilis_saas_architecture_and_zero_storage.md` para governança do produto SaaS comercial (/home/orca/orca/habilis), separação estrita de escopo em relação a skills locais, e garantia in-memory de credenciais do cliente.
- **Script de Execução Automatizada:** Ver `scripts/audit_account.py` para script de probe de integridade de conta e anúncios.

---

## 🎯 DIRETRIZES ESTRATÉGICAS DE CONVERSÃO & COMPLIANCE DE API

- **Regra de Ouro (Vendas = Conversão com Pixel):** Toda campanha cujo objetivo final seja vendas ou faturamento deve ser configurada obrigatoriamente como Conversão (`OUTCOME_SALES` com `promoted_object: {"pixel_id": "<PIXEL_ID>", "custom_event_type": "PURCHASE"}` e `optimization_goal: OFFSITE_CONVERSIONS`), nunca tráfego de cliques (`OUTCOME_TRAFFIC` / `LINK_CLICKS`).
- **Guards de Criação e Duplicação na Graph API v20.0+:**
  - **Budget Sharing em ABO (Meta Error 4834011):** Ao criar campanhas `OUTCOME_SALES` sem orçamento a nível de campanha (ABO), envie explicitamente `is_adset_budget_sharing_enabled=false`.
  - **Bid Strategy em Conversão (Meta Error 2490487):** Ao criar AdSets de conversão sem limite de custo, defina explicitamente `bid_strategy=LOWEST_COST_WITHOUT_CAP` para evitar a exigência de `bid_amount`.
  - **Compliance Brasil / Anunciante Ausente (Meta Error 3858634):** Para conjuntos veiculados no Brasil, envie obrigatoriamente:
    - `regional_regulated_categories=["BRAZIL_REGULATION","VOLUNTARY_VERIFICATION"]`
    - `regional_regulation_identities={"universal_beneficiary":"<BM_ID>","universal_payer":"<BM_ID>"}`
  - **Rate Limit em Operações Individuais de Anúncios (Meta Error 613/4841018):** Atualizações individuais de anúncios (`update_ad`) em tokens de usuário sofrem throttle de 1 requisição a cada 30 segundos. Para operações manuais, respeite um delay de 31s entre chamadas ou utilize endpoints em lote (`batch`).
  - **Obrigatoriedade da Taxonomia de Nomenclatura (3 Níveis):** Toda e qualquer campanha, conjunto e anúncio criado ou ajustado DEVE seguir rigorosamente a taxonomia de 3 níveis (`[CAMPANHA].[SUB]_[CRIATIVO]_[AUDIENCE]_[DATA]`). Consulte `references/naming_conventions_and_briefing_standards.md`.
  - **Segurança e Rascunho:** Ao duplicar campanhas para reestruturação, mantenha a campanha, adsets e anúncios criados com `status="PAUSED"` para validação do gestor antes de ativar a veiculação.

---

## 🎨 FRAMEWORK DE CRIATIVOS VISUAIS
- **Padrão de Nomenclatura & Hierarquia em 3 Níveis (Start Company / Evandro Santos):** Consulte `references/naming_conventions_and_briefing_standards.md` para a taxonomia e metodologia de teste:
  - **Nível 0 (Campanha):** `[TAG] {NUM} [{OBJETIVO}] {ESTRUTURA}_{ORCAMENTO}_[{OFERTA}] – {DATA}` (ex: `[START] 001 [ENG-MSG] 1-1-1_CBO_[ONETIME] – 16.06.26`)
  - **Nível 1 (Ad Set):** `{CAMPANHA}.{SUB}_[{POS}]_({GENERO}_{IDADE})_{INTERESSES}_{GEO}_{DATA}` (ex: `001.01_[AUTO]_H-M_20-55_Devs-Software_BR_08.09.26` ou `001.02_[IG]_H_25-45_Marketing-Ecom_SP_16.06.26`)
  - **Nível 2 (Anúncio):** `Ad{NUM} - {HEADLINE} | {PREÇO} | {COR/VARIAÇÃO}` (ex: `Ad01 - WhatsApp API Oficial | R$ 14,90 | Amarelo` e `Ad02 - WhatsApp API Oficial | R$ 14,90 | Azul / V2`). Prefixo colado sem espaço (`Ad01`, `Ad02`, `Ad03`...); numeração estritamente única e sequencial para todos os anúncios, sem repetir o prefixo (a versão 2 do Ad01 vira Ad02); extrair headline do criativo/vídeo, preço e cor/variação de forma legível e objetiva. Apresentar proposta antes de alterar na API.
  - **Regras Críticas:** Posicionamento (`[AUTO]`, `[FB/IG]`, `[IG]`, `[FB]`), Gênero/Idade (`H-M_20-55`, `H_25-50`), Máximo 2 interesses no nome para manter clareza, Localização (`BR`, `SP`, `POA`, etc.) e Data.
- **Padrão Narrativo Visual de 3 Etapas:** Consulte `references/visual_creative_framework.md` para a estrutura completa de criativos B2B/SaaS no padrão *Cliente falando ➔ IA processando ➔ Empresa faturando ($)* renderizados via Chrome Headless / Playwright (1080x1080).
- **Diagnóstico de Funil e Conversão Pós-Clique:** Consulte `references/funnel_and_conversion_troubleshooting.md` para auditoria de gargalos de conversão (aba incorreta em /auth, fricção de CPF/CNPJ, cadastro embutido on-page e templates de relatórios PAPI WhatsApp).
- **Safe-Zones e Logos Obrigatórias:** Margens de segurança de 60px a 80px para evitar cortes de texto e inclusão do logotipo oficial em vetor SVG.
- **Link Data API Guard (Meta Error 1815520):** Ao criar `adcreative` com `link_data`, certifique-se de que `link` e `call_to_action.value.link` apontem para a URL exata do destino externo (site/landing page), evitando que a Meta reclame de inconsistência ou formato de payload.
- **Prepay Account Spend Cap Guard (Meta Error 100 / Subcode 1487840):** Em contas pré-pagas (`is_prepay_account: true`), o Graph API rejeita qualquer alteração de `spend_cap` (`POST /act_<ID> {"spend_cap": ...}`). O limite de veiculação é o próprio saldo pré-pago recarregado. Para desbloquear/aumentar entregas, oriente o usuário a recarregar saldo via PIX/Cartão diretamente pelo Billing Hub (`https://adsmanager.facebook.com/billing_hub/payment_settings?act=<ID>`).
rejeições em conjuntos com otimização `LINK_CLICKS`.
- **Prepay Accounts & Spend Cap Guard (Meta Error 1487840):** Em contas com modalidade pré-paga (`is_prepay_account: true` via PIX/Boleto/Crédito pré-pago), a API rejeita alterações manuais no campo `spend_cap` com o erro *"Alteração inválida para uma conta pré-paga"* (OAuthException 100 / subcode 1487840). O limite máximo de veiculação é rigorosamente vinculado ao saldo de fundos adicionados (`funding_source_details`). Para liberar veiculação adicional, os fundos devem ser recarregados no Gerenciador de Cobrança / Billing Hub da Meta.
- **Teste A/B de Copys (AIDA & PAS):** Ao substituir ou testar variações de anúncios de baixa entrega ou CTR fraco (<0,80%), crie novos `adcreatives` e adicione novos `ads` ativos dentro do mesmo conjunto de anúncios (ABO) em vez de sobrescrever o criativo original imediatamente. Isso permite que o algoritmo da Meta distribua impressões para a melhor copy sem perder o histórico do aprendizado.
- **Identidade do Anunciante (Facebook Page):** Consulte `references/page_identity_and_branding.md` — CONFIRME a `page_id` com o usuário **antes** de gerar criativos (nunca aceite a Page default da API).
- **Otimização de Funil e Telas de Conversão:** Consulte `references/funnel_checkout_optimization.md` para diretrizes de redução de fricção pós-clique, adaptação dinâmica de formulários por DDI internacional e deep linking direto na aba de cadastro (`signup`).
- **Auditoria de Funil & Falso Alarme de Saldo:** Consulte `references/funnel_audit_and_billing_troubleshooting.md` para resolução do erro de restrição em contas pré-pagas (saldo R$ 0,00), diagnóstico de conversão pós-clique e critérios de expansão LATAM.
- **Compliance de Anunciante & Gestão de Faturamento (Meta Graph API v21.0+):** Consulte `references/meta_api_compliance_and_billing.md` para resolver erros de `compliance_section` / anunciante ausente (passando `regional_regulation_identities` com `universal_beneficiary` e `universal_payer` numéricos) e tratar falsos positivos de restrição em contas pré-pagas com saldo zerado.
- **Falso Bloqueio Mobile por Saldo Zero:** Consulte `references/auth_and_api_troubleshooting.md` (Seção 3) quando o app mobile travar na tela *"Restrição da conta de anúncio"* — em contas pré-pagas com saldo zerado, a Meta bloqueia recargas in-app; a solução é enviar o link web direto de cobrança (`/billing_hub/payment_settings?act=<id>`).
- **Auditoria de Procedência de Ativos ("de onde saiu esse anúncio?"):** Consulte `references/asset_provenance_audit.md`. NUNCA deduza a origem de um ativo desconhecido — varra a Graph API em **todas** as contas do token via `scripts/meta_asset_provenance_sweep.py` E faça grep nos outputs/prompts do cron.
- **Auditoria Contínua, Stop-Loss e Health Check de LPs:** Consulte `references/meta_ads_audit_and_lp_monitoring.md` e `references/unanswered_leads_triaging_patterns.md` para o protocolo de inspeção periódica de métricas (`last_7d`), verificação de Account Spend Cap (teto da conta), diagnóstico de Delivery Skew (vício de entrega entre anúncios), regras de stop-loss (+30% CPA/CPC), teste HTTP/latência de landing pages, triagem/priorização de conversas inbound no CRM (GHL) e formatação executiva (≤3.000 caracteres) para Telegram.
- **Troca de URL de Destino & Estratégia de Cupons:** Consulte `references/creative_url_swapping_and_pricing_strategy.md` para o procedimento de contornar a imutabilidade de `adcreative` na Graph API e governança de descontos conversacionais (1-on-1 no WhatsApp) para produtos low-ticket.
- **Instagram Actor / Placement Linking (Meta Error 1815199):** Ao criar `adcreative` com `object_story_spec` vinculando a uma Facebook Page, o Meta Ads valida automaticamente permissões de posicionamento no Instagram. Se a conta de anúncios não tiver acesso direto à conta de Instagram vinculada à página ou omitir `instagram_user_id`, a API retornará `OAuthException code 200 (error_subcode 1815199: "A conta de anúncios não tem acesso à conta do Instagram")`. Para solucionar:
  1. Consulte as contas de Instagram atribuídas à conta de anúncios via `GET /act_<AD_ACCOUNT_ID>/instagram_accounts`.
  2. Passe explicitamente o `instagram_user_id` correspondente (ou utilize o PBIA / Page-Backed Instagram Account com `GET /<PAGE_ID>/page_backed_instagram_accounts`) dentro do `object_story_spec` para autorizar a entrega multiplataforma.
- **Validação Pré-Tráfego da Landing Page:** Consulte `references/landing_page_traffic_readiness.md` — antes de direcionar tráfego pago, valide o alinhamento mensagem/preço (message match), prova interativa (demos de voz/chat), parâmetros de checkout (`/auth?plan=...`) e presença do Meta Pixel ativo.
- **Protocolo de Conversão e Pré-Aprovação de Landing Pages:** Consulte `references/landing_page_conversion_protocol.md` — NUNCA alterar ou publicar modificações em Landing Pages sem apresentar o diagnóstico, cópia e componentes para validação prévia explícita do usuário. Garanta alinhamento de mensagem (Message Match) entre o gancho do anúncio (ex: IA de Voz a R$ 49,90) e a 1ª dobra da LP (players de áudio interativos e precificação visível).
- **Diagnóstico de Vício de Entrega (Delivery Skew) & Equalização de Criativos:**
  - O algoritmo da Meta tende a concentrar mais de 70-80% do orçamento no primeiro anúncio que obtém cliques iniciais baratos, mesmo quando outros criativos no mesmo conjunto possuem CTR significativamente superior (ex: 2.0%+ vs 0.45%) e maior intenção comercial (ex: Voz IA vs WhatsApp genérico).
  - **Ação Recomendada:** Isolar criativos de alta performance em ad sets dedicados (ABO) ou pausar temporariamente por 24-48h o criativo dominante para forçar a fase de aprendizado e entrega nos novos ângulos.
- **Estratégia de Destino (Landing Page vs Click-to-WhatsApp):**
  - Para produtos de tecnologia e SaaS com teste grátis ou onboarding imediato, testar em paralelo:
    1. *Landing Page (Tráfego/Conversão):* Leva para o domínio oficial com Pixel/CAPI.
    2. *Click-to-WhatsApp (Direct Lead):* Reduz atrito, direcionando o clique direto para o agente de IA no WhatsApp para qualificação e liberação de cupom/acesso em tempo real. Inclui descoberta de Pages via `me/accounts` + `BM/owned_pages`, os limites do System User token (rename/foto/bio de Page = erro `#283`/`#3`, sempre trabalho manual do usuário), o kit de entrega (avatar 800x800 + capa 1640x924 + tabela de campos + bio copiável) e como trocar a identidade de anúncios já criados sem recriar a campanha. Templates: `templates/fb_page_avatar.html`, `templates/fb_page_cover.html`.
- **Meta Pixel & Gestão Financeira:** Consulte `references/meta_pixel_and_billing_management.md` para o ciclo completo de criação do Pixel via API, injeção em SPAs (React/Vite/Next.js), auditoria de saldo pré-pago e resolução da armadilha do limite de gastos (*Spend Cap*).

## 🛡️ REGRAS DE GOVERNANÇA E HUMAN-IN-THE-LOOP (OBRIGATÓRIO)
1. **Stop-Loss Autônomo (+30% CPA):** O Hermes pode **pausar automaticamente** anúncios ou adsets que ultrapassarem +30% do CPA meta configurado.
2. **Orçamento Diário Alto (Human-in-the-Loop):** Para criar ou ativar campanhas com verba diária superior a **R$ 100,00/dia**, o Hermes **DEVE solicitar confirmação humana** antes de executar a rota ativa.
3. **Orçamento de Teste Baixo (ex: R$ 10,00 a R$ 20,00/dia):** A Meta exige um gasto mínimo de ~$1 USD/dia por conjunto de anúncios (~R$ 6,00). Com verba diária baixa (ex: R$ 10/dia), **NÃO** fragmentar em múltiplos conjuntos;
4. **Status Inicial Padrão:** Toda nova campanha/conjunto deve ser criada inicialmente com status `PAUSED` para revisão visual e conferência de ativos antes da ativação.

---

## ⚠️ PITFALLS E REQUISITOS TÉCNICOS DA META GRAPH API (v21.0+)

0. **Parâmetro `fields` em `mcp_meta_ads_get_ad_account` (Erro 100 business_management) e Verificação de Spend Cap:**
   - Chamar `mcp_meta_ads_get_ad_account` sem o parâmetro `fields` requisita campos padrão que exigem permissão de administrador de negócios (`(#100) Requires business_management permission to access the field`).
   - **Solução:** Sempre passe campos explícitos e seguros: `fields="id,name,account_status,amount_spent,spend_cap,balance,currency,disable_reason,min_daily_budget"`.
   - **Spend Cap Exaurido ou Margem Crítica (`amount_spent >= spend_cap` ou margem restante < R$ 50,00):** Quando o gasto acumulado atinge o teto da conta (`spend_cap`), o Meta Ads cessa silenciosamente a entrega de todos os anúncios da conta, mantendo o status `ACTIVE` mas com 0 impressões novas. Calcule a margem restante (`spend_cap - amount_spent`); se a margem for baixa (ex: < R$ 50,00) ou esgotada, reporte como alerta de severidade máxima no topo do relatório para evitar interrupção iminente de tráfego.
- **Listagem de Anúncios na Graph API v21.0 (Edge `/ads` no Ad Account vs Campaign):** Ao consultar anúncios via chamadas diretas REST na Graph API v21.0, a rota `GET /{campaign_id}/ads` pode retornar `{"data": []}` em determinadas configurações de conta/token. Utilize sempre a rota da conta de anúncios `GET /act_{AD_ACCOUNT_ID}/ads?fields=id,name,status,effective_status,adset_id,campaign_id,creative...` ou o endpoint MCP `mcp_meta_ads_list_ads` com `ad_account_id` para mapeamento confiável de todos os anúncios.

1. **Campo `is_adset_budget_sharing_enabled` (ABO vs CBO):**

1. **Campo `is_adset_budget_sharing_enabled` (ABO vs CBO):**
   - Ao criar campanhas ABO (orçamento no conjunto de anúncios e não na campanha), a API exige explicitamente `is_adset_budget_sharing_enabled: False` (ou `True`). Caso omitido, a API retorna erro `OAuthException code 100 (error_subcode 4834011)`.

2. **Flag `targeting_automation` e `advantage_audience`:**
   - Em novos conjuntos de anúncios, a Meta exige a definição de `targeting_automation: {'advantage_audience': 1}` (ou `0`).
   - **Atenção à Idade Máxima:** Quando `advantage_audience: 1` estiver habilitado, o campo `age_max` **NÃO** pode ser menor que 65 anos (retorna erro `subcode 1870189`). Defina apenas `age_min` ou mantenha `age_max: 65`.

3. **`bid_amount` Obrigatório em Otimização de Cliques/Tráfego:**
   - Para adsets com `optimization_goal: 'LINK_CLICKS'`, forneça `bid_amount` em centavos (ex: `150` para R$ 1,50) para evitar o erro `subcode 2490487`.

4. **Anúncios Híbridos: Site vs WhatsApp Direto (`wa.me`):**
   - **Link para Landing Page:** Utilize `call_to_action: {'type': 'LEARN_MORE', 'value': {'link': 'https://...'}}`.
   - **Link Direto para WhatsApp:** Utilize `call_to_action: {'type': 'CONTACT_US', 'value': {'link': 'https://wa.me/55...?'}}` com texto codificado em URL (`?text=...`) para pré-carregar a mensagem do lead. consolidar 100% da verba em **1 único conjunto de anúncios forte** rodando 2 a 3 criativos em paralelo por 5 a 7 dias.
4. **Exclusão de Dados no GHL ou Meta:** É estritamente **PROIBIDO deletar** campanhas, contatos ou dados sem validação humana manual prévia.
5. **Resiliência e Fallback de Ferramentas:** Em caso de oscilação ou manutenção no MCP, utilizar queries diretas ou rotas alternativas conforme diretrizes de fallback.
6. **Gestão de Token e Processos MCP:**
   - **Diagnóstico de Expiração:** Erro `OAuthException 190 / subcode 463` indica token expirado.
   - **Atualização:** Atualizar em `~/.hermes/.env` (`hermes config set META_ACCESS_TOKEN <token>`) e `~/.hermes/config.yaml` em `mcp_servers.meta-ads.env.META_ACCESS_TOKEN`.
   - **Recarregar Processo MCP:** Executar `pkill -f mcp-meta-ads` para encerrar workers antigos e permitir que o Hermes instancie processos com o novo token.
   - **Tratamento de Indisponibilidade:** Se o MCP retornar erro temporário de rede, registrar no relatório a indisponibilidade, manter o estado seguro (campanhas preservadas) e prosseguir com a auditoria dos demais módulos. Token Expirado (Code 190):** Se o token retornar `OAuthException 190` ou erro de autenticação, emitir alerta de necessidade de renovação de credencial.TTP e GHL). Não travar a execução.
5. **Execução Segura em Cron Jobs:** Em execuções via Cron, evitar comandos com pipes para interpretadores (`cat | python3`) ou `execute_code` (bloqueado sem aprovação interativa). Utilize scripts auxiliares gravados em arquivo ou comandos diretos.

---

## 🚀 FLUXO DE EXECUÇÃO DA AUDITORIA
1. **Mapeamento da Estrutura:**
   - Inspecionar a conta de anúncios (`mcp_meta_ads_get_ad_account` passando `fields="id,name,account_status,amount_spent,spend_cap,balance,currency,disable_reason,min_daily_budget"` para evitar erro de permissão `business_management` do default) e limites (`mcp_meta_ads_get_ads_volume`) para verificar status da conta, spend cap, saldo disponível e limite de anúncios ativos.
   - Listar todas as campanhas da conta (`mcp_meta_ads_list_campaigns`).
   - Listar os anúncios e seus estados de veiculação (`mcp_meta_ads_list_ads`), mapeando a hierarquia (Campanha -> Conjunto de Anúncios -> Anúncio).
   - Identificar problemas estruturais, erros de configuração ou direcionamentos descontinuados nos anúncios (ex: erros `WITH_ISSUES` de código 1870250).
2. **Extração e Teste das URLs de Destino (Landing Pages):**
   - Coletar as mídias/criativos via `mcp_meta_ads_list_creatives`.
   - Extrair links estruturados (`link_data.link`, `website_url`) e links embutidos em formato de texto no campo `body` (como URLs de WhatsApp, YouTube ou encurtadores/afiliados).
   - Testar o funcionamento e a resposta HTTP detectando redirecionamentos via terminal com:
     `curl -sIL -o /dev/null -w "%{http_code} %{url_effective}\n" <URL>`
3. **Puxar Insights e Aplicar Otimização / Stop-Loss (Últimos 7 dias):**
   - Executar leitura via MCP `mcp_meta_ads_get_campaign_insights` e `mcp_meta_ads_get_ad_insights` nos últimos 7 dias (`last_7d`). **Nota:** Mesmo quando `amount_spent >= spend_cap`, consulte o período (`last_7d`) para auditar o desempenho prévio e identificar Delivery Skew / CTR dos criativos.
   - Tratar retornos vazios `{"data": []}` em campanhas pausadas sem histórico recente como ausência de gasto.
   - **Avaliar Matriz de Otimização:**
     - CPA > Meta + 30% $\to$ Pausa Anúncio (`mcp_meta_ads_update_ad`).
     - Dispara `meta-ads-copywriter` para criar 3 variações novas.
     - Envia Alerta ao WhatsApp do Gestor via `ghl_client.py --action notify_manager`.
4. **Verificação de Leads GHL (Cross-Skill):**
   - Quando a auditoria inclui GHL (skill `ghl-integration`), executar `ghl_client.py --action unanswered` para obter leads sem resposta.
   - **ATENÇÃO:** O output do script retorna `id` = Conversation ID, **NÃO** Contact ID. Para obter o `contactId` (necessário para `send_msg`, movimentação de pipeline, etc.), é preciso fazer uma chamada raw à API GHL `/conversations/search` e extrair o campo `contactId` de cada conversa. Veja pitfall #1 do `ghl-integration`.
   - Classificar leads conforme `references/unanswered_leads_triaging_patterns.md` do `ghl-integration`.
5. **Relatório Gerencial:**
   - Consolidar o checklist em um relatório estruturado informando o status da conta, gastos reais, detalhes de eventuais termos descontinuados ou bloqueios detectados na leitura da API, e o status final dos destinos testados.
   - Quando spend_cap esgotado, destacar como item CRÍTICO no topo do relatório.

---

## 🛠️ COMPORTAMENTOS CONHECIDOS & TROUBLESHOOTING (CRON)
1. **Bloqueio de Python Scripts (execute_code) no Cron:**
   Quando executado como cron job agendado, a ferramenta `execute_code` é desabilitada por motivos de segurança. **Nunca** use scripts Python para fazer query ou chamadas em lote nas APIs; utilize chamadas diretas aos endpoints do MCP correspondentes.
2. **Erros de Validação da API do Meta (HTTP 400 / Código 3907143 e 1991005):**
   Ao tentar atualizar anúncios antigos ou com erros no criativo/mídia (por exemplo, erros do tipo *"Sua mídia é inválida"* - Código 3907143, ou *"A edição de posts turbinados somente é permitida no app do Instagram"* - Código 1991005 / HTTP 400 Code 10), a API do Meta pode rejeitar a alteração de status (`PAUSED`/`ACTIVE`) no nível do anúncio ou adset.
   - **Solução:** Reporte o bloqueio exato da API e o erro correspondente no relatório sintetizado. Se necessário interromper a veiculação e o anúncio/adset direto estiver bloqueado (por validação de mídia ou por ser post turbinado), o controle deve ser feito pausando a Campanha (`campaign`) correspondente.
   - **Fallback quando ad-level update falha (confirmado 2026-08-12):** Ao tentar pausar um anúncio e receber 3907143 ("Sua mídia é inválida"), verificar se a campanha-pai já está PAUSED. Se sim, documentar o bloqueio no relatório e não insistir na chamada — a veiculação já está interrompida pelo nível acima. Se a campanha estiver ACTIVE e o ad/adset recusar pausa, escalar pausando a campanha via `mcp_meta_ads_update_campaign`.
3. **Erros de Configuração de Público / Direcionamento Detalhado Descontinuado (Código 1870250):**
   - **Causa:** O Meta remove/descontinua opções de direcionamento detalhado frequentemente. AdSets antigos podem falhar com `effective_status: WITH_ISSUES` e `error_code: 1870250` (*"Este conjunto de anúncios não está sendo veiculado porque usa opções de direcionamento detalhado que foram combinadas. Edite seu público..."*).
   - **Solução:** O público precisa ser editado e limpo antes da ativação do AdSet.
4. **Insights Vazios para Campanhas Inativas:**
   - Ao executar `mcp_meta_ads_get_campaign_insights`, se a campanha permaneceu pausada no período (e.g. `last_7d`), o retorno de insights será `{"data": []}`. Tratar isso como ausência de veiculação/gasto e não como erro de API.
5. **Extração e Verificação de Destinos (Landing Pages/WhatsApp):**
   - Em auditorias de disponibilidade, extraia links do criativo inspecionando `asset_feed_spec.link_urls` (chave `website_url`) ou varrendo o texto do `body` para URLs (como YouTube, links de afiliados ou APIs do WhatsApp).
     * Comando para extração em massa via `jq`:
     ```bash
     jq -r '.result | fromjson | .data[] | [.id, .name, .body, (.object_story_spec.link_data.link? // .asset_feed_spec.link_urls[0].website_url? // .object_story_spec.video_data.call_to_action.value.link?)] | @tsv' /tmp/hermes-results/<CALL_ID>.txt
     ```
     * Comando para filtrar criativos específicos por ID via `jq`:
     ```bash
     jq -r '.result | fromjson | .data[] | select(.id == "ID_1" or .id == "ID_2")' /tmp/hermes-results/<CALL_ID>.txt
     ```
     > **Filename dinâmico:** `/tmp/hermes-results/<CALL_ID>.txt` muda a cada chamada — use o path retornado pelo tool result.
   - Valide usando requisições HTTP detalhadas que sigam redirecionamentos (-L) para identificar problemas de link quebrado ou domínio fora do ar:
     ```bash
     curl -sIL -o /dev/null -w "%{http_code} %{url_effective}\n" <URL>
     ```
   - O histórico de baseline e listagem dos destinos da conta Ramel se encontra em `references/landing_page_audit.md`.
6. **Processamento de Retornos Grandes de Criativos (JSON volumoso):**
   - **Causa:** O endpoint `mcp_meta_ads_list_creatives` pode retornar dados enormes (100KB+), fazendo com que o agente salve o resultado em `/tmp/hermes-results/xxxx.txt`.
   - **Solução:** Evite ler tudo no contexto. Use `jq` via terminal para extrair de forma cirúrgica e performática os atributos necessários (como `id`, `name`, `body`, `asset_feed_spec.link_urls[].website_url`).
   - **Detecção de links em `body`:** Criativos com links de afiliados ou YouTube costumam ter o URL embutido no campo `body` (texto livre) ao invés do campo estruturado. Varra o campo `body` via `jq` para não deixar passar destinos indiretos:
     ```bash
     jq -r '.result | fromjson | .data[] | select(.body != null) | [.id, .name, .body] | @tsv' /tmp/hermes-results/<CALL_ID>.txt
     ```
   - **Links em anúncios de vídeo (video_data CTA):** Adicionalmente ao `link_data` e `asset_feed_spec`, anúncios de vídeo expõem a URL de destino sob `object_story_spec.video_data.call_to_action.value.link`. Incluir esse caminho no jq de extração:
     ```bash
     jq -r '.result | fromjson | .data[] | {id, name, link: (.object_story_spec.link_data.link // .asset_feed_spec.link_urls[0].website_url // .object_story_spec.video_data.call_to_action.value.link), body: (.body // .object_story_spec.link_data.message // .object_story_spec.video_data.message)}' /tmp/hermes-results/<CALL_ID>.txt
     ```
   - **Filename dinâmico:** O path do resultado (`/tmp/hermes-results/call_NNNNN.txt`) muda a cada invocação MCP. Use o path retornado pelo tool result ao invés de hardcodar o nome do arquivo.

9. **Teste de Landing Pages em Lote (curl multi-URL):**
   - O `curl -sIL` aceita múltiplas URLs em sequência na mesma chamada de terminal. Use para testar vários destinos de uma vez:
     ```bash
     curl -sIL -o /dev/null -w "%{http_code} %{url_effective}\n" "https://url1" "https://url2" "https://url3"
     ```
   - Retorna código HTTP final após seguir todos os redirecionamentos (301/302/303). Código 200 = destino funcionando. Código 404/500/timeout = destino quebrado.
   - Links de afiliados/encurtadores (ex: `anrdoezrs.net`, `kqzyfj.com`) são legítimos se o destino final retorna 200. Documentar o domínio final na auditoria para referência.

8. **Diagnóstico de Painel Web/Dashboard e Conexão de Gateway:**
 - **Acesso HTTP vs HTTPS por IP:** Requisição direta via IP cru deve ser feita via HTTP (`http://<server-ip>/metaads.html`). Para HTTPS, utilize o domínio configurado (`https://xvix.com.br`).
 - **Status da Instância WhatsApp/Papi:** Se relatórios/automações falharem, valide se o gateway WhatsApp não está desconectado (`papi_disconnected` / instância inativa). A solução exige releitura do QR Code no painel Papi.
