---
name: GitHub Development Standard
description: 完整的 GitHub 项目开发标准流程 - 9步流程 + 4层验证 + 15项验收清单
---

# GitHub Development Standard v2.0

> **用方法论驯服低端模型，让代码质量不再妥协**

## 💡 核心价值

解决低端模型在代码开发中的常见问题：
- ❌ 过度修改（200+ 行，夹带重构）
- ❌ 无验证（直接说"修好了"）
- ❌ 夹带私货（顺便优化、重构）

## 📋 9 步开发流程

```
1. 读 issue → 2. 写任务卡 → 3. 确定基线
     ↓
4. 列改动点 → 5. 编码 → 6. 本地验证
     ↓
7. 看 diff → 8. 写发布说明 → 9. 复盘
```

## ✅ 8 条编码纪律

1. 先复制旧代码，再局部替换
2. 改函数前，先通读输入/输出/副作用
3. 涉及数据结构变化时，先搜所有使用点
4. 不要同时改逻辑和风格
5. 不要在 bug fix 里做重构
6. 不要修改未被需求要求的行为
7. 不要在没有验证前说"修好了"
8. 不要让 release note 超前于实际代码

## 🔍 4 层验证

```bash
# Layer 1: 语法验证
python3 -m py_compile scripts/xxx.py

# Layer 2: 导入验证
python3 -c "from scripts.xxx import ClassName"

# Layer 3: 行为验证
python3 test_fix.py

# Layer 4: 回归验证
python3 -m pytest tests/
```

## 📊 15 项验收清单

### A. 需求一致性（3 项）
- [ ] A1. 我能用一句话说清这次修复的目标
- [ ] A2. 我知道这次"不打算修"的内容有哪些
- [ ] A3. 代码改动与 issue 描述一致

### B. 技术正确性（4 项）
- [ ] B1. 我基于正确版本开始修改
- [ ] B2. 我没有重写整个文件
- [ ] B3. 数据结构变化已同步所有引用点
- [ ] B4. 新逻辑不会破坏旧逻辑

### C. 测试验证（4 项）
- [ ] C1. 语法检查通过
- [ ] C2. 导入检查通过
- [ ] C3. 最小样例验证通过
- [ ] C4. 回归测试通过

### D. 发布质量（4 项）
- [ ] D1. diff 大小与任务规模匹配
- [ ] D2. release note 与实际代码一致
- [ ] D3. 版本号、文档、注释已同步
- [ ] D4. 我可以指出这次改动的风险点

## 🔧 GitHub CLI 使用

```bash
# 查看 Issue
gh issue view 53 --repo owner/repo

# 评论 Issue
gh issue comment 53 --repo owner/repo --body "修复说明..."

# 关闭 Issue
gh issue close 53 --repo owner/repo
```

## 📄 多文件修复注意事项

1. **同步修改** - 修改 README.md 时，检查其他语言版本
2. **工具验证** - 用 `grep` 等工具验证比人工更可靠
3. **文档清理** - 先整合内容，再删除冗余文件

## 📊 效果对比

| 指标 | 使用前 | 使用后 | 提升 |
|------|--------|--------|------|
| Bug 修复返工率 | 60% | 5% | **↓ 55%** |
| 平均改动量 | 200+ 行 | 15 行 | **↓ 185 行** |
| 夹带私货率 | 70% | 0% | **↓ 70%** |

## 💡 核心理念

> **先定义问题，再定义改法，再写代码，再做验证，最后才发布。**

## 🔗 相关链接

- **GitHub**: https://github.com/SonicBotMan/github-development-standard
- **ClawHub**: https://clawhub.com/skills/github-development-standard

---

**让代码质量不再妥协** 💕
