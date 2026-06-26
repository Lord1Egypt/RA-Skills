#!/usr/bin/env python3
"""
wps_convert.py — Convert PPTX to PNG/PDF using WPS Office via pywpsrpc.

Follows the official pywpsrpc example pattern:
  https://github.com/timxx/pywpsrpc/blob/master/examples/rpcwppapi/wpp_convert.py

WPS rendering is significantly closer to MS PowerPoint than LibreOffice,
making it the primary cross-platform validation tool.

Requirements:
  - WPS Office 11.1.0.x or 12.x (check pywpsrpc compatibility)
  - pywpsrpc >= 2.3 (pip install pywpsrpc)
  - xvfb for headless operation
  - libqt5xml5, libqt5gui5 system packages

Usage:
    xvfb-run --auto-servernum --server-args="-screen 0 1920x1080x24" \
        python3 wps_convert.py <input.pptx> <output_dir> [png|pdf|both]

Experience log (DO NOT DELETE — accumulated lessons):
  E1: pywpsrpc REQUIRES QtApp(sys.argv) to initialize the Qt event loop.
      Without it, createWppRpcInstance returns S_OK but getWppApplication
      returns None. This is the #1 cause of "RPC connected but no app".
  E2: Do NOT manually launch wpp binary and then connect — let pywpsrpc
      manage the WPS process via its RPC mechanism.
  E3: Use WithWindow=msoFalse when opening presentations for export.
  E4: After export, kill the WPS process by PID (rpc.getProcessPid).
      app.Quit() alone is unreliable and may hang.
  E5: Segfault on exit is normal (pywpsrpc cleanup). Does not affect output.
  E6: EULA + multi-component mode must be pre-configured in Office.conf.
  E7: WPS CLI --convert-to pdf hangs — do NOT rely on CLI, use RPC only.
  E8: SaveAs(dir, 18) = ppSaveAsPNG — exports all slides as Slide1.png etc.
  E9: SaveAs(path, 32) = ppSaveAsPDF.
"""

import sys
import os
import subprocess

PP_SAVE_AS_PNG = 18
PP_SAVE_AS_PDF = 32


def ensure_wps_config():
    """Ensure WPS EULA accepted and multi-component mode enabled (E6)."""
    conf_dir = os.path.expanduser("~/.config/Kingsoft")
    conf_path = os.path.join(conf_dir, "Office.conf")
    os.makedirs(conf_dir, exist_ok=True)

    needed = {
        "common\\AcceptedEULA": "true",
        "wpsoffice\\Application%20Settings\\AppComponentMode": "prome_independ",
        "wpsoffice\\Application%20Settings\\AppComponentModeInstall": "prome_independ",
    }

    existing = ""
    if os.path.exists(conf_path):
        with open(conf_path, "r") as f:
            existing = f.read()

    missing = [f"{k}={v}" for k, v in needed.items() if k not in existing]
    if missing:
        with open(conf_path, "a") as f:
            if "[common]" not in existing:
                f.write("\n[common]\n")
            f.write("\n".join(missing) + "\n")


def export_png(pres, output_dir):
    """Export all slides as PNG using SaveAs (E8)."""
    os.makedirs(output_dir, exist_ok=True)
    hr = pres.SaveAs(output_dir, PP_SAVE_AS_PNG)
    if hr == 0:
        print(f"[WPS] PNG export OK -> {output_dir}")
        return True

    print(f"[WPS] PNG batch failed (hr={hr}), trying per-slide fallback...")
    slide_count = pres.Slides.Count
    ok = True
    for i in range(1, slide_count + 1):
        png_path = os.path.join(output_dir, f"Slide{i}.png")
        try:
            hr2 = pres.Slides(i).Export(png_path, "PNG", 1920, 1080)
            if hr2 != 0:
                print(f"[WPS]   Slide {i}: FAIL hr={hr2}")
                ok = False
        except Exception as e:
            print(f"[WPS]   Slide {i}: {e}")
            ok = False
    return ok


def export_pdf(pres, pdf_path):
    """Export presentation as PDF (E9)."""
    hr = pres.SaveAs(pdf_path, PP_SAVE_AS_PDF)
    if hr == 0:
        print(f"[WPS] PDF OK -> {pdf_path}")
        return True
    print(f"[WPS] PDF failed: hr={hr}")
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: wps_convert.py <input.pptx> <output_dir> [png|pdf|both]")
        sys.exit(1)

    input_path = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    fmt = sys.argv[3] if len(sys.argv) > 3 else "png"

    if not os.path.exists(input_path):
        print(f"[ERR] Not found: {input_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    ensure_wps_config()

    print(f"[WPS] Input:  {input_path}")
    print(f"[WPS] Output: {output_dir}")
    print(f"[WPS] Format: {fmt}")

    from pywpsrpc.rpcwppapi import createWppRpcInstance, wppapi
    from pywpsrpc.common import S_OK, QtApp

    qApp = QtApp(sys.argv)  # E1: REQUIRED for RPC event loop

    hr, rpc = createWppRpcInstance()
    if hr != S_OK:
        print(f"[ERR] createWppRpcInstance failed: hr={hex(hr & 0xFFFFFFFF)}")
        sys.exit(1)

    hr, app = rpc.getWppApplication()
    if hr != S_OK or app is None:
        print(f"[ERR] getWppApplication failed: hr={hex(hr & 0xFFFFFFFF)}")
        sys.exit(1)

    wps_pid = None
    hr, wps_pid = rpc.getProcessPid()
    if hr == S_OK:
        print(f"[WPS] Connected, WPS PID={wps_pid}")
    else:
        print("[WPS] Connected (PID unknown)")

    try:
        hr, pres = app.Presentations.Open(
            input_path,
            ReadOnly=True,
            WithWindow=wppapi.MsoTriState.msoFalse,  # E3
        )
        if hr != S_OK:
            print(f"[ERR] Open failed: hr={hex(hr & 0xFFFFFFFF)}")
            sys.exit(1)

        slide_count = pres.Slides.Count
        print(f"[WPS] Opened {slide_count} slides")

        if fmt in ("png", "both"):
            png_dir = os.path.join(output_dir, "slides")
            export_png(pres, png_dir)

        if fmt in ("pdf", "both"):
            pdf_path = os.path.join(output_dir, "output.pdf")
            export_pdf(pres, pdf_path)

        pres.Close()
        print("[WPS] Done")

    except Exception as e:
        print(f"[ERR] {e}")
    finally:
        try:
            app.Quit()
        except Exception:
            pass
        if wps_pid is not None:  # E4: kill by PID for reliable cleanup
            subprocess.call(f"kill -9 {wps_pid}", shell=True)


if __name__ == "__main__":
    main()
