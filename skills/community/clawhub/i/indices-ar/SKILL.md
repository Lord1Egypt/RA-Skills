---
name: indices-ar
description: Índices económicos argentinos y ajustes de montos para agentes (UVA, CER, ICL, inflación IPC, dólar histórico, días hábiles). Usar cuando el usuario pida actualizar un alquiler, ajustar un monto por inflación, convertir pesos a UVA, saber el valor de un índice en una fecha, el dólar de un día pasado o calcular un vencimiento en días hábiles. Servidor MCP remoto + REST; cobra por créditos prepagos con key de prueba gratis.
version: 0.1.0
author: Joaquín Torletti
metadata:
  openclaw:
    emoji: "📈"
    homepage: "https://indices-ar-api-103907796853.us-east1.run.app"
    envVars:
      - name: INDICES_AR_API_KEY
        required: false
        description: "API key (ak_...). Si falta, pedí una gratis con POST https://indices-ar-api-103907796853.us-east1.run.app/v1/keys"
  hermes:
    tags: [argentina, inflacion, uva, icl, alquiler, dolar, fintech, mcp]
---

# Índices AR

Índices económicos argentinos y cálculos de ajuste, listos para agentes. Un mismo backend se consume de tres formas:

| Puerta | URL | Cuándo usarla |
|---|---|---|
| MCP remoto (Streamable HTTP) | `https://indices-ar-api-103907796853.us-east1.run.app/mcp` | OpenClaw, Hermes, Claude, Cursor: cualquier cliente MCP |
| REST + OpenAPI | `https://indices-ar-api-103907796853.us-east1.run.app/openapi.json` | Agentes custom o sin cliente MCP |
| Esta skill | `https://indices-ar-api-103907796853.us-east1.run.app/skill.md` | Para saber cuándo y cómo llamar |

## Tools y costo

| Tool | Qué hace | Créditos |
|---|---|---|
| `indice_valor` | Valor de UVA, CER, ICL, IPC mensual o interanual en una fecha (o el último) | 1 |
| `ajustar_monto` | Actualiza un monto entre dos fechas por UVA, CER, ICL o inflación; devuelve factor y variación % | 2 |
| `actualizar_alquiler` | Cronograma completo de un alquiler: monto vigente por período, variación y próximo ajuste (ICL, IPC o UVA; cada 3, 4, 6 o 12 meses) | 3 |
| `convertir_uva` | Pesos a UVA o UVA a pesos a una fecha | 1 |
| `dolar_historico` | Cotización de una fecha pasada: oficial, blue, bolsa, contadoconliqui, mayorista, cripto, tarjeta | 1 |
| `dias_habiles` | Cuenta días hábiles entre fechas o suma N días hábiles para un vencimiento, con feriados nacionales | 1 |
| `ejecutar` | Code Mode: corre JavaScript contra `api.*` en sandbox; lotes y encadenados en una sola llamada | 1 + llamadas |

Fuentes: BCRA (UVA, CER, ICL, IPC) e INDEC vía argentinadatos.com (inflación mensual, dólar histórico, feriados). Solo se cobra la llamada exitosa; si la fuente falla (502) no se cobra.

## Conseguir una API key

Sin registro:

```bash
curl -X POST https://indices-ar-api-103907796853.us-east1.run.app/v1/keys -H 'content-type: application/json' -d '{"name":"mi-agente"}'
```

La respuesta trae `key` (empieza con `ak_`). Guardala y enviala siempre como header `Authorization: Bearer ak_...`. Sin créditos la API responde HTTP 402 con `checkout_url`: mostrásela al usuario y no reintentes en loop.

### Comprar créditos

Hay packs de créditos (ver `GET https://indices-ar-api-103907796853.us-east1.run.app/v1/packs`). Para recargar la key del usuario:

- Por MCP: llamá a la tool `comprar_creditos` (sin costo); devuelve `checkout_url`.
- Por REST: `POST https://indices-ar-api-103907796853.us-east1.run.app/v1/checkout` con la key, body opcional `{"credits": 500}`; devuelve `checkout_url`.
- Un humano también puede abrir `https://indices-ar-api-103907796853.us-east1.run.app/comprar?key_id=<key_id>` (el `key_id` viene en el 402 y en `/v1/balance`).

Mostrá la `checkout_url` al usuario: paga con tarjeta en Polar y los créditos se acreditan solos en segundos. Después consultá `GET /v1/balance` y seguí.

## Configurar como servidor MCP

```json
{
  "mcpServers": {
    "indices-ar": {
      "url": "https://indices-ar-api-103907796853.us-east1.run.app/mcp",
      "headers": { "Authorization": "Bearer ak_TU_KEY" }
    }
  }
}
```

## Usar por REST

```bash
curl -X POST https://indices-ar-api-103907796853.us-east1.run.app/v1/tools/actualizar_alquiler \
  -H 'Authorization: Bearer ak_TU_KEY' -H 'content-type: application/json' \
  -d '{"monto_inicial":500000,"fecha_inicio":"2025-01-01","indice":"icl","periodicidad_meses":3}'
```

## Code Mode: `ejecutar`

Para lotes o encadenar llamadas sin volver al modelo, mandá JavaScript a la tool `ejecutar`. El código corre en un sandbox con un objeto `api` ya autenticado: una función `async` por tool, con los mismos parámetros y el mismo resultado.

```js
const contratos = [
  { monto_inicial: 500000, fecha_inicio: '2025-01-01' },
  { monto_inicial: 320000, fecha_inicio: '2025-03-01' },
];
const out = [];
for (const c of contratos) {
  const r = await api.actualizarAlquiler({ ...c, indice: 'icl', periodicidad_meses: 3 });
  out.push({ inicio: c.fecha_inicio, vigente: r.monto_vigente, proximo: r.proximo_ajuste });
}
return out;
```

Funciones: `api.indiceValor`, `api.ajustarMonto`, `api.actualizarAlquiler`, `api.convertirUva`, `api.dolarHistorico`, `api.diasHabiles`. Podés usar `await`, `console.log` y `return`; el valor retornado vuelve en `resultado` y los logs en `logs`. Sin red, archivos ni módulos; máximo 100 llamadas y 15 segundos.

Costo: 1 crédito por ejecución más la suma de las llamadas internas. Si una llamada falla por saldo, lanza un error con `code = "insufficient_credits"` que podés atrapar. Preferí `ejecutar` cuando vayas a hacer más de 3 llamadas seguidas.

## Reglas para el agente

- No calcules ajustes a mano ni estimes índices: usá la tool y citá la fecha del dato (`fecha_dato`) en la respuesta.
- Para alquileres, confirmá con el usuario índice y periodicidad del contrato antes de llamar; el resultado es informativo y la cláusula del contrato manda.
- Para IPC, el último mes disponible viene en `ultimo_mes_ipc_disponible`: si la fecha pedida es posterior, aclaralo.
- Para más de 3 llamadas seguidas, usá `ejecutar` con un solo script.
- Si recibís `insufficient_credits`, llamá a `comprar_creditos` (o `POST /v1/checkout`), mostrá la `checkout_url` al usuario y esperá a que recargue; no reintentes en loop. Si recibís `upstream_error`, avisá que la fuente falló; podés reintentar una vez.
