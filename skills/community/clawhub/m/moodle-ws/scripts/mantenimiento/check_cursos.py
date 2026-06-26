import os, json, requests

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/secrets/moodle-ws.json")
config = json.load(open(CONFIG_PATH))

def call(fn, p={}):
    d = {"wstoken": config["token"], "wsfunction": fn, "moodlewsrestformat": "json", **p}
    return requests.post(config["baseUrl"] + "/webservice/rest/server.php", data=d).json()

excluir = ["info@campusinda.net", "profe-ia@campusinda.net"]
cursos = call("core_course_get_courses")
con = []
sin = []

for c in cursos:
    if c["id"] == 1: continue
    reales = [a for a in call("core_enrol_get_enrolled_users", {"courseid": c["id"]}) if a.get("email","") not in excluir]
    if reales:
        con.append(c)
        print(f"CON | {c['id']} | {c['fullname']} | {len(reales)} alumnos")
    else:
        sin.append(c["id"])

print(f"\nCon alumnos: {len(con)} | Vacios: {len(sin)}")
json.dump(con, open("/tmp/con_alumnos.json","w"), indent=2)
json.dump(sin, open("/tmp/vacios.json","w"))
print("Guardado en /tmp/")
