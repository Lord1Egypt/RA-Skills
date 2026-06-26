#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import textwrap
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, Draw
except Exception:  # pragma: no cover
    Chem = None
    Draw = None

# Patent extractor API 与 patsight 使用同一套 OPS token
DEFAULT_PATENT_BASE_URL = os.getenv("PATSIGHT_BASE_URL", "https://patent.xinsight-ai.com/patent/api").strip().rstrip("/")
DEFAULT_OPS_TOKEN_URL = os.getenv("PATSIGHT_OPS_TOKEN_URL", "https://xops.xtalpi.com/api/v2/public/token")
DEFAULT_OPS_VERIFY_URL = os.getenv("PATSIGHT_OPS_VERIFY_URL", "https://xops.xtalpi.com/api/public/token/verify")

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

# =========================
# Dark tech style colors
# =========================
BG = (8, 12, 20)
PANEL = (14, 20, 34)
PANEL_2 = (18, 28, 46)
GRID = (38, 58, 94)
TEXT = (235, 244, 255)
TEXT_DIM = (150, 176, 210)
ACCENT = (64, 220, 255)
ACCENT_2 = (107, 123, 255)
WHITE = (255, 255, 255)


def parse_args() -> argparse.Namespace:
    # 向后兼容：若首个参数不是 patent，则视为 patent 的图片列表
    argv = sys.argv[1:]
    if argv and argv[0] != "patent" and not argv[0].startswith("-"):
        argv = ["patent"] + argv

    parser = argparse.ArgumentParser(
        description="Run OCSR on molecular images and generate a stylish PNG report (patent extractor API).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="API to use")
    p = subparsers.add_parser("patent", help="Patent extractor image/molecules API (requires token)")
    p.add_argument("images", nargs="+", help="Input molecular image files")
    p.add_argument(
        "--request-id",
        default=os.getenv("OPENCLAW_OCSR_REQUEST_ID"),
        help="Request ID (default: timestamp in ms)",
    )
    p.add_argument(
        "--base-url",
        default=DEFAULT_PATENT_BASE_URL,
        help="Patent API base URL (default: PATSIGHT_BASE_URL)",
    )
    p.add_argument(
        "--outdir",
        default="./ocsr_output",
        help="Output directory",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="HTTP timeout in seconds",
    )
    p.add_argument(
        "--panel-image-size",
        type=int,
        default=300,
        help="Displayed size for source image and molecule image block",
    )
    p.add_argument("--token", default=None, help="OPS token (or PATSIGHT_TOKEN)")
    p.add_argument("--account", default=None, help="OPS account (or PATSIGHT_ACCOUNT)")
    p.add_argument("--password", default=None, help="OPS password (or PATSIGHT_PASSWORD)")

    return parser.parse_args(argv)


def validate_images(image_paths: List[str]) -> List[Path]:
    valid: List[Path] = []
    for raw in image_paths:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        if not path.is_file():
            raise ValueError(f"Not a file: {path}")
        if path.suffix.lower() not in SUPPORTED_EXTS:
            raise ValueError(f"Unsupported image type: {path}")
        valid.append(path)
    return valid


def guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def _encode_credential_from_password(password: str) -> str:
    return base64.b64encode(password.encode("utf-8")).decode("utf-8")


def _get_ops_token(
    account: str,
    password: str,
    ops_token_url: str = DEFAULT_OPS_TOKEN_URL,
) -> Dict[str, Any]:
    if not account or not password:
        raise ValueError("Missing OPS account or password. Set PATSIGHT_ACCOUNT and PATSIGHT_PASSWORD.")
    credential = _encode_credential_from_password(password)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        ops_token_url,
        json={"account": account, "credential": credential},
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def _verify_ops_token(
    token: str,
    verify_url: str = DEFAULT_OPS_VERIFY_URL,
) -> Dict[str, Any]:
    if not token:
        raise ValueError("Empty token cannot be verified.")
    body_token = base64.b64encode(token.encode("utf-8")).decode("utf-8")
    resp = requests.post(
        verify_url,
        json={"token": body_token, "from": "login"},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_valid_token(
    token: Optional[str] = None,
    account: Optional[str] = None,
    password: Optional[str] = None,
    ops_token_url: str = DEFAULT_OPS_TOKEN_URL,
    verify_url: str = DEFAULT_OPS_VERIFY_URL,
) -> str:
    """获取可用于 Patent API 的有效 token，与 patsight client 一致：优先使用已有 token，否则用 account/password 换 token。"""
    token = token or os.environ.get("PATSIGHT_TOKEN")
    account = account or os.environ.get("PATSIGHT_ACCOUNT")
    password = password or os.environ.get("PATSIGHT_PASSWORD")

    if token:
        try:
            payload = _verify_ops_token(token, verify_url=verify_url)
            if payload.get("code") == 0:
                return token
        except Exception:
            pass

    if not account or not password:
        raise ValueError(
            "Valid token required. Set PATSIGHT_TOKEN, or PATSIGHT_ACCOUNT and PATSIGHT_PASSWORD."
        )
    token_payload = _get_ops_token(account, password, ops_token_url=ops_token_url)
    token_val = (token_payload.get("data") or {}).get("token")
    if not token_val:
        raise ValueError(f"Token not found in PatSight response: {token_payload}")
    return token_val


def post_patent_extractor_image_molecules(
    base_url: str,
    request_id: str,
    images: List[Path],
    timeout: int,
    token: Optional[str] = None,
    account: Optional[str] = None,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """POST 到 /patent/api/v1/u/extractor/image/molecules，必须传有效 token（与 patsight 一致获取）。"""
    if not base_url:
        raise ValueError("Missing base URL. Set --base-url or PATSIGHT_BASE_URL.")

    base_url = base_url.rstrip("/")
    if "patent.xinsight-ai.com" in base_url and "/patent/api" not in base_url:
        base_url = f"{base_url}/patent/api"

    auth_token = get_valid_token(token=token, account=account, password=password)
    url = f"{base_url}/v1/u/extractor/image/molecules"
    params = {"request_id": request_id}

    files = []
    handles = []
    try:
        for path in images:
            fh = open(path, "rb")
            handles.append(fh)
            files.append(("image", (path.name, fh, guess_mime(path))))
        files.append(("label", (None, "molvision")))

        response = requests.post(
            url,
            params=params,
            files=files,
            headers={
                "Accept": "application/json",
                "Authorization": auth_token,
            },
            timeout=timeout,
        )
    finally:
        for fh in handles:
            fh.close()

    if not response.ok:
        body_preview = response.text[:500] if response.text else "(empty)"
        raise ValueError(
            f"{response.status_code} {response.reason} for {response.url}\n"
            f"Response body: {body_preview}"
        )
    try:
        raw = response.json()
    except Exception as exc:
        raise ValueError(f"Response is not valid JSON: {exc}") from exc
    # Patent API 返回 {"code":1, "data":{"data":[...], "msg":"SUCCESS", ...}}，需转为与 OCSR 一致的 {"data": [...]}
    inner = (raw.get("data") or {}) if isinstance(raw.get("data"), dict) else {}
    records = inner.get("data") if isinstance(inner.get("data"), list) else raw.get("data")
    if isinstance(records, list):
        return {"data": records}
    return raw


def safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def compute_rdkit_properties(smiles: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "rdkit_ok": False,
        "formula": None,
        "exact_mw": None,
        "mol_wt": None,
        "logp": None,
        "tpsa": None,
        "hba": None,
        "hbd": None,
        "rotatable_bonds": None,
        "ring_count": None,
        "heavy_atom_count": None,
        "fraction_csp3": None,
    }

    if not smiles or Chem is None:
        return result

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return result

    result["rdkit_ok"] = True
    result["formula"] = rdMolDescriptors.CalcMolFormula(mol)
    result["exact_mw"] = round(Descriptors.ExactMolWt(mol), 4)
    result["mol_wt"] = round(Descriptors.MolWt(mol), 4)
    result["logp"] = round(Crippen.MolLogP(mol), 4)
    result["tpsa"] = round(rdMolDescriptors.CalcTPSA(mol), 4)
    result["hba"] = int(Lipinski.NumHAcceptors(mol))
    result["hbd"] = int(Lipinski.NumHDonors(mol))
    result["rotatable_bonds"] = int(Lipinski.NumRotatableBonds(mol))
    result["ring_count"] = int(rdMolDescriptors.CalcNumRings(mol))
    result["heavy_atom_count"] = int(mol.GetNumHeavyAtoms())
    result["fraction_csp3"] = round(rdMolDescriptors.CalcFractionCSP3(mol), 4)
    return result


def enrich_records(payload: Dict[str, Any], images: List[Path]) -> List[Dict[str, Any]]:
    records = payload.get("data", [])
    if not isinstance(records, list):
        raise ValueError("Payload field 'data' is not a list.")

    enriched: List[Dict[str, Any]] = []
    for i, (item, image_path) in enumerate(zip(records, images)):
        if not isinstance(item, dict):
            continue
        smiles = item.get("smiles") or ""
        props = compute_rdkit_properties(smiles)
        enriched.append(
            {
                **item,
                "score": safe_float(item.get("score")),
                "rdkit": props,
                "source_image": str(image_path),
            }
        )
    return enriched


def load_font(size: int, bold: bool = False):
    candidates = []
    if bold:
        candidates.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ])
    candidates.extend([
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ])
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def fit_image(img: Image.Image, max_w: int, max_h: int, background=(255, 255, 255)) -> Image.Image:
    img = img.convert("RGB")
    w, h = img.size
    if w <= 0 or h <= 0:
        return Image.new("RGB", (max_w, max_h), background)

    scale = min(max_w / w, max_h / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    resized = img.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGB", (max_w, max_h), background)
    x = (max_w - new_w) // 2
    y = (max_h - new_h) // 2
    canvas.paste(resized, (x, y))
    return canvas


def rounded_mask(size: Tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0], size[1]], radius=radius, fill=255)
    return mask


