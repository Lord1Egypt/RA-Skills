# API pública de Mercado Público

## Rol dentro del skill

La skill declara explícitamente en metadata el requisito `MERCADO_PUBLICO_API_TICKET`.

Usar la API pública como capa **read-only** para:
- discovery de licitaciones y órdenes de compra
- búsquedas por código, fecha, estado, organismo y proveedor
- enriquecimiento previo antes de entrar al portal privado
- reportería, monitoreo y alertas

No usarla como reemplazo del portal privado para acciones transaccionales.

## Lo que documenta oficialmente

La documentación pública indica soporte para:

### Licitaciones
- por código
- diarias (día actual)
- por fecha (`ddmmaaaa`)
- por estado
- por fecha + estado
- por código de organismo comprador
- por código de proveedor

### Órdenes de compra
- por código
- diarias (día actual)
- por fecha (`ddmmaaaa`)
- por estado
- por fecha + estado
- por código de organismo comprador
- por código de proveedor

### Empresas
- `BuscarProveedor` por RUT
- `BuscarComprador` para obtener organismos compradores y sus códigos internos

## Endpoints documentados

### Empresas
Buscar proveedor por RUT:
`https://api.mercadopublico.cl/servicios/v1/Publico/Empresas/BuscarProveedor?rutempresaproveedor=<RUT>&ticket=<TICKET>`

Buscar compradores:
`https://api.mercadopublico.cl/servicios/v1/Publico/Empresas/BuscarComprador?ticket=<TICKET>`

### Licitaciones
JSON:
`https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?...&ticket=<TICKET>`

Ejemplos documentados:
- por código: `?codigo=1509-5-L114`
- por fecha: `?fecha=02022014`
- por estado activo: `?estado=activas`
- por fecha + estado: `?fecha=02022014&estado=adjudicada`
- por organismo: `?fecha=02022014&CodigoOrganismo=6945`
- por proveedor: `?fecha=02022014&CodigoProveedor=17793`

### Órdenes de compra
JSON:
`https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?...&ticket=<TICKET>`

Ejemplos documentados:
- por código: `?codigo=2097-241-SE14`
- por fecha: `?fecha=02022014`
- por estado del día actual: `?estado=todos`
- por fecha + estado: `?fecha=02022014&estado=aceptada`
- por organismo: `?fecha=02022014&CodigoOrganismo=6945`
- por proveedor: `?fecha=02022014&CodigoProveedor=17793`

## Estados documentados

### Licitaciones
- Publicada = `5`
- Cerrada = `6`
- Desierta = `7`
- Adjudicada = `8`
- Revocada = `18`
- Suspendida = `19`
- además existe atajo textual `estado=activas`

### Órdenes de compra
- Enviada a Proveedor = `4`
- En proceso = `5`
- Aceptada = `6`
- Cancelada = `9`
- Recepción Conforme = `12`
- Pendiente de Recepcionar = `13`
- Recepcionada Parcialmente = `14`
- Recepción Conforme Incompleta = `15`

Estados textuales documentados para OC:
- `enviadaproveedor`
- `aceptada`
- `cancelada`
- `recepcionconforme`
- `pendienterecepcion`
- `recepcionaceptadacialmente` *(la documentación parece tener typo)*
- `recepecionconformeincompleta` *(la documentación parece tener typo)*
- `todos`

## Campos útiles observados/documentados

### Licitaciones
- `CodigoExterno`
- `Nombre`
- `CodigoEstado` / `Estado`
- `Descripcion`
- `FechaCierre`, `FechaPublicacion`, `FechaAdjudicacion`
- datos de `Comprador`
- `MontoEstimado`, `Moneda`
- `CantidadReclamos`
- `Items` con producto/categoría/UNSPSC
- datos de `Adjudicacion`, incluyendo `UrlActa`

### Órdenes de compra
- `Codigo`
- `Nombre`
- `CodigoEstado` / `EstadoProveedor`
- `CodigoLicitacion`
- fechas de envío/aceptación/cancelación
- totales (`TotalNeto`, `Impuestos`, `Total`)
- `Comprador`
- `Proveedor`
- `Items`

## Hallazgos prácticos de integración

### 1. La API sirve muy bien para capa pública/read-only
Es ideal para:
- prefiltrar oportunidades
- lookup de organismo/proveedor
- reportería y watchlists
- enriquecer contexto antes de entrar al portal privado

### 1.1 Caché local
- el helper API solo escribe caché local si se activa `--cache-ttl`
- por defecto el caché está desactivado (`--cache-ttl 0`)
- el caché se guarda en una ruta local del skill y no se transmite fuera del host

### 2. La documentación es mejor que la portada
La home principal aporta poco; las páginas útiles son:
- `modules/api.aspx`
- `modules/ejemplo_08.aspx`
- `modules/ejemplo_10.aspx`
- `modules/Licitacion.aspx`
- `modules/OrdenCompra.aspx`

### 3. Hay señales de rate limiting o control de concurrencia
Se observó respuesta de error:
- `{"Codigo":10500,"Mensaje":"Lo sentimos. Hemos detectado que existen peticiones simultáneas."}`

Por diseño del skill:
- serializar llamadas
- evitar bursts
- respetar pausas cortas entre requests
- cachear resultados cuando sea razonable

### 4. No asumir que el ticket de prueba sirve bien para todo
El ticket de prueba funciona al menos para lookup de empresas, pero no confiar en él para flujos de producción.

## Regla de negocio central

**API primero, portal después.**

Usar la API pública cuando resuelva el caso con suficiente fidelidad. Reservar el portal privado para los casos donde la API no alcance, falte contexto autenticado del proveedor o exista una acción/revisión propia del portal.

