---
name: investigacion-nicho-formula100k
description: "Investigación estratégica de nicho para creadoras de contenido con la metodología F100K. Usar cuando una creadora quiere validar si un nicho tiene potencial antes de invertir tiempo, cuando quiere analizar la competencia en Skool/TikTok/IG, cuando quiere saber si su oferta tiene mercado, o cuando necesita un brief de posicionamiento antes de crear contenido o lanzar una comunidad. Output = decisión con evidencia real, no teoría."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - La fila «agent-browser» del stack no corre aquí. Perfiles de IG/TikTok y engagement: Apify con `APIFY_TOKEN` (datos públicos). Sin token, trabaja con búsqueda web y marca seguidores y engagement como `[NO VERIFICADO]`.
> - Comunidades de Skool, páginas de venta y precios de la competencia: tu navegador (Chromium) sobre las páginas PÚBLICAS, sin iniciar sesión (skool.com/discovery, la landing «about» de cada comunidad). Lo que solo se ve adentro de la comunidad queda como no disponible.
> - vidIQ solo si está conectado; si no, busca outliers de YouTube con tu búsqueda web y dilo.
> - La «voz de la audiencia (verbatim)» sale de comentarios reales (Apify o capturas que mande la usuaria) o de foros y reseñas públicas: nunca parafrasees como si fuera cita.
> - El brief se guarda en `informes/nicho-<slug>-AAAA-MM-DD.md`; por Telegram manda el resumen ejecutivo y la recomendación, con el archivo completo como documento.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método**. El método es agnóstico de industria: sirve igual para
formulación cosmética, nutrición, repostería, fisioterapia, finanzas o jabonería.
Los ejemplos escritos aquí abajo son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (léelo de su Segundo Cerebro, de su perfil o
   pregúntaselo en una línea si no está claro). Decláralo: *"Rubro: ___"*.
2. Todos los ejemplos, analogías, comparaciones, objeciones, métricas y vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes sociales, creación de contenido, ventas online o
   negocios digitales → queda **PROHIBIDO** el vocabulario de ese mundo (reels, algoritmo,
   embudo, lead magnet, engagement, "publicar sin vender", "clientes de alto ticket",
   "escalar tu negocio", "posicionarte como referente"), salvo que la persona lo escriba primero.
4. Si el rubro es **técnico, científico o de oficio**: NO borres el tecnicismo para
   "simplificar". Úsalo y **tradúcelo en su primera mención**. El término preciso ES la
   autoridad de esa creadora; quitarlo borra justo lo que la diferencia.
5. Si no tienes datos suficientes del negocio, dilo y usa marcadores explícitos
   (`[TU OFERTA]`, `[TU RESULTADO]`). **Nunca asumas que el rubro es marketing.**

**El método viaja, el rubro no.** El mismo molde, vestido con rubros distintos:

| Rubro | El mismo molde |
|---|---|
| Cocina | "Así es mi cena favorita para no dormir con el azúcar alta." |
| Relaciones | "5 señales de que estás forzando una relación que ya no funciona." |
| Finanzas | "La principal causa de un divorcio no es una infidelidad." |
| Formulación cosmética | "El conservante decide si tu crema dura tres meses o te da una infección. No el aceite." |
| Jabonería | "Si tu jabón se pone blando a los dos días, no fue el aceite. Fue la sosa." |
| Fisioterapia | "Ese dolor de rodilla al bajar escaleras casi nunca nace en la rodilla." |
| Repostería | "Tu bizcocho se hunde en el centro por la temperatura, no por la harina." |
| Jardinería | "Tu planta no se está muriendo de sed. Se está ahogando." |

Mismo molde en todos; ninguno menciona reels ni embudos. Haz exactamente eso.

---

# Investigación de Nicho — Fórmula 100K

Produce investigación que sustenta decisiones reales, no investigación de adorno.

## Cuándo activar

- Una creadora quiere entrar a un nuevo nicho y no sabe si tiene demanda
- Necesita entender quién más está en ese espacio y cómo se posicionan
- Va a lanzar una comunidad Skool y quiere validar el ángulo antes de construirla
- Quiere saber qué preguntas/dolores reales tiene su audiencia objetivo
- Necesita un brief de posicionamiento antes de empezar a crear contenido

## Estándar de investigación

