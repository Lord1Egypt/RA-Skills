# zimage — Generazione gratuita di immagini con IA

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>Genera immagini gratis da testo con il tuo assistente IA.</strong><br>
  Compatibile con Claude Code · OpenClaw · Codex · Antigravity · Paperclip
</p>

<p align="center">
  <a href="../README.md">English</a> ·
  <a href="./README_TW.md">繁體中文</a> ·
  <a href="./README_JA.md">日本語</a> ·
  <a href="./README_KO.md">한국어</a> ·
  <a href="./README_ES.md">Español</a> ·
  <a href="./README_DE.md">Deutsch</a> ·
  <a href="./README_FR.md">Français</a> ·
  <a href="./README_IT.md">Italiano</a>
</p>

---

## Panoramica

**zimage** aggiunge al tuo assistente IA la capacità di generare immagini da descrizioni testuali. Utilizza [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image) — un modello open source con 6 miliardi di parametri del team Tongyi-MAI di Alibaba — tramite l'API gratuita di ModelScope.

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| Prezzo | **Gratis** | $0,04–0,08 / immagine | Da $10/mese |
| Open source | Apache 2.0 | No | No |

> Quota gratuita: 2.000 chiamate API/giorno in totale, 500/giorno per modello ([limiti ufficiali](https://modelscope.ai/docs/model-service/API-Inference/limits)). I limiti possono essere regolati dinamicamente.

---

## Configurazione

### 1 — Account Alibaba Cloud (gratis)

Registrati qui: **https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

È necessaria la verifica telefonica e un metodo di pagamento durante la registrazione. **Z-Image è gratuito e non ti verrà addebitato nulla**, ma Alibaba Cloud richiede informazioni di pagamento sull'account.

### 2 — Account ModelScope + collegamento

1. Vai su **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** → registrati (login con GitHub disponibile)
2. In **Impostazioni → Bind Alibaba Cloud Account**, collega il tuo account

### 3 — Token API

1. Visita **https://modelscope.ai/my/access/token**
2. Clicca su **Create Your Token**
3. Copia il token (formato: `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

---

## Installazione

<details>
<summary><b>Claude Code</b></summary>

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

```
Set my MODELSCOPE_API_KEY environment variable to ms-il-tuo-token
```

Riavvia Claude Code.
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-il-tuo-token"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / Altri</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
export MODELSCOPE_API_KEY="ms-il-tuo-token"
python3 imgforge.py "un tramonto sull'oceano" sunset.jpg
```
</details>

---

## Utilizzo

```
Genera un'immagine di un caffè accogliente, luce calda, cinematografico
Disegna un drago pixel art che sputa fuoco
Crea un logo minimalista, sfumature blu
```

### CLI

```bash
python3 imgforge.py "un astronauta su Marte" -o astronauta.jpg -W 1280 -H 720
python3 imgforge.py "arte astratta" --json
```

---

## Risoluzione dei problemi

| Problema | Soluzione |
|----------|----------|
| `MODELSCOPE_API_KEY is not set` | Completa la [configurazione](#configurazione) |
| `401 Unauthorized` | Usa **modelscope.ai** (non .cn). Collega Alibaba Cloud. Rigenera il token. |
| Timeout | API sovraccarica — riprova tra un minuto |

---

## Licenza

MIT-0 — usalo come vuoi, nessuna attribuzione richiesta.
