"""
OCR2Markdown pipeline constants.
"""

# GPU type for OCR workload
GPU_TYPE = "L4"

# Volume names (shared with audio pipelines via same Modal account)
VOLUME_DATA_NAME = "speech2srt-data"
VOLUME_MODELS_NAME = "speech2srt-models"

# Volume mount points
MOUNT_DATA = "/mnt/data"
MOUNT_MODELS = "/mnt/models"

# Directory names under slug
DIR_UPLOAD = "upload"
DIR_OUTPUT = "output"

# OCR timeout (seconds) — 2 hours for large PDFs
TIMEOUT_OCR2MD = 7200

# App name
APP_NAME = "speech2srt.com"
