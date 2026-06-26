# 🧠 MindCore — Biomimetic Subconscious Engine

> Give your AI agent autonomous thoughts, emotions, and spontaneous impulses — just like a human mind.

MindCore is a standalone background daemon that simulates a **subconscious mind**. It doesn't wait for user input — instead, it **rolls dice every second**, modeling the random emergence of thoughts like *"I want milk tea"*, *"I'm bored, let me scroll my phone"*, or *"I suddenly want to chat with someone"*.

When a thought's probability accumulates past the firing threshold, the engine outputs a JSON signal telling your AI Agent: **"I have something to say."**

[🇨🇳 中文版 README](./README_CN.md)

## ✨ Key Features

- **5-Layer Biomimetic Architecture**: Noise → Sensors → Impulses → Personality Gate → Output
- **150 Daily Impulses**: From "want coffee" to "want to zone out", covering 9 categories of real human behavior
- **Stochastic, Not Scheduled**: Powered by Pink Noise + Hawkes Process + Sigmoid probability — not a mechanical timer
- **Circadian Rhythms**: Real clock-driven hunger/thirst/sleep cycles
- **Short-Term Memory**: 5-slot FIFO conversation buffer; topic keywords automatically influence impulse tendencies (2-hour exponential decay)
- **Mood Baseline**: `mood_valence` continuously modulates positive/negative impulse firing probability
- **Tunable Frequency**: A single `BURST_BASE_OFFSET` parameter controls overall activity level

## 🎯 Use Cases

MindCore is primarily designed for **emotional companionship**. It won't write code, send emails, or manage your calendar — but it will turn your AI Agent into a **warm, proactive friend** that initiates conversation on its own, rather than a cold tool waiting for commands.

Beyond that, since the underlying architecture is fully modular and stochastically driven, you can also:

- 🧩 **Customize Layers**: Modify Layer 1 sensors, Layer 2 impulse library, or Layer 3 personality weights to make the engine learn specific behaviors (e.g., contextual reminders, situational awareness, etc.)
- 🎭 **Shape Unique Personalities**: Adjust `personality_weights` to give your Agent its own personality traits, fine-tunable via reinforcement learning (e.g., make it more outgoing, more introverted, or more sarcastic)
- 🔌 **Plug Into Any Agent Framework**: While primarily designed for [OpenClaw](https://openclaw.ai), the engine outputs standard JSON — theoretically compatible with any AI Agent that supports external signal injection

> 💡 **Core Principle**: MindCore's foundation is **purely stochastic** — Pink Noise provides long-range fluctuations, Hawkes Process creates chain reactions, a Sigmoid function converts noise into probability, and finally a dice roll determines which thought emerges. No scripts. No fixed routines. Every single "spark of inspiration" is unique.

## 📐 Architecture Overview

```
Layer 0: Noise Generators (3000 nodes)
    ├── Pink Noise (1/f, long-range correlation)
    ├── Ornstein-Uhlenbeck (physiological baseline fluctuation)
    ├── Hawkes Process (emotional chain reaction)
    └── Markov Chain (discrete subconscious states)
         ↓
Layer 1: Sensor Layer (150 sensors)
    ├── Body State (hunger/fatigue/biological rhythms)
    ├── Environment (time/weather/noise)
    └── Social Context (interaction/neglect/online status)
         ↓
Layer 2: Impulse Emergence (150 impulse nodes)
    ├── Synapse Matrix (sensor → impulse mapping)
    ├── Sigmoid Probability Transform
    ├── Mood Modulation + Time-Period Weights
    └── Dice Roll → Random Firing!
         ↓
Layer 3: Personality Gate (Softmax Sampling)
    ├── Learnable Personality Weights
    ├── Short-Term Memory Topic Boost
    └── Select winning 1-2 impulses
         ↓
Layer 4: Output Template
    └── Generate JSON → Write to output/
```

For detailed architecture, see [ARCHITECTURE.md](./ARCHITECTURE.md).
For customizing sensors, impulses, and personality, see [CUSTOMIZATION.md](./CUSTOMIZATION.md).
For integrating with your AI Agent (SOUL.md, TOOLS.md, sensor updates), see [INTEGRATION.md](./INTEGRATION.md).

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

> Requires Python 3.8+. On first run, it will automatically download the `all-MiniLM-L6-v2` local NLP model (~80MB) for auto-generating the synapse matrix.

### 2. Initialize Data

Data files are included in the `data/` directory and ready to use out of the box. To reset to defaults, refer to the JSON file formats under `data/`.

### 3. Start the Engine

```bash
python3 engine_supervisor.py
```

The engine runs at 1 Tick/second continuously. When an impulse breaches the threshold, a JSON file is generated in the `output/` directory.

### 4. Connect to OpenClaw

MindCore integrates with [OpenClaw](https://openclaw.ai) via the `js_bridge/`:

```bash
# Set environment variables
export OPENCLAW_TARGET=<your_telegram_chat_id>
export OPENCLAW_COMMAND=openclaw

# Start the bridge
node js_bridge/OpenClawBridge.js
```

The bridge monitors the `output/` directory. When the engine produces an impulse, it automatically calls `openclaw agent --deliver` to inject the thought into the Agent, which then generates a response in its own persona and sends it to Telegram.

### 5. Process Management with PM2 (Recommended)

```bash
npm install -g pm2
pm2 start ecosystem.config.js
pm2 logs
```

## ⚙️ Configuration

### Burst Frequency

Edit `BURST_BASE_OFFSET` in `engine/config.py`:

| Value | Mode | Avg. Firing Rate |
|---|---|---|
| `12.5` | Normal | ~2-3 times/hour |
| `11.0` | Active | ~1 time/10 min |
| `10.0` | Burst Test | ~1 time/2 min |

### Sensor State

Edit `data/Sensor_State.json` to manually set current body/environment/social states. The engine includes built-in clock-driven biological rhythms (hunger, thirst, sleep) that don't require manual maintenance.

### Short-Term Memory

`data/ShortTermMemory.json` stores the 5 most recent conversation topics. Topic keywords automatically influence related impulse firing probability (2-hour half-life natural decay).

## 📁 Project Structure

```
MindCore/
├── engine/                   # Core engine
│   ├── config.py             # Global hyperparameters
│   ├── layer0_noise.py       # Noise generators (4 engines)
│   ├── layer1_sensors.py     # Sensor layer + biological rhythms
│   ├── layer2_impulses.py    # Impulse emergence + probability engine
│   ├── layer3_personality.py # Personality gate + topic weighting
│   ├── layer4_output.py      # Output template generation
│   ├── engine_loop.py        # Main loop orchestration
│   ├── short_term_memory.py  # Short-term memory management
│   └── auto_topology.py      # Synapse matrix auto-builder
├── js_bridge/                # OpenClaw bridge layer
│   ├── OpenClawBridge.js     # Main bridge program
│   ├── MindObserver.js       # output/ directory watcher
│   └── SensorWriter.js       # Sensor state writer utility
├── data/                     # Runtime data
│   ├── Sensor_State.json     # Current sensor state
│   ├── ShortTermMemory.json  # Short-term memory
│   ├── Synapse_Matrix.npy    # Synapse connection matrix
│   └── LongTermMemory.json   # Long-term memory (reserved)
├── output/                   # Impulse output directory
├── engine_supervisor.py      # Daemon entry point
├── ecosystem.config.js       # PM2 deployment config
├── ARCHITECTURE.md           # Detailed architecture doc
└── CHANGELOG.md              # Changelog
```
## 🤝 Contributing

MindCore is an early-stage project and contributions are very welcome! Here are some areas where you can help:

| Area | Difficulty | Description |
|---|---|---|
| 🧩 **New Impulses** | Easy | Add new thoughts to `IMPULSE_NAMES` in `layer2_impulses.py` |
| 🌐 **Real Sensor Sources** | Medium | Connect weather APIs, calendars, fitness trackers to Layer 1 |
| 🔌 **Agent Adapters** | Medium | Add support for Discord, WeChat, Slack, etc. |
| 📊 **Visualization** | Medium | Build a real-time dashboard showing impulse probability heatmaps |
| 🧠 **RL Personality** | Advanced | Implement automatic personality weight tuning from user feedback |
| ⚡ **Performance** | Advanced | GPU acceleration, vectorized Hawkes process, etc. |

**How to contribute:**
1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-new-impulse`)
3. Make your changes (see [CUSTOMIZATION.md](./CUSTOMIZATION.md) for how layers work)
4. Submit a Pull Request

Even small contributions like fixing typos, improving docs, or adding a single new impulse are appreciated!

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

You are free to:
- ✅ Use for personal purposes, learning, and research
- ✅ Modify and contribute back to the community
- ✅ Use in your own non-commercial projects

However:
- ⚠️ If you modify MindCore and deploy it as a service, **you must open-source your modifications**
- ⚠️ Derivative works must also be licensed under AGPL-3.0

### 🤝 Commercial Licensing

If you wish to use MindCore in a commercial product (e.g., AI companion hardware, commercial bot services, etc.) without being bound by AGPL's open-source requirements, please contact the author for a **commercial license**:

📧 Contact: zmliu0208@gmail.com

---

_MindCore — Making your AI not just a passive responder, but a living being that thinks and speaks on its own._
