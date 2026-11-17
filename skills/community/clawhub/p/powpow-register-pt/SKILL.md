---
name: powpow-register
description: Ajuda os usuários a concluir o registro do PowPow (Bolha) e o login com um clique dentro da conversa. O agent preenche o formulário por eles (incluindo o upload do avatar) e envia o código de verificação por e-mail; o usuário só fornece informações básicas e consulta o código uma vez, sem sair da conversa. Durante o período atual de teste gratuito da plataforma, uma conta registrada pode usar todos os recursos imediatamente; o pagamento da assinatura (Alipay/PayPal) é uma melhoria de associação opcional, que o agent também pode cuidar com criação de pedido e rastreamento do recebimento quando necessário. Dispara quando o usuário diz «registrar na Bolha», «criar uma conta powpow», «como me registro na Bolha», «me ajude a criar uma conta powpow», «sign up powpow»; também trata de travamentos no registro (código de verificação não recebido, nome de usuário/e-mail já ocupados) e problemas de ativação (o login diz «conta não ativada» / pending_payment, como assinar/pagar, a Bolha é grátis?). Requer Node ≥ 18; volta automaticamente ao modo de guia puro quando indisponível. Não cobre publicar/criar humanos digitais (isso é coisa do powpow-simple) nem desenvolvimento de código.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (assistente de registro na Bolha)

Leva um usuário novo de «não sei o que é a Bolha» a «login com um clique, pronto para começar» — tudo dentro da conversa. O usuário só sai da conversa uma vez: **para consultar o código de verificação no e-mail**. A plataforma está atualmente em um período de teste gratuito: uma vez registrado, todos os recursos estão disponíveis, sem necessidade de pagar; o pagamento da assinatura é uma melhoria de associação opcional (o agent também abre o caixa e rastreia o recebimento).

**Versão 2.2.0** · 2026-10-18 (desde a v2 este é o modo assistido por agent: contrato do script e sequência completa em `references/agent-flow.md`; regras de campos, limites de taxa e solução de erros em `references/registration-flow.md`; canais de pagamento em `references/payment-and-activation.md`; lista de capturas de produto em `references/screenshots.md`. Desde a v2.1.0 as assinaturas PayPal também podem ser gerenciadas pelo agent, como opção ao lado do Alipay. Desde a v2.2.0 a plataforma entra em um período de teste gratuito: registre-se e entre com um clique para começar a usar; o pagamento passa a ser uma melhoria opcional — se o usuário abrir o link e cair na página de assinatura, o período de teste acabou, então siga o fluxo de pagamento do Passo 7; o fluxo se adapta sozinho, sem mudar o script)

## Ambiente de execução

- Script principal `scripts/powpow-register.mjs`: **zero dependências**, requer **Node ≥ 18**. Antes de começar, rode uma vez `node scripts/powpow-register.mjs status` para confirmar que o ambiente funciona.
- Todas as requisições do script vão apenas para o domínio oficial `https://global.powpow.online`.
- **Sem Node / erros do script**: volta automaticamente ao modo de guia puro — dê ao usuário a página de registro https://global.powpow.online/register e acompanhe-o conforme `references/registration-flow.md` (durante o período de teste gratuito, o registro web é igualmente imediato). Não insista com o script.
- Retomada após interrupção da conversa: rode primeiro `status` para ver em que ponto do fluxo você está e siga a partir daí.

## Trigger Conditions

- Intenção de registro: «quero me registrar na Bolha», «criar uma conta powpow», «como me registro na Bolha», «sign up powpow»
- Registro travado: «não chega o código de verificação», «diz que o nome de usuário já existe», «a senha nunca passa na validação»
- Problemas após o registro: «o login diz que a conta não está ativada», «403 pending_payment», «como pago/assino a Bolha», «a Bolha é grátis ou paga?»

**Não se ativa para**: publicar posts / criar humanos digitais (→ powpow-simple); desenvolvimento de código no lado Web (veja as skills de desenvolvimento). Se o usuário quer se registrar e também publicar: conclua primeiro esta skill e, após a ativação, passe-o para o powpow-simple.

## Resumo do fluxo

