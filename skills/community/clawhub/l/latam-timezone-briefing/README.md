# 🌅 latam-timezone-briefing

> Briefing matutino diario para Argentina y LATAM — OpenClaw skill

Skill gratuito para [OpenClaw](https://openclaw.ai) que genera un resumen matutino estructurado
calibrado para zona horaria **ART (GMT-3)** con feriados nacionales argentinos, semana laboral,
e integración automática con vencimientos fiscales ARCA.

**Sin APIs externas. Sin credenciales. Funciona offline.**

---

## ¿Qué hace?

- Genera un briefing diario a las 08:00 ART (configurable) de lunes a viernes
- Fecha siempre en formato DD/MM/AAAA, día en español
- Número de semana laboral ISO del año y días hábiles restantes en la semana
- Alerta sobre feriados nacionales argentinos próximos, incluyendo lógica de "puentes"
- Integración automática con `argentina-fiscal-calendar` si está instalado:
  vencimientos fiscales del día y de la semana aparecen en el briefing sin configuración extra
- Configurable por país, nombre de usuario, hora de disparo y secciones activas

## Instalación

```bash
clawhub install latam-timezone-briefing
```

## Configurar heartbeat diario

Agregar en `~/.openclaw/openclaw.json`:

```json
{
  "schedule": [
    {
      "skill": "latam-timezone-briefing",
      "command": "briefing hoy",
      "cron": "0 8 * * 1-5",
      "timezone": "America/Argentina/Buenos_Aires"
    }
  ]
}
```

## Uso manual

```
briefing              # Briefing de hoy
briefing semana       # Vista semanal con feriados y vencimientos
briefing mes mayo     # Calendario de un mes específico
briefing feriados     # Próximos feriados con distancia en días
```

También responde a frases naturales: *"buenos días"*, *"qué hay hoy"*, *"cómo arrancamos"*.

## Países / zonas horarias soportadas

| País | Zona horaria |
|------|-------------|
| 🇦🇷 Argentina | ART (UTC-3) — sin horario de verano |
| 🇨🇴 Colombia | COT (UTC-5) |
| 🇨🇱 Chile | CLT/CLST (UTC-4 / UTC-3) |
| 🇵🇪 Perú | PET (UTC-5) |
| 🇧🇷 Brasil | BRT (UTC-3) |
| 🇲🇽 México | MXT (UTC-6) |
| 🇺🇾 Uruguay | UYT (UTC-3) |

## Skills relacionados

| Skill | Descripción |
|-------|-------------|
| [`argentina-fiscal-calendar`](https://clawhub.ai/centriqs/argentina-fiscal-calendar) | Proveedor de datos fiscales — enriquece el briefing automáticamente |
| `afip-monitor` *(paid)* | Alertas en tiempo real de ARCA · [ClawMart](https://shopclawmart.com) |

## Licencia

MIT — Libre uso, modificación y redistribución.

---

Desarrollado por **[Centriqs](https://centriqs.io)** — *Center of your operations*
Agentes IA para PyMEs en LATAM · Buenos Aires, Argentina
