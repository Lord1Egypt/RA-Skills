# Pesquisar jurisprudência brasileira

Use somente as ferramentas e schemas descobertos na conexão `iajus` do OpenClaw. Os nomes abaixo identificam operações; não são aliases a presumir. Se a conexão retornar 401, oriente o operador pelo [guia de conexão](../../README.md); não execute login nem peça tokens ou senhas. Recusa de permissão ou plano exige informar o limite devolvido. Ferramenta ausente deve ser declarada indisponível, sem inventar nomes ou responder o mérito jurídico de memória.

Use somente os nomes e schemas que a conexão realmente exibe. Os schemas são fechados: envie apenas os campos aceitos pelo ramo escolhido. Se uma rota não estiver listada, informe a indisponibilidade; não presuma outro nome.

## Pesquisa de decisões

pesquisar_decisoes recebe um único objeto busca com modo. Exemplo (híbrida, recortada por tribunal e ano):

```json
{"busca": {"modo": "hibrida", "consulta": "responsabilidade civil por vazamento de dados pessoais", "filtros": {"tribunal": "STJ", "ano_min": 2020}}}
```

Mantenha todos os filtros escolhidos em uma repetição.

| modo | Uso e filtros próprios |
|---|---|
| hibrida | Pergunta em consulta; combina significado e texto. Aceita tribunal, ano_min/ano_max e data_julgamento_min/max (AAAA-MM-DD), relator, orgao_julgador, tipo e tipo_unidade, classe e filtros CNJ, tema, OJBU (ramo_l1) e natureza_foro. |
| semantica | Consulta por significado. Aceita tribunal, um único ano, kind, ramo_l1, natureza_foro e discovery_only. Não aceita faixa de anos. |
| textual | Termos no texto em consulta; filtros de órgão, classe_sigla, anos/datas e frase_exata, mais filtros CNJ/tema. Aceita ordenar_por (relevancia, ano, tamanho) e direcao_ordenacao. |
| expressao | Regex POSIX em expressao (não em consulta); filtros de órgão, classe_sigla, anos/datas e ignorar_maiusculas. allow_unindexed_scan é opt-in explícito e o padrão é falso. |
| ontologia | filtros é obrigatório: informe ojbu_l1 (código ou slug) ou tema_transversal. L2/L3 e escopo do rótulo dependem do ramo; tema_transversal não combina com filtros de ramo. Consulte references/ontologia-ojbu.md. |
| cnj | Informe numero completo ou componentes em filtros (sequencial, ano, segmento, tribunal_cnj, origem), não ambos. Aceita ordenar_por (data, ano, recente). |

O limite padrão é 20, ajustável de 1 a 100 conforme a quantidade pedida. Para buscar mais, use page_info.next_cursor em busca.cursor e repita consulta, filtros e tamanho; pare na quantidade solicitada ou quando não houver continuação. Não percorra todas as páginas sem necessidade.

Híbrida, semântica, textual e ontológica percorrem uma janela de até três páginas, limitada a 100 resultados (60 com páginas de 20). Fim da janela ou truncated não significa fim do acervo: refine o recorte para pesquisar além dela. Cursor expirado, inválido ou ranking alterado exige reiniciar a busca; não acumule a primeira página repetida como novos resultados. Expressão e CNJ usam a paginação oferecida pelo executor; varredura sem índice pode não oferecer cursor. A consulta textual por número de processo exato, sem frase_exata nem cursor, localiza o próprio processo: ignora ordenação e tamanho_pagina e não admite tema_tipo nem discovery_only.

Comece pela modalidade adequada à pergunta. Buscas adicionais só para fato faltante, pedido exaustivo ou afirmação ainda sem suporte, não para melhorar o fraseado. Para “entendimento atual”, priorize precedentes qualificados (pesquisar_precedentes); confira o estado retornado antes de usá-los como amparo.

## Consulta por número de processo

Quando o usuário citar um número, a tabela abaixo diz a ferramenta e como passar cada forma. O CNJ incompleto tem regra própria, depois da tabela e da lista do que a busca não lê.