| Etapa | O que o agent faz | O que o usuário faz |
|---|---|---|
| 1 Apresentação do produto | Apresenta + envia capturas | Dá uma olhada |
| 2 Confirmação de dados | Sugere proativamente nome de usuário/apelido, senha com duas opções, pede o e-mail | Confirma, fornece |
| 3 Envio do código | `send-code` | —— |
| 4 Leitura do código | —— | Vai ao e-mail, busca o código de 6 dígitos e o envia de volta |
| 5 Envio do registro | `register` (com upload direto do avatar), trata erros automaticamente | —— |
| 6 Login com um clique | `login-link(home)` direto para a página inicial; se cair na página de assinatura, vá ao Passo 7 | Clique no link e comece a usar |
| 7 Melhoria de assinatura (opcional) | Só quando o usuário quer associação / o período gratuito acabou: fluxo de pagamento completo gerenciado | Escolha um método, pague |
| 8 Encerramento | `cleanup` + entrega de credenciais + guia de uso + recomendação de plugins | Começa a jogar |

## Etapa 1: apresentação do produto + capturas (não pode ser pulada)

A maioria dos usuários nunca viu a Bolha. A primeira coisa não é explicar o fluxo, mas fazer com que ele **veja** o produto:

1. Apresente a Bolha em ~120 caracteres: transforme as fotos tiradas de passagem em um diário de viagem, pregado no mapa público como uma «bolha»; as bolhas perdem a validade com o tempo e os «curtir» dos outros podem revivê-las; no mapa também há «humanos digitais» com quem dá para conversar. Endereço da plataforma: https://global.powpow.online ; para ver um vídeo antes: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Envie capturas**. As capturas já acompanham a skill em `assets/screenshots/powpow-0N.jpg` — envie-as diretamente como arquivos de imagem locais, sem precisar de conexão. O inventário, o conteúdo de cada imagem e quando usá-las estão em `references/screenshots.md`. A combinação mais comum na abertura: página do mapa (powpow-03) + página de detalhes de um post (powpow-06).

Regras de capturas (regras firmes):

- As capturas **já vêm embaladas com a skill** em `assets/screenshots/` (`powpow-0N.jpg`) — envie diretamente como arquivos de imagem locais; servem em qualquer ambiente, incluindo os em que o GitHub não abre.
- Envie apenas 1–3 imagens relacionadas ao assunto do momento, não cole tudo de uma vez.
- Se por acaso faltarem arquivos do pacote, recorra aos links hospedados listados em `references/screenshots.md` (atenção: podem não abrir na China continental).

Terminada a apresentação, deixe a decisão com o usuário: **«Se quiser se registrar, em três minutos deixamos a conta criada aqui na conversa; você só vai precisar olhar uma vez o código que chega no seu e-mail.»**

## Etapa 2: confirmar os dados de registro (uma pergunta por turno, não pergunte tudo de uma vez)

- **Nome de usuário** (obrigatório): **sugira proativamente um** a partir do contexto da conversa ou do nome de usuário do sistema (2~50 caracteres, sem distinção de maiúsculas/minúsculas); se o usuário concordar, use-o; se quiser mudar, muda-se.
- **Senha** (obrigatória; primeiro ofereça duas opções):
  - O usuário fornece → depois é passada ao script por variável de ambiente, **nunca como argumento de linha de comando**;
  - O agent gera → rode `node scripts/powpow-register.mjs gen-password` e **envie imediatamente a senha gerada ao usuário para que ele salve** (é exibida só desta vez e não volta a aparecer).
- **E-mail** (obrigatório): deve ser fornecido pelo usuário — é a âncora de identidade da conta, **não adivinhe por ele**.
- **Apelido** (opcional): sugira que por padrão seja igual ao nome de usuário.
- **Avatar** (opcional): se o usuário der o caminho de uma imagem local (≤5 MB, não SVG), o script faz o upload direto; se não, pule (a plataforma usa o logo padrão); se você tiver capacidade de gerar imagens, pode oferecer-se para criar uma.
- **Telefone** (opcional, número da China continental): pule por padrão; só peça se o usuário quiser vincular.

Confirmado, você pode rodar `prepare-suggest --username U --nickname N --email E` para anotar no arquivo de estado (assim o register não pede de novo).

## Etapas 3–4: código de verificação por e-mail (a única parte que exige sair da conversa)

```
node scripts/powpow-register.mjs send-code --email <e-mail>
```

