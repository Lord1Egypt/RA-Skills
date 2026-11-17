---
name: "mealie-recipe-import"
description: "Import recipes into a self-hosted Mealie instance from a photo, text, or URL, with AI ingredient parsing and cover image upload."
---

# Mealie Recipe Import

Add a recipe to a self-hosted [Mealie](https://mealie.io) instance (v1 API, app v3.x) from a photo, plain text, or a URL. Handles AI ingredient parsing, food/unit dedup + creation, recipe metadata, and cover-image upload. Verified against Mealie v3.21.0.

## Requirements

- A running self-hosted **Mealie** instance (v1 API / app v3.x; verified on v3.21.0) reachable over the network.
- A **Mealie API token** (see Setup).
- **Python 3** (standard library only) for the bundled script — no `pip install` needed.
- **For photo import:** an agent with a **vision/image capability** to transcribe the recipe. Plain-text and URL import work without vision.
- **Optional but recommended:** an **AI ingredient parser** configured in Mealie admin (OpenAI or Gemini) for best ingredient structuring; otherwise the built-in `nlp`/`brute` parser is used.

## Setup

Two env vars (never hardcode instance/token):

- `MEALIE_URL` — base URL, e.g. `http://mealie.example.lan:9925`
- `MEALIE_API_KEY` — long-lived Mealie API token

Get a token: Mealie UI -> user profile -> "Manage Your API Tokens" -> create; or `POST /api/users/api-tokens {"name":"agent"}`. Store it in your agent's `.env`, never in the skill.

Verify access:

```bash
curl -s -H "Authorization: Bearer $MEALIE_API_KEY" "$MEALIE_URL/api/users/self"   # 200 + user json
curl -s "$MEALIE_URL/api/app/about"                                                # version
```

## Workflow

1. **Extract.** Photo -> use your vision/image tool to transcribe: title, servings, times, ingredient lines (one per line, keep quantity + unit + note), and steps. Text -> use as-is. URL -> `POST /api/recipes/create/url {"url":..,"includeTags":false}` returns the slug (URL import parses ingredients weakly, so still run the parser in step 3).
2. **Create record** (photo/text): `POST /api/recipes {"name":"<Title>"}` returns the slug as a bare quoted JSON string.
3. **Parse ingredients:** `POST /api/parser/ingredients {"parser":"openai","ingredients":[...]}`. Each result item has `.ingredient` = `{quantity, unit|null, food|null, note, originalText, referenceId}` plus `.confidence.average`. The AI parser auto-resolves existing foods/units to their DB ids.
4. **Dedup + create foods/units.** `GET /api/foods?perPage=2000` and `GET /api/units?perPage=2000`. For any parsed food/unit that has no `id`: match by lowercased/trimmed name; if still missing `POST /api/foods {"name":..}` / `POST /api/units {"name":..}` and use the returned object. Prevents duplicate foods.
5. **Build + PUT recipe.** `GET /api/recipes/{slug}` for the full object, then set `recipeIngredient` (array), `recipeInstructions` (`[{title:"",text,ingredientReferences:[]}]`), `recipeServings` (number), `recipeYield` (string), `totalTime`/`prepTime` (strings), then `PUT /api/recipes/{slug}` with the modified object.
6. **Cover image:** `PUT /api/recipes/{slug}/image` as multipart form `image=@<file>;type=image/jpeg` + `extension=jpg` -> `{"image":"<n>"}`. If you have both a cookbook-page scan and a finished-dish photo, use the **finished dish** as the cover.
7. **Verify (VBR):** `GET /api/recipes/{slug}` (check name, servings, ingredient/instruction counts, image id) and `GET /api/media/recipes/{recipe_id}/images/original.webp` -> expect HTTP 200.

The bundled `scripts/mealie_import.py` performs steps 2 + 4-7 (and step 3 if you pass raw ingredient lines) from a JSON job file.

## recipeIngredient entry shape

```json
{
  "quantity": 250.0,
  "unit": { "id": "...", "name": "Gramm" },
  "food": { "id": "...", "name": "Tortellini" },
  "note": "dry",
  "isFood": true,
  "disableAmount": false,
  "originalText": "250 g dry tortellini",
  "referenceId": "<uuid>"
}
```

## Gotchas

- `parser:"openai"` selects whichever AI provider is configured in Mealie admin (OpenAI **or** Gemini). If no AI parser is configured, fall back to `"parser":"nlp"` or `"brute"`, or keep lines as plain notes (`food`/`unit` null, `disableAmount:true`).
- The parser can return a transient HTTP 500 -> retry once.
- Set `disableAmount:true` when an ingredient has no quantity and no unit (e.g. Salt, Pepper) so it renders as just the name.
- `POST /api/recipes` returns the slug as a bare quoted JSON string, not an object.
- URL import (`/api/recipes/create/url`) stores ingredients as weakly-parsed raw text -> re-run the parser and PUT.
- Every write needs the Bearer token; keep it in env only.

## Usage example (photo -> Mealie)

```bash
export MEALIE_URL=http://mealie.example.lan:9925
export MEALIE_API_KEY=****

# After transcribing the photo, write a job file:
cat > job.json <<'JSON'
{
  "title": "Party Tortellini Salad",
  "servings": 4,
  "yield": "4 servings",
  "total_time": "40 min",
  "instructions": [
    "Cook tortellini per package. Dice peppers, wedge tomatoes, strip the ham. Drain and cool.",
    "Whisk yogurt with sour cream, balsamic and chives. Season, fold everything in, rest 10 min, serve."
  ],
  "ingredient_lines": [
    "250 g dry tortellini", "Salt", "1 yellow bell pepper", "1 green bell pepper",
    "4 tomatoes", "6 slices cooked ham", "250 g low-fat yogurt", "2 tbsp sour cream",
    "1 tbsp balsamic vinegar", "3 tbsp chives", "Pepper"
  ],
  "parser": "openai",
  "image_path": "/path/to/finished-dish.jpg"
}
JSON

python3 scripts/mealie_import.py job.json
```
