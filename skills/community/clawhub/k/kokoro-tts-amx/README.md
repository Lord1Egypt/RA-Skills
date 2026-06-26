# kokoro-tts-amx

Kokoro-82M 多语种 TTS, PyTorch CPU + bf16 autocast (oneDNN AMX-BF16).
支持中/英/日/法/西/印地/意/葡 等 (见 Kokoro 官方 voice 列表)。

## 从 GitHub 安装

**给用户**: 把这个 repo 的 URL 发给你的 agent, 说 "帮我安装这个 skill".

**给 agent**: 运行下面任一条命令即可完成安装 (apt 装 espeak-ng + venv + pip + 软链注册到 skills 目录), 完成后让用户 /reset:

```bash
# 方法 1: clone 后装 (推荐, repo 留在当前目录)
git clone https://github.com/Wray151/xeontts.git
cd xeontts && bash install.sh

# 方法 2: 远程一键 (自动 clone 到 ~/.local/share/kokoro-tts-amx)
curl -fsSL https://raw.githubusercontent.com/Wray151/xeontts/main/install.sh \
  | REPO_URL=https://github.com/Wray151/xeontts bash

# 想装到 ~/.claude/skills/ 而不是 openclaw, 加 TARGET=claude
TARGET=claude bash install.sh
```

## 首次安装
 Python 3.10+ 和系统的 `espeak-ng` (misaki 用来兜底音素化)。

```bash
# Debian/Ubuntu
sudo apt-get install -y espeak-ng

# 建虚拟环境并装依赖 (中文用 misaki[zh], 纯英文 misaki[en] 即可)
python3 -m venv .venv
source .venv/bin/activate
pip install torch kokoro 'misaki[zh]' numpy

# 预下载模型 (~350MB) 到 HF cache, 之后离线也能用
python -c "from kokoro import KPipeline; KPipeline(lang_code='z', repo_id='hexgrad/Kokoro-82M')"
```

## 用法
```bash
source .venv/bin/activate

# 中文 (默认 voice=zf_xiaobei, 自动 lang=z)
python tts.py "春天的早晨阳光明媚。"

# 英文
python tts.py "Hello world, this is a test." -v af_heart -o en.wav

# 显式指定语言 (voice 与 lang 不同前缀时)
python tts.py "Bonjour" -v ff_siwis -l f -o fr.wav

# fp32 对照 (默认是 bf16/AMX, 加 --fp32 走 fp32)
python tts.py "你好" --fp32 -o hi_fp32.wav
```

voice 前缀: `zf_/zm_`=zh, `af_/am_`=en-US, `bf_/bm_`=en-GB, `jf_/jm_`=ja,
`ff_`=fr, `ef_`=es, `hf_`=hi, `if_`=it, `pf_`=pt-BR. 完整清单见
<https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices>.

参考: Xeon 6982P-C / 容器 2 vCPU / 中文 20 字 → bf16 RTF 0.54, fp32 RTF 0.76.

## 注意事项
- **AMX 硬件**: 仅 Intel Sapphire Rapids / Emerald Rapids / Granite Rapids 有 AMX-BF16; 老 CPU 会 fallback 到 AVX-512 BF16 或 FP32, 仍可跑但拿不到完整加速。验证: `lscpu | grep amx`。
- **首次联网**: 第一次跑会从 HuggingFace 拉模型 (~350MB), 离线机器请提前在联网环境完成"预下载"那一步, 然后拷贝 `~/.cache/huggingface`。
- **Python 版本**: 推荐 3.10–3.12; misaki 在 3.13 上可能装不全。
- **多语种依赖**: 中文要 `misaki[zh]` (含 jieba/pypinyin); 日文要 `misaki[ja]` (含 pyopenjtalk); 其余靠 espeak-ng。
- **音质 vs 精度**: bf16 与 fp32 输出有极轻微差异 (听感无损); 默认 bf16/AMX, 显式跑 fp32 加 `--fp32`。
- **许可**: Kokoro-82M 模型 Apache-2.0, 商用前自查 HuggingFace 仓库。
- **线程**: 不显式设, 由 PyTorch / oneDNN 按可见 CPU 自动分配; 容器/`taskset` 限核场景下也会自动收敛。
