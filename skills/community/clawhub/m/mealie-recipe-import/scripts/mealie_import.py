#!/usr/bin/env python3
"""Create/fill a Mealie recipe from a JSON job file (stdlib only).

Env:
  MEALIE_URL      base URL, e.g. http://mealie.example.lan:9925
  MEALIE_API_KEY  long-lived Mealie API token

Usage:
  python3 mealie_import.py job.json

job.json fields (all optional unless noted):
  title            recipe title (required unless slug given)
  slug             existing recipe slug; if set, skip create
  servings         number
  yield            string
  total_time       string
  prep_time        string
  instructions     ["step text", ...]
  ingredient_lines ["250 g dry tortellini", ...]  parsed via the AI parser
  parsed_ingredients   pre-parsed list (output of /api/parser/ingredients)
  parser           "openai" (default) | "nlp" | "brute"
  image_path       cover image file (uploaded as-is)
"""
import json, os, sys, time, uuid, mimetypes
import urllib.request, urllib.error

BASE = os.environ.get("MEALIE_URL", "").rstrip("/")
KEY = os.environ.get("MEALIE_API_KEY", "")
if not BASE or not KEY:
    sys.exit("Set MEALIE_URL and MEALIE_API_KEY env vars.")
AUTH = {"Authorization": "Bearer " + KEY}


def req(method, path, data=None):
    h = dict(AUTH)
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + path, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else None
    except urllib.error.HTTPError as e:
        print("HTTPError", method, path, e.code, e.read().decode()[:300], file=sys.stderr)
        raise


def parse_ingredients(lines, parser="openai"):
    for attempt in range(2):
        try:
            return req("POST", "/api/parser/ingredients",
                       {"parser": parser, "ingredients": lines})
        except urllib.error.HTTPError as e:
            if e.code == 500 and attempt == 0:
                time.sleep(2)
                continue
            raise


def upload_image(slug, path):
    ext = (os.path.splitext(path)[1].lstrip(".") or "jpg").lower()
    ctype = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        filedata = f.read()
    boundary = "----mealie" + uuid.uuid4().hex
    body = b"".join([
        ("--%s\r\nContent-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\n"
         "Content-Type: %s\r\n\r\n" % (boundary, os.path.basename(path), ctype)).encode()
        + filedata + b"\r\n",
        ("--%s\r\nContent-Disposition: form-data; name=\"extension\"\r\n\r\n%s\r\n"
         % (boundary, ext)).encode(),
        ("--%s--\r\n" % boundary).encode(),
    ])
    h = dict(AUTH)
    h["Content-Type"] = "multipart/form-data; boundary=" + boundary
    r = urllib.request.Request(BASE + "/api/recipes/%s/image" % slug,
                               data=body, headers=h, method="PUT")
    with urllib.request.urlopen(r, timeout=90) as resp:
        return json.loads(resp.read().decode())


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 mealie_import.py job.json")
    job = json.load(open(sys.argv[1]))
    parser = job.get("parser", "openai")

    slug = job.get("slug")
    if not slug:
        if not job.get("title"):
            sys.exit("job needs 'title' or 'slug'")
        slug = req("POST", "/api/recipes", {"name": job["title"]})
    print("slug:", slug)

    parsed = job.get("parsed_ingredients")
    if parsed is None and job.get("ingredient_lines"):
        parsed = parse_ingredients(job["ingredient_lines"], parser)
    parsed = parsed or []

    foods = req("GET", "/api/foods?perPage=2000")["items"]
    units = req("GET", "/api/units?perPage=2000")["items"]
    fmap = {f["name"].lower().strip(): f for f in foods}
    umap = {u["name"].lower().strip(): u for u in units}
    made_f, made_u = [], []

    recipe_ings = []
    for p in parsed:
        ing = p["ingredient"] if isinstance(p, dict) and "ingredient" in p else p
        food = ing.get("food")
        if food and food.get("name") and not food.get("id"):
            k = food["name"].lower().strip()
            if k in fmap:
                ing["food"] = fmap[k]
            else:
                nf = req("POST", "/api/foods", {"name": food["name"]})
                ing["food"] = nf; fmap[k] = nf; made_f.append(food["name"])
        unit = ing.get("unit")
        if unit and unit.get("name") and not unit.get("id"):
            k = unit["name"].lower().strip()
            if k in umap:
                ing["unit"] = umap[k]
            else:
                nu = req("POST", "/api/units", {"name": unit["name"]})
                ing["unit"] = nu; umap[k] = nu; made_u.append(unit["name"])
        qty = ing.get("quantity") or 0
        has_amount = bool(qty and qty > 0) or (ing.get("unit") is not None)
        recipe_ings.append({
            "quantity": ing.get("quantity"),
            "unit": ing.get("unit"),
            "food": ing.get("food"),
            "note": ing.get("note") or "",
            "isFood": ing.get("food") is not None,
            "disableAmount": not has_amount,
            "originalText": ing.get("originalText"),
            "referenceId": ing.get("referenceId") or str(uuid.uuid4()),
        })

    recipe = req("GET", "/api/recipes/%s" % slug)
    if recipe_ings:
        recipe["recipeIngredient"] = recipe_ings
    if job.get("instructions"):
        recipe["recipeInstructions"] = [
            {"title": "", "text": s, "ingredientReferences": []}
            for s in job["instructions"]
        ]
    if job.get("servings") is not None:
        recipe["recipeServings"] = job["servings"]
    if job.get("yield") is not None:
        recipe["recipeYield"] = job["yield"]
    if job.get("total_time") is not None:
        recipe["totalTime"] = job["total_time"]
    if job.get("prep_time") is not None:
        recipe["prepTime"] = job["prep_time"]
    req("PUT", "/api/recipes/%s" % slug, recipe)

    if job.get("image_path"):
        print("image:", upload_image(slug, job["image_path"]))

    v = req("GET", "/api/recipes/%s" % slug)
    print("created_foods:", made_f)
    print("created_units:", made_u)
    print("VERIFY name=%s servings=%s ings=%d steps=%d image=%s" % (
        v.get("name"), v.get("recipeServings"),
        len(v.get("recipeIngredient", [])),
        len(v.get("recipeInstructions", [])), v.get("image")))
    print("OK")


if __name__ == "__main__":
    main()
