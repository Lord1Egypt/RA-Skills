# Meta Ads API — Insights e Comportamentos Documentados

## Conta Ramel: act_327126129438619
- **Business:** Ramel Tecnologia e Desenvolvimento (ID: 100754338860752)
- **Page:** Ramel Segurança E Tecnologia / Papi (actor_id: 112665111651993 / 1336366589550605) | Limite: 250 anúncios ativos.
- **Moeda:** BRL | **Timezone:** America/Sao_Paulo (-3)
- **Pixel:** 1079270794502909

---

## 📊 Desempenho Real da Campanha PAPI (2026-09-10)
- **Campanha Ativa:** `[PAPI] 001 [CONV-PURCHASE] 1-2-8_ABO_[RECORRENTE] – 08.09.26` (`120253639419180154`)
- **Status da Campanha:** `ACTIVE` (ABO - R$ 10,00/dia no conjunto Devs)
- **Conjunto Ativo:** `001.01_[AUTO]_H-M_20-55_Devs-Software_BR_08.09.26` (`120253639428040154`)
- **Métricas Consolidadas:**
  - Investimento Total: **R$ 16,53**
  - Impressões: **448** | Alcance: **349 pessoas** (Frequência: 1.28)
  - Cliques Totais: **24** | Cliques no Link: **16**
  - CTR Médio: **5,36%** (Top performance)
  - CPC Médio: **R$ 0,69** | CPM: **R$ 36,90**
  - Pageviews na Landing: **9**
  - Leads no Pixel: **4 cadastros registrados**
  - Custo por Lead Médio (CPL): **R$ 4,13**

### 🏆 Comparativo por Criativo & Anúncio
1. **Ad001-v2 - Conecte seu n8n ao WhatsApp Oficial | R$ 14,90 | Amarelo** (`120253639433980154`):
   - Gasto: R$ 6,74 | Impressões: 138 | Cliques: 7 | CTR: 5,07%
   - Landing Page Views: 5 | Leads: **3** | **CPL: R$ 2,25 / lead** 🚀
   - *Diagnóstico:* Campeão absoluto de conversão em leads qualificados. O gancho do n8n aliado ao preço de entrada de R$ 14,90 elimina atrito de decisão.
2. **Ad001 - WhatsApp API Oficial | R$ 14,90 | Devs** (`120253639435670154`):
   - Gasto: R$ 5,17 | Impressões: 156 | Cliques: 14 | **CTR: 8,97%** 🔥
   - CPC: **R$ 0,37** | Landing Page Views: 3 | Leads: **1** | CPL: R$ 5,17
   - *Diagnóstico:* Campeão de atração de tráfego e clique barato. Alto volume de cliques, ideal para topo de funil e retargeting.
3. **Ad002 - Atendente com IA 24/7 | R$ 49,90 | Base** (`120253639435540154`):
   - Gasto: R$ 3,26 | Impressões: 101 | Cliques: 2 | CTR: 1,98% | Leads: 0.
4. **Ad002-v2 - Voz com IA e VoIP SIP | R$ 49,90 | Azul** (`120253639435350154`):
   - Gasto: R$ 1,36 | Impressões: 53 | Cliques: 1 | CTR: 1,89% | Leads: 0.

---

## ⚡ Arquitetura de Cadastro de Alta Conversão (Modelo ZAI na rota /auth)
Para maximizar a conversão dos cliques em leads registrados:
1. **Google OAuth 1-Click no Topo:** Posicionado antes de qualquer formulário para captura instantânea.
2. **Campos Essenciais Apenas:** Nome Completo, WhatsApp (E.164 com máscara dinâmica), E-mail e Senha.
3. **Progressive Profiling:** Eliminação total da exigência de CPF/CNPJ ou dados de cartão no primeiro acesso. Dados fiscais são coletados somente no checkout de recarga/assinatura no Asaas.
4. **Rastreamento Imediato:**
   - Disparo de `fbq('track', 'Lead', { content_name: 'Auth ZAI Lead', status: 'registered' })` e `fbq('track', 'CompleteRegistration')`.
   - GTag `generate_lead` e `sign_up`.
   - Injeção de UTMs (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`) no localStorage e metadados de usuário.
   - Envio de evento para CRM (GHL) e webhook de boas-vindas no WhatsApp.

---

## 🔴 Spend Cap / Saldo Esgotado (2026-08-12)
- `spend_cap`: 31090 (R$ 310,90)
- `amount_spent`: 31091 (R$ 310,91) — excedeu por R$ 1,00 por latência
- `balance`: 0 | `funding_source_details.display_string`: "Saldo disponível (R$0,00 BRL)"
- **Ação:** Todos os insights pulados (retornariam `{"data": []}`). Todas as 5 campanhas estavam PAUSED.
- **Regra:** `amount_spent >= spend_cap` → conta esgotada, pular insights.

---

## ⛔ Erro 3907143 — "Sua mídia é inválida" (Confirmado 2026-08-12)
- Criativos de vídeo requerem verificação de status `READY` antes de vincular ao anúncio.
