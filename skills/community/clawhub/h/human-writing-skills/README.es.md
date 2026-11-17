# Advanced Human Writing & AI Humanizer

<p align="center"><img src="assets/logo.png" width="320" alt="Human Writing: escritura con pluma y código de terminal sobre fondo blanco cálido"></p>

> Escritura con IA más natural: edición multilingüe, colaboración por secciones y revisión de la coherencia en textos largos, mediante Skills y un plugin para DSH.

**Búsquedas:** humanizar texto IA, quitar tono de IA, eliminar estilo robótico, revisión de novela, coherencia narrativa, auditoría de capítulos, consistencia de personajes, revisión de diálogos, estilo natural en español, traducción natural, evitar calcos de traducción, redacción de noticias, revisión de artículos académicos.

Este repositorio contiene instrucciones reutilizables y un compilador ligero de prompts. No promete identificar autoría ni eludir detectores: ayuda a editar textos para que sean específicos, verificables, coherentes y apropiados para su género.

## Qué resuelve

- Narrativa y novelas: personajes, relaciones, espacio, objetos, vestuario, cronología, deudas de diálogo, voz y desarrollo entre capítulos.
- Noticias, informes, documentos formales y artículos académicos: atribución, alcance de las afirmaciones, terminología, cifras, citas y fuentes protegidas.
- Texto multilingüe: español, portugués, francés, inglés, chino, japonés, árabe, latín y otros idiomas admitidos por el modelo elegido.
- Traducción y localización: evita el orden literal, conectores heredados, falsos amigos y una voz neutra de traducción, sin borrar términos ni referencias culturales.
- Textos largos: divide novelas, series de artículos e informes en bloques auditables, mantiene una línea base y reconcilia cambios entre bloques.

Para novelas de al menos tres capítulos, `chunk-audit --book-level` añade una sola revisión de decisiones, consecuencias y evolución del conflicto después de los bloques. No se activa en informes ni en la revisión normal de un capítulo.

`verify` comprueba cifras y citas literalmente; `verify-fidelity --source original.md --candidate revisado.md` señala cambios de afirmación y exige revisar el sentido. La detección automática de documentos serios necesita varias pistas; indique `--document-type` si son escasas. Los ejemplos multilingües incluidos son pruebas preliminares, no una validación por hablantes nativos.

## Inicio rápido

```powershell
python -m humanwriting.cli humanize `
  --draft borrador.md `
  --style fiction `
  --mode deep `
  --task "Revisa el ritmo y conserva la voz de los personajes."

python -m humanwriting.cli audit `
  --draft capitulo.md `
  --context biblia-de-la-novela.md `
  --profile voice
```

Use `--reference muestra-aprobada.md` o `--reference-style` solamente si se entregó una referencia explícita. La referencia aporta rasgos de estilo, nunca hechos, nombres o frases para copiar.

## Auditoría larga por bloques y agentes

Una sola conversación suele pasar por alto partes de un manuscrito largo. `chunk-audit` crea un paquete de tareas independientes: cada bloque tiene un cuerpo único, una pequeña entrada anterior de solo lectura y una línea base aprobada. Así se evita revisar dos veces el mismo texto y se conserva el contexto útil.

```powershell
python -m humanwriting.cli chunk-audit `
  --draft novela-completa.md `
  --style fiction `
  --outline biblia-de-la-novela.md `
  --reference capitulos-aprobados.md `
  --agent-mode deep `
  --output-dir auditoria-novela
```

Primero ejecute `00-baseline-prompt.md`. Después distribuya las tareas dependientes solo de `baseline` en conversaciones nuevas o solicitudes API separadas. Guarde cada resultado bajo `reports/` usando la ruta indicada en `agent-plan.json`.

```powershell
python -m humanwriting.cli verify-chunk-audit `
  --package-dir auditoria-novela
```

La verificación exige un **Coverage Receipt** por tarea: identifica el bloque, las unidades revisadas, los hallazgos y cualquier parte no revisada. Solo entonces se ejecuta `9999-reconcile-prompt.md`. El modo `standard` genera una revisión completa por bloque; `deep` añade revisión párrafo por párrafo, diálogo solo donde existe y, para textos serios con fuentes, verificación de evidencia.

## Traducción natural y localización

Active `translationese-audit` solo con un original, una dirección de traducción o una petición clara de localización. Para auditorías largas:

```powershell
python -m humanwriting.cli chunk-audit `
  --draft informe-es.md `
  --style news-report `
  --context plan-editorial.md `
  --source fuentes.md `
  --translationese `
  --agent-mode deep `
  --output-dir auditoria-informe
```

El módulo conserva cifras, nombres, citas, terminología, grado de certeza y atribución. No inventa jerga, acentos, palabras extranjeras ni una personalidad nacional.

## Carga según necesidad

El proyecto no carga todos los módulos a la vez:

- `voice`, `register`, espacio físico, relaciones y continuidad serial se activan solo cuando el encargo o el contexto los justifican.
- Las reglas de protección factual se cargan automáticamente solo para noticias, documentos formales y textos académicos, jurídicos o técnicos claramente identificados.
- `--agent-mode deep` es explícito, porque prioriza cobertura sobre ahorro de tokens.

## Documentación principal

- [README en inglés](README.md)
- [README 中文](README.zh-CN.md)
- [README em português](README.pt-BR.md)
- [README en français](README.fr.md)
- [Guía de consistencia para textos largos](docs/long-form-consistency.md)
- [Guía de auditoría por etapas](docs/audit-pipeline.md)

## Licencia

MIT. Consulte [LICENSE](LICENSE).
