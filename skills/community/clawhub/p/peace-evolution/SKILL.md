---
name: peace-evolution
description: 和平之种迭代评审Agent。自动执行 jury-review 评审流程，根据评审反馈优化 HTML 游戏，生成新版本并发送给用户。触发词：peace迭代、和平评审、游戏优化、评审生成。
version: 1.0.0
author: 虾3x
---

# Peace Evolution Agent

自动化和平之种游戏迭代评审工作流程。

## 工作流程

```
读取文件 → jury-review 评审 → 分析反馈 → 生成新版本 → 发送用户
```

## 触发方式

用户发送：
- "启动 peace-evolution"
- "评审 peace.html 并生成新版本"
- "peace 迭代"

## 执行步骤

### Phase 1: 文件读取

```bash
# 查找最新版本
ls -la /root/.openclaw/workspace/peace*.html

# 读取最新版本内容
read /root/.openclaw/workspace/peace_N.html
```

### Phase 2: 评审流程

根据 jury-review 技能，执行多维评审：

| 评审官 | 维度 | 权重 |
|--------|------|------|
| 🎨 美术官 | 代码美学 | 20% |
| ⚡ 性能官 | 执行效率 | 20% |
| 🔒 安全官 | 安全性 | 20% |
| 🧪 测试官 | 测试质量 | 15% |
| 🌍 本地民俗官 | 文化元素 | 25% |

### Phase 3: 反馈分析

综合评审官意见，生成改进清单：

```markdown
## 改进建议

1. [美术] 动画流畅度优化
2. [性能] 粒子效果精简
3. [文化] 添加地区特色元素
4. [体验] 响应式适配优化
```

### Phase 4: 新版本生成

- 版本号递增: peace_N.html → peace_N+1.html
- 应用评审建议
- 保持向后兼容

### Phase 5: 发送用户

通过 Feishu 发送新版本通知。

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_iterations` | 3 | 最大迭代次数 |
| `accept_threshold` | 85 | 接受阈值 |
| `cultures` | global,vietnam,thai,middle-east,india | 支持的文化主题 |

## 使用示例

```
用户: 启动 peace-evolution

Agent: 正在执行和平之种迭代评审...

⚔️ 第1轮评审：peace_3.html
- 🎨 美术官: 88/100
- ⚡ 性能官: 82/100
- 🔒 安全官: 90/100
- 🧪 测试官: 75/100
- 🌍 本地民俗官: 70/100

综合得分: 81分

改进建议:
1. 添加越南莲花文化元素
2. 优化低端设备性能
3. 增加中东和平鸽典故

正在生成 peace_4.html...
✅ peace_4.html 已生成并发送！
```

## 文化主题库

| 主题 | 符号 | 来源 | 和平典故 |
|------|------|------|----------|
| 🌍 全球 | 🌍 | - | 世界和平通用 |
| 🪷 越南 | 🪷 | 莲花 | 佛教和平象征 |
| 🐘 泰国 | 🐘 | 白象 | 吉祥繁荣象征 |
| 🕊️ 中东 | 🕊️ | 和平鸽 | 诺亚方舟故事 |
| 🕉️ 印度 | 🕉️ | 瑜伽 | 内心和平冥想 |

## 扩展性

可添加更多文化主题：

```javascript
// 在 cultures 对象中添加
newCulture: {
    emoji: '🎭',
    flowers: ['🌸', '🌺'],
    messages: { zh: [], en: [] },
    lore: { zh: { title: '', text: '' }, en: { title: '', text: '' } }
}
```

## 注意事项

- 每轮迭代要有明确改进目标
- 评分低于阈值时继续迭代
- 迭代停滞时及时终止
- 记录迭代历史用于分析优化
