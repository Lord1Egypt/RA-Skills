#!/usr/bin/env python3
"""Cuello de botella unico de envio de Lazarillo.

Todo envio pasa por aqui. Falla CERRADO: ante cualquier duda, no manda.

  enviar.py --a "Nombre Completo" --u4 4318 --confirmacion "manda" --texto "hola"
  enviar.py --a "Nombre Completo" --u4 4318 --confirmacion "manda" --audio /ruta.ogg
"""
import argparse, hashlib, json, os, re, subprocess, sys, unicodedata
from datetime import datetime

BASE = os.environ.get("LAZARILLO_BASE", os.path.expanduser("~/.openclaw"))
WS = f"{BASE}/workspace"
LIBRETA = f"{WS}/memory/contactos.md"
MODO_F = f"{WS}/modo-envio.txt"
REG = f"{BASE}/registro/enviados.jsonl"
MEDIA_OK = f"{BASE}/media"          # unica raiz permitida para --audio
TIMEOUT_ENVIO = 90

# El portón acepta: [prefijo afirmativo] + NÚCLEO + [sufijo vacío].
# Las correcciones SIEMPRE vienen después del verbo ("manda pero cámbiale"),
# nunca antes, así que un prefijo afirmativo cerrado no abre riesgo y sí admite
# la forma en que la gente habla de verdad.
PREFIJOS = {"si", "va", "sale", "andale", "orale", "ya", "bueno", "ok", "va pues", "sale pues"}
NUCLEOS  = {"manda", "mandalo", "mandaselo", "manda le", "envia", "envialo", "enviaselo", "confirmo"}
SUFIJOS  = {"ya", "pues", "porfa", "por favor", "porfavor", "va", "sale", "de una vez"}


def confirma(dicho):
    """dicho ya viene normalizado. Debe ser prefijo? + nucleo + sufijo? y NADA mas."""
    t = dicho.split()
    if not t:
        return False
    # quitar prefijos (hasta 2, para "va pues manda")
    for _ in range(2):
        for n in (3, 2, 1):
            if len(t) > n and " ".join(t[:n]) in PREFIJOS:
                t = t[n:]
                break
        else:
            break
    # quitar sufijos (hasta 2)
    for _ in range(2):
        for n in (3, 2, 1):
            if len(t) > n and " ".join(t[-n:]) in SUFIJOS:
                t = t[:-n]
                break
        else:
            break
    return " ".join(t) in NUCLEOS
MODOS_VALIDOS = ("confirmado", "solo-lectura")

DIGITOS = {"0": "cero", "1": "uno", "2": "dos", "3": "tres", "4": "cuatro",
           "5": "cinco", "6": "seis", "7": "siete", "8": "ocho", "9": "nueve"}


def no(msg, code, tecnico=""):
    """Rechaza en DOS lineas: una para la persona y otra tecnica. La habilidad instruye
    al agente a leerle SOLO la linea que empieza con DECIR."""
    print(f"DECIR: {msg}", file=sys.stderr)
    print(f"TECNICO: rc={code} {tecnico or msg}", file=sys.stderr)
    sys.exit(code)


def deletrear(s):
    return " ".join(DIGITOS.get(c, c) for c in s)


def normaliza(s):
    """minusculas, sin acentos, sin puntuacion, espacios colapsados, TODAS las lineas unidas."""
    s = " ".join(s.split())                       # une lineas y colapsa espacios
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return " ".join(s.split())


