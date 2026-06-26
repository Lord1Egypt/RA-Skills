#!/usr/bin/env python3
"""检查语音识别模型是否存在"""
import sys
from faster_whisper import WhisperModel

model_dir = sys.argv[1] if len(sys.argv) > 1 else None

try:
    model = WhisperModel(
        "tiny",
        device="cpu",
        compute_type="int8",
        download_root=model_dir,
        local_files_only=True
    )
    print("OK")
    sys.exit(0)
except Exception as e:
    print(f"Model not found: {e}", file=sys.stderr)
    sys.exit(1)
