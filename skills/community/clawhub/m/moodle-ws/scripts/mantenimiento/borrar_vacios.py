import os, json, requests, time

# Requiere haber corrido check_cursos.py antes
# Lee /tmp/vacios.json y borra esos cursos en Moodle

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/secrets/moodle-ws.json")
config = json.load(open(CONFIG_PATH))

def call(fn, p={}):
    d = {"wstoken": config["token"], "wsfunction": fn, "moodlewsrestformat": "json", **p}
    return requests.post(config["baseUrl"] + "/webservice/rest/server.php", data=d).json()

ids = json.load(open("/tmp/vacios.json"))
print(f"Cursos a borrar: {len(ids)}")

ok = 0
errores = 0
for cid in ids:
    r = call("core_course_delete_courses", {"courseids[0]": cid})
    if isinstance(r, dict) and "exception" in r:
        print(f"Error ID {cid}: {r.get('message','')}")
        errores += 1
    else:
        ok += 1
        print(f"Borrado ID {cid}")
    time.sleep(0.2)

print(f"\nBorrados: {ok} | Errores: {errores}")
