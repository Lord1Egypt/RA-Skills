#!/usr/bin/env python3
"""Multimedia Manager — Lite Web Gallery (Community Edition).
Full gallery with AI tagging, face recognition, maps, and more
available in the Pro edition.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

def _load_dotenv():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

_load_dotenv()

from flask import Flask, request, jsonify, send_file, abort, render_template_string, g, redirect as flask_redirect, make_response
from image_db import (get_db, init_db, search_images, get_all_categories, get_all_tags,
                      get_stats, get_image_by_id, toggle_favorite, delete_image,
                      list_albums, get_album_images, create_album,
                      add_to_album, remove_from_album, backup_db,
                      VAULT_DIR)

_SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_DATA_DIR = os.path.join(_SKILL_DIR, "data")

app = Flask(__name__)

AUTH_TOKEN = os.environ.get("IMAGE_VAULT_TOKEN", "")
AUTH_EXEMPT_PATHS = {"/api/health", "/api/status"}


def _get_conn():
    if "db" not in g:
        g.db = get_db()
        init_db()
    return g.db


@app.teardown_appcontext
def _close_conn(exc):
    db = g.pop("db", None)
    if db:
        db.close()


LOGIN_TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Media Vault</title>
<style>body{background:#1a1a2e;color:#fff;font-family:system-ui;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
.card{background:#16213e;padding:2em;border-radius:12px;text-align:center;width:320px}
input{width:90%;padding:10px;margin:10px 0;border:1px solid #444;border-radius:6px;background:#0f3460;color:#fff}
button{padding:10px 24px;background:#e94560;color:#fff;border:none;border-radius:6px;cursor:pointer}
.err{color:#e94560;margin:8px 0}</style></head><body>
<div class="card"><h1>Media Vault</h1>
{% if error %}<div class="err">{{ error }}</div>{% endif %}
<form method="POST"><input name="token" type="password" placeholder="Enter access token" autofocus /><button type="submit">Enter</button></form>
</div></body></html>"""


@app.before_request
def _check_auth():
    if request.path in AUTH_EXEMPT_PATHS:
        return
    if request.path == "/login":
        if request.method == "GET":
            return render_template_string(LOGIN_TEMPLATE, error=None)
        if request.method == "POST":
            t = request.form.get("token", "").strip()
            if t == AUTH_TOKEN:
                resp = make_response(flask_redirect("/"))
                resp.set_cookie("vault_token", t, max_age=86400*30, httponly=True, samesite="Lax")
                return resp
            return render_template_string(LOGIN_TEMPLATE, error="Invalid token")
    if not AUTH_TOKEN:
        return
    token = request.args.get("token") or request.cookies.get("vault_token")
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = token or auth_header[7:].strip()
    if token == AUTH_TOKEN:
        g._need_set_cookie = not request.cookies.get("vault_token")
        return
    return flask_redirect("/login")


@app.after_request
def _after(resp):
    if getattr(g, "_need_set_cookie", False):
        resp.set_cookie("vault_token", AUTH_TOKEN, max_age=86400*30, httponly=True, samesite="Lax")
    return resp


@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok", "edition": "community"})


@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats(_get_conn()))


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "")
    cat = request.args.get("category")
    limit = int(request.args.get("limit", 100))
    return jsonify(search_images(_get_conn(), q, category=cat, limit=limit))


@app.route("/api/categories")
def api_categories():
    return jsonify(get_all_categories(_get_conn()))


@app.route("/api/tags")
def api_tags():
    return jsonify(get_all_tags(_get_conn()))


@app.route("/api/images/<int:image_id>")
def api_image(image_id):
    img = get_image_by_id(_get_conn(), image_id)
    if not img:
        abort(404)
    return jsonify(img)


@app.route("/api/images/<int:image_id>/favorite", methods=["POST"])
def api_toggle_favorite(image_id):
    return jsonify({"favorited": toggle_favorite(_get_conn(), image_id)})


@app.route("/api/images/<int:image_id>", methods=["DELETE"])
def api_delete_image(image_id):
    delete_image(_get_conn(), image_id)
    return jsonify({"deleted": True})


@app.route("/api/albums")
def api_albums():
    return jsonify(list_albums(_get_conn()))


@app.route("/api/albums/<int:album_id>/images")
def api_album_images(album_id):
    return jsonify(get_album_images(_get_conn(), album_id))


