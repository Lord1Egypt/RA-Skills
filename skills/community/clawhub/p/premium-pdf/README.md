# premium-pdf

OpenClaw skill to generate enterprise-style PDFs from markdown input, with a built-in de-AI humanization pipeline.

---

*Skill OpenClaw per generare PDF enterprise-style da input markdown, con pipeline di de-AI humanization integrata.*

---

## Installation

### Via ClawHub (recommended)

```bash
clawhub install premium-pdf
```

If you don't have `clawhub` installed:

```bash
npm install -g clawhub
clawhub install premium-pdf
```

### Manual (from this repository)

1. Copy the `premium-pdf/` folder into the `skills/` directory of your OpenClaw project
2. Install the Python dependencies:

```bash
pip install -r skills/premium-pdf/requirements.txt
```

---

*## Installazione*

*### Via ClawHub (consigliato)*

```bash
clawhub install premium-pdf
```

*Se non hai `clawhub` installato:*

```bash
npm install -g clawhub
clawhub install premium-pdf
```

*### Manuale (da questo repository)*

*1. Copia la cartella `premium-pdf/` nella directory `skills/` del tuo progetto OpenClaw*
*2. Installa le dipendenze Python:*

```bash
pip install -r skills/premium-pdf/requirements.txt
```

---

## System Requirements

- Python 3.8+
- macOS or Linux (Windows not supported)

*## Requisiti di sistema*

*- Python 3.8+*
*- macOS o Linux (Windows non supportato)*

---

## Usage

### Direct markdown string

```bash
python3 premium-pdf/generate_pdf.py \
  --input "# Title\n\nDocument body..." \
  --output document.pdf \
  --title "Document Title"
```

### Markdown file

```bash
python3 premium-pdf/generate_pdf.py \
  --input path/to/file.md \
  --output output.pdf \
  --title "Optional Title"
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--input` | Yes | Markdown string or path to a `.md` file |
| `--output` | Yes | Output PDF file path |
| `--title` | No | Document title (default: output filename) |

---

*## Utilizzo*

*### Testo markdown diretto*

```bash
python3 premium-pdf/generate_pdf.py \
  --input "# Titolo\n\nTesto del documento..." \
  --output documento.pdf \
  --title "Titolo Documento"
```

*### File markdown*

```bash
python3 premium-pdf/generate_pdf.py \
  --input path/to/file.md \
  --output output.pdf \
  --title "Titolo Opzionale"
```

*### Argomenti*

| Argomento | Obbligatorio | Descrizione |
|-----------|-------------|-------------|
| `--input` | Sì | Stringa markdown o percorso a file `.md` |
| `--output` | Sì | Percorso del PDF generato |
| `--title` | No | Titolo del documento (default: nome file output) |

---

## Output

The command prints the absolute path of the generated PDF:

```
PDF generated successfully: /absolute/path/to/output.pdf
```

*## Output*

*Il comando stampa il percorso assoluto del PDF generato:*

```
PDF generated successfully: /percorso/assoluto/output.pdf
```

---

## Design

- Page format: A4
- Margins: 1 inch on all sides
- Color palette: dark navy (`#1A2B4A`), white, gold (`#C9A84C`)
- Header: document title on navy background with gold rule
- Footer: centered page number with navy rule
- Typography: Helvetica — H1 28pt, H2 20pt, H3 16pt, H4 13pt, body 11pt

*## Design*

*- Formato pagina: A4*
*- Margini: 1 inch su tutti i lati*
*- Palette colori: navy scuro (`#1A2B4A`), bianco, oro (`#C9A84C`)*
*- Header: titolo documento su sfondo navy con riga oro*
*- Footer: numero pagina centrato con riga navy*
*- Tipografia: Helvetica — H1 28pt, H2 20pt, H3 16pt, H4 13pt, body 11pt*

---

## De-AI Humanization

Before rendering, the text is processed to remove patterns typical of LLM-generated content:

- Transition phrases (`Furthermore,`, `In conclusion,`, etc.)
- Overused verbs (`utilize` → `use`, `leverage` → `use`, `implement` → `build`)
- Em dashes and en dashes replaced with commas or hyphens
- Ellipses normalized

*## De-AI Humanization*

*Prima del rendering, il testo viene processato per rimuovere pattern tipici dei testi generati da LLM:*

*- Frasi di transizione (`Furthermore,`, `In conclusion,`, ecc.)*
*- Verbi abusati (`utilize` → `use`, `leverage` → `use`, `implement` → `build`)*
*- Em dash e en dash sostituiti con virgola o trattino*
*- Puntini di sospensione normalizzati*

---

## Supported Markdown Elements

- Headings H1–H4
- Paragraphs with justified text
- **Bold**, *italic*, `inline code`
- Code blocks (` ``` `)
- Bullet and numbered lists (including nested)
- Blockquotes (`>`)
- Horizontal rules (`---`)

*## Elementi markdown supportati*

*- Heading H1–H4*
*- Paragrafi con testo giustificato*
*- **Grassetto**, *corsivo*, `codice inline`*
*- Blocchi di codice (\`\`\`)*
*- Liste puntate e numerate (anche annidate)*
*- Citazioni (`>`)*
*- Linee orizzontali (`---`)*