def paste_rounded(base: Image.Image, patch: Image.Image, xy: Tuple[int, int], radius: int) -> None:
    patch = patch.convert("RGBA")
    mask = rounded_mask(patch.size, radius)
    base.paste(patch, xy, mask)


def add_glow_rect(draw: ImageDraw.ImageDraw, box, radius=18, outline=ACCENT, fill=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def load_source_image(path: Optional[str], size: int) -> Image.Image:
    if not path:
        return Image.new("RGB", (size, size), (240, 244, 248))
    try:
        img = Image.open(path)
        return fit_image(img, size, size, background=(248, 250, 252))
    except Exception:
        return Image.new("RGB", (size, size), (240, 244, 248))


def placeholder_mol(size: int, text: str = "NO MOLECULE") -> Image.Image:
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    font = load_font(24, bold=True)
    sub = load_font(16)

    draw.rounded_rectangle([8, 8, size - 8, size - 8], radius=18, outline=(220, 230, 240), width=2)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((size - tw) / 2, size / 2 - th), text, font=font, fill=(60, 70, 90))
    draw.text((size / 2 - 52, size / 2 + 18), "SMILES invalid", font=sub, fill=(120, 130, 150))
    return img


def smiles_to_mol_image(smiles: str, size: int) -> Image.Image:
    if not smiles or Chem is None or Draw is None:
        return placeholder_mol(size)

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return placeholder_mol(size)

    try:
        img = Draw.MolToImage(mol, size=(size, size))
        return img.convert("RGB")
    except Exception:
        return placeholder_mol(size, "DRAW FAILED")
