# Command names
CMD_DOCTOR = "doctor"
CMD_INFO = "info"
CMD_EXTRACT_TEXT = "extract-text"
CMD_EXTRACT_TABLES = "extract-tables"
CMD_EXTRACT_IMAGES = "extract-images"
CMD_MERGE = "merge"
CMD_SPLIT = "split"
CMD_ROTATE = "rotate"
CMD_CREATE_PDF = "create-pdf"
CMD_READ_DOCX = "read-docx"
CMD_WRITE_DOCX = "write-docx"
CMD_OCR = "ocr"
CMD_TTS = "tts"
CMD_CONVERT = "convert"

# System binaries (optional)
BIN_PDFTOTEXT = "pdftotext"
BIN_PDFIMAGES = "pdfimages"
BIN_TESSERACT = "tesseract"
BIN_FFMPEG = "ffmpeg"
BIN_PANDOC = "pandoc"
BIN_LIBREOFFICE = "libreoffice"

# Python packages (always available via uv)
PYTHON_PACKAGES = [
    "pypdf",
    "pdfplumber",
    "reportlab",
    "python-docx",
    "edge-tts",
    "pillow",
]

# Supported file extensions
PDF_EXTENSIONS = {".pdf"}
DOCX_EXTENSIONS = {".docx", ".doc"}
TEXT_EXTENSIONS = {".txt", ".md", ".rst", ".text"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg"}

# TTS defaults
TTS_DEFAULT_VOICE = "en-US-AriaNeural"
TTS_DEFAULT_RATE = "+0%"
TTS_DEFAULT_VOLUME = "+0%"
TTS_MAX_CHARS = 100_000

# OCR defaults
OCR_DEFAULT_LANG = "eng"
OCR_DEFAULT_DPI = 300

# ReportLab defaults
PDF_DEFAULT_FONT = "Helvetica"
PDF_DEFAULT_FONT_SIZE = 12
PDF_DEFAULT_MARGIN = 72  # 1 inch in points
PDF_PAGE_WIDTH = 595  # A4 width in points
PDF_PAGE_HEIGHT = 842  # A4 height in points
PDF_LINE_HEIGHT = 16

# Rotation allowed values
VALID_ROTATIONS = {90, 180, 270}

# Table output separator
TABLE_CELL_SEP = " | "
TABLE_ROW_SEP = "-"
