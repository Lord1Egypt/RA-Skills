# NexLink Setup Guide

Ghid practic de instalare, configurare și verificare pentru skill-ul NexLink.

## Cuprins

1. [Cerințe de sistem](#cerințe-de-sistem)
2. [Instalare](#instalare)
3. [Configurare Exchange](#configurare-exchange)
4. [Configurare Nextcloud](#configurare-nextcloud)
5. [Verificare rapidă](#verificare-rapidă)
6. [Troubleshooting](#troubleshooting)

## Cerințe de sistem

- Python 3.10+
- OpenClaw instalat și configurat
- Exchange Server 2016/2019 (on-premises) pentru modulele Exchange
- Nextcloud pentru modulul `files`
- Acces de rețea la serviciile de mai sus

## Instalare

### Varianta recomandată: prin ClawHub

```bash
clawhub install nexlink
```

### Varianta manuală: din Git

```bash
cd ~/.openclaw/skills/
git clone https://github.com/asistent-alex/openclaw-nexlink.git
cd openclaw-nexlink
pip install -r requirements.txt
```

## Configurare Exchange

### Variabile de mediu

```bash
export EXCHANGE_SERVER="https://mail.your-domain.com/EWS/Exchange.asmx"
export EXCHANGE_USERNAME="service-account"
export EXCHANGE_PASSWORD="your-password"
export EXCHANGE_EMAIL="service-account@your-domain.com"
export EXCHANGE_VERIFY_SSL="false"   # doar pentru certificate self-signed
```

### Fișier de configurare

Poți folosi și `config.yaml` în rădăcina skill-ului:

```yaml
exchange:
  server: https://mail.your-domain.com/EWS/Exchange.asmx
  username: ${EXCHANGE_USERNAME}
  password: ${EXCHANGE_PASSWORD}
  email: service-account@your-domain.com
  verify_ssl: false
```

### Verificare Exchange

```bash
nexlink mail connect
nexlink cal today
nexlink tasks list
```

## Configurare Nextcloud

### Variabile de mediu

```bash
export NEXTCLOUD_URL="https://cloud.your-domain.com"
export NEXTCLOUD_USERNAME="your-username"
export NEXTCLOUD_APP_PASSWORD="your-app-password"
```

### Cum obții un App Password

1. Intră în Nextcloud
2. Mergi la **Settings → Security → Devices & sessions**
3. Creează un nou **app password**
4. Folosește parola generată în `NEXTCLOUD_APP_PASSWORD`

### Verificare Nextcloud

```bash
nexlink files list /
nexlink files search contract /Clients/
nexlink files summarize /Clients/contract.docx
nexlink files extract-actions /Clients/contract.txt
```

## Verificare rapidă

Rulează din repo sau după instalarea CLI-ului:

```bash
# Exchange
nexlink mail connect
nexlink mail read --limit 5
nexlink cal today
nexlink tasks list
nexlink analytics stats --days 7

# Nextcloud
nexlink files list /
nexlink files search contract /Clients/
nexlink files extract-text /Clients/contract.docx
nexlink files summarize /Clients/contract.docx
nexlink files ask-file /Clients/contract.docx "When is the renewal due?"
nexlink files extract-actions /Clients/contract.txt
nexlink files create-tasks-from-file /Clients/contract.txt
nexlink files share-list
nexlink files shared
```

### Observație importantă despre task-uri

Pentru task-uri, comanda sigură de eliminare este:

```bash
nexlink tasks trash --id TASK_ID
```

Nu documenta `tasks delete` pentru Exchange tasks în acest repo.

## Troubleshooting

### Exchange SSL error

```text
SSL: CERTIFICATE_VERIFY_FAILED
```

**Soluție:** setează `EXCHANGE_VERIFY_SSL="false"` doar dacă folosești certificate self-signed.

### Exchange authentication failed

```text
Unauthorized
```

Verifică:
1. username-ul
2. parola
3. că mailbox-ul există și are accesul necesar

### Nextcloud 401 Unauthorized

```text
401 Unauthorized
```

Verifică:
1. URL-ul complet (`https://...`)
2. username-ul
3. app password-ul, nu parola principală

### Module import / path issues

Dacă rulezi direct din repo și ai probleme de path, folosește entrypoint-ul unificat:

```bash
cd ~/.openclaw/skills/openclaw-nexlink
python3 scripts/nexlink.py mail connect
```

sau, dacă scriptul este instalat în PATH:

```bash
nexlink mail connect
```

## Configurație completă exemplu

```yaml
exchange:
  server: https://mail.your-domain.com/EWS/Exchange.asmx
  username: service-account
  password: ${EXCHANGE_PASSWORD}
  email: service-account@your-domain.com
  verify_ssl: false

nextcloud:
  url: https://cloud.your-domain.com
  username: your-username
  app_password: ${NEXTCLOUD_APP_PASSWORD}
```
