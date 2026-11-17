# Brief de motion graphics (1 página)

Copia, rellena, firma con el cliente. Si algo queda vacío, es un riesgo del proyecto.

```yaml
proyecto:            ""
cliente:             ""
fecha_entrega:       ""
version:             "v01"

# 1. Qué
mensaje:             ""          # una frase, ≤ 12 palabras
objetivo:            []          # informar / vender / explicar / entretener / recordar marca
publico:             ""          # quién, en qué contexto y en qué dispositivo
dolor_o_deseo:       ""

# 2. Formato
plataformas:         []          # YouTube / IG Reels / TikTok / web / presentación / TV
aspect_ratios:       []          # 16:9, 9:16, 1:1, 4:5
resolucion:          "1080p"     # 1080p / 4K
fps:                 30          # 24 cine, 25 broadcast, 30 web, 60 deporte/UI
duracion_objetivo:   ""          # en segundos
con_audio:           true        # hay voz / solo música / mudo
con_voz:             false
subtitulos:          false       # quemados / .srt / ninguno

# 3. Cómo suena y se ve
tono:                []          # 3 adjetivos
bpm:                 ""          # o "sin música definida"
referencias:         []          # 3 links, con nota de QUÉ te gusta de cada uno
evitar:              []          # lo que el cliente no quiere ver/escuchar
paleta_cliente:      []          # hex oficiales
tipografia_cliente:  []          # familia + pesos disponibles
logo_assets:         ""          # ruta / link a SVG y normas de marca

# 4. Entregables
entregables:         []          # master, MP4, alpha, MOGRT, plantilla, fuente
archivos_fuente:     true        # ¿el cliente pide el proyecto?
licencia_musica:     ""          # quién la compra
num_revisiones:      2

# 5. Producción
responsable:         ""
aprobador:           ""
hitos:               {}          # guion / animatic / v01 / final
notas:               ""
```

## Supuestos por defecto si falta información

Declara estos supuestos en voz alta y sigue trabajando; no bloquees el proyecto:

1. Formato principal 16:9 a 1920×1080, 30 fps.
2. Duración de 15 s si no se especifica (o 8 s para stinger, 30 s para explainer).
3. 120 BPM si no hay música definida.
4. Dos familias tipográficas: una display y una de texto.
5. Entregables: master ProRes + MP4 H.264 + versión muda.
6. Dos rondas de revisión.
7. Música con licencia a cargo del cliente si no se sintetiza.
