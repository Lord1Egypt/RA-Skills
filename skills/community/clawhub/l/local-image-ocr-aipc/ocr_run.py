"""
Step 3: Run GLM-OCR inference on an image via llama-server.exe HTTP API.
Usage:  Set IMG_PATH below (or pass as first argument), then run: python ocr_run.py
"""
import sys, os, subprocess, time, json, base64, socket, threading

# Force UTF-8 output on Windows to avoid GBK encoding errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Resolve OCR_DIR from env or config file
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ocr_cfg import OCR_DIR

if not OCR_DIR:
    print("[ERROR] OCR_DIR not resolved. Run preflight_workdir.py first.", file=sys.stderr)
    sys.exit(1)

# Windows: prevent child process from opening a console window.
_CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def _find_free_port():
    """Find an available TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_server(port, timeout=120):
    """Wait until the server is ready to accept connections."""
    import urllib.request
    url = f"http://127.0.0.1:{port}/health"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = urllib.request.urlopen(url, timeout=2)
            data = json.loads(resp.read())
            if data.get("status") == "ok":
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def _stream_stderr(proc):
    """Print server stderr in real-time for diagnostics."""
    for line in iter(proc.stderr.readline, b""):
        print(line.decode("utf-8", errors="replace"), end="", file=sys.stderr)


# ── Configuration ─────────────────────────────────────────────────────────────
# Set IMG_PATH to the image file to recognize, or pass it as a command-line argument.
IMG_PATH  = r""   # e.g. r"C:\Users\you\Pictures\invoice.png"
MODEL_DIR = os.path.join(OCR_DIR, "models", "GLM-OCR-GGUF")
LLAMA_DIR = os.path.join(OCR_DIR, "llama.cpp")
# ─────────────────────────────────────────────────────────────────────────────

# Allow overriding IMG_PATH via command-line argument
if len(sys.argv) > 1:
    IMG_PATH = sys.argv[1]

if not IMG_PATH:
    print("[ERROR] IMG_PATH is not set. Edit ocr_run.py or pass the image path as an argument.", file=sys.stderr)
    sys.exit(1)

M          = os.path.join(MODEL_DIR, "GLM-OCR-Q8_0.gguf")
MM         = os.path.join(MODEL_DIR, "mmproj-GLM-OCR-Q8_0.gguf")
SERVER_EXE = os.path.join(LLAMA_DIR, "llama-server.exe")
PROMPT     = ("Please recognize and extract all text from this image. "
              "Output the text content line by line, preserving the original layout.")

TIMEOUT = 300  # seconds for inference request

# ── Validate inputs ───────────────────────────────────────────────────────────
for label, path in [("Image", IMG_PATH), ("Model", M), ("mmproj", MM), ("Server", SERVER_EXE)]:
    if not os.path.exists(path):
        print(f"[ERROR] {label} not found: {path}", file=sys.stderr)
        sys.exit(1)

# ── Start llama-server ────────────────────────────────────────────────────────
port = _find_free_port()
server_args = [
    SERVER_EXE,
    "-m", M, "--mmproj", MM,
    "-ngl", "99", "--device", "Vulkan0", "-c", "12000",
    "--host", "127.0.0.1", "--port", str(port),
]

print(f"[INFO] Starting llama-server on port {port} ...", file=sys.stderr)
server_proc = subprocess.Popen(
    server_args,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.DEVNULL,
    creationflags=_CREATE_NO_WINDOW,
)

# Stream server stderr in background for diagnostics
t_err = threading.Thread(target=_stream_stderr, args=(server_proc,), daemon=True)
t_err.start()

try:
    if not _wait_for_server(port):
        print("[ERROR] llama-server failed to start within 120s.", file=sys.stderr)
        server_proc.kill()
        sys.exit(1)

    print("[INFO] Server ready. Sending OCR request ...", file=sys.stderr)

    # ── Send inference request ────────────────────────────────────────────────
    import urllib.request

    # Encode image as base64 data URL
    with open(IMG_PATH, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("ascii")

    # Detect mime type
    ext = os.path.splitext(IMG_PATH)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}
    mime = mime_map.get(ext, "image/png")
    img_url = f"data:{mime};base64,{img_data}"

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": img_url}},
                    {"type": "text", "text": PROMPT},
                ]
            }
        ],
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    resp = urllib.request.urlopen(req, timeout=TIMEOUT)
    result = json.loads(resp.read())

    # Extract text from response
    text = result["choices"][0]["message"]["content"]
    print(text)

finally:
    # ── Shut down server ──────────────────────────────────────────────────────
    server_proc.terminate()
    try:
        server_proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_proc.kill()
    print("[INFO] Server stopped.", file=sys.stderr)
