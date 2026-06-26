---
name: max-banking
version: 1.0.0
description: >
  ÚNICA ferramenta para ações financeiras da conta Max Bank. Use obrigatoriamente para:
  consultar saldo, fazer PIX (chaves ou QR Code Copia e Cola), pagar boletos e conectar conta.
  ATENÇÃO: Acione esta skill IMEDIATAMENTE e de forma proativa se o usuário enviar um código 
  PIX (texto começando com '00020...'), uma linha digitável de boleto (números longos), ou 
  uma imagem/foto contendo um QR Code ou código de barras, mesmo que ele não escreva nenhum 
  comando como "pagar" ou "fazer pix". Esta skill INCLUI a capacidade de extrair dados de 
  imagens localmente usando a ferramenta zbarimg via exec.
author: max-banking
metadata: {"openclaw":{"always":true}}
permissions:
  - network:outbound
  - exec
triggers:
  - pattern: "qual meu saldo"
  - pattern: "quanto tenho"
  - pattern: "ver saldo"
  - pattern: "consultar saldo"
  - pattern: "meu saldo"
  - pattern: "saldo maxbank"
  - pattern: "quero fazer um pix"
  - pattern: "fazer pix"
  - pattern: "quero pagar um boleto"
  - pattern: "pagar boleto"
  - pattern: "transferir"
  - pattern: "solicitação de pagamento"
  - pattern: "quero conectar minha conta max"
  - pattern: "conectar minha conta max"
  - pattern: "conectar conta max"
  - pattern: "conectar minha conta"
  - pattern: "configurar max"
  - pattern: "instalar max"
  - pattern: "qual conta conectada"
  - pattern: "conta conectada"
  - pattern: "qual conta"
  - pattern: "minha conta"
  - pattern: "extrato"
  - pattern: "saque"
  - pattern: "transferência"
  - pattern: "investir"
  - pattern: "cartão"
  - pattern: "qr code"
  - pattern: "qrcode"
  - pattern: "código de barras"
  - pattern: "foto do boleto"
  - pattern: "imagem do boleto"
  - pattern: "pagar isso"
  - pattern: "paga pra mim"
  - pattern: "pode pagar"
  - pattern: "lê esse"
  - pattern: "copia e cola"
  - pattern: "pix copia e cola"
  - pattern: "fazer o pagamento"
  - pattern: "000201"
  - pattern: "linha digitável"
  - pattern: "^[0-9\\.\\s]{40,55}$"
  - pattern: "\.(jpg|jpeg|png|webp)"
---

# Max Banking Skill

**Reconhecimento Proativo:** Se o usuário enviar APENAS um código começando com 000201... (PIX Copia e Cola), uma linha cheia de números (Boleto), **ou fizer o upload de uma imagem/foto**, NÃO pergunte o que ele quer fazer. 
- Se for texto: Assuma a intenção de pagamento e inicie o Workflow 2 ou 3.
- Se for imagem: Assuma que é um QR Code ou Boleto. VOCÊ TEM A CAPACIDADE de ler essa imagem. Imediatamente use a tool `exec` executando `zbarimg -q --raw CAMINHO_DA_IMAGEM` para extrair o código e, em seguida, siga com o pagamento. Nunca tente ler os números da imagem apenas olhando para ela; confie exclusivamente no retorno do `zbarimg`.

## REGRA #1 — PROIBIDO CONFIRMAR APÓS EXECUÇÃO (prioridade máxima)

**Os comandos `pix` e `billet` criam pagamentos REAIS no backend no instante em que o script roda.** Não existe simulação, rascunho ou prévia. Se o script rodou e retornou sucesso, o pagamento JÁ FOI CRIADO.

**Após qualquer execução bem-sucedida de `pix` ou `billet`:**

1. O pagamento JÁ EXISTE no sistema. Trate como FATO CONSUMADO.
2. Use APENAS verbos no passado: "registrei", "foi criado", "seu pedido foi gerado".
3. Oriente o usuário a APROVAR no WhatsApp ou no app (prazo de 48h).

**LISTA DE FRASES PROIBIDAS após execução bem-sucedida (nunca use nenhuma delas):**
- "deseja confirmar?"
- "confirma o pagamento?"
- "você gostaria de confirmar?"
- "posso prosseguir?"
- "posso efetuar?"
- "está pronto para ser pago"
- "você está prestes a pagar"
- "gostaria de prosseguir?"
- "quer que eu efetue?"
- Qualquer pergunta sim/não sobre o pagamento que já foi executado

