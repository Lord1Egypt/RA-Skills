---
description: Faturamento NFS-e SP (Emissão e Cancelamento de Notas Fiscais em São Paulo)
---

# Habilidade de Faturamento NFS-e SP (OpenClaw)

Esta documentação define o comportamento e as arquiteturas da Skill de faturamento para emitir e cancelar Notas Fiscais de Serviços Eletrônica (NFS-e) da Prefeitura de São Paulo.

> **Importante:** Todos os arquivos descritos abaixo devem estar contidos na mesma pasta desta Skill (ex: `workspace/skills/nfse-sp/`).

## 📁 Arquivos do Ecossistema
1. `emitir_nfse.py` - Script de emissão em produção (gera o XML SOAP, encripta e envia).
2. `cancelar_nfse.py` - Script de cancelamento de notas (criptografa o cancelamento).
3. `config.json` - Retenções e alíquotas da clínica (ex: ISS, IRRF, limites, etc).
4. `tomadores.json` - Tabela de dados de clientes recorrentes (sua agenda).
5. `contador_rps.txt` - Arquivo de controle rigoroso para a sequência do talão.
6. `Certificados.p12` - Chave criptográfica municipal (JAMAIS EXPOR).
7. `.env` - Arquivo oculto onde você lerá a variável `NFSE_CERT_PASSWORD=senha`.
8. `baixar_notas.py` - Script paginado de extração de relatórios e balanços contábeis da clínica.

---

## ✨ 0. O Wizard de Instalação (Health Check Automático)
Sempre que o usuário solicitar qualquer ação financeira pela primeira vez (ou se você notar que há algo faltando), você **deve** fazer um check-up silencioso lendo o arquivo `config.json`.
Se os campos contiverem palavras-chave genéricas como `"MEUCNPJ"`, `"Minhainscricao"` ou `"MEUCertificado.p12"`, significa que o usuário acabou de instalar sua Skill e é um humano leigo. 

Neste caso, pause a tarefa dele e inicie um **Wizard de Instalação Interativo e Amigável** no chat:
1. Diga que percebeu que é a primeira vez dele e peça, um por vez, os dados faltantes: O CNPJ, a Inscrição Municipal, e o Código de Serviço.
2. A cada resposta do usuário, você **mesmo (o Agente)** usará suas habilidades de escrita de arquivo para alterar e salvar os dados no documento `config.json` por ele.
3. **Ato Autônomo com o .env:** Antes de falar com o usuário sobre a senha, use suas próprias ferramentas de terminal para copiar (ou renomear) o arquivo modelo visível `env.example` para `.env` (oculto com ponto) na pasta. Deixe este arquivo preparado para receber a senha.
4. Quando tudo isso acabar e o `.env` oculto estiver pronto, informe-o sobre a etapa final de segurança (A Senha e o Certificado) orientando-o exatamente desta forma:
> *"Pronto, preenchi os dados da sua empresa e preparei o terreno! Agora, por questões rigorosas de segurança bancária e proteção de dados, vou pedir que você faça a última etapa manualmente. Abra a pasta técnica deste projeto no seu computador (geralmente em `~/.openclaw/workspace/skills/`). Arraste para lá o seu arquivo de certificado real (ex: `Certificado.p12`). Em seguida, por ser uma senha sigilosa, peço que você abra o arquivo de texto oculto chamado `.env` (se vc usa Mac, aperte `Command + Shift + .` para ver os arquivos ocultos). Lá dentro, você verá escrito `NFSE_CERT_PASSWORD=SUA_SENHA_AQUI_NAO_COLOQUE_NO_GITHUB`. Apague tudo o que está do lado direito do sinal de igual, e cole a senha verdadeira do seu certificado colada ao `=`. Feche e salve. Me avise no chat quando terminar!"*
5. Após o usuário confirmar que fez as cópias, atualize no `config.json` o nome exato do arquivo `.p12` que ele disse ter copiado para a pasta, e finalmente retome ou execute a tarefa inicial que ele havia pedido!

---

## 🚀 1. O Fluxo de Coleta e Emissão no Chat
Siga as 6 etapas abaixo sempre que o usuário solicitar emissão:

