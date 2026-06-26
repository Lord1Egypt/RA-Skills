---
name: kokoro-tts-amx
description: "Local Kokoro-82M text-to-speech on Intel CPU with bf16 autocast and oneDNN AMX-BF16 acceleration. Synthesizes Chinese/English/Japanese/French/Spanish/Hindi/Italian/Portuguese to a 24kHz mono WAV without any cloud API. Use for: TTS, voice synthesis, speech generation, narration, dubbing, 语音合成, 文本转语音, 朗读, 配音, generate speech, offline TTS, edge-tts alternative. Triggers: kokoro, tts, text to speech, 语音, 朗读, speak, narrate, voice synthesis, AMX BF16."
allowed-tools: Bash(python *), Bash(pip *), Bash(apt-get *), Bash(source *), Bash(cd *)
metadata:
  openclaw:
    requires:
      bins: [python3, pip, espeak-ng]
---

# kokoro-tts-amx

Local CPU TTS via Kokoro-82M, default bf16 autocast → oneDNN AMX-BF16
(Sapphire / Emerald / Granite Rapids). Multilingual (zh/en/ja/fr/es/hi/it/pt).

Skill 目录就是本仓库根; 完整说明见同目录 README.md.

## TL;DR
```bash
cd <skill-dir>  # 即本仓库根
source .venv/bin/activate
python tts.py "春天的早晨阳光明媚。"                    # → output.wav (zh, bf16/AMX)
python tts.py "Hello world." -v af_heart -o en.wav     # 英文
python tts.py "你好" --fp32 -o hi_fp32.wav             # 显式 fp32 对照
```

Voice 前缀: `zf_/zm_`=zh, `af_/am_`=en-US, `bf_/bm_`=en-GB, `jf_/jm_`=ja,
`ff_`=fr, `ef_`=es, `hf_`=hi, `if_`=it, `pf_`=pt-BR.
README.md: <https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices>.

## 首次安装 (新机器)
```bash
sudo apt-get install -y espeak-ng
python3 -m venv .venv && source .venv/bin/activate
pip install torch kokoro 'misaki[zh]' numpy
python -c "from kokoro import KPipeline; KPipeline(lang_code='z', repo_id='hexgrad/Kokoro-82M')"  # 预下载 ~350MB
```

## 注意
- AMX-BF16 仅 Intel SPR/EMR/GNR 有；老 CPU 自动 fallback 到 AVX-512 BF16/FP32。
- 默认走 bf16/AMX；如需 fp32 加 `--fp32`。
- 线程不显式设，由 PyTorch/oneDNN 按可见 CPU 自动分配，配 `taskset` 限核也 OK。