<!-- registro_identificadores:inicio -->
<!-- registro de identificadores, versão 3: gerado por scripts/ops/render_skill_identificadores.py --write; não editar à mão -->

| Forma citada | Tribunais | Ferramenta | Como passar | Exemplos |
|---|---|---|---|---|
| número único CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO) | todos | `pesquisar_decisoes` com `busca.modo` = `cnj` | `numero` com os 20 dígitos, com ou sem máscara. | «0000077-51.2012.4.05.8103», «00000775120124058103» |
| classe + número de registro (citação de STF, STJ e TSE) | STF, STJ, TSE | `pesquisar_decisoes` com `busca.modo` = `cnj` | `numero` como o advogado cita, com a sigla da classe antes do número. A UF final é opcional. Incidentes vêm na frente (TutPrv, AgInt, AgRgRD, AgRg, EDcl, EDv, AgRE, AgR, EAg, RCDESP, RCD, PetExe, Pet, QO, ED, ProAfR, PExt, PDist, PSusOr, ParExe, ImpExe, RtPaut, IUJur, IAC, EInf, EXC, DESIS, Acordo, OF, Embargos de decl, Emb. de decl, Emb de decl, Embargos, Emb., Emb, seguidos de nos, nas, no, na ou em) ou atrás do número (EDv, AgR, ED, MC, RG, QO, Ref). A rota alcança só STF, STJ e TSE. | «RE 1.003.433», «HC 111.840» |
| número de registro sem classe | STF, STJ, TSE | `pesquisar_decisoes` com `busca.modo` = `cnj` | `numero` só com os dígitos, com o filtro `filtros.tribunal` obrigatório. Sem ele o mesmo número pode existir no STF, no STJ e no TSE. | «126292», «1.003.433» |
| Acórdão N/AAAA do TCU | TCU | `pesquisar_decisoes` com `busca.modo` = `hibrida` | Na `consulta`, «Acórdão N/AAAA». A forma nua «N/AAAA» só vale com `filtros.tribunal` = `TCU` e nenhum outro tribunal. | «Acórdão 2622/2015», «Acórdão 1234/2019» |

Formas que a busca não lê como estão:

- máscara CNJ truncada («0001234-56.2020»): não há chave indexada para um CNJ parcial; recusa e pede os 20 dígitos. Siga a regra do CNJ incompleto, logo depois deste bloco.
- «no.» como abreviação de número («REsp no. 1.604.048»): A busca por número já corrige esta forma; chame com o texto como o usuário escreveu.
- número seguido de palavras («REsp 1.604.048 dano moral»): texto depois da citação não é citação; a gramática é ancorada. Busque só a citação; o assunto vai numa busca à parte.
- classe + número fora de STF, STJ e TSE («AC 2001.34.00.012345-0/DF»): a sigla não está na lista de classes. Peça ao usuário o CNJ de 20 dígitos.
- número com UF e sem classe («1.604.048/RS»): A busca por número já corrige esta forma; chame com o texto como o usuário escreveu.
- ano com dois dígitos («acórdão 2622/15»): o ano tem de ter quatro dígitos. Peça ao usuário o ano com quatro dígitos.
- número do processo no TCU (TC NNN.NNN/AAAA-D) («TC 012.345/2019-0»): só o número do acórdão é lido. Peça ao usuário o número do acórdão.

Nunca monte nem invente a parte que falta: o que só o usuário sabe, peça a ele.
<!-- registro_identificadores:fim -->

CNJ incompleto ou de origem desconhecida, como «0600201-63.2024»: o numero truncado é recusado. Não monte os 20 dígitos nem invente a origem (nunca «6.00.0000»). Omita numero e envie em filtros sequencial (600201), ano (2024, o do ajuizamento; o sequencial sozinho é recusado) e, se souber, segmento (o dígito J do CNJ) e tribunal_cnj. Entre os resultados, escolha o que tiver classe e tese compatíveis com o que o usuário descreveu; se mais de um servir, mostre-os e pergunte.