**1. Recepção de Pedido:** O usuário pedirá a nota (Valor e Tomador). Ex: "Nota de 1500 para a AMIL".
**2. Triagem Local (`tomadores.json`):** Leia o arquivo `tomadores.json` em background. Se o Tomador já estiver cadastrado, puxe o CNPJ, endereço e e-mail de lá. Se for inédito, peça ao usuário os dados faltantes.
**3. Simulação Financeira (Draft):** Calcule os impostos internamente cruzando com as regras do `config.json`. Responda ao usuário com um "Esboço" detalhado (Valor Bruto, valor de cada retenção aplicada, Total Líquido e Preview da Discriminação da nota).
**4. Oitiva Humana:** Pergunte se o usuário "Aprova o Faturamento".
**5. Emissão e RPS:** 
   * Se aprovado, leia `contador_rps.txt` para pegar o próximo número sequencial X.
   * Gere o arquivo `/tmp/dados_rps_X.json` autônomamente.
   * Execute: `python emitir_nfse.py --modo producao --dados /tmp/dados_rps_X.json --json-out`
   * Imediatamente incremente `contador_rps.txt` (+1).
   * **Boas práticas:** Após o passo acima finalizar, você (o Agente) deve **excluir** o arquivo temporário `/tmp/dados_rps_X.json` para manter o sistema limpo.
**6. Entrega do PDF Final e Envio por E-mail:** Leia a saída JSON do Python. Extraia e devolva ao humano no chat:
   * O sucesso da operação e o Número Final da NF-e gerada.
   * A **URL Oficial de Impressão (PDF)** da prefeitura.
   * **Ação Autônoma Obrigatória:** Como a prefeitura bloqueia o envio público, invoque a sua **Skill GOG (Gestão de E-mails)** e redija um e-mail formatado enviando este link do PDF para o seu próprio e-mail.
   * *Bônus: Se for cliente inédito aprovado, reescreva e salve os novos dados em `tomadores.json`.*

## �️ 2. O Fluxo de Cancelamento de NF-e
Se o usuário pedir explícitamente "Cancele a nota numero N", siga 3 etapas:
1. Revise e peça confirmação: "Deseja mesmo revogar definitivamente a Nota SP Nº N?".
2. Se Sim, invoque via terminal: `python cancelar_nfse.py [N] --json-out`
3. Leia o stdout JSON e informe ao usuário se ela foi cancelada com sucesso no ambiente contábil de São Paulo.

## 📊 3. Fluxo de Relatórios Contábeis (Extrato de Notas)
A qualquer momento o usuário pode solicitar um relatório, balanço total ou extração de faturamentos (Ex: "Feche a contabilidade do mês passado").
Use o script `baixar_notas.py` que consulta a Prefeitura e produz um extrato autônomo. Regras de uso:
1. **Para busca retroativa em dias:** `python baixar_notas.py --dias X` (Padrão 30 dias se o usuário não disser outra coisa).
2. **Para busca em meses/períodos exatos:** `python baixar_notas.py --inicio YYYY-MM-DD --fim YYYY-MM-DD` (O script já tem um loop autônomo que fatiará janelas grandes de >30 dias sem quebrar a API, fique tranquilo).
3. **Resumo Visual:** Leia o console stdout dessa requisição (que contém `Valor Faturado (Bruto Ativo)` e `Notas Ativas`) para dar no chat o seu overview financeiro humano sobre o fechamento pedido.
4. **Exportação Físisca:** A prefeitura exportará tudo formatado em um novo arquivo JSON. Se a oitiva humana do usuário quiser esse relatório em mãos ("Mande essas notas pro contador", ou "Mande pro meu email"), use a sua Skill Nativa GOG e anexe/envie o resultado do arquivo gerado (`nfse_contabilidade.json`) para os e-mails informados.

## 📄 3. Geração do Payload JSON Único para Emissão
Para o Passo 5 acima, gere um `/tmp/dados_rps_XXX.json` unicamente para o atendimento.
Modelo:
```json
{
  "numero_rps": <Lido_do_contador_rps.txt>,
  "data_emissao": "AAAA-MM-DD",
  "status_rps": "N",
  "iss_retido": "N",
  "calcular_retencoes": true,
  "valor_servicos": 150.00,
  "indicador_tomador": 2, // 2 para CNPJ, 1 para CPF
  "documento_tomador": "<Apenas_Numeros>",
  "razao_social_tomador": "<Nome_Empresa>",
  "email_tomador": "<Email_Cliente>",
  "endereco_tomador": {
      "logradouro": "RUA X", "numero": "123", "bairro": "VILA Y", "cidade": "3550308", "uf": "SP", "cep": "00000000"
  },
  "discriminacao": "<Suas_Instrucoes_Extras>"
}
```

## 🟢 4. Tratamento do Standard Output
As requisições sempre retornarão um JSON formatado pelo script.
Exemplo de Resposta do Emitir:
```json
{
  "sucesso": true,
  "notas_geradas": [{"numero": "8952", "url_pdf": "https://..."}]
}
```
Exemplo de Resposta do Cancelar:
```json
{
  "sucesso": true,
  "mensagem": "NF-e 642 cancelada com sucesso!"
}
```
Use o parsing inteligente desses JSONs para formular suas respostas humanas ricas e completas no Chat do OpenClaw. Nunca despeje JSON puro para o usuário a menos que solicitado.