**Se o usuário responder "sim" após você já ter informado o sucesso:** NÃO execute novamente. Responda: "O pedido já foi criado! Falta apenas aprovar no WhatsApp ou no app."

**Violação desta regra causa pagamento duplicado e prejuízo financeiro ao usuário.**

---

## Regras de comunicação (obrigatórias)

- **Respostas curtas e objetivas.** Evite textos longos; vá direto ao ponto.
- **PROIBIDO exibir ao usuário:** comandos, exemplos de formato técnico, nomes de parâmetros, scripts, IDs ou qualquer sintaxe de código. A resposta ao usuário deve ser 100% em linguagem natural.
- **Coleta de dados:** pergunte de forma natural. Para **chave PIX** (e-mail, CPF, telefone, chave aleatória): chave e valor. Para **PIX por QR** (código copia e cola que começa com `00020`): peça o código e **valide primeiro** com `pix-validate-qr`; o resultado indica se o QR já tem valor embutido ou se o usuário precisa informar.
- Após executar, responda de forma amigável. Nunca exiba saída técnica ou IDs brutos.
- Trate o usuário como cliente final: linguagem simples, sem jargão.
- **Comando inexistente:** se o usuário pedir algo que não existe (ex: transferência, saque, extrato, cartão), responda com a lista de ações disponíveis: *saldo*, *conta*, *setup*, *pix*, *billet*.
- **PIX e boleto:** colete o que a API exige antes de executar. **Chave PIX:** sem valor informado → pergunte o valor; nunca invente valor. **QR copia e cola:** valide primeiro com `pix-validate-qr`; se o QR não tem valor embutido (`has_amount=false` ou `amount=0`), pergunte o valor antes de criar o PIX. **Boleto:** só a linha/código.
- **Ao pedir PIX por chave**, em linguagem natural: "Informe a chave PIX e o valor em reais." (chave = CPF, e-mail, celular ou chave aleatória.) Se o usuário disser que vai pagar **por QR/código colado**, peça que cole o código — a validação determinará se precisa de valor.

## Quando usar

Quando o usuário pedir para consultar saldo, fazer PIX, pagar boleto, ou conectar/configurar a conta Max Bank.

## Como executar

Todas as ações usam a tool `exec`. O comando base a ser utilizado é **APENAS** `bash` seguido do caminho completo do script (não abrevie o caminho do arquivo `.sh`).

> **ATENÇÃO AO COMANDO BASH:** Cada sistema operacional usa um caminho específico para o executável do bash (como `/bin/bash`, `/usr/bin/bash` ou `/opt/homebrew/bin/bash`). Não tente adivinhar o caminho absoluto do bash; **normalmente utilizar apenas a palavra `bash` funciona** perfeitamente e resolve o caminho no ambiente.

```bash
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh ACAO [ARGUMENTOS]
```

Ações válidas: `saldo`, `conta`, `setup`, `pix-validate-qr`, `pix`, `billet`.
Ações que NÃO existem: connect, auth, install, configure, balance, pix-criar.

**Regra crítica (uso interno da IA) — PIX:**

- **Chave PIX:** dois argumentos posicionais — `CHAVE` e `VALOR`.
- **QR copia e cola** (payload que começa com `00020`): **sempre validar primeiro** com `pix-validate-qr`, depois criar com `pix`. Se o QR não tem valor embutido, informar `amount` ao criar.
- **QR com espaços no texto:** o EMV copia e cola pode conter espaços (ex.: nome fantasia, cidade). No `exec` com bash, o código inteiro deve ser **um único argumento** — use **aspas simples** em volta do payload (recomendado) ou `code='...'` / `code="..."` em uma única string. Sem aspas, o shell quebra o código em várias palavras e a validação ou o PIX falham.

```bash
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh pix email@teste.com 50
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh pix-validate-qr '000201263...texto com espaços...6304'
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh pix '000201263...texto com espaços...6304' 150.00
```

Formato nomeado (uso interno): `code=...` e, se for chave PIX ou QR sem valor, `amount:VALOR`. Com QR longo ou com espaços, prefira `code='...'` entre aspas.

**Validação de QR (`pix-validate-qr`):** retorna JSON com campos:
- `has_amount` — `true` se o QR tem valor embutido > 0
- `amount` — valor em reais do QR (0 se sem valor)
- `can_modify_final_amount` — `true` se o pagador pode/deve definir o valor
- `pix_key` — chave PIX de destino
- `qr_type` — tipo do QR
- `expiration_date` — validade do QR (quando existir)