@app.route("/api/file")
def api_file():
    path = request.args.get("path", "")
    if not path or not os.path.isfile(path):
        abort(404)
    allowed_bases = [os.path.abspath(VAULT_DIR), os.path.abspath(_DATA_DIR)]
    abs_path = os.path.abspath(path)
    if not any(abs_path.startswith(b) for b in allowed_bases):
        abort(403)
    return send_file(abs_path)


@app.route("/api/backup", methods=["POST"])
def api_backup():
    path = backup_db()
    return jsonify({"backup": path})


GALLERY_PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Media Vault</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#111;color:#eee;font-family:system-ui}
.header{background:#1a1a2e;padding:16px 24px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.header h1{font-size:1.2em;color:#e94560}
.header input{flex:1;min-width:200px;padding:8px 12px;border:1px solid #333;border-radius:6px;background:#0f3460;color:#fff}
.header button{padding:8px 16px;background:#e94560;color:#fff;border:none;border-radius:6px;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;padding:16px}
.item{position:relative;aspect-ratio:1;overflow:hidden;border-radius:8px;cursor:pointer;background:#222}
.item img{width:100%;height:100%;object-fit:cover;transition:transform .2s}
.item:hover img{transform:scale(1.05)}
.badge{position:absolute;top:6px;left:6px;background:rgba(0,0,0,.7);color:#fff;padding:2px 6px;border-radius:4px;font-size:11px}
.fav{position:absolute;top:6px;right:6px;font-size:18px;cursor:pointer}
.empty{text-align:center;padding:80px 20px;color:#666}
.pro-banner{background:linear-gradient(135deg,#e94560,#0f3460);padding:12px 24px;text-align:center;font-size:14px}
.pro-banner a{color:#fff;text-decoration:underline}
</style></head><body>
<div class="pro-banner">Community Edition — <a href="https://clawhub.com/skills/multimedia-manager-pro">Upgrade to Pro</a> for AI tagging, face recognition, maps & more | Contact: <a href="mailto:xujk2012@gmail.com">xujk2012@gmail.com</a></div>
<div class="header">
<h1>Media Vault</h1>
<input id="q" placeholder="Search..." />
<button onclick="doSearch()">Search</button>
</div>
<div class="grid" id="grid"></div>
<div class="empty" id="empty" style="display:none">No images found. Import some with the CLI!</div>
<script>
const tk=new URLSearchParams(location.search).get('token')||'';
function _a(u){return tk?(u+(u.includes('?')?'&':'?')+'token='+encodeURIComponent(tk)):u;}
function load(q){
  const url=q?'/api/search?limit=200&q='+encodeURIComponent(q):'/api/search?limit=200';
  fetch(_a(url)).then(r=>r.json()).then(imgs=>{
    const grid=document.getElementById('grid');
    const empty=document.getElementById('empty');
    grid.innerHTML='';
    if(!imgs||!imgs.length){empty.style.display='block';return;}
    empty.style.display='none';
    imgs.forEach(img=>{
      const div=document.createElement('div');
      div.className='item';
      const src=img.thumb_path||img.vault_path;
      div.innerHTML='<img src="'+_a('/api/file?path='+encodeURIComponent(src))+'" loading="lazy"/>'
        +(img.category?'<span class="badge">'+img.category+'</span>':'')
        +'<span class="fav" onclick="event.stopPropagation();toggleFav('+img.id+',this)">'+(img.favorited?'❤️':'🤍')+'</span>';
      div.onclick=()=>window.open(_a('/api/file?path='+encodeURIComponent(img.vault_path)),'_blank');
      grid.appendChild(div);
    });
  });
}
function doSearch(){load(document.getElementById('q').value.trim());}
function toggleFav(id,el){
  fetch(_a('/api/images/'+id+'/favorite'),{method:'POST'}).then(r=>r.json()).then(d=>{
    el.textContent=d.favorited?'❤️':'🤍';
  });
}
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter')doSearch();});
load('');
</script></body></html>"""


@app.route("/")
def index():
    return render_template_string(GALLERY_PAGE)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9876))
    print(f"Media Vault (Community Edition) running at http://localhost:{port}")
    host = os.environ.get("IMAGE_VAULT_HOST", "127.0.0.1")
    app.run(host=host, port=port, debug=False)
