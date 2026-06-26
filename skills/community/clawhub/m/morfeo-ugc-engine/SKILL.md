# Morfeo UGC Engine Skill

Sistema autónomo de generación de videos UGC para marcas argentinas.
Genera contenido TikTok/Instagram que parece orgánico pero termina con un plot twist revelando que es IA de Morfeo Labs.

## Cuándo usar esta skill

Cuando Paul pida:
- "generá un video de [marca]"
- "corré el pipeline"
- "qué runs hay en curso"
- "avanzá el run de [marca] al siguiente paso"
- "mostrá el estado del engine"
- "publicá el video de [run]"
- Cualquier operación sobre el Morfeo UGC Engine

---

## Configuración

### API Local
- **Base URL**: `http://localhost:3336`
- **Token**: `morfeo-admin-2026` (o `$MORFEO_API_TOKEN`)
- **Auth header**: `Authorization: Bearer morfeo-admin-2026`
- **Project header**: `x-project-id: morfeo_labs`

### Proyectos disponibles
- `morfeo_labs` — Pipeline principal (productos argentinos)
- `animado` — Variante estilo animado

### Paths clave
- API: `~/clawd/projects/morfeo-engine/api/server.js`
- Pipeline: `~/clawd/projects/morfeo-content-engine/pipeline.py`
- Outputs: `~/clawd/projects/morfeo-content-engine/output/`
- PM2: `morfeo-engine-api` (puerto 3336)

---

## Endpoints principales

```bash
BASE="http://localhost:3336"
TOKEN="morfeo-admin-2026"
H_AUTH="Authorization: Bearer $TOKEN"
H_PROJ="x-project-id: morfeo_labs"
```

### Ver todos los runs
```bash
curl -s "$BASE/api/runs" -H "$H_AUTH" -H "$H_PROJ" | python3 -c "
import json,sys
runs = json.load(sys.stdin)
for r in runs[:10]:
    print(f\"{r['id']} | {r['stage']:12} | {r.get('brief',{}).get('marca_nombre','?') if r.get('brief') else '?'}\")"
```

### Crear run nuevo (elegir marca aleatoria del catálogo)
```bash
curl -s -X POST "$BASE/api/queue/add" \
  -H "$H_AUTH" -H "$H_PROJ" -H "Content-Type: application/json" \
  -d '{"marca_id": null}'  # null = aleatoria
```

### Crear run con marca específica
Primero obtener ID de la marca:
```bash
curl -s "$BASE/api/marcas" -H "$H_AUTH" -H "$H_PROJ" | python3 -c "
import json,sys
for m in json.load(sys.stdin):
    print(m['id'], m['nombre'])"
```
Luego crear run:
```bash
curl -s -X POST "$BASE/api/queue/add" \
  -H "$H_AUTH" -H "$H_PROJ" -H "Content-Type: application/json" \
  -d "{\"marca_id\": \"havanna\"}"
```

### Ver estado de un run
```bash
RUN_ID="20260307_190100"
curl -s "$BASE/api/runs/$RUN_ID" -H "$H_AUTH" -H "$H_PROJ" | python3 -c "
import json,sys
r = json.load(sys.stdin)
print('Stage:', r['stage'])
print('Status:', r['status'])
print('Marca:', r.get('brief',{}).get('marca_nombre','?') if r.get('brief') else '?')
print('Video:', r.get('video_url','ninguno'))"
```

### Avanzar run a la siguiente etapa
```bash
curl -s -X POST "$BASE/api/runs/$RUN_ID/advance" \
  -H "$H_AUTH" -H "$H_PROJ" -H "Content-Type: application/json"
```

### Regenerar campo específico del guión
```bash
# campos: HOOK, STORY_1, STORY_2, PLOT_TWIST, CTA
curl -s -X POST "$BASE/api/runs/$RUN_ID/regen-guion-field" \
  -H "$H_AUTH" -H "$H_PROJ" -H "Content-Type: application/json" \
  -d '{"field": "HOOK"}'
```