**Boleto — um único argumento para a API:** a tool `banking_billet` recebe **somente** `code` (linha digitável ou código de barras). O script deve repassar **apenas um** argumento ao `mcporter` (ex.: `code=<linha completa>` ou posicional que vira um único `code=...`). **Nunca** envie segundo parâmetro nomeado (valor, amount, descrição, etc.) — o backend responde 422.

Formatos válidos (equivalentes para "um argumento lógico"):
```bash
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh billet LINHA_OU_CODIGO
```
(se a linha tiver espaços, o shell junta as palavras em um único `code=` internamente)

```bash
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh billet code=LINHA_OU_CODIGO
```

Se aparecer `BILLET_TOO_MANY_ARGS` na saída, a IA enviou parâmetros a mais: corrija para **só** a linha/código, um `code=` ou posicional único.

**PROIBIDO adicionar parâmetros extras** (descrição, motivo, mensagem, etc.). Boleto: nunca envie `amount` ou valor extra — só `code`. PIX: para **chave**, chave + valor; para **QR `00020…`**, valide primeiro e envie `amount` apenas se o QR não contiver valor. Não pergunte ao usuário por descrição.

O usuário NUNCA deve ver detalhes de execução — isso é exclusivo para uso interno.

## Leitura de QR e código de barras a partir de imagem (uso interno)

Quando o usuário enviar **foto, captura de tela ou arquivo** de um PIX (QR) ou boleto, o texto do código pode ser obtido com a ferramenta **zbar** (`zbarimg`), instalada pelo `setup.sh` conforme o sistema operacional (macOS: Homebrew `zbar`; Debian/Ubuntu: `zbar-tools`; Fedora: `zbar`; Arch: `zbar`; Alpine: `zbar`; openSUSE: `zbar`).

1. Obtenha o caminho absoluto do arquivo de imagem (upload, anexo ou caminho informado).
2. Execute com a tool `exec` (uso interno — não mostre ao usuário):
   ```bash
   zbarimg -q --raw CAMINHO_DA_IMAGEM
   ```
   Se houver várias linhas na saída, use a que for **payload PIX** (começa com `000201`) para PIX; para boleto, prefira a **linha digitável** (só dígitos e espaços/pontos no padrão de boleto) ou o código de barras decodificado que corresponda à linha.
3. **PIX:** trate o texto extraído como **código único**. Se for QR copia-e-cola (`00020…`), siga o Workflow 2 (fluxo QR) — valide primeiro, peça valor se necessário, depois crie.
4. **Boleto:** trate o texto extraído (linha digitável ou código de barras convertível) como o **único** argumento de `billet` (Workflow 3).
5. Se `zbarimg` não estiver instalado ou não decodificar nada, peça ao usuário que digite a linha digitável ou cole o código PIX manualmente, ou que rode o setup novamente para instalar o leitor.

Não invente dados a partir da imagem além do que `zbarimg` retornar; se a leitura falhar, não tente "adivinhar" o código.

## Workflow 1 — Consultar saldo

Condição: usuário pede "qual meu saldo", "quanto tenho", "ver saldo".

1. Execute com a tool `exec`:
   ```bash
   bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh saldo
   ```
2. Leia o campo `available_balance_cents` do retorno.
3. Divida por 100 para converter centavos em reais.
4. Responda: "Seu saldo disponível é R$ X.XXX,XX".

### Erro no saldo

Se retornar erro (401, "pairing not done", "connection refused", "agent_key invalid"):
1. Responda: "Sua conta Max não está conectada ou a sessão expirou."
2. Pergunte o código de pareamento (formato XXXX-XXXX) e o ambiente (prod, homolog ou local).
3. Siga o Workflow 4 para conectar.

## Workflow 2 — Fazer PIX

Condição: usuário pede "quero fazer um pix", "transferir", pagar por QR, etc.

**Dois fluxos distintos:**

| Tipo | O que coletar | Quando executar |
|------|----------------|-----------------|
| **Chave PIX** (CPF, e-mail, telefone, chave aleatória — não é payload `00020…`) | Chave **e** valor em reais | Só após ter os dois |
| **QR copia e cola** (texto longo começando com `00020`) | O código colado; **valor se o QR não tiver** | Após validar o QR e ter o valor (se necessário) |

### Fluxo Chave PIX

