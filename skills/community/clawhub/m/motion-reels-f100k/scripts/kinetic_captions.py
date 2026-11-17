#!/usr/bin/env python3
"""kinetic_captions.py — genera el bloque HTML/GSAP de una FRASE cuyas palabras
aparecen una a una sincronizadas a la voz (kinetic typography).

A diferencia del viejo "kinetic word" (UNA palabra suelta), aquí toda una frase
del transcript se revela palabra por palabra en el timestamp en que se dice, con
la tipografía grande del pack F100K. Es la capa que "lleva el ritmo" sin amontonar
memes/cards.

Importable:
    from kinetic_captions import build_kinetic
    html, anims = build_kinetic(words, cid="kin0", top=820, align="center")
  donde words = [{"text":"hola","start":1.20,"end":1.45}, ...]
  (start/end en segundos, ya alineados al video; típicamente un tramo de captions.json)

Devuelve:
  html  → un <div> absoluto con un <span> por palabra (opacity 0 al inicio)
  anims → string con las líneas GSAP que revelan cada palabra en su 'start'

CLI (test):  kinetic_captions.py            → escribe /tmp/kin_test/index.html
"""
import os, sys, json, html as _html

# Familia canónica del pack (cargada por fonts.css). Cambiar la fuente = editar fonts.css.
DISPLAY = "'F100K Display','Inter',sans-serif"

def _esc(s): return _html.escape(str(s))

def build_kinetic(words, cid="kin", top=820, align="center",
                  font_size=78, color="#ffffff", accent="#f5c451",
                  accent_idx=None, tail=0.45):
    """Construye (html, gsap) para una frase con revelado por palabra.

    - top: y en px (0..1920). Para reels 9:16, zona segura superior ~200, inferior ~1380.
    - accent_idx: índice de palabra a pintar con 'accent' (énfasis). None = ninguna.
    - tail: segundos extra que la frase permanece tras la última palabra.
    """
    if not words:
        return "", ""
    t0 = float(words[0]["start"])
    t_last_end = float(words[-1]["end"])
    total_dur = (t_last_end + tail) - t0

    spans, anims = [], []
    for i, w in enumerate(words):
        wid = f"{cid}_w{i}"
        col = accent if (accent_idx is not None and i == accent_idx) else color
        spans.append(
            f'<span id="{wid}" style="display:inline-block;opacity:0;'
            f'margin:0 0.18em 0.12em 0;color:{col};'
            f'will-change:transform,opacity,filter;">{_esc(w["text"])}</span>')
        st = max(float(w["start"]), t0)  # nunca antes de que el bloque aparezca
        # Entrada: opacity 0→1, sube 22px y se desenfoca→nítido (blur-in tipo "pop").
        anims.append(
            f'  tl.fromTo("#{wid}",'
            f'{{opacity:0,y:22,filter:"blur(8px)",scale:0.92}},'
            f'{{opacity:1,y:0,filter:"blur(0px)",scale:1,duration:0.32,'
            f'ease:"back.out(1.7)"}},{round(st,3)});')

    just = {"center": "center", "left": "flex-start", "right": "flex-end"}.get(align, "center")
    block = (
        f'\n  <div id="{cid}" data-start="{round(t0,3)}" data-duration="{round(total_dur,3)}" '
        f'data-track-index="200"\n'
        f'       style="position:absolute;top:{top}px;left:60px;right:60px;opacity:0;\n'
        f'              display:flex;flex-wrap:wrap;justify-content:{just};align-items:flex-start;\n'
        f'              font:900 {font_size}px/1.06 {DISPLAY};letter-spacing:-1px;\n'
        f'              text-shadow:0 6px 30px rgba(0,0,0,0.55);">\n'
        f'    {"".join(spans)}\n'
        f'  </div>')
    # El contenedor entra (opacity 1) un pelo antes de la 1ª palabra y sale en fade.
    container = (
        f'  tl.to("#{cid}",{{opacity:1,duration:0.12}},{round(max(t0-0.08,0),3)});\n'
        f'  tl.to("#{cid}",{{opacity:0,duration:0.3,ease:"power2.in"}},'
        f'{round(t0+total_dur-0.3,3)});')
    return block, container + "\n" + "\n".join(anims)


def _test():
    out = "/tmp/kin_test"; os.makedirs(out, exist_ok=True)
    # Copiar fonts.css del pack para que el test sea fiel.
    pack = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
    words = [
        {"text": "ESTO", "start": 0.3, "end": 0.55},
        {"text": "lo", "start": 0.6, "end": 0.72},
        {"text": "cambia", "start": 0.8, "end": 1.15},
        {"text": "TODO", "start": 1.25, "end": 1.7},
    ]
    html_block, anims = build_kinetic(words, cid="kin0", top=760, accent_idx=3)
    doc = f'''<!DOCTYPE html><html><head><meta charset="UTF-8">
<link rel="stylesheet" href="{pack}/fonts.css">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;overflow:hidden;}}</style></head><body>
<div id="stage" data-composition-id="kin" data-start="0" data-width="1080" data-height="1920">
{html_block}
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
const tl = gsap.timeline({{paused:true}});
{anims}
window.__timelines = window.__timelines || {{}};
window.__timelines["kin"] = tl;
</script></div></body></html>'''
    open(os.path.join(out, "index.html"), "w").write(doc)
    print(f"✅ test en {out}/index.html")

if __name__ == "__main__":
    _test()
