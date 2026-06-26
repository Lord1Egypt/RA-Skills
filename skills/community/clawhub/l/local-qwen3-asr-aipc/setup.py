"""
setup.py — One-time environment setup for local-asr-qwen3 skill.

Run once from a terminal:
    python setup.py

What this does:
  1. Creates a shared Python venv under {USERNAME}_openvino\venv\
  2. Installs all required packages into the venv
  3. Clones the Qwen3-ASR repo at the pinned commit
  4. Writes state.json so the skill knows where everything is

After this, run:
    python download_model.py
"""

import json, os, re, shutil, subprocess, sys
from pathlib import Path


def _read_skill_version():
    """Read SKILL_VERSION from SKILL.md — single source of truth for all deployed files."""
    try:
        md = Path(__file__).parent / "SKILL.md"
        m = re.search(r"\*\*SKILL_VERSION\*\*[^'\"]*['\"]([^'\"]+)['\"]", md.read_text(encoding='utf-8'))
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"

QWEN_ASR_REPO   = "https://github.com/QwenLM/Qwen3-ASR.git"
QWEN_ASR_COMMIT = "c17a131fe028b2e428b6e80a33d30bb4fa57b8df"

PACKAGES = [
    "openvino>=2025.4",
    "numpy<2.0",
    "librosa",
    "transformers",
    "huggingface_hub",
    "accelerate",
    "soundfile",
    "scipy",
    "modelscope",
]

# ── Banner ─────────────────────────────────────────────────
print("=" * 55)
print("  local-asr-qwen3  ·  Environment Setup")
print("=" * 55)

# ── Locate root directory ──────────────────────────────────
username  = os.environ.get("USERNAME", "user").lower()
root_name = f"{username}_openvino"
drives    = [f"{d}:\\" for d in ("C", "D") if Path(f"{d}:\\").exists()]

root = next(
    (Path(d) / root_name for d in drives if (Path(d) / root_name).exists()),
    None
)
if not root:
    best = max(drives, key=lambda d: shutil.disk_usage(d).free)
    root = Path(best) / root_name

asr_dir  = root / "asr"
venv_dir = root / "venv"
venv_py  = venv_dir / "Scripts" / "python.exe"

root.mkdir(parents=True, exist_ok=True)
asr_dir.mkdir(parents=True, exist_ok=True)

print(f"\n  Root:    {root}")
print(f"  ASR:     {asr_dir}")
print(f"  Venv:    {venv_dir}")

# ── Create or validate venv ────────────────────────────────
print("\n[1/4] Checking venv...")

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
    print(f"  Venv created: {r.stdout.decode().strip()} [OK]")

def venv_run(args, **kw):
    return subprocess.run([str(venv_py)] + args, **kw)

# ── Upgrade pip ────────────────────────────────────────────
print("\n[2/4] Upgrading pip...")
venv_run(["-m", "pip", "install", "--upgrade", "pip", "--quiet"], check=True)

# ── Install packages ───────────────────────────────────────
print("\n[3/4] Installing packages...")

missing = []
for pkg in PACKAGES:
    imp = pkg.split(">=")[0].split("<")[0].replace("-", "_")
    r = venv_run(["-c", f"import {imp}"], capture_output=True)
    if r.returncode != 0:
        missing.append(pkg)

if missing:
    print(f"  Installing: {missing}")
    venv_run(["-m", "pip", "install", "--quiet"] + missing, check=True)
    print("  Packages installed [OK]")
else:
    print("  All packages already present [OK]")

# ── Clone Qwen3-ASR repo ───────────────────────────────────
print("\n[4/4] Qwen3-ASR repo...")

repo = asr_dir / "Qwen3-ASR"
if repo.exists():
    print(f"  Repo already exists: {repo} [OK]")
else:
    print(f"  Cloning from {QWEN_ASR_REPO}...")
    subprocess.run(["git", "clone", QWEN_ASR_REPO, str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "checkout", QWEN_ASR_COMMIT], check=True)
    print("  Cloned [OK]")

print("  Installing qwen_asr package...")
venv_run(["-m", "pip", "install", "-q", "-e", str(repo)], check=True)
print("  qwen_asr installed [OK]")

# ── Write state.json ───────────────────────────────────────
state = {
    "ROOT":        str(root),
    "ASR_DIR":     str(asr_dir),
    "VENV_DIR":    str(venv_dir),
    "VENV_PY":     str(venv_py),
    "VENV_EXISTS": True,
}
state_file = asr_dir / "state.json"
state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
print(f"\n  state.json written: {state_file} [OK]")

