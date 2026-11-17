# Fluxo de gestão delegada do agent e contrato do script — powpow-register

Detalhes de execução de cada etapa do SKILL.md. Todos os comandos são `node scripts/powpow-register.mjs <subcomando> [parâmetros]`,
o script é **zero dependências** e requer **Node ≥ 18**; todas as requisições vão apenas para `https://global.powpow.online`.

## Design de segurança (por que é assim)

| Design | Razão |
|---|---|
| A senha só entra pela variável de ambiente `POWPOW_REGISTER_PASSWORD` | Os argumentos de linha de comando de um processo ficam visíveis para os demais processos da mesma máquina (superfície de vazamento do argv); a variável de ambiente é lida dentro do script e usada na hora |
| A senha **jamais é escrita no arquivo de estado**, jamais aparece nos logs | O arquivo de estado pode permanecer no disco; no modo geração ela só é exibida uma vez para o usuário salvar |
| O arquivo de estado fica no diretório temporário do sistema (`os.tmpdir()/powpow-register-state.json`, 0600) | Contém apenas os cinco campos email / username / nickname / token / outTradeNo; o `cleanup` apaga tudo de uma vez |
| O JWT que o agent recebe é trocado por um cookie de navegador pelo endpoint oficial `me?token=` | É a ponte oficial desenhada pela plataforma para o WebView do HarmonyOS; a verificação confere só assinatura + validade, sem amarrar à impressão digital do aparelho, logo o navegador do usuário serve |
| O pagamento só faz create-order / query / abrir o caixa | O ato de pagar e as credenciais de pagamento ficam sempre entre o usuário e o caixa oficial do Alipay; o agent não pega neles |

## Referência de comandos

| Comando | Parâmetros-chave | O que faz / quando |
|---|---|---|
| `status` | —— | Ver o progresso do fluxo (lê o arquivo de estado); depois de uma conversa interrompida, rode isto primeiro |
| `gen-password` | —— | Gera uma senha forte de 24 caracteres (maiúsculas + minúsculas + números); o stdout exibe **só esta uma vez** |
| `prepare-suggest` | `--username --nickname --email` | Anota no arquivo de estado as informações confirmadas (depois o register não pede de novo) |
| `send-code` | `--email` | Dispara o envio pela plataforma do código de verificação de 6 dígitos (válido 10 minutos, espera de 60s) |
| `register` | `--code` (obrigatório); `--username --nickname --avatar --phone` (opcionais, dispensados se já estão no arquivo de estado) | Cria a conta pending; a senha vai pela variável de ambiente `POWPOW_REGISTER_PASSWORD`; após o sucesso o JWT é guardado automaticamente no arquivo de estado |
| `login-link` | `--target pending` ou `--target home` | Gera um link de login com um clique (design de link duplo, veja abaixo) |
| `create-order` | `--package monthly\|quarterly\|yearly` (Alipay é o padrão)<br>`--provider alipay\|paypal` | Cria o pedido de pagamento; o Alipay devolve o caminho do arquivo da página de pagamento + outTradeNo; o PayPal devolve o caminho do arquivo da página de autorização + subscriptionId (gravado automaticamente no arquivo de estado) |
| `query` | —— | Consulta o estado do pedido/assinatura. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; consulta a cada 10–15s |
| `refresh-login` | Senha por variável de ambiente | Faz login de novo e troca por um **JWT novo** (a declaração de assinatura passa de NONE para ACTIVE); obrigatório depois que o pagamento cai |
| `whoami` | —— | Consulta com o token do arquivo de estado o estado da conta e da assinatura (verificar se a ativação valeu) |
| `cleanup` | —— | Apaga o arquivo de estado (obrigatório no encerramento) |

**Passagem da variável de ambiente** (a senha jamais vai para a linha de comando):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<senha>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<senha>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<senha> && node scripts/powpow-register.mjs register --code 123456
```

## Mecanismo de link duplo (design central)

O estado de login da plataforma é um cookie HttpOnly, que o agent não pode plantar diretamente no navegador; a ponte é o endpoint oficial
`/api/auth/me?token=<JWT>&redirect=<caminho interno>`: verificar assinatura → criar sessão automaticamente
→ `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 dias) → validar
o redirect (deve começar com uma única barra, `//` e barras invertidas proibidos, mesma origem após o parse) → 307 redirecionamento temporário para a página de destino.

Há dois destinos de link, **gere primeiro o home e decida se passa pelo pending conforme onde o usuário cair**:

- **link home (enviado por padrão primeiro, `--target home` → cai em `/`)**: gerado e enviado ao usuário imediatamente após o registro bem-sucedido.
  Durante o período de teste gratuito o usuário entra direto na página inicial, tudo utilizável; **se o usuário abrir e cair na página de assinatura, o período de teste gratuito acabou** — mude então para o caminho de pagamento (veja abaixo); sem mudar o script e sem se registrar de novo.