## Matriz de decisión API vs portal

### Preferir API cuando el caso de uso sea:
- discovery de oportunidades
- búsqueda/listado por código, fecha, estado, comprador o proveedor
- lookup de proveedor o comprador
- reportería y monitoreo
- prefiltrado antes de revisar casos concretos en el portal
- enriquecimiento de contexto read-only

### Preferir portal privado cuando el caso de uso sea:
- revisar el estado real de una cuenta o entidad autenticada
- ver preguntas/respuestas, adjuntos, botones y restricciones visibles de una pantalla real
- validar ofertabilidad con contexto del proveedor
- revisar órdenes de compra desde la experiencia real del proveedor
- preparar cotización/oferta/reclamo hasta preconfirmación
- ejecutar una acción transaccional o con cambio de estado

## Regla práctica de decisión

### Si la pregunta del usuario es de tipo:
- "buscar"
- "listar"
- "monitorear"
- "reportar"
- "identificar oportunidades"

→ empezar por **API**.

### Si la pregunta del usuario es de tipo:
- "revisar mi caso real"
- "ver qué acciones tengo disponibles"
- "entender esta pantalla"
- "ejecutar/preparar una acción"

→ usar **portal privado**.

### Si la pregunta mezcla ambos planos

→ usar **API para reducir el espacio de búsqueda** y luego **portal para validar el caso concreto**.

## Guardrails técnicos

- Mantener el ticket fuera de archivos versionados.
- Evitar paralelismo agresivo.
- Tratar respuestas 500/10500 como posible límite o política anti-concurrencia, no como “sin datos”.
- Si la API falla, explicar eso y ofrecer fallback por portal o reintento seguro.

## Helper CLI

Script incluido en la skill:
- `scripts/mercado_publico_api.py`

### Configuración

Requiere ticket por variable de entorno (no hardcodear):

```bash
export MERCADO_PUBLICO_API_TICKET="TU_TICKET"
```

Si la variable no existe, el script falla con mensaje útil y código de salida `2`.

### Operaciones soportadas

```bash
# Empresas
python3 scripts/mercado_publico_api.py buscar-proveedor --rut 76123456-7
python3 scripts/mercado_publico_api.py buscar-comprador
python3 scripts/mercado_publico_api.py buscar-comprador --filter salud

# Licitaciones
python3 scripts/mercado_publico_api.py licitaciones --codigo 1509-5-L114
python3 scripts/mercado_publico_api.py licitaciones --fecha 02022014
python3 scripts/mercado_publico_api.py licitaciones --fecha 02022014 --estado activas
python3 scripts/mercado_publico_api.py licitaciones --fecha 02022014 --codigo-organismo 6945
python3 scripts/mercado_publico_api.py licitaciones --fecha 02022014 --codigo-proveedor 17793

# Órdenes de compra
python3 scripts/mercado_publico_api.py ordenes --codigo 2097-241-SE14
python3 scripts/mercado_publico_api.py ordenes --fecha 02022014
python3 scripts/mercado_publico_api.py ordenes --fecha 02022014 --estado aceptada
python3 scripts/mercado_publico_api.py ordenes --fecha 02022014 --codigo-organismo 6945
python3 scripts/mercado_publico_api.py ordenes --fecha 02022014 --codigo-proveedor 17793
```

### Flags nuevas y comportamiento (v1.1)

- `--cache-ttl <segundos>`: activa caché local TTL (default `0`, sin caché).
- `--cache-dir <path>`: ruta alternativa para caché. Default: `skills/mercado-publico-chilecompra/run/api-cache`.
- `--summary`: salida breve estable en formato `clave=valor` (útil para monitoreo ligero).

Notas de caché:
- La clave de caché se calcula desde endpoint + query normalizada (hash SHA-256).
- Si hay hit vigente (`age <= ttl`), no llama a la API.
- Si el cache está vencido, hace request nuevo y reemplaza cache.
- No hay fallback automático a cache vencido cuando falla la API (comportamiento explícito y simple).

### Summary estable (`--summary`)

La salida es intencionalmente corta y consistente:
- incluye siempre `summary_version`, `command`, `source`, `count`
- cuando caché está activa: `cache_ttl_seconds`, `cache_age_seconds`
- agrega campos de consulta + primer registro para cada comando

Cobertura mínima v1.1:
- `buscar-proveedor`
- `buscar-comprador`
- `licitaciones --codigo`
- `licitaciones --fecha ...`
- `ordenes --codigo`
- `ordenes --fecha ...`

### Ejemplos concretos

```bash
# 1) Consultar licitación por código con caché por 10 minutos y salida estable
python3 scripts/mercado_publico_api.py \
  --cache-ttl 600 --summary \
  licitaciones --codigo 1509-5-L114

# 2) Consultar órdenes por fecha + estado usando directorio de caché custom
python3 scripts/mercado_publico_api.py \
  --cache-ttl 300 --cache-dir ./tmp/mp-cache --summary \
  ordenes --fecha 02022014 --estado aceptada

# 3) Buscar comprador filtrado localmente y resumen corto
python3 scripts/mercado_publico_api.py \
  --summary buscar-comprador --filter salud
```

### Comportamiento de robustez

- Llamadas seriales (1 request por ejecución).
- Timeout configurable (`--timeout`, default 15s).
- Retries suaves con backoff corto para errores transitorios (`--max-retries`, `--backoff`).
- Manejo explícito de `Codigo 10500` / “peticiones simultáneas”.
- Salida JSON legible por defecto (`pretty`).
- Modo `--summary` estable para lectura humana y automatización simple.
