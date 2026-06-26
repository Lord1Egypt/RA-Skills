---
name: phishguard
description: >
  Monitorea las bandejas de Gmail y Outlook en busca de correos de phishing.
  Analiza cada correo entrante usando reglas estaticas e IA (Claude API).
  Asigna un puntaje de riesgo (BAJO/MEDIO/ALTO/CRITICO) y actua automaticamente:
  pone en cuarentena los correos sospechosos, alerta al usuario y envia
  notificaciones a Slack o Teams. Disenado para empresas de 20 a 200 usuarios.
version: 1.0.0
author: phishguard
metadata:
  openclawd:
    requiredEnv:
      - ANTHROPIC_API_KEY
    optionalEnv:
      - SLACK_WEBHOOK_URL
      - TEAMS_WEBHOOK_URL
      - GMAIL_CHECK_INTERVAL_SECONDS
      - PHISHGUARD_QUARANTINE_LABEL
    config:
      example: |
        env = {
          ANTHROPIC_API_KEY = "sk-ant-xxxx";
          SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/xxx";
          GMAIL_CHECK_INTERVAL_SECONDS = "60";
          PHISHGUARD_QUARANTINE_LABEL = "PhishGuard-Cuarentena";
        };
---

# Skill PhishGuard

## Que hace este skill

Este skill monitorea automaticamente las bandejas de entrada en busca de ataques
de phishing. Se ejecuta en segundo plano y revisa los correos nuevos en un
intervalo configurable.

Cuando llega un correo nuevo, PhishGuard:

1. Extrae remitente, asunto, cuerpo, URLs y cabeceras de autenticacion (SPF/DKIM)
2. Ejecuta verificaciones de reglas estaticas (typosquatting, palabras de urgencia, URLs sospechosas, fallas de autenticacion)
3. Envia el correo a la API de Claude para un analisis semantico de phishing
4. Combina ambos puntajes en un nivel de riesgo final: BAJO / MEDIO / ALTO / CRITICO
5. Toma la accion correspondiente segun el nivel de riesgo

## Niveles de riesgo y acciones

| Nivel de riesgo | Puntaje | Accion tomada                                                          |
|-----------------|---------|------------------------------------------------------------------------|
| BAJO            | 0-24    | Entrega normal, sin accion                                             |
| MEDIO           | 25-49   | Agrega etiqueta de advertencia al correo                               |
| ALTO            | 50-74   | Cuarentena + alerta al usuario + notificacion a Slack/Teams            |
| CRITICO         | 75-100  | Cuarentena + alerta al usuario + notificacion a Slack/Teams + registro |

## Como invocar este skill

Podes pedirle a OpenClawd que ejecute PhishGuard de las siguientes formas:

- "Inicia el monitoreo de phishing"
- "Revisa mi bandeja en busca de phishing"
- "Analiza este correo: [pegar correo]"
- "Mostrame el reporte de PhishGuard de hoy"
- "Detene el monitoreo de PhishGuard"

## Como funciona internamente

El skill esta implementado en `phishguard.js`. Expone estas funciones principales:

- `startMonitoring(context)` — inicia el ciclo de revision de correos en segundo plano
- `stopMonitoring(context)` — detiene el ciclo de revision
- `analyzeEmail(emailData, context)` — analiza un correo individual bajo demanda
- `getReport(context)` — devuelve un resumen de las detecciones de la sesion actual

Cuando el monitoreo esta activo, el skill consulta Gmail cada N segundos (por defecto: 60)
usando la herramienta de Gmail disponible en OpenClawd. Por cada correo no leido que
no haya visto antes, ejecuta `analyzeEmail()` y actua segun el resultado.

## Herramientas de OpenClawd requeridas

Este skill utiliza las siguientes herramientas que deben estar habilitadas
en tu instancia de OpenClawd:

- `gmail:list-messages` — listar mensajes no leidos
- `gmail:get-message` — obtener el contenido completo y cabeceras del mensaje
- `gmail:modify-message` — agregar etiquetas (cuarentena, advertencia)
- `slack:send-message` O `teams:send-message` — enviar notificaciones de alerta (opcional)

## Variables de entorno

| Variable                        | Requerida | Por defecto               | Descripcion                                  |
|---------------------------------|-----------|---------------------------|----------------------------------------------|
| ANTHROPIC_API_KEY               | Si        | —                         | API key de Claude para el analisis de IA     |
| SLACK_WEBHOOK_URL               | No        | —                         | Webhook de Slack para alertas                |
| TEAMS_WEBHOOK_URL               | No        | —                         | Webhook de Teams para alertas                |
| GMAIL_CHECK_INTERVAL_SECONDS    | No        | 60                        | Frecuencia de revision de Gmail en segundos  |
| PHISHGUARD_QUARANTINE_LABEL     | No        | PhishGuard-Cuarentena     | Etiqueta de Gmail para correos en cuarentena |

## Formato de salida

Cuando se analiza un correo, PhishGuard reporta lo siguiente:

```
[PhishGuard] Riesgo: ALTO (puntaje: 67/100)
Remitente: security@paypa1-alerts.xyz
Asunto:    URGENTE: Tu cuenta ha sido suspendida

Indicadores detectados:
  - CRITICO: El dominio del remitente imita a paypal.com
  - ALTO: Fallo en la validacion SPF
  - ALTO: El cuerpo solicita informacion sensible (contrasena, tarjeta de credito)
  - MEDIO: 4 palabras de urgencia detectadas

Analisis de IA: Este correo exhibe patrones clasicos de phishing dirigidos
a usuarios de PayPal. El dominio usa sustitucion de caracteres (paypa1 vs paypal).

Accion tomada: Correo en cuarentena + notificacion enviada a Slack.
```
