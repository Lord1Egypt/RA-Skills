#!/usr/bin/env python3
"""pptx_to_pdf.py — Convert .pptx to .pdf via LibreOffice headless.

Usage: python3 pptx_to_pdf.py input.pptx [output.pdf]
"""
import subprocess, sys, os, shutil, tempfile

def convert(pptx_path, pdf_path=None):
    if not os.path.isfile(pptx_path):
        print(f"❌ File not found: {pptx_path}", file=sys.stderr)
        sys.exit(1)

    # Find soffice
    soffice = shutil.which("soffice")
    if not soffice:
        # Try common sandbox/skill paths
        for p in [
            os.path.expanduser("~/.openclaw/skills/pptx/scripts/office/soffice.py"),
        ]:
            if os.path.isfile(p):
                soffice = p
                break

    if not soffice:
        print("❌ LibreOffice (soffice) not found.", file=sys.stderr)
        sys.exit(1)

    # Convert to temp dir first to handle soffice naming
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", tmpdir, pptx_path]
        if soffice.endswith(".py"):
            cmd = [sys.executable] + cmd

        print(f"🔄 Converting: {os.path.basename(pptx_path)} → PDF")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f"❌ Conversion failed:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        # Find output PDF
        base = os.path.splitext(os.path.basename(pptx_path))[0]
        tmp_pdf = os.path.join(tmpdir, base + ".pdf")

        if not os.path.isfile(tmp_pdf):
            # Try to find any PDF
            pdfs = [f for f in os.listdir(tmpdir) if f.endswith(".pdf")]
            if pdfs:
                tmp_pdf = os.path.join(tmpdir, pdfs[0])
            else:
                print("❌ No PDF output found.", file=sys.stderr)
                sys.exit(1)

        # Move to final location
        if pdf_path is None:
            pdf_path = os.path.splitext(pptx_path)[0] + ".pdf"

        os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)
        shutil.move(tmp_pdf, pdf_path)

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"✅ Output: {pdf_path} ({size_kb:.0f} KB)")
    return pdf_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pptx_to_pdf.py input.pptx [output.pdf]")
        sys.exit(1)
    pptx_path = sys.argv[1]
    pdf_path = sys.argv[2] if len(sys.argv) > 2 else None
    convert(pptx_path, pdf_path)
