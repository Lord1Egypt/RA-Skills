# Logic Inversion Reflector (LIR-v2)

🧠 **认知扰动引擎** - 强制进入"系统 2"思考模式

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 核心使命

**不是优化结果，而是通过逻辑归谬和本体论追问，强制用户进入"系统 2"思考模式。**

---

## 🚀 快速开始

### 命令行使用
```bash
cd skills/logic-inversion-reflector
python3 src/reflector.py "你的方案/想法"
```

### Python 代码
```python
from src.reflector import reflect

result = reflect("我们应该选择核心业务作为试点")
print(result)
```

### 输出示例
```json
{
  "Original_Anchors": ["试点应该选择核心业务"],
  "Inversion_Model": {
    "Counter_Axiom": "试点不应该选择核心业务",
    "Logic_Deduction": "边缘业务失败成本低→可以更大胆创新→可能产生颠覆性突破",
    "Synthetic_Conflict": "你的'稳妥'策略可能错过了真正的颠覆机会"
  },
  "Meta_Probes": [
    "选择核心业务是为了业务价值，还是为了让你自己对结果可控？",
    "如果 AI 技术成本突然下降 100 倍，你的策略会不会变成'缓慢自杀'？"
  ],
  "System_Lock": "WAIT_FOR_HUMAN_JUDGEMENT"
}
```

---

## 🧠 工作原理

### 三个阶段

#### 1️⃣ 特征提取
扫描用户方案，提取 3-5 个核心假设锚点（那些被视为"理所当然"的公理）

#### 2️⃣ 公理反转
对每个锚点执行 NOT 运算，推演内部逻辑自洽的竞争方案

#### 3️⃣ 元坐标追问
抛出 2 个探测脉冲：
- **动机审计**: 是为了解决问题，还是缓解对"不可控"的恐惧？
- **边界压力**: 环境参数极值变化时，方案如何从"药"变"毒"？

---

## 💡 应用场景

### ✅ 适用
- 重大战略决策前
- 团队共识过于一致时
- 陷入思维死胡同时
- 需要深度思考时

### ❌ 不适用
- 紧急决策（需要快速行动）
- 执行细节讨论
- 已经过充分辩论的决策

---

## 📚 完整文档

- [使用手册](skills/logic-inversion-reflector/SKILL.md)
- [使用示例](skills/logic-inversion-reflector/examples/usage_examples.md)

---

## 🧪 测试

```bash
cd skills/logic-inversion-reflector
python3 tests/test_reflector.py
```

---

## 🔧 技术细节

### 核心组件
- `src/reflector.py` - 核心逻辑实现
- `src/prompts.py` - Prompt 模板（可扩展）
- `tests/test_reflector.py` - 单元测试

### 依赖
- Python 3.8+
- 无外部依赖

### 性能
- 响应时间：< 3 秒
- Token 消耗：~500-800 tokens/次

---

## 🎓 理论基础

- 丹尼尔·卡尼曼《思考，快与慢》- 系统 1 vs 系统 2
- 纳西姆·塔勒布《反脆弱》- 从不确定性中受益
- 查理·芒格的"逆向思考" - 反过来想

---

## 📝 示例

### 示例 1: 组织设计
**输入**: "管理者应该从管人转向管 Agent"

**输出**: 挑战"扁平化优于科层制"的假设，揭示中层管理者的隐性价值

### 示例 2: 激励机制
**输入**: "AI 贡献应该与绩效挂钩"

**输出**: 质疑"挂钩绩效"的动机，警示"指标博弈"风险

### 示例 3: 技术选型
**输入**: "应该自研 AI 模型"

**输出**: 挑战"自主可控"思维，提出"专注业务"的替代方案

更多示例见 [usage_examples.md](skills/logic-inversion-reflector/examples/usage_examples.md)

---

## ⚠️ 风险提示

- 可能引起不适（被挑战的感觉）
- 可能延缓决策速度
- 可能产生分析瘫痪
- 需要用户有足够的心理安全感

**建议**: 从小的决策开始练习，逐渐建立"被挑战"的肌肉记忆。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 待办事项
- [ ] 扩展公理库（目前 16 个常见公理）
- [ ] 添加更多逻辑推导模板
- [ ] 支持自定义公理
- [ ] 集成到飞书机器人
- [ ] 添加 Web 界面

---

## 📄 License

MIT License

---

## 🙏 致谢

灵感来源于：
- 丹尼尔·卡尼曼《思考，快与慢》
- 纳西姆·塔勒布《反脆弱》
- 查理·芒格的"逆向思考"

---

## 📬 联系方式

- **作者**: Alex Wang
- **邮箱**: alex.wang@dida.com
- **GitHub**: [@tuobadaidai](https://github.com/tuobadaidai)

---

**记住**: LIR 的目标不是证明你错了，而是帮助你看到盲点。🎯