### Seleccionar shots para el video (índices 0-9)
```bash
curl -s -X PUT "$BASE/api/runs/$RUN_ID/shots-selection" \
  -H "$H_AUTH" -H "$H_PROJ" -H "Content-Type: application/json" \
  -d '{"shots": [0, 2, 4, 6, 8]}'
```

### Publicar en redes (Postiz → borrador)
```bash
curl -s -X POST "$BASE/api/runs/$RUN_ID/publish" \
  -H "$H_AUTH" -H "$H_PROJ" -H "Content-Type: application/json"
```

### Ver log de ejecución
```bash
curl -s "$BASE/api/log?run_id=$RUN_ID" -H "$H_AUTH" -H "$H_PROJ"
```

---

## Stages del pipeline

| Stage | Descripción |
|-------|-------------|
| `pending` | Esperando inicio |
| `brief` | Guión generado ✓ |
| `portrait` | Personaje diseñado ✓ |
| `hero` | Escena Morpheus generada ✓ |
| `multishot` | 10 variaciones generadas ✓ |
| `video` | Video con lip-sync listo ✓ |
| `published` | Publicado en redes ✓ |

---

## Flujo completo manual (modo supervisor)

```
1. Crear run con marca → POST /api/queue/add
2. Esperar brief (stage=brief) → ver guión y personaje
3. Si guión ok → POST /advance
4. Esperar portrait (stage=portrait) → ver imagen del personaje
5. Si personaje ok → POST /advance
6. Esperar hero (stage=hero) → ver escena Morpheus
7. Si escena ok → POST /advance
8. Esperar multishot (stage=multishot) → ver 10 shots
9. Seleccionar 5 mejores → PUT /shots-selection
10. POST /advance → genera videos con lip-sync
11. Esperar video (stage=video) → ver video final
12. Si ok → POST /publish → borrador en Postiz
```

---

## Polling de un run en curso

```python
import requests, time

BASE = "http://localhost:3336"
HEADERS = {
    "Authorization": "Bearer morfeo-admin-2026",
    "x-project-id": "morfeo_labs"
}

def poll_run(run_id, target_stage, timeout=600):
    """Espera hasta que el run llegue a target_stage."""
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{BASE}/api/runs/{run_id}", headers=HEADERS).json()
        stage = r.get("stage", "")
        print(f"Stage: {stage}")
        if stage == target_stage or r.get("status") == "error":
            return r
        time.sleep(15)
    return None
```

---

## Operaciones de diagnóstico

### Verificar que la API está levantada
```bash
curl -s http://localhost:3336/api/runs -H "Authorization: Bearer morfeo-admin-2026" -H "x-project-id: morfeo_labs" | python3 -c "import json,sys; print(len(json.load(sys.stdin)), 'runs')"
```

### Levantar API si está caída
```bash
cd ~/clawd/projects/morfeo-engine/api && pm2 restart morfeo-engine-api
# Si no existe: pm2 start server.js --name morfeo-engine-api
```

### Ver logs en tiempo real
```bash
pm2 logs morfeo-engine-api --lines 50
```

### Ver outputs del día
```bash
ls ~/clawd/projects/morfeo-content-engine/output/ | sort -r | head -10
```

---

## Marcas disponibles (pool principal)

Havanna, Bon o Bon, Topper, Mantecol, Stella Artois, Andes Origen, Quilmes, Fernet Branca, Yerba Taragüí, Dulce de Leche La Serenísima, Alfajores Terrabusi, CasanCrem, Freddo, Ketchup Heinz, Mayonesa Hellmann's, y ~20 más en `~/clawd/projects/morfeo-content-engine/pipeline.py` (MARCAS_ARG).

---

## Notas importantes

- **Postiz siempre a DRAFT** — nunca publicar directo, verificar manualmente
- El pipeline puede tardar 10-30 min por etapa (ComfyDeploy + VEED)
- Los outputs se guardan en `/output/YYYYMMDD_HHMMSS/`
- Para ver el video final: `~/clawd/projects/morfeo-content-engine/output/<run_id>/final_tg.mp4`
- El dashboard visual está en `https://morfeo-engine-ui.vercel.app`
