# eworm-de/routeros-scripts — Referência Completa
> GitHub: https://github.com/eworm-de/routeros-scripts
> GitLab: https://gitlab.com/eworm-de/routeros-scripts
> Docs: https://rsc.eworm.de/main/
> 1.8k ⭐ · GPL v3 · Mantido desde 2013 por Christian Hesse

Framework de scripts de produção em RouterOS puro.
**Requer RouterOS 7.17+** para o framework global-functions completo.

---

## Instalação do Framework Base

### 1. Certificado HTTPS

```routeros
# RouterOS 7.19+ — usa builtin trust anchors
/certificate/settings/set builtin-trust-anchors=trusted

# RouterOS < 7.19 — importa manualmente
/tool/fetch "https://rsc.eworm.de/main/certs/Root-YE.pem" dst-path="root-ye.pem"
/certificate/import file-name="root-ye.pem" passphrase=""
/certificate/set name="Root-YE" [ find where common-name="Root YE" ]
# Verifica fingerprint:
/certificate/print proplist=name,fingerprint \
  where fingerprint="e14ffcad5b0025731006caa43a121a22d8e9700f4fb9cf852f02a708aa5d5666"
```

### 2. Scripts base (obrigatórios)

```routeros
:foreach Script in={ "global-config"; "global-config-overlay"; "global-functions" } do={
  /system/script/add name=$Script owner=$Script \
    source=([ /tool/fetch check-certificate=yes-without-crl \
    ("https://rsc.eworm.de/main/" . $Script . ".rsc") output=user as-value ]->"data");
}
/system/script { run global-config; run global-functions; }
```

### 3. Scheduler de boot

```routeros
# Carrega config e funções no boot
/system/scheduler/add name="global-scripts" start-time=startup \
  on-event="/system/script { run global-config; run global-functions; }"

# Auto-update diário dos scripts (opcional)
/system/scheduler/add name="ScriptInstallUpdate" start-time=startup interval=1d \
  on-event=":global ScriptInstallUpdate; \$ScriptInstallUpdate;"
```

### 4. Instalar scripts

```routeros
# Um script
$ScriptInstallUpdate netwatch-notify

# Vários de uma vez
$ScriptInstallUpdate check-routeros-update,check-health,backup-upload,mod/notification-telegram
```

---

## Catálogo Completo de Scripts

### 💾 Backup

| Script | Função |
|--------|--------|
| `backup-cloud` | Upload de backup para MikroTik Cloud |
| `backup-email` | Envia backup por e-mail |
| `backup-partition` | Salva config na partição fallback (dual-boot) |
| `backup-upload` | Upload de backup para servidor via SCP/FTP |

```routeros
$ScriptInstallUpdate backup-upload
# Configurar destino no global-config-overlay:
# :global BackupUploadUrl "sftp://user:pass@servidor/path/"
# :global BackupSendBinary true
# :global BackupSendExport true

/system/scheduler/add name=backup-upload interval=1d start-time=startup \
  on-event="/system/script/run backup-upload;"
```

---

### 🔔 Monitoramento & Saúde

| Script | Função |
|--------|--------|
| `check-health` | Notifica sobre saúde do sistema (CPU, RAM, temp, tensão) |
| `check-routeros-update` | Notifica quando há atualização de RouterOS disponível |
| `check-certificates` | Renova e notifica sobre expiração de certificados |
| `check-lte-firmware-upgrade` | Notifica sobre upgrade de firmware LTE |
| `check-perpetual-license` | Verifica licença perpetual em CHR |

```routeros
$ScriptInstallUpdate check-health,check-routeros-update

/system/scheduler/add name=check-health interval=1m start-time=startup \
  on-event="/system/script/run check-health;"
/system/scheduler/add name=check-routeros-update interval=1d start-time=startup \
  on-event="/system/script/run check-routeros-update;"
```

---

### 📡 Netwatch & Failover

#### `netwatch-notify` — Monitoramento de hosts com máquina de estado ⭐

