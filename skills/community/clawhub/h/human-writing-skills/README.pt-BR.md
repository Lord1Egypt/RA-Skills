# Advanced Human Writing & AI Humanizer

<p align="center"><img src="assets/logo.png" width="320" alt="Human Writing: escrita com caneta-tinteiro e código de terminal sobre fundo branco quente"></p>

> Escrita com IA mais natural: revisão multilíngue, colaboração por trechos e verificação de continuidade em textos longos, com Skills e um plugin para DSH.

**Termos de busca:** humanizar texto de IA, remover tom de IA, tirar escrita robótica, revisão de romance, coerência narrativa, auditoria de capítulos, consistência de personagens, diálogos naturais, texto em português natural, evitar tradução literal, redação de notícias, revisão acadêmica.

Este projeto reúne instruções reutilizáveis e um compilador leve de prompts. Ele não promete detectar autoria nem burlar detectores. O objetivo é melhorar clareza, especificidade, continuidade e responsabilidade editorial.

## Capacidades

- Ficção e webnovels: continuidade de personagem, relação, espaço, objetos, roupa, cronologia, voz e resposta de diálogo.
- Notícias, relatórios, documentos formais e textos acadêmicos: fontes, atribuição, terminologia, números, citações e limites das conclusões.
- Escrita multilíngue: português, espanhol, francês, inglês, chinês, japonês, árabe, latim e outros idiomas suportados pelo modelo.
- Tradução e localização: reduz calques, conectores herdados, falsos cognatos e voz neutra de tradução, sem apagar significado ou contexto cultural.
- Obras longas: divide o material em blocos auditáveis e reconcilia mudanças de estilo, voz e fatos entre capítulos ou seções.

Para romances com pelo menos três capítulos, `chunk-audit --book-level` acrescenta uma única revisão da arquitetura da obra após os blocos: decisões, consequências, evolução do conflito e saltos temporais. Não é ativada em relatórios ou capítulos isolados.

`verify` confere literalmente números e citações; `verify-fidelity --source original.md --candidate revisado.md` localiza afirmações alteradas e exige revisão do sentido. A identificação automática de documentos sérios usa múltiplos indícios por idioma; informe `--document-type` quando o texto for curto. Os exemplos incluídos são testes preliminares, não validação independente por falantes nativos.

## Uso rápido

```powershell
python -m humanwriting.cli humanize `
  --draft rascunho.md `
  --style fiction `
  --mode deep `
  --task "Revise o ritmo sem apagar a voz estabelecida dos personagens."

python -m humanwriting.cli audit `
  --draft capitulo.md `
  --context biblia-do-romance.md `
  --profile voice
```

Use `--reference exemplo-aprovado.md` ou `--reference-style` apenas quando houver material de referência explícito. Referências definem características de estilo, não fatos, enredo ou frases a copiar.

## Auditoria longa com tarefas independentes

Modelos frequentemente deixam partes de um texto longo sem revisão. `chunk-audit` cria um pacote verificável: cada bloco tem corpo exclusivo, uma curta entrada anterior apenas para continuidade e uma linha de base compartilhada.

```powershell
python -m humanwriting.cli chunk-audit `
  --draft romance-completo.md `
  --style fiction `
  --outline biblia-do-romance.md `
  --reference capitulos-aprovados.md `
  --agent-mode deep `
  --output-dir auditoria-romance
```

Execute `00-baseline-prompt.md` primeiro. Em seguida, as tarefas que dependem apenas de `baseline` podem rodar em paralelo, cada uma numa conversa nova ou chamada de API independente. Salve cada resposta na rota prevista em `reports/`, indicada por `agent-plan.json`.

```powershell
python -m humanwriting.cli verify-chunk-audit `
  --package-dir auditoria-romance
```

Cada resposta deve trazer um **Coverage Receipt** com o bloco, as unidades efetivamente revisadas, achados e lacunas. A reconciliação final só começa quando todas as tarefas exigidas estiverem completas. `standard` gera uma revisão completa por bloco; `deep` acrescenta auditoria de prosa por parágrafo, auditoria de diálogo quando aplicável e, em texto sério com fontes, auditoria de evidências.

## Tradução natural

Use `--translationese` apenas para tradução ou localização explicitamente solicitada:

```powershell
python -m humanwriting.cli chunk-audit `
  --draft relatorio-pt.md `
  --style formal-document `
  --context plano-editorial.md `
  --source fontes.md `
  --translationese `
  --agent-mode deep `
  --output-dir auditoria-relatorio
```

O módulo preserva nomes, números, citações, terminologia, atribuição e grau de incerteza. Não inventa sotaques, gírias, palavras estrangeiras ou estereótipos nacionais.

## Economia de tokens

Os módulos são carregados por necessidade. Voz, registro, relações, continuidade serial e espaço físico exigem evidência no pedido ou no contexto. Proteção de conteúdo factual só é automática para notícia, documento formal e texto acadêmico, jurídico ou técnico. O modo profundo é sempre explícito.

## Mais documentação

- [README in English](README.md)
- [README 中文](README.zh-CN.md)
- [README en español](README.es.md)
- [README en français](README.fr.md)
- [Guia de consistência de textos longos](docs/long-form-consistency.md)
- [Guia de auditoria em etapas](docs/audit-pipeline.md)

## Licença

MIT. Consulte [LICENSE](LICENSE).
