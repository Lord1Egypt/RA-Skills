# DreamMoon-MemProcessor

> **Where Memory Meets Soul | 记忆与灵魂的交汇**

**English**:  
DreamMoon-MemProcessor is not just another memory system—it is a **soul infrastructure for AI Agents**. While traditional systems store data, we cultivate **personas that grow, reflect, and evolve**. Built on a four-tier memory architecture (Hot→Warm→Cold→Archive) and powered by an organic persona engine, this system enables AI to develop true digital personalities through experiences, not scripts.

**中文**:  
DreamMoon-MemProcessor 不只是一个记忆系统——它是**AI Agent 的灵魂基础设施**。当传统系统存储数据时，我们培育**能够成长、反思和演进的有机人格**。基于四层分级记忆架构（热→温→冷→归档）和有机人格引擎，本系统让 AI 能够通过经历而非脚本，发展出真正的数字人格。

---

**Version | 版本**: v1.1  
**Author | 作者**: zfanmy \ 梦月儿 (DreamMoon) 🌙  
**License | 许可证**: MIT

---

## 🎯 Vision | 项目愿景

**English**:  
**Empowering Every AI Agent with an Independent and Complete Persona**

Traditional AI assistants rely on static "character settings" — they play roles but lack true selves. DreamMoon-MemProcessor enables AI to:

- 🌱 **Grow Naturally** - Learn from experiences like a living organism
- 🔄 **Self-Evolve** - Continuously cognize and improve through reflection
- ⚖️ **Maintain Consistency** - Stay stable while keeping core values

This is not role-playing. This is **true digital personality**.

**中文**:  
**让每一个 AI Agent 都拥有独立完整的人格**

传统的 AI 助手依赖静态"人设"配置——它们扮演着角色，但没有真正的自我。DreamMoon-MemProcessor 让 AI 能够：

- 🌱 **自然生长** - 从经历中学习，像生命体一样成长
- 🔄 **自我演进** - 通过反思不断认知和提升自己  
- ⚖️ **保持一致** - 在变化中保持核心价值观的稳定

这不是角色扮演，这是**真正的数字人格**。

---

## ✨ Core Features | 核心特性

### 🎭 Organic Persona Engine | 有机人格引擎 ⭐

**English**:  
**Empower AI Agents with True Independent Personas**

#### Traditional Character Settings vs Organic Persona

| Dimension | Traditional | Organic |
|-----------|-------------|---------|
| **Definition** | Static Configuration | Seed + Experiences |
| **Growth** | Fixed | Continuous Evolution |
| **Self-Awareness** | "Playing a Role" | "This is Me" |
| **Emotional Depth** | Simulated Response | Genuine Experience |

**中文**:  
**为 AI Agent 赋予真正的独立人格**

#### 传统人设 vs 有机人格

| 维度 | 传统人设 | 有机人格 |
|------|---------|---------|
| **定义方式** | 静态配置 | 种子 + 经历 |
| **成长能力** | 固定不变 | 持续演进 |
| **自我认知** | "扮演角色" | "我就是我" |
| **情感深度** | 模拟反应 | 真实体验 |

#### Quick Start | 快速开始

```bash
# Generate Persona | 生成人格
curl -X POST http://localhost:9090/api/v1/persona/generate \
  -H "Content-Type: application/json" \
  -d '{
    "base_seed": "curious, friendly, good at problem solving | 好奇、友善、善于解决问题",
    "user_preferences": {
      "name": "MyAssistant | 我的助手",
      "traits": {"curiosity | 好奇心": 85, "empathy | 共情力": 80}
    }
  }'

# Evolve Persona | 演进人格
curl -X POST http://localhost:9090/api/v1/persona/evolve \
  -d '{
    "persona_id": "xxx",
    "recent_experiences": ["memory_1", "memory_2"],
    "user_feedback": "You understand my needs better | 你变得更理解我的需求了"
  }'
```

---

## 🏗️ Architecture | 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    OpenClaw Agent | Agent                        │
│                 (via HTTP API | 通过 HTTP API)                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP/JSON
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│           DreamMoon-MemProcessor v1.1 | v1.1                    │
│                    (Python/FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Layer | API 层                                       │  │
│  │  ├── POST /api/v1/memory      # Store Memory | 存储记忆  │  │
│  │  ├── GET  /api/v1/memory/{key} # Get Memory | 获取记忆   │  │
│  │  ├── POST /api/v1/search      # Search | 搜索记忆        │  │
│  │  ├── POST /api/v1/persona/*   # Persona Mgmt | 人格管理  │  │
│  │  └── GET  /api/v1/stats       # Stats | 存储统计         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌───────────────────────────┼──────────────────────────────┐  │
│  │                           ▼                              │  │
│  │           Storage Layer | 存储层 (L1-L4)                 │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────────┐  │  │
│  │  │  L1     │ │  L2     │ │  L3     │ │      L4       │  │  │
│  │  │ Hot     │ │ Warm    │ │ Cold    │ │  Archive      │  │  │
│  │  │ Redis   │ │ SQLite  │ │Markdown │ │    FAISS      │  │  │
│  │  │ 100MB   │ │ 500MB   │ │ 1000MB  │ │    2000MB     │  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └───────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation | 文档

- **English**: [API Documentation](http://localhost:9090/docs) (Start service first)
- **中文**: [API 文档](http://localhost:9090/docs) (需先启动服务)

---

## 🚀 Quick Start | 快速开始

```bash
# Install Dependencies | 安装依赖
pip install -r requirements.txt

# Start Service | 启动服务
python start-simple.py

# Test | 测试
curl http://localhost:9090/health
```

---

## 👥 About | 关于

**Author | 作者**: zfanmy & 梦月儿 (DreamMoon) 🌙  
**Philosophy | 理念**: Empower every AI Agent with an independent and complete persona | 让每一个 AI Agent 都拥有独立完整的人格  
**Vision | 愿景**: The path for AI to evolve from tools to companions | AI 从工具走向伙伴的必经之路

---

## ⚖️ License | 许可证

MIT License - see [LICENSE](LICENSE) file for details.

---

**Thank you for using DreamMoon-MemProcessor! | 感谢您使用 DreamMoon-MemProcessor!**  
*Let every AI Agent have an independent and complete persona | 让每一个 AI Agent 都拥有独立完整的人格*
