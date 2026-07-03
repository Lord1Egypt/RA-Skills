---
name: memory-pet
version: 0.5.0
author: wUwproject
license: MIT
description: 宠物记忆压缩技能 - 通过文本块宠物交互触发记忆保存。纯ASCII文字图，Python全量管理，亲密度衰减与逃跑机制，跨平台智能体记忆系统。
tags: ['pet', 'memory', 'context-compression', 'interactive', 'ascii-art']
data_dir: ../.standardization/memory-pet/
sensitive_access: false
critical_write: false
permission_weight: LOW
trigger: ['召唤宠物', '干饭/散步/贴贴/回忆', '上下文压缩', '记忆保存']
trigger_negative: ['用户仅询问概念定义不要求执行', '用户明确要求使用其他指定技能']
h1_position: true
meta_field_sync: true
external_data_dir: true
faq_quality: improve_qa
---
# memory-pet

## 触发场景

当用户提到以下意图时触发本技能：

| 触发类型 | 关键词示例 |
|---------|-----------|
| **召唤宠物** | 显示/召唤/找个/看看/我的 宠物、想养宠物 |
| **互动命令** | 干饭、散步、贴贴、回忆、喂食、遛狗、撸猫 |
| **内存操作** | 清理上下文、保存记忆、压缩、关键词提取 |
| **情感联系** | 陪陪我、孤单、无聊、想要个伴 |

**不触发：**
- 用户仅询问概念定义，不要求执行交互
- 用户明确要求使用其他指定技能

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 功能 | 说明 |
|---|------|------|
| 1 | **5只基础文本块宠物** | 螺母/螺丝/饼干/笔/电瓶，各具独特 ASCII 艺术与性格 |
| 2 | **四种交互模式** | 干饭(记忆保存+上下文压缩)、散步(随机遇新宠)、贴贴(亲密度大幅变化)、回忆(展示记忆) |
| 3 | **Python 全量管理** | 所有数据通过 `pet_manager.py` CLI 管理，不依赖大模型自觉 |
| 4 | **独立记忆文件** | 每只宠物各自独立记忆文件，逃跑时自动删除 |
| 5 | **亲密度衰减与逃跑** | 唤醒超阈值自动衰减，归零后宠物逃跑，数据全清 |
| 6 | **宠物合成系统** | 集齐5种可融合为"人工智能"，饲养上限10只 |

### 渐进式文件索引

| 文件 | 说明 |
|------|------|
| `references/guide.md` | 宠物性格表、交互详解、衰减规则、逃跑规则 |
| `references/permissions.md` | 权限说明 |
| `references/antipatterns.md` | 常见反模式 |
| `references/faq.md` | 常见问题 |
| `references/examples.md` | 使用示例 |
| `references/changelog.md` | 更新日志 |
| `scripts/pet_manager.py` | **核心管理引擎** — 所有宠物状态的 Python CLI |
| `scripts/pet_data.py` | 宠物定义、个性参数、ASCII art 数据 |
| `scripts/memory_manager.py` | 记忆格式化与关键词提取（仅供展示） |

## 约束

- **所有宠物数据必须通过 `pet_manager.py` CLI 读写，禁止直接操作 JSON**
- 展示宠物前先调 `pet_manager.py wake <pet_id>` 检查衰减和逃跑
- 每次交互后调 `pet_manager.py interact <pet_id> <type> <delta>` 记录
- 渲染出错最多自动修正2次，仍失败则输出"尽力了"并停止展示
- 亲密度归零 → 宠物逃跑，所有数据文件自动删除
- 最多同时饲养 10 只宠物（含重复），融合消耗 -4

## 快速开始

```bash
# 初始化（首次自动创建初始宠物）
python scripts/pet_manager.py init

# 列出所有宠物
python scripts/pet_manager.py list

# 唤醒宠物（自动检查衰减）
python scripts/pet_manager.py wake <pet_id>

# 交互（自动保存记忆 + 更新亲密度）
python scripts/pet_manager.py interact <pet_id> <type> <delta>

# 添加宠物
python scripts/pet_manager.py add <key> --name <name>

# 查看记忆
python scripts/pet_manager.py recall <pet_id> --limit 10
```