# --- filtro de contenido: Unicode de verdad, con limites de palabra ---
PATRONES = [
    (r"\bcontrase(?:n|ñ)a\b", "una contraseña"),
    (r"\bpassword\b", "una contraseña"),
    (r"\bnip\b", "un NIP"),
    (r"\bn\.?\s?i\.?\s?p\.?\b", "un NIP"),
    (r"\bpin\b", "un NIP"),
    (r"\bclaves?\b", "una clave"),
    (r"\b(?:sk|pk)-[A-Za-z0-9_-]{16,}", "una llave de sistema"),
    (r"\bAIza[A-Za-z0-9_-]{20,}", "una llave de sistema"),
    (r"\bcvv\b", "un CVV"),
    (r"\bclabe\b", "una CLABE"),
    (r"\b(?:codigo|código)\s+(?:de\s+)?(?:verificacion|verificación|seguridad|acceso)\b", "un código"),
    # solo corridas SIN separadores, o con separadores de tarjeta, para no
    # bloquear codigo postal, dos telefonos juntos ni una lista de años
    (r"(?<!\d)\d{16,18}(?!\d)", "un número de tarjeta o CLABE"),
    (r"(?<!\d)[3-6]\d{3}[ .\-]\d{4}[ .\-]\d{4}[ .\-]\d{4}(?!\d)", "un número de tarjeta"),
    (r"\b(?:codigo|código)\b(?!\s+postal)[^\d]{0,15}\d{4,8}\b", "un código"),
]


def revisa_contenido(texto):
    n = unicodedata.normalize("NFC", texto.lower())
    for pat, que in PATRONES:
        if re.search(pat, n, flags=re.UNICODE):
            return que
    return None


def lee_modo():
    """Falla CERRADO: ausente, vacio, ilegible o desconocido -> no manda."""
    try:
        with open(MODO_F, encoding="utf-8") as f:
            crudo = f.read().strip().lower()
    except Exception as e:
        no("No mande nada. Se me rompio algo por dentro. Hablale a Javier y dile que Lazarillo no puede mandar mensajes.", 10, f"modo ilegible: {e.__class__.__name__}")
    if not crudo:
        no("No mande nada. Se me rompio algo por dentro. Hablale a Javier.", 10, "modo vacio")
    if crudo in MODOS_VALIDOS:
        return crudo, 0
    m = re.fullmatch(r"retenido:(\d+)", crudo)
    if m:
        seg = int(m.group(1))
        if not (5 <= seg <= 120):
            no("No mande nada. Se me rompio algo por dentro. Hablale a Javier.", 10, f"retenido:{seg} fuera de rango")
        return "retenido", seg
    no("No mande nada. Se me rompio algo por dentro. Hablale a Javier.", 10, f"modo desconocido: {crudo}")


def lee_libreta():
    try:
        lineas = open(LIBRETA, encoding="utf-8").read().splitlines()
    except Exception as e:
        no("No mande nada. No pude abrir tu libreta. Hablale a Javier.", 11, f"libreta ilegible: {e.__class__.__name__}")
    filas = []
    for ln in lineas:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        c = [x.strip() for x in s.strip("|").split("|")]
        if len(c) < 3:
            continue
        nombre = re.sub(r"[*_`]", "", c[0]).strip()
        if not nombre or nombre.lower().startswith("nombre") or set(nombre) <= set("-: "):
            continue
        tel_celda = c[2].strip()
        # la celda del telefono NO acepta prosa: si trae letras, esa fila no sirve
        if re.search(r"[^\d\s()+\-.]", tel_celda):
            filas.append({"nombre": nombre, "alias": c[1], "tel": None, "crudo": tel_celda})
            continue
        tel = re.sub(r"[^\d+]", "", tel_celda)
        # C1: NUNCA fabricar el "+". Un numero sin lada (6621234567) se convertia
        # en +66... = Tailandia, y --u4 no lo detecta porque los ultimos 4 coinciden.
        ok = bool(re.fullmatch(r"\+\d{11,15}", tel)) and not tel.startswith("+0")
        filas.append({"nombre": nombre, "alias": c[1], "crudo": tel_celda,
                      "tel": tel if ok else None})
    return filas


