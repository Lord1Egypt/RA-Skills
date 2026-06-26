# zimage — Kostenlose KI-Bildgenerierung

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>Generiere kostenlos Bilder aus Text mit deinem KI-Programmierassistenten.</strong><br>
  Kompatibel mit Claude Code · OpenClaw · Codex · Antigravity · Paperclip
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

## Überblick

**zimage** gibt deinem KI-Assistenten die Fähigkeit, Bilder aus Textbeschreibungen zu generieren. Es nutzt [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image) — ein Open-Source-Modell mit 6 Milliarden Parametern vom Tongyi-MAI-Team bei Alibaba — über die kostenlose ModelScope-API.

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| Preis | **Kostenlos** | $0,04–0,08 / Bild | Ab $10/Monat |
| Open Source | Apache 2.0 | Nein | Nein |

> Kostenloses Kontingent: 2.000 API-Aufrufe/Tag gesamt, 500/Tag pro Modell ([offizielle Limits](https://modelscope.ai/docs/model-service/API-Inference/limits)). Limits können dynamisch angepasst werden.

---

## Einrichtung

### 1 — Alibaba Cloud Konto (kostenlos)

Registriere dich hier: **https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

Bei der Registrierung sind eine Telefonnummer-Verifizierung und eine Zahlungsmethode erforderlich. **Z-Image selbst ist kostenlos und verursacht keine Kosten**, aber Alibaba Cloud verlangt Zahlungsinformationen im Konto.

### 2 — ModelScope Konto + Verknüpfung

1. Gehe zu **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** → registriere dich (GitHub-Login möglich)
2. Unter **Einstellungen → Bind Alibaba Cloud Account** dein Konto verknüpfen

### 3 — API-Token

1. Besuche **https://modelscope.ai/my/access/token**
2. Klicke auf **Create Your Token**
3. Kopiere den Token (Format: `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

---

## Installation

<details>
<summary><b>Claude Code</b></summary>

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

```
Set my MODELSCOPE_API_KEY environment variable to ms-dein-token
```

Claude Code neu starten.
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-dein-token"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / Andere</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
export MODELSCOPE_API_KEY="ms-dein-token"
python3 imgforge.py "ein Sonnenuntergang über dem Meer" sunset.jpg
```
</details>

---

## Nutzung

```
Erstelle ein Bild von einem gemütlichen Café, warmes Licht, filmisch
Zeichne einen Pixel-Art-Drachen, der Feuer speit
Erstelle ein minimalistisches Logo, blaue Farbverläufe
```

### CLI

```bash
python3 imgforge.py "ein Astronaut auf dem Mars" -o astronaut.jpg -W 1280 -H 720
python3 imgforge.py "abstrakte Kunst" --json
```

---

## Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| `MODELSCOPE_API_KEY is not set` | [Einrichtung](#einrichtung) abschließen |
| `401 Unauthorized` | **modelscope.ai** verwenden (nicht .cn). Alibaba Cloud verknüpfen. Token erneuern. |
| Timeout | API ausgelastet — in einer Minute erneut versuchen |

---

## Lizenz

MIT-0 — frei verwendbar, keine Namensnennung erforderlich.
