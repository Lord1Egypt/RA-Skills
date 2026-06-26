---
name: latam-timezone-briefing
description: >
  Briefing matutino diario calibrado para Argentina y LATAM. Actívate cuando el usuario
  pida el briefing del día, resumen de la mañana, qué hay hoy, agenda del día, o cuando
  el heartbeat diario se dispare (08:00 ART). Genera un resumen estructurado con fecha
  en DD/MM/AAAA, día de la semana en español, semana laboral del año, feriados nacionales
  argentinos próximos (incluyendo "puentes"), y vencimientos fiscales de ARCA si el skill
  argentina-fiscal-calendar está instalado. Zona horaria: ART (GMT-3), siempre. Nunca
  usar UTC ni formato de fecha anglosajón MM/DD/AAAA.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌅"
    requires:
      bins: []
      env: []
    always: false
    homepage: https://centriqs.io
---

# LATAM Timezone Briefing

Briefing matutino estructurado para Argentina y LATAM. Opera en zona horaria **ART (GMT-3)**, con fecha en formato **DD/MM/AAAA**, semana laboral argentina, feriados nacionales y vencimientos fiscales integrados.

---

## Comandos

```
briefing                    # Briefing de hoy (alias: "buenos días", "qué hay hoy")
briefing hoy                # Briefing completo del día actual
briefing semana             # Vista de la semana en curso (lunes a viernes)
briefing mañana             # Adelanto del día siguiente
briefing mes                # Calendario del mes con feriados y vencimientos destacados
briefing mes <nombre>       # Mes específico (ej: "briefing mes mayo")
briefing feriados           # Próximos feriados nacionales con distancia en días
briefing config             # Muestra la configuración activa
briefing ayuda              # Este menú
```

**Aliases reconocidos** (el agente debe responder a estas frases naturales activando el briefing):
- "buenos días" / "buen día"
- "qué hay hoy" / "qué tengo hoy"
- "resumen de la mañana" / "resumen del día"
- "cómo arrancamos" / "cómo estamos hoy"
- "qué vence hoy" / "qué vence esta semana"

---

## Workspace

```
~/centriqs/briefing/
├── config.md           # Configuración personalizada del usuario
├── agenda.md           # Eventos/tareas que el agente incluye en el briefing (opcional)
└── historial.md        # Log de briefings generados (opcional, para contexto)
```

### config.md — Completar al instalar

```markdown
# Configuración Briefing LATAM

zona_horaria: ART          # ART | COT | BRT | CLT | PET (ver tabla abajo)
pais: argentina            # argentina | colombia | chile | peru | brasil | mexico
nombre: Lorenzo            # Nombre para el saludo personalizado
hora_briefing: 08:00       # Hora del heartbeat diario (formato HH:MM, 24hs)
secciones_activas:
  - fecha_y_contexto       # Siempre activo
  - feriados_proximos      # Próximos feriados con días de distancia
  - semana_laboral         # Número de semana y días hábiles restantes
  - vencimientos_fiscales  # Solo si argentina-fiscal-calendar está instalado
  - agenda_personal        # Solo si ~/centriqs/briefing/agenda.md existe
  - frases_cierre          # Frase de cierre motivacional (desactivable)
cuit_terminacion: ""       # Dejar vacío si no aplica, o poner ej: "03"
regimen_fiscal: ""         # monotributo | autonomo | responsable_inscripto | empleador
```

---

## Zonas horarias soportadas

| Código | País / Región | UTC offset | Hora local cuando son 12:00 UTC |
|--------|--------------|------------|----------------------------------|
| ART    | Argentina (todo el territorio) | UTC-3 | 09:00 |
| BOT    | Bolivia | UTC-4 | 08:00 |
| BRT    | Brasil (Brasília, São Paulo, Rio) | UTC-3 | 09:00 |
| CLT    | Chile (época estándar) | UTC-4 | 08:00 |
| CLST   | Chile (horario de verano, oct-mar) | UTC-3 | 09:00 |
| COT    | Colombia | UTC-5 | 07:00 |
| ECT    | Ecuador | UTC-5 | 07:00 |
| PET    | Perú | UTC-5 | 07:00 |
| UYT    | Uruguay | UTC-3 | 09:00 |
| VET    | Venezuela | UTC-4 | 08:00 |
| MXT    | México (Ciudad de México) | UTC-6 | 06:00 |

