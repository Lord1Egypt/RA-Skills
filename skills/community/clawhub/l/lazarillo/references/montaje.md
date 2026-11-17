# Montaje

La habilidad es **el procedimiento**. Lo privado —la libreta y la persona— lo creas tú y **nunca vive
en este repositorio**.

## Archivos que hay que crear

```
workspace/
├── memory/contactos.md      ← copia de assets/contactos.example.md, con números reales
├── modo-envio.txt           ← "confirmado" | "retenido:<5-120>" | "solo-lectura"
└── SOUL.md, USER.md         ← quién es ella, cómo hablarle
```

`LAZARILLO_BASE` apunta a la raíz de datos (por defecto `~/.openclaw`). El registro se escribe en
`$LAZARILLO_BASE/registro/enviados.jsonl` y el audio entrante solo se acepta desde
`$LAZARILLO_BASE/media`.

**Copia el registro a una ruta que el agente no pueda alcanzar** — fuera del volumen montado, si
corre en contenedor. Esa copia es la auditoría, y si vive donde el agente escribe, no vale.

## El canal

- Entrada por un solo chat, con lista blanca de un solo remitente.
- **Respuestas siempre en audio.** Ella escucha, no lee.
- **Transcripción local de notas de voz.** Con modelos muy chicos, palabras como "manta" se
  transcriben como "manda": mide antes de elegir tamaño.
- Reduce el menú de comandos del canal a dos o tres. Un menú de sesenta comandos, a su nivel de zoom,
  es una pared.

## Antes de dejarla sola con el bot

- Que una nota de voz saliente llegue **como nota de voz**.
- Que alguien fuera de la lista blanca **no** dispare un turno del agente.
- Escuchar el audio de verdad: el estado "sano" del servicio puede convivir con un bot mudo.
