# voice/ 目录说明

此目录存放声音克隆相关文件。

```
voice/
├── training_data/
│   ├── wavs/              # 预处理后的 WAV 文件（voice_preprocessor.py 输出）
│   ├── manifest.json      # 训练数据清单（文件数、总时长）
│   └── annotations.list   # Whisper 转录标注（格式：wav路径|说话人|语言|文本）
│
├── gpt_sovits/
│   ├── *.pth              # SoVITS 微调模型（约 80MB）
│   ├── *.ckpt             # GPT 微调模型（约 150MB，方言数据可能不需要）
│   └── train_config.json  # 训练参数记录
│
└── README.md              # 本文件
```

## 生成流程

```bash
# Step 1: 微信语音提取
python tools/wechat_voice_extractor.py --group "群名" --person "人名" --outdir memorials/{slug}/materials/audio/raw

# Step 2: 预处理（格式转换 + 降噪）
python tools/voice_preprocessor.py --dir materials/audio/raw --outdir materials/audio/processed

# Step 3: 一键训练（自动检测方言并选择策略）
python tools/voice_trainer.py --action full --slug {slug} --audio-dir materials/audio/processed

# Step 4: 合成测试
python tools/voice_synthesizer.py --slug {slug} --text "测试声音效果"
```
