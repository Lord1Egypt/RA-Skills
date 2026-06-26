# Robô de Notas Fiscais (NFS-e São Paulo) para OpenClaw

Bem-vindo! Este pacote de arquivos foi criado para dar ao seu assistente virtual (OpenClaw) o "superpoder" de emitir, cancelar e baixar relatórios de Notas Fiscais diretamente no sistema da Prefeitura de São Paulo.

Você não precisa ser um programador para usar. Siga este passo a passo simples usando palavras do dia a dia para configurar sua clínica/empresa!

---

## 🛠️ Instalação Passo a Passo (Para Leigos)

### 1. Onde colocar a pasta do projeto?
Para que o seu robô (OpenClaw) entenda e adote essas funções financeiras, você deve colocar todos estes arquivos dentro da "Central de Habilidades" (Skills) do seu Agente.
- Geralmente, fica na pasta `workspace/skills/` (por exemplo: crie uma pasta chamada `faturamento_sp` lá dentro e jogue todos os arquivos nela).

### 2. A Mágica do "Wizard Automático" (Mais Fácil! ✨)
Sabe a parte chata de configurar arquivos cheios de códigos e números? **O seu robô agora faz isso por você!**
Nós programamos um *Assistente de Instalação (Wizard)* embutido.

Se você não quer mexer em nenhum arquivo de texto, basta fazer o seguinte:
1. Abra o chat do seu OpenClaw.
2. Diga a ele algo como: *"Emita uma Nota"* ou *"Preciso testar a skill de nota fiscal"*.
3. **Imediatamente**, o robô perceberá que este é seu primeiro acesso, pausará tudo, e vai entrevistar você no próprio chat! Ele perguntará qual o seu CNPJ, qual o seu registro na Prefeitura, e etc. Você só precisa responder conversando, e ele preencherá as configurações nos bastidores para você! 

No final da conversa, o robô pedirá apenas que você faça os **Passos 3 e 4** abaixo manualmente por rigorosas razões de segurança bancária.

---

### 3. Onde coloco o meu Certificado Digital?
Você precisará do seu certificado digital (aquele arquivo `.p12` ou `.pfx` concedido pelo governo ou seu contador).
- Pegue o seu próprio arquivo e **cole-o dentro da pasta** onde estão o resto dos arquivos do projeto. Se o robô não souber o nome do seu certificado, não tem problema: ele perguntará o nome do arquivo para você lá no chat!

### 4. Onde eu coloco a SENHA do meu Certificado?
No mundo dos desenvolvedores, colocar senha mestra diretamente no chat ou em arquivos tradicionais é perigoso. Por isso, a sua senha vai morar num arquivo "secreto" e seguro chamado **`.env`** (Sim, ele começa com um ponto final mesmo!).

- Abra esse arquivo `.env` usando o Bloco de Notas ou o editor de texto do seu computador.
- Você verá um texto assim: `NFSE_CERT_PASSWORD=SUA_SENHA_AQUI_NAO_COLOQUE_NO_GITHUB`
- Apague toda a frase da direita e digite a sua verdadeira senha **colada** ao sinal de Igual `=`.
- Ficará assim: `NFSE_CERT_PASSWORD=senha123` (Salve e feche).

*(Dica: Computadores Mac costumam esconder da sua visão arquivos que começam com um ponto para evitar que as crianças o apaguem. Se você não estiver vendo o `.env` ou o `.gitignore` na tela da sua pasta, aperte `Command + Shift + .` (Ponto) para o seu Mac revelar os arquivos fantasma!)*

---

### ⚠️ Método Alternativo: Configuração Manual (Para usuários avançados)
Se, por qualquer motivo, você não quiser conversar com o robô para ele preencher os dados, você pode fazer "na mão":
- Abra o arquivo **`config.json`**.
- Troque os campos `"MEUCNPJ"`, `"Minhainscricao"`, `"Meucodigo"`, e `"MEUCertificado.p12"` pelos seus dados reais, sempre mantendo as aspas.
- Inclusive, no final desse arquivo há o campo `"mensagem_padrao": ""`, onde você pode digitar leis ou dados bancários que sairão no rodapé de todas as notas fiscais emitidas!


### 🚀 6. Pronto pra Voar!
A sua personalização está 100% terminada.
Agora, no seu OpenClaw, o arquivo "Mestre" robótico chamado `SKILL.md` fará o elo do sistema.

Basta abrir a janela de chat do robô e dizer: *"Emita uma Nota de R$ 38.000,00 para a Clínica Exemplo usando a skill de nota fiscal!"*. A IA resgatará este manual, lerá os seus bloqueios e as senhas nas sombras e lhe devolverá pelo próprio chat o Link definitivo e impresso com sucesso validado em São Paulo!
