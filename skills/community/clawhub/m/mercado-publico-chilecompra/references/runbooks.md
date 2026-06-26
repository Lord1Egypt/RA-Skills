# Runbooks operativos mínimos

## Regla previa a cualquier runbook

Antes de abrir el portal, evaluar si el caso se puede resolver por API pública.

- Si es discovery, búsqueda, listado, reportería o prefiltrado → intentar primero por API.
- Si es revisión autenticada, validación de ofertabilidad real, lectura de botones/estados del proveedor o preparación/ejecución de acciones → usar portal.
- Si hace falta ambos, usar API para reducir candidatos y portal para confirmar el caso final.

Source of truth para esta decisión:
- `references/api-publica.md`

## Uso

Aplicar estos runbooks solo con sesión `authenticated` y entidad correcta seleccionada. Mantener secuencia base: **leer → preparar → confirmar → ejecutar**.

---

## 1) Buscar licitación

1. Entrar por `Menu.aspx` y navegar al módulo de Licitaciones (evitar deep link directo inicial).
2. Confirmar filtros con el usuario: código, organismo, estado, fecha de cierre, rubro.
3. Ejecutar búsqueda con el set mínimo de filtros para evitar falsos negativos.
4. Refinar filtros progresivamente si hay demasiados resultados.
5. Abrir detalle de la licitación objetivo y validar que corresponde al requerimiento.
6. Resumir hallazgos clave: estado, fecha/hora cierre, modalidad, documentos disponibles.

**Guardrails**
- No asumir que “sin resultados” implica inexistencia; revisar contexto/iframe/rango de fechas.
- No avanzar a ofertar sin confirmación explícita.

---

## 2) Revisar licitación y ofertabilidad

1. Verificar identificación exacta: ID licitación, organismo, nombre, etapa.
2. Revisar bases/adjuntos y registrar requisitos críticos (técnicos, administrativos, garantías, plazos).
3. Identificar restricciones de habilitación del proveedor (estado hábil, categoría, documentos vigentes).
4. Validar ventanas de tiempo: cierre de preguntas, cierre de ofertas, actos asociados.
5. Evaluar viabilidad operativa en formato semáforo:
   - Verde: ofertable sin bloqueo aparente.
   - Amarillo: ofertable con aclaraciones/riesgos.
   - Rojo: no ofertable por bloqueo objetivo.
6. Preparar checklist de pre-oferta y pendientes.
7. Pedir decisión humana para continuar o descartar.

**Guardrails**
- No inferir cumplimiento documental sin evidencia explícita en portal/adjuntos.
- No presionar botón de envío/oferta sin confirmación final.

---

## 3) Revisar orden de compra

1. Navegar a módulo de Órdenes de Compra desde el menú autenticado.
2. Buscar por número OC, comprador, rango de fechas o estado.
3. Abrir detalle de la OC y extraer: ítems, cantidades, montos, plazos, estado, hitos de aceptación.
4. Verificar acciones habilitadas (aceptar, rechazar, solicitar cancelación, adjuntar respaldo).
5. Identificar bloqueos o inconsistencias (botones deshabilitados, estado no hábil, errores de ruta).
6. Entregar resumen operativo y opciones de acción con impacto.
7. Solicitar confirmación explícita antes de cualquier cambio de estado.

**Guardrails**
- No aceptar/rechazar/cancelar sin instrucción explícita del usuario.
- Si hay error de portal, diagnosticar antes de reintentar acción sensible.

---

## 4) Preparar cotización hasta preconfirmación

1. Ingresar al flujo de Cotizaciones / Trato Directo / Compra Ágil aplicable.
2. Confirmar convocatoria objetivo, vigencia y reglas del formulario.
3. Levantar insumos requeridos: precios, condiciones comerciales, plazos, observaciones, adjuntos.
4. Completar borrador en portal sin enviar.
5. Validar consistencia de montos, unidades, moneda, impuestos y anexos.
6. Generar preconfirmación para el usuario:
   - qué se completó
   - qué falta
   - qué riesgo detectado existe
7. Esperar autorización explícita para envío final.

**Guardrails**
- No pulsar enviar/confirmar definitivo sin aprobación expresa.
- Si el portal cambia de ruta o embebe iframe inesperado, pausar y revalidar contexto.

---

## 5) Diagnosticar error del portal

1. Capturar síntoma exacto: mensaje, URL, módulo, acción previa, timestamp.
2. Clasificar error inicial:
   - 404 / ruta
   - `NullReferenceException` u otro ASP.NET
   - botón deshabilitado
   - redirección inesperada
   - CAPTCHA/validación externa
3. Probar recuperación segura mínima:
   - volver a menú autenticado
   - recargar módulo por navegación oficial
   - verificar sesión y entidad activa
4. Determinar causa probable: contexto roto, sesión vencida, bug del portal, prerrequisito faltante, permisos.
5. Proponer siguiente paso seguro y costo de riesgo.
6. Escalar a intervención humana cuando el diagnóstico no sea concluyente o la acción siguiente implique riesgo de estado.

**Guardrails**
- No ejecutar “pruebas” que cambien estado para depurar.
- No ocultar incertidumbre: explicitar hipótesis y nivel de confianza.

---

## Checklist previo a ejecutar acciones sensibles

- Entidad correcta confirmada.
- Estado del trámite vigente validado.
- Evidencia mínima leída y resumida.
- Impacto de la acción explicado.
- Confirmación explícita del usuario recibida.