- **link pending (usado no caminho de pagamento, `--target pending` → cai em `/subscription`)**:
  o navegador do usuário entra em estado de «meio-login»: a página de assinatura e a página de retorno do pagamento ficam visíveis e operáveis. Após o recebimento,
  execute `refresh-login` para trocar por um novo JWT com a declaração ACTIVE e envie o link home mais uma vez para a associação completa.

## Sequência completa

### Caminho rápido (durante o período de teste gratuito — a grande maioria dos casos)

```
1.  status                          # autoverificação do ambiente
2.  (Passo 2 conversa para confirmar as informações, senha a escolher; modo gerado: gen-password → fazer o usuário salvar na hora)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → usuário consulta o código no e-mail (a única saída da conversa)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → envie o link ao usuário; um clique e ele está na página inicial
7.  (usuário confirma que entrou) → encerre direto: cleanup + cartão da conta + guia dos primeiros passos
```

### Caminho de pagamento (quando o usuário quer associação, ou o período de teste gratuito acabou)

```
1–5. Igual ao caminho rápido (o state já tem o token depois do register bem-sucedido)
6.  login-link --target pending     # → link de meio-login, mantém a página de retorno do pagamento funcionando
7.  (usuário escolhe o método de pagamento)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <arquivo da página de pagamento>   # Windows; macOS usa open, Linux usa xdg-open
    # → usuário conclui o pagamento/autorização no caixa do Alipay/PayPal (sai da conversa)
9.  query (a cada 10–15 s) até paid / ACTIVE
10. refresh-login                   # troca por um novo JWT com a declaração ACTIVE
11. login-link --target home        # → envie o link de associação completa ao usuário
12. whoami                          # confirmar subscriptionStatus: ACTIVE (opcional)
13. cleanup                         # limpa o arquivo de estado
```
## Mapeamento comando → API da plataforma

| Comando do script | Interface da plataforma |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, upload direto do avatar) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (o link em si, vale ao ser clicado no navegador) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Origem das regras: campos de registro e limites de frequência em `registration-flow.md`; planos e cadeia de ativação em
`payment-and-activation.md` (ambos citam os arquivos do código-fonte da plataforma).

## Tratamento de erros a nível de script

| Sintoma | Tratamento |
|---|---|
| `Versão do Node baixa demais` | Recue para o modo de orientação pura, não force |
| Erro de rede / timeout | Tente uma vez de novo; se continuar falhando, o usuário verifica a rede e segue (o arquivo de estado continua lá; recupere rodando `status` desde o início) |
| register devolve erro de negócio (nome de usuário já existe etc.) | Trate pela tabela da etapa 5 do SKILL.md, **não é preciso reenviar o código de verificação** (continua válido por 10 minutos) |
| register devolve 「邮箱验证码错误或已过期」 (código de verificação errado ou expirado) | Tempo esgotado → rodar `send-code` de novo |
| O usuário fechou a página de pagamento depois do `create-order` | Rode `create-order` de novo direto (o pedido antigo fecha sozinho em 2h; assinaturas PENDING do PayPal expiram em 1h) |
| `create-order --provider paypal` devolve 409 | Já existe uma assinatura PayPal não concluída; espere 1h para expirar ou conclua a autorização antiga no navegador |
| `query` fica em pending / PENDING | O usuário talvez não tenha pago; pergunte. Se pagou mesmo → siga a tabela de diagnóstico do payment-and-activation.md |
| O usuário abre o link home mas cai na página de assinatura | O período de teste gratuito acabou → mude para o caminho de pagamento: `login-link --target pending` → escolha um método de pagamento → `create-order` |
| `refresh-login` 403 `pending_payment` | O período de teste gratuito acabou e o pagamento ainda não foi recebido; volte ao passo 9 para continuar consultando, ou confirme se o usuário concluiu o pagamento |
| Arquivo de estado perdido (apagado sem querer / troca de máquina) | `whoami`/`refresh-login` ficam inutilizáveis; o usuário atualiza direto a página de assinatura no navegador onde abriu o link 1 para confirmar o estado, ou faz login de novo (modo web) |

## Modo de recuo (orientação pura)

Em qualquer destas situações, recue imediatamente para a orientação pura estilo v1 e pare de insistir com o script:

- Não há Node ≥ 18, ou o script falha duas vezes seguidas na mesma coisa;
- O usuário diz claramente «eu mesmo faço na página web»;
- Políticas da empresa / do aparelho restringem scripts de rede.

Após voltar ao modo guia: dê a página de registro https://global.powpow.online/register (durante o período de teste gratuito, o registro web é igualmente imediato; quando uma assinatura for necessária, dê também a página de assinatura https://global.powpow.online/subscription ), acompanhe a solução conforme as regras de `registration-flow.md`, mantenha o mesmo tom e encerre cada turno com um bloco de «próximo passo».
https://global.powpow.online/subscription, acompanhe na resolução de erros pelas regras de
`registration-flow.md`, mantenha o tom e feche cada rodada com o bloco de «próximo passo».