def resuelve(filas, buscado):
    b = normaliza(buscado)
    if not b:
        no("Se me fue a quien era. Me lo repites?", 12, "destinatario vacio")
    por_nombre = [f for f in filas if normaliza(f["nombre"]) == b]
    por_alias = [f for f in filas
                 if any(normaliza(a) == b for a in f["alias"].split(",") if a.strip())]
    # si coincide como nombre de una fila y como alias de otra, es ambiguo: no se adivina
    candidatos = {id(f): f for f in por_nombre + por_alias}.values()
    candidatos = list(candidatos)
    if not candidatos:
        conocidos = ", ".join(f["nombre"] for f in filas) or "la libreta esta vacia"
        no(f"No tengo a {buscado} en tu libreta. Dime su numero con lada y te lo repito digito por digito.", 13, f"sin coincidencia; libreta: {conocidos}")
    if len(candidatos) > 1:
        nombres = ", ".join(f["nombre"] for f in candidatos)
        no(f"Tengo mas de uno con ese nombre: {nombres}. Cual de ellos?", 14, "ambiguo")
    f = candidatos[0]
    if not f["tel"]:
        no(f"El numero de {f['nombre']} esta incompleto en tu libreta. Dictamelo con lada y lo dejo bien.", 15, f"celda invalida: {f['crudo']}")
    return f


