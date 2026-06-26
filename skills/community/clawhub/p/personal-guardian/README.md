# personal-guardian — 个体终端应急守护智能体（PTERA）

**版本**: 0.1.0-Alpha | **融合来源**: Claude（架构设计）× QClaw（执行实现）

---

## 快速开始

```bash
# 场景模拟：摔倒检测
python3 scripts/situation_assessor.py --simulate fall

# 场景模拟：迷路失联
python3 scripts/situation_assessor.py --simulate lost

# 执行引擎测试（L4级）
python3 scripts/action_executor.py --level L4 --simulate

# 生命体征监控测试
python3 scripts/vitals_monitor.py

# 广播协调器测试
python3 scripts/broadcast_coordinator.py
```

---

## 架构概览

```
SOS触发 ────────┐
                ↓
        situation_assessor    ← 量化评分 (0-100) → L1-L5
                ↓
        autonomous_decision   ← 复合信号升级 + 决策编排
                ↓
        action_executor       ← 录音 / 定位 / 通知 / 呼叫
                ↓
        broadcast_coordinator ← SMS / 电话 / 推送 / 无人机网络
                ↑
        vitals_monitor        ← 持续生命体征趋势监控（输入源）
```

---

详见 [SKILL.md](./SKILL.md) 完整文档。
