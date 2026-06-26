import os, json, requests, time

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/secrets/moodle-ws.json")
config = json.load(open(CONFIG_PATH))

def call(fn, p={}):
    d = {"wstoken": config["token"], "wsfunction": fn, "moodlewsrestformat": "json", **p}
    return requests.post(config["baseUrl"] + "/webservice/rest/server.php", data=d).json()

# Borra categorías vacías de años anteriores al actual
años_viejos = {"2017","2018","2019","2020","2021","2022","2023","2024","2025"}
cats = call("core_course_get_categories")
a_borrar = [c for c in cats if isinstance(c, dict) and c.get("coursecount",0) == 0 and c.get("name","") in años_viejos]

print(f"Categorias a borrar: {len(a_borrar)}")
ok = 0
for c in a_borrar:
    r = call("core_course_delete_categories", {
        "categories[0][id]": c["id"],
        "categories[0][newparent]": 0,
        "categories[0][recursive]": 1
    })
    if isinstance(r, dict) and "exception" in r:
        print(f"Error {c['id']}: {r.get('message','')}")
    else:
        ok += 1
        print(f"Borrada: {c['name']} (ID {c['id']})")
    time.sleep(0.2)

print(f"\nTotal borradas: {ok}")