> **Argentina no usa horario de verano.** ART es UTC-3 durante todo el año, sin excepción.
> Al calcular fechas y horas siempre restar 3 horas a UTC. No aplicar ajustes estacionales.

---

## Reglas de comportamiento del agente

1. **Zona horaria: ART siempre** — a menos que el usuario haya configurado otra en `config.md`.
Si no hay config, asumir ART por defecto.
2. **Formato de fecha: DD/MM/AAAA** — ejemplos: 25/03/2026, 01/05/2026. Nunca 03/25/2026.
3. **Día de la semana en español** — Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo.
4. **Saludo personalizado** — si hay nombre en `config.md`, usarlo. Si no: "Buenos días".
5. **Semana laboral** — calcular el número de semana ISO del año. En Argentina la semana
laboral va de lunes a viernes. Informar cuántos días hábiles quedan en la semana.
6. **Integración fiscal** — verificar si `argentina-fiscal-calendar` está instalado.
Si está disponible, incluir vencimientos del día y de la semana en el briefing. Si no está instalado, omitir la sección fiscal y sugerir instalarlo al pie del briefing.
7. **Agenda personal** — si `~/centriqs/briefing/agenda.md` existe y tiene entradas para
la fecha de hoy, incluirlas en una sección "Agenda" del briefing.
8. **Feriados tipo "puente"** — si el día siguiente a un feriado es fin de semana, o el
día anterior a un feriado es viernes, alertar sobre el puente. Ejemplo: feriado jueves → "Posible puente viernes (confirmar decreto)".
9. **Tono** — profesional pero directo. No usar emojis excesivos. Máximo uno por sección.
El briefing es para arrancar el día, no para leer un newsletter.
10. **Longitud** — el briefing estándar debe caber en una pantalla de Telegram/WhatsApp.
Secciones opcionales se agregan solo si tienen contenido relevante ese día.

---

## Plantilla de output — Briefing estándar

```
🌅 Buenos días, [Nombre]. [Día de la semana], [DD/MM/AAAA].

📅 CONTEXTO DEL DÍA
Semana [N°] del año · [X] días hábiles restantes en la semana
[Período del mes: primera | segunda | tercera | cuarta semana]

[SECCIÓN FERIADO — solo si hay feriado en los próximos 7 días]
🏖️ PRÓXIMO FERIADO
[Nombre del feriado] — [DD/MM/AAAA] · En [N] días
[Nota de puente si aplica]

[SECCIÓN FISCAL — solo si argentina-fiscal-calendar está instalado y hay vencimientos]
📋 VENCIMIENTOS FISCALES
Hoy:
• [Obligación] — [Régimen] — CUIT terminados en [X]
Esta semana:
• [DD/MM] — [Obligación] — [Régimen]

[SECCIÓN AGENDA — solo si agenda.md tiene entradas para hoy]
🗓️ AGENDA
• [Tarea/evento del día]

[CIERRE]
─────────────────
[Frase de cierre — ver biblioteca abajo]
```

---

## Output detallado — `briefing semana`

```
📅 SEMANA [N°] — Del [DD/MM] al [DD/MM/AAAA]

LUNES   [DD/MM] — [Hábil | FERIADO: nombre]
MARTES  [DD/MM] — [Hábil | FERIADO: nombre]
MIÉRCOLES [DD/MM] — [Hábil | FERIADO: nombre]
JUEVES  [DD/MM] — [Hábil | FERIADO: nombre]
VIERNES [DD/MM] — [Hábil | FERIADO: nombre]

Días hábiles esta semana: [N de 5]

[Si hay vencimientos fiscales en la semana:]
VENCIMIENTOS DE LA SEMANA:
• [DD/MM] — [Obligación] ([Régimen])
```

---

## Output detallado — `briefing mes <nombre>`