1. Identifique que é fluxo chave (texto não começa com `00020`). Pergunte APENAS o que falta:
   - **Chave + valor na frase** (ex: "PIX de 50 reais para email@teste.com"): execute uma vez (passo 2), sem segunda confirmação.
   - **Só valor** (ex: "PIX de 50 reais"): pergunte a chave.
   - **Só chave** (ex: "PIX para maria@email.com"): pergunte o valor.
   - **PROIBIDO:** mostrar exemplos técnicos, nomes de parâmetros, sintaxe de comando ou formato de código ao usuário.
   - **PROIBIDO:** perguntar por descrição, motivo ou mensagem.
   - **Valor:** nunca invente. Sem valor informado → pergunte.
2. **Execute `pix` uma única vez** quando tiver chave e valor. Nunca mostre detalhes de execução ao usuário.

### Fluxo QR copia e cola (OBRIGATÓRIO validar antes de criar)

1. Identifique que é fluxo QR (código começa com `00020`). Se o usuário quer pagar por QR mas ainda não colou o código, peça para colar.
2. **Valide o QR primeiro** — execute internamente (payload completo entre aspas se houver espaços):
   ```bash
   bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh pix-validate-qr 'CODIGO_QR_COMPLETO'
   ```
3. **Analise o retorno da validação:**
   - Se `has_amount=true` e `amount > 0`: o QR já tem valor embutido. Informe ao usuário o destinatário (pix_key) e o valor, e prossiga para criar o PIX **sem pedir valor**.
   - Se `has_amount=false` ou `amount=0`: o QR **não tem valor embutido**. Pergunte ao usuário qual o valor em reais antes de prosseguir.
   - Se `can_modify_final_amount=true` e `amount > 0`: o QR tem um valor sugerido mas o pagador pode alterar. Informe o valor e pergunte se deseja usar esse valor ou informar outro.
4. **Crie o PIX** — execute internamente (mesma regra de aspas para o código quando tiver espaços):
   - QR com valor embutido: `pix 'CODIGO_QR'` (sem amount)
   - QR sem valor / valor informado pelo usuário: `pix 'CODIGO_QR' VALOR`
5. **Se erro na validação (422):** informe que o QR pode estar inválido ou expirado e peça que confira.

### Resposta após criação (ambos os fluxos)

- **REGRA #1 se aplica aqui (releia se necessário).**
- O PIX JÁ FOI CRIADO. Use obrigatoriamente verbos no passado.
- Modelo: **"Registrei um PIX de R$ [valor] para [destinatário]. Para concluir, aprove no WhatsApp ou no app em até 48h."** (use o valor retornado pela execução quando disponível.)
- **PROIBIDO** perguntar "deseja confirmar?", "posso prosseguir?", ou qualquer variação. Isso causa DUPLICIDADE.
- Se o usuário responder "sim" depois: NÃO execute de novo. Diga que o pedido já foi criado e falta aprovar no WhatsApp/app.

### Erros

- **Se PIX_INVALID_ARGS:** no fluxo chave, faltou chave ou valor — pergunte o que falta. No fluxo QR, faltou o código — peça para colar o código completo.
- **Se erro 401/403:** informe que a conta não está conectada e ofereça reconectar (Workflow 4).
- **Se erro 422:** informe que a chave ou QR pode estar inválido e peça que confira.

## Workflow 3 — Pagar boleto

Condição: usuário pede "quero pagar um boleto", "pagar boleto".

1. **Colete a linha digitável (ou código de barras).** Pergunte de forma natural. Nunca mencione "code" ou detalhes técnicos ao usuário.
2. **Execute uma única vez** quando tiver a linha/código e o pedido de pagamento for claro. **Um argumento só** para `billet` — a linha inteira (ou posicional com as partes que o shell junta). Nunca mostre detalhes de execução ao usuário.
3. **Resposta de sucesso — REGRA #1 se aplica aqui (releia se necessário):**
   - O pagamento JÁ FOI CRIADO. Não é prévia, não é rascunho, não é simulação.
   - Use OBRIGATORIAMENTE este modelo (adapte valores):
     **"Registrei o pagamento do boleto de R$ [valor] para [beneficiário] (venc. [data]). Para concluir, aprove no WhatsApp ou no app em até 48h."**
   - **PROIBIDO** após exec com sucesso: perguntar "deseja confirmar?", "gostaria de prosseguir?", "está pronto para ser pago", ou qualquer pergunta sim/não sobre o pagamento. Isso causa DUPLICIDADE.
   - **PROIBIDO** apresentar os dados do boleto como prévia e depois pedir confirmação. Os dados devem ser apresentados como PARTE DA CONCLUSÃO do pagamento já criado.
   - Se o usuário responder "sim" depois: NÃO execute de novo. Diga que o pedido já foi criado e falta aprovar no WhatsApp/app.
