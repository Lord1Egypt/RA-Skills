from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.utils import ImageReader

from ..core.overlay import apply_overlay
from ..core.ranges import parse_page_ranges


def sign_visible(
    input_path: Path,
    output_path: Path,
    *,
    text: str | None = None,
    image: Path | None = None,
    x: float = 50,
    y: float = 50,
    width: float = 200,
    height: float = 80,
    pages: str | None = None,
) -> None:
    if not text and not image:
        raise ValueError("Provide --text or --image for visible signature")

    reader = PdfReader(str(input_path))
    total = len(reader.pages)
    target_pages = set(parse_page_ranges(pages, total))

    def _draw(c, page_num: int, page_width: float, page_height: float) -> None:
        if (page_num - 1) not in target_pages:
            return
        if image:
            img = ImageReader(str(image))
            c.drawImage(img, x, y, width, height, preserveAspectRatio=True)
        if text:
            c.setFont("Helvetica", 12)
            c.drawString(x, y + height + 4, text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    apply_overlay(str(input_path), str(output_path), _draw)


def sign_digital(
    input_path: Path,
    output_path: Path,
    *,
    cert_path: Path,
    key_path: Path,
    key_password: str | None = None,
) -> None:
    try:
        from pyhanko.sign import signers
        from pyhanko.sign.fields import SigFieldSpec
        from pyhanko.sign.general import load_cert_from_pemder
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("pyhanko is required. Install with: pip install 'pdfagent[sign]'") from exc

    with open(cert_path, "rb") as cert_f, open(key_path, "rb") as key_f:
        signer = signers.SimpleSigner(
            signing_cert=load_cert_from_pemder(cert_f.read()),
            signing_key=key_f.read(),
            passphrase=key_password.encode() if key_password else None,
        )

    with open(input_path, "rb") as inf:
        pdf_writer = signers.PdfSigner(
            signers.PdfSignatureMetadata(field_name="Signature1"),
            signer=signer,
        )
        with open(output_path, "wb") as outf:
            pdf_writer.sign_pdf(inf, output=outf)
