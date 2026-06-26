#!/usr/bin/env python3
"""
KDP PDF Compiler — kompiliert Typst zu KDP-fertigem PDF via TypeTex API.
Verwendung: python compile.py <main.typ> [output.pdf] [template.typ]
Beispiel:   python compile.py build/main.typ output/buch.pdf kdp-book.typ
"""
import requests, base64, json, os, sys, time, re, io

LINKS_JSON = os.path.expanduser(
    "~/Desktop/openclaw-projekt/agentic-authorship-dashboard/shared/links.json"
)

def _load_qr_urls():
    if not os.path.exists(LINKS_JSON):
        return {}, {}
    data = json.load(open(LINKS_JSON, encoding="utf-8"))
    base = data.get("eigene_projekte", {}).get("DASHBOARD_URL", "https://openclaw-buch.de")
    targets, print_urls = {}, {}
    for qr_id, entry in data.get("qr_codes", {}).items():
        if qr_id.startswith("_"):
            continue
        if isinstance(entry, dict) and "target" in entry:
            targets[qr_id] = entry["target"].replace("{{DASHBOARD_URL}}", base)
            if "print_url" in entry:
                print_urls[qr_id] = entry["print_url"]
    targets.setdefault("DISCORD-SETUP", f"{base}/?module=config-builder&preset=discord")
    targets.setdefault("HUMANIZER-INSTALL", "https://clawhub.ai/Tikitackr/humanizer-de")
    return targets, print_urls

QR_URLS, PRINT_URLS = _load_qr_urls()

def generate_qr_svg(url):
    import qrcode
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    n = len(matrix)
    cell = 10
    size = n * cell
    rects = []
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val:
                x, y = c * cell, r * cell
                rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'width="{size}" height="{size}">'
        f'<rect width="{size}" height="{size}" fill="white"/>'
        f'<g fill="black">{"".join(rects)}</g>'
        f'</svg>'
    )

def inject_qr_codes(main_content, aux):
    # Ersetzt vollständige qr-block-Aufrufe: Bild UND Anzeige-URL (mit oder ohne hint:)
    def replace_qr_block(m):
        qr_id = m.group(1)
        width = m.group(2)
        label = m.group(3)
        hint_part = m.group(4)  # '' oder ', hint: "..."'
        url = QR_URLS.get(qr_id, "https://openclaw-buch.de/")
        print_url = PRINT_URLS.get(qr_id, url.replace("https://", "").replace("http://", ""))
        print(f"[KDP] QR generieren: {qr_id} → {print_url}")
        svg = generate_qr_svg(url).replace("\\", "\\\\").replace('"', '\\"')
        return f'#qr-block(image.decode("{svg}", format: "svg", width: {width}), "{label}", "{print_url}"{hint_part})'
    main_content = re.sub(
        r'#qr-block\(\s*image\("qr-([A-Z0-9-]+)\.svg",\s*width:\s*([^)]+)\)\s*,\s*"([^"]*)"\s*,\s*"[^"]*"((?:,\s*hint:\s*"[^"]*")?)\s*\)',
        replace_qr_block,
        main_content
    )
    # Fallback: standalone image-Referenzen außerhalb von qr-block
    def replace_qr_image(m):
        qr_id = m.group(1)
        width = m.group(2)
        url = QR_URLS.get(qr_id, "https://openclaw-buch.de/")
        print(f"[KDP] QR generieren (standalone): {qr_id} → {url}")
        svg = generate_qr_svg(url).replace("\\", "\\\\").replace('"', '\\"')
        return f'image.decode("{svg}", format: "svg", width: {width})'
    main_content = re.sub(
        r'image\("qr-([A-Z0-9-]+)\.svg",\s*width:\s*([^)]+)\)',
        replace_qr_image,
        main_content
    )
    return main_content, aux

API_URL = os.environ.get(
    "TYPETEX_API_URL",
    "https://studio-intrinsic--typetex-compile-app.modal.run"
)