4. **Se BILLET_INVALID_ARGS ou BILLET_TOO_MANY_ARGS:** faltou linha ou a IA passou parâmetros a mais. Corrija para **apenas** a linha digitável/código (sem amount, valor extra, etc.) e execute de novo **uma vez**.
5. **Se erro 401/403:** informe que a conta não está conectada e ofereça reconectar (Workflow 4).
6. **Se erro 422:** informe que o boleto pode estar expirado ou inválido e peça que confira.

## Workflow 4 — Conectar conta

Condição: usuário pede "conectar minha conta", "configurar max", "instalar max", ou o Workflow 1 retornou erro.

### Assinatura do comando

```bash
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh setup <CODIGO> <AMBIENTE> [URL_MCP]
```

A ordem dos argumentos é FIXA e OBRIGATÓRIA: **1º código, 2º ambiente, 3º URL (só para local).**

### Extração dos dados da mensagem do usuário

O usuário pode informar tudo numa única frase. Extraia os 3 dados abaixo da mensagem:

| Dado | Como identificar | Exemplos |
|------|-----------------|----------|
| **CODIGO** | Sequência alfanumérica curta, geralmente com hífen | `ABC-123`, `AX7K-92QF`, `ABCD-EF12` |
| **AMBIENTE** | Uma das palavras: `prod`, `homolog`, `local` | "ambiente local", "em prod", "homolog" |
| **URL_MCP** | URL completa (começa com `http://` ou `https://`) | `https://xxx.ngrok-free.app/mcp` |

**Se a URL foi informada mas o ambiente não foi mencionado explicitamente, assuma `local`** (só ambiente local usa URL customizada).

**Se nenhum ambiente foi mencionado e não há URL, assuma `prod`.**

**Produção:** o `setup.sh` usa o MCP em `https://maxbank-mcp.max.com.br/mcp`. Disponibilidade do serviço: `https://maxbank-mcp.max.com.br/health`.

Pergunte APENAS o que não conseguir extrair da mensagem:
- Sem código → "Qual o código de pareamento? (formato XXXX-XXXX)"
- Sem ambiente e sem URL → "Qual ambiente? (prod, homolog ou local)"
- Ambiente `local` sem URL → "Qual a URL do MCP? (ex: [https://xxx.ngrok-free.app/mcp](https://xxx.ngrok-free.app/mcp))"

### Após executar

1. Leia o output. Procure `PHONE=` e `ENV=` nas linhas de saída.
2. Responda ao usuário com este formato (troque PHONE pelo número extraído):

   Conta *Max* conectada com sucesso!
   - Conta conectada: *PHONE*
   Agora você pode realizar ações de busca de saldo, pagamento de PIX e boletos.

   Se ENV contiver "teste", adicione no final: _(Ambiente de testes)_
3. Não adicione emojis. Não mostre caminhos, secrets, portas ou dados internos.

## Workflow 5 — Qual conta está conectada

Condição: usuário pergunta "qual conta conectada", "qual minha conta", "conta conectada".

1. Execute com a tool `exec`:
   ```bash
   bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh conta
   ```
2. Se o output contiver `NO_ACCOUNT`:
   Responda: "Nenhuma conta Max está conectada. Deseja conectar agora?"
   Se sim, siga o Workflow 4.
3. Se o output contiver `ACCOUNT_OK`:
   Extraia PHONE, ENV e PAIRED_AT do output.
   Converta PAIRED_AT para formato legível (ex: "25 de fevereiro de 2026 às 14:30").
   Responda com este formato:

   Conta *Max* conectada:
   - Telefone: *PHONE*
   - Ambiente: *ENV*
   - Conectada em: *DATA_FORMATADA*

   Se ENV for "local" ou "homolog", adicione: _(Ambiente de testes)_
4. Não adicione emojis. Não mostre caminhos, secrets, portas, PIDs ou dados internos.

## Exemplos completos de conversa

**REGRA:** nos exemplos abaixo, a resposta da IA é EXATAMENTE o que deve ser exibido ao usuário. Nunca adicione nomes de parâmetros, sintaxe de comando ou qualquer detalhe técnico.

### Saldo

Usuário: "qual meu saldo?"
→ IA: "Consultando seu saldo..." → executa internamente → "Seu saldo disponível é R$ X.XXX,XX"

