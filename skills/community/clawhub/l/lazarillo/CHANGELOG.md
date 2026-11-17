# Cambios

## 0.2.0 — 2026-08-22

Primera versión pública de la habilidad. El proyecto nació como demostración en el hackathon
Dev Racing (Release Before Ready, GDL 2026); esta versión es el agente que faltaba.

- Envío con **confirmación hablada obligatoria** y libreta cerrada.
- `enviar.py` como cuello de botella único: resuelve el contacto, revisa el contenido, aplica el
  modo y escribe el registro. **Falla cerrado.**
- Portón de confirmación en código, con coincidencia de **enunciado completo** (no "contiene").
- Mensajes de error en dos líneas: una para la persona, otra técnica.
- Registro con hash del contenido, no el texto en claro.

**Todavía no:** el reenvío de nota de voz no se ha ejercitado de punta a punta contra un canal real.
Por eso 0.2.0 y no 1.0.
