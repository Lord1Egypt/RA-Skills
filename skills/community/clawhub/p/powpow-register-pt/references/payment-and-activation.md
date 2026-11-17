# Ativação da assinatura e pagamento — powpow-register

## Conclusão (a resposta primeiro)
> **Período de teste gratuito (a partir de 2026-10-18; vale o comportamento real da plataforma)**: durante este período uma conta registrada pode usar todos os recursos diretamente, e **assinar é uma melhoria opcional e não um requisito** — siga o fluxo deste arquivo apenas quando o usuário quiser ativamente a associação. Quando o período de teste acabar, contas sem assinatura que visitarem páginas de conteúdo serão redirecionadas para a página de assinatura; basta concluir a assinatura conforme este arquivo.


**Tanto a assinatura por Alipay como a por PayPal podem ser gerenciadas pelo agent — criação do pedido e acompanhamento do pagamento inclusos.**
O Alipay é compra única sem renovação automática, para usuários da China continental e com Alipay; o PayPal renova automaticamente todo mês e pode ser cancelado a qualquer momento,
para usuários no exterior e sem Alipay. O QR code do WeChat (confirmação manual) e o Huawei IAP continuam existindo, mas não são gerenciados pela skill.

Limites de responsabilidade no pagamento: o agent pode **criar o pedido, abrir o caixa e consultar o
pagamento**; **jamais** toca na conta Alipay/PayPal do usuário ou nas suas credenciais de pagamento, e jamais
promete «pagar por ele». O ato de pagar é sempre realizado pelo próprio usuário no caixa oficial.

## Canal Alipay (vibepay, via principal)

Compra única sem renovação: paga-se uma vez para liberar o período correspondente, **sem renovação
automática**. Os planos estão fixados em `src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Nome | Preço | Duração |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Membro mensal | ¥6.99 | 30 dias |
| `quarterly` | alipay-quarterly | Membro trimestral | ¥19.99 | 90 dias |
| `yearly` | alipay-yearly | Membro anual | ¥69.99 | 365 dias |

### Contrato das interfaces (já encapsuladas pelo script da skill, o agent não monta as requisições à mão)

| Interface | Método | Descrição |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Exige `Authorization: Bearer <JWT>` (basta um usuário pending). body `{package}` → devolve `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` é uma página de formulário que se autoenvia para o gateway do Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Mesma autenticação Bearer. Devolve `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback do servidor do Alipay) | Verificação de assinatura em cinco pontos (assinatura, app_id, coincidência do valor, TRADE_SUCCESS/TRADE_FINISHED, unicidade do comerciante) → atualização **idempotente** do pedido + criação da assinatura + ativação da conta. A skill jamais toca nesta interface |
| `/payment/alipay/return` | Página de retorno do navegador | Caminho público; após o pagamento exibe a confirmação 「支付成功」 e faz polling na página do estado real do backend |

- Pedidos não pagos **fecham automaticamente em 2 horas**; se o usuário desistir no meio → rode
  `create-order` de novo direto, sem se ocupar do pedido antigo.
- O script grava o `paymentHtml` num arquivo HTML temporário; o agent o abre com um comando do sistema e
  assim se entra no caixa do Alipay (escaneando o QR code ou fazendo login no Alipay para pagar).

### Cadeia de ativação (automática, sem intervenção manual)

Verificação de assinatura do notify aprovada → `paymentOrders` marcado como pago → `user_subscriptions`
criada/prorrogada (`planId`, `currentPeriodEnd` calculados por durationDays; as renovações se prorrogam
sobre a data de vencimento original) → `users.accountStatus: active` + `subscriptionStatus: ACTIVE` → a
página de retorno constata o paid e exibe o sucesso.

## Depois de pagar é obrigatório renovar o estado de login (importante)

O JWT carrega dentro a declaração de assinatura (numa conta pending é `NONE`). **O pagamento só atualiza o
banco de dados, não altera um JWT já emitido** — a declaração do token antigo continua NONE; usá-lo
direto para gerar o link de login manifesta-se como «sem membro». Por isso a skill, depois de confirmar o
`paid` / PayPal `ACTIVE`, roda primeiro `refresh-login` (refaz o login e troca por um JWT novo, com a declaração ACTIVE) e
só depois gera o link 2. É comportamento de design, não correção de bug.

## Canal de assinatura PayPal (gerenciado pela skill; web, fora do HarmonyOS)

Existe apenas um plano, o Premium Monthly (cerca de $1/mês, conforme o retorno de `/api/subscription/plans`); **renova automaticamente todo mês**
e o usuário pode cancelar quando quiser na sua conta PayPal.

### Contrato das interfaces (já encapsuladas pelo script da skill; o agent não monta as requisições à mão)

| Interface | Método | Descrição |
|---|---|---|
| `/api/subscription/plans` | GET | Auth Bearer; devolve a lista de planos disponíveis (atualmente só 1) |
| `/api/subscription/create` | POST | body `{planId}` → devolve `{subscriptionId, approveUrl, status}`; `status` costuma ser `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Auth Bearer; devolve `{activeSubscription, allSubscriptions}`; o agent faz polling de `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Chamada automaticamente pela página de sucesso (com o cookie); ativa direto pela API do PayPal se o webhook não chegou |
| `/subscription/success` | Página de retorno do navegador | Onde o usuário cai após a autorização do PayPal; faz polling de verify automaticamente e depois volta para a home/página original |
| `/subscription/cancel` | Página do navegador | Onde o usuário cai se cancelar ou falhar; dá para recomeçar |

