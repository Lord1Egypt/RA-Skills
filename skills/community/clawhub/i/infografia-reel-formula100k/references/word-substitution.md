# Word Substitution — Sustitución de palabras problemáticas

Módulo que se aplica al brief ANTES de generar la imagen base. Resuelve dos problemas conocidos:

1. **Falsos positivos NSFW** del moderador de seedance_2_0 (rara vez también de nano_banana_2).
2. **Palabras largas** (>8 letras) que tienden a deformarse al animar el video, especialmente
   cuando comparten línea con otra palabra larga.

---

## CUÁNDO APLICAR EL MÓDULO

Se ejecuta en el **Paso 1.5** del pipeline (entre destilar el brief y clasificar arquetipo):

```
Paso 1   — Destilar input → brief
Paso 1.5 — APLICAR WORD SUBSTITUTION → brief sanitizado
Paso 2   — Clasificar arquetipo
Paso 3+  — (resto del pipeline)
```

---

## DICCIONARIO DE SUSTITUCIONES

### Triggers NSFW conocidos (seedance_2_0)

| Palabra original | Reemplazo | Motivo |
|---|---|---|
| FURminator | deshedder / cepillo deshedder | Marca registrada confunde el filtro |
| anti-flea | de pulgas / pulguicida | "anti-X" dispara falso positivo |
| anti-pulgas | de pulgas | Mismo |
| deshedding | de muda / quita-pelo | Verbo confuso |
| pet harness | arnés | "harness" trigger |
| spray | rociado / aplicador | A veces dispara |

### Palabras largas propensas a romperse (>8 letras)

Cuando una etiqueta tiene una palabra de más de 8 letras Y comparte línea con otra palabra larga,
la animación del video tiende a romperla en frames. Sustituir por sinónimo corto:

| Palabra larga | Reemplazo corto | Notas |
|---|---|---|
| sensibles (9) | delicados (9) o "Pieles sensibles" | Cambiar el sujeto puede ayudar |
| Mantenimiento (13) | Diario / Cuidado | Brutal en 9:16 |
| Diagnóstico (11) | Detecta / Examen | Cabe mejor |
| Profesional (11) | Pro / Experto | |
| Específico (10) | Puntual / Único | |
| Recomendado (11) | Sugerido / Top | |
| Extraordinario (14) | Extra / Premium | Casi nunca cabe |
| Convencional (12) | Clásico / Común | |
| Limpieza profunda (16) | Detox / Limpieza | Comprimir |
| Hidratación (11) | Hidrata / Agua | Verbo en lugar de sustantivo |
| Rejuvenece (10) | Renueva / Joven | |

### Palabras que conviene poner en MAYÚSCULA

Algunos sustantivos cortos rinden mejor en UPPERCASE como pill destacado en lugar de
intentar caber en una línea de descripción:

| Lower-case | UPPERCASE pill | Cuándo |
|---|---|---|
| cuidado intensivo | INTENSIVO | Si la línea es estrecha |
| uso diario | DIARIO | |
| sólo profesionales | PRO | |

---

## ALGORITMO

```python
def sanitize_brief(brief: dict) -> dict:
    out = deepcopy(brief)
    
    # Paso 1: aplicar diccionario NSFW (siempre)
    for key in ["hook_principal", "sub_hook_a", "sub_hook_b"]:
        if out.get(key):
            out[key] = apply_dict(out[key], NSFW_DICT)
    
    for item in out.get("items", []):
        item["nombre"] = apply_dict(item["nombre"], NSFW_DICT)
        item["atributo"] = apply_dict(item["atributo"], NSFW_DICT)
    
    # Paso 2: detectar palabras largas en atributos del brief
    LONG_THRESHOLD = 8
    for item in out.get("items", []):
        atributo = item["atributo"]
        # Si la frase tiene 2+ palabras largas o 1 palabra >10 letras
        long_words = [w for w in atributo.split() if len(w) > LONG_THRESHOLD]
        if len(long_words) >= 2 or any(len(w) > 10 for w in long_words):
            # Aplicar diccionario LONG_DICT
            atributo = apply_dict(atributo, LONG_DICT)
            item["atributo"] = atributo
    
    return out
```

---

## CONFIRMACIÓN AL USUARIO

Cuando el módulo realice una sustitución, **avisarle al usuario** en una línea corta antes de
generar:

```
🛡  Sanitización aplicada:
   • "Gatos sensibles" → "Pieles sensibles" (palabra larga propensa a romperse en video)
   • "FURminator" mantenido en imagen, suavizado a "deshedder" en prompt de video
¿Continuamos con estos textos? (sí / cambia X por Y)
```

Si el usuario propone su propia sustitución, respetarla y agregar la entrada al diccionario en
una sección "Custom" (no commitear, sólo memoria de la sesión).

---

## MARCAS REGISTRADAS

Algunas marcas (FURminator, Roomba, Kleenex) **conviene mantenerlas en la imagen** (es lo que
busca la audiencia) pero **suavizarlas en el prompt del video** porque los moderadores de
modelos de IA se ponen nerviosos:

- Imagen → "FURminator-style deshedding tool" (en prompt nano_banana_2 está OK)
- Video → "deshedding tool" o "yellow grooming tool" (sin nombre de marca)

Documentar esto en el `prompts.md` del output para auditoría.
