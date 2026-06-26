# Ollama on Windows — Complete Setup, CORS Fix & Custom Models

## What This Solves

Getting Ollama working on Windows with CORS headers (needed for web-based AI apps) and creating custom models with personality prompts.

## Installation

1. Download Ollama from [ollama.com](https://ollama.com)
2. Run the installer
3. Open a terminal and verify: `ollama --version`

## CORS Fix (Required for Web Apps)

Web-based AI interfaces need CORS headers. Set this environment variable:

### Via PowerShell (temporary):
```powershell
$env:OLLAMA_ORIGINS = "*"
ollama serve
```

### Via System Settings (permanent):
1. Open **System Properties** → **Environment Variables**
2. Under **User variables**, click **New**
3. Variable name: `OLLAMA_ORIGINS`
4. Variable value: `*`
5. Restart Ollama

## Custom Models with Modelfiles

Create a file called `MyModel.modelfile`:

```
FROM llama3.1:8b
PARAMETER temperature 0.7
PARAMETER top_p 0.9

SYSTEM """
You are a helpful assistant with expertise in [your domain].
Keep responses concise and practical.
"""
```

Build it:
```bash
ollama create my-model -f MyModel.modelfile
```

Test it:
```bash
ollama run my-model "Hello, how are you?"
```

## Model Recommendations by VRAM

| VRAM | Recommended Model | Size |
|------|------------------|------|
| 4GB | gemma3:4b | ~2.5GB |
| 8GB | llama3.1:8b | ~4.7GB |
| 12GB | qwen2.5:14b | ~9GB |
| 16GB+ | llama3.1:70b (quantized) | ~40GB |

## Troubleshooting

**"Connection refused" errors:** Ollama isn't running. Start it with `ollama serve` or check if it's in your system tray.

**CORS errors in browser:** The `OLLAMA_ORIGINS` variable isn't set or Ollama wasn't restarted after setting it.

**Model won't load:** Check your available VRAM with `nvidia-smi`. The model might be too large.

**Slow generation:** If using CPU instead of GPU, check that CUDA/ROCm drivers are installed.
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
