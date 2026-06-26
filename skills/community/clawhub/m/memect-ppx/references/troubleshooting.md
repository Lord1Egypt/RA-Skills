# Troubleshooting

## Python Version

- Require Python `>= 3.12`.
- Check the active interpreter with:

```bash
python3 --version
```

- If the system default is older than 3.12, create the virtual environment with an explicit interpreter such as `python3.12`.

## Recommended Environment

- Prefer a dedicated virtual environment for PPX.
- Example setup:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install memect-ppx
pip install onnxruntime
pip install opencv-contrib-python
```

- If `python3.12` is unavailable, use any Python interpreter version `>= 3.12`.

## `ppx` Not Found

- Install the CLI:

```bash
source .venv/bin/activate
pip install memect-ppx
pip install onnxruntime
pip install opencv-contrib-python
```

- On headless Linux, prefer:

```bash
pip install opencv-python-headless
```

## Common Runtime Issues

- `ImportError: libGL.so.1`
  Install `opencv-python-headless` or the system `libgl1` package.

- `onnxruntime` and `onnxruntime-gpu` conflict
  Keep only one of them installed in the active environment.

- CUDA backend not available on macOS
  Use CPU mode or a remote/local service backend instead.

## Output Validation

After a successful parse, verify that the output directory contains:

- `doc.md`
- `doc.json`
- `pages/`

If one of these is missing, treat the run as partial and report that explicitly.