Uma linha que apenas cita o número no texto não é a decisão pedida. Quando signals.numero_citado vier verdadeiro, ou o aviso disser que a decisão com esse número não foi encontrada e que as decisões listadas só contêm o número, diga isso ao usuário e não apresente nenhuma delas como o julgamento do processo.

## Recusas e selos da busca

Leia error_code, busca_status (completa, parcial ou incompleta), busca_motivos, aviso_busca e filtros_ignorados antes de responder.

| Sinal | O que fazer |
|---|---|
| input_contract_refused | A entrada não foi lida (número que não normaliza, regex malformada, tipo inexistente). Reformule como a mensagem indicar e repita; não é falha do acervo. |
| filtro_nao_suportado, ou filtros_ignorados não vazio | O filtro nomeado não foi aplicado. Preserve a restrição do usuário e informe essa limitação; não apresente resultados como se o recorte tivesse valido. Só repita por outra modalidade ou fonte suportada se ela mantiver o mesmo filtro e um recorte equivalente. Se isso exigir remover ou enfraquecer a restrição, pare e pergunte ao usuário se deseja uma busca mais ampla. |
| parcial com janela_limitada | Foi vista só uma janela. Continue com page_info.next_cursor ou refine o recorte; a lista não é o conjunto. |
| incompleta, com falha_busca ou timeout | A busca não terminou. Repita uma vez com recorte mais estreito; se persistir, diga que a busca FALHOU. Nunca diga «não encontrado». |
| completa com zero resultados | Zero medido neste recorte: diga «não está no acervo» e, se vier link_pesquisa_geral, ofereça-o como a pesquisa oficial do tribunal para conferir. no_result_reason como index_gap, embedding_gap, timeout_degraded, source_error ou unattributed_empty não autoriza essa frase. |

## Ler uma decisão

Para ler uma decisão devolvida pela busca, use ler_documento com leitura.modo texto_acordao e o unit_id (UUID) exato do resultado:

```json
{"leitura": {"modo": "texto_acordao", "unit_id": "<unit_id do resultado>"}}
```

Só esse ramo abre decisões. Os campos opcionais são parte (inteiro_teor, o padrão, ou ementa), offset, versao_texto e, para ler dentro da decisão, consulta, modo_leitura, secao, janela e k. A leitura é paginada em caracteres: para continuar, repita com o next_offset devolvido e a versao_texto da página anterior, até next_offset nulo; se a resposta disser que o texto mudou, recomece do zero. O campo conteudo diz o que veio: com ementa ou texto da unidade, o inteiro teor não foi servido e votos, relator e resultado se conferem na fonte oficial (link devolvido).

Para achar o trecho num acórdão longo sem paginar tudo, ou ler só uma parte dele, leia dentro da decisão:

```json
{"leitura": {"modo": "texto_acordao", "unit_id": "<unit_id do resultado>", "consulta": "<frase ou termos>", "modo_leitura": "relevancia", "secao": "voto"}}
```

- consulta: frase ou termos, até 500 caracteres, sem diferença de acento, caixa ou espaço. A resposta traz trechos (inicio, fim, secao, texto, ocorrencias, motivo) e escopo, no lugar da página.
- modo_leitura, só com consulta: relevancia (o padrão) devolve os k trechos mais relevantes; exato procura a frase literal e devolve todas as ocorrências, contadas em total_ocorrencias (continue com next_offset e a mesma versao_texto).
- secao: cabecalho, ementa, relatorio, voto_relator, dispositivo, voto_vogal, voto_vencido, voto_vista, declaracao_voto, acordao, certidao_julgamento, assinatura e os aliases preambulo e voto; vale com ou sem consulta e só no inteiro teor. certidao_julgamento contém o resultado do julgamento (extrato da ata ou certidão). voto abrange do primeiro ao último voto, inclusive os trechos entre eles e o dispositivo que fecha o último; para um voto específico, use o rótulo correspondente. Se uma seção se repete, a consulta percorre todas as ocorrências; sem consulta, a leitura pagina uma e informa os offsets das outras. Seção não detectada responde secao_indisponivel com as seções achadas: se outra seção listada servir ao mesmo pedido, peça-a. Se só vier desconhecida (segmentação plana), ou o texto servido for ementa ou texto da unidade, declare que a seção não foi isolada; a leitura sem secao ou pela fonte oficial não comprova esse recorte.
- janela, só com consulta: contexto por trecho, de 200 a 4.000 caracteres (padrão 1.200). k, só com consulta: trechos ou ocorrências por resposta, de 1 a 50 (padrão 5 em relevancia, 20 em exato). Fora da faixa é ajustado e declarado em avisos.

