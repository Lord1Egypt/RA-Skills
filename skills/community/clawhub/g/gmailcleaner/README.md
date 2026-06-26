# 📬 OpenClaw Email Skills v2 — con gog CLI

Pack de 6 skills para OpenClaw que gestionan completamente tu Gmail
usando el CLI `gog` (Google Workspace CLI) como backend nativo.

> **v2.0** — Reescritas para usar `gog` en lugar de scripts Python.
> Más simples, más rápidas, sin dependencias extras.

---

## Skills incluidas

| Skill | Emoji | Función |
|-------|-------|---------|
| `email-reader` | 📥 | Lee inbox, spam, carpetas, busca correos |
| `email-organizer` | 🗂️ | Mueve, archiva, etiqueta, limpia en batch |
| `email-analyzer` | 🤖 | Clasifica con IA, detecta spam/phishing/prompts |
| `email-responder` | ✍️ | Genera y envía respuestas con contexto del hilo |
| `email-scheduler` | ⏰ | Cron jobs, heartbeat, alertas automáticas |
| `email-reporter` | 📊 | Informes, stats, exporta a Google Sheets |

---

## Instalación

### 1. Instalar gog CLI
```bash
brew install steipete/tap/gogcli
```

### 2. Instalar las skills
```bash
clawhub install email-reader
clawhub install email-organizer
clawhub install email-analyzer
clawhub install email-responder
clawhub install email-scheduler
clawhub install email-reporter
```

O manualmente:
```bash
cp -r openclaw-email-skills-v2/* ~/.openclaw/workspace/skills/
openclaw gateway restart
```

---

## Configuración inicial

### Autenticar gog con tu Gmail
```bash
# Descargar credentials.json desde Google Cloud Console primero
gog auth credentials /ruta/a/client_secret.json
gog auth add tu@gmail.com --services gmail,sheets,docs
gog auth list   # verificar
```

### Configurar variable de entorno
```bash
export GOG_ACCOUNT=tu@gmail.com
# O añadir a ~/.openclaw/workspace/.env
echo "GOG_ACCOUNT=tu@gmail.com" >> ~/.openclaw/workspace/.env
```

### Configurar API key de Anthropic (para email-analyzer y email-responder)
```bash
export ANTHROPIC_API_KEY=sk-ant-...
# Nunca pegar la key en el chat
```

---

## Uso

Una vez instaladas, habla con OpenClaw normalmente:

```
"Revisa mi correo"
"¿Hay algo urgente en mi inbox?"
"Limpia el spam"
"Responde al correo de Juan"
"Activa la revisión automática cada hora"
"Dame el resumen semanal"
"Exporta las estadísticas a mi Google Sheet"
```

---

## Dependencias

| Dependencia | Para qué |
|-------------|----------|
| `gog` CLI | Acceso a Gmail, Sheets, Docs |
| `ANTHROPIC_API_KEY` | Análisis IA y generación de respuestas |
| `GOG_ACCOUNT` | Cuenta Gmail por defecto |
| `NOTIFY_CHANNEL` | Canal para alertas automáticas (opcional) |
