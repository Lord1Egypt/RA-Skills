---
name: iajus-verificar-citacoes
description: Verifica uma a uma citações de decisões, precedentes e normas contra
  registros e fontes disponíveis. Use para checar existência, fidelidade e vigência;
  não use para pesquisar do zero.
version: 3.0.19
license: MIT-0
---

Os arquivos desta skill são distribuídos sob [MIT-0](LICENSE). Essa licença não licencia o serviço hospedado, o corpus ou os dados. O MCP hospedado continua sujeito aos planos, autenticação, limites, preços e termos IAJUS ([termos](https://iajus.com.br/termos)). Instalar a skill não concede acesso gratuito ao serviço.

Use a conexão `iajus` para jurisprudência e legislação brasileiras. Endpoint: https://mcp.iajus.com.br/mcp.

# Verificar citações jurídicas

Use somente as ferramentas e schemas descobertos na conexão `iajus` do OpenClaw. Os nomes abaixo identificam operações; não são aliases a presumir. Se a conexão retornar 401, oriente o operador pelo [guia de conexão](README.md); não execute login nem peça tokens ou senhas. Recusa de permissão ou plano exige informar o limite devolvido. Ferramenta ausente deve ser declarada indisponível, sem inventar nomes ou responder o mérito jurídico de memória.

Confira cada citação separadamente contra ferramentas e schemas listados nesta conexão. Se a rota necessária não estiver disponível, informe a limitação em vez de presumir outro nome.

| Citação | Rota quando listada |
|---|---|
| Processo por número | `pesquisar_decisoes` com busca.modo cnj: CNJ de 20 dígitos ou número legado como citado («REsp 1.604.048/RS», «RE 1.003.433»); as formas aceitas estão em [pesquisar-jurisprudencia](references/pesquisar-jurisprudencia/README.md). CNJ incompleto: filtros sequencial e ano (e segmento), sem inventar a origem. |
| Súmula, tema ou outro precedente qualificado | `pesquisar_precedentes` por numero/tribunal; use `ver_historico_juridico` com id_documento devolvido quando a redação ou vigência exigir histórico. |
| Acórdão citado por tese ou ementa | `pesquisar_decisoes` em modo hibrida, semantica ou textual, com os filtros pertinentes. |
| Trecho que se atribui a uma decisão | `ler_documento` com leitura.modo texto_acordao e o unit_id devolvido pela busca (ver abaixo). |
| Informativo STF/STJ citado | `pesquisar_informativos` com tribunal, consulta e, se citado, ano ou numero_informativo. |
| Norma ou dispositivo legal | `pesquisar_normas` por nome/número; `localizar_norma_fonte_oficial` para localização e `consultar_alteracoes_norma` para alterações federais; `pesquisar_artigos` para localizar um dispositivo; `ler_documento` para ler a norma ou dispositivo identificado. |
| Relação de citações | `explorar_relacoes_juridicas` somente depois de obter o identificador pelo resultado de busca. |

Confirme identidade e conteúdo pelo registro retornado. Preserve link oficial, órgão, número, data, redação e situação exatamente como aparecem. Declare CONFIRMADA somente quando a fonte sustentar a referência e a afirmação do texto. Declare DESATUALIZADA apenas com evidência de versão ou estado adverso. Use NÃO LOCALIZADA somente após uma busca concluída e medida; use NÃO VERIFICÁVEL quando houver erro, indisponibilidade, limite, retorno parcial ou falta de fonte/conteúdo suficiente.

Um status ausente não confirma vigência; ausência de histórico não prova que não houve alteração. Um zero sem indicador de medição não prova inexistência. Erro, falha, timeout, retorno parcial e medição indisponível deixam a citação não verificável; só o zero medido, com a busca concluída, sustenta NÃO LOCALIZADA.

Reaja aos sinais da busca como em [pesquisar-jurisprudencia](references/pesquisar-jurisprudencia/README.md): input_contract_refused, corrija a entrada; filtro_nao_suportado ou filtros_ignorados, preserve a restrição e informe que ela não foi aplicada. Só repita por modalidade ou fonte suportada com recorte equivalente; remover ou enfraquecer a restrição exige a escolha do usuário; parcial com janela_limitada, continue pelo cursor; incompleta com falha_busca ou timeout, repita uma vez mais estreito e, persistindo, declare NÃO VERIFICÁVEL, nunca NÃO LOCALIZADA. Completa com zero resultados é NÃO LOCALIZADA neste recorte; ofereça link_pesquisa_geral quando vier. Uma linha que apenas cita o número (signals.numero_citado ou aviso equivalente) não é a decisão citada.

Dados de julgamento (relator, redator, vencidos, votos, placar, resultado, tese, data, órgão) só valem se vierem de um trecho devolvido nesta conversa; sem ele, escreva «não localizei esse dado no trecho da decisão», nunca de memória. Se o usuário contestar o veredito, reconsulte pelo número completo e cite o trecho.

Faça uma verificação direcionada por citação. Chamadas adicionais só para completar existência, fidelidade ou vigência, ou esgotar alternativas pertinentes após vazio medido; preserve a referência e os filtros. Não repita consultas apenas para melhorar o fraseado do veredito. Entregue veredito por citação e resumo dos vereditos; sinalize os ajustes e só reescreva o texto quando solicitado.

## Conferir o que a decisão diz

Para conferir se uma decisão diz o que o texto atribui a ela, leia-a com ler_documento:

```json
{"leitura": {"modo": "texto_acordao", "unit_id": "<unit_id devolvido pela busca>", "parte": "inteiro_teor"}}
```

A leitura é paginada em caracteres: continue com o next_offset e a mesma versao_texto até next_offset nulo, e recomece do zero se a resposta disser que o texto mudou. O campo conteudo diz o que veio; parte ementa devolve só a ementa.

Para achar a frase citada num acórdão longo sem paginar tudo, leia dentro da decisão:

```json
{"leitura": {"modo": "texto_acordao", "unit_id": "<unit_id devolvido pela busca>", "consulta": "<frase citada>", "modo_leitura": "exato"}}
```

consulta (até 500 caracteres, sem diferença de acento, caixa ou espaço, mas a pontuação conta) devolve trechos e escopo no lugar da página. Em exato, procure o trecho literal mais longo da citação sem marcas de omissão ((...), [...]) nem aspas: com elas o exato dá 0 e o servidor avisa que o inteiro teor não contém a frase, mesmo que a decisão a traga. modo_leitura, só com consulta: exato procura a frase literal e conta todas as ocorrências em total_ocorrencias; relevancia (o padrão) devolve os k trechos mais relevantes e não prova ausência. Também aceitos: secao (só no inteiro teor; valores e escopo dos aliases em [pesquisar-jurisprudencia](references/pesquisar-jurisprudencia/README.md)), janela e k, os dois só com consulta; os limites estão em [pesquisar-jurisprudencia](references/pesquisar-jurisprudencia/README.md). CONFIRMADA exige o trecho devolvido. Só o modo exato sobre o inteiro teor completo sustenta que a decisão não traz a frase (total_ocorrencias 0 e o aviso de que o inteiro teor não contém a frase), e antes de concluir ausência a partir de um zero confirme com modo_leitura relevancia: se ele devolver o trecho, a frase consta. Uma busca com secao prova ausência só naquela seção (o aviso diz «na seção X»); para afirmar que a decisão não traz a frase, repita sem secao. Se a leitura parou antes do fim, busca_status veio parcial, veio só a ementa ou o inteiro teor não foi servido, a citação fica NÃO VERIFICÁVEL.
