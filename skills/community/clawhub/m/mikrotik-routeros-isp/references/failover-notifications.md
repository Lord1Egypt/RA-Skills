# Failover Actions + Notificações (Telegram, WhatsApp, Google Sheets)

Scripts para monitorar links e enviar alertas automáticos quando ocorre failover.
Compatível com Netwatch (V6/V7), rota flutuante e load balance.

---

## Como funciona

O RouterOS detecta queda/subida de link via **Netwatch** ou **rota flutuante**.
Nos eventos `ifdown` / `ifup`, ele seta variáveis globais e chama o script de actions.

### Variáveis globais usadas pelos scripts

| Variável | Quem seta | Descrição |
|----------|-----------|-----------|
| `$comentario` | netwatch / rota | Nome do link (ex: "FIBRA PRINCIPAL") |
| `$LinkState` | netwatch / rota | `1` = UP, `0` = DOWN |
| `$LinkStatus` | FAILOVER_ACTIONS | Texto "UP" ou "DOWN" |
| `$emoji` | FAILOVER_ACTIONS | 🟢 (UP) ou 🔴 (DOWN) |
| `$botToken` | script | Token do bot Telegram |
| `$groupID` | script | Chat ID do Telegram |
| `$urlGoogleSheets` | script | URL do Apps Script (Google Sheets) |

---

## Integração com Netwatch

### RouterOS V6 — ifdown / ifup
```routeros
/ip/netwatch/add host=8.8.8.8 interval=5s timeout=1s \
    down-script=":global comentario \"FIBRA PRINCIPAL\"; :global LinkState 0; /system script run FAILOVER_ACTIONS" \
    up-script=":global comentario \"FIBRA PRINCIPAL\"; :global LinkState 1; /system script run FAILOVER_ACTIONS"
```

### RouterOS V7 — ifdown / ifup
```routeros
/ip/netwatch/add host=8.8.8.8 interval=5s timeout=1s \
    down-script=":global comentario \"FIBRA PRINCIPAL\"; :global LinkState 0; execute {/system script run FAILOVER_ACTIONS}" \
    up-script=":global comentario \"FIBRA PRINCIPAL\"; :global LinkState 1; execute {/system script run FAILOVER_ACTIONS}"
```

> V7: use `execute { }` em vez de chamar direto — garante contexto limpo de execução.

---

## Script FAILOVER_ACTIONS — Telegram + Google Sheets

### Versão V6 (comando sem `/`)
```routeros
/system script
add name=FAILOVER_ACTIONS policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon \
source={
#=======================================================================
# =============== VARIAVEIS GERAIS =====================================
#=======================================================================
:global comentario
:global LinkStatus
:global LinkState
:local LinkStateActions $LinkState
:global emoji
:global routerName [/system identity get name]
:if ($LinkStateActions > 0) do={:global emoji "%F0%9F%9F%A2"; :global LinkStatus "UP"} \
    else={:global emoji "%F0%9F%94%B4"; :global LinkStatus "DOWN"}

#=======================================================================
#=============== GERAR LOG =============================================
#=======================================================================
/log warning message=("LINK: $comentario -- STATUS: $LinkStatus ")

#=======================================================================
#=============== ENVIO DE AVISO NO TELEGRAM ============================
#=======================================================================
:global botToken "SEU_TOKEN_AQUI"
:global groupID "SEU_CHAT_ID_AQUI"
:delay 2
/tool fetch url=("https://api.telegram.org/bot" . $botToken . "/sendMessage?chat_id=" . $groupID . \
    "&parse_mode=HTML&text=" . \
    $emoji . $emoji . $emoji . $emoji . $emoji . $emoji . $emoji . "%0A%0A" . \
    "<b>ROTEADOR:</b> " . $routerName . " %0A%0A" . \
    "<b>LINK:</b> " . $comentario . " %0A%0A" . \
    "<b>STATUS:</b> " . $LinkStatus . " %0A" . \
    "____________________________") keep-result=no

#=======================================================================
#=============== ENVIO GOOGLE SHEETS ===================================
#=======================================================================
:global urlGoogleSheets "URL_DO_APPS_SCRIPT_AQUI"
:global sheetName "REGISTROS"
/tool fetch http-method=post http-header-field="Content-Type: application/json" \
    url=$urlGoogleSheets \
    http-data=("{\"sheet\":\"" . $sheetName . "\",\"ROTEADOR\":\"" . $routerName . \
               "\",\"LINK\":\"" . $comentario . "\",\"STATUS\":\"" . $LinkStatus . "\"}")
}
```

