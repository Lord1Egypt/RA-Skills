#!/usr/bin/env python3
"""
Generate one image per post (optional step). No SSH, no server upload.

Images are saved locally under --outdir. If you have public hosting, pass
--image-base-url https://yourdomain.com/social and the CSV imageUrls column
will be filled with https://yourdomain.com/social/post-001.png style URLs.
Without it, the CSV keeps imageUrls empty (HighLevel import still works,
posts just have no image attached).

Providers tried in order (whichever key you provide):
  --kling-ak/--kling-sk (or KLING_ACCESS_KEY/KLING_SECRET_KEY env)
  --gemini-key (or GEMINI_API_KEY env)
  --fal-key (or FAL_KEY env)
"""
import argparse
import base64
import csv
import hashlib
import hmac
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

from common import load_env

STYLE_SUFFIX = (
    "When you create this image, it should be similar to a stock photo, realistic, "
    "avoiding animated or cartoon styles. You should avoid any images that seem like "
    "a dream or any image effects. Avoid using people, words or letters. Any screens, "
    "laptops, phones, monitors or displays shown must be blank or show only abstract "
    "shapes, never text, letters, numbers, logos or interface labels. It should be "
    "free of any branding or any specific product."
)


def llm_chat(env, prompt: str, max_tokens: int = 500, llm_key: str = "", llm_model: str = "", llm_base: str = "") -> str:
    key = llm_key
    if not key:
        raise RuntimeError("no LLM key (pass --llm-key; the only env var here is HIGHLEVEL_ACCESS_TOKEN)")
    model = llm_model or "deepseek-chat"
    base = llm_base or "https://api.deepseek.com/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.8,
    }).encode()
    req = urllib.request.Request(base, data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read())
    return resp["choices"][0]["message"]["content"].strip()


def image_idea_prompt(biz_cat: str, post_content: str) -> str:
    return (
        f"You are an art director for a {biz_cat} company's social media feed. "
        f"Write ONE detailed image prompt for a realistic stock-photo style image that DIRECTLY "
        f"illustrates the topic of the post below. The scene must be a clear visual metaphor or "
        f"literal depiction of that topic, never a generic desk scene.\n\n"
        f"POST:\n{post_content}\n\n"
        f"RULES:\n"
        f"- The main subject must clearly represent the post's core topic.\n"
        f"- Do NOT use generic filler objects (coffee mugs, potted plants, succulents, blank notebooks, "
        f"plain desks) unless they directly support the topic.\n"
        f"- No people, no faces. No readable text, letters, numbers, logos, or brand names anywhere. "
        f"If a screen, laptop, phone, or monitor appears it must be blank or show only abstract shapes.\n"
        f"- Realistic, professional, well-lit, sharp focus, natural colors, good composition.\n"
        f"- Output only the prompt itself, 1-3 sentences, no preamble, no quotes."
    )


def gemini_generate(key: str, prompt: str, timeout: int = 300) -> str:
    model = "gemini-3.1-flash-image-preview"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST",
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"gemini submit failed: {e.code} {e.read().decode()[:300]}")
    for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            b64 = part["inlineData"].get("data", "")
            mime = part["inlineData"].get("mimeType", "image/png")
            ext = "png" if "png" in mime else "jpg"
            tmp = f"/tmp/gemini-img-{int(time.time()*1000)}.{ext}"
            open(tmp, "wb").write(base64.b64decode(b64))
            return tmp
    raise RuntimeError(f"no image in gemini response: {str(resp)[:200]}")


