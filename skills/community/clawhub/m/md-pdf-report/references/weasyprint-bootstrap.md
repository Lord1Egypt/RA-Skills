# weasyprint C Library Bootstrap Recipe

## Problem

`weasyprint` Python package installs cleanly via pip, but it depends on
several C libraries (pango, cairo, gobject) that macOS does not ship by default.
On first import you get:

```
WeasyPrint could not import some external libraries.
cannot load library 'libgobject-2.0-0': dlopen(...): tried: 'libgobject-2.0-0' (no such file), ...
```

## One-time Setup

```bash
# 1. Install pango (pulls in cairo, glib, etc. as deps)
brew install pango

# 2. Verify brew installed the libs
ls /opt/homebrew/lib/libpango-1.0.dylib
ls /opt/homebrew/lib/libgobject-2.0.dylib
```

## The DYLD Trick

`weasyprint` uses `ctypes` to load `libgobject-2.0`, which is in
`/opt/homebrew/lib`. macOS's dyld doesn't search there by default. The fix is
to set `DYLD_FALLBACK_LIBRARY_PATH`:

```bash
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
```

This must be set **before** Python starts (exporting it inside Python won't
work because dyld has already cached its library search paths).

## The Bootstrap Pattern (auto-set on import)

The `md2pdf.py` module handles this automatically:

```python
def bootstrap_macos():
    if platform.system() != 'Darwin':
        return False
    if os.environ.get('DYLD_FALLBACK_LIBRARY_PATH'):
        return False
    if os.path.exists('/opt/homebrew/lib'):
        os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/opt/homebrew/lib'
    return True

if not os.environ.get('MD2PDF_NO_BOOTSTRAP'):
    bootstrap_macos()
```

To disable (e.g. for testing on Linux):
```bash
export MD2PDF_NO_BOOTSTRAP=1
```

## Manual Verification

After setup, run this to confirm weasyprint works:

```python
from weasyprint import HTML
HTML(string='<html><body><h1>测试中文</h1></body></html>').write_pdf('/tmp/test.pdf')
```

If it produces a valid PDF, you're set. If it still fails, check:
1. `which brew` — Homebrew installed?
2. `brew list pango` — pango installed?
3. `echo $DYLD_FALLBACK_LIBRARY_PATH` — env var set?
4. `ls /opt/homebrew/lib/libgobject-2.0.dylib` — file exists?

## Linux Alternative

On Linux (Debian/Ubuntu):
```bash
sudo apt install libpango-1.0-0 libpangoft2-1.0-0
```
No env var needed — libraries are in standard paths.

## Windows Alternative

Windows is not officially supported by weasyprint. Consider:
- Use WSL with the Linux instructions
- Or use reportlab directly (no C library dependencies, but more verbose code)
