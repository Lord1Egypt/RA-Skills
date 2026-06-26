#!/usr/bin/env python3
"""
Photo Grader — Apply Lightroom-style color grading via RawTherapee CLI.

Reads a JSON parameter file (from LLM output or manual creation) and applies
professional color grading to each specified photo file, exporting high-quality JPGs.

Uses RawTherapee CLI (rawtherapee-cli) as the sole processing engine.
LR parameters are automatically mapped to PP3 sidecar files for rendering.

Supported Camera RAW Formats:
    Nikon (.nef .nrw), Canon (.cr2 .cr3 .crw), Sony (.arw .srf .sr2),
    Fujifilm (.raf), Olympus (.orf), Panasonic (.rw2), Pentax (.pef),
    Samsung (.srw), Leica (.rwl .dng), Adobe (.dng), Hasselblad (.3fr .fff),
    Phase One (.iiq), Sigma (.x3f)

Also supports: JPEG (.jpg/.jpeg), Apple HEIC/HEIF (.heic/.heif)

Dependencies:
    RawTherapee CLI (rawtherapee-cli)
    tomllib (stdlib 3.11+) / tomli (<3.11)

    Check & install: bash scripts/setup_deps.sh

Usage:
    python grade.py grading_params.json
    python grade.py grading_params.json --raw-dir ~/Photos/RAW --output ~/Photos/Graded
    python grade.py grading_params.json --dry-run
    python grade.py grading_params.json --pp3-only --pp3-output ./pp3/
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add photo-toolkit to path for shared utilities
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "photo-toolkit" / "scripts"))
from file_matcher import find_file_by_stem, find_raw_file, SUPPORTED_EXTENSIONS

# ── Configuration ───────────────────────────────────────────────

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

_SKILL_DIR = Path(__file__).resolve().parent.parent
_ROOT_DIR = _SKILL_DIR.parent
_DEFAULT_CONFIG_PATH = (
    _SKILL_DIR / "config.toml" if (_SKILL_DIR / "config.toml").exists() else _ROOT_DIR / "config.toml"
)


def load_config(config_path=None):
    """Load configuration from config.toml."""
    path = Path(config_path or _DEFAULT_CONFIG_PATH).expanduser().resolve()
    if not path.exists():
        return {}
    try:
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
        if not isinstance(cfg, dict):
            print(f"⚠️  Config is not a valid mapping, ignoring: {path}", file=sys.stderr)
            return {}
        print(f"📄 Loaded config: {path}")
        return cfg
    except Exception as e:
        print(f"⚠️  Failed to read config ({path}): {e}", file=sys.stderr)
        return {}


# ── RawTherapee CLI Detection ──────────────────────────────────

_RT_CLI = None


def find_rawtherapee_cli(cli_path=None):
    """Find rawtherapee-cli executable."""
    global _RT_CLI
    if _RT_CLI is not None:
        return _RT_CLI

    if cli_path and Path(cli_path).exists():
        _RT_CLI = str(Path(cli_path).resolve())
        return _RT_CLI

    # Search PATH
    rt = shutil.which("rawtherapee-cli")
    if rt:
        _RT_CLI = rt
        return rt

    # Try 'rawtherapee' (some distros only install GUI binary)
    rt_gui = shutil.which("rawtherapee")
    if rt_gui:
        gui_dir = Path(rt_gui).parent
        cli_candidate = gui_dir / "rawtherapee-cli"
        if cli_candidate.exists():
            _RT_CLI = str(cli_candidate.resolve())
            return _RT_CLI
        _RT_CLI = rt_gui  # Fallback: use GUI binary (works but slower)
        return _RT_CLI

    return None


def _rt_cli_install_hint():
    if sys.platform == "darwin":
        # Always verify the CLI on macOS. If an agent installed RawTherapee via
        # Homebrew and the user has not explicitly opened/authorized it yet,
        # macOS may block startup with 133 / SIGTRAP. A user-authorized
        # Homebrew CLI can work; otherwise use the official standalone CLI.
        return (
            "Verify with rawtherapee-cli -h. If macOS blocks a Homebrew-installed CLI, "
            "open/authorize it manually or use the official standalone rawtherapee-cli in PATH"
        )
    return "Install: apt install rawtherapee-cli (Debian/Ubuntu) / dnf install RawTherapee (Fedora/RHEL)"


def _validate_rt_cli_executable(rt):
    """Run a lightweight smoke test to ensure rawtherapee-cli can actually start."""
    try:
        result = subprocess.run([rt, "-h"], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, f"failed to start: {e}"

    output = f"{result.stdout}\n{result.stderr}"
    output_lower = output.lower()
    if "rawtherapee, version" in output_lower and "command line" in output_lower:
        return True, output.splitlines()[0] if output.splitlines() else "RawTherapee CLI"

    if result.returncode == 133 or "sigtrap" in output_lower or "trace trap" in output_lower:
        return False, "exited with 133 (SIGTRAP / trace trap), often macOS blocking an unapproved CLI before startup"
    if result.returncode == 132 or "sigill" in output_lower or "illegal instruction" in output_lower:
        return False, "exited with 132 (SIGILL / illegal instruction), usually an incompatible macOS CLI build"

    if result.returncode != 0:
        tail = output.strip().splitlines()[-1] if output.strip() else f"exit code {result.returncode}"
        return False, tail

    return (
        False,
        "executable did not print RawTherapee command-line help; make sure this is rawtherapee-cli, not the GUI binary",
    )


def check_rt_cli(config=None):
    """Check that rawtherapee-cli is available and can start successfully."""
    cfg = config or {}
    rt = find_rawtherapee_cli(cfg.get("rawtherapee_cli", ""))
    if not rt:
        print("❌ RawTherapee CLI not found.", file=sys.stderr)
        print(f"   {_rt_cli_install_hint()}", file=sys.stderr)
        sys.exit(1)

    ok, message = _validate_rt_cli_executable(rt)
    if not ok:
        print(f"❌ RawTherapee CLI is not usable: {rt}", file=sys.stderr)
        print(f"   Reason: {message}", file=sys.stderr)
        print(f"   Verify manually with: {rt} -h", file=sys.stderr)
        print(f"   {_rt_cli_install_hint()}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Engine: RawTherapee ({rt}) — {message}")
    return rt


# ═══════════════════════════════════════════════════════════════
# RawTherapee: LR → PP3 Parameter Mapping
# ═══════════════════════════════════════════════════════════════


def rt_clamp(v, lo=0, hi=999):
    """Clamp value to range [lo, hi] for RT PP3."""
    return max(lo, min(hi, v))


def rt_clamp_f(v, lo=0.0, hi=999.0):
    """Clamp float value to range [lo, hi] for RT PP3."""
    return max(lo, min(hi, v))


def rt_map_exposure(pp3, basic):
    """Map LR exposure ±2.0 → RT Exposure.Comensation + Black."""
    val = basic.get("exposure", 0)
    if abs(val) < 0.001:
        return
    pp3[("Exposure", "Compensation")] = round(val * 2.0, 3)
    if val < -0.3:
        pp3[("Exposure", "Black")] = int(round(-val * 500))


def rt_map_contrast(pp3, basic):
    """Map LR contrast ±100 → RT Exposure.Contrast."""
    val = basic.get("contrast", 0)
    if abs(val) < 0.5:
        return
    pp3[("Exposure", "Contrast")] = round(val * 0.8)


def rt_map_tone_compression(pp3, basic):
    """Map LR highlights/shadows/whites/blacks → RT HighlightCompr/ShadowCompr."""
    hl = basic.get("highlights", 0)
    sh = basic.get("shadows", 0)

    if abs(hl) >= 0.5:
        if hl > 0:
            pp3[("Exposure", "HighlightCompr")] = round(rt_clamp(hl, 0, 100))
        else:
            pp3[("HLRecovery", "Enabled")] = True
            pp3[("HLRecovery", "Method")] = "Coloropp"
            pp3[("HLRecovery", "Hlbl")] = round(rt_clamp(-hl, 0, 100))

    if abs(sh) >= 0.5:
        if sh > 0:
            pp3[("Exposure", "ShadowCompr")] = round(rt_clamp(sh, 0, 100))
        else:
            # RT Shadow recovery via Shadows & Highlights
            pp3[("Shadows & Highlights", "Enabled")] = True
            pp3[("Shadows & Highlights", "Shadows")] = round(rt_clamp(-sh, 0, 100))

    # Whites/Blacks adjustment via tone curve points
    # (No direct RT key; handled by rt_map_tone_curve if tone_curve params exist)


def rt_map_whitebalance(pp3, basic):
    """Map explicit RawTherapee white balance values.

    Lightroom-style temp_offset is intentionally not mapped to RT Temperature:
    RawTherapee expects an absolute Kelvin value, not a relative offset.
    Use temperature_kelvin for absolute WB, and green for RT's green multiplier.
    """
    temp_kelvin = basic.get("temperature_kelvin")
    green = basic.get("green")
    tint = basic.get("tint_offset", 0)

    if temp_kelvin is not None:
        try:
            temp_kelvin = float(temp_kelvin)
        except (TypeError, ValueError) as e:
            raise ValueError("temperature_kelvin must be a number") from e
        if not 2000 <= temp_kelvin <= 25000:
            raise ValueError("temperature_kelvin must be between 2000 and 25000")
        pp3[("White Balance", "Temperature")] = int(round(temp_kelvin))

    if green is not None:
        try:
            green = float(green)
        except (TypeError, ValueError) as e:
            raise ValueError("green must be a number") from e
        if not 0.5 <= green <= 2.0:
            raise ValueError("green must be between 0.5 and 2.0")
        pp3[("White Balance", "Green")] = round(green, 3)
    elif abs(tint) >= 0.5:
        pp3[("White Balance", "Green")] = round(rt_clamp_f(1.0 + tint * 0.005, 0.5, 2.0), 3)


def rt_map_vibrance_saturation(pp3, basic):
    """Map LR vibrance/saturation → RT Vibrance.Pastels/Saturated."""
    vib = basic.get("vibrance", 0)
    sat = basic.get("saturation", 0)
    if abs(vib) >= 0.5:
        pp3[("Vibrance", "Enabled")] = True
        pp3[("Vibrance", "Pastels")] = round(vib * 0.9)
    if abs(sat) >= 0.5:
        pp3[("Vibrance", "Enabled")] = True
        pp3[("Vibrance", "Saturated")] = round(sat * 0.7)


def rt_map_tone_curve(pp3, tc_params):
    """Map LR 4-point S-curve → RT Exposure.Curve (Control Cage for RT 5.10)."""
    hl = tc_params.get("highlights", 0)
    lt = tc_params.get("lights", 0)
    dk = tc_params.get("darks", 0)
    sh = tc_params.get("shadows", 0)
    if all(abs(v) < 0.5 for v in [hl, lt, dk, sh]):
        return

    # RT 5.10 uses simple semicolon-separated values (Control Cage), not CubicSpline
    base_y = [0, 111, 222, 333, 444, 555, 666, 777, 888, 999]
    hl_adj = hl / 100.0 * 80
    lt_adj = lt / 100.0 * 40
    dk_adj = dk / 100.0 * 40
    sh_adj = sh / 100.0 * 80

    y = [
        rt_clamp(base_y[0] + sh_adj * 150),
        rt_clamp(base_y[1] + sh_adj * 60),
        rt_clamp(base_y[2] + dk_adj * 30),
        rt_clamp(base_y[3] + dk_adj * 50),
        rt_clamp(base_y[4]),
        rt_clamp(base_y[5]),
        rt_clamp(base_y[6] + lt_adj * 50),
        rt_clamp(base_y[7] + lt_adj * 30),
        rt_clamp(base_y[8] + hl_adj * 60),
        rt_clamp(base_y[9] + hl_adj * 150),
    ]
    pts_str = ";".join(f"{rt_clamp(v, 0, 999)}" for v in y)
    # RT 5.10: simple format, no CubicSpline prefix
    pp3[("Exposure", "Curve")] = pts_str
    pp3[("Exposure", "CurveMode")] = "Standard"


_RT_HSL_MAP = {
    "red": "Red",
    "orange": "Orange",
    "yellow": "Yellow",
    "green": "Green",
    "aqua": "Cyan",
    "blue": "Blue",
    "purple": "BluePurple",
    "magenta": "Purple",
}


def rt_map_hsl(pp3, hsl_list):
    """Map LR 8-channel HSL adjustments → RT HSV Equalizer curves.

    RawTherapee's HSV Equalizer uses HCurve/SatCurve/ValCurve (CubicSpline),
    not per-channel keys. We convert LR's 8-channel adjustments into these
    curves by mapping each channel's hue/saturation/luminance offset to
    control points on the respective curve.

    The 8 LR channels map to approximate positions on the 0-360 hue wheel:
      Red=0, Orange=30, Yellow=60, Green=120, Cyan=180, Blue=240, Purple=270, Magenta=300
    """
    if not hsl_list:
        return
    has_any = any(any(abs(item.get(k, 0)) >= 0.5 for k in ("hue", "saturation", "luminance")) for item in hsl_list)
    if not has_any:
        return

    # Map LR channel names to hue positions (degrees)
    CHANNEL_HUE_POS = {
        "red": 0,
        "orange": 30,
        "yellow": 60,
        "green": 120,
        "aqua": 180,
        "blue": 240,
        "purple": 270,
        "magenta": 300,
    }

    # Collect per-channel adjustments
    h_adj = {}  # hue_pos → hue_offset
    s_adj = {}  # hue_pos → sat_offset
    l_adj = {}  # hue_pos → lum_offset

    for item in hsl_list:
        ch = item.get("channel", "").lower()
        if ch not in CHANNEL_HUE_POS:
            continue
        hue_pos = CHANNEL_HUE_POS[ch]
        h_val = item.get("hue", 0)
        s_val = item.get("saturation", 0)
        l_val = item.get("luminance", 0)
        if abs(h_val) >= 0.5:
            h_adj[hue_pos] = h_val * 0.8
        if abs(s_val) >= 0.5:
            s_adj[hue_pos] = s_val * 0.8
        if abs(l_val) >= 0.5:
            l_adj[hue_pos] = l_val * 0.8

    # Build CubicSpline curves from adjustments
    # Base control points: evenly spaced across hue wheel (0-999 mapped from 0-360)
    # We use 9 points: 0, 45, 90, 135, 180, 225, 270, 315, 360 → 0, 125, 250, 375, 500, 625, 750, 875, 999
    BASE_POINTS = [0, 125, 250, 375, 500, 625, 750, 875, 999]
    BASE_HUE = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    def build_curve(adj_map):
        """Build a CubicSpline curve from hue-position adjustments."""
        if not adj_map:
            return None
        points = list(BASE_POINTS)  # flat baseline = identity
        for i, hue in enumerate(BASE_HUE):
            # Find the nearest adjustment
            best_adj = 0
            best_dist = float("inf")
            for adj_hue, adj_val in adj_map.items():
                dist = min(abs(hue - adj_hue), 360 - abs(hue - adj_hue))
                if dist < best_dist and dist <= 30:
                    best_dist = dist
                    best_adj = adj_val * (1 - dist / 60)  # falloff
            points[i] = rt_clamp(points[i] + round(best_adj * 3), 0, 999)
        # RT 5.10: simple format, no CubicSpline prefix
        return ";".join(str(v) for v in points)

    h_curve = build_curve(h_adj)
    s_curve = build_curve(s_adj)
    l_curve = build_curve(l_adj)

    if h_curve:
        pp3[("HSV Equalizer", "Enabled")] = True
        pp3[("HSV Equalizer", "HueCurve")] = h_curve
    if s_curve:
        pp3[("HSV Equalizer", "Enabled")] = True
        pp3[("HSV Equalizer", "SatCurve")] = s_curve
    if l_curve:
        pp3[("HSV Equalizer", "Enabled")] = True
        pp3[("HSV Equalizer", "ValCurve")] = l_curve


def rt_map_color_grading(pp3, cg_params):
    """Map LR 3-way color grading → RT Color Toning."""
    if not cg_params:
        return
    sh_hue = cg_params.get("shadow_hue", 0)
    sh_sat = cg_params.get("shadow_saturation", 0)
    mh_hue = cg_params.get("midtone_hue", 0)
    mh_sat = cg_params.get("midtone_saturation", 0)
    hh_hue = cg_params.get("highlight_hue", 0)
    hh_sat = cg_params.get("highlight_saturation", 0)

    has_sh = abs(sh_hue) >= 0.5 or abs(sh_sat) >= 0.5
    has_hh = abs(hh_hue) >= 0.5 or abs(hh_sat) >= 0.5
    has_mh = abs(mh_hue) >= 0.5 or abs(mh_sat) >= 0.5
    if not (has_sh or has_hh or has_mh):
        return

    pp3[("Color Toning", "Enabled")] = True
    pp3[("Color Toning", "Method")] = "Splitlr"
    if has_sh:
        pp3[("Color Toning", "Shadows_Hue")] = rt_clamp(int(sh_hue), 0, 360)
        pp3[("Color Toning", "Shadows_Saturation")] = round(rt_clamp(sh_sat, 0, 100) * 0.8)
    if has_hh:
        pp3[("Color Toning", "Highlights_Hue")] = rt_clamp(int(hh_hue), 0, 360)
        pp3[("Color Toning", "Highlights_Saturation")] = round(rt_clamp(hh_sat, 0, 100) * 0.8)
    if has_mh:
        pp3[("Color Toning", "AutoCorrection")] = round(rt_clamp(mh_sat, 0, 100) * 0.6)
        pp3[("Color Toning", "Split")] = round(rt_clamp(abs(mh_sat) * 0.35, 0, 70))


def rt_map_sharpening(pp3, detail):
    """Map LR sharpening → RT Sharpening (RL Deconvolution)."""
    if not detail:
        return
    amount = detail.get("sharpen_amount", 0)
    radius = detail.get("sharpen_radius", 1.0)
    if amount < 1:
        return
    pp3[("Sharpening", "Enabled")] = True
    pp3[("Sharpening", "Method")] = "rl"
    pp3[("Sharpening", "DeconvRadius")] = round(rt_clamp_f(radius * 0.75, 0.5, 2.0), 2)
    pp3[("Sharpening", "DeconvAmount")] = round(rt_clamp(amount * 1.5, 0, 250))
    pp3[("Sharpening", "DeconvIterations")] = 30


def rt_map_noise_reduction(pp3, detail):
    """Map LR noise reduction → RT Directional Pyramid Denoising."""
    if not detail:
        return
    nr = detail.get("noise_reduction", 0)
    nd = detail.get("noise_detail", 50)
    if nr < 1:
        return
    pp3[("Directional Pyramid Denoising", "Enabled")] = True
    pp3[("Directional Pyramid Denoising", "Luma")] = round(rt_clamp(nr * 0.8, 0, 100))
    pp3[("Directional Pyramid Denoising", "Ldetail")] = round(rt_clamp(100 - nd, 0, 100))
    pp3[("Directional Pyramid Denoising", "Chroma")] = round(rt_clamp(nr * 0.5 + 15, 0, 100))
    pp3[("Directional Pyramid Denoising", "Gamma")] = 1.4
    pp3[("Directional Pyramid Denoising", "Method")] = "Lab"


def rt_map_vignette(pp3, effects):
    """Map LR vignette → RT Vignetting Correction."""
    if not effects:
        return
    vig = effects.get("vignette_amount", 0)
    if abs(vig) < 0.5:
        return
    pp3[("Vignetting Correction", "Amount")] = round(abs(vig) * 1.5)
    pp3[("Vignetting Correction", "Radius")] = 50
    pp3[("Vignetting Correction", "Strength")] = 1
    pp3[("Vignetting Correction", "CenterX")] = 0
    pp3[("Vignetting Correction", "CenterY")] = 0


def rt_map_grain(pp3, effects):
    """Map LR grain → RT FilmSimulation (approximation).

    RawTherapee has no built-in film grain module. As an approximation,
    we configure a subtle grain effect via the [FilmSimulation] section
    if a film simulation CLUT is available. Otherwise this is a no-op.
    """
    if not effects:
        return
    grain = effects.get("grain_amount", 0)
    if grain < 1:
        return
    # Store grain params for potential post-processing; RT itself doesn't
    # have a grain module. The FilmSimulation section requires a CLUT file.
    # We leave a comment-style entry that RT will ignore.
    pp3[("_Comment", "FilmGrain")] = f"LR grain_amount={round(grain * 6)}; RT has no grain module"


def build_pp3(params, style="graded", config=None):
    """Convert a single LR parameter set to a RawTherapee PP3 file content string.

    All rt_map_* functions populate pp3 with (section, key) → value entries,
    which are then serialized to INI format with correct RT section names.
    """
    cfg = config or {}
    pp3 = {}

    basic = params.get("basic", {})
    tc = params.get("tone_curve", {})
    hsl = params.get("hsl", [])
    cg = params.get("color_grading", {})
    detail = params.get("detail", {})
    effects = params.get("effects", {})

    rt_map_exposure(pp3, basic)
    rt_map_contrast(pp3, basic)
    rt_map_tone_compression(pp3, basic)
    rt_map_whitebalance(pp3, basic)
    rt_map_vibrance_saturation(pp3, basic)
    rt_map_tone_curve(pp3, tc)
    rt_map_hsl(pp3, hsl)
    rt_map_color_grading(pp3, cg)
    rt_map_sharpening(pp3, detail)
    rt_map_noise_reduction(pp3, detail)
    rt_map_vignette(pp3, effects)
    rt_map_grain(pp3, effects)

    # RAW preprocessing defaults
    pp3[("RAW", "CA_AutoCorrect")] = False
    pp3[("RAW", "DenoiseBlack")] = False
    pp3[("RAW", "HotPixelFilter")] = False
    pp3[("RAW", "DeadPixelFilter")] = False
    pp3[("RAW", "FF_AutoClipControl")] = False

    # Output settings
    bpp = cfg.get("output_bpp", 8)
    pp3[("Color Management", "OutputBPC")] = True
    if bpp == 16:
        pp3[("Output", "Format")] = "TIFF"
        pp3[("Output", "BitDepth")] = 16
    else:
        pp3[("Output", "Format")] = "JPEG"
        pp3[("Output", "Quality")] = cfg.get("output_quality", 95)

    # Lens correction
    if cfg.get("lens_correction", True):
        pp3[("LensProfile", "LcMode")] = "lensfun"
        pp3[("LensProfile", "UseDistortion")] = True
        pp3[("LensProfile", "UseVignette")] = True
        pp3[("LensProfile", "UseCA")] = True

    # Auto-Matched Camera Curve
    if cfg.get("auto_matched_curve", True):
        pp3[("Color Management", "ToneCurve")] = False

    # ── Section order for PP3 output ──
    # Defines the order sections appear in the PP3 file.
    # Sections not in this list but present in pp3 will be appended at the end.
    SECTION_ORDER = [
        "Version",
        "Exposure",
        "HLRecovery",
        "White Balance",
        "Vibrance",
        "Color Management",
        "HSV Equalizer",
        "Color Toning",
        "Sharpening",
        "Directional Pyramid Denoising",
        "Vignetting Correction",
        "LensProfile",
        "Shadows & Highlights",
        "RAW",
        "Output",
    ]

    # Group pp3 entries by section
    sections = {}
    for (sec, key), val in pp3.items():
        sections.setdefault(sec, {})[key] = val

    # Build INI content
    lines = []
    written_sections = set()

    # Always write Version header first
    lines.append("[Version]")
    lines.append("AppVersion=5.11")
    lines.append("Version=333")
    lines.append("")

    def _fmt_val(val):
        # RawTherapee expects 1/0 for booleans, not Python True/False
        if isinstance(val, bool):
            return 1 if val else 0
        return val

    for sec_name in SECTION_ORDER:
        if sec_name == "Version":
            written_sections.add(sec_name)
            continue
        if sec_name in sections:
            lines.append(f"[{sec_name}]")
            for key, val in sections[sec_name].items():
                lines.append(f"{key}={_fmt_val(val)}")
            lines.append("")
            written_sections.add(sec_name)

    # Append any remaining sections not in SECTION_ORDER (except _Comment)
    for sec_name in sorted(sections.keys()):
        if sec_name in written_sections or sec_name.startswith("_"):
            continue
        lines.append(f"[{sec_name}]")
        for key, val in sections[sec_name].items():
            lines.append(f"{key}={_fmt_val(val)}")
        lines.append("")

    style_tag = params.get("style", style)
    safe_style = "".join(c if c.isalnum() or c in "-_" else "_" for c in style_tag)[:20]

    return "\n".join(lines), safe_style


def _compute_output_name(raw_path, safe_style, raw_root=None):
    """Compute output filename with subdirectory prefix if needed.

    If raw_path is under a subdirectory of raw_root, prefix the output name
    with the subdirectory path: e.g., 001_DSC_0001_暖春丝滑.jpg
    """
    stem = raw_path.stem
    if raw_root:
        try:
            rel = raw_path.relative_to(raw_root)
            if rel.parent != Path("."):
                prefix = str(rel.parent).replace("/", "_").replace("\\", "_")
                return f"{prefix}_{stem}_{safe_style}.jpg"
        except ValueError:
            pass
    return f"{stem}_{safe_style}.jpg"


def grade_single_file(
    raw_path,
    output_dir,
    params,
    config,
    quality=95,
    overwrite=False,
    dry_run=False,
    pp3_only=False,
    pp3_output_dir=None,
    fast_export=False,
    raw_root=None,
):
    """Grade a single photo using RawTherapee CLI: LR params → PP3 → render."""
    start = time.monotonic()
    raw_name = raw_path.name

    try:
        style = params.get("style", "graded")
        safe_style = "".join(c if c.isalnum() or c in "_-" else "_" for c in style)[:20]

        pp3_content, safe_style = build_pp3(params, style=safe_style, config=config)

        # PP3-only mode
        if pp3_only and pp3_output_dir:
            pp3_dir = Path(pp3_output_dir).expanduser().resolve()
            pp3_path = pp3_dir / f"{raw_path.stem}_{safe_style}.pp3"
            pp3_dir.mkdir(parents=True, exist_ok=True)
            with open(pp3_path, "w", encoding="utf-8") as f:
                f.write(pp3_content)
            elapsed = time.monotonic() - start
            return (raw_name, True, f"✓ PP3 generated: {pp3_path.name} ({len(pp3_content)} bytes)", elapsed)

        jpg_name = _compute_output_name(raw_path, safe_style, raw_root)
        jpg_path = output_dir / jpg_name

        if jpg_path.exists() and not overwrite:
            elapsed = time.monotonic() - start
            return (raw_name, True, f"⏭ Skipped (exists): {jpg_name}", elapsed)

        if dry_run:
            tmp_pp3 = output_dir / f"{raw_path.stem}_{safe_style}.pp3"
            with open(tmp_pp3, "w", encoding="utf-8") as f:
                f.write(pp3_content)
            elapsed = time.monotonic() - start
            return (raw_name, True, f"🔍 Dry-run: PP3 written to {tmp_pp3.name} ({len(pp3_content)} bytes)", elapsed)

        # Write PP3 to temp file
        tmp_pp3 = output_dir / f"__rt_tmp_{raw_path.stem}__.pp3"
        with open(tmp_pp3, "w", encoding="utf-8") as f:
            f.write(pp3_content)

        # Build rawtherapee-cli command (RT 5.10: -c must be last)
        cli = [_RT_CLI]
        if fast_export:
            cli += ["-f"]
        cli += ["-o", str(output_dir)]
        cli += [f"-j{quality}"]  # RT 5.10: -j95 not -j 95
        cli += ["-p", str(tmp_pp3)]
        if overwrite:
            cli += ["-Y"]
        cli += ["-c", str(raw_path)]  # Must be last

        result = subprocess.run(cli, capture_output=True, text=True, timeout=300)

        tmp_pp3.unlink(missing_ok=True)

        if result.returncode != 0:
            stderr_tail = result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
            elapsed = time.monotonic() - start
            return (raw_name, False, f"✗ {raw_name}: RT error (code {result.returncode})\n{stderr_tail}", elapsed)

        # Find output file - RT may place it in input dir, move to output_dir
        matched = list(output_dir.glob(f"{raw_path.stem}_*.jpg"))
        output_jpg = matched[0] if matched else jpg_path

        # RT 5.10 sometimes outputs to input directory; move if needed
        alt_jpg = raw_path.parent / f"{raw_path.stem}.jpg"
        if not output_jpg.exists() and alt_jpg.exists():
            import shutil

            shutil.move(str(alt_jpg), str(jpg_path))
            output_jpg = jpg_path

        elapsed = time.monotonic() - start
        if output_jpg.exists():
            file_size_kb = output_jpg.stat().st_size / 1024
            return (raw_name, True, f"✓ {output_jpg.name} ({file_size_kb:.0f}KB)", elapsed)
        else:
            alt_jpg = raw_path.parent / f"{raw_path.stem}_{safe_style}.jpg"
            if alt_jpg.exists():
                return (raw_name, True, f"✓ {alt_jpg.name} (RT side-by-side)", elapsed)
            return (raw_name, True, f"✓ {raw_name} (RT completed)", elapsed)

    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return (raw_name, False, f"✗ {raw_name}: Timeout after {elapsed:.1f}s", elapsed)
    except Exception as e:
        elapsed = time.monotonic() - start
        return (raw_name, False, f"✗ {raw_name}: {e}", elapsed)


# ═══════════════════════════════════════════════════════════════
# Shared file helpers
# ═══════════════════════════════════════════════════════════════


def _normalize_flat_params(entry):
    """Convert flat params dict to nested structure."""
    BASIC_KEYS = {
        "exposure",
        "contrast",
        "highlights",
        "shadows",
        "whites",
        "blacks",
        "temp_offset",
        "tint_offset",
        "vibrance",
        "saturation",
    }
    DETAIL_KEYS = {"sharpen_amount", "sharpen_radius", "noise_reduction", "noise_detail"}
    EFFECTS_KEYS = {"vignette_amount", "grain_amount", "grain_size"}
    RAW_KEYS = {"auto_bright", "bright"}

    flat = entry.get("params", {})
    if not flat:
        return entry
    if any(k in entry for k in ("basic", "detail", "effects", "tone_curve", "hsl")):
        return entry

    result = {"file": entry.get("file", ""), "style": entry.get("style", "graded")}
    basic, detail, effects, raw_params = {}, {}, {}, {}
    for k, v in flat.items():
        if k in BASIC_KEYS:
            basic[k] = v
        elif k in DETAIL_KEYS:
            detail[k] = v
        elif k in EFFECTS_KEYS:
            effects[k] = v
        elif k in RAW_KEYS:
            raw_params[k] = v
    if basic:
        result["basic"] = basic
    if detail:
        result["detail"] = detail
    if effects:
        result["effects"] = effects
    if raw_params:
        result["raw"] = raw_params
    return result


def load_grading_params(json_path):
    """Load grading parameters from JSON file. Supports multiple formats."""
    path = Path(json_path).expanduser().resolve()
    if not path.exists():
        print(f"❌ Parameter file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = []
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        if "files" in data and isinstance(data["files"], list):
            entries = data["files"]
        else:
            entries = [data]
    else:
        print("❌ Invalid JSON format: expected object or array", file=sys.stderr)
        sys.exit(1)

    return [_normalize_flat_params(e) for e in entries]


def find_supported_files(input_dir, recursive=False):
    """Find all supported photo files in directory, sorted by name.

    Skips special directories (thumbnails, graded, sessions) to avoid
    processing already-converted or already-graded files.
    """
    SKIP_DIRS = {"thumbnails", "graded", "sessions", ".ds_store"}
    input_dir = Path(input_dir)
    results = []
    if recursive:
        for p in sorted(input_dir.rglob("*")):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                if any(part in SKIP_DIRS for part in p.parts):
                    continue
                results.append(p)
    else:
        for p in sorted(input_dir.iterdir()):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                results.append(p)
    return results


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds) // 60
    secs = seconds - minutes * 60
    return f"{minutes}m {secs:.0f}s"


def get_cpu_count():
    """Get a reasonable default worker count (cpu_count * 2, max 16)."""
    try:
        return min((os.cpu_count() or 4) * 2, 16)
    except Exception:
        return 4


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="Apply Lightroom-style color grading to camera photos via RawTherapee",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats: RAW (NEF, CR2, CR3, ARW, RAF, ORF, RW2, DNG, PEF, SRW, etc.), JPG, HEIC/HEIF

Engine: RawTherapee CLI (rawtherapee-cli) — professional-grade output
  AMAZE demosaicing, RL Deconvolution sharpening, IWT denoise,
  lensfun correction, Auto-Matched Camera Profiles (~50 models).

Examples:
  %(prog)s grading_params.json
  %(prog)s grading_params.json --raw-dir ~/Photos/RAW --output ~/Photos/Graded
  %(prog)s grading_params.json --quality 98 --no-resize
  %(prog)s grading_params.json --dry-run
  %(prog)s grading_params.json --pp3-only --pp3-output ./pp3_files/

  # Uniform mode: apply one parameter set to all files in a directory
  %(prog)s grading_params.json --uniform-dir ~/Photos/timelapse --output ~/Photos/graded
        """,
    )
    parser.add_argument("params_json", help="JSON file with grading parameters")
    parser.add_argument("--raw-dir", type=str, default=None, help="RAW 文件目录（仅当 file 字段为相对路径时需要）")
    parser.add_argument(
        "--uniform-dir", type=str, default=None, help="Apply first parameter set to ALL files in this directory"
    )
    parser.add_argument("--output", type=str, default=None, help="Output directory for graded JPGs")
    parser.add_argument("--config", type=str, default=None, help="Path to config.toml")
    parser.add_argument("--quality", type=int, default=None, help="JPEG quality 1-100 (default: 95)")
    parser.add_argument("--overwrite", action="store_true", default=None, help="Overwrite existing output files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without processing")
    # RT-specific options
    parser.add_argument("--pp3-only", action="store_true", help="Only generate PP3 files, don't render")
    parser.add_argument(
        "--pp3-output", type=str, default="./pp3/", help="Directory for PP3-only output (default: ./pp3/)"
    )
    parser.add_argument("--fast-export", action="store_true", help="Use fast export mode (skip heavy modules)")
    parser.add_argument(
        "--lens-corr", action="store_true", default=None, help="Enable lens correction (default: from config)"
    )
    parser.add_argument("--no-lens-corr", dest="lens_corr", action="store_false", help="Disable lens correction")
    parser.add_argument("--auto-match", action="store_true", default=None, help="Enable Auto-Matched Camera Profile")
    parser.add_argument(
        "--no-auto-match", dest="auto_match", action="store_false", help="Disable Auto-Matched Camera Profile"
    )
    parser.add_argument("--workers", type=int, default=None, help="Parallel workers")

    args = parser.parse_args()

    cfg = load_config(args.config)

    # Check RT CLI
    check_rt_cli(cfg)

    # Merge CLI flags into config
    if args.lens_corr is not None:
        cfg["lens_correction"] = args.lens_corr
    if args.auto_match is not None:
        cfg["auto_matched_curve"] = args.auto_match

    raw_dir_raw = args.raw_dir or cfg.get("raw_dir") or cfg.get("nef_dir")
    output_raw = args.output or cfg.get("output_dir")
    quality = args.quality if args.quality is not None else cfg.get("jpeg_quality", 95)
    workers = args.workers if args.workers is not None else cfg.get("workers") or get_cpu_count()
    overwrite = args.overwrite if args.overwrite is not None else cfg.get("overwrite", False)
    fast_export = args.fast_export or cfg.get("fast_export", False)

    if not args.uniform_dir and not raw_dir_raw:
        # raw_dir is optional when params use absolute paths
        raw_dir = None
    else:
        raw_dir = Path(raw_dir_raw).expanduser().resolve() if raw_dir_raw else None

    if not output_raw:
        parser.error("--output is required. Provide it as an argument or set 'output_dir' in config.toml")
    if not 1 <= quality <= 100:
        print("Error: --quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    output_dir = Path(output_raw).expanduser().resolve()

    all_params = load_grading_params(args.params_json)
    print(f"📋 Loaded {len(all_params)} grading parameter set(s)")

    # Uniform mode
    uniform_dir = args.uniform_dir
    if uniform_dir:
        uniform_path = Path(uniform_dir).expanduser().resolve()
        if not uniform_path.exists():
            print(f"❌ Uniform directory not found: {uniform_path}", file=sys.stderr)
            sys.exit(1)
        base_params = all_params[0]
        base_params.pop("file", None)
        all_files = find_supported_files(uniform_path)
        if not all_files:
            print(f"❌ No supported photo files found in: {uniform_path}")
            sys.exit(1)

        ext_counts = {}
        for f in all_files:
            ext = f.suffix.upper()
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
        ext_summary = ", ".join(f"{ext}: {cnt}" for ext, cnt in sorted(ext_counts.items()))
        print(f"📷 Uniform mode: applying 1 parameter set to {len(all_files)} file(s) ({ext_summary})")

        tasks = [(f, base_params) for f in all_files]
    else:
        tasks = []
        for p in all_params:
            filename = p.get("file", "")
            if not filename:
                print(f"  ⚠️  Skipping entry with no 'file' field: {p.get('style', '?')}")
                continue
            raw_path = find_raw_file(filename, raw_dir)
            if raw_path is None:
                print(f"  ⚠️  RAW file not found: {filename}")
                continue
            tasks.append((raw_path, p))

    if not tasks:
        print("❌ No matching RAW files found for any parameter set.")
        sys.exit(1)

    print(f"\n📷 Will process {len(tasks)} file(s) via RawTherapee")

    if args.dry_run:
        print(f"\n🔍 Dry run — files that would be graded:")
        for raw_path, p in tasks:
            print(f"  📸 {raw_path.name} [{raw_path.suffix.upper().lstrip('.')}] → style: {p.get('style', '?')}")
        sys.exit(0)

    if args.pp3_only:
        pp3_dir = Path(args.pp3_output).expanduser().resolve()
        print(f"\n📝 PP3-only mode: generating PP3 files to {pp3_dir}")
    else:
        print(f"\n⚙️  Grading: quality={quality}, workers={workers}")
        if uniform_dir:
            print(f"   Source: {Path(uniform_dir).expanduser().resolve()} (uniform)")
        elif raw_dir:
            print(f"   RAW dir: {raw_dir}")
        else:
            print(f"   RAW files: from absolute paths in params")
        print(f"   Output:  {output_dir}\n")

    output_dir.mkdir(parents=True, exist_ok=True)

    total_start = time.monotonic()
    success_count = 0
    skip_count = 0
    error_count = 0
    total = len(tasks)

    # RT is I/O-bound (external CLI), use ThreadPoolExecutor
    max_workers = min(workers, total) if workers > 0 else min(total, get_cpu_count())

    if max_workers <= 1 or total == 1:
        for i, (raw_path, p) in enumerate(tasks, 1):
            raw_name, success, message, elapsed = grade_single_file(
                raw_path,
                output_dir,
                p,
                cfg,
                quality,
                overwrite,
                args.dry_run,
                args.pp3_only,
                args.pp3_output if args.pp3_only else None,
                fast_export,
                raw_root=raw_dir,
            )
            print(f"  [{i}/{total}] {message} ({format_time(elapsed)})")
            if success:
                skip_count += 1 if "Skipped" in message else 0
                success_count += 0 if "Skipped" in message else 1
            else:
                error_count += 1
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    grade_single_file,
                    raw_path,
                    output_dir,
                    p,
                    cfg,
                    quality,
                    overwrite,
                    args.dry_run,
                    args.pp3_only,
                    args.pp3_output if args.pp3_only else None,
                    fast_export,
                    raw_root=raw_dir,
                ): raw_path
                for raw_path, p in tasks
            }
            done = 0
            for future in as_completed(futures):
                done += 1
                raw_name, success, message, elapsed = future.result()
                print(f"  [{done}/{total}] {message} ({format_time(elapsed)})")
                if success:
                    skip_count += 1 if "Skipped" in message else 0
                    success_count += 0 if "Skipped" in message else 1
                else:
                    error_count += 1

    total_elapsed = time.monotonic() - total_start
    print(f"\n{'─' * 55}")
    print(f"✅ Done in {format_time(total_elapsed)}")
    if args.pp3_only:
        print(f"   PP3 files generated: {success_count} in {Path(args.pp3_output).resolve()}")
    else:
        print(f"   Graded: {success_count}  |  Skipped: {skip_count}  |  Errors: {error_count}")
        print(f"   Output: {output_dir}")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
