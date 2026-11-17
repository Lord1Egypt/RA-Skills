#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 1 —— 日语 ASMR/音声 词级 ASR（faster-whisper large-v3-turbo, int8, CPU）

用法:
    python whisper_word_gen.py <audio> <out_words.txt> [script.txt]

输出: TSV，每行  start<TAB>end<TAB>word

要点（踩过的坑，勿改）:
  * vad_filter 必须 False：ASMR 耳语音量低于语音阈值，开 VAD 会把整段判成静音
  * condition_on_previous_text=False + compression_ratio_threshold=2.4：压制复读幻觉
  * no_speech_threshold=0.85：放宽，低声耳语不误判为静音
  * word_timestamps=True：给 Step 2 的对齐提供词级时间基准
  * initial_prompt 自动取台本前若干行 → 专名/口语识别率明显提升
"""
import os, sys, re

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")          # XET CAS 会 401，必须关
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

if len(sys.argv) < 3:
    sys.exit(__doc__)
audio, out = sys.argv[1], sys.argv[2]
script = sys.argv[3] if len(sys.argv) > 3 else ""

prompt = ""
if script and os.path.exists(script):
    DROP = re.compile(r"[^ぁ-んァ-ヶー一-龥々〆a-zA-Z0-9\s]")
    lines = [re.sub(r"\s+", "", DROP.sub("", l)) for l in open(script, encoding="utf-8")]
    lines = [l for l in lines if l][:40]
    prompt = "。".join(lines)[:240]
print("initial_prompt:", prompt[:80], "...", flush=True)

from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=16)
segs, info = model.transcribe(
    audio, language="ja", beam_size=5,
    condition_on_previous_text=False,
    compression_ratio_threshold=2.4,
    no_speech_threshold=0.85,
    initial_prompt=prompt,
    word_timestamps=True,
    vad_filter=False,
)
n = 0
with open(out, "w", encoding="utf-8") as f:
    for s in segs:
        for w in s.words:
            f.write(f"{w.start:.3f}\t{w.end:.3f}\t{w.word.strip()}\n")
            n += 1
print("word 条数:", n)
