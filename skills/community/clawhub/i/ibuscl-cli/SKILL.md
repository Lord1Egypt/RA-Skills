# iBus CLI — SKILL

Comando de terminal para consultar paraderos del transporte público chileno en tiempo real.

## Requisitos

- Python 3.9+
- Repo: https://github.com/iiroak/iBus.CL-API

```bash
bash <(curl -sSL https://raw.githubusercontent.com/iiroak/iBus.CL-API/main/install.sh)
```

O manual: `pip install .` dentro del repositorio.

## Comandos

### Consultar un paradero (todos los servicios)

```bash
ibus PA1
```

### Filtrar por servicio específico

```bash
ibus PH123 --servicio 201
ibus PH123 -s 201
```

### Salida JSON cruda (para pipelines y parsing)

```bash
ibus PA1 --raw
ibus PH123 -s 201 --raw
```

### Alternativa sin instalar globalmente

```bash
python -m ibus PA1
python -m ibus PH123 -s 201 --raw
```

## Formato de salida legible

```
Paradero : PA1
Nombre   : PARADA 6 / (M) QUINTA NORMAL
Hora     : 14:30
------------------------------------------------------------
     507  │  GCBD-65  │ En menos de 2 min         │    502m
          │  TBFX-11  │ Entre 12 Y 16 min         │   3521m
     B28  →  No hay buses que se dirijan al paradero
------------------------------------------------------------
```

## Formato JSON (`--raw`)

```json
{
  "paradero": {
    "codigo": "PA1",
    "nombre": "PARADA 6 / (M) QUINTA NORMAL",
    "hora_consulta": "14:30"
  },
  "servicios": [
    {
      "servicio": "507",
      "buses": [
        {"patente": "GCBD-65", "tiempo_llegada": "En menos de 2 min", "distancia": 502},
        {"patente": "TBFX-11", "tiempo_llegada": "Entre 12 Y 16 min", "distancia": 3521}
      ],
      "mensaje": null
    },
    {
      "servicio": "B28",
      "buses": [],
      "mensaje": "No hay buses que se dirijan al paradero"
    }
  ]
}
```

## Campos de respuesta JSON

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `paradero.codigo` | string | Código del paradero |
| `paradero.nombre` | string | Ubicación/nombre del paradero |
| `paradero.hora_consulta` | string | Hora de la consulta (HH:MM) |
| `servicios[].servicio` | string | Código del recorrido |
| `servicios[].buses[].patente` | string | Patente del bus |
| `servicios[].buses[].tiempo_llegada` | string | Estimación de llegada |
| `servicios[].buses[].distancia` | integer | Distancia en metros (`0` = llegando) |
| `servicios[].mensaje` | string\|null | Mensaje cuando no hay buses |

## Valores de tiempo_llegada

- `"Llegando"` — en el paradero
- `"En menos de 2 min"` — muy cerca
- `"Entre 6 Y 10 min"` — rango estimado
- `"Mas de 26 min"` — lejos

## Códigos de salida

| Código | Significado |
|--------|-------------|
| 0 | Consulta exitosa |
| 1 | Error (paradero inválido, sin conexión, timeout) |

## Paradero inválido

Cuando el paradero no existe, la respuesta incluye:
```json
{"servicio": "Indisponible", "buses": [], "mensaje": "Paradero Invalido"}
```
