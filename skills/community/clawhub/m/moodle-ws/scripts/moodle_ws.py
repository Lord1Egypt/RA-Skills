import requests
import json
import os
import sys
import time
import datetime
import calendar

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/secrets/moodle-ws.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("No se encontro el archivo de configuracion.")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)

def moodle_call(config, wsfunction, params={}):
    url = config["baseUrl"] + "/webservice/rest/server.php"
    data = {"wstoken": config["token"], "wsfunction": wsfunction, "moodlewsrestformat": "json"}
    data.update(params)
    r = requests.post(url, data=data)
    result = r.json()
    if isinstance(result, dict) and "exception" in result:
        print("Error Moodle: " + result.get("message", ""))
        sys.exit(1)
    return result

def listar_cursos(config):
    return moodle_call(config, "core_course_get_courses")

def listar_alumnos(config, course_id):
    return moodle_call(config, "core_enrol_get_enrolled_users", {"courseid": course_id})

def buscar_usuario(config, email):
    return moodle_call(config, "core_user_get_users_by_field", {"field": "email", "values[0]": email})

def enviar_mensaje(config, user_id, texto):
    return moodle_call(config, "core_message_send_instant_messages", {
        "messages[0][touserid]": user_id,
        "messages[0][text]": texto,
        "messages[0][textformat]": 0
    })

def mensaje_a_todos(config, course_id, texto):
    excluir = ["info@campusinda.net", "profe-ia@campusinda.net"]
    alumnos = listar_alumnos(config, course_id)
    reales = [a for a in alumnos if a.get("email","") not in excluir]
    print("Alumnos encontrados: " + str(len(reales)))
    for alumno in reales:
        uid = alumno["id"]
        nombre = alumno.get("fullname","").split()[0] if alumno.get("fullname") else "estudiante"
        msg = texto.replace("{nombre}", nombre)
        enviar_mensaje(config, uid, msg)
        print("Mensaje enviado a " + alumno.get("fullname", str(uid)))

def seguimiento_todos(config, texto):
    excluir = ["info@campusinda.net", "profe-ia@campusinda.net"]
    cursos = listar_cursos(config)
    print("Total cursos: " + str(len(cursos)))
    enviados = 0
    for curso in cursos:
        if curso["id"] == 1:
            continue
        alumnos = listar_alumnos(config, curso["id"])
        reales = [a for a in alumnos if a.get("email","") not in excluir]
        if not reales:
            continue
        print("Curso: " + curso["fullname"] + " | " + str(len(reales)) + " alumnos")
        for alumno in reales:
            uid = alumno["id"]
            nombre = alumno.get("fullname","").split()[0] if alumno.get("fullname") else "estudiante"
            msg = texto.replace("{nombre}", nombre).replace("{curso}", curso["fullname"])
            enviar_mensaje(config, uid, msg)
            print("  -> Enviado a " + alumno.get("fullname", str(uid)))
            enviados += 1
    print("Total mensajes enviados: " + str(enviados))

def crear_curso_completo(config, nombre, categoria_id=1, meses=6):
    shortname = nombre.lower().replace(" ", "-") + "-" + str(int(time.time()))[-4:]
    hoy = datetime.date.today()
    inicio = datetime.date(hoy.year, hoy.month, 1)
    inicio_ts = int(time.mktime(inicio.timetuple()))
    cursos = moodle_call(config, "core_course_create_courses", {
        "courses[0][fullname]": nombre,
        "courses[0][shortname]": shortname,
        "courses[0][categoryid]": categoria_id,
        "courses[0][visible]": 1,
        "courses[0][format]": "topics",
        "courses[0][numsections]": meses,
        "courses[0][startdate]": inicio_ts
    })
    if not cursos:
        print("Error al crear el curso")
        return
    curso_id = cursos[0]["id"]
    print("Curso creado: " + nombre + " (ID: " + str(curso_id) + ")")
    print("Shortname: " + shortname)
    print("Formato: temas mensuales (" + str(meses) + " meses)")
    print("Inicio: " + str(inicio))
    print("Curso listo para inscribir alumnos!")
    return curso_id

def duplicar_curso(config, nombre, curso_id, categoria_id=1089):
    shortname = nombre.lower().replace(" ", "-").replace("_", "-") + "-" + str(int(time.time()))[-4:]
    r = moodle_call(config, "core_course_duplicate_course", {
        "courseid": curso_id,
        "fullname": nombre,
        "shortname": shortname,
        "categoryid": categoria_id,
        "visible": 1
    })
    if "id" in r:
        print("Curso duplicado: " + nombre)
        print("ID nuevo: " + str(r["id"]))
        print("Shortname: " + r["shortname"])
        print("Ver en: " + config["baseUrl"] + "/course/view.php?id=" + str(r["id"]))
        return r["id"]
    else:
        print("Error: " + str(r))

if __name__ == "__main__":
    config = load_config()
    if len(sys.argv) < 2:
        print("Uso:")
        print("  listar_cursos")
        print("  listar_alumnos <course_id>")
        print("  mensaje_todos <course_id> <texto>")
        print("  seguimiento_todos <texto>")
        print("  buscar_usuario <email>")
        print("  crear_curso <nombre> [categoria_id] [meses]")
        print("  duplicar_curso <nombre> <curso_plantilla_id> [categoria_id]")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "listar_cursos":
        for c in listar_cursos(config):
            print("ID: " + str(c["id"]) + " | " + c["fullname"])
    elif cmd == "listar_alumnos":
        for a in listar_alumnos(config, sys.argv[2]):
            print("ID: " + str(a["id"]) + " | " + a["fullname"] + " | " + a.get("email",""))
    elif cmd == "mensaje_todos":
        mensaje_a_todos(config, sys.argv[2], sys.argv[3])
    elif cmd == "seguimiento_todos":
        seguimiento_todos(config, sys.argv[2])
    elif cmd == "buscar_usuario":
        for u in buscar_usuario(config, sys.argv[2]):
            print("ID: " + str(u["id"]) + " | " + u["fullname"])
    elif cmd == "crear_curso":
        cat_id = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        meses = int(sys.argv[4]) if len(sys.argv) > 4 else 6
        crear_curso_completo(config, sys.argv[2], cat_id, meses)
    elif cmd == "duplicar_curso":
        cat_id = int(sys.argv[4]) if len(sys.argv) > 4 else 1089
        duplicar_curso(config, sys.argv[2], int(sys.argv[3]), cat_id)
