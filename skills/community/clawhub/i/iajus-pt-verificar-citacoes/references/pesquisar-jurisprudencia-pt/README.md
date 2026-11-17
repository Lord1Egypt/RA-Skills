# Pesquisar jurisprudência portuguesa (IAJUS)

Use somente as ferramentas e schemas descobertos na conexão `iajus-pt` do OpenClaw. Os nomes abaixo identificam operações; não são aliases a presumir. Se a conexão retornar 401, oriente o operador pelo [guia de conexão](../../README.md); não execute login nem peça tokens ou senhas. Recusa de permissão ou plano exige informar o limite devolvido. Ferramenta ausente deve ser declarada indisponível, sem inventar nomes ou responder o mérito jurídico de memória.

Veja primeiro as ferramentas expostas nesta ligação. Use apenas as que aparecem e siga o esquema de cada uma. Para decisões, a ferramenta é pesquisar_decisoes, com um objeto busca cujo campo modo é um dos quatro modos portugueses abaixo; para precedentes qualificados, pesquisar_precedentes.

## Escolher a modalidade

| Intenção | busca.modo |
|---|---|
| Questão por significado e termos complementares | hibrida |
| Tema ou conceito, sem exigir correspondência literal | semantica |
| Termos presentes no texto, frase exata ou número de processo | textual |
| Padrão literal ou forma de citação (por exemplo um ECLI) | expressao |

A entrada é fechada e varia por modo; consulta é obrigatória em hibrida, semantica e textual, e expressao é obrigatória em expressao. Use apenas filtros que o modo aceita:

- hibrida: tribunal, classe, tipo_recurso e os campos comuns;
- semantica: tribunal, um único ano e kind;
- textual: tribunal, classe_sigla, frase_exata e os campos comuns;
- expressao: tribunal, classe_sigla, ignorar_maiusculas, allow_unindexed_scan e os campos comuns.

Os campos comuns são ano_min, ano_max, data_julgamento_min e data_julgamento_max (AAAA-MM-DD), relator, orgao_julgador, tipo e tipo_unidade. limite vai de 1 a 100 e, por defeito, é 20; ajuste à quantidade pedida. Em textual e expressao há também ordenar_por (textual: relevancia, ano ou tamanho; expressao: ano ou tamanho), direcao_ordenacao (asc ou desc) e tamanho_pagina. Os códigos de tribunal aceites vêm do acervo: consulte a secção orgaos de consultar_acervo em vez de os adivinhar.

Exemplos (os argumentos completos de cada chamada):

```json
{"busca": {"modo": "hibrida", "consulta": "responsabilidade civil do médico por falta de consentimento informado", "filtros": {"ano_min": 2015}, "limite": 10}}
```

```json
{"busca": {"modo": "textual", "consulta": "abuso de direito", "filtros": {"frase_exata": true}}}
```

Para obter mais resultados, repita consulta, filtros e limite com page_info.next_cursor em busca.cursor. Pare na quantidade pedida ou quando não houver continuação; não percorra todas as páginas sem necessidade. Híbrida, semântica e textual percorrem uma janela de até três páginas, limitada a 100 resultados; expressão usa a paginação do executor e pode não ter cursor na pesquisa sem índice. Fim da janela ou truncated não prova fim do acervo: refine o recorte. Cursor expirado, inválido ou ranking alterado exige reiniciar, sem contar a primeira página repetida como novos resultados.

Em expressao, use uma expressão regular POSIX com âncora literal; só permita allow_unindexed_scan quando o pedido justificar uma pesquisa sem essa âncora. ignorar_maiusculas não elimina diferenças de acentuação.

## Pesquisa por número de processo

Esta ligação não tem modo CNJ. Em textual, um número de processo em consulta, sem frase_exata nem cursor, localiza o próprio processo e ignora ordenação e tamanho_pagina:

```json
{"busca": {"modo": "textual", "consulta": "1234/19.4T8LSB"}}
```

