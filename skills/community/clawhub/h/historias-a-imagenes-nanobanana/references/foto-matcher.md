# FOTO MATCHER — Cómo elegir la mejor foto del folder por slide

Algoritmo para que la skill seleccione automáticamente la foto base correcta de la carpeta del usuario.

---

## INPUT DEL MATCHER

Para cada slide:
- **Descripción de foto necesaria** del bloque ⚙️ del guion (ej: "la creadora caminando en escenario amplio")
- **Lista de archivos** de la carpeta de fotos del usuario

## OUTPUT

- **Path absoluto** de la foto elegida
- **Score de confianza** (0-1)
- **Razón** de la elección (para mostrar al usuario)

---

## ALGORITMO DE 3 ETAPAS

### Etapa 1 — Match por nombre de archivo

Si los archivos están bien nombrados (el usuario organiza con tags), buscar match exacto:

| Descripción del slide | Tags a buscar en filename |
|---|---|
| "playa", "rocas", "mar" | `playa*`, `rocas*`, `mar*`, `beach*` |
| "Buda", "estatua", "Japón" | `buda*`, `japon*`, `estatua*`, `temple*` |
| "escritorio", "laptop", "trabajando" | `escritorio*`, `laptop*`, `trabajo*`, `desk*` |
| "café", "cafetería" | `cafe*`, `cafeteria*`, `coffee*` |
| "calle", "caminando", "ciudad" | `calle*`, `caminando*`, `street*`, `city*` |
| "metro", "estación", "tren" | `metro*`, `estacion*`, `subway*` |
| "parque" | `parque*`, `park*` |
| "Disney", "Universal", "parque temático" | `disney*`, `universal*`, `parque-tematico*` |

Si encuentra match → Score 0.9, retornar.

### Etapa 2 — Match por características inferidas

Si el usuario no tagea por nombre, usar heurística:

1. **Por fecha de creación:** si la descripción dice "Japón" y hay un cluster de fotos de fechas similares (ej. todas en abril), priorizarlas
2. **Por carpeta:** si las fotos están organizadas en subcarpetas (ej. `/playa/`, `/escritorio/`), usar el nombre de la carpeta como tag
3. **Por hash visual** (si está disponible): usar `imagemagick` para extraer color dominante y comparar con la descripción (ej. "playa" → tonos azul/beige)

Score 0.5-0.7.

### Etapa 3 — Pedir al usuario

Si el match es ambiguo (varios candidatos con scores parecidos) o no hay match (<0.4):

Mostrar 3 candidatos al usuario y pedir elección:

```
"Para el slide 1 ('la creadora caminando en escenario amplio') tengo estos 3 candidatos:

1. cerebro/fotos/playa-japon-2026-04.jpg (Score 0.65)
2. cerebro/fotos/calle-tokio.jpg (Score 0.58)
3. cerebro/fotos/parque-universal.jpg (Score 0.52)

¿Cuál usamos? (responde 1, 2 o 3, o pásame la ruta de otra)"
```

---

## CACHE DENTRO DE UNA SESIÓN

Si una secuencia tiene 5 slides y los slides 1, 3, 5 piden "playa", la skill debe:

1. Resolver la foto UNA VEZ para "playa"
2. Cachear la elección
3. Reutilizar la misma foto para los 3 slides

Esto crea **continuidad visual** (igual que el usuario en sus secuencias reales — usa el mismo escenario para 2-3 slides).

Cache se guarda en variables de sesión, NO en disco.

---

## REGLAS DE PREFERENCIA

Cuando hay múltiples fotos posibles, preferir:

1. **Plano general** sobre primer plano (más espacio para texto/cajas)
2. **la creadora no centrada** (deja espacio a un lado para mockup/captura)
3. **Buena iluminación** (clara, natural)
4. **Fondo limpio** sin gente alrededor (si la hay, está borrosa)
5. **Aspect ratio cercano a 9:16** (si la foto es muy horizontal, marcar como menos ideal)

---

## EXTENSIONES SOPORTADAS

```
.jpg .jpeg .png .heic .heif .webp
```

Si encuentra `.heic` y el motor no los acepta directamente, convertir con:
```bash
magick convert input.heic output.jpg
```

---

## EJEMPLO COMPLETO

**Carpeta del usuario:** `~/Pictures/marca-personal/`

**Contenido:**
```
playa-japon-1.jpg
playa-japon-2.jpg
buda-templo-1.jpg
escritorio-laptop.jpg
calle-tokio-noche.jpg
disney-1.jpg
disney-2.jpg
parque-minions.jpg
metro-estacion.jpg
escritorio-noche.jpg
```

**Guion del slide 1 dice:** "la creadora caminando frente al Buda en Japón, plano general"

**Resultado del matcher:**
```
{
  "path": "~/Pictures/marca-personal/buda-templo-1.jpg",
  "score": 0.92,
  "razon": "Match por filename 'buda-templo-1' → exact tag match"
}
```

**Guion del slide 2 dice:** "captura de auditoría en escritorio"

**Resultado:**
```
{
  "path": "~/Pictures/marca-personal/escritorio-laptop.jpg",
  "score": 0.88,
  "razon": "Match por filename 'escritorio-laptop' → tag escritorio"
}
```

**Guion del slide 5 (CTA) dice:** "la creadora con escenario bonito tipo playa o parque"

**Resultado:**
```
{
  "path": "ASK_USER",
  "candidatos": [
    {"path": ".../playa-japon-1.jpg", "score": 0.7},
    {"path": ".../disney-1.jpg", "score": 0.65},
    {"path": ".../parque-minions.jpg", "score": 0.6}
  ],
  "razon": "Múltiples candidatos válidos — pedir elección al usuario"
}
```

---

## SI LA CARPETA ESTÁ VACÍA O FALTA

Si el usuario dio una carpeta pero no tiene fotos compatibles:

1. Listar lo que SÍ tiene
2. Preguntar si quiere:
   a. Subir más fotos a esa carpeta
   b. Cambiar de carpeta
   c. Generar las fotos desde cero con Higgsfield (sin foto base — riesgo: cara distinta)
   d. Saltarse este slide y dejarlo para después

Nunca proceder sin foto base si el slide la requiere — el output sería una persona random generada por IA, no la de otra persona.