def health_check():
    try:
        r = requests.get(f"{API_URL}/public/compile/health", timeout=10)
        return r.json().get("status") == "ok"
    except Exception:
        return False

def compile_typst_to_pdf(main_content, auxiliary_files=None, output_path="output.pdf"):
    payload = {
        "content": main_content,
        "main_filename": "main.typ",
        "auxiliary_files": auxiliary_files or {}
    }
    print(f"[KDP] Sende an TypeTex API...")
    start = time.time()
    try:
        r = requests.post(f"{API_URL}/public/compile/typst", json=payload, timeout=120)
        elapsed = round(time.time() - start, 1)
        if r.status_code != 200:
            return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:300]}"}
        result = r.json()
        if result.get("success"):
            pdf = base64.b64decode(result["pdf_base64"])
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            open(output_path, "wb").write(pdf)
            size_kb = len(pdf) // 1024
            print(f"[KDP] ✓ PDF: {output_path} ({size_kb} KB, {elapsed}s)")
            return {"success": True, "pdf_path": os.path.abspath(output_path), "size_kb": size_kb}
        else:
            print(f"[KDP] ✗ Fehler: {result.get('error')}")
            print(result.get("log_output", "")[:800])
            return {"success": False, "error": result.get("error"), "log": result.get("log_output","")}
    except requests.Timeout:
        return {"success": False, "error": "Timeout — Buch zu groß. Kapitel einzeln kompilieren."}
    except requests.ConnectionError:
        return {"success": False, "error": f"API nicht erreichbar: {API_URL}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main_file     = sys.argv[1]
    output_file   = sys.argv[2] if len(sys.argv) > 2 else main_file.replace(".typ", ".pdf")
    template_file = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(main_file):
        print(f"[KDP] Fehler: {main_file} nicht gefunden"); sys.exit(1)

    main_content = open(main_file, encoding="utf-8").read()
    aux = {}
    main_dir = os.path.dirname(os.path.abspath(main_file))

    # Alle #include "datei.typ" aus main automatisch hochladen
    for inc in re.findall(r'#include\s+"([^"]+)"', main_content):
        inc_path = os.path.join(main_dir, inc)
        if os.path.exists(inc_path):
            aux[inc] = open(inc_path, encoding="utf-8").read()
            print(f"[KDP] Include: {inc}")
        else:
            print(f"[KDP] Warnung: #include \"{inc}\" nicht gefunden ({inc_path})")

    candidates = [
        template_file,
        os.path.join(os.path.dirname(os.path.abspath(main_file)), "kdp-book.typ.txt"),
        os.path.join(os.path.dirname(os.path.abspath(main_file)), "kdp-book.typ"),
        os.path.join(os.getcwd(), "kdp-book.typ.txt"),
        os.path.join(os.getcwd(), "kdp-book.typ"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            aux["kdp-book.typ"] = open(candidate, encoding="utf-8").read()
            break
    else:
        print("[KDP] Warnung: kdp-book.typ nicht gefunden — bitte als 3. Argument übergeben.")

    main_content, aux = inject_qr_codes(main_content, aux)
    # QR-Injektion auch in aux-Dateien (z.B. #include-Kapitel)
    for fname in list(aux.keys()):
        if fname.endswith(".typ") and fname != "kdp-book.typ":
            aux[fname], _ = inject_qr_codes(aux[fname], {})

    if not health_check():
        print(f"[KDP] API nicht erreichbar — versuche lokales Typst...")
        import subprocess
        try:
            r = subprocess.run(["typst","compile",main_file,output_file],
                               capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                print(f"[KDP] ✓ Lokal: {output_file}")
            else:
                print(f"[KDP] ✗ {r.stderr}"); sys.exit(1)
        except FileNotFoundError:
            print("[KDP] Typst nicht installiert: https://github.com/typst/typst/releases")
            sys.exit(1)
        return

    result = compile_typst_to_pdf(main_content, aux, output_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["success"]: sys.exit(1)

if __name__ == "__main__":
    main()