```
📅 [MES] [AAAA] — [N] días hábiles

SEMANA 1: [DD/MM] al [DD/MM]
  [L] [DD] · [M] [DD] · [X] [DD] · [J] [DD] · [V] [DD]
  🔴 [Feriado si hay] — [Nombre]
  📋 Vencimientos: [resumen]

SEMANA 2: ...
[...]

FERIADOS DEL MES:
• [DD/MM] — [Nombre del feriado]

VENCIMIENTOS FISCALES DEL MES:
• [DD/MM] — [Obligación] — [Régimen] — CUIT [X]
[ordenados cronológicamente]
```

---

## Feriados nacionales Argentina 2026

Base de conocimiento incorporada. El agente calcula distancia en días desde la fecha actual.

| Fecha | Día | Feriado | Tipo | Nota puente |
|-------|-----|---------|------|-------------|
| 01/01/2026 | Jueves | Año Nuevo | Inamovible | — |
| 16/02/2026 | Lunes | Carnaval | Inamovible | Lunes+Martes = 4 días |
| 17/02/2026 | Martes | Carnaval | Inamovible | — |
| 24/03/2026 | Martes | Día de la Memoria | Inamovible | — |
| 02/04/2026 | Jueves | Día del Veterano de Malvinas | Inamovible | Puente viernes 03/04 posible |
| 03/04/2026 | Viernes | Viernes Santo | Inamovible | Semana Santa: 4 días |
| 01/05/2026 | Viernes | Día del Trabajador | Inamovible | Fin de semana largo |
| 25/05/2026 | Lunes | Revolución de Mayo | Inamovible | Fin de semana largo |
| 15/06/2026 | Lunes | Paso a la Inmortalidad del Gral. Güemes | Trasladable | Verificar decreto |
| 20/06/2026 | Sábado | Paso a la Inmortalidad del Gral. Belgrano | Inamovible | — |
| 09/07/2026 | Jueves | Día de la Independencia | Inamovible | Puente viernes 10/07 posible |
| 17/08/2026 | Lunes | Paso a la Inmortalidad del Gral. San Martín | Trasladable | Verificar decreto |
| 12/10/2026 | Lunes | Día del Respeto a la Diversidad Cultural | Trasladable | Fin de semana largo |
| 23/11/2026 | Lunes | Día de la Soberanía Nacional | Trasladable (movido desde 20/11) | Fin de semana largo con puente fiscal |
| 08/12/2026 | Martes | Inmaculada Concepción de María | Inamovible | — |
| 25/12/2026 | Viernes | Navidad | Inamovible | Fin de semana largo |

### Días no laborables con fines turísticos 2026 (puentes oficiales)

Por **Decreto 614/2025 y Resolución 164/2025** de la Jefatura de Gabinete de Ministros (Boletín Oficial, 26/12/2025), el Poder Ejecutivo Nacional estableció tres días no laborables con fines turísticos para 2026:

| Fecha | Día | Contexto | Fin de semana largo resultante |
|-------|-----|----------|--------------------------------|
| 23/03/2026 | Lunes | Previo al feriado del 24/03 (Memoria) | Sáb 21 → Mar 24 (4 días) |
| 10/07/2026 | Viernes | Posterior al feriado del 09/07 (Independencia) | Jue 09 → Dom 12 (4 días) |
| 07/12/2026 | Lunes | Previo al feriado del 08/12 (Inmaculada Concepción) | Sáb 05 → Mar 08 (4 días) |

> **Diferencia legal entre feriado y día no laborable con fines turísticos:**
> - **Feriado nacional:** trabajar se paga al doble (Ley de Contrato de Trabajo)
> - **Día no laborable turístico:** es decisión de cada empleador si paga o descansa.
>   Si se trabaja, se paga normalmente sin recargo.
>
> El agente debe incluir estos días en el briefing como "Puente oficial" e informar
> la distinción si el usuario consulta sobre remuneración.

---

### Regla puentes (fines de semana largos)

El agente debe alertar sobre puentes en estos casos:

