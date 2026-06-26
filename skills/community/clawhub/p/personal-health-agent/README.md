# 🏥 Personal Health Agent — OpenClaw Skill

Turn your OpenClaw assistant into a personal health agent powered by your Fitbit wearable data.

Based on [The Anatomy of a Personal Health Agent](https://arxiv.org/abs/2508.20148) (Liu, McDuff, Xu et al., 2025).

## Install

```bash
clawhub install pha-openclaw-skill
```

Or manually:
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/xliucs/pha-openclaw-skill.git personal-health-agent
```

## Setup (2 minutes)

1. **Register a Fitbit app** at [dev.fitbit.com/apps/new](https://dev.fitbit.com/apps/new)
   - Type: **Personal**, Redirect URL: `http://localhost:8080/callback`, Access: **Read Only**

2. **Save credentials:**
   ```bash
   cd ~/.openclaw/workspace/skills/personal-health-agent
   cp .env.example .env
   # Edit .env with your Client ID and Secret
   ```

3. **Authorize:** Tell your OpenClaw agent `/health_setup` and follow the prompts.

4. **Sync data:** `/health_sync`

## Usage

Just talk to your agent about your health:

- "How has my sleep been this week?"
- "What's my resting heart rate trend?"
- "Help me improve my step count"
- "Give me a weekly health summary"

## Supported Metrics

- Steps & calories
- Heart rate (resting HR, zones)
- Heart rate variability (HRV)
- Sleep (duration, stages, efficiency)
- SpO2 (blood oxygen)
- Breathing rate
- Skin temperature

## How it works

This skill teaches your OpenClaw agent (any model — Claude, GPT, Gemini) how to query and analyze your Fitbit data. No additional API keys needed beyond what OpenClaw already has. Your health data stays local on your machine.

## Privacy

- All Fitbit data is stored locally in the `data/` directory
- No data is sent to any third party
- Your OpenClaw agent processes everything locally
- You control your own Fitbit API credentials

## License

MIT

## Citation

```bibtex
@article{liu2025pha,
  title={The Anatomy of a Personal Health Agent},
  author={Liu, Xin and McDuff, Daniel and Xu, Xin "Orson" and others},
  journal={arXiv preprint arXiv:2508.20148},
  year={2025}
}
```