# ── Write asr_engine.py ────────────────────────────────────
SKILL_VERSION = _read_skill_version()  # pulled from SKILL.md — single source of truth
engine_file = asr_dir / "asr_engine.py"

# Build the engine payload and redeploy whenever the skill version changes.
engine_code = r'''SKILL_VERSION = "v1.0"
"""
asr_engine.py — OpenVINO inference engine for Qwen3-ASR.
Inference only — no model conversion.
"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional
import numpy as np
import openvino as ov

try:
    from qwen_asr.inference.utils import (
        SAMPLE_RATE, MAX_ASR_INPUT_SECONDS, SUPPORTED_LANGUAGES,
        normalize_audios, parse_asr_output,
        split_audio_into_chunks, merge_languages,
    )
    from qwen_asr.core.transformers_backend.processing_qwen3_asr import Qwen3ASRProcessor
    INFERENCE_UTILS_AVAILABLE = True
except ImportError:
    INFERENCE_UTILS_AVAILABLE = False
    SAMPLE_RATE = 16000
    MAX_ASR_INPUT_SECONDS = 1200
    SUPPORTED_LANGUAGES = ["Chinese", "English"]

core = ov.Core()


def _get_feat_extract_output_lengths(input_lengths):
    input_lengths = np.asarray(input_lengths, dtype=np.int64)
    leave = input_lengths % 100
    feat = (leave - 1) // 2 + 1
    return ((feat - 1) // 2 + 1 - 1) // 2 + 1 + (input_lengths // 100) * 13


class SinusoidsPositionEmbedding:
    def __init__(self, max_pos, embed_dim, max_ts=10000.0):
        half = embed_dim // 2
        inv = np.exp(-np.log(max_ts) / (half - 1) * np.arange(half, dtype=np.float32))
        t = np.arange(max_pos, dtype=np.float32)[:, None] * inv[None, :]
        self.pe = np.concatenate([np.sin(t), np.cos(t)], axis=1).astype(np.float32)
    def __getitem__(self, n): return self.pe[:n, :]


def load_audio_file(path, sr=16000):
    try:
        import soundfile as sf
        audio, orig_sr = sf.read(str(path), dtype="float32")
    except Exception:
        import scipy.io.wavfile as wav
        orig_sr, audio = wav.read(str(path))
        audio = audio.astype(np.float32) / 32768.0
    if audio.ndim > 1: audio = audio.mean(axis=1)
    if orig_sr != sr:
        import librosa
        audio = librosa.resample(audio, orig_sr=orig_sr, target_sr=sr)
    return np.asarray(audio, dtype=np.float32)


@dataclass
class ASRTranscription:
    language: str
    text: str
    time_stamps: Optional[Any] = None


class OVQwen3ASRPipeline:
    def __init__(self, model_dir, device="CPU"):
        self.model_dir = Path(model_dir)
        with open(self.model_dir / "config.json") as f:
            cfg = json.load(f)
        t = cfg.get("thinker_config", {})
        a = t.get("audio_config", {})
        c = t.get("text_config", {})
        self.d_model = a["d_model"]
        self.num_mel_bins = a["num_mel_bins"]
        self.max_source_positions = a["max_source_positions"]
        self.n_window = a["n_window"]
        self.n_window_infer = a.get("n_window_infer", self.n_window * 2)
        self.hidden_size = c["hidden_size"]
        self.audio_token_id = t["audio_token_id"]
        self.pos_emb = SinusoidsPositionEmbedding(self.max_source_positions, self.d_model)
        root = self.model_dir
        thinker = self.model_dir / "thinker"
        def _find(self_names, opt_names):
            for n in self_names:
                if (root / n).exists(): return root / n
            for n in opt_names:
                if (thinker / n).exists(): return thinker / n
            raise FileNotFoundError(f"Model file not found. Tried: {self_names}")
        self.audio_conv    = core.compile_model(_find(["openvino_audio_conv_model.xml"],    ["openvino_thinker_audio_model.xml"]),    device)
        self.audio_encoder = core.compile_model(_find(["openvino_audio_encoder_model.xml"], ["openvino_thinker_audio_encoder_model.xml"]), device)
        self.text_emb      = core.compile_model(_find(["openvino_text_embeddings_model.xml"],["openvino_thinker_embedding_model.xml"]), device)
        lm = core.read_model(_find(["openvino_language_model.xml"], ["openvino_thinker_language_model.xml"]))
        self.lm_input_names = {k.get_any_name(): i for i, k in enumerate(lm.inputs)}
        self._pos_ndim = len(lm.input("position_ids").get_partial_shape())
        self.lm_req = core.compile_model(lm, device).create_infer_request()
        print("All models loaded [OK]")

    def _audio_tower(self, feats, feat_len):
        cs = self.n_window * 2
        aftercnn = int(_get_feat_extract_output_lengths(feat_len))
        cn = int(np.ceil(feat_len / cs))
        clens = np.full(cn, cs, dtype=np.int64)
        if feat_len % cs: clens[-1] = feat_len % cs
        ft = feats.T; chunks = []; s = 0
        for l in clens: chunks.append(ft[s:s+int(l)]); s += int(l)
        mx = max(c.shape[0] for c in chunks)
        pad = [np.pad(c, ((0, mx-c.shape[0]), (0, 0))) if c.shape[0] < mx else c for c in chunks]
        pf = np.stack(pad).transpose(0, 2, 1).astype(np.float32)
        lcnn = _get_feat_extract_output_lengths(clens)
        co = self.audio_conv(pf)[self.audio_conv.output(0)]
        co = co + self.pos_emb[co.shape[1]][None, :, :]
        mask = np.zeros((len(clens), co.shape[1]), dtype=bool)
        for j, cl in enumerate(lcnn): mask[j, :int(cl)] = True
        hidden = co[mask]
        wcnn = mask.shape[-1] * (self.n_window_infer // cs)
        cu = [0] + [wcnn] * (aftercnn // wcnn)
        r = aftercnn % wcnn
        if r: cu.append(r)
        cus = np.cumsum(cu).astype(np.int32)
        segs = []
        for si in range(len(cus) - 1):
            s, e = int(cus[si]), int(cus[si+1])
            out = self.audio_encoder({"hidden_states": hidden[s:e].astype(np.float32), "cu_seqlens": np.array([0, e-s], dtype=np.int32)})[self.audio_encoder.output(0)]
            segs.append(out)
        return np.concatenate(segs, axis=0)

    def _process_audio(self, feats, feat_mask):
        lens = np.sum(feat_mask, axis=1).astype(np.int64)
        return np.concatenate([self._audio_tower(feats[i, :, :int(lens[i])], int(lens[i])) for i in range(feats.shape[0])], axis=0)

    def _embed(self, ids): return self.text_emb(ids)[self.text_emb.output(0)]

    def _lm(self, emb, attn, pos, last_only=True):
        if self._pos_ndim == 3 and pos.ndim == 2: pos = np.stack([pos] * 3, axis=0)
        inp = {"inputs_embeds": emb.astype(np.float32), "attention_mask": attn.astype(np.int64), "position_ids": pos.astype(np.int64)}
        if "beam_idx" in self.lm_input_names: inp["beam_idx"] = np.arange(emb.shape[0], dtype=np.int32)
        self.lm_req.start_async(inp, share_inputs=False); self.lm_req.wait()
        logits = self.lm_req.get_tensor("logits").data
        return logits[:, -1:, :].copy() if last_only else logits.copy()

    _CHUNK = 256
    def _prefill(self, emb, attn, pos):
        seq = emb.shape[1]
        if seq <= self._CHUNK: return self._lm(emb, attn, pos)
        logits = None
        for s in range(0, seq, self._CHUNK):
            e = min(s + self._CHUNK, seq)
            logits = self._lm(emb[:, s:e, :], attn[:, :e], pos[:, s:e])
        return logits

    def transcribe_audio(self, audio, processor, max_new_tokens=512):
        msgs = [{"role": "system", "content": ""}, {"role": "user", "content": [{"type": "audio", "audio": audio}]}]
        text = processor.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
        inp = processor(text=[text], audio=[audio], return_tensors="np", padding=True)
        af = self._process_audio(inp["input_features"], inp["feature_attention_mask"])
        emb = self._embed(inp["input_ids"])
        amask = inp["input_ids"][0] == self.audio_token_id
        na, nf = int(amask.sum()), af.shape[0]
        if na != nf:
            n = min(na, nf); emb[0, np.where(amask)[0][:n]] = af[:n]
        else:
            emb[0, amask] = af
        attn = inp["attention_mask"]
        pos = np.where(attn == 0, 0, np.cumsum(attn, axis=-1) - 1)
        self.lm_req.reset_state(); logits = self._prefill(emb, attn, pos)
        tok = processor.tokenizer; eos = set()
        if tok.eos_token_id: eos.add(tok.eos_token_id)
        for t in ["<|im_end|>", "<|endoftext|>"]:
            tid = tok.convert_tokens_to_ids(t)
            if tid and tid != tok.unk_token_id: eos.add(tid)
        gen = []; cur_attn = attn.copy()
        for _ in range(max_new_tokens):
            t = int(np.argmax(logits[:, -1, :], axis=-1)[0])
            if t in eos: break
            gen.append(t)
            ne = self._embed(np.array([[t]]))
            cur_attn = np.concatenate([cur_attn, np.ones((1, 1), dtype=np.int64)], axis=1)
            logits = self._lm(ne, cur_attn, np.array([[cur_attn.shape[1] - 1]], dtype=np.int64))
        raw = tok.decode(gen, skip_special_tokens=True); clean, lang = raw, "unknown"
        try:
            from qwen_asr.inference.utils import parse_asr_output
            lang, clean = parse_asr_output(raw, user_language=None)
        except Exception:
            for sp in ["<|im_end|>", "<|endoftext|>", "<|im_start|>", "</asr_text>"]: clean = clean.replace(sp, "")
            clean = clean.strip()
        return {"text": clean, "language": lang, "generated_tokens": len(gen)}


class OVQwen3ASRModel:
    def __init__(self, model_dir, device="CPU", max_new_tokens=4096, max_inference_batch_size=32):
        self.max_new_tokens = max_new_tokens
        self.max_inference_batch_size = max(1, int(max_inference_batch_size))
        self.pipeline = OVQwen3ASRPipeline(str(model_dir), device=device)
        self.processor = None
        try:
            self.processor = Qwen3ASRProcessor.from_pretrained(str(model_dir))
            print("Processor loaded [OK]")
        except Exception as e:
            print(f"[WARN] Processor load failed: {e}")
        print(f"OVQwen3ASRModel ready [OK] batch={self.max_inference_batch_size}")

    @classmethod
    def from_pretrained(cls, model_dir, device="CPU", max_new_tokens=4096, max_inference_batch_size=32, **kw):
        return cls(
            model_dir=model_dir,
            device=device,
            max_new_tokens=max_new_tokens,
            max_inference_batch_size=max_inference_batch_size,
        )

    def get_supported_languages(self): return list(SUPPORTED_LANGUAGES)

    def transcribe(self, audio, language=None, **kw):
        if self.processor is None: raise RuntimeError("Processor not loaded")
        wavs = normalize_audios(audio) if INFERENCE_UTILS_AVAILABLE else [self._to_wav(a) for a in (audio if isinstance(audio, list) else [audio])]
        out_l = [[] for _ in range(len(wavs))]
        out_t = [[] for _ in range(len(wavs))]
        for i, wav in enumerate(wavs):
            chunk_buffer = []
            if INFERENCE_UTILS_AVAILABLE:
                chunk_iter = split_audio_into_chunks(wav, sr=SAMPLE_RATE, max_chunk_sec=MAX_ASR_INPUT_SECONDS)
                for cwav, _ in chunk_iter:
                    chunk_buffer.append(cwav)
                    if len(chunk_buffer) >= self.max_inference_batch_size:
                        for buffered_wav in chunk_buffer:
                            r = self.pipeline.transcribe_audio(buffered_wav, self.processor, self.max_new_tokens)
                            out_l[i].append(r["language"]); out_t[i].append(r["text"])
                        chunk_buffer.clear()
            else:
                chunk_buffer.append(wav)

            for buffered_wav in chunk_buffer:
                r = self.pipeline.transcribe_audio(buffered_wav, self.processor, self.max_new_tokens)
                out_l[i].append(r["language"]); out_t[i].append(r["text"])
        return [
            ASRTranscription(
                language=merge_languages(out_l[i]) if INFERENCE_UTILS_AVAILABLE else (out_l[i][0] if out_l[i] else "unknown"),
                text="".join(out_t[i])
            )
            for i in range(len(wavs))
        ]

    @staticmethod
    def _to_wav(a):
        if isinstance(a, str): return load_audio_file(a)
        if isinstance(a, tuple):
            wav, sr = a; wav = np.asarray(wav, dtype=np.float32)
            if wav.ndim > 1: wav = wav.mean(axis=-1)
            if sr != 16000:
                import librosa; wav = librosa.resample(wav, orig_sr=sr, target_sr=16000)
            return wav.astype(np.float32)
        if isinstance(a, np.ndarray): return a.astype(np.float32)
        raise ValueError(f"Unsupported type: {type(a)}")
'''
engine_payload = engine_code.strip().replace('SKILL_VERSION = "v1.0"', f'SKILL_VERSION = "{SKILL_VERSION}"', 1)

