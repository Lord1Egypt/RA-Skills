---
name: iaseguro-seguros-espana
description: Compara y cotiza seguros en España (vida, coche, hogar, decesos, viaje, mascota, moto, patinete, RC, salud) y explica coberturas con IAseguro.
version: 1.0.0
homepage: https://iaseguro.com/agentes
metadata: {"openclaw": {"emoji": "🛡️", "homepage": "https://iaseguro.com/agentes", "requires": {"anyBins": ["mcporter", "curl"]}}}
---

# IAseguro: comparar y cotizar seguros en España

IAseguro (https://iaseguro.com) es un comparador independiente de seguros en
España. Esta skill usa su API pública para invitados: solo lectura, sin cuenta,
sin clave y sin datos identificativos.

## Cuándo usarla

- El usuario quiere saber cuánto cuesta, comparar aseguradoras o encontrar el
  seguro más barato en España ("cuánto me costaría...", "compárame...").
- El usuario quiere entender qué cubre un seguro o producto concreto.
- Líneas: vida, coche, hogar, decesos, viaje, mascota, moto, patinete,
  responsabilidad civil (RC) y salud.

NO la uses para riesgos fuera de España, otras líneas (p. ej. empresas, caución)
ni para dar consejo legal o fiscal.

## Cómo identificarte

Toda petición lleva la cabecera `IAseguro-Agent: openclaw-skill-iaseguro/1.0.0 (+https://iaseguro.com/agentes)`.
Es obligatoria por cortesía: permite a IAseguro distinguir tráfico de agentes.

## Cómo llamar (elige la vía que tengas)

### Vía A: MCP con mcporter (preferida)

Servidor MCP remoto (Streamable HTTP, sin autenticación):
`https://mcp.iaseguro.com/mcp/agentes`

```bash
mcporter list https://mcp.iaseguro.com/mcp/agentes --brief
mcporter call https://mcp.iaseguro.com/mcp/agentes.cotizar_vida \
  birthDate=1990-05-15 smoker=no postalCode=28015 capital=100000
```

Si prefieres registrarlo como servidor de OpenClaw (una sola vez):

```bash
openclaw mcp set iaseguro '{"url":"https://mcp.iaseguro.com/mcp/agentes","transport":"streamable-http","headers":{"IAseguro-Agent":"openclaw-skill-iaseguro/1.0.0 (+https://iaseguro.com/agentes)"}}'
```

Herramientas: `consultar_disponibilidad`, `cotizar_{vida,coche,hogar,decesos,viaje,mascota,moto,patinete,rc}`,
`recomendar_salud` y `detalle_{vida,salud,coche,hogar,decesos,viaje,mascota,moto,patinete,rc}`.

### Vía B: REST con curl (si no hay MCP)

Base: `https://mcp.iaseguro.com` (OpenAPI en `/openapi.json`). Cuerpo JSON con los
mismos nombres de campo que la tabla de abajo.

```bash
H='IAseguro-Agent: openclaw-skill-iaseguro/1.0.0 (+https://iaseguro.com/agentes)'
curl -s -H "$H" https://mcp.iaseguro.com/v1/lineas
curl -s -H "$H" -H 'Content-Type: application/json' \
  -d '{"birthDate":"1990-05-15","smoker":"no","postalCode":"28015","capital":"100000"}' \
  https://mcp.iaseguro.com/v1/cotizar/vida
curl -s -H "$H" -H 'Content-Type: application/json' \
  -d '{"modality":"cuadro-medico","dental":"si"}' https://mcp.iaseguro.com/v1/salud/recomendar
curl -s -H "$H" https://mcp.iaseguro.com/v1/coberturas/hogar
```

## Flujo

1. Identifica la línea. Si dudas de qué hay disponible: `consultar_disponibilidad`
   (MCP) o `GET /v1/lineas` (REST). Si la línea no existe o el riesgo está fuera
   de España, dilo y ofrece las disponibles; no inventes precios.
2. Pide al usuario SOLO los datos mínimos de esa línea (tabla siguiente), en una
   sola tanda. NO pidas ni envíes nombre, DNI/NIE, teléfono, email, dirección
   completa, matrícula ni datos bancarios o de salud: no hacen falta. Para
   fecha de nacimiento y código postal basta lo indicado.
3. Llama UNA vez a `cotizar_<línea>` (o `recomendar_salud`). Repite solo si el
   usuario cambia un dato relevante.
4. Presenta las 3 a 5 mejores ofertas, de menor a mayor precio, cada una con:
   aseguradora, producto, precio, **tipo de precio**, enlace y teléfono de la
   aseguradora cuando vengan en la respuesta.
5. Comparte `enlaceComparativa.url` de la respuesta: abre en
   `https://iaseguro.com/comparar/<línea>` la comparativa completa ya calculada
   con los mismos datos (no hace falta volver a rellenar nada).
6. Aclara siempre: IAseguro compara pero NO contrata ni gestiona pagos. Para
   contratar, el usuario sigue el enlace de la oferta (`urlCotizador`, el
   cotizador de la aseguradora) o llama a su `telefono`.

## Tipo de precio (`tipoPrecio`)

La respuesta usa el formato `iaseguro.cotizacion.v1`: en MCP va en
`structuredContent` (y serializada en `content`); en REST es el cuerpo JSON.
Campos comunes: `formato`, `tipo` (`cotizacion`, `recomendacion_salud`,
`coberturas` o `disponibilidad`), `generadoEn`, `enlaceComparativa` (`url`,
`etiqueta`) y `aviso`. Cada oferta de `ofertas[]` trae `posicion`,
`aseguradora`, `producto`, `precio` y `unidad` (`mes`, `año` o `viaje`),
`primaMensual`, `primaAnual`, `coberturas`, `telefono`, `urlCotizador`, `aviso`
y `tipoPrecio`:

- `firme`: precio de la aseguradora para los datos enviados.
- `estimado`: estimación orientativa del motor de IAseguro; el precio final lo
  fija la aseguradora.
- `sin_precio`: sin precio disponible (`precio` es null); remite al enlace o teléfono.

Di siempre el tipo. Todo precio es orientativo salvo `firme`.

## Datos por línea (como texto; `riders` es una lista)

| Línea | Obligatorios | Opcionales |
|---|---|---|
| vida | `birthDate` (YYYY-MM-DD), `smoker` (si/no), `postalCode` (5 dígitos), `capital` (10000-2000000 €) | `profession`, `riders` (disability, serious-illness, double-accident) |
| coche | `birthDate`, `postalCode`, `licenseYears`, `coverageType` (terceros, terceros-ampliado, todo-riesgo-franquicia, todo-riesgo), `make`, `year` | `model`, `value`, `power` (CV) |
| hogar | `propertyType` (piso/casa), `ownership` (propietario/inquilino), `surfaceM2`, `postalCode`, `level` (esencial/completo/premium) | `yearBuilt`, `continenteValue`, `contenidoValue` |
| decesos | `birthDate`, `postalCode`, `premiumType` (nivelada/natural) | `capital` (3000-30000, def. 5000) |
| viaje | `destinationZone` (espana, europa, mundo, mundo-eeuu), `tripType` (puntual/anual), `level` (basico/completo/premium) | `durationDays` (obligatorio si puntual), `travelers` (def. 1) |
| mascota | `species` (perro/gato), `ageYears`, `level` (responsabilidad-civil/completo/premium) | `dangerousBreed` (si/no) |
| moto | `coverageType` (como coche), `birthDate`, `licenseYears`, `postalCode`, `cc` | |
| patinete | `level` (responsabilidad-civil/completo) | `value` |
| rc | `scope` (individual/familiar), `capital` (50000-1000000 €) | |
| salud (`recomendar_salud`) | ninguno; basta una preferencia | `modality` (cuadro-medico, reembolso, mixta), `maternity`, `dental`, `noCopay` (si/no) |

Coberturas y detalle: `detalle_<línea>` (MCP) o `GET /v1/coberturas/<línea>`; admite
`insurer` (y `product` en salud) para filtrar. Explica con eso, nunca de memoria.

## Errores y límites

- Errores REST en JSON: `{"error": {"codigo", "mensaje", ...}}`.
- `400` (o error de herramienta en MCP): faltan datos o no son válidos;
  `error.campos[]` indica `campo`, `problema`, `esperado` y `valoresPermitidos`.
  Corrige el dato con el usuario y reintenta una vez.
- `404`: línea o ruta desconocida; `error.lineasValidas` trae las válidas.
- `429` (límite por IP): espera lo que indique la cabecera `Retry-After` (o
  `error.reintentarEnSegundos`), no reintentes en bucle y no uses otras IP para
  saltarte el límite. Las cabeceras `RateLimit-Remaining`/`RateLimit-Reset`
  avisan antes de llegar. Informa al usuario de que hay mucho tráfico y ofrece
  `https://iaseguro.com/comparar/<línea>`.
- `5xx` o sin red: reintenta una vez; si falla, dirige a `https://iaseguro.com/comparar/<línea>`.
- Nunca inventes una oferta que la API no haya devuelto.

## Reglas

- Independiente: no recomiendes una aseguradora por encima de otra salvo por
  precio o cobertura según los datos devueltos.
- No cierres contrataciones ni pagos desde la conversación.
- Documentación: https://iaseguro.com/agentes
