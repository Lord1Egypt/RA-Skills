# 🌀 anti-loop v2.0 (中文版)

> **轻量级 LLM 智能体反无限循环守护器。治愈优于终止。**

```bash
pip install anti-loop
```

```python
from anti_loop import AntiLoop
guard = AntiLoop(mode="heal")
# 就这样。3 行代码。9 层保护。
```

[完整 SKILL.md](./SKILL.md) | [ClawHub](https://clawhub.ai/p/morgana-anti-infinite-loop-v2-zh) | [GitHub](https://github.com/kofna336/anti-loop)

---

## 为什么选择 v2.0?

v1(反响平平)只做了 `max_iter` + `kill`。v2.0 是:

- **可预测**(在崩溃前 5–10 轮提前预判)
- **可治愈**(注入系统消息,不会粗暴中止)
- **零依赖**(仅使用标准库,numpy 可选)
- **跨框架**(Claude、OpenAI、Hermes、LangChain、AutoGen、自定义)
- **9 层保护**(熵检测、新颖性、分类、治愈、自适应、呼吸率、飞行前、DNA、适配器)

**一次安装 = 6+ 层保护,零配置。**

---

## 快速开始 (30 秒)

```bash
pip install anti-loop
```

```python
from anti_loop import AntiLoop

guard = AntiLoop(mode="heal", max_iter=10)

for action in agent_actions:
    result = guard.observe(action, intent="你的目标")
    if result["intervene"]:
        # 智能体即将陷入循环
        if result["directive"]["action"] == "heal":
            inject_system_message(result["directive"]["system_message"])
        elif result["directive"]["action"] == "pause":
            time.sleep(result["directive"]["duration_seconds"])
        else:  # hard_kill
            raise Exception("智能体在循环中被中止")
```

**完整文档见 [SKILL.md](./SKILL.md)。**

---

## 三种治愈模式

| 模式 | 行为 | 适用场景 |
|---|---|---|
| `heal`(默认) | 注入上下文系统消息 | 生产环境、对话型智能体 |
| `pause` | `time.sleep(N)` | 后台任务、批处理 |
| `hard_kill` | `raise`/abort | 测试、关键边缘场景 |

**经验法则:** 默认使用 `heal`,批处理用 `pause`,安全关键路径用 `hard_kill`。

---

## 零依赖

```bash
# 核心:仅使用 Python 标准库
pip install anti-loop

# 可选扩展
pip install anti-loop[embeddings]      # + numpy
pip install anti-loop[kan]             # + torch
pip install anti-loop[multi-agent]     # + DFS 死锁图
```

---

## 许可证

MIT-0 —— 自由使用、修改、再分发,无需署名。

---

_为中文社区倾力打造_ 🧚