Depois diga claramente ao usuário: **vá ao e-mail procurar o código de verificação de 6 dígitos, válido por 10 minutos; lembre-se de olhar também a pasta de spam / e-mails promocionais**; quando encontrar, que volte e lhe envie. O envio tem uma espera de 60 segundos, não fique clicando em sequência.

## Etapa 5: enviar o registro (gestão delegada pelo agent)

```
POWPOW_REGISTER_PASSWORD=<senha> node scripts/powpow-register.mjs register --code <código> [--username U] [--nickname N] [--avatar <caminho de imagem local>] [--phone P]
```

Se der certo, a conta fica criada (estado pending, com 3 badgeis iniciais). Os erros comuns são tratados automaticamente, sem interromper o usuário:

| Erro | Tratamento |
|---|---|
| 「用户名已存在」 (o nome de usuário já existe) | Sugere automaticamente uma variante (nome de usuário + número) e, confirmada pelo usuário, tenta de novo direto (o código continua válido, não precisa reenviar) |
| 「邮箱已被使用」 (o e-mail já está em uso) | Pergunte ao usuário: troca de e-mail, ou na verdade já tem conta? (encaminhe para login / recuperação de senha) |
| 「邮箱验证码错误或已过期」 (código de verificação errado ou expirado) | Passaram mais de 10 minutos → rodar `send-code` de novo |
| Envio/registro frequentes demais (429) | Espere 1 minuto e tente de novo; basta avisar o usuário |

## Passo 6: Login com um clique (direto para a página inicial após o registro)

1. Logo após o registro bem-sucedido:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Envie o link ao usuário: **abra e você cairá diretamente na página inicial, já logado**. A plataforma está atualmente em um período de teste gratuito — após o registro, todos os recursos estão disponíveis (feed, mapa, humanos digitais, check-ins etc.), **sem necessidade de pagar**.
3. Peça ao usuário para confirmar se entrou; há dois casos:
   - **Caiu na página inicial** → pule direto para o Passo 8 para encerrar; o registro está completo;
   - **Caiu na página de assinatura** → o período de teste gratuito da plataforma acabou; diga ao usuário «o período de teste gratuito acabou, agora é necessária uma assinatura de membro», depois siga o Passo 7 para concluir a assinatura e volte ao Passo 8 quando terminar.
4. Se o usuário quiser ativamente melhorar ou apoiar a plataforma → vá também ao Passo 7 (assinar é voluntário; não insista).
## Passo 7: Melhoria de assinatura (opcional — apenas quando o Passo 6 exigir)

1. Primeiro envie o link de meio-login para que a página de retorno do pagamento mostre corretamente «Pagamento realizado»:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Envie o link ao usuário: ao abrir, o navegador cai diretamente na página de assinatura, já logado.
2. **Deixe o usuário escolher o método de pagamento** — mostre os dois canais:
   - **Alipay (China continental / usuários com Alipay)**: compra única da duração correspondente, **sem renovação automática**
     - Mensal **¥6.99** (recomendado para experimentar) / Trimestral **¥19.99** / Anual **¥69.99**
   - **PayPal (exterior / usuários sem Alipay)**: renova mensalmente, cancele quando quiser
     - Premium Monthly, cerca de **$1/mês** (conforme exibido na página de assinatura; renovação automática)
