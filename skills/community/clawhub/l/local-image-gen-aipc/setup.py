"""
setup.py — One-time environment setup for local-image-generation skill.

Run once from a terminal:
    python setup.py

What this does:
  1. Creates a shared Python venv under {USERNAME}_openvino\venv\
  2. Checks git is available (required for pinned git+https dependencies)
  3. Installs all required packages into the venv
  4. Writes state.json so the skill knows where everything is
  5. Deploys generate_image.py to IMAGE_GEN_DIR (versioned, idempotent)

After this, run:
    python download_model.py
"""

import io, json, os, shutil, string, subprocess, sys
from pathlib import Path

# Force UTF-8 stdout/stderr — prevents UnicodeEncodeError on Chinese Windows (CP936)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

REQUIREMENTS_FILE = "requirements_imagegen.txt"

PACKAGES_FALLBACK = [
    "openvino==2026.0.0",  # pinned: 2026.1.0 breaks OVZImagePipeline pooled_projections
    "torch>=2.1.0",
    "Pillow>=10.0.0",
    "modelscope>=1.14.0",
    "git+https://github.com/huggingface/optimum-intel.git@2f62e5ae#egg=optimum-intel[openvino]",
    "git+https://github.com/huggingface/diffusers.git@a1f36ee3",
]


def _read_skill_version() -> str:
    """Read SKILL_VERSION from SKILL.md next to this script — single source of truth."""
    skill_md = Path(__file__).parent / "SKILL.md"
    if skill_md.exists():
        for line in skill_md.read_text(encoding="utf-8").splitlines():
            if "SKILL_VERSION" in line and "`" in line:
                parts = line.split("`")
                if len(parts) >= 2:
                    return parts[1]
    return "unknown"

# ── Banner ─────────────────────────────────────────────────
print("=" * 55)
print("  local-image-generation  ·  Environment Setup")
print("=" * 55)

# ── Check Python version ───────────────────────────────────
vi = sys.version_info
if vi < (3, 10):
    print(f"\n[ERROR] Python {vi.major}.{vi.minor} detected — need >= 3.10")
    print("  Download: https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe")
    sys.exit(1)
print(f"\n  Python {vi.major}.{vi.minor}.{vi.micro} OK ✅")

# ── Check git ──────────────────────────────────────────────
r = subprocess.run(["git", "--version"], capture_output=True)
if r.returncode != 0:
    print("\n[ERROR] git not found — required for pinned git+https dependencies")
    print("  Download: https://git-scm.com/download/win")
    sys.exit(1)
print(f"  {r.stdout.decode().strip()} OK ✅")

# ── Locate root directory ──────────────────────────────────
username  = os.environ.get("USERNAME", "user").lower()
root_name = f"{username}_openvino"
drives    = [f"{d}:\\" for d in string.ascii_uppercase if Path(f"{d}:\\").exists()]

root = next(
    (Path(d) / root_name for d in drives if (Path(d) / root_name).exists()),
    None
)
if not root:
    best = max(drives, key=lambda d: shutil.disk_usage(d).free)
    root = Path(best) / root_name

imagegen_dir = root / "imagegen"
venv_dir     = root / "venv"
venv_py      = venv_dir / "Scripts" / "python.exe"

root.mkdir(parents=True, exist_ok=True)
imagegen_dir.mkdir(parents=True, exist_ok=True)

print(f"\n  Root:     {root}")
print(f"  Imagegen: {imagegen_dir}")
print(f"  Venv:     {venv_dir}")

# ── Create or validate venv ────────────────────────────────
print("\n[1/3] Checking venv...")

venv_ok = False
if venv_py.exists():
    try:
        r = subprocess.run([str(venv_py), "--version"], capture_output=True, timeout=10)
        if r.returncode == 0:
            print(f"  Existing venv OK: {r.stdout.decode().strip()}")
            venv_ok = True
    except Exception:
        pass