**Substituto profissional ao FAILOVER_ACTIONS simples.** Implementa state machine com threshold de contagem e modelo de dependência pai/filho.

```routeros
$ScriptInstallUpdate netwatch-notify

# Scheduler a cada 1 minuto
/system/scheduler/add interval=1m name=netwatch-notify start-time=startup \
  on-event="/system/script/run netwatch-notify;"

# Hosts a monitorar (comentário controla comportamento)
/tool/netwatch/add comment="notify, name=FIBRA-PRINCIPAL" host=8.8.8.8
/tool/netwatch/add comment="notify, name=LINK-BACKUP, count=3" host=1.1.1.1
/tool/netwatch/add comment="notify, name=CLIENTE-01, parent=FIBRA-PRINCIPAL" host=10.0.0.1
/tool/netwatch/add comment="notify, name=SERVER, count=5, no-down-notification" host=10.0.0.10

# Parâmetros disponíveis no comentário:
# name=<nome>               — nome na notificação (obrigatório)
# count=<N>                 — alertar só após N falhas consecutivas (padrão: 5)
# parent=<nome>             — suprimir alerta se host pai estiver down
# no-down-notification      — não notifica queda, só retorno
# resolve=<hostname>        — atualiza IP dinamicamente via DNS
# link=<url>                — adiciona link clicável na notificação
# note=<texto>              — nota extra incluída na notificação
# silent                    — grava log sem enviar notificação
# up-hook=<comando>         — executa comando quando host sobe
# down-hook=<comando>       — executa comando quando host cai
```

#### `netwatch-dns` — Failover de DNS / DoH

```routeros
$ScriptInstallUpdate netwatch-dns
# Troca automaticamente o servidor DNS/DoH quando principal cai
```

---

### 🌐 DHCP & DNS

| Script | Função |
|--------|--------|
| `dhcp-to-dns` | Cria registros DNS estáticos para cada lease DHCP |
| `dhcp-lease-comment` | Comenta leases DHCP com info do access list |
| `lease-script` | Executa scripts em eventos de lease DHCP |
| `ipsec-to-dns` | Atualiza DNS para peers IPsec dinâmicos |

```routeros
$ScriptInstallUpdate dhcp-to-dns,lease-script
/ip/dhcp-server/set lease-script=lease-script [ find ]
/system/scheduler/add name="dhcp-to-dns" interval=5m start-time=startup \
  on-event="/system/script/run dhcp-to-dns;"
```

---

### 🔥 Firewall

| Script | Função |
|--------|--------|
| `fw-addr-lists` | Baixa e importa blocklists de fontes externas |
| `accesslist-duplicates` | Encontra e remove duplicatas no access list wireless |

```routeros
$ScriptInstallUpdate fw-addr-lists
/system/scheduler/add name=fw-addr-lists interval=1d start-time=startup \
  on-event="/system/script/run fw-addr-lists;"
```

---

### 📱 PPP / ISP

| Script | Função |
|--------|--------|
| `ppp-on-up` | Executa scripts quando conexão PPP/PPPoE sobe |
| `update-gre-address` | Atualiza config GRE com IPs dinâmicos |
| `update-tunnelbroker` | Atualiza configuração tunnelbroker (IPv6) |

```routeros
$ScriptInstallUpdate ppp-on-up
/ppp/profile/set default on-up="/system/script/run ppp-on-up"
# Configurar no global-config-overlay:
# :global PppOnUpScripts { "meu-script-de-failover" }
```

---

### 📶 WiFi & CAPsMAN

| Script | Função |
|--------|--------|
| `capsman-download-packages` | Download automático de pacotes CAP via CAPsMAN |
| `capsman-rolling-upgrade` | Upgrade sequencial de CAPs via CAPsMAN |
| `collect-wireless-mac` | Coleta MACs no access list wireless |
| `daily-psk` | Rotaciona PSK do wireless diariamente |
| `hotspot-to-wpa` | Usa rede WPA2 com credenciais do hotspot |
| `hotspot-to-wpa-cleanup` | Limpa registros hotspot-to-wpa |

---

