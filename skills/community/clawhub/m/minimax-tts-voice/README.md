# MiniMax Text-to-Speech Skill

Generate natural-sounding MP3 audio from text using MiniMax's `speech-2.8-hd` model.

## Setup

1. Install:
   ```bash
   clawhub install minimax-tts
   ```

2. Set your API key:
   ```bash
   export MINIMAX_API_KEY=your_key_here
   ```

3. Get your API key at: https://platform.minimax.io

## Usage

```bash
python scripts/minimax_media.py tts "你好，這是語音測試。" --voice female-tianmei --speed 1.0 --output hello.mp3
```

## Voice Options

| Voice ID | Language | Gender |
|----------|----------|--------|
| female-tianmei | Chinese | Female |
| male-qn-qingse | Chinese | Male |
| male-qn-jianbin | Chinese | Male |
| English_expressive_narrator | English | Male |

Speed: `--speed 0.5` to `--speed 2.0` (default: 1.0)

## Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| MINIMAX_API_KEY | Yes | - |
| MINIMAX_BASE_URL | No | https://api.minimax.io |

## License

MIT
