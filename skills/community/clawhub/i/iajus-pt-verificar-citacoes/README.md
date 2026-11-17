# IAJUS - Jurisprudência PT - candidato OpenClaw PT

Fonte: canal codex-pt, versão 2.0.21. Servidor `iajus-pt`: https://pt.mcp.iajus.com.br/mcp.

[Site](https://iajus.pt) | [Privacidade](https://iajus.pt/privacidade) | [Termos](https://iajus.pt/termos) | [Suporte](https://iajus.pt/contacto.html)

# IAJUS no OpenClaw e ClawHub

O OpenClaw oferece conexão MCP remota com OAuth. Os candidatos IAJUS usam
entradas separadas: `iajus` para Brasil e `iajus-pt` para Portugal. A conexão BR
oferece jurisprudência e legislação; PT oferece jurisprudência portuguesa.
Consulte a cobertura declarada pela conexão, sem presumir completude ou atualização.

## Candidato e configuração

O gerador `scripts/ops/build_plugin_submission_bundle.py --country BR --alvo openclaw
--output <pasta-nova>` produz um ZIP com as skills `iajus` (conexão e pesquisa)
e `iajus-verificar-citacoes` (verificação de citações).
Para Portugal, use `--country PT`: os nomes serão `iajus-pt` e
`iajus-pt-verificar-citacoes`. Cada pasta de skill contém `SKILL.md`,
`openclaw.json`, este guia, `REVIEW_CASES.md` e `LICENSE`.
A skill de verificação inclui as instruções canônicas de pesquisa do país em
`references/`, para conferir filtros e modalidades sem depender de outro plugin.
Nome, versão, URL e contatos vêm do canal Codex do país; não edite a saída gerada.
Os builds do projeto são executados na testbox AWS.

A skill ensina o uso da conexão: instalar a skill não configura nem autentica
o servidor. O JSON ao lado dela é um trecho de configuração manual, não um
manifesto de plugin executável. Não instala as skills dos pacotes Claude/Codex.

No perfil OpenClaw que será utilizado, confira primeiro:

```text
openclaw mcp status --verbose
openclaw mcp doctor <nome>
```

Substitua `<nome>` por `iajus` ou `iajus-pt`. Se já houver uma entrada, reconcilie
URL e estado antes de modificá-la; não duplique servidor, conta ou cliente OAuth.
No OpenClaw consultado, alterações de configuração, login e sondagens precisam
do Gateway parado. O operador deve planejar essa pausa sem interromper trabalho
em andamento; não pare automaticamente uma sessão de outro dono.

Com essa condição atendida, mescle somente a entrada do `openclaw.json` gerado
em `mcp.servers` de `~/.openclaw/openclaw.json`, preservando os outros servidores.
O trecho usa `url`, `transport: streamable-http`, `auth: oauth` e os escopos
OAuth do canal em `oauth.scope`.
Se a entrada ainda não existir, a CLI também oferece:

```text
openclaw mcp add <nome> --url <URL-do-openclaw.json> --transport streamable-http --auth oauth --oauth-scope "<escopos-do-openclaw.json>"
openclaw mcp login <nome>
```

Conclua o consentimento no navegador com a conta existente autorizada para o
país. O fluxo normal recebe o callback local; a colagem manual de código é uma
alternativa para ambiente remoto ou callback inacessível. Não copie códigos ou
tokens para chat, arquivos do pacote, logs ou vídeo. O OpenClaw mantém as
credenciais localmente. Não combine essa configuração OAuth com header estático
de autorização: o cliente o ignora em modo OAuth.

## Comprovar a jornada

Depois do login, com a condição do Gateway atendida, execute
`openclaw mcp probe <nome> --json`. `status` e `doctor` sem `--probe` inspecionam
configuração; não comprovam conexão. Um probe que lista ferramentas ainda não
comprova renovação OAuth ou uma consulta com fonte.

No agente conectado, use os nomes e schemas efetivamente descobertos. Para BR,
exemplos de recursos do catálogo OAuth são:

| Ferramenta | Uso |
|---|---|
| `pesquisar_decisoes` | Localizar decisões por tema, texto ou identidade. |
| `ler_documento` | Ler o documento disponibilizado pela conexão. |
| `pesquisar_precedentes` | Consultar precedentes qualificados. |
| `pesquisar_informativos` | Consultar informativos. |
| `explorar_relacoes_juridicas` | Examinar relações e citações. |
| `pesquisar_normas` | Pesquisar normas brasileiras. |
| `pesquisar_artigos` | Localizar dispositivos de normas brasileiras. |
| `localizar_norma_fonte_oficial` | Localizar norma na fonte oficial. |
| `consultar_alteracoes_norma` | Conferir o histórico da redação de uma norma. |
| `consultar_cobertura_acervo` | Consultar cobertura declarada do acervo. |

Essa tabela BR não descreve o catálogo PT. A conexão portuguesa não oferece
legislação, vigência, doutrina nem Lex. Não envie pesquisa brasileira a PT nem
apresente uma resposta do outro país como se fosse do solicitado.

Execute os casos do país em `REVIEW_CASES.md` e registre versão do cliente,
host/país, chamada real, resposta com fontes, refresh e negativas de jurisdição
e autorização, sem credenciais. Diferencie resultado vazio, incompleto e erro.
Os casos são roteiro; só execução real produz evidência. Capture a demonstração
apenas após a jornada funcionar, omitindo códigos, tokens e dados pessoais.

## Preparação para ClawHub

ClawHub distribui skills e plugins. Este candidato é uma skill companheira,
com `SKILL.md` e seus arquivos de apoio no mesmo diretório. A superfície
declarativa `mcpServers` dos plugins OpenClaw consultada descreve processos
`stdio`; não é um registro declarativo de endpoints remotos OAuth.
Uma integração executável seria outro produto, com código próprio.

Antes de qualquer envio, reconcilie slug, conta publicadora, versões existentes
e condições do catálogo. A prévia documentada é
`clawhub skill publish <pasta-da-skill> --slug <nome> --dry-run`.
Ela não foi executada na preparação deste candidato e não equivale a análise
verde ou publicação. `clawhub package validate` destina-se a plugins executáveis,
não a esta skill.

Os arquivos de cada skill OpenClaw, incluindo referências e exemplo de configuração,
são distribuídos sob MIT-0, conforme o `LICENSE` dentro da sua pasta
(fonte: `LICENSE.skills`). Essa licença não licencia o serviço hospedado, o corpus ou os dados.
O MCP hospedado continua sujeito aos planos, autenticação, limites, preços e termos
IAJUS. Instalar a skill não concede acesso gratuito ao serviço.
OAuth/refresh, jornada nativa, análise ClawHub, conta/namespace e eventual vídeo
permanecem pendentes até receberem evidência própria.

## Referências do formato

Conferidas em 16/10/2026, OpenClaw `4e334e81e6946ff66ad06639c1d7dfde306a8b5d`:
[CLI MCP e login](https://github.com/openclaw/openclaw/blob/4e334e81e6946ff66ad06639c1d7dfde306a8b5d/docs/cli/mcp/registry.md),
[configuração](https://github.com/openclaw/openclaw/blob/4e334e81e6946ff66ad06639c1d7dfde306a8b5d/docs/cli/mcp/json-output.md),
[superfície de plugins](https://github.com/openclaw/openclaw/blob/4e334e81e6946ff66ad06639c1d7dfde306a8b5d/docs/plugins/manifest/surfaces.md).
ClawHub `6cc4aea3df7c08aef7d31eb6b0271646da7af14a`:
[formato e licença da skill](https://github.com/openclaw/clawhub/blob/6cc4aea3df7c08aef7d31eb6b0271646da7af14a/docs/skill-format.md),
[CLI](https://github.com/openclaw/clawhub/blob/6cc4aea3df7c08aef7d31eb6b0271646da7af14a/docs/cli.md),
[publicação](https://github.com/openclaw/clawhub/blob/6cc4aea3df7c08aef7d31eb6b0271646da7af14a/docs/publishing.md).
