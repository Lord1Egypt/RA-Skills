from __future__ import annotations

from collections import OrderedDict, deque
from pathlib import Path
from typing import Any, Callable, Deque, Dict, Generic, List, Optional, Tuple, TypeVar
import hashlib
import json
import logging
import math
import os
import re
import shutil
import subprocess
import threading
import time
import uuid

import numpy as np
import torch
import torchaudio as ta
from fastapi import HTTPException, UploadFile

# Chatterbox/perth compatibility guard:
# some environments expose perth.PerthImplicitWatermarker as None, which crashes model init.
try:
    import perth  # type: ignore

    if not callable(getattr(perth, "PerthImplicitWatermarker", None)):
        class _NoopWatermarker:
            def apply_watermark(self, wav, sample_rate=None):
                return wav

        perth.PerthImplicitWatermarker = _NoopWatermarker  # type: ignore[attr-defined]
except Exception:
    pass

from chatterbox.tts import ChatterboxTTS


DEFAULT_VOICE_NAME = "juno"
DEFAULT_SPEED = 1.2
DEFAULT_EXAGGERATION = 0.5
DEFAULT_CFG = 0.5
DEFAULT_PAUSE_MS = 90
SILENCE_THRESHOLD = 0.006
OPUS_BITRATE = "32k"
SPEED_MIN = 0.5
SPEED_MAX = 2.0
TARGET_SAMPLE_RATE = 16000
MAX_EMBED_CACHE_ITEMS = 8
MAX_PHRASE_RAM_CACHE_ITEMS = 24
MAX_BENCHMARK_RUNS = 100
FFMPEG_TIMEOUT_SEC = 60
VOICE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
ALLOWED_UPLOAD_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
CHUNK_SPLIT_RE = re.compile(r"(?<=[\u3002\uff01\uff1f!?\.\n])")
OUTPUT_EXT = ".opus"

PIPELINE_VERSION = "v3.4"
PIPELINE_SINGLE = "v3.4-single"
PIPELINE_STREAM = "v3.4-stream"

T = TypeVar("T")


class LruCache(Generic[T]):
    """Small thread-safe in-memory LRU."""

    def __init__(self, max_items: int):
        self.max_items = max_items
        self._cache: "OrderedDict[str, T]" = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[T]:
        with self._lock:
            if key not in self._cache:
                return None
            value = self._cache.pop(key)
            self._cache[key] = value
            return value

    def put(self, key: str, value: T) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.pop(key)
            self._cache[key] = value
            while len(self._cache) > self.max_items:
                self._cache.popitem(last=False)

    def keys(self) -> List[str]:
        with self._lock:
            return list(self._cache.keys())


