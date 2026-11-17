---
name: "pc368-filter-analyzer"
description: "打开PC368网站抓取开奖数据，按尾数匹配筛选，排除三重/三连号，统计占比与计算盈亏"
metadata:
  openclaw:
    emoji: "🔍"
    triggers:
      - "启动筛选"
      - "开始统计"
      - "分析PC368"
      - "跑筛选"
      - "筛选统计"
      - "pc368统计"
---

# PC368 数据筛选分析器

## 触发条件
当用户明确表达以下意图时启动本技能（任一匹配即触发）：
- "启动筛选"
- "开始统计"
- "分析PC368"
- "跑筛选"
- "筛选统计"
- "pc368统计"
- 类似含义的指令

## 前置询问

技能启动后，先向用户确认以下两项信息（必须获取后才能继续）：

1. **3个合数**：请用户提供3个独立的数字（作为尾数匹配目标）。需验证每个数字为合数（大于1且非质数）。常见一位合数：4、6、8、9。若用户提供非合数，提醒并重新询问。
2. **统计期数 X**：用户希望统计最近多少期已开奖结果。

确认格式示例：
> 请提供3个合数（如4,6,8）和本次统计期数X（如60）。

## 整体流程

### 步骤1：启动浏览器并打开页面

确保浏览器已启动，然后打开 https://pc368.net/：

使用 browser 工具打开：
```json
{"action":"open","url":"https://pc368.net/","label":"pc368-screener"}
```

等待页面加载后，用 snapshot 或 evaluate 确认页面状态。

### 步骤2：关闭弹窗

首次访问可能有"知道了！"弹窗，先尝试关闭：

1. 先snapshot获取页面状态
2. 如果存在弹窗按钮，用 evaluate 找到并点击关闭（按钮文本通常是"知道了！"）
3. 弹窗关闭后重新 snapshot 确认

若弹窗已关闭或无弹窗，直接继续。

### 步骤3：提取表格数据

找到结果表格（通常是页面上的第3个 table，即 document.querySelectorAll('table')[2]），提取数据：

```javascript
() => {
  const t2 = document.querySelectorAll('table')[2];
  const rows = t2.querySelectorAll('tr');
  const data = [];
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll('td');
    if (cells.length >= 3) {
      const issue = cells[0].textContent.trim();
      const nums = cells[2] || cells[1];
      const numsStr = (nums ? nums.textContent.trim() : '');
      if (issue && !isNaN(parseInt(issue)) && numsStr.includes('+')) {
        data.push({issue, time: cells[1]?.textContent?.trim() || '', nums: numsStr});
      }
    }
  }
  return data;
}
```

### 步骤4：循环加载更多（如数据不足X条）

当前页面默认显示约30条数据。每次点击"加载更多"约增加30条。

如果当前提取的数据中有效条数不足 X 条：

1. 用 evaluate 找到加载更多元素：`document.getElementById('addmore')` 或 `document.querySelector('#addmore a')`
2. 点击之：`el.scrollIntoView({behavior:'instant',block:'center'}); el.click();`
3. 等待 2-3 秒（Start-Sleep 或延迟）
4. 重新 evaluate 提取数据
5. 重复直到有效数据 >= X 条

**注意**：每次加载更多后需要重新提取全部数据，因为表格会追加新行。

### 步骤5：数据解析与筛选（在 evaluate 中完成）

在获取到 X 条有效数据后，执行筛选计算。注意先去重（按期号 issue 去重，保留首次出现）。

筛选逻辑：
1. 解析号码格式 "a+b+c=sum" → [a, b, c]
2. 排除三重数（三个数字相同）和三连号（排序后差为1）
3. 对剩余数据，计算两两相加的尾数：[ (a+b)%10, (a+c)%10, (b+c)%10 ]
4. 匹配用户提供的3个合数尾数
5. 计算盈亏：matched × 995 - total × 630

完整的 evaluate 函数参考技能详细说明。

### 步骤6：输出结果

```
📊 PC368 筛选统计结果
━━━━━━━━━━━━━━━━━━━━━━
统计期数范围：{startIssue} 期 至 {endIssue} 期（共 {xPeriods} 期）

目标合数：{a}, {b}, {c}

✅ 符合条件的期数：{matchedPeriods} 期
❌ 排除的期数（三重/三连）：{excludedPeriods} 期
📈 占 {xPeriods} 期总数的：{percentage}

💰 盈亏计算：
{matchedPeriods} × 995 - {xPeriods} × 630 = {profit} 元
━━━━━━━━━━━━━━━━━━━━━━
```

### 步骤7：清理

任务完成后，关闭浏览器标签（如有需要）。

## 边界情况处理

- **浏览器未启动**：先用 openclaw browser status 检查，必要时 start
- **弹窗干扰**：每次操作前确认弹窗已关闭
- **加载更多点击失败**：若 id=addmore 元素失效，尝试用 evaluate 直接触发 click
- **数据不足X条**：如果加载到历史尽头仍不足X条，使用实际可用的数据量，并在结果中注明
- **网络异常**：等待页面加载完成，必要时重试

## 合数验证规则

一位数合数：4, 6, 8, 9
其他数字（0,1,2,3,5,7）不是合数，需要提醒用户重新选择。