### Versão V7 (comandos com `/`)
```routeros
# Diferença do V6: /log/warning e /tool/fetch (com barra)
/log/warning message=("LINK: $comentario -- STATUS: $LinkStatus ")
/tool/fetch url=(...) keep-result=no
/tool fetch http-method=post ...
```

---

## Versão Load Balance — Diferença chave

No load balance, o comentário da rota costuma ter sufixo `#N` (ex: `"FIBRA PRINCIPAL#1"`).
O script limpa o sufixo antes de enviar:

```routeros
:global comentario
# Remove tudo após o "#" para exibir só o nome do link
:local comentarioActions [pick $comentario 0 [find in=$comentario key="#"]]

# Usar $comentarioActions no lugar de $comentario para Telegram/Sheets
```

---

## Script FAILOVER_WPP — WhatsApp via Evolution API

### Pré-requisito: Evolution API rodando via Docker

```yaml
# docker-compose.yml (simplificado)
services:
  evolution_api:
    image: atendai/evolution-api:v2.2.3
    ports:
      - "8080:8080"
    environment:
      - SERVER_URL=http://<seu-ip>
      - AUTHENTICATION_TYPE=apikey
      - AUTHENTICATION_API_KEY=<sua-api-key>
      - DATABASE_ENABLED=true
      - DATABASE_PROVIDER=postgresql
      - DATABASE_CONNECTION_URI=postgresql://postgres:postgres@postgres:5432/evolution?schema=public
  postgres:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=evolution
```

Após subir, criar instância via API:
```bash
curl -X POST http://<ip>:8080/instance/create \
  -H "Content-Type: application/json" \
  -H "apikey: <sua-api-key>" \
  -d '{"instanceName":"failover","qrcode":true}'
# Escanear o QR code para conectar o WhatsApp
```

### Script RouterOS — Envio WhatsApp
```routeros
/system script
add name=FAILOVER_WPP policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon \
source={
:global comentario
:local comentarioActions $comentario
:global LinkStatus
:global LinkState
:local LinkStateActions $LinkState
:global emoji
:global routerName [/system identity get name]

:if ($LinkStateActions > 0) do={:global emoji "U+1F7E2"; :global LinkStatus "UP"} \
    else={:global emoji "U+1F534"; :global LinkStatus "DOWN"}

:global TextoEnvio ("*ROTEADOR:* " . $routerName . "\\n\\n*LINK:* " . $comentario . "\\n\\n*STATUS:* " . $LinkStatus)

#=============== GERAR LOG =============================================
/log warning message=("LINK: $comentario -- STATUS: $LinkStatus ")

#=============== ENVIO DE AVISO NO WHATSAPP ============================
:delay 2
/tool fetch mode=http http-method=post \
    http-header-field="Content-Type: application/json, apikey: SUA_API_KEY_AQUI" \
    http-data=("{\"number\": \"55XXXXXXXXXXX\", \"text\": \"" . $TextoEnvio . "\"}") \
    url="http://<evolution-ip>:8080/message/sendText/failover"
}
```

### Integração Netwatch (WPP — V6)
```routeros
/ip/netwatch/add host=8.8.8.8 interval=5s \
    down-script=":global comentario \"FIBRA\"; :global LinkState 0; /system script run FAILOVER_WPP" \
    up-script=":global comentario \"FIBRA\"; :global LinkState 1; /system script run FAILOVER_WPP"
```

---

## Google Sheets — Apps Script

Planilha modelo: https://docs.google.com/spreadsheets/d/1SuYyxqMlYcm8-fAahs3irtxXjJWmZklX2fAYUG4J9yY/edit

O Apps Script recebe POST JSON com campos: `sheet`, `ROTEADOR`, `LINK`, `STATUS`.
Substituir `urlGoogleSheets` pela URL de deploy do Web App (Extensions → Apps Script → Deploy).

---

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Telegram não chega | Token/groupID errado | Testar com `curl` do PC |
| V7 não executa | Usar `execute {}` no netwatch | Ver seção V7 acima |
| WPP não envia | Instância não conectada | Verificar QR code / status da instância |
| Sufixo `#1` no nome do link | Load balance com comentário numerado | Usar versão load balance do script |
| `$comentario` vazio | Global não setada antes de chamar script | Setar no ifdown/ifup do netwatch |