### 🔑 Certificados

| Script | Função |
|--------|--------|
| `certificate-renew-issued` | Renova certificados emitidos localmente |
| `check-certificates` | Renova e notifica sobre expiração |

---

### 🔧 Sistema

| Script | Função |
|--------|--------|
| `firmware-upgrade-reboot` | Upgrade automático de firmware e reboot |
| `packages-update` | Gerencia atualização de pacotes RouterOS |
| `unattended-lte-firmware-upgrade` | Upgrade automático de firmware LTE |
| `global-wait` | Aguarda global-functions e módulos estarem prontos |
| `gps-track` | Envia posição GPS para servidor |
| `ospf-to-leds` | Visualiza estado OSPF via LEDs do device |
| `sms-action` | Executa ações baseado em SMS recebido |
| `sms-forward` | Encaminha SMS recebido |
| `log-forward` | Encaminha log via notificação |
| `telegram-chat` | Chat bidirecional com o roteador via Telegram |
| `super-mario-theme` | Toca tema do Super Mario (🎵 fun!) |

---

## Módulos (mod/)

Instalados automaticamente quando chamados por outros scripts.

| Módulo | Função |
|--------|--------|
| `mod/notification-telegram` | **Notificações via Telegram** ← mais usado |
| `mod/notification-email` | Notificações por e-mail |
| `mod/notification-gotify` | Notificações via Gotify |
| `mod/notification-matrix` | Notificações via Matrix |
| `mod/notification-ntfy` | Notificações via Ntfy |
| `mod/bridge-port-to` | Gerencia portas em bridges |
| `mod/bridge-port-vlan` | Gerencia VLANs em bridge ports |
| `mod/ipcalc` | Calculadora de sub-redes em RouterOS script |
| `mod/inspectvar` | Debug de variáveis em scripts |

---

## Configuração do Telegram

```routeros
# Instalar módulo
$ScriptInstallUpdate mod/notification-telegram

# Editar overlay de configuração
/system/script/edit global-config-overlay source

# Adicionar (copiar de global-config, seção Telegram):
:global TelegramTokenId "123456789:AAABBB..."
:global TelegramChatId "-1001234567890"

# Salvar (Ctrl+O) e recarregar
/system/script/run global-config-overlay

# Testar
:global SendNotification2
$SendNotification2 ({subject="Teste"; message="Olá do RouterOS!"})
```

---

## Comparação: FAILOVER_ACTIONS simples vs netwatch-notify

| Feature | FAILOVER_ACTIONS (nosso) | netwatch-notify (eworm) |
|---------|------------------------|------------------------|
| Threshold de falhas | ❌ alerta na 1ª falha | ✅ count=N configurável |
| Dependência pai/filho | ❌ | ✅ parent=nome |
| Múltiplos canais | ❌ | ✅ Telegram, Email, Ntfy, Matrix, Gotify |
| DNS dinâmico do host | ❌ | ✅ resolve=hostname |
| Hooks up/down | ❌ | ✅ up-hook, down-hook |
| Auto-atualização | ❌ | ✅ via $ScriptInstallUpdate |
| WhatsApp | ✅ (Evolution API) | ❌ |
| Google Sheets | ✅ | ❌ |
| Complexidade setup | Baixa | Média (precisa framework) |

**Recomendação:**
- Links simples + WhatsApp/Sheets → `FAILOVER_ACTIONS` (references/failover-notifications.md)
- ISP com múltiplos links, hierarquia, múltiplos canais → `netwatch-notify`

---

## URLs de Referência

| Recurso | URL |
|---------|-----|
| Site oficial | https://rsc.eworm.de/main/ |
| GitHub | https://github.com/eworm-de/routeros-scripts |
| GitLab | https://gitlab.com/eworm-de/routeros-scripts |
| Script direto | `https://rsc.eworm.de/main/<nome>.rsc` |
| Doc de um script | `https://rsc.eworm.de/doc/<nome>.md` |
| Scripts custom | https://gitlab.com/eworm-de/routeros-scripts-custom |
