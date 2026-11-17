# Padrão de Nomenclatura Oficial (Start Company / Evandro Santos)

Este documento define a taxonomia rigorosa e oficial para Campanhas, Conjuntos de Anúncios (Ad Sets) e Anúncios (Criativos) no Meta Ads.

---

## 🏛️ HIERARQUIA DE NOMENCLATURA (3 NÍVEIS)

### 1. Nível 0 — Campanha
**Fórmula:**
`[TAG] {NUM} [{OBJETIVO}] {ESTRUTURA}_{ORÇAMENTO}_[{OFERTA}] – {DATA}`

* **`[TAG]`**: Identificador da empresa / produto (ex: `[START]`, `[PAPI]`).
* **`{NUM}`**: Sequencial da campanha (`001`, `002`, `010`).
* **`[{OBJETIVO}]`**: `[ENG-MSG]` (Engajamento/Mensagem), `[CONV-PURCHASE]` (Conversão/Compra), `[LEADS]`, `[TRAFEGO]`.
* **`{ESTRUTURA}`**: Arquitetura da campanha (ex: `1-1-1`, `1-2-8`, `1-10-10`).
* **`{ORÇAMENTO}`**: `CBO` (Campaign Budget Optimization) ou `ABO` (Ad Set Budget Optimization).
* **`[{OFERTA}]`**: Modelo comercial (ex: `[ONETIME]`, `[RECORRENTE]`, `[PERPETUO]`, `[LANCAMENTO]`).
* **`{DATA}`**: Data de criação no formato `DD.MM.AA`.

*Exemplo:* `[START] 001 [ENG-MSG] 1-1-1_CBO_[ONETIME] – 16.06.26`

---

### 2. Nível 1 — Conjunto de Anúncios (Ad Set)
**Fórmula:**
`{CAMPANHA}.{SUB}_[{POS}]_({GENERO}_{IDADE})_{INTERESSES}_{GEO}_{DATA}`

* **`{CAMPANHA}.{SUB}`**: Índice hierárquico (ex: `001.01`, `001.02`, `002.01`).
* **`[{POS}]` (Posicionamento):**
  * `[AUTO]`: Posicionamento Automático (Advantage+ Placements / Todos).
  * `[FB/IG]`: Feed/Stories de Facebook e Instagram.
  * `[IG]`: Somente Instagram.
  * `[FB]`: Somente Facebook.
* **`{GENERO}_{IDADE}` (Demografia):**
  * `H-M_20-55`: Homens e Mulheres de 20 a 55 anos.
  * `H_25-50`: Somente Homens de 25 a 50 anos.
  * `M_18-40`: Somente Mulheres de 18 a 40 anos.
* **`{INTERESSES}` (Segmentação):**
  * Resumo conciso dos interesses. Se houver mais de 4 ou 5 interesses, incluir no **máximo 2 termos principais** para manter o nome limpo (ex: `Devs-Software`, `IA-Automacao`).
* **`{GEO}` (Geolocalização):**
  * País ou Praça regional (ex: `BR`, `SP`, `POA`, `RJ`, `MG`).
* **`{DATA}`**: Data de criação no formato `DD.MM.AA`.

*Exemplos:*
* `001.01_[AUTO]_H-M_20-55_Devs-Software_BR_08.09.26`
* `001.02_[AUTO]_H-M_22-65_IA-Automacao_BR_08.09.26`

---

### 3. Nível 2 — Anúncio (Criativo Individual / Vídeo)
**Fórmula:**
`Ad{NUM} - {HEADLINE} | {PREÇO} | {VARIAÇÃO/COR}`
*(Exemplos: `Ad01`, `Ad02`, `Ad03`, `Ad04` ou `Ad001`, `Ad002`, `Ad003`, `Ad004`)*

> **Regras Fundamentais de Anúncios:**
> 1. **Prefixo sem espaço:** Escrever sempre colado: `Ad01` / `Ad001`, `Ad02` / `Ad002`... (nunca `Ad 01` ou `AD 01`).
> 2. **Sem poluição de hierarquia longa:** Não colocar prefixos gigantescos de campanha/conjunto (`001.01.001_...` é proibido).
> 3. **Numeração Única e Estritamente Sequencial:** Cada anúncio veiculado recebe o próximo número da sequência (`Ad01`, `Ad02`, `Ad03`, `Ad04`...). **NUNCA repetir o mesmo prefixo de numeração.**
> 4. **Variações / Versões do Mesmo Criativo:** Se houver uma versão 2 de um criativo, **ela NÃO usa sufixo `-v2` no mesmo ID**. Ela avança para o próximo número da sequência (ex: Criativo 1 v1 = `Ad01`; Criativo 1 v2 = `Ad02`; Criativo 2 = `Ad03`; Criativo 3 = `Ad04`).
> 5. **Análise do Criativo / Vídeo (Headline):** Analisar o criativo e extrair a Headline principal (redline) como nome central do anúncio.
> 6. **Preço (se houver na oferta/arte):** Incluir o valor ou condição comercial (ex: `R$ 14,90`, `R$ 49,90`, `50% OFF`).
> 7. **Variação Visual / Cor / Formato:** Indicar cor, formato ou ângulo caso haja variações do material (ex: `Amarelo`, `Azul`, `Vídeo`, `V2 - Azul`).
> 8. **Aprovação Prévia Mandatória:** Sempre apresentar tabela com a proposta de nomes antes de executar alterações na API.

*Exemplos de Nomes de Anúncios:*
* `Ad01 - WhatsApp API Oficial | R$ 14,90 | Amarelo` (Criativo 1 - Versão 1)
* `Ad02 - WhatsApp API Oficial | R$ 14,90 | Azul / V2` (Criativo 1 - Versão 2)
* `Ad03 - Chamada Voz com IA | R$ 49,90 | Base` (Criativo 2 - Versão 1)
* `Ad04 - Agente IA para Empresas | R$ 49,90 | Vídeo` (Criativo 3)Agente de Voz IA 24/7 | R$ 49,90 | AIDA`
* `Ad003 - Conecte n8n ao WhatsApp Oficial | Sem Bloqueio | Vídeo`

---

## 🧪 Metodologia de Teste e Mensuração
* A hierarquia em 3 níveis garante clareza absoluta na leitura do Gerenciador de Anúncios do Meta.
* O Nível 0 identifica a macroestratégia e modelo comercial.
* O Nível 1 isola demografia, posicionamento, interesses e praça.
* O Nível 2 permite auditoria visual imediata de criativos, headlines e ofertas sem truncamento na tela.