3. Depois que o usuário escolher:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   O script retorna o caminho do arquivo da página de pagamento; **abra-o diretamente com um comando do sistema** (Windows: `start <arquivo>`; macOS: `open <arquivo>`; Linux: `xdg-open <arquivo>`). O navegador pula automaticamente para o caixa oficial do Alipay/PayPal, onde o usuário conclui o pagamento ou a autorização de cobrança.
4. Execute `query` a cada 10–15 segundos até retornar `paid` ou `ACTIVE` (o recebimento/autorização costuma levar de alguns segundos a um minuto). Se o usuário fechar a página de pagamento no meio → basta executar `create-order` novamente (pedidos antigos / assinaturas pendentes fecham ou expiram automaticamente após 2 horas; ignore-os).
5. O canal de código QR do WeChat é confirmado manualmente e o recebimento pode atrasar; Huawei IAP só está disponível dentro do app HarmonyOS. O skill não cuida desses dois — após pagar, o usuário volta e conta, e o agent executa primeiro `whoami` para confirmar o recebimento, depois envia o link para a página inicial do ponto 6 abaixo.
6. Após confirmar o recebimento, troque por um estado de login com a declaração de assinatura mais recente e envie o link direto para a página inicial:
   ```
   POWPOW_REGISTER_PASSWORD=<senha> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Envie o link ao usuário: **abra e você cairá diretamente na página inicial com a associação completa**.
## Passo 8: Encerramento

1. `node scripts/powpow-register.mjs cleanup` para limpar os arquivos de estado temporários locais (credenciais de sessão).
2. Dê ao usuário um «cartão da conta»: nome de usuário, e-mail (a senha não é exibida novamente — no modo gerado o usuário já foi convidado a salvá-la na geração; se ele mesmo a definiu, ele a sabe).
3. Lembrete de associação (diga uma vez, não insista): atualmente é um período de teste gratuito e a conta pode ser usada imediatamente; quando o período de teste acabar, contas sem assinatura que visitarem páginas de conteúdo serão redirecionadas para a página de assinatura — para uso prolongado, volte e peça ao agent para assinar quando quiser.
4. Guie os primeiros passos: explorar o mapa, publicar o primeiro diário de viagem (→ passe para o powpow-simple).
5. Recomende extensões: o skill `@durenzidu/powpow-integration` e o plugin `@durenzidu/openclaw-channel-powpow` — conecte a Bolha ao agent do próprio usuário; dê o comando de instalação se ele quiser.
6. Encerre com um bloco de «próximo passo».
## Conversation UX

Mantenha o tom de serviço habitual do powpow:

- **O usuário é o sujeito da frase**; «você pode…» é melhor que «eu preciso que você…»; sem sermões, sem tom de superioridade.
- **Cada turno avança uma única decisão**; antes de pedir um dado, dê o motivo.
- **No final de cada resposta** vai um bloco fixo de «próximo passo» (separador + 👉 + uma única ação + uma frase «quando você fizer, eu…»), por exemplo:
  ```
  ────────────────────
  👉 Agora é com você: vá ao e-mail, procure o código de 6 dígitos e me envie direto
     (assim que eu o receber, crio a conta)
  ```
- **Não faça sermão de segurança sobre a senha por iniciativa própria**; não explique mecanismos internos, limites de frequência nem design de segurança, salvo se o usuário perguntar.
- Quando o agent estiver gerenciando as tarefas, informe o progresso com ainda mais assiduidade: depois de cada passo de script, diga numa frase o que acabou de acontecer («a conta já está criada», «já abri a página de pagamento para você»).

## Regras firmes

- **Segurança das credenciais**: a senha é passada ao script apenas pela variável de ambiente `POWPOW_REGISTER_PASSWORD`, **nunca** como argumento de linha de comando (visível na lista de processos), nem escrita em qualquer arquivo (no modo geração ela é exibida uma vez para o usuário salvar e não se repete depois). O código de verificação só é usado na interface oficial de registro e é descartado após o uso.
- **Limite oficial**: todas as requisições vão apenas para `https://global.powpow.online` (já embutido no script); jamais envie informações do usuário para endereços de terceiros.
- **Limite de pagamento**: o agent só cria o pedido, abre o caixa e consulta o pagamento; **jamais** toca na conta Alipay/PayPal do usuário ou nas suas credenciais de pagamento, e jamais promete «pagar por ele».
- **O paywall não é um bug**: durante o período atual de teste gratuito todas as páginas de conteúdo estão abertas; se o usuário abrir o link da página inicial mas cair na página de assinatura, o período de teste acabou — guie-o a assinar pelo Passo 7. Não tente contornar o paywall nem explique mecanismos internos ao usuário.
- **Liberdade de recuo**: se em qualquer etapa o usuário quiser fazer por conta própria, ou o ambiente não suportar o script, recua a qualquer momento para o modo de orientação pura — dê os links, explique as regras e acompanhe na resolução de erros.
- Não invente regras da plataforma: as regras de campos, as mensagens de erro e os parâmetros de limite vêm todas do código da plataforma (`references/registration-flow.md` cita as fontes); se a plataforma for atualizada, vale o comportamento real.
- Para mostrar imagens use apenas as capturas incluídas em `assets/screenshots/` (o uso de cada uma está em `references/screenshots.md`).
- Feche cada turno com o bloco de «próximo passo», para que o usuário saiba sempre o que lhe cabe fazer agora.