Relevância só ordena trechos: não diz o papel do trecho no julgamento nem prova que algo não consta. Só o modo_leitura exato sobre o inteiro teor completo, com total_ocorrencias 0 e o aviso de que o inteiro teor não contém a frase, sustenta que uma frase não consta, e só no escopo lido: com secao, o aviso diz «na seção X» e a ausência vale só naquela seção. Com busca_status parcial (íntegra cortada) ou conteudo ementa, a ausência não está provada; de outro modo, diga que a leitura não cobriu o acórdão inteiro.

## Fundamentação dura

Dados de um julgamento (relator, redator, vencidos, votos, placar, resultado, tese, data, órgão julgador) só podem vir de um trecho que uma ferramenta devolveu nesta conversa. Sem o trecho, diga «não localizei esse dado no trecho da decisão»; nunca complete de memória, mesmo reconhecendo o caso. Se nenhuma ferramenta devolveu informação, não responda o mérito: diga que não localizou e ofereça pesquisar. Se o usuário contestar («tem certeza?», uma correção), consulte de novo pelo número completo e cite o trecho devolvido; não se esquive nem ceda sem reconsultar. O trecho de uma decisão já localizada se acha lendo-a com ler_documento (seção anterior).

## Direitos, deveres e regime

Em pergunta sobre direitos, deveres ou regime jurídico de uma categoria, busque antes a norma canônica pelo número (use a ferramenta de legislação descoberta na conexão e seu schema; se ela estiver ausente, declare a indisponibilidade) e só depois a jurisprudência sobre ela.

## Vocabulário jurídico por operação

Cada uma destas ferramentas faz uma operação de vocabulário, com campos planos. Servem para descobrir o valor certo de um filtro antes de pesquisar_decisoes. Não pesquisam nem abrem decisões, não classificam texto novo e não mostram rótulos atribuídos a um documento.

- consultar_ontologia_ojbu (formato markdown ou json; ramo opcional): resolve sigla de ramo, tema transversal ou código TPU para ojbu_l1, ojbu_l2, ojbu_l3 ou tema_transversal da modalidade ontologia (references/ontologia-ojbu.md). Sem ramo devolve a ontologia inteira; quando já se sabe a área, informe ramo.
- consultar_regras_classificacao (secao opcional: protocolo, desempate, temas, schema ou exemplos): explica como a classificação OJBU decide, para conferir ou justificar um rótulo; sem secao devolve todas.
- consultar_tipo_documental (tipo; numero e ano opcionais, e ano exige numero): dá a família e sugestões de ramo de um tipo como LEI, SUM ou PEC. Tipo desconhecido volta com nota e família presumida: é presunção, não confirmação.
- consultar_orgaos_julgadores (tribunal; trecho_nome e limite opcionais): lista turmas, câmaras e seções, das mais às menos frequentes, para preencher orgao_julgador em pesquisar_decisoes. O padrão é 50 e o máximo 200; use trecho_nome para estreitar.

Leia notas, recusas e limites do retorno. Entrada recusada (entrada_invalida) tem sempre a mensagem «Confira os campos e os limites da consulta.» e não nomeia o campo: reconfira os campos obrigatórios e as faixas no schema listado, como ano sem numero, e repita; não corrija por palpite. Resultado vazio diz só que o vocabulário não tem aquela chave neste recorte: confira a grafia, a sigla ou o tribunal e não invente código nem órgão; não conclua que o assunto, o tipo ou o órgão não existe no corpus. A lista de órgãos até o limite não é o rol completo do tribunal.