class VoiceEngine:
    def __init__(self, device: str, base_dir: Path):
        self.log = logging.getLogger("tarvis.voice.engine")
        self.device = device
        self.base_dir = base_dir.resolve()
        self.voices_dir = (self.base_dir / "voices").resolve()
        self.cache_dir = (self.base_dir / "voice_cache").resolve()
        self.manifest_path = self.cache_dir / "manifest.json"
        self.audio_cache_dir = (self.cache_dir / "audio").resolve()
        default_outputs_dir = Path.home() / ".openclaw" / "media" / "outbound" / "voice-server-v3"
        self.outputs_dir = Path(
            os.getenv("TARVIS_VOICE_OUTPUT_DIR", str(default_outputs_dir))
        ).expanduser().resolve()
        self.ffmpeg_timeout_sec = self._read_int_env("TARVIS_VOICE_FFMPEG_TIMEOUT_SEC", FFMPEG_TIMEOUT_SEC, 5)
        self.phrase_ram_cache_items = self._read_int_env(
            "TARVIS_VOICE_PHRASE_RAM_CACHE_ITEMS", MAX_PHRASE_RAM_CACHE_ITEMS, 1
        )

        self.voices_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.audio_cache_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

        self._manifest_lock = threading.RLock()
        self._lock_map_guard = threading.Lock()
        self._embedding_locks: Dict[str, threading.Lock] = {}
        self._phrase_locks: Dict[str, threading.Lock] = {}

        self.log.info(
            "engine_init device=%s base_dir=%s outputs_dir=%s phrase_ram_cache_items=%s ffmpeg_timeout_sec=%s",
            self.device,
            self.base_dir,
            self.outputs_dir,
            self.phrase_ram_cache_items,
            self.ffmpeg_timeout_sec,
        )
        self.log.debug("engine_init loading chatterbox model")
        self.model = ChatterboxTTS.from_pretrained(device=device)
        self.cache: LruCache[Any] = LruCache(MAX_EMBED_CACHE_ITEMS)
        self.phrase_ram_cache: LruCache[torch.Tensor] = LruCache(self.phrase_ram_cache_items)
        self.voice_registry: Dict[str, Dict[str, str]] = self._load_manifest()
        self.ffmpeg_ok = shutil.which("ffmpeg") is not None
        self.run_history: Deque[Dict[str, Any]] = deque(maxlen=MAX_BENCHMARK_RUNS)

        # Resolve optional model methods once. Repeated reflection is needless overhead.
        self.encode_method_name, self.encode_method = self._find_first_callable(
            ["encode_audio_prompt", "encode_prompt", "get_speaker_embedding", "extract_speaker_embedding"]
        )
        self.generate_embedding_method_name, self.generate_embedding_method = self._find_first_callable(
            ["generate_from_embedding", "generate_with_embedding"]
        )
        self.log.info(
            "engine_ready ffmpeg_ok=%s encode_method=%s generate_embedding_method=%s loaded_voices=%s",
            self.ffmpeg_ok,
            self.encode_method_name,
            self.generate_embedding_method_name,
            len(self.voice_registry),
        )

    @staticmethod
    def _read_int_env(name: str, default: int, minimum: int) -> int:
        raw = os.getenv(name, str(default))
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return default
        return max(minimum, value)

    def _find_first_callable(self, names: List[str]) -> Tuple[Optional[str], Optional[Callable[..., Any]]]:
        for name in names:
            fn = getattr(self.model, name, None)
            if callable(fn):
                return name, fn
        return None, None

    def _entry_lock(self, lock_map: Dict[str, threading.Lock], key: str) -> threading.Lock:
        with self._lock_map_guard:
            lock = lock_map.get(key)
            if lock is None:
                lock = threading.Lock()
                lock_map[key] = lock
            return lock

    def _resolve_manifest_path(self, path_value: str) -> Path:
        candidate = Path(path_value).expanduser()
        if not candidate.is_absolute():
            candidate = (self.base_dir / candidate).resolve()
        return candidate

    def _load_manifest(self) -> Dict[str, Dict[str, str]]:
        if not self.manifest_path.exists():
            return {}
        try:
            raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except Exception:
            self.log.exception("manifest_load_failed path=%s", self.manifest_path)
            return {}
        if not isinstance(raw, dict):
            self.log.warning("manifest_invalid_type path=%s", self.manifest_path)
            return {}

        cleaned: Dict[str, Dict[str, str]] = {}
        for key, value in raw.items():
            if not isinstance(key, str) or not isinstance(value, dict):
                continue
            try:
                voice_name = self._normalize_voice_name(key)
            except HTTPException:
                continue
            voice_path_raw = str(value.get("voice_path", "")).strip()
            if not voice_path_raw:
                continue
            voice_path = self._resolve_manifest_path(voice_path_raw)
            if not voice_path.exists() or not voice_path.is_file():
                continue
            audio_sha = str(value.get("audio_sha") or self._sha256(voice_path))
            emb_path_raw = str(value.get("embedding_path") or "")
            emb_path = (
                self._resolve_manifest_path(emb_path_raw)
                if emb_path_raw
                else self._embedding_cache_path(voice_name, audio_sha)
            )
            cleaned[voice_name] = {
                "voice_path": str(voice_path),
                "audio_sha": audio_sha,
                "embedding_path": str(emb_path),
                "updated_at": str(value.get("updated_at", int(time.time()))),
            }

        if cleaned.keys() != raw.keys():
            self.log.warning(
                "manifest_cleaned original=%s cleaned=%s path=%s",
                len(raw),
                len(cleaned),
                self.manifest_path,
            )
            self.voice_registry = cleaned
            self._save_manifest()
        return cleaned

    def _save_manifest(self) -> None:
        with self._manifest_lock:
            tmp = self.manifest_path.with_suffix(".tmp.json")
            try:
                tmp.write_text(json.dumps(self.voice_registry, indent=2), encoding="utf-8")
                os.replace(tmp, self.manifest_path)
            finally:
                if tmp.exists():
                    tmp.unlink(missing_ok=True)
        self.log.debug("manifest_saved entries=%s path=%s", len(self.voice_registry), self.manifest_path)

    @staticmethod
    def _validate_text(text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        return cleaned

    @staticmethod
    def _normalize_speed(speed: float) -> float:
        if speed <= 0:
            raise HTTPException(status_code=400, detail="speed must be > 0")
        return max(SPEED_MIN, min(SPEED_MAX, float(speed)))

    @staticmethod
    def _normalize_voice_name(voice_name: str) -> str:
        cleaned = (voice_name or "").strip().lower()
        if not VOICE_NAME_RE.fullmatch(cleaned):
            raise HTTPException(
                status_code=400,
                detail="Invalid voice_name; use 1-64 chars: letters, numbers, underscore, hyphen",
            )
        return cleaned

    @staticmethod
    def _assert_within_dir(target: Path, root: Path, detail: str) -> Path:
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=detail) from exc
        return target

    @staticmethod
    def _sha256(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def _sha256_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def _split_text_chunks(text: str, max_chars: int = 140) -> List[str]:
        raw_parts = [p.strip() for p in CHUNK_SPLIT_RE.split(text) if p.strip()]
        if not raw_parts:
            return []

        chunks: List[str] = []
        for part in raw_parts:
            if len(part) <= max_chars:
                chunks.append(part)
                continue

            # Space-delimited languages: chunk by words.
            if re.search(r"\s", part):
                words = part.split()
                cur: List[str] = []
                cur_len = 0
                for w in words:
                    extra = len(w) + (1 if cur else 0)
                    if cur and (cur_len + extra) > max_chars:
                        chunks.append(" ".join(cur).strip())
                        cur = [w]
                        cur_len = len(w)
                    else:
                        cur.append(w)
                        cur_len += extra
                if cur:
                    chunks.append(" ".join(cur).strip())
                continue

            # No spaces (common in CJK): hard-slice by length.
            for i in range(0, len(part), max_chars):
                chunks.append(part[i : i + max_chars].strip())

        return [c for c in chunks if c]

    @staticmethod
    def _trim_silence(wav: torch.Tensor, threshold: float = SILENCE_THRESHOLD) -> torch.Tensor:
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        if wav.numel() == 0:
            return wav

        mono = wav.abs().mean(dim=0)
        nz = torch.where(mono > threshold)[0]
        if nz.numel() == 0:
            return wav
        start = int(nz[0].item())
        end = int(nz[-1].item()) + 1
        return wav[:, start:end]

    @staticmethod
    def _resample_if_needed(wav: torch.Tensor, src_sr: int, target_sr: int) -> torch.Tensor:
        if src_sr == target_sr:
            return wav
        return ta.functional.resample(wav, src_sr, target_sr)

    @staticmethod
    def _pause_wav(sample_rate: int, pause_ms: int) -> torch.Tensor:
        n = max(1, int(sample_rate * (pause_ms / 1000.0)))
        return torch.zeros((1, n), dtype=torch.float32)

    @staticmethod
    def _atomic_save_wav(cache_path: Path, wav: torch.Tensor, sample_rate: int) -> None:
        tmp = cache_path.with_suffix(".tmp.wav")
        ta.save(str(tmp), wav, sample_rate)
        os.replace(tmp, cache_path)

    @staticmethod
    def _atomic_save_torch(path: Path, obj: Any) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        torch.save(obj, tmp)
        os.replace(tmp, path)

    def _write_sidecar(self, out_file: Path, meta: Dict[str, Any]) -> bool:
        sidecar = out_file.with_suffix(".json")
        tmp = sidecar.with_suffix(".tmp.json")
        try:
            tmp.write_text(json.dumps(meta, indent=2), encoding="utf-8")
            os.replace(tmp, sidecar)
            return True
        except Exception:
            self.log.exception("sidecar_write_failed path=%s", sidecar)
            return False
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)

    def _encode_opus_tensor(
        self,
        wav: torch.Tensor,
        sample_rate: int,
        dst_opus: Path,
        speed: float,
        bitrate: str = OPUS_BITRATE,
    ) -> float:
        speed = self._normalize_speed(speed)

        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        if wav.dim() != 2:
            raise HTTPException(status_code=500, detail="Invalid wav tensor shape for opus encoding")

        wav_cpu = wav.detach().to("cpu", dtype=torch.float32).clamp(-1.0, 1.0).contiguous()
        pcm = (wav_cpu.transpose(0, 1).numpy() * 32767.0).astype(np.int16)
        channels = wav_cpu.shape[0]

        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-y",
            "-f",
            "s16le",
            "-ar",
            str(sample_rate),
            "-ac",
            str(channels),
            "-i",
            "pipe:0",
        ]
        if not math.isclose(speed, 1.0, rel_tol=1e-4, abs_tol=1e-4):
            cmd.extend(["-filter:a", f"atempo={speed:.3f}"])
        cmd.extend(
            [
                "-c:a",
                "libopus",
                "-b:a",
                bitrate,
                "-vbr",
                "on",
                "-application",
                "voip",
                str(dst_opus),
            ]
        )

        self.log.debug(
            "opus_encode_start dst=%s sample_rate=%s channels=%s speed=%.3f bitrate=%s",
            dst_opus,
            sample_rate,
            channels,
            speed,
            bitrate,
        )
        try:
            subprocess.run(
                cmd,
                input=pcm.tobytes(),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=self.ffmpeg_timeout_sec,
            )
        except FileNotFoundError as exc:
            raise HTTPException(status_code=500, detail="ffmpeg not found; cannot encode opus") from exc
        except subprocess.TimeoutExpired as exc:
            raise HTTPException(status_code=500, detail="Opus encode timed out") from exc
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr.decode("utf-8", errors="ignore") if exc.stderr else "ffmpeg failed").strip()
            raise HTTPException(status_code=500, detail=f"Opus encode failed: {detail[:500]}") from exc

        self.log.debug("opus_encode_done dst=%s", dst_opus)
        return speed

    def _embedding_cache_path(self, voice_name: str, audio_sha: str) -> Path:
        return self.cache_dir / f"{voice_name}_{audio_sha[:16]}.pt"

    def _phrase_cache_path(self, key: str) -> Path:
        return self.audio_cache_dir / f"{key}.wav"

    def _phrase_cache_key(self, voice_name: str, text: str, exaggeration: float, cfg: float, sample_rate: int) -> str:
        fingerprint = f"{PIPELINE_VERSION}|{voice_name}|{text}|{exaggeration:.3f}|{cfg:.3f}|{sample_rate}"
        return self._sha256_text(fingerprint)

    def _load_phrase_from_cache(self, key: str, sample_rate: int) -> Optional[torch.Tensor]:
        mem = self.phrase_ram_cache.get(key)
        if mem is not None:
            self.log.debug("phrase_cache_hit key=%s source=memory", key[:12])
            return mem

        path = self._phrase_cache_path(key)
        if not path.exists():
            return None
        try:
            wav, sr = ta.load(str(path))
            if sr != sample_rate:
                wav = self._resample_if_needed(wav, sr, sample_rate)
            wav = wav.contiguous()
            self.phrase_ram_cache.put(key, wav)
            self.log.debug("phrase_cache_hit key=%s source=disk", key[:12])
            return wav
        except Exception:
            self.log.exception("phrase_cache_load_failed path=%s", path)
            return None

    def _save_phrase_to_cache(self, key: str, wav: torch.Tensor, sample_rate: int) -> None:
        wav_cpu = wav.detach().to("cpu", dtype=torch.float32).contiguous()
        self.phrase_ram_cache.put(key, wav_cpu)
        try:
            self._atomic_save_wav(self._phrase_cache_path(key), wav_cpu, sample_rate)
        except Exception:
            self.log.exception("phrase_cache_save_failed key=%s", key[:12])

    def bootstrap_default_voice(self, voice_name: str = DEFAULT_VOICE_NAME) -> bool:
        voice_name = self._normalize_voice_name(voice_name)
        with self._manifest_lock:
            if voice_name in self.voice_registry:
                self.log.debug("bootstrap_default_voice skip existing voice=%s", voice_name)
                return True

        candidates = [
            self.base_dir.parent / "voice" / f"{voice_name}_ref.wav",
            self.base_dir.parent / "voice" / f"{voice_name}.wav",
            self.voices_dir / f"{voice_name}.wav",
        ]
        src = next((p for p in candidates if p.exists()), None)
        if src is None:
            self.log.warning("bootstrap_default_voice missing voice=%s", voice_name)
            return False

        dst = self.voices_dir / f"{voice_name}.wav"
        if src.resolve() != dst.resolve():
            dst.write_bytes(src.read_bytes())

        audio_sha = self._sha256(dst)
        emb_path = self._embedding_cache_path(voice_name, audio_sha)
        with self._manifest_lock:
            self.voice_registry[voice_name] = {
                "voice_path": str(dst),
                "audio_sha": audio_sha,
                "embedding_path": str(emb_path),
                "updated_at": str(int(time.time())),
            }
            self._save_manifest()
        self.log.info("bootstrap_default_voice ok voice=%s path=%s", voice_name, dst)
        return True

    def register_voice(self, voice_name: str, uploaded: UploadFile, data: bytes) -> Dict[str, Any]:
        started = time.perf_counter()
        trace_id = uuid.uuid4().hex[:12]
        self.log.debug(
            "register_voice_start trace_id=%s voice=%s filename=%s size=%s",
            trace_id,
            voice_name,
            uploaded.filename,
            len(data),
        )

        voice_name = self._normalize_voice_name(voice_name)
        ext = Path(uploaded.filename or "sample.wav").suffix.lower() or ".wav"
        if ext not in ALLOWED_UPLOAD_EXTS:
            raise HTTPException(status_code=400, detail="Unsupported audio format")

        voice_path = (self.voices_dir / f"{voice_name}{ext}").resolve()
        self._assert_within_dir(voice_path, self.voices_dir, "Voice path is outside voices directory")
        voice_path.write_bytes(data)
        audio_sha = self._sha256(voice_path)
        emb_path = self._embedding_cache_path(voice_name, audio_sha)

        with self._manifest_lock:
            self.voice_registry[voice_name] = {
                "voice_path": str(voice_path),
                "audio_sha": audio_sha,
                "embedding_path": str(emb_path),
                "updated_at": str(int(time.time())),
            }
            self._save_manifest()

        precomputed = False
        mode = "wav_per_request"
        try:
            emb = self._compute_embedding(str(voice_path))
            if emb is not None:
                self.cache.put(voice_name, emb)
                self._atomic_save_torch(emb_path, emb)
                precomputed = True
                mode = "cached_embedding"
        except Exception:
            self.log.exception("register_voice_embedding_failed trace_id=%s voice=%s", trace_id, voice_name)
            precomputed = False
            mode = "wav_per_request"

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        self.log.info(
            "register_voice_done trace_id=%s voice=%s precomputed=%s mode=%s elapsed_ms=%.2f",
            trace_id,
            voice_name,
            precomputed,
            mode,
            elapsed_ms,
        )
        return {
            "ok": True,
            "voice_name": voice_name,
            "voice_path": str(voice_path),
            "precomputed": precomputed,
            "mode": mode,
        }

    def _compute_embedding(self, voice_path: str) -> Optional[Any]:
        if self.encode_method is None:
            return None
        emb = self.encode_method(voice_path)
        if isinstance(emb, torch.Tensor):
            emb = emb.detach().to(self.device)
        return emb

    def _load_or_build_embedding(self, voice_name: str) -> Optional[Any]:
        cached = self.cache.get(voice_name)
        if cached is not None:
            self.log.debug("embedding_cache_hit voice=%s source=memory", voice_name)
            return cached

        lock = self._entry_lock(self._embedding_locks, voice_name)
        with lock:
            cached = self.cache.get(voice_name)
            if cached is not None:
                self.log.debug("embedding_cache_hit voice=%s source=memory_after_lock", voice_name)
                return cached

            with self._manifest_lock:
                info = dict(self.voice_registry.get(voice_name) or {})
            if not info:
                raise HTTPException(status_code=404, detail=f"Voice '{voice_name}' not registered")

            emb_path = self._resolve_manifest_path(info.get("embedding_path", ""))
            if emb_path.exists():
                try:
                    emb = torch.load(emb_path, map_location=self.device)
                    self.cache.put(voice_name, emb)
                    self.log.debug("embedding_cache_hit voice=%s source=disk", voice_name)
                    return emb
                except Exception:
                    self.log.exception("embedding_load_failed voice=%s path=%s", voice_name, emb_path)

            voice_path = info.get("voice_path")
            emb = self._compute_embedding(voice_path)
            if emb is None:
                self.log.debug("embedding_unavailable voice=%s", voice_name)
                return None
            self.cache.put(voice_name, emb)
            try:
                self._atomic_save_torch(emb_path, emb)
            except Exception:
                self.log.exception("embedding_save_failed voice=%s path=%s", voice_name, emb_path)
            return emb

    def _generate_wav(self, voice_name: str, text: str, exaggeration: float, cfg: float) -> Tuple[torch.Tensor, str]:
        with self._manifest_lock:
            info = dict(self.voice_registry.get(voice_name) or {})
        if not info:
            raise HTTPException(status_code=404, detail=f"Voice '{voice_name}' not registered")
        voice_path = info["voice_path"]

        emb = self._load_or_build_embedding(voice_name)
        with torch.inference_mode():
            if emb is not None and self.generate_embedding_method is not None:
                try:
                    wav = self.generate_embedding_method(
                        text=text,
                        embedding=emb,
                        exaggeration=exaggeration,
                        cfg_weight=cfg,
                    )
                except TypeError:
                    wav = self.generate_embedding_method(
                        text=text,
                        embedding=emb,
                        exaggeration=exaggeration,
                        cfg=cfg,
                    )
                mode = f"embedding:{self.generate_embedding_method_name}"
            else:
                wav = self.model.generate(
                    text,
                    audio_prompt_path=voice_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg,
                )
                mode = "wav_per_request"
        return wav, mode

    def _get_or_generate_phrase(
        self,
        voice_name: str,
        text: str,
        exaggeration: float,
        cfg: float,
        sample_rate: int,
    ) -> Tuple[torch.Tensor, str, bool]:
        key = self._phrase_cache_key(voice_name, text, exaggeration, cfg, sample_rate)
        cached = self._load_phrase_from_cache(key, sample_rate)
        if cached is not None:
            return cached, "phrase_cache", True

        lock = self._entry_lock(self._phrase_locks, key)
        with lock:
            cached = self._load_phrase_from_cache(key, sample_rate)
            if cached is not None:
                return cached, "phrase_cache", True

            wav, mode = self._generate_wav(voice_name, text, exaggeration, cfg)
            self._save_phrase_to_cache(key, wav, sample_rate)
            return wav, mode, False

    def _record_run(
        self,
        endpoint: str,
        voice_name: str,
        cache_hits: int,
        cache_misses: int,
        latency_ms: Dict[str, float],
    ) -> None:
        self.run_history.append(
            {
                "ts": int(time.time()),
                "endpoint": endpoint,
                "voice_name": voice_name,
                "cache_hits": cache_hits,
                "cache_misses": cache_misses,
                "latency_ms": {k: float(v) for k, v in latency_ms.items()},
            }
        )

    def benchmark_summary(self) -> Dict[str, Any]:
        runs = list(self.run_history)
        if not runs:
            return {"count": 0, "cache_hit_ratio": 0.0, "stages": {}}

        stage_values: Dict[str, List[float]] = {}
        total_hits = 0
        total_misses = 0
        for run in runs:
            total_hits += int(run.get("cache_hits", 0))
            total_misses += int(run.get("cache_misses", 0))
            for k, v in (run.get("latency_ms") or {}).items():
                stage_values.setdefault(k, []).append(float(v))

        def _pct(vals: List[float], p: float) -> float:
            if not vals:
                return 0.0
            arr = np.array(sorted(vals), dtype=np.float64)
            idx = int(round((len(arr) - 1) * p))
            return float(arr[idx])

        stages: Dict[str, Dict[str, float]] = {}
        for stage, vals in stage_values.items():
            stages[stage] = {
                "p50": round(_pct(vals, 0.50), 2),
                "p95": round(_pct(vals, 0.95), 2),
                "mean": round(float(np.mean(vals)), 2),
            }

        denom = total_hits + total_misses
        hit_ratio = (total_hits / denom) if denom else 0.0
        return {
            "count": len(runs),
            "cache_hit_ratio": round(hit_ratio, 4),
            "cache_hits": total_hits,
            "cache_misses": total_misses,
            "stages": stages,
        }

    def synthesize(
        self,
        voice_name: str,
        text: str,
        exaggeration: float = DEFAULT_EXAGGERATION,
        cfg: float = DEFAULT_CFG,
        speed: float = DEFAULT_SPEED,
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        run_id = trace_id or uuid.uuid4().hex[:12]
        self.log.debug(
            "synthesize_start run_id=%s voice=%s text_len=%s speed=%.3f exaggeration=%.3f cfg=%.3f",
            run_id,
            voice_name,
            len(text or ""),
            speed,
            exaggeration,
            cfg,
        )
        started = time.perf_counter()
        timings: Dict[str, float] = {}

        t0 = time.perf_counter()
        voice_name = self._normalize_voice_name(voice_name)
        text = self._validate_text(text)
        timings["validate_ms"] = (time.perf_counter() - t0) * 1000.0

        sample_rate = self.model.sr

        t1 = time.perf_counter()
        wav, mode, cache_hit = self._get_or_generate_phrase(
            voice_name=voice_name,
            text=text,
            exaggeration=exaggeration,
            cfg=cfg,
            sample_rate=sample_rate,
        )
        timings["tts_and_cache_ms"] = (time.perf_counter() - t1) * 1000.0

        t2 = time.perf_counter()
        wav = self._trim_silence(wav)
        timings["trim_ms"] = (time.perf_counter() - t2) * 1000.0

        out_file = self.outputs_dir / f"{voice_name}_{int(time.time() * 1000)}{OUTPUT_EXT}"

        t3 = time.perf_counter()
        normalized_speed = self._encode_opus_tensor(wav, sample_rate, out_file, speed=speed)
        timings["encode_ms"] = (time.perf_counter() - t3) * 1000.0

        t4 = time.perf_counter()
        meta = {
            "trace_id": run_id,
            "voice_name": voice_name,
            "mode": mode,
            "device": self.device,
            "sample_rate": sample_rate,
            "pipeline": PIPELINE_SINGLE,
            "output_format": "opus",
            "speed": normalized_speed,
            "cache_hits": 1 if cache_hit else 0,
            "cache_misses": 0 if cache_hit else 1,
        }
        sidecar_written = self._write_sidecar(out_file, {**meta, "latency_ms": {}})
        timings["sidecar_ms"] = (time.perf_counter() - t4) * 1000.0

        timings["total_ms"] = (time.perf_counter() - started) * 1000.0
        meta["latency_ms"] = {k: round(v, 2) for k, v in timings.items()}
        meta["sidecar_written"] = sidecar_written

        if sidecar_written:
            self._write_sidecar(out_file, meta)

        self._record_run("/speak", voice_name, meta["cache_hits"], meta["cache_misses"], timings)
        self.log.debug(
            "synthesize_done run_id=%s voice=%s mode=%s cache_hit=%s total_ms=%.2f",
            run_id,
            voice_name,
            mode,
            cache_hit,
            timings["total_ms"],
        )
        return {"path": str(out_file), "meta": meta}

    def synthesize_stream(
        self,
        voice_name: str,
        text: str,
        exaggeration: float = DEFAULT_EXAGGERATION,
        cfg: float = DEFAULT_CFG,
        speed: float = DEFAULT_SPEED,
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        run_id = trace_id or uuid.uuid4().hex[:12]
        self.log.debug(
            "synthesize_stream_start run_id=%s voice=%s text_len=%s speed=%.3f exaggeration=%.3f cfg=%.3f",
            run_id,
            voice_name,
            len(text or ""),
            speed,
            exaggeration,
            cfg,
        )
        started = time.perf_counter()
        timings: Dict[str, float] = {}

        t0 = time.perf_counter()
        voice_name = self._normalize_voice_name(voice_name)
        text = self._validate_text(text)
        timings["validate_ms"] = (time.perf_counter() - t0) * 1000.0

        t1 = time.perf_counter()
        chunks = self._split_text_chunks(text)
        timings["chunking_ms"] = (time.perf_counter() - t1) * 1000.0
        if not chunks:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        sample_rate = self.model.sr
        generated: List[torch.Tensor] = []
        modes: List[str] = []
        cache_hits = 0
        cache_misses = 0

        t2 = time.perf_counter()
        for idx, chunk in enumerate(chunks):
            self.log.debug(
                "synthesize_stream_chunk run_id=%s index=%s len=%s",
                run_id,
                idx,
                len(chunk),
            )
            wav, mode, cache_hit = self._get_or_generate_phrase(
                voice_name=voice_name,
                text=chunk,
                exaggeration=exaggeration,
                cfg=cfg,
                sample_rate=sample_rate,
            )
            if cache_hit:
                cache_hits += 1
            else:
                cache_misses += 1
            generated.append(self._trim_silence(wav))
            modes.append(mode)
        timings["tts_and_cache_ms"] = (time.perf_counter() - t2) * 1000.0

        t3 = time.perf_counter()
        pause = self._pause_wav(sample_rate, DEFAULT_PAUSE_MS)
        stitched: List[torch.Tensor] = []
        for i, wav in enumerate(generated):
            stitched.append(wav)
            if i < len(generated) - 1:
                stitched.append(pause)
        merged = torch.cat(stitched, dim=1) if stitched else torch.zeros((1, 1), dtype=torch.float32)
        timings["stitch_ms"] = (time.perf_counter() - t3) * 1000.0

        t4 = time.perf_counter()
        merged_16k = self._resample_if_needed(merged, sample_rate, TARGET_SAMPLE_RATE)
        timings["resample_16k_ms"] = (time.perf_counter() - t4) * 1000.0

        t5 = time.perf_counter()
        out_file = self.outputs_dir / f"{voice_name}_{int(time.time() * 1000)}_stream{OUTPUT_EXT}"
        normalized_speed = self._encode_opus_tensor(merged_16k, TARGET_SAMPLE_RATE, out_file, speed=speed)
        timings["encode_ms"] = (time.perf_counter() - t5) * 1000.0

        t6 = time.perf_counter()
        meta = {
            "trace_id": run_id,
            "voice_name": voice_name,
            "device": self.device,
            "sample_rate": TARGET_SAMPLE_RATE,
            "chunk_count": len(chunks),
            "chunks": chunks,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "modes": modes,
            "pipeline": PIPELINE_STREAM,
            "output_format": "opus",
            "speed": normalized_speed,
            "features": [
                "speak_stream_chunked",
                "phrase_audio_cache",
                "phrase_ram_cache",
                "single_and_stream_cache_reuse",
                "pause_trim_and_16k",
                "per_stage_latency_metrics",
                "debug_trace_ids",
            ],
        }
        sidecar_written = self._write_sidecar(out_file, {**meta, "latency_ms": {}})
        timings["sidecar_ms"] = (time.perf_counter() - t6) * 1000.0

        timings["total_ms"] = (time.perf_counter() - started) * 1000.0
        meta["latency_ms"] = {k: round(v, 2) for k, v in timings.items()}
        meta["sidecar_written"] = sidecar_written

        if sidecar_written:
            self._write_sidecar(out_file, meta)

        self._record_run("/speak_stream", voice_name, cache_hits, cache_misses, timings)
        self.log.debug(
            "synthesize_stream_done run_id=%s voice=%s chunks=%s cache_hits=%s cache_misses=%s total_ms=%.2f",
            run_id,
            voice_name,
            len(chunks),
            cache_hits,
            cache_misses,
            timings["total_ms"],
        )
        return {"path": str(out_file), "meta": meta}

    def assert_within_output_dir(self, path_str: str) -> Path:
        target = Path(path_str).expanduser().resolve()
        return self._assert_within_dir(target, self.outputs_dir, "Path is outside voice output directory")

    def cleanup_output(self, path_str: str) -> Dict[str, Any]:
        target = self.assert_within_output_dir(path_str)
        if target.suffix.lower() != OUTPUT_EXT:
            raise HTTPException(status_code=400, detail="cleanup supports only .opus outputs")
        sidecar = target.with_suffix(".json")
        deleted: List[str] = []
        missing: List[str] = []

        for path in (target, sidecar):
            if path.exists():
                if not path.is_file():
                    raise HTTPException(status_code=400, detail="cleanup target must be a file")
                path.unlink()
                deleted.append(str(path))
            else:
                missing.append(str(path))
        self.log.debug("cleanup_output path=%s deleted=%s missing=%s", path_str, len(deleted), len(missing))
        return {"ok": True, "deleted": deleted, "missing": missing}