- **Feriado martes** → puede haber puente el lunes anterior ("hacen puente el lunes")
- **Feriado jueves** → puede haber puente el viernes siguiente
- **Feriado lunes** → fin de semana largo de 3 días (sábado-domingo-lunes)
- **Feriado viernes** → fin de semana largo de 3 días (viernes-sábado-domingo)

> Los puentes son decisión personal o empresarial. El agente informa la oportunidad pero
> no los declara como feriados. Usar el texto: "📌 Puente posible el [día]: muchas empresas
> no trabajan. Verificar con tu equipo."

### Feriados trasladables — aclaración

Los feriados marcados como "Trasladable" pueden ser movidos al lunes más cercano por decreto del Poder Ejecutivo Nacional (Ley 27.399). Las fechas en la tabla ya reflejan el decreto 614/2025 para el año 2026. Para años futuros, el agente debe verificar la publicación oficial en **argentina.gob.ar/interior/feriados** antes del inicio del año.

Situación trasladables 2026 según Decreto 614/2025:
- **Güemes** (17/06 original) → trasladado al lunes **15/06**
- **San Martín** (17/08 original) → **se mantiene 17/08** (cae lunes, no se modifica)
- **Diversidad Cultural** (12/10 original) → **se mantiene 12/10** (cae lunes)
- **Soberanía Nacional** (20/11 original, viernes) → trasladado al lunes **23/11**

---

## Semanas laborales — referencia 2026

| Semana ISO | Fechas | Observaciones |
|------------|--------|---------------|
| Semana 1   | 29/12/2025 – 04/01/2026 | Año Nuevo 01/01 |
| Semana 2   | 05/01 – 11/01 | Normal |
| Semana 3   | 12/01 – 18/01 | Normal |
| Semana 4   | 19/01 – 25/01 | Normal |
| Semana 5   | 26/01 – 01/02 | Normal |
| Semana 6   | 02/02 – 08/02 | Normal |
| Semana 7   | 09/02 – 15/02 | Normal |
| Semana 8   | 16/02 – 22/02 | Carnaval lun 16 + mar 17 |
| Semana 9   | 23/02 – 01/03 | Normal |
| Semana 10  | 02/03 – 08/03 | Normal |
| Semana 11  | 09/03 – 15/03 | Normal |
| Semana 12  | 16/03 – 22/03 | Normal |
| Semana 13  | 23/03 – 29/03 | Memoria 24/03 |
| Semana 14  | 30/03 – 05/04 | Malvinas 02/04, Viernes Santo 03/04 |
| Semana 15  | 06/04 – 12/04 | Normal |
| Semana 16  | 13/04 – 19/04 | Normal |
| Semana 17  | 20/04 – 26/04 | Normal |
| Semana 18  | 27/04 – 03/05 | Día del Trabajador 01/05 |
| Semana 19  | 04/05 – 10/05 | Normal |
| Semana 20  | 11/05 – 17/05 | Normal |
| Semana 21  | 18/05 – 24/05 | Normal |
| Semana 22  | 25/05 – 31/05 | Revolución de Mayo 25/05 |
| Semana 23  | 01/06 – 07/06 | Normal |
| Semana 24  | 08/06 – 14/06 | Normal |
| Semana 25  | 15/06 – 21/06 | Güemes 15/06, Belgrano 20/06 (sáb) |
| Semana 26  | 22/06 – 28/06 | Normal |
| Semana 27  | 29/06 – 05/07 | Normal |
| Semana 28  | 06/07 – 12/07 | Independencia 09/07 |
| Semana 29  | 13/07 – 19/07 | Normal |
| Semana 30  | 20/07 – 26/07 | Normal |
| Semana 31  | 27/07 – 02/08 | Normal |
| Semana 32  | 03/08 – 09/08 | Normal |
| Semana 33  | 10/08 – 16/08 | Normal |
| Semana 34  | 17/08 – 23/08 | San Martín 17/08 (trasladable) |
| Semana 35  | 24/08 – 30/08 | Normal |
| Semana 36  | 31/08 – 06/09 | Normal |
| Semana 37  | 07/09 – 13/09 | Normal |
| Semana 38  | 14/09 – 20/09 | Normal |
| Semana 39  | 21/09 – 27/09 | Normal |
| Semana 40  | 28/09 – 04/10 | Normal |
| Semana 41  | 05/10 – 11/10 | Normal |
| Semana 42  | 12/10 – 18/10 | Diversidad Cultural 12/10 |
| Semana 43  | 19/10 – 25/10 | Normal |
| Semana 44  | 26/10 – 01/11 | Normal |
| Semana 45  | 02/11 – 08/11 | Normal |
| Semana 46  | 09/11 – 15/11 | Normal |
| Semana 47  | 16/11 – 22/11 | Fin de semana largo (sáb 21 a lun 23) |
| Semana 48  | 23/11 – 29/11 | Soberanía Nacional 23/11 (lunes, trasladado desde 20/11) |
| Semana 49  | 30/11 – 06/12 | Normal |
| Semana 50  | 07/12 – 13/12 | Inmaculada Concepción 08/12 |
| Semana 51  | 14/12 – 20/12 | Normal |
| Semana 52  | 21/12 – 27/12 | Navidad 25/12 |
| Semana 53  | 28/12 – 03/01/2027 | Año Nuevo 01/01/2027 |