def registra(evento):
    os.makedirs(os.path.dirname(REG), exist_ok=True)
    try:
        import fcntl
        with open(REG, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            fh.write(json.dumps(evento, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
            fcntl.flock(fh, fcntl.LOCK_UN)
    except Exception as e:
        # el registro es la unica auditoria que ella puede consultar: si no se escribe, no se manda
        no("No mande nada. Se me rompio algo por dentro. Hablale a Javier.", 16, f"registro no escribible: {e.__class__.__name__}")


def main():
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("--a", required=True, help="nombre del destinatario, como esta en la libreta")
    p.add_argument("--u4", required=True, help="los 4 digitos que se le dijeron a la persona")
    p.add_argument("--confirmacion", required=True, help="transcripcion literal de lo que ella contesto")
    p.add_argument("--texto")
    p.add_argument("--audio")
    p.add_argument("--dry-run", action="store_true")
    try:
        a = p.parse_args()
    except SystemExit:
        raise
    if not a.texto and not a.audio:
        no("Se me fue que querias mandar. Me lo repites?", 2, "sin texto ni audio")
    if a.texto and a.audio:
        no("No mande nada. Fue un error mio. Dime otra vez que quieres mandar.", 2, "texto y audio a la vez")

    modo, segundos = lee_modo()
    if modo == "solo-lectura":
        no("Ahorita no puedo mandar mensajes, Javier me tiene en pausa. Hablale a el.", 3, "modo solo-lectura")

    # --- porton de confirmacion, en codigo, enunciado completo ---
    if "\u00bf" in a.confirmacion:
        no("Eso sono a pregunta. Si quieres que salga, di: manda.", 25, "interrogacion")
    dicho = normaliza(a.confirmacion)
    if not confirma(dicho):
        no("Todavia no sale. Di nada mas: manda.", 20, f"no confirma: {a.confirmacion.strip()!r}")

    # --- resolver y amarrar los 4 digitos ---
    filas = lee_libreta()
    f = resuelve(filas, a.a)
    u4_pedido = re.sub(r"\D", "", a.u4)
    if len(u4_pedido) != 4:
        no("No mande nada. Fue un error mio al pasar los digitos, no tuyo. Dime otra vez a quien y lo repito.", 21, f"u4 mal formado: {a.u4!r}")
    if f["tel"][-4:] != u4_pedido:
        no("No mande nada. Te dije una terminacion y en la libreta hay otra. Fue mi error. Te lo repito desde el principio.", 22, f"u4 {u4_pedido} != {f['tel'][-4:]}")

    # --- contenido: SOLO corre para texto. Para audio no hay transcripcion aqui,
    #     asi que el filtro NO lo revisa. Es una limitacion conocida, no un olvido. ---
    if a.texto:
        mal = revisa_contenido(a.texto)
        if mal:
            no(f"Ese mensaje trae {mal}. Eso no te lo mando por mensaje. Diselo por telefono.", 5, "filtro de contenido")
        cuerpo_hash = hashlib.sha256(a.texto.encode()).hexdigest()[:16]
        largo = len(a.texto)
    else:
        ruta = os.path.realpath(a.audio)
        if not ruta.startswith(os.path.realpath(MEDIA_OK) + os.sep):
            no("No mande nada. Se me rompio algo por dentro. Hablale a Javier.", 23, f"ruta fuera de media: {a.audio}")
        if not os.path.isfile(ruta):
            no("No halle tu nota de voz. Vuelvemela a mandar y la reenvio.", 24, "audio inexistente")
        a.audio = ruta
        cuerpo_hash = hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:16]
        largo = os.path.getsize(ruta)

    ahora = datetime.now().astimezone().isoformat()
    registra({"t": ahora, "fase": "intento", "a": f["nombre"], "tel4": f["tel"][-4:],
              "modo": modo, "tipo": "audio" if a.audio else "texto",
              "hash": cuerpo_hash, "largo": largo, "dry_run": bool(a.dry_run)})

    if modo == "retenido" and segundos:
        # C5: releer el modo al despertar. No es una cancelacion por voz --eso
        # sigue sin existir-- pero al menos respeta un cambio a solo-lectura.
        import time
        time.sleep(segundos)
        modo2, _ = lee_modo()
        if modo2 == "solo-lectura":
            registra({"t": datetime.now().astimezone().isoformat(), "fase": "cancelado",
                      "a": f["nombre"], "tel4": f["tel"][-4:], "motivo": "solo-lectura durante la retencion"})
            no("No salio nada. Javier me puso en pausa mientras esperaba.", 26, "solo-lectura durante retencion")

    cmd = ["openclaw", "message", "send", "--channel", "whatsapp", "--target", f["tel"]]
    cmd += ["--media", a.audio] if a.audio else ["-m", a.texto]
    if a.dry_run:
        cmd.append("--dry-run")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_ENVIO)
        rc, salida = r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        rc, salida = 124, f"se colgo mas de {TIMEOUT_ENVIO} segundos"
    except OSError as e:
        rc, salida = 125, f"no pude ejecutar el envio: {e.__class__.__name__}"

    # C3: aqui el mensaje YA pudo haberse entregado. Si el registro falla ahora,
    # NO se puede decir "no se mando": seria pedirle que lo repita.
    try:
        registra({"t": datetime.now().astimezone().isoformat(), "fase": "resultado",
                  "a": f["nombre"], "tel4": f["tel"][-4:], "rc": rc, "salida": salida[:800],
                  "dry_run": bool(a.dry_run)})
    except SystemExit:
        print(f"OJO: ya se lo mande a {f['nombre']} pero no pude anotarlo. "
              f"Diselo a Javier. No lo vuelvas a mandar.", file=sys.stderr)
        sys.exit(7)

    if rc == 124:
        # C4: se colgo DESPUES de entregar, quiza. No se puede afirmar que no salio.
        print(f"NO SE SI SALIO. Se tardo demasiado con {f['nombre']}. "
              f"NO lo vuelvas a mandar: preguntale a Javier si llego.", file=sys.stderr)
        sys.exit(8)
    if rc != 0:
        print(f"NO SALIO. Fallo el envio a {f['nombre']}. {salida[:300]}", file=sys.stderr)
        sys.exit(6)
    marca = " (simulacro)" if a.dry_run else ""
    print(f"SALIO{marca}. Para {f['nombre']}, terminacion {deletrear(f['tel'][-4:])}, "
          f"{datetime.now().strftime('%H:%M')}.")


if __name__ == "__main__":
    main()