Restrinja ao tribunal com filtros.tribunal quando o utilizador o indicar. Escreva o número na forma em que o acórdão o regista; não o converta nem o complete de memória. Para um ECLI ou outro identificador literal, use expressao com âncora literal. Um acórdão que apenas cita o número no texto não é o processo pedido: diga-o. Zero resultados não prova que o processo não exista.

## Precedentes

pesquisar_precedentes exige busca.filtros.tipo. Para acórdãos uniformizadores, use tipo auj; tribunal é opcional (por exemplo pt_stj) e incluir_canceladas é verdadeiro por defeito:

```json
{"busca": {"filtros": {"tipo": "auj", "tribunal": "pt_stj"}, "limite": 5}}
```

limite aceita até 10 resultados e não há cursor nem escolha de ordem. Número e matéria não selecionam precedentes nesta linha: para localizar um acórdão uniformizador pelo número, use pesquisar_decisoes. Preserve estados e avisos devolvidos; desconhecido continua desconhecido. Um resultado curto ou zero não é um inventário do acervo.

Leia `uniformizador_valido` em cada resultado quando existir: se for falso, não apresente o acórdão como uniformizador, mesmo que o tipo devolvido seja `auj`. Preserve a indicação de classificação inconsistente; um acórdão de Relação não deve ser promovido a AUJ. Vigência desconhecida não significa vigente; não há histórico de redações dos precedentes.

## Resultado e citação

Cite apenas elementos devolvidos nesta chamada: tribunal, número, data, excerto e ligação de origem quando presentes. Preserve a proveniência e não rotule uma ligação como oficial sem indicação da própria fonte. Um excerto não sustenta afirmações que não contém.

Uma pesquisa concluída sem resultados é zero para esse pedido e recorte. Erro, tempo de espera excedido, interrupção, resposta parcial ou medida indisponível não são ausência. Não trate o limite de resultados como censo nem afirme completude.

## Recusas e selos da pesquisa

Leia error_code, busca_status (completa, parcial ou incompleta), busca_motivos, aviso_busca e filtros_ignorados antes de responder:

- input_contract_refused: a entrada não foi lida (expressão regular malformada, tipo inexistente). Reformule como a mensagem indicar e repita; não é falha do acervo.
- filtro_nao_suportado, ou filtros_ignorados não vazio: o filtro nomeado não foi aplicado. Preserve a restrição do utilizador e informe essa limitação; não apresente resultados como se o recorte tivesse sido aplicado. Só repita através de outra modalidade ou fonte suportada se mantiver o mesmo filtro e um recorte equivalente. Se isso exigir remover ou enfraquecer a restrição, pare e pergunte ao utilizador se pretende uma pesquisa mais ampla.
- parcial com janela_limitada: viu-se apenas uma janela. Continue com page_info.next_cursor ou refine o recorte; a lista não é o conjunto.
- incompleta, com falha_busca ou timeout: a pesquisa não terminou. Repita uma vez com um recorte mais estreito; se persistir, diga que a pesquisa FALHOU, nunca «não encontrado».
- completa com zero resultados: zero medido neste recorte; diga que não consta do acervo para este pedido e, se vier link_pesquisa_geral, ofereça-o como pesquisa pública do tribunal.

## Fundamentação

Os dados de um julgamento (relator, vencidos, votos, resultado, tese, data, tribunal) só podem vir de um excerto que uma ferramenta devolveu nesta conversa. Sem o excerto, diga «não localizei esse dado no excerto do acórdão»; nunca complete de memória. Se nenhuma ferramenta devolveu informação, não responda quanto ao mérito: diga que não localizou e ofereça pesquisar. Se o utilizador contestar («tem a certeza?», uma correção), volte a consultar pelo número completo e cite o excerto devolvido, sem se esquivar.

## O que esta ligação não faz

Não há ferramenta registada para ler a íntegra de uma decisão, nem para obter relações ou citações entre decisões, nem o histórico de redações de um precedente; também não há legislação, doutrina nem jurisprudência brasileira. Diga-o ao utilizador em vez de improvisar, e remeta a íntegra para a ligação de origem devolvida, quando existir.