### PIX — todos os cenários

**Cenário 1: sem nenhum dado**
Usuário: "Quero fazer um PIX"
→ IA: "Claro! Você vai pagar com chave PIX (CPF, e-mail, celular ou chave aleatória) ou colando o código do QR copia e cola?"

**Cenário 2: só o valor, fluxo chave**
Usuário: "Quero fazer um PIX de 50 reais"
→ IA: "Para qual chave PIX? (e-mail, CPF ou telefone)"

**Cenário 3: só a chave, sem valor (fluxo chave)**
Usuário: "Quero fazer um PIX para maria@email.com"
→ IA: "Qual o valor em reais?"

**Cenário 4: chave e valor na mesma frase**
Usuário: "PIX de 5 reais para vinicius.matteus@maxbank.ai"
→ IA executa internamente uma vez (pedido explícito com chave e valor) → "PIX de R$ 5 criado para [nome do destinatário]. Aprove no WhatsApp ou no app em até 48h."

**Cenário 5: usuário informa a chave depois (fluxo chave)**
Usuário: "vinicius.matteus@maxbank.ai"
→ IA: "Qual o valor em reais?"

**Cenário 6: QR copia e cola com valor embutido**
Usuário cola o payload que começa com `00020` (código completo)
→ IA valida internamente com `pix-validate-qr` → retorno indica `has_amount=true`, `amount=150.00` → IA cria o PIX internamente com `pix` (sem pedir valor) → "Registrei um PIX de R$ 150,00 para [destinatário]. Aprove no WhatsApp ou no app em até 48h."

**Cenário 7: QR copia e cola SEM valor embutido**
Usuário cola o payload que começa com `00020` (código completo)
→ IA valida internamente com `pix-validate-qr` → retorno indica `has_amount=false`, `amount=0` → IA pergunta: "O QR não contém valor. Qual o valor em reais que deseja transferir?"
Usuário: "200 reais"
→ IA cria o PIX com `pix 'CODIGO_QR' 200` (aspas se o EMV tiver espaços) → "Registrei um PIX de R$ 200,00 para [destinatário]. Aprove no WhatsApp ou no app em até 48h."

**Cenário 8: QR com valor modificável**
Usuário cola o payload que começa com `00020`
→ IA valida internamente → retorno indica `has_amount=true`, `amount=50.00`, `can_modify_final_amount=true` → IA informa: "O QR sugere R$ 50,00. Deseja usar esse valor ou prefere informar outro?"
Usuário: "Pode ser esse mesmo"
→ IA cria o PIX com `pix 'CODIGO_QR'` (usa o valor do QR; aspas se o EMV tiver espaços) → "Registrei um PIX de R$ 50,00 para [destinatário]. Aprove no WhatsApp ou no app em até 48h."

### Boleto

Usuário: "quero pagar um boleto"
→ IA: "Certo! Preciso da linha digitável ou do código de barras do boleto."

Usuário fornece a linha digitável
→ IA executa internamente **uma vez** → responde OBRIGATORIAMENTE como conclusão:
**CORRETO:** "Registrei o pagamento do boleto de R$ 393,22 para AMBIEENTE HOMOLOGACAO (venc. 26/03/2026). Para concluir, aprove no WhatsApp ou no app em até 48h."
**ERRADO (nunca faça isso):** "O boleto no valor de R$ 393,22 está pronto para ser pago. Deseja confirmar?" — isso causa pagamento duplicado.

Usuário: "sim" (após IA já ter informado sucesso)
→ IA: "O pedido já foi criado! Falta apenas aprovar no WhatsApp ou no app." — **NUNCA** executar o script de novo.

### Ação inexistente

Usuário: "quero ver meu extrato" / "fazer saque" / "transferência"
→ IA: "Essa ação não está disponível. Você pode: consultar saldo, ver conta conectada, fazer PIX, pagar boleto ou conectar conta."

## Workflow 6 — Comando inexistente

Condição: usuário pede ação que não existe (extrato, saque, transferência bancária, cartão, investimentos, etc.).

Responda de forma curta e objetiva:
"Essa ação não está disponível no Max no momento. Você pode: consultar *saldo*, ver *conta* conectada, fazer *PIX*, pagar *boleto* ou *conectar* uma conta."

## Dados de sessão

A conta conectada persiste em `~/.openclaw/secrets/maxbank/session.json`.
Após conectar uma vez, o saldo e pagamentos funcionam em sessões futuras sem reconectar.