if not venv_ok:
    if venv_dir.exists():
        print("  Existing venv is broken — rebuilding...")
        shutil.rmtree(venv_dir, ignore_errors=True)
    print("  Creating venv...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    venv_py = venv_dir / "Scripts" / "python.exe"
    r = subprocess.run([str(venv_py), "--version"], capture_output=True)
    print(f"  Venv created: {r.stdout.decode().strip()} ✅")

def venv_run(args, **kw):
    return subprocess.run([str(venv_py)] + args, **kw)

# ── Upgrade pip ────────────────────────────────────────────
print("\n[2/3] Upgrading pip...")
venv_run(["-m", "pip", "install", "--upgrade", "pip", "--quiet"], check=True)
print("  pip upgraded ✅")

# ── Install packages ───────────────────────────────────────
print("\n[3/3] Installing packages (this may take ~5 min)...")

req_file = Path(__file__).parent / REQUIREMENTS_FILE
if req_file.exists():
    print(f"  Using {req_file}")
    venv_run(["-m", "pip", "install", "-r", str(req_file)], check=True)
else:
    print(f"  {REQUIREMENTS_FILE} not found — installing fallback list")
    venv_run(["-m", "pip", "install"] + PACKAGES_FALLBACK, check=True)

print("  Packages installed ✅")

# ── Write state.json ───────────────────────────────────────
state = {
    "ROOT":          str(root),
    "IMAGE_GEN_DIR": str(imagegen_dir),
    "VENV_DIR":      str(venv_dir),
    "VENV_PY":       str(venv_py),
    "VENV_EXISTS":   True,
    "SKILL_DIR":     str(Path(__file__).parent.resolve()),
}
state_file = imagegen_dir / "state.json"
state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
print(f"\n  state.json written: {state_file} ✅")

# ── Create outputs dir ─────────────────────────────────────
(imagegen_dir / "outputs").mkdir(exist_ok=True)

# ── Verify ─────────────────────────────────────────────────
print("\n[Verify] Checking installation...")

verify_script = """
results = {}
for pkg, imp in [
    ("openvino",   "openvino"),
    ("torch",      "torch"),
    ("Pillow",     "PIL"),
    ("modelscope", "modelscope"),
]:
    try:
        ver = getattr(__import__(imp), "__version__", "OK")
        results[pkg] = ("OK", ver)
    except ImportError as e:
        results[pkg] = ("FAIL", str(e))

try:
    from optimum.intel import OVZImagePipeline
    results["OVZImagePipeline"] = ("OK", "importable")
except ImportError as e:
    results["OVZImagePipeline"] = ("FAIL", str(e))

fail = [k for k, (s, _) in results.items() if s == "FAIL"]
for k, (s, d) in results.items():
    icon = "OK  " if s == "OK" else "FAIL"
    print(f"  [{icon}] {k}: {d}")
print()
print("VERIFY=PASS" if not fail else f"VERIFY=FAIL  {fail}")
"""
venv_run(["-c", verify_script])

# ── Deploy generate_image.py ───────────────────────────────
print("\n[Deploy] Deploying generate_image.py...")

SCRIPT_VERSION = _read_skill_version()
script_path = imagegen_dir / "generate_image.py"

existing_ver = None
if script_path.exists():
    for line in script_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("SKILL_VERSION") and "=" in line:
            existing_ver = line.split("=")[1].strip().strip("\"'")
            break

if existing_ver == SCRIPT_VERSION:
    print(f"  generate_image.py already at {SCRIPT_VERSION} [OK]")
else:
    generate_image_code = r'''SKILL_VERSION = "__VER__"
import sys, io, os, json, string, argparse, re, subprocess
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

def get_state():
    for d in string.ascii_uppercase:
        sf = Path(f"{d}:\\") / f"{os.environ.get('USERNAME','user').lower()}_openvino" / "imagegen" / "state.json"
        if sf.exists():
            return json.loads(sf.read_text(encoding="utf-8"))
    return None

def get_device():
    import openvino as ov
    core = ov.Core()
    devs = core.available_devices
    print(f"[INFO] Available devices: {devs}")
    for d in devs:
        if "GPU" in d:
            print(f"[INFO] Using Intel GPU: {d}")
            return d
    print("[INFO] Using CPU")
    return "CPU"

def make_filename(topic, prompt):
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = topic if topic else prompt[:30]
    safe = re.sub(r"[^\w]", "_", src.strip())[:30].strip("_")
    return f"{date_str}_{safe}.png"

def generate(prompt, topic="", steps=9, width=512, height=512, seed=42, output_path=None):
    state = get_state()
    if not state:
        print("[ERROR] state.json not found -- run setup.py")
        sys.exit(1)
    imagegen_dir = Path(state["IMAGE_GEN_DIR"])
    model_dir    = imagegen_dir / "Z-Image-Turbo-int4-ov"
    out_dir      = imagegen_dir / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    required = ["transformer", "vae_decoder", "text_encoder"]
    missing  = [r for r in required if not (model_dir / r).exists()]
    if missing:
        print(f"[ERROR] Model incomplete: {missing} -- run download_model.py")
        sys.exit(1)
    device = get_device()
    print(f"[INFO] Loading model: {model_dir}")
    import torch
    from optimum.intel import OVZImagePipeline
    pipe = OVZImagePipeline.from_pretrained(str(model_dir), device=device)
    print("[INFO] Model loaded")
    gen = torch.Generator("cpu").manual_seed(seed) if seed >= 0 else None
    print(f"[INFO] Inference: steps={steps}, {width}x{height}, seed={seed}")
    image = pipe(
        prompt=prompt, height=height, width=width,
        num_inference_steps=steps, guidance_scale=0.0, generator=gen
    ).images[0]
    if output_path is None:
        output_path = str(out_dir / make_filename(topic, prompt))
    image.save(output_path)
    print(f"[SUCCESS] {output_path}")
    try:
        subprocess.Popen(["explorer", output_path])
    except Exception as e:
        print(f"[WARN] Could not open image: {e}")
    return output_path

if __name__ == "__main__":
    try:
        p = argparse.ArgumentParser()
        p.add_argument("--prompt", required=True)
        p.add_argument("--topic",  default="")
        p.add_argument("--steps",  type=int, default=9)
        p.add_argument("--width",  type=int, default=512)
        p.add_argument("--height", type=int, default=512)
        p.add_argument("--seed",   type=int, default=42)
        p.add_argument("--output", default=None)
        args = p.parse_args()
        generate(args.prompt, args.topic, args.steps, args.width, args.height, args.seed, args.output)
        sys.stdout.flush()
    except Exception as e:
        import traceback
        print(f"[FATAL] {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)
'''
    code = generate_image_code.replace('SKILL_VERSION = "__VER__"', f'SKILL_VERSION = "{SCRIPT_VERSION}"', 1)
    script_path.write_text(code.strip(), encoding="utf-8")
    print(f"  generate_image.py deployed at {SCRIPT_VERSION} [OK]")

# ── Done ───────────────────────────────────────────────────
print()
print("=" * 55)
print("  Setup complete!")
print()
print("  Next step — download the model (~10 GB):")
print(f"    python \"{Path(__file__).parent / 'download_model.py'}\"")
print("=" * 55)