## Outras intenções

- Pesquisar tese qualificada: pesquisar_precedentes, por numero (do ato ou tema) ou consulta (matéria ou ramo, como trabalhista; não é texto livre), com filtros de tipo (súmula, SV, tema, IAC, IRDR, OJ, precedente normativo), tribunal, apenas_vinculantes e tipo_familia. Exemplo: `{"busca": {"numero": "7", "filtros": {"tribunal": "STJ", "tipo": "sumula"}}}`. Para texto livre, pesquise decisões. O limite é 10 e não há cursor. Canceladas ficam incluídas e marcadas por padrão (incluir_canceladas); a vinculatividade depende do registro.
- Pesquisar conteúdo editorial: pesquisar_informativos exige busca.tribunal (STF ou STJ) e aceita consulta e filtros de ramo, ano ou numero_informativo. O padrão é 20 notas, com limite de 1 a 50. Para continuar, repita o recorte e a quantidade com page_info.next_cursor em busca.cursor; pare na quantidade pedida. A janela recuperada cobre até três páginas, limitada a 50 notas, e seu fim não prova fim do acervo. Informativo não substitui o acórdão nem prova vinculatividade.
- Ver versões de uma tese: ver_historico_juridico exige busca.id_documento (o entity_id devolvido por uma pesquisa de precedentes). Alterações de normas ficam em consultar_alteracoes_norma.
- Explorar citações: explorar_relacoes_juridicas, com relacao.modo citacoes (id_documento ou filtros.referencia_normalizada; filtros de sentido, tipo de relação e profundidade de 1 a 3), citantes_dispositivo (quem cita uma norma ou artigo) ou dispositivos_citados (o que um documento cita), sempre com identificadores devolvidos pela busca. Não invente IDs nem converta uma relação em decisão de mérito.
- Órgãos julgadores de um tribunal (turmas, câmaras, seções), para usar no filtro orgao_julgador: consultar_orgaos_julgadores com tribunal (seção «Vocabulário jurídico por operação»). Não é uma busca de decisões.
- Consultar cobertura: use consultar_cobertura_acervo e indique o as_of retornado. Contagem de cobertura não comprova completude nem serving.
- Abrir painel: chame abrir_painel_iajus apenas se a conexão o listar e o usuário pedir o painel ou houver um resultado profundo existente que deva ser aberto. Abrir o painel não inicia pesquisa.
- Apresentar síntese (opcional): a chamada a apresentar_sintese transmite o texto da análise ao serviço remoto IAJUS, mesmo sendo uma operação de apresentação. Use somente se a conexão expuser a ferramenta, o host suportar o painel e o usuário tiver autorizado explicitamente o envio desse texto à IAJUS. Se essa autorização ainda não existir, mostre o texto a enviar, explique o destino e peça autorização antes da chamada. Um pedido de pesquisa, verificação de citações ou abertura do painel não autoriza por si só essa transmissão. Sem autorização, ou se o usuário recusar, não chame apresentar_sintese e entregue a análise normalmente no chat. Quando autorizado, envie somente o texto aprovado (até 8.192 bytes UTF-8) e, se útil, até 20 entity_ids de decisões BR retornadas na pesquisa. Use o entity_id real; não use unit_id, consulta_id ou query_id e não peça ao usuário que digite IDs. O corpus valida os metadados e descarta IDs indisponíveis; referências localizadas não confirmam mérito nem citações. A tool não pesquisa, inicia Lex, chama modelo nem lê o histórico do host. O painel só auxilia a apresentação.

Cite apenas registros, links, trechos e estados que o retorno realmente trouxer. Diferencie zero medido, erro, timeout, indisponibilidade e resultado parcial conforme os campos retornados. Consulte references/campos-e-trust.md para tratar campos de autoridade.
