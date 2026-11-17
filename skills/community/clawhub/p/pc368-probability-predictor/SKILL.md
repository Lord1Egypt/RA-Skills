---
name: "pc368-probability-predictor"
description: "PC368开奖数据抓取+频率统计+冷号预测(最低概率)+热号TOP5方案+模型验证"
metadata:
  openclaw:
    emoji: "🔮"
    triggers:
      - "启动预测"
      - "跑预测"
      - "分析走势"
      - "预测下一期"
      - "pc368预测"
      - "冷号预测"
      - "热号预测"
      - "概率预测"
---

# PC368 概率预测分析器

## 触发条件
当用户表达以下意图时启动本技能（任一匹配即触发）：
- "启动预测"
- "跑预测"
- "分析走势"
- "预测下一期"
- "pc368预测"
- "冷号预测"
- "热号预测"
- "概率预测"
- 类似含义的指令

## 交互流程

启动预测时，你需要提供两个参数：
1. **训练期数 N**：用最新 N 期历史数据建频率库
2. **持续期数 M**：这个预测将对接下来 M 期未开奖期次生效

（注意：持续期数 M 是**未来跟踪**的概念，指这套频率模型对这 M 期有效，之后频率变化需要重新训练）

如果你启动时指定了训练期数（如"启动预测 300期"），我会接着问你：**"本次预测需要持续多久？"**

如果你说的是"启动预测"（没带数字），则会依次问：
1. **"训练期数设置多少？"**（默认 300）
2. **"本次预测需要持续多久？"**（默认 100）

你逐个回答后我再执行。

## 核心原理

本技能基于频率统计原理：在大量随机样本中，每个数字在每个位置上出现的概率理论上趋近于均等。

**方案A：冷号预测（追冷号）**：
出现频率最低的数字，在短周期内继续低概率出现的可能性较大。
1. 取最新 N 期数据每个位置（第1位、第2位、第3位）上各数字出现的频次
2. 对每个位置，选取出现频次最低的数字作为该位置的"最低概率预测"
3. 预测该最低频数字不会出现在接下来未开奖的期次中
4. 组合为 3 位预测 = [pos1_least, pos2_least, pos3_least]
5. （可选）用训练期之前的历史数据做滑动窗口验证，作为置信度

**方案B：热号TOP5预测（追热号）**：
出现频率最高的数字，在短周期内继续保持高频率的趋势较强。
1. 取最新 N 期数据每个位置（第1位、第2位、第3位）上各数字出现的频次
2. 对每个位置，选取出现频次最高的 TOP5 数字作为该位置的"热号范围"
3. 预测下一期的实际号码落在该 TOP5 范围内
4. （可选）用训练期之前的历史数据做滑动窗口验证，作为置信度

## 前置检查

技能启动后，检查以下条件：
1. 浏览器可用（检查 openclaw browser status）
2. 根据用户输入的N（训练期数）和M（持续期数）执行，默认N=300, M=100

## 整体流程

### 步骤1：启动浏览器并打开页面

使用 browser 工具打开：
```json
{"action":"open","url":"https://pc368.net/","label":"pc368-predict"}
```

等待页面加载完成后，用 evaluate 确认页面状态。

### 步骤2：关闭弹窗

首次访问可能有"知道了！"弹窗，用 evaluate 找到并点击关闭。

### 步骤3：提取表格数据

结果表格是页面上的第3个 table（table[2]）。提取数据：

```javascript
() => {
  const t2 = document.querySelectorAll('table')[2];
  const rows = t2.querySelectorAll('tr');
  const data = [];
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll('td');
    if (cells.length >= 3) {
      const issue = cells[0].textContent.trim();
      const numsStr = cells[1].textContent.trim();
      if (issue && /^\d+$/.test(issue) && numsStr.includes('+')) {
        data.push({issue, nums: numsStr});
      }
    }
  }
  return data;
}
```

### 步骤4：循环加载更多至足够条数

1. 用 evaluate 找到加载更多按钮：`document.querySelector('#addmore a')`
2. 滚动到视口并点击：`el.scrollIntoView({behavior:'instant',block:'center'}); el.click();`
3. 等待 2-3 秒，重新提取数据
4. 持续点击直到有效去重数据达到 N + M 期（默认 400 期）

### 步骤5：构建频率跟踪库（Node.js 层）

在 Node.js 层（或直接在 evaluate 中）构建频率库：

```javascript
function parseNums(str) {
  const m = str.match(/(\d+)\+(\d+)\+(\d+)=\d+/);
  return m ? [parseInt(m[1]), parseInt(m[2]), parseInt(m[3])] : null;
}

function buildFreqLib(data) {
  const freqMap = [null, new Map(), new Map(), new Map()];
  for (const d of data) {
    const nums = parseNums(d.nums);
    if (!nums) continue;
    for (let p = 0; p < 3; p++)
      freqMap[p+1].set(nums[p], (freqMap[p+1].get(nums[p]) || 0) + 1);
  }
  return {
    sortedByFreq: [null, ...freqMap.slice(1).map(m => [...m].sort((a,b) => a[1]-b[1]))],
    sortedByFreqDesc: [null, ...freqMap.slice(1).map(m => [...m].sort((a,b) => b[1]-a[1]))]
  };
}
```

### 步骤6：执行预测

**冷号预测**：取每个位置 `sortedByFreq[位置][0]` 的最低频数字
**热号TOP5**：取每个位置 `sortedByFreqDesc[位置].slice(0,5)` 的高频数字

### 步骤7：滑动窗口验证

用训练期之前的历史数据做滚动验证。训练集大小 N=300，最多验证 M=100 期。

### 步骤8：达标判断

**冷号方案**：全位准确率 >= 70% 或 综合位置准确率 >= 85%
**热号方案**：全位准确率 >= 80% 或 综合位置准确率 >= 90%

任一方案达标即视为模型有效。

### 步骤9：输出结果

```
📊 PC368 概率预测双方案分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━
📚 训练库：{N} 期
🧪 验证集：{testCount} 期

📐 频率分布...
━━━ 方案A：冷号预测（追冷号）━━━
🔮 最低概率组合预测：{coldPred}
🎯 冷号模型验证结果...

━━━ 方案B：热号TOP5预测（追热号）━━━
🔮 热号TOP5范围：{hotRanges}
🎯 热号模型验证结果...

📢 结论：{verdict}
```

## 准确率达标标准

### 冷号方案（追冷号）
- **全位准确率 >= 70%**：预测的 3 个最低概率数字全部未出现在对应位置的期数占比
- **综合位置准确率 >= 85%**：各位置分别预测正确的比例均值
- 两个条件满足其一即视为达标

### 热号方案（追热号）
- **全位准确率 >= 80%**：预测的 TOP5 范围全部覆盖了实际号码的期数占比
- **综合位置准确率 >= 90%**：各位置分别落在 TOP5 范围内的比例均值
- 两个条件满足其一即视为达标

## 边界情况处理

- **数据不足**：如果网站历史数据不足 N+M 期，尽量使用最大可用数据，并在报告中注明
- **浏览器问题**：如果 browser 不可用，报错并退出
- **弹窗干扰**：每次操作前确认无弹窗干扰
- **加载更多异常**：如果连续两次点击不增加数据，可能是已到历史尽头，使用当前数据
- **验证数据不足 M 期**：用实际可用的验证期数，达不到没关系，但结果要注明
