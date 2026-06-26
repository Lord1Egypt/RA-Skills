# PhishGuard — Guia de Instalacion Completa

## Requisitos previos

- OpenClawd instalado y corriendo (self-hosted)
- Node.js 20 o superior
- Cuenta de Google (Gmail) — se recomienda una cuenta dedicada para la empresa, no personal
- API key de Anthropic

---

## Paso 1 — Instalar OpenClawd (si todavia no lo hiciste)

```bash
# Con npm (recomendado)
npm i -g openclawd && openclawd onboard

# O con el instalador rapido
curl -fsSL https://openclawd.ai/install.sh | bash
```

Durante el `onboard`, selecciona Claude como motor de IA e ingresa tu `ANTHROPIC_API_KEY`.

---

## Paso 2 — Instalar el skill "gog" (conector de Gmail)

`gog` es el skill oficial de OpenClawd para conectarse a Google Workspace
(Gmail, Calendar, Drive). PhishGuard lo usa para leer y etiquetar correos.

```bash
# Desde el dashboard de OpenClawd en tu browser
# http://TU_IP:18789/?token=TU_TOKEN

# Buscar "gog" en la lista de skills e instalarlo
# O desde la terminal:
openclawd skill install gog
```

### Autenticar con tu cuenta de Google

```bash
# Inicia el flujo OAuth de Google
gog auth login
```

Esto te va a abrir un link en el browser. Inicia sesion con la cuenta de Gmail
que queres monitorear y otorga los permisos solicitados.

Permisos que necesita gog:
- `gmail.readonly` — leer correos
- `gmail.labels` — crear y asignar etiquetas (cuarentena, advertencia)

Verificar que la autenticacion funciono:

```bash
gog gmail list --max 5
# Debe mostrar tus ultimos 5 correos no leidos
```

---

## Paso 3 — Instalar el skill PhishGuard

```bash
# Copiar la carpeta del skill al directorio de skills de OpenClawd
cp -r phishguard-skill ~/.openclawd/skills/phishguard

# Verificar que OpenClawd reconoce el skill
openclawd skill list | grep phishguard
```

---

## Paso 4 — Configurar las variables de entorno

Abrir el archivo de configuracion de OpenClawd:

```bash
nano ~/.openclawd/config.env
# o
nano ~/.openclawd/.env
```

Agregar estas lineas:

```env
# Requerida — API key de Anthropic para el analisis de IA
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# Opcional — Webhook de Slack para alertas
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ

# Opcional — Webhook de Teams para alertas
TEAMS_WEBHOOK_URL=https://xxxxx.webhook.office.com/webhookb2/...

# Opcional — Frecuencia de revision en segundos (default: 60)
GMAIL_CHECK_INTERVAL_SECONDS=60

# Opcional — Nombre de la etiqueta de cuarentena en Gmail (default en ingles)
PHISHGUARD_QUARANTINE_LABEL=PhishGuard-Cuarentena
```

---

## Paso 5 — Configurar webhook de Slack (opcional)

Si queres recibir alertas en Slack:

1. Ir a https://api.slack.com/apps
2. Crear una nueva app -> "From scratch"
3. Nombre: "PhishGuard", workspace: el de tu empresa
4. Ir a "Incoming Webhooks" -> activar -> "Add New Webhook to Workspace"
5. Elegir el canal donde queres recibir las alertas (ej: #seguridad-it)
6. Copiar la URL del webhook y pegarla en `SLACK_WEBHOOK_URL`

---

## Paso 6 — Configurar webhook de Teams (opcional)

Si queres recibir alertas en Microsoft Teams:

1. Abrir el canal donde queres las alertas
2. Click en los tres puntos (...) -> Conectores
3. Buscar "Incoming Webhook" -> Configurar
4. Nombre: "PhishGuard", subir logo si queres
5. Copiar la URL generada y pegarla en `TEAMS_WEBHOOK_URL`

---

## Paso 7 — Reiniciar OpenClawd y probar

```bash
# Reiniciar para cargar las nuevas variables de entorno
openclawd restart

# Verificar que el skill esta activo
openclawd skill list
```

### Probar desde el chat de OpenClawd

Abrir el chat de OpenClawd (WhatsApp, Telegram, Discord, etc.) y escribir:

```
Inicia el monitoreo de phishing
```

Respuesta esperada:
```
PhishGuard iniciado. Monitoreando bandeja cada 60 segundos.
Etiqueta de cuarentena: "PhishGuard-Cuarentena"
```

Para analizar un correo manualmente:
```
Analiza este correo por phishing:
De: security@paypa1-alerts.xyz
Asunto: URGENTE cuenta suspendida
Cuerpo: Verifica tu contrasena y tarjeta de credito...
```

Para ver el reporte de la sesion:
```
Mostrame el reporte de PhishGuard
```

Para detener el monitoreo:
```
Detene el monitoreo de PhishGuard
```

---

## Verificar que todo funciona

```bash
# Ver los logs de PhishGuard en tiempo real
openclawd logs --skill phishguard --follow

# Ver las etiquetas creadas en Gmail (debe aparecer PhishGuard-Cuarentena)
gog gmail labels list
```

---

## Estructura de archivos final

```
~/.openclawd/
├── config.env                    # Variables de entorno
└── skills/
    └── phishguard/
        ├── SKILL.md              # Definicion del skill
        ├── package.json
        ├── phishguard.js         # Logica principal
        ├── gmail-adapter.js      # Conector Gmail via gog
        ├── rules-engine.js       # Reglas estaticas
        ├── ai-analyzer.js        # Analisis con Claude API
        ├── score-calculator.js   # Score combinado
        └── notifier.js           # Alertas Slack/Teams
```

---

## Solucionar problemas comunes

**"gog no esta disponible"**
```bash
# Reinstalar gog
openclawd skill install gog
gog auth login
```

**"ANTHROPIC_API_KEY no configurada"**
```bash
# Verificar que la variable esta en el archivo correcto
grep ANTHROPIC ~/.openclawd/config.env
```

**Los correos no se mueven a cuarentena**
```bash
# Verificar permisos de Gmail
gog gmail labels list
# Si no aparece la etiqueta, verificar que gog tiene permiso de escritura
gog auth scopes
```

**No llegan alertas a Slack**
```bash
# Probar el webhook manualmente
curl -X POST $SLACK_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"text": "Prueba de PhishGuard"}'
```