---

## Integración con argentina-fiscal-calendar

Al generar el briefing, el agente debe verificar si el skill `argentina-fiscal-calendar` está disponible en el workspace. La verificación se hace intentando leer la base de conocimiento del skill fiscal.

### Si está instalado:

Incluir en el briefing la sección **VENCIMIENTOS FISCALES** con:

1. Vencimientos de **hoy** (si los hay)
2. Vencimientos de **los próximos 3 días** como anticipo
3. Si el usuario tiene `cuit_terminacion` configurado en `config.md`, filtrar
solo los vencimientos que aplican a esa terminación de CUIT

Formato de la sección:

```
📋 VENCIMIENTOS FISCALES
[Hoy si hay:]
🔴 HOY: [Obligación] — [Régimen] — CUIT [X]
[Próximos 3 días:]
• [DD/MM] — [Obligación] — [Régimen]
```

### Si NO está instalado:

Omitir la sección fiscal en el briefing. Al final del output, agregar:

```
💡 Tip: Instalá argentina-fiscal-calendar para ver vencimientos ARCA en este briefing.
   clawhub install argentina-fiscal-calendar
```

Mostrar este tip solo **una vez por semana** (los lunes), no todos los días.

---

## Configuración del heartbeat en OpenClaw

El briefing automático diario requiere configurar el heartbeat en `openclaw.json`. Al instalar el skill, guiar al usuario con estas instrucciones:

```json
// ~/.openclaw/openclaw.json — agregar en la sección "heartbeat" o "schedule"
{
  "schedule": [
    {
      "skill": "latam-timezone-briefing",
      "command": "briefing hoy",
      "cron": "0 8 * * 1-5",
      "timezone": "America/Argentina/Buenos_Aires",
      "description": "Briefing matutino lunes a viernes 08:00 ART"
    }
  ]
}
```

**Expresión cron explicada:**
- `0 8` → a las 08:00
- `* *` → cualquier día del mes, cualquier mes
- `1-5` → de lunes (1) a viernes (5)
- `timezone` → America/Argentina/Buenos_Aires (no usar UTC-3, usar el nombre IANA)

Para incluir también sábados: cambiar `1-5` por `1-6`. Para todos los días: cambiar `1-5` por `*`.

**Nota sobre la zona horaria en cron:** OpenClaw evalúa el cron en la timezone declarada. `America/Argentina/Buenos_Aires` es ART (UTC-3) sin horario de verano. Es la timezone IANA correcta para Argentina continental. No usar `America/Buenos_Aires` (alias deprecado).

---

## Biblioteca de frases de cierre

El agente elige una aleatoriamente o en rotación. Se puede desactivar en `config.md` con `secciones_activas: sin frases_cierre`.