needs_write = True
if engine_file.exists():
    m = re.search(r'SKILL_VERSION\s*=\s*["\'](.+?)["\']', engine_file.read_text(encoding="utf-8", errors="ignore"))
    if m and m.group(1) == SKILL_VERSION:
        needs_write = False

if needs_write:
    print(f"\n  Writing asr_engine.py {SKILL_VERSION}...")
    engine_file.write_text(engine_payload, encoding="utf-8")
    print(f"  asr_engine.py written [OK]")
else:
    print(f"\n  asr_engine.py already at {SKILL_VERSION} [OK]")

# ── Deploy transcribe.py ──────────────────────────────────
transcribe_dst = asr_dir / "transcribe.py"
transcribe_src = Path(__file__).parent / "transcribe.py"

# patch __SKILL_VERSION__ placeholder with the actual version from SKILL.md
_content = transcribe_src.read_text(encoding="utf-8")
_content = re.sub(
    r'(SKILL_VERSION\s*=\s*["\'])([^"\']+)(["\'])',
    rf'\g<1>{SKILL_VERSION}\g<3>',
    _content,
    count=1,
)

_needs_deploy = True
if transcribe_dst.exists():
    _m = re.search(
        r'SKILL_VERSION\s*=\s*["\'](.+?)["\']',
        transcribe_dst.read_text(encoding="utf-8", errors="ignore"),
    )
    if _m and _m.group(1) == SKILL_VERSION:
        _needs_deploy = False

