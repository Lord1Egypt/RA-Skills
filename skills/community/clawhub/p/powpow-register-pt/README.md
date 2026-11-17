# powpow-register

Assistente de registro no PowPow Bolha (edição OpenClaw): leva um usuário novo de «não sei o que é a
Bolha» até «conta ativada, login com um clique, hora de jogar» — apresentação do produto (com capturas de
tela), registro delegado ao agent (com upload de avatar), pedido de assinatura via Alipay/PayPal e acompanhamento
do pagamento, login com um clique de link duplo, diagnóstico de erros.

**Desde a v2.0.0 modo assistido por agent, e desde a v2.2.0 adaptação ao período de teste gratuito da plataforma**: o script central `scripts/powpow-register.mjs` é de zero dependência
(Node ≥ 18); o usuário sai da conversa apenas uma vez: para consultar o código de verificação no e-mail. Durante o período atual de teste gratuito, uma conta registrada pode usar todos os recursos imediatamente — o pagamento da assinatura é uma melhoria opcional; se o período de teste acabar e o usuário cair na página de assinatura, o fluxo muda automaticamente para o caminho de pagamento. Sem Node, ou quando o usuário prefere fazer sozinho, volta automaticamente ao modo de guia puro.

## Instalação

```
openclaw skills install @durenzidu/powpow-register
```

## Funcionalidades

1. **Apresentação do produto**: abertura de ~120 caracteres + capturas de tela embutidas no pacote
   (`assets/screenshots/`, 6 imagens: página do mapa, página de detalhes de um post etc.; escolha 1–3
   conforme a cena; sem hospedagem externa, funciona offline).
2. **Registro delegado**: o agent sugere proativamente nome de usuário/apelido, senha com duas opções
   (fornecida pelo usuário ou gerada pelo agent), envio e envio do código de verificação, upload direto do
   avatar (≤5 MB, não SVG), tratamento automático dos erros comuns (ocupado / expirado / limite de
   frequência).
3. **Login com um clique (link duplo)**: logo após o registro bem-sucedido, um link de login leva o usuário direto para a página inicial (durante o período de teste gratuito, um clique e já está usável);
   se cair na página de assinatura (período de teste acabado) ou o usuário quiser melhorar, siga o fluxo de assinatura — após o recebimento, troque por um novo estado de login e o link de associação completa o leva à página inicial
   (através da ponte oficial `me?token=` da plataforma, que planta o cookie HttpOnly automaticamente).
4. **Pagamento da assinatura**: tanto no Alipay (mensal ¥6.99 /
   trimestral ¥19.99 / anual ¥69.99, compra única sem renovação automática) como no PayPal (Premium Monthly, cerca de $1/mês, renovação automática, cancele quando quiser) o agent faz o pedido e a consulta em loop até cair;
   QR code WeChat / Huawei IAP apenas indica-se o caminho.
5. **Diagnóstico de erros**: código de verificação não chega, nome de usuário/e-mail ocupados, 403 não
   ativado, conta bloqueada e outros problemas comuns, todos vindos do código-fonte da plataforma com as
   fontes citadas.

## Estrutura de arquivos

```
powpow-register/
├── SKILL.md                            # Guia principal (condições de disparo, fluxo de 8 etapas, normas de tom, regras firmes)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Capturas do produto embutidas (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Script principal (zero dependências Node≥18, 11 subcomandos)
└── references/
    ├── agent-flow.md                   # Contrato do script, sequência completa, mecanismo de link duplo, design de segurança
    ├── registration-flow.md            # Regras de campos, limites, tabela de diagnóstico (com fontes no código)
    ├── payment-and-activation.md       # Contrato Alipay vibepay, cadeia de ativação, diagnóstico dos canais
    └── screenshots.md                  # Inventário das capturas embutidas + consulta rápida por cena
```

## Segurança

- **Senha**: entra no processo do script apenas por variável de ambiente, nunca em argumento de linha de
  comando, nunca no disco, nunca no arquivo de estado; a senha gerada pelo agent é exibida uma única vez
  para o usuário salvar.
- **Código de verificação**: usado apenas na interface oficial de registro, descartado após o uso; o
  arquivo de estado (e-mail/nome de usuário/token/número do pedido) fica no diretório temporário do
  sistema, apagado de uma vez pelo `cleanup` ao fim do fluxo.
- **Pagamento**: o agent só cria o pedido, abre o caixa e consulta o pagamento; jamais toca na conta
  Alipay/PayPal do usuário ou nas suas credenciais de pagamento, jamais paga por ele. O pagamento acontece
  sempre entre o usuário e o caixa oficial.
- Todas as requisições vão apenas para o domínio oficial `https://global.powpow.online`; nenhuma chave incluída.

## Licença

MIT-0 (licença unificada do ClawHub).

## Links

- Site oficial: https://global.powpow.online
- Registro: https://global.powpow.online/register
- Conheça a Bolha (vídeo): https://www.bilibili.com/video/BV1Wu826UEVz/
