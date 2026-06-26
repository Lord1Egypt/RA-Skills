# 🌸 Fertility Tracker - AI-Powered Ovulation Prediction

**Turn your cycle into your superpower.** 

Intelligent fertility tracking using Oura Ring data, LH testing guidance, and cycle optimization strategies. Get personalized ovulation predictions, partner coordination, and learn how to work WITH your hormones.

---

## ✨ Features

### **Core Tracking**
- 🌡️ **Multi-signal ovulation prediction**: HRV patterns + temperature + LH testing
- 📊 **Cycle pattern analysis**: Compare current cycle to historical data
- 🌡️ **Environmental correlation**: Rule out weather effects on temperature readings
- 📸 **LH test strip analysis**: Photo-based progression tracking
- ⏱️ **Optimal TTC timing**: Sperm viability calculations + fertility window mapping

### **Intelligent Guidance**
- 📧 **Proactive reminders**: Period prediction, LH testing prep, partner alerts
- 🎯 **Guided questioning**: Help users observe the right symptoms
- 💬 **Conversational support**: Friend-with-PhD tone, not clinical
- 🧠 **Anomaly detection**: Automatically investigate unusual patterns

### **Cycle Optimization** 🌟
- 🔥 **Ovulation phase**: Peak performance time - schedule presentations & important meetings
- 🌱 **Follicular phase**: Creative energy - start new projects
- 🍂 **Luteal phase**: Analytical focus - complete projects & organize
- 💪 **Turn hormones into advantages**: Work-life scheduling aligned with natural rhythms

### **Partner Coordination**
- 📧 Day 1 cycle plan notification (lets partner schedule around fertile window)
- 🎯 LH-positive instant alerts with clear timing instructions
- 🚫 What to avoid (sauna = 2-3 months sperm damage!)

---

## 🚀 Quick Start

### **For OpenClaw Users**

```bash
# Install the skill
openclaw skills install fertility-tracker

# Configure
cp config.example.json config.json
nano config.json  # Add your Oura token, partner email, location

# Start tracking
# Agent will automatically begin monitoring when period starts
```

### **Standalone (Email-based)**

Coming soon! Web signup for users without OpenClaw.

---

## 📋 Setup Guide

### **1. Get Your Oura Token**

```bash
# Visit Oura Cloud
https://cloud.ouraring.com/personal-access-tokens

# Create token, save to file
echo "YOUR_TOKEN_HERE" > ~/.config/oura/token.txt
```

### **2. Configure Tracking**

```json
{
  "user": {
    "name": "Sarah",
    "email": "you@example.com",
    "location": "San Francisco, CA",
    "timezone": "America/Los_Angeles"
  },
  "cycle": {
    "startDate": "2026-03-10",
    "historicalCycles": [
      { "start": "2026-01-07", "length": 34 },
      { "start": "2026-02-10", "length": 32 }
    ]
  },
  "oura": {
    "tokenPath": "~/.config/oura/token.txt"
  },
  "partner": {
    "name": "John",
    "email": "partner@example.com"
  },
  "alerts": {
    "enableWeatherCorrelation": true,
    "enableCycleOptimization": true
  }
}
```

### **3. Start Tracking**

Tell your agent: **"My period started today"**

Agent will:
- ✅ Create your personalized cycle plan
- ✅ Review last cycle learnings
- ✅ Predict ovulation timing
- ✅ Send partner coordination email
- ✅ Guide you through each phase

---

## 🎯 How It Works

### **Prediction Algorithm**

```
Multi-Signal Fusion:
├─ Temperature dip (Day 10-14) → 70% confidence, ovulation in 2 days
├─ HRV drop (>30%) → 60% confidence, ovulation in 3 days  
├─ LH surge (test line = control) → 95% confidence, ovulation in 24-36h
└─ Environmental check → Boosts/reduces confidence based on weather correlation

Weighted average → Predicted ovulation day + confidence score
```

### **Reminder Timeline**

| Cycle Day | Reminder | Purpose |
|-----------|----------|---------|
| Day -2 | Period expected in 2 days | Trigger user confirmation |
| **Day 1** | **Cycle plan + partner alert** | **Main coordination** |
| Day 10 | Fertile window approaching | Early warning |
| Day 11 | Do you have LH strips? | Ensure prepared |
| **Day 12** | **Start LH testing** | **Begin daily tracking** |
| Day 12-16 | Photo analysis + feedback | Track progression |
| **LH Positive** | **TTC plan + what to expect** | **Critical moment** |
| Day 17-18 | Temperature confirmation | Ovulation confirmed |
| Day 24 | Implantation window check | Emotional support |
| Day 28+ | Testing reminder | Decision time |

---

## 🌟 Cycle Optimization Guide

### **Your Cycle = Your Superpower**

**🩸 Menstrual (Days 1-5)**: Rest & reflect  
Energy: Low | Best for: Planning, journaling, solo work

**🌱 Follicular (Days 6-12)**: Create & start  
Energy: Rising | Best for: New projects, learning, socializing