if _needs_deploy:
    transcribe_dst.write_text(_content, encoding="utf-8")
    print(f"\n  transcribe.py {SKILL_VERSION} deployed [OK]")
else:
    print(f"\n  transcribe.py already at {SKILL_VERSION} [OK]")

# ── Verify ─────────────────────────────────────────────────
print("\n[Verify] Checking installation...")

verify_script = f"""
results = {{}}
for pkg, imp in [
    ("openvino","openvino"), ("numpy","numpy"), ("librosa","librosa"), ("transformers","transformers"),
    ("huggingface_hub","huggingface_hub"), ("accelerate","accelerate"),
    ("soundfile","soundfile"), ("scipy","scipy"), ("modelscope","modelscope"),
]:
    try:
        ver = getattr(__import__(imp), "__version__", "OK")
        results[pkg] = ("OK", ver)
    except ImportError as e:
        results[pkg] = ("FAIL", str(e))

try:
    import numpy as np
    v = tuple(int(x) for x in np.__version__.split(".")[:2])
    results["numpy"] = ("WARN", f"{{np.__version__}} must be <2.0 — run setup.py again") if v >= (2,0) else ("OK", np.__version__)
except: pass

try:
    from qwen_asr.inference.utils import SAMPLE_RATE
    results["qwen_asr"] = ("OK", f"SAMPLE_RATE={{SAMPLE_RATE}}")
except ImportError as e:
    results["qwen_asr"] = ("FAIL", str(e))

try:
    import sys as _sys
    _sys.path.insert(0, r"{asr_dir}")
    from asr_engine import OVQwen3ASRModel
    results["asr_engine"] = ("OK", "importable")
except ImportError as e:
    results["asr_engine"] = ("FAIL", str(e))

fail = [k for k,(s,_) in results.items() if s == "FAIL"]
for k,(s,d) in results.items():
    icon = "OK  " if s == "OK" else ("WARN" if s == "WARN" else "FAIL")
    print(f"  [{{icon}}] {{k}}: {{d}}")
print()
print("VERIFY=PASS" if not fail else f"VERIFY=FAIL  {{fail}}")
"""
venv_run(["-c", verify_script])

# ── Done ───────────────────────────────────────────────────
print()
print("=" * 55)
print("  Setup complete!")
print()
print("  Next step — download the model (~2 GB):")
print(f"    python \"{Path(__file__).parent / 'download_model.py'}\"")
print("=" * 55)