def download(url: str, dest: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(dest, "wb").write(r.read())


def kling_generate(ak: str, sk: str, prompt: str, aspect_ratio: str = "1:1", count: int = 1,
                   base: str = "https://api-singapore.klingai.com", timeout: int = 180) -> str:
    def _jwt():
        if not sk:
            return ak
        n = int(time.time())
        h = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
        p = base64.urlsafe_b64encode(json.dumps({"iss": ak, "exp": n + 120, "nbf": n - 5}).encode()).rstrip(b"=").decode()
        s = base64.urlsafe_b64encode(hmac.new(sk.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
        return f"{h}.{p}.{s}"

    def _post(path, body):
        req = urllib.request.Request(f"{base}{path}", data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {_jwt()}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"kling submit failed: {e.code} {e.read().decode()[:300]}")

    def _get(path):
        req = urllib.request.Request(f"{base}{path}",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {_jwt()}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"kling poll failed: {e.code} {e.read().decode()[:300]}")

    body = {"model": "kling-v3", "prompt": prompt, "n": count, "aspect_ratio": aspect_ratio}
    task_id = _post("/v1/images/generations", body).get("data", {}).get("task_id")
    if not task_id:
        raise RuntimeError("kling: no task_id in submit response")
    start = time.time()
    while time.time() - start < timeout:
        d = _get(f"/v1/images/generations/{task_id}").get("data", {})
        status = d.get("task_status", "")
        if status == "succeed":
            images = d.get("task_result", {}).get("images", [])
            if not images:
                raise RuntimeError(f"kling: no images in result: {str(d)[:200]}")
            img_url = images[0].get("url", "")
            if not img_url:
                raise RuntimeError(f"kling: no url in image result: {str(images[0])[:200]}")
            tmp = f"/tmp/kling-img-{int(time.time()*1000)}.png"
            download(img_url, tmp)
            return tmp
        if status in ("failed", "error"):
            raise RuntimeError(f"kling image failed: {d.get('task_status_msg', '?')}")
        time.sleep(5)
    raise TimeoutError(f"kling task {task_id} timed out after {timeout}s")


def fal_generate(key: str, prompt: str, timeout: int = 300) -> str:
    url = "https://queue.fal.run/fal-ai/flux/dev"
    body = json.dumps({
        "prompt": prompt,
        "image_size": "landscape_4_3",
        "num_images": 1,
        "output_format": "png",
        "enable_safety_checker": False,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST",
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"fal submit failed: {e.code} {e.read().decode()[:300]}")
    status_url = resp.get("status_url") or resp.get("response_url")
    if status_url and resp.get("status") != "COMPLETED":
        deadline = time.time() + timeout
        while time.time() < deadline:
            time.sleep(3)
            q = urllib.request.Request(status_url, headers={"Authorization": f"Key {key}"})
            try:
                with urllib.request.urlopen(q, timeout=30) as r:
                    st = json.loads(r.read())
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"fal poll failed: {e.code} {e.read().decode()[:200]}")
            if st.get("status") in ("COMPLETED", "succeeded"):
                resp = st
                break
            if st.get("status") in ("FAILED", "failed", "error"):
                raise RuntimeError(f"fal task failed: {str(st)[:200]}")
        else:
            raise TimeoutError(f"fal task timed out after {timeout}s")
    urls = resp.get("images", []) or resp.get("image_url", None)
    if isinstance(urls, list) and urls and isinstance(urls[0], dict):
        img_url = urls[0].get("url", "")
    elif isinstance(urls, list) and urls:
        img_url = urls[0]
    elif isinstance(urls, str):
        img_url = urls
    else:
        raise RuntimeError(f"no image in fal response: {str(resp)[:200]}")
    tmp = f"/tmp/fal-img-{int(time.time()*1000)}.png"
    download(img_url, tmp)
    return tmp


def ssh_upload(host: str, user: str, key: str, local: str, remote_path: str):
    """Upload one file to a remote host over SSH (scp). Returns None or raises."""
    import subprocess
    conn = ["-i", key, "-o", "ConnectTimeout=15", "-o", "StrictHostKeyChecking=accept-new"]
    dest = f"{user}@{host}:{remote_path}"
    r = subprocess.run(["scp"] + conn + [local, dest], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"scp failed: {r.stderr[-300:]}")


def ftp_upload(host: str, user: str, passwd: str, local: str, remote_path: str):
    """Upload one file over FTP. Creates remote dirs as needed. Returns or raises."""
    from ftplib import FTP, error_perm
    ftp = FTP(host, timeout=30)
    ftp.login(user, passwd)
    parts = remote_path.split("/")
    cur = ""
    for p in parts[:-1]:
        if not p:
            continue
        cur += "/" + p
        try:
            ftp.cwd(cur)
        except error_perm:
            ftp.mkd(cur)
            ftp.cwd(cur)
    with open(local, "rb") as f:
        ftp.storbinary(f"STOR {parts[-1]}", f)
    ftp.quit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts-json", required=True)
    ap.add_argument("--csv", default="", help="CSV to update with imageUrls")
    ap.add_argument("--client-json", default="", help="client JSON (for Business Category)")
    ap.add_argument("--biz-cat", default="", help="Business Category override")
    ap.add_argument("--limit", type=int, default=0, help="only first N posts (test)")
    ap.add_argument("--outdir", default="images")
    ap.add_argument("--image-base-url", default="", help="https://yourdomain.com/social to fill CSV imageUrls")
    ap.add_argument("--llm-key", default="")
    ap.add_argument("--llm-model", default="")
    ap.add_argument("--llm-base", default="", help="OpenAI-compatible endpoint (default DeepSeek; use https://api.openai.com/v1/chat/completions for ChatGPT/OpenAI keys)")
    ap.add_argument("--gemini-key", default="")
    ap.add_argument("--fal-key", default="")
    ap.add_argument("--kling-ak", default="")
    ap.add_argument("--kling-sk", default="")
    # Upload options: SSH or FTP (uploads images + fills CSV imageUrls with the public URL)
    ap.add_argument("--ssh-host", default="", help="SSH host for image upload, e.g. yourdomain.com or user@host")
    ap.add_argument("--ssh-user", default="", help="SSH username (default: current user)")
    ap.add_argument("--ssh-key", default="", help="Path to SSH private key")
    ap.add_argument("--ssh-remote-dir", default="public_html/social", help="Remote dir relative to SSH home (default public_html/social)")
    ap.add_argument("--ftp-host", default="")
    ap.add_argument("--ftp-user", default="")
    ap.add_argument("--ftp-pass", default="")
    ap.add_argument("--ftp-remote-dir", default="public_html/social", help="Remote dir for FTP (default public_html/social)")
    ap.add_argument("--public-url-base", default="", help="Public URL base for uploaded images, e.g. https://yourdomain.com/social (default: https://<ssh/ftp host>/<remote-dir>)")
    args = ap.parse_args()

    posts = json.load(open(args.posts_json))
    limited = bool(args.limit)
    if args.limit:
        posts = posts[:args.limit]

    biz_cat = args.biz_cat
    if not biz_cat and args.client_json:
        client = json.load(open(args.client_json))
        biz_cat = client.get("customFields", {}).get("Business Category", "")
    if not biz_cat:
        print("WARN: no Business Category provided; image ideas will be generic", file=sys.stderr)

    env = load_env()
    gemini_key = args.gemini_key
    fal_key = args.fal_key
    kling_ak = args.kling_ak
    kling_sk = args.kling_sk
    has_kling = bool(kling_ak and (kling_sk or kling_ak.startswith("api-key-")))
    if not gemini_key and not fal_key and not has_kling:
        print("ERROR: need --gemini-key, --fal-key, or --kling-ak(+--kling-sk). Images skipped.", file=sys.stderr)
        sys.exit(2)

    # Resolve upload transport once: SSH > FTP > none
    upload_fn = None
    upload_host = ""
    if args.ssh_host:
        ssh_host = args.ssh_host.replace("ssh://", "")
        if "@" in ssh_host:
            user, host = ssh_host.split("@", 1)
        else:
            user, host = (args.ssh_user or "root"), ssh_host
        key = args.ssh_key or os.path.expanduser("~/.ssh/id_rsa")
        upload_fn = lambda local, remote: ssh_upload(host, user, key, local, remote)
        upload_host = host
        print(f"    upload via SSH: {user}@{host}:{args.ssh_remote_dir}", file=sys.stderr)
    elif args.ftp_host:
        upload_fn = lambda local, remote: ftp_upload(args.ftp_host, args.ftp_user, args.ftp_pass, local, remote)
        upload_host = args.ftp_host
        print(f"    upload via FTP: {args.ftp_user}@{args.ftp_host}:{args.ftp_remote_dir}", file=sys.stderr)

    # Public URL base: explicit > host + remote dir
    if args.public_url_base:
        public_base = args.public_url_base.rstrip("/")
    elif upload_host:
        remote_for_url = (args.ssh_remote_dir if args.ssh_host else args.ftp_remote_dir).lstrip("/")
        # strip a leading public_html/ from the URL path
        url_path = remote_for_url.replace("public_html/", "", 1) if remote_for_url.startswith("public_html/") else remote_for_url
        public_base = f"https://{upload_host}/{url_path}"
    else:
        public_base = ""

    os.makedirs(args.outdir, exist_ok=True)
    results = []
    for i, p in enumerate(posts):
        fname = f"post-{i+1:03d}.png"
        local = os.path.join(args.outdir, fname)
        try:
            idea = llm_chat(env, image_idea_prompt(biz_cat, p["content"]), llm_key=args.llm_key, llm_model=args.llm_model, llm_base=args.llm_base)
            idea = re.sub(r"^[\"'`\s]+|[\"'`\s]+$", "", idea)
            full_prompt = f"{idea} {STYLE_SUFFIX}"
            img = None
            errs = []
            if kling_ak and (kling_sk or kling_ak.startswith("api-key-")):
                try:
                    img = kling_generate(kling_ak, kling_sk, full_prompt)
                except Exception as e:
                    errs.append(f"kling: {e}")
            if img is None and gemini_key:
                try:
                    img = gemini_generate(gemini_key, full_prompt)
                except Exception as e:
                    errs.append(f"gemini: {e}")
            if img is None and fal_key:
                try:
                    img = fal_generate(fal_key, full_prompt)
                except Exception as e:
                    errs.append(f"fal: {e}")
            if img is None:
                raise RuntimeError("; ".join(errs) or "no image provider available")
            if img.startswith("http"):
                download(img, local)
            else:
                import shutil
                shutil.copy(img, local)
                os.remove(img)
            # Upload (SSH/FTP) if configured; fall back to --image-base-url or local only
            p["imageUrl"] = ""
            if upload_fn:
                remote_dir = args.ssh_remote_dir if args.ssh_host else args.ftp_remote_dir
                try:
                    upload_fn(local, f"{remote_dir}/{fname}")
                    p["imageUrl"] = f"{public_base}/{fname}"
                except Exception as e:
                    print(f"    upload failed for {fname}: {e}", file=sys.stderr)
            elif args.image_base_url:
                p["imageUrl"] = f"{args.image_base_url.rstrip('/')}/{fname}"
            p["imagePrompt"] = full_prompt
            results.append((i + 1, fname, local))
            print(f"[{i+1}/{len(posts)}] OK {local} -> {p['imageUrl'] or 'no public URL'}", flush=True)
        except Exception as e:
            p["imageUrl"] = ""
            print(f"[{i+1}/{len(posts)}] FAIL {fname}: {e}", flush=True)

    if not limited:
        json.dump(posts, open(args.posts_json, "w"), indent=2)
    print(f"images done: {len(results)}/{len(posts)} (saved in {args.outdir})")

    if args.csv and os.path.exists(args.csv):
        rows = list(csv.reader(open(args.csv)))
        if rows and rows[0][0].startswith("postAtSpecificTime"):
            for row, p in zip(rows[1:], posts):
                row[3] = p.get("imageUrl", "")
            with open(args.csv, "w", newline="") as f:
                csv.writer(f).writerows(rows)
            print(f"CSV updated: {args.csv}")


if __name__ == "__main__":
    main()
