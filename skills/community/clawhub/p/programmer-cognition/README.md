# programmer-cognition

> 程序员认知 Skill —— SOUL五律适配软件开发，让Agent用程序员的思维方式写代码、审代码、调Bug

**作者**: KingOfZhao  
**版本**: 1.0.0  
**发布日期**: 2026-03-31  
**许可证**: MIT

---

## 解决什么问题？

Agent写代码时经常：不检查依赖、不处理边缘case、不写测试、裸except、硬编码密钥。
`programmer-cognition` 把SOUL五律转化为程序员的日常实践：

- **已知/未知** → 写代码前明确输入契约和边缘case
- **四向碰撞** → Code Review从4个方向碰撞
- **人机闭环** → CI自动测试 → 人工Review → 生产验证
- **文件即记忆** → docstring + CHANGELOG + debug日志
- **置信度+红线** → 6条程序员红线永不触碰

## 核心特色

- 🔍 四向代码碰撞（正面正确性/反面失败场景/侧面复用性/整体架构一致性）
- 🐛 调试方法论（禁止猜→试，强制假设验证）
- 🚀 部署Checklist（7项强制检查）
- 🔴 6条程序员红线（不硬编码密钥、不裸except、不跳过测试...）

## 快速安装

```bash
clawhub install programmer-cognition
```

## 变更日志

### v1.0.0 (2026-03-31)
- Skill工厂自动生成（skill-collision-engine碰撞产出）
- self-evolution × human-ai-closed-loop → 程序员专用
- 四向代码碰撞 + 调试方法论 + 部署红线
- 通过自验证: 96%

---

*自动开源认知 Skill by Skill Factory — KingOfZhao*
