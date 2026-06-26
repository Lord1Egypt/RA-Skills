# zimage — Generación gratuita de imágenes con IA

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>Genera imágenes gratis con texto desde tu asistente de programación con IA.</strong><br>
  Compatible con Claude Code · OpenClaw · Codex · Antigravity · Paperclip
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

## Descripción

**zimage** añade a tu asistente de IA la capacidad de generar imágenes a partir de texto. Utiliza [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image), un modelo de código abierto con 6.000 millones de parámetros del equipo Tongyi-MAI de Alibaba, a través de la API gratuita de ModelScope.

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| Precio | **Gratis** | $0,04–0,08 / imagen | Desde $10/mes |
| Código abierto | Apache 2.0 | No | No |

> Cuota gratuita: 2.000 llamadas API/día en total, 500/día por modelo ([límites oficiales](https://modelscope.ai/docs/model-service/API-Inference/limits)). Los límites pueden ajustarse dinámicamente.

---

## Configuración

### 1 — Cuenta Alibaba Cloud (gratis)

Regístrate en: **https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

Se requiere verificación telefónica y un método de pago al registrarse. **Z-Image es gratis y no se te cobrará**, pero Alibaba Cloud requiere información de pago en la cuenta.

### 2 — Cuenta ModelScope + vinculación

1. Ve a **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** → regístrate (login con GitHub disponible)
2. En **Configuración → Bind Alibaba Cloud Account**, vincula tu cuenta

### 3 — Token API

1. Visita **https://modelscope.ai/my/access/token**
2. Haz clic en **Create Your Token**
3. Copia el token (formato: `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

---

## Instalación

<details>
<summary><b>Claude Code</b></summary>

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

```
Set my MODELSCOPE_API_KEY environment variable to ms-tu-token
```

Reinicia Claude Code.
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-tu-token"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / Otros</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
pip install Pillow  # opcional
export MODELSCOPE_API_KEY="ms-tu-token"
python3 imgforge.py "una puesta de sol sobre el océano" sunset.jpg
```
</details>

---

## Uso

```
Genera una imagen de una cafetería acogedora, iluminación cálida, cinematográfica
Dibuja un dragón pixel art lanzando fuego
Crea un logo minimalista, gradientes azules
```

### CLI

```bash
python3 imgforge.py "un astronauta en Marte" -o astronauta.jpg -W 1280 -H 720
python3 imgforge.py "arte abstracto" --json
```

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| `MODELSCOPE_API_KEY is not set` | Completa la [configuración](#configuración) |
| `401 Unauthorized` | Usa **modelscope.ai** (no .cn). Vincula Alibaba Cloud. Regenera el token. |
| Timeout | API con carga alta — reintenta en un minuto |

---

## Licencia

MIT-0 — úsalo como quieras.
