# KB Framework – Installation

## Voraussetzungen

- Python 3.10+
- Git
- Optional: Tesseract OCR (`tesseract-ocr` + Sprachpakete)

## Installation

### 1. Repository klonen

```bash
git clone <repo-url> ~/projects/kb-framework
```

### 2. Symlink erstellen

```bash
ln -s ~/projects/kb-framework ~/.openclaw/kb
```

Der Symlink sorgt dafür, dass das Repo die einzige Source of Truth ist.
Keine Kopie nötig – Änderungen am Repo sind sofort aktiv.

### 3. Virtual Environment erstellen

```bash
python3 -m venv ~/.openclaw/kb/venv
```

Falls `ensurepip` nicht verfügbar (Debian/Ubuntu):

```bash
sudo apt install python3.12-venv
# oder:
python3 -m venv --without-pipe ~/.openclaw/kb/venv
~/.openclaw/kb/venv/bin/python -m ensurepip
# oder: curl -sS https://bootstrap.pypa.io/get-pip.py | ~/.openclaw/kb/venv/bin/python
```

### 4. Dependencies installieren

```bash
~/.openclaw/kb/venv/bin/pip install -r ~/.openclaw/kb/requirements.txt
```

Optional:

```bash
~/.openclaw/kb/venv/bin/pip install -r ~/.openclaw/kb/requirements-transformers.txt
~/.openclaw/kb/venv/bin/pip install -r ~/.openclaw/kb/requirements-dev.txt
```

### 5. Konfiguration

```bash
cp ~/.openclaw/kb/kb/config.py.template ~/.openclaw/kb/kb/config.py
# config.py anpassen (Pfade, Engine-Config etc.)
```

### 6. Testen

```bash
bash ~/.openclaw/kb/kb.sh --help
bash ~/.openclaw/kb/kb.sh --version
```

## Architektur

```
~/.openclaw/kb/              → Symlink → ~/projects/kb-framework/
├── venv/                    ← Virtual Environment (nicht in Git!)
├── library/                 ← User Data (nicht in Git!)
│   ├── biblio.db
│   ├── chroma_db/
│   ├── projektplanung/
│   ├── audit/
│   ├── llm/
│   └── biblio/
├── chroma_db/               ← Vektor-Datenbank (nicht in Git!)
├── knowledge.db             ← SQLite DB (nicht in Git!)
├── kb/                      ← Python Package
├── kb.sh                    ← CLI Wrapper (nutzt venv)
├── requirements.txt
└── install.sh               ← Setup-Script (Tesseract, Deps, Dirs)

~/projects/kb-framework/     ← Git Repo (Source of Truth)
```

## CLI Wrapper

`kb.sh` nutzt automatisch das venv unter `KB_DIR/venv/` und setzt `PYTHONPATH`.

```bash
# Direkt
bash ~/.openclaw/kb/kb.sh sync --stats

# Alias in .bashrc
alias kb='bash ~/.openclaw/kb/kb.sh'
kb sync --stats
```

## Update

Da der Symlink direkt auf das Repo zeigt:

```bash
cd ~/projects/kb-framework
git pull
# Bei neuen Dependencies:
~/.openclaw/kb/venv/bin/pip install -r requirements.txt
```

## Rollback

Falls etwas schief geht:

```bash
# Symlink entfernen und Backup zurückspielen
rm ~/.openclaw/kb
cp -r <backup-pfad> ~/.openclaw/kb
```

## .gitignore

Die `.gitignore` schließt automatisch aus:
- `*.db` – Datenbank-Dateien
- `chroma_db/` – Vektor-Datenbank
- `library/biblio.db`, `library/indexes/`, `library/chroma_db/` – User Data
- `venv/` – Virtual Environment
- `__pycache__/`, `*.pyc` – Python Cache
- `config_local.py` – Lokale Konfiguration