def mol_from_sdf_str(sdf_str: str):
    if not sdf_str or Chem is None:
        return None
    try:
        mol = Chem.MolFromMolBlock(sdf_str, sanitize=True, removeHs=False)
        return mol
    except Exception:
        return None


def smiles_to_mol_image(smiles: str, sdf_str: str, size: int) -> Image.Image:
    if Chem is None or Draw is None:
        return placeholder_mol(size)

    mol = None

    # 1️⃣ 优先使用 SDF
    if sdf_str:
        mol = mol_from_sdf_str(sdf_str)

    # 2️⃣ fallback 到 SMILES
    if mol is None and smiles:
        try:
            mol = Chem.MolFromSmiles(smiles)
        except Exception:
            mol = None

    if mol is None:
        return placeholder_mol(size)

    try:
        img = Draw.MolToImage(
            mol,
            size=(size, size),
            kekulize=True,
            wedgeBonds=True
        )
        return img.convert("RGB")
    except Exception:
        return placeholder_mol(size, "DRAW FAILED")

def draw_gradient_background(canvas: Image.Image) -> None:
    w, h = canvas.size
    px = canvas.load()
    for y in range(h):
        for x in range(w):
            nx = x / max(1, w - 1)
            ny = y / max(1, h - 1)
            r = int(8 + 8 * ny + 6 * nx)
            g = int(12 + 18 * ny + 10 * nx)
            b = int(20 + 38 * ny + 30 * (1 - nx * 0.4))
            px[x, y] = (r, g, b)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([w - 380, -80, w + 120, 420], fill=(64, 220, 255, 28))
    d.ellipse([-160, h - 320, 360, h + 120], fill=(107, 123, 255, 30))
    d.ellipse([w // 2 - 180, 30, w // 2 + 180, 390], fill=(80, 255, 200, 12))
    overlay = overlay.filter(ImageFilter.GaussianBlur(50))
    canvas.alpha_composite(overlay)


def wrap_text(text: str, width: int) -> List[str]:
    if not text:
        return []
    out: List[str] = []
    for part in text.splitlines():
        if not part.strip():
            out.append("")
            continue
        out.extend(textwrap.wrap(part, width=width, break_long_words=True, break_on_hyphens=False))
    return out


def metric_rows(rec: Dict[str, Any]) -> List[Tuple[str, str]]:
    rd = rec.get("rdkit", {})
    return [
        ("Formula", str(rd.get("formula") or "-")),
        ("Exact MW", str(rd.get("exact_mw") or "-")),
        ("MolWt", str(rd.get("mol_wt") or "-")),
        ("LogP", str(rd.get("logp") or "-")),
        ("TPSA", str(rd.get("tpsa") or "-")),
        ("HBA / HBD", f"{rd.get('hba') if rd.get('hba') is not None else '-'} / {rd.get('hbd') if rd.get('hbd') is not None else '-'}"),
        ("RotBonds", str(rd.get("rotatable_bonds") or "-")),
        ("Rings", str(rd.get("ring_count") or "-")),
        ("HeavyAtoms", str(rd.get("heavy_atom_count") or "-")),
        ("FractionCSP3", str(rd.get("fraction_csp3") or "-")),
    ]


def draw_panel(draw: ImageDraw.ImageDraw, box, title: str, title_font, fill=PANEL, outline=GRID):
    add_glow_rect(draw, box, radius=20, fill=fill, outline=outline, width=2)
    x1, y1, x2, y2 = box
    draw.text((x1 + 16, y1 + 12), title, font=title_font, fill=TEXT)
    draw.line((x1 + 16, y1 + 48, x2 - 16, y1 + 48), fill=GRID, width=2)


def draw_property_grid(img: Image.Image, box, rec: Dict[str, Any], title_font, label_font, value_font):
    draw = ImageDraw.Draw(img)
    draw_panel(draw, box, "Molecular Properties", title_font, fill=PANEL_2, outline=ACCENT_2)
    x1, y1, x2, y2 = box

    rows = metric_rows(rec)
    col1_w = 180
    start_y = y1 + 66
    row_h = 34

    for i, (k, v) in enumerate(rows):
        yy = start_y + i * row_h
        if yy + row_h > y2 - 10:
            break

        if i % 2 == 0:
            draw.rounded_rectangle([x1 + 12, yy - 2, x2 - 12, yy + row_h - 2], radius=10, fill=(22, 34, 58))

        draw.text((x1 + 22, yy + 3), k, font=label_font, fill=TEXT_DIM)
        draw.text((x1 + 22 + col1_w, yy + 3), v, font=value_font, fill=TEXT)


def build_report_image(payload: Dict[str, Any], records: List[Dict[str, Any]], panel_image_size: int = 300) -> Image.Image:
    title_font = load_font(22, bold=True)
    header_font = load_font(20, bold=True)
    label_font = load_font(17)
    value_font = load_font(18)

    margin = 28
    gap = 20
    section_gap = 24

    left_w = panel_image_size + 32
    mid_w = panel_image_size + 32
    right_w = 470
    total_w = margin * 2 + left_w + gap + mid_w + gap + right_w

    card_h = panel_image_size + 160
    top_h = 36

    total_h = top_h + len(records) * (card_h + section_gap) + margin
    canvas = Image.new("RGBA", (total_w, total_h), BG + (255,))
    draw_gradient_background(canvas)

    start_y = 18
    for idx, rec in enumerate(records):
        card_y1 = start_y + idx * (card_h + section_gap)
        card_y2 = card_y1 + card_h
        card_box = (margin, card_y1, total_w - margin, card_y2)

        glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.rounded_rectangle(card_box, radius=26, fill=(30, 90, 140, 40))
        glow = glow.filter(ImageFilter.GaussianBlur(18))
        canvas.alpha_composite(glow)

        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(card_box, radius=26, fill=(12, 18, 30, 238), outline=GRID, width=2)

        smiles = str(rec.get("smiles") or "N/A")
        title_lines = wrap_text(smiles, width=70)
        title_y = card_y1 + 14
        for line in title_lines[:2]:
            draw.text((margin + 18, title_y), line, font=title_font, fill=ACCENT)
            title_y += 28

        left_box = (margin + 16, card_y1 + 72, margin + 16 + left_w, card_y2 - 16)
        mid_box = (left_box[2] + gap, card_y1 + 72, left_box[2] + gap + mid_w, card_y2 - 16)
        right_box = (mid_box[2] + gap, card_y1 + 72, total_w - margin - 16, card_y2 - 16)

        draw_panel(draw, left_box, "Original Image", header_font, fill=PANEL, outline=ACCENT_2)
        draw_panel(draw, mid_box, "Recognized Molecule", header_font, fill=PANEL, outline=ACCENT)
        draw_property_grid(canvas, right_box, rec, header_font, label_font, value_font)

        src_img = load_source_image(rec.get("source_image"), panel_image_size)
        mol_img = smiles_to_mol_image(rec.get("smiles") or "", rec.get("sdf_str") or "", panel_image_size)

        src_patch = fit_image(src_img, panel_image_size, panel_image_size, background=(246, 249, 252))
        mol_patch = fit_image(mol_img, panel_image_size, panel_image_size, background=(255, 255, 255))

        paste_rounded(canvas, src_patch, (left_box[0] + 16, left_box[1] + 62), 16)
        paste_rounded(canvas, mol_patch, (mid_box[0] + 16, mid_box[1] + 62), 16)

    return canvas.convert("RGB")


def write_json(path: Path, payload: Dict[str, Any], enriched: List[Dict[str, Any]]) -> None:
    wrapped = {
        "raw_response": payload,
        "enriched_data": enriched,
    }
    path.write_text(json.dumps(wrapped, ensure_ascii=False, indent=2), encoding="utf-8")


def write_png(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", quality=95)


def main() -> int:
    args = parse_args()
    if not getattr(args, "images", None) or not args.images:
        print("Usage: run_ocsr.py [patent] IMAGES... [--request-id ID] [--base-url URL]", file=sys.stderr)
        return 2
    images = validate_images(args.images)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    request_id = getattr(args, "request_id", None) or os.getenv("OPENCLAW_OCSR_REQUEST_ID") or str(int(time.time() * 1000))
    if not request_id or not str(request_id).strip():
        request_id = str(int(time.time() * 1000))
    payload = post_patent_extractor_image_molecules(
        base_url=args.base_url,
        request_id=str(request_id).strip(),
        images=images,
        timeout=args.timeout,
        token=getattr(args, "token", None),
        account=getattr(args, "account", None),
        password=getattr(args, "password", None),
    )

    records = enrich_records(payload, images)
    ts = int(time.time())
    json_path = outdir / f"ocsr_result_{ts}.json"
    png_path = outdir / f"ocsr_dashboard_{ts}.png"

    write_json(json_path, payload, records)
    report_img = build_report_image(
        payload=payload,
        records=records,
        panel_image_size=args.panel_image_size,
    )
    write_png(png_path, report_img)

    print(json.dumps(
        {
            "status": "ok",
            "command": "patent",
            "input_images": [str(p) for p in images],
            "recognized_records": len(records),
            "json_output": str(json_path.resolve()),
            "ocsr_dashboard_output": str(png_path.resolve()),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())