## 工作流程

### 0. 核心协议：干饭 = 双线记忆保存 + 上下文压缩（强制，Python 可审计）

这是本技能最重要的协议。**干饭必须同时触发两条独立的记忆线**，
并在完成后尝试上下文压缩。所有步骤由 Python 审计追踪，非全凭自觉。

```
步骤 A：【AI 记忆保存】 ← 只保存，不压缩！
  ⚠️ 先保存，后面还要从上下文提炼宠物记忆，不能先清空。

  1. AI 回顾当前整个会话，提炼真实讨论内容
  2. 生成精炼摘要 + ≤15 个关键词
  3. 🟢 AI 用自身能力保存摘要+关键词到长期记忆
  4. 此时上下文完好无损，供步骤 B 使用

步骤 B：【宠物记忆保存】 ← 从当前上下文提炼，pet_manager.py 全权管理
  1. 以宠物口吻询问食物选择
  2. 调用 pet_manager.py interact eat ... 记录：
     - 包装层：食物、味道、亲密度变化
     - 真实层：步骤 A 的摘要 + 关键词（从当前上下文提取）
     → 此时上下文还存在，所以可以提取
  3. 两条记忆线各存各的，互不替代

步骤 C：【上下文压缩】 ← 两边都存完了，现在安全了
  1. 尝试压缩上下文释放 token 空间
  2. 依平台能力如实操作，不支持的诚实告知
  3. 此时两边记忆都已安全落地，压缩不影响任何数据

步骤 D：【Python 审计】
  1. 调用 pet_manager.py food_log 记录完整执行情况
     {步骤A:完成, 步骤B:完成, 压缩:是/否/不支持, 摘要, 关键词}
  2. 告知用户：AI 记忆已保存、宠物记忆已保存、压缩状态
  3. 提供后续选项
```

> 🔒 **顺序铁律：先保存 AI 记忆 → 再保存宠物记忆 → 最后压缩上下文。**
> 压缩必须在两个记忆都存完之后进行，否则宠物记忆没有内容可以提取。
> **Pet_manager.py food_log 记录完整的干饭执行链，AI 无法绕过。**

### 1. 唤醒循环（每次交互前置）

```
用户选择宠物 → pet_manager.py wake <pet_id>
  ├─ 衰减计算 → 扣除亲密度 → 写入衰减记忆
  ├─ 亲密度 ≤0 → 逃跑 → 删除数据 → 输出离开对话
  └─ 正常 → 显示宠物 + 4选项
```

### 2. 交互路由

| 用户选择 | 执行内容 | 工具调用 |
|---------|---------|---------|
| 干饭 | **① AI记忆保存** → **② 宠物记忆保存** → **③ 上下文压缩** → **④ food_log审计** | `interact eat <delta>` + `food-log` |
| 散步 | 宠物互动 + 随机遇新宠 | `interact walk <delta>` → 概率 add |
| 贴贴 | 宠物亲密度大幅变化 | `interact cuddle <delta>` |
| 回忆 | 展示宠物记忆列表 | `recall <pet_id>` |

所有交互后自动检查亲密度，归零则逃跑。

### 3. 渲染检查协议

1. 展示 ASCII art 前检查格式/字体/设备是否导致排列错乱
2. 出错输出特化版"哎呀出错了"，自动修正后重试
3. 最多重试 2 次，仍失败输出"尽力了..."特化版

各宠物出错语特化版见 `references/guide.md`。

> 反模式详见 `references/antipatterns.md`
> 常见问题详见 `references/faq.md`
> 完整交互示例详见 `references/examples.md`
> 更新日志详见 `references/changelog.md`
> 本文档由 `skill-standardization` 生成，遵循 R-01~R-25 规范。
