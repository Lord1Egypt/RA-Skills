# Pesquisar por OJBU

Use pesquisar_decisoes com busca.modo ontologia quando esse nome estiver listado. O recorte fica em busca.filtros:

- ojbu_l1 aceita código positivo ou slug e é obrigatório salvo quando tema_transversal for usado.
- ojbu_l2 e ojbu_l3 são códigos positivos; informe ojbu_l1 junto.
- tema_transversal é um recorte alternativo. Não o misture com filtros de ramo, escopo, relator ou classificação principal.
- tribunal, anos, escopo_rotulo, somente_principal e relator só se aplicam conforme o ramo descrito pelo schema.
- Pesquisar um conceito amplo sem seleção OJBU é outra intenção: use hibrida ou semantica em vez de presumir um código.

Para resolver classificações existentes, use consultar_ontologia_ojbu, com campos planos: ramo aceita a sigla do ramo, o tema transversal ou o código TPU, e formato aceita markdown (padrão) ou json. Exemplo: `{"ramo": "DCV", "formato": "json"}`. Sem ramo a ontologia vem inteira; prefira informar ramo. Para as regras de classificação use consultar_regras_classificacao (secao: protocolo, desempate, temas, schema ou exemplos); para a família e sugestões de ramo de um tipo documental (como LEI, SUM ou PEC, com numero e ano opcionais), consultar_tipo_documental. Não adivinhe códigos nem trate um rótulo sem resultado como ausência do assunto no corpus. Resultado vazio ou entrada_invalida pede nova grafia ou campo corrigido, nunca um código presumido.

Use as ferramentas e schemas disponíveis nesta conexão; se uma rota estiver indisponível, informe a limitação.