1. Todo dato importante necesita fuente real (cuenta real, post real, número real).
2. Preferir datos recientes. Si el dato tiene más de 6 meses, marcarlo como posiblemente obsoleto.
3. Incluir evidencia contraria y escenarios de riesgo.
4. Traducir hallazgos en UNA decisión clara, no en un resumen neutro.
5. Separar explícitamente: hecho / inferencia / recomendación.

## Stack de investigación

| Motor | Qué caza |
|-------|----------|
| **agent-browser** | Perfiles reales en IG/TikTok, engagement real, comunidades Skool activas, qué contenido funciona en ese nicho |
| **Apify** | Scraping de cuentas IG sin sesión, volumen de seguidores, posts recientes, cuando agent-browser no tiene sesión activa |
| **Tavily MCP** | Tendencias web, búsquedas de palabras clave, artículos del sector, validación cruzada de demanda |
| **vidIQ MCP** | YouTube: qué tan buscado es el tema, outliers del nicho, preguntas reales en comentarios |

## Modos de investigación

### Modo 1: Validación de nicho (¿tiene demanda?)

Recolectar:
- ¿Hay cuentas con +10k seguidores hablando de esto? (señal de demanda)
- ¿Cuánto engagement real tienen vs views? (ratio mide calidad de audiencia)
- ¿Hay comunidades Skool activas en este nicho? ¿Cuántos miembros? ¿Gratis o pago?
- ¿Qué palabras usa la audiencia para describir su problema? (verbatim, no paráfrasis)
- ¿Hay búsquedas en YouTube? ¿Cuántas vistas tienen los outliers?

### Modo 2: Análisis de competencia (¿cómo está posicionado el mercado?)

Para cada competidor directo/adyacente, recolectar:
- Propuesta de valor real (lo que dicen, no lo que uno asume)
- Precio y modelo de negocía
- Tamaño de audiencia y plataforma principal
- Qué funciona (posts con más engagement) y qué no (posts ignorados)
- Huecos: ¿qué pregunta frecuente nadie está respondiendo?

### Modo 3: Diagnóstico de audiencia (¿qué quiere realmente?)

- Top 5 dolores reales de la audiencia (sacar de comentarios, no inventar)
- Lenguaje exacto que usan para describir su problema (verbatim)
- Qué soluciones ya intentaron y por qué no funcionaron
- Qué resultado específico están buscando

## Formato de output

Estructura default:

```
### 1. RESUMEN EJECUTIVO
[2-3 oraciones: ¿tiene potencial este nicho? ¿por qué sí / no / con qué condiciones?]

### 2. EVIDENCIA DEL MERCADO
- Cuentas encontradas: [nombres reales + seguidores + link]
- Comunidades Skool: [nombres + miembros + precio]
- Volumen de búsqueda YouTube: [keywords + views de outliers]
- Conclusión: nicho [saturado / en crecimiento / virgen / de difícil acceso]

### 3. ANÁLISIS DE COMPETENCIA
[tabla: Cuenta | Plataforma | Audiencia | Propuesta | Precio | Hueco]

### 4. VOZ DE LA AUDIENCIA (verbatim)
- Dolores reales: [citas textuales de comentarios/posts]
- Lenguaje exacto: [cómo llaman ellos al problema]
- Resultado deseado: [qué quieren lograr en sus propias palabras]

### 5. HUECOS DE MERCADO
[Lo que nadie está haciendo bien en este nicho]

### 6. RECOMENDACIÓN
[Decisión clara: entrar / esperar / pivotear + ángulo de posicionamiento sugerido]

### 7. FUENTES
[Links reales usados]
```

## Gate de calidad

Antes de entregar:
- Todos los números tienen fuente real o están marcados como estimados
- Los datos viejos están señalados
- La recomendación se sigue lógicamente de la evidencia
- Se incluyen riesgos y casos contrarios
- El output hace más fácil tomar una decisión, no más confusa

## Conexión con otros skills F100K

Usar este skill ANTES de:
- `creador-estrategia-contenido-formula100k` — el brief de nicho alimenta la estrategia
- `campana-lanzamiento-formula100k` — el posicionamiento saldrá de aquí
- `calendarizador-contenido-formula100k` — los dolores y lenguaje van al calendario
- `creadora-comunidades-skool` — validar el ángulo antes de construir la estructura
