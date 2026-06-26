# zimage — Génération d'images IA gratuite

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>Générez des images gratuitement à partir de texte avec votre assistant IA.</strong><br>
  Compatible avec Claude Code · OpenClaw · Codex · Antigravity · Paperclip
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

## Présentation

**zimage** donne à votre assistant IA la capacité de générer des images à partir de descriptions textuelles. Il utilise [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image) — un modèle open source de 6 milliards de paramètres de l'équipe Tongyi-MAI d'Alibaba — via l'API gratuite de ModelScope.

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| Prix | **Gratuit** | 0,04–0,08 $ / image | À partir de 10 $/mois |
| Open source | Apache 2.0 | Non | Non |

> Quota gratuit : 2 000 appels API/jour au total, 500/jour par modèle ([limites officielles](https://modelscope.ai/docs/model-service/API-Inference/limits)). Les limites peuvent être ajustées dynamiquement.

---

## Configuration

### 1 — Compte Alibaba Cloud (gratuit)

Inscrivez-vous ici : **https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

Une vérification téléphonique et un moyen de paiement sont requis à l'inscription. **Z-Image est gratuit et ne vous facturera rien**, mais Alibaba Cloud exige des informations de paiement sur le compte.

### 2 — Compte ModelScope + liaison

1. Allez sur **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** → inscrivez-vous (connexion GitHub possible)
2. Dans **Paramètres → Bind Alibaba Cloud Account**, liez votre compte

### 3 — Jeton API

1. Visitez **https://modelscope.ai/my/access/token**
2. Cliquez sur **Create Your Token**
3. Copiez le jeton (format : `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

---

## Installation

<details>
<summary><b>Claude Code</b></summary>

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

```
Set my MODELSCOPE_API_KEY environment variable to ms-votre-jeton
```

Redémarrez Claude Code.
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-votre-jeton"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / Autres</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
export MODELSCOPE_API_KEY="ms-votre-jeton"
python3 imgforge.py "un coucher de soleil sur l'océan" sunset.jpg
```
</details>

---

## Utilisation

```
Génère une image d'un café chaleureux, éclairage tamisé, cinématographique
Dessine un dragon en pixel art crachant du feu
Crée un logo minimaliste, dégradés bleus
```

### CLI

```bash
python3 imgforge.py "un astronaute sur Mars" -o astronaute.jpg -W 1280 -H 720
python3 imgforge.py "art abstrait" --json
```

---

## Dépannage

| Problème | Solution |
|----------|----------|
| `MODELSCOPE_API_KEY is not set` | Complétez la [configuration](#configuration) |
| `401 Unauthorized` | Utilisez **modelscope.ai** (pas .cn). Liez Alibaba Cloud. Régénérez le jeton. |
| Timeout | API surchargée — réessayez dans une minute |

---

## Licence

MIT-0 — utilisez-le comme vous voulez, aucune attribution requise.
