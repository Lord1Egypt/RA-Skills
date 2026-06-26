#!/usr/bin/env python3
import importlib
import shutil
import subprocess
import sys

PYTHON_MODULES = [
    ("pypdf", "PDF embedded text extraction"),
    ("docx", "DOCX extraction via python-docx"),
    ("openpyxl", "XLSX extraction"),
    ("pptx", "PPTX extraction via python-pptx"),
]

SYSTEM_TOOLS = [
    ("pdftoppm", "PDF rasterization for OCR (from poppler-utils)"),
    ("tesseract", "OCR engine"),
    ("libreoffice", "Legacy Office conversion (.doc/.xls/.ppt)"),
    ("antiword", "Legacy .doc extraction fallback"),
    ("catdoc", "Legacy .doc extraction fallback"),
]

RECOMMENDED_LANGS = ["chi_sim", "eng"]


def check_python_modules():
    print("[Python modules]")
    missing = []
    for mod, desc in PYTHON_MODULES:
        try:
            importlib.import_module(mod)
            print(f"OK   {mod:<10} - {desc}")
        except Exception as e:
            print(f"MISS {mod:<10} - {desc} ({e})")
            missing.append(mod)
    print()
    return missing


def check_system_tools():
    print("[System tools]")
    missing = []
    for tool, desc in SYSTEM_TOOLS:
        path = shutil.which(tool)
        if path:
            print(f"OK   {tool:<10} - {desc} [{path}]")
        else:
            print(f"MISS {tool:<10} - {desc}")
            missing.append(tool)
    print()
    return missing


def check_tesseract_langs():
    print("[Tesseract languages]")
    if not shutil.which("tesseract"):
        print("SKIP tesseract not installed")
        print()
        return RECOMMENDED_LANGS[:]

    try:
        r = subprocess.run(
            ["tesseract", "--list-langs"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except Exception as e:
        print(f"ERROR unable to query tesseract languages: {e}")
        print()
        return RECOMMENDED_LANGS[:]

    lines = [x.strip() for x in (r.stdout or "").splitlines() if x.strip()]
    if lines and lines[0].lower().startswith("list of available"):
        lines = lines[1:]
    langs = set(lines)

    missing = []
    for lang in RECOMMENDED_LANGS:
        if lang in langs:
            print(f"OK   {lang}")
        else:
            print(f"MISS {lang}")
            missing.append(lang)
    print()
    return missing


def main():
    py_missing = check_python_modules()
    tool_missing = check_system_tools()
    lang_missing = check_tesseract_langs()

    print("[Summary]")
    if not py_missing and not tool_missing and not lang_missing:
        print("All recommended dependencies are available.")
        sys.exit(0)

    if py_missing:
        print("Missing Python modules:", ", ".join(py_missing))
    if tool_missing:
        print("Missing system tools:", ", ".join(tool_missing))
    if lang_missing:
        print("Missing OCR languages:", ", ".join(lang_missing))

    print("\nMinimum modern-document support requires Python modules only.")
    print("Best real-world coverage also needs pdftoppm, tesseract, libreoffice, antiword/catdoc, and chi_sim OCR.")
    sys.exit(1)


if __name__ == "__main__":
    main()