### Fluxo delegado

```
create-order --provider paypal  # → devolve approveUrl, gravado num arquivo HTML local
abrir o arquivo HTML            # → o navegador salta para a página de autorização do PayPal
query (a cada 10–15s)           # → fazer polling até ACTIVE
refresh-login                   # → trocar por um JWT novo (declaração de assinatura ACTIVE)
login-link --target home        # → gerar o link de login definitivo
```

- Assinaturas PENDING que não forem concluídas em 1 hora são limpas automaticamente pelo backend; basta recomeçar.
- Se o usuário repetir `create-order`, o backend reaproveita a assinatura `APPROVAL_PENDING` ainda válida, evitando um 409.
- Igual ao Alipay: o pagamento só atualiza o banco, um JWT antigo não se renova sozinho — **é obrigatório** rodar `refresh-login` antes de mandar o link da home.

## Os quatro canais da página de assinatura

A página de assinatura `src/app/(public)/subscription/page.tsx` exibe conforme o ambiente de execução:

| Canal | Ambiente | Mecanismo | Forma de ativação |
|---|---|---|---|
| **Alipay (principal)** | Web | `AlipayPaymentSection` vai pelas interfaces do vibepay (tabela acima) | Ativação automática no servidor via notify, em segundos |
| Assinatura PayPal | Web (fora do HarmonyOS) | `/api/subscription/create` → salto para a autorização do PayPal; renovação mensal automática, cancelável a qualquer momento (`/api/subscription/manage`) | O Webhook do PayPal (`BILLING.SUBSCRIPTION.*`) ativa automaticamente |
| Assinatura por QR code WeChat | Web (fora do HarmonyOS) | No rodapé da página 「微信扫码订阅」 (escaneie para assinar): transferência por QR code | **Confirmação manual**, o pagamento pode demorar a cair; não conclua às pressas que falhou logo após pagar |
| Compra dentro do app Huawei | Dentro do app HarmonyOS | `NativeBridge.purchaseSubscription()` nativo | `/api/subscription/activate-huawei` valida o pedido Huawei e ativa |

Os planos e preços do PayPal são lidos dinamicamente de `/api/subscription/plans`; texto fixo da página:
Auto-renews. Cancel anytime.

## Estados e redirecionamentos

- Alipay concluído → a página de retorno exibe o sucesso; PayPal com sucesso → `/subscription/success` →
  conta active → retorno automático à página de origem indicada pelo parâmetro `next` (se não houver, a
  home).
- Usuário já assinante que revisite a página de assinatura → vê "You're All Set!", e após 3 segundos volta
  automaticamente para a home.
- Pagamento falhado / cancelado (PayPal) → `/subscription/cancel`, dá para iniciar de novo.

## Diagnóstico

| Sintoma | Tratamento |
|---|---|
| Alipay pago mas o `query` segue pending | O notify raramente atrasa; espere 30 segundos e consulte de novo. Se ainda não, o usuário olha no navegador o estado da página de retorno; se persistir, contate o suporte da plataforma (dongtao@outlook.com) informando o `outTradeNo` |
| Alipay pago, mas com o link 2 continua bloqueado | Pulou o `refresh-login` (a declaração do JWT antigo não foi atualizada) — primeiro `refresh-login`, depois `login-link` |
| O `query` do PayPal fica em PENDING | O usuário não concluiu a autorização no PayPal; confirme se o link de autorização foi aberto no navegador. Se mesmo autorizado continuar PENDING, pode ser atraso do webhook: peça ao usuário para esperar mais alguns segundos na página de sucesso ou recarregá-la |
| O `query` do PayPal devolve 409 | Já existe uma assinatura PENDING não concluída; espere 1 hora para expirar ou conclua a autorização do link antigo no navegador |
| PayPal pago, mas com o link 2 continua bloqueado | Igual ao Alipay: primeiro `refresh-login`, depois `login-link` |
| Depois de pagar continua 403 (PayPal) | O Webhook às vezes atrasa; refaça o login para atualizar o estado |
| Pagou no WeChat e não ativou | A confirmação manual é assíncrona; se em algumas horas não ativar, contate o suporte da plataforma |
| A página de assinatura mostra "No subscription plans available" | `/api/subscription/plans` não tem planos PayPal disponíveis, problema de configuração do lado da plataforma; usuários da China continental podem usar o Alipay |

## Nota histórica

No código existe ainda **um antigo** canal de pagamento web do Alipay (`src/lib/alipay.ts`,
`/api/payment/create-order`, ¥9.90/¥99 compra única, degradado para pagamento simulado quando o sandbox
está sem chaves configuradas), que nunca foi ligado à UI da página de assinatura e não tem relação com o
vibepay. A skill não o toca em hipótese alguma; `alipay-vibepay.ts` é o canal vigente.