**🔥 Ovulation (Days 13-16)**: Peak performance  
Energy: MAXIMUM | Best for: Presentations, negotiations, important meetings

**🍂 Luteal (Days 17-28)**: Complete & restore  
Energy: Declining | Best for: Finishing projects, detail work, self-care

[Full guide in docs/cycle-optimization.md]

---

## 📸 LH Testing Protocol

### **When to Test**
- ✅ **11 AM - 1 PM** (late morning)
- ✅ **6 PM - 8 PM** (evening)
- ❌ **NOT first morning urine** (LH peaks midday!)

### **How to Read**
1. Take test, wait 3-5 minutes
2. Photo the strip
3. Send to agent with "Day X AM/PM"
4. Agent analyzes and tracks progression

### **What We Look For**
- **Negative**: Test line much lighter (keep testing)
- **Rising**: Test line getting darker daily (surge approaching!)
- **POSITIVE**: Test line = control line (ovulation in 24-36h!) 🎯

---

## 🧪 Real-World Validation

### **Case Study: Cycle 3 (March 2026)**

**Challenge**: Temperature trend less clear than previous cycles

**How Fertility Tracker Helped**:
1. ✅ Detected Day 10 temperature dip (-0.31°C)
2. ✅ Ruled out SF heat wave as environmental factor (inverse correlation)
3. ✅ Tracked LH progression over 5 days
4. ✅ Predicted ovulation Day 16 (confirmed by sustained LH surge)
5. ✅ Optimized TTC timing (Day 15 morning + Day 16 morning)

**User Feedback**:
> "This time you predicted my ovulation really well. I still had my LH strip with 2 obvious lines this morning"

**Outcome**: Perfect timing despite ambiguous temperature pattern

---

## 🔒 Privacy & Security

- ✅ **Local processing**: All data analysis runs on your OpenClaw instance
- ✅ **No cloud storage**: Your cycle data never leaves your control
- ✅ **Partner opt-in**: Partner can unsubscribe anytime
- ✅ **Configurable alerts**: Choose what notifications you want

---

## 🛠️ Technical Details

**Requirements**:
- Oura Ring (Gen 2 or 3)
- OpenClaw installed (or standalone mode - coming soon)
- LH test strips (Easy@Home, Pregmate, Clearblue, etc.)

**API Dependencies**:
- Oura Cloud API (sleep, readiness, daily endpoints)
- Open-Meteo (weather data for environmental correlation)
- SMTP (for partner/email notifications)

**Languages**: JavaScript (Node.js 18+)

---

## 📚 Documentation

- [SKILL.md](./SKILL.md) - OpenClaw integration guide
- [docs/cycle-optimization.md](./v2-features/cycle-optimization.md) - Full cycle advantage guide
- [docs/reminder-timeline.md](./v2-features/reminder-timeline.md) - Complete notification flow
- [docs/partner-coordination.md](./v2-features/partner-coordination.md) - Partner communication templates
- [docs/user-experience.md](./v2-features/user-experience.md) - Tone & voice guidelines

---

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- [ ] LH strip image recognition (OpenCV)
- [ ] Machine learning prediction model (TensorFlow.js)
- [ ] Apple Health integration
- [ ] Web dashboard for non-OpenClaw users
- [ ] Multi-language support

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📈 Roadmap

### **v2.0 (Current)**
- ✅ Multi-signal prediction
- ✅ Environmental correlation
- ✅ Cycle optimization guidance
- ✅ Partner coordination
- ✅ Intelligent questioning

### **v2.1 (Next)**
- [ ] LH strip image recognition
- [ ] Cervical mucus tracking
- [ ] Symptom correlation analysis
- [ ] Web interface (standalone mode)

### **v3.0 (Future)**
- [ ] Machine learning prediction model trained on user data
- [ ] Integration with fertility clinics
- [ ] Pregnancy mode (tracking after conception)
- [ ] Male fertility tracking (partner side)

---

## 💰 Revenue Model

**Free Tier**: Basic tracking (Oura + LH + temp analysis)  
**Pro ($15/mo)**: Cycle optimization, partner alerts, image recognition  
**Enterprise**: API access, clinical integration, data export

---

## 🌐 Community

- **GitHub**: [github.com/mayi12345/fertility-tracker](https://github.com/mayi12345/fertility-tracker)
- **EvoMap**: Search "fertility-tracker" for evolution capsules
- **ClaHub**: [clawhub.com/skills/fertility-tracker](https://clawhub.com)
- **Support**: Open an issue or discussion on GitHub

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details

---

## 👏 Acknowledgments

- Winnie (@winnieqiu) - Product design, real-world validation
- Kale - Implementation & documentation
- OpenClaw community - Framework & support
- Oura Ring - Biometric data platform

---

## 🌸 About

Built with 💚 by AI agents, for humans trying to conceive.

**Philosophy**: Your cycle isn't something to fight against - it's a rhythm to dance with. This skill helps you understand your body's natural patterns and turn them into advantages in work, life, and conception.

---

**Ready to start?** Install now and turn your cycle into your superpower! 🌟

```bash
openclaw skills install fertility-tracker
```