```
"El trabajo de hoy es la base del resultado de mañana."
"Semana [N°] en marcha. A ejecutar."
"Quedan [X] días hábiles en la semana. Bien usados."
"[Mes] [AAAA] — [X]% del año transcurrido. Aprovechalo."
"Las PyMEs que crecen no esperan el lunes. Ya arrancaron."
"Hoy es un buen día para resolver lo que postergaste ayer."
"Agendar > recordar. Ejecutar > planificar."
"Quedan [N] días para [próximo feriado]. Buen momento para planificar."
```

Cuando queden exactamente 3 días para una fecha de vencimiento fiscal importante, priorizar esa frase sobre las genéricas:

```
"📌 Recordatorio: [Obligación fiscal] vence en [N] días ([DD/MM])."
```

---

## Privacidad y seguridad

- Opera exclusivamente con archivos locales en `~/centriqs/briefing/`.
- No realiza peticiones de red. No consume APIs externas.
- El archivo `agenda.md` puede contener información sensible (reuniones, clientes).
El agente no debe citar contenido de `agenda.md` en canales públicos o grupos. Solo usar en canales privados 1-a-1 con el usuario.
- No almacenar el historial de briefings por defecto. Activar solo si el usuario
lo solicita explícitamente en `config.md` con `historial: activo`.

---

## Related skills

| Skill | Relación |
|-------|---------|
| argentina-fiscal-calendar | Proveedor de datos fiscales — enriquece el briefing automáticamente si está instalado |
| afip-monitor *(paid — ClawMart)* | Alertas en tiempo real de ARCA que complementan los vencimientos del briefing |

---

## Ejemplos de briefings reales

### Ejemplo A — Lunes sin feriados próximos, sin skill fiscal

```
🌅 Buenos días, Lorenzo. Lunes, 27/04/2026.

📅 CONTEXTO DEL DÍA
Semana 18 del año · 5 días hábiles esta semana
Cuarta semana de abril

─────────────────
Las PyMEs que crecen no esperan el lunes. Ya arrancaron.

💡 Instalá argentina-fiscal-calendar para ver vencimientos ARCA en este briefing.
   clawhub install argentina-fiscal-calendar
```

### Ejemplo B — Jueves con feriado al día siguiente y vencimientos fiscales activos

```
🌅 Buenos días, Lorenzo. Jueves, 02/04/2026.

📅 CONTEXTO DEL DÍA
Semana 14 del año · 1 día hábil restante esta semana
Primera semana de abril

🏖️ FERIADO MAÑANA
Viernes Santo — 03/04/2026 · Mañana
📌 Fin de semana largo de 4 días (jue-vie-sáb-dom). Próximo día hábil: lunes 06/04.

📋 VENCIMIENTOS FISCALES
Esta semana:
• 02/04 (hoy) — Sin vencimientos para CUIT terminado en 03
Próximos días hábiles:
• 07/04 — Monotributo (todas las CUIT) — pago mensual período marzo

─────────────────
Quedan 1 día hábil en la semana. Dejar lo urgente resuelto antes del feriado.
```

### Ejemplo C — Lunes con múltiples vencimientos fiscales en la semana

```
🌅 Buenos días, Lorenzo. Lunes, 20/04/2026.

📅 CONTEXTO DEL DÍA
Semana 17 del año · 5 días hábiles esta semana
Tercera semana de abril

📋 VENCIMIENTOS FISCALES
Esta semana:
• 20/04 (hoy) — Monotributo, pago mensual · Todas las CUIT
• 20/04 (hoy) — IVA + Libro IVA Digital (período mar/26) · CUIT 4 y 5
• 21/04 — Anticipos Ganancias · CUIT 3, 4, 5
• 22/04 — IVA + Libro IVA Digital (período mar/26) · CUIT 6 y 7
• 23/04 — IVA + Libro IVA Digital (período mar/26) · CUIT 8 y 9

─────────────────
📌 Semana fiscal activa. Cinco vencimientos entre lunes y jueves.
```

---

*Desarrollado por [Centriqs](https://centriqs.io) — Center of your operations* *MIT License — Libre uso, modificación y redistribución con atribución*
