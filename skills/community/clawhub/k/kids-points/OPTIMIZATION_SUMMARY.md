# 📝 kids-points 积分系统优化清单

> **优化日期**: 2026-03-23  
> **当前版本**: v1.2  
> **目标版本**: v1.3  

---

## ✅ 已完成优化

### 1. Bug 修复：积分消费识别失败

**问题描述**:
- `handleExpenseInput` 函数中金额提取正则表达式有误
- 正则 `/(\d+)\s*(分 | pts|ポイント)/` 中"分"后面多了一个空格
- 导致"积分消费 忘带书包花了 5 分"无法识别（"5 分"后无空格）

**修复内容**:
- 文件：`scripts/handler.js` 第 473 行
- 修改前：`const amountMatch = input.match(/(\d+)\s*(分 | pts|ポイント)/);`
- 修改后：`const amountMatch = input.match(/(\d+)\s*(分|pts|ポイント)/);`

**测试验证**:
```bash
node scripts/index.js "积分消费 买零食花了 20 分"  # ✅ 成功
node scripts/index.js "积分消费 忘带书包花了 5 分"  # ✅ 成功
```

---

### 2. Bug 修复：积分消费无语音播报

**问题描述**:
- `handleExpenseInput` 函数缺少语音播报功能
- 消费记录后没有语音反馈
- 响应消息中总是显示"配置 API Key 后可解锁语音功能"提示（即使 API Key 已配置）

**修复内容**:
1. **文件**: `scripts/handler.js` `handleExpenseInput` 函数
   - 添加语音播报逻辑（与 `handlePointsInput` 一致）
   - 语音文案：`好的，已记录消费${amount}分，${description}。要合理消费哦！`

2. **文件**: `scripts/handler.js` `handleExpenseInput` 函数
   - 移除默认添加的 `t('voiceHint', 'zh')`
   - 仅在 API Key 未配置时显示语音配置提示

**修改对比**:
```javascript
// 修改前（消费无语音）
response = `✅ **${t('expenseRecorded', 'zh')}**\n\n`;
response += `💸 **支出**: ${amount}分\n`;
response += `📝 **用途**: ${description}\n\n`;
response += `_已自动记入账本_\n\n`;
response += t('voiceHint', 'zh');  // ❌ 总是显示提示

// 修改后（消费有语音）
response = `✅ **${t('expenseRecorded', 'zh')}**\n\n`;
response += `💸 **支出**: ${amount}分\n`;
response += `📝 **用途**: ${description}\n\n`;
response += `_已自动记入账本_\n\n`;
// ✅ 移除默认提示

// 语音播报（仅中文）
if (lang === 'zh') {
  const ttsText = `好的，已记录消费${amount}分，${description}。要合理消费哦！`;
  playTTS(ttsText, (error, stdout, stderr) => {
    if (stderr === 'API_KEY_NOT_CONFIGURED') {
      response += t('voiceHint', 'zh');  // ✅ 仅在需要时显示
    }
  });
}
```

**测试验证**:
```bash
# 测试消费播报
node scripts/index.js "积分消费 买零食花了 20 分"
# 预期：
# - 文字消息正常显示
# - 语音自动播放："好的，已记录消费 20 分，买零食花了 20 分。要合理消费哦！"
# - 不显示"配置 API Key"提示

# 检查音频文件
ls -lt workspace/audio/2026-03-23/
# 预期：生成新的 WAV 文件
```

**修复状态**: ✅ 已完成
- 语音文件生成正常
- 播放功能正常
- 提示语显示正常

---

## 🔧 待实现优化（v1.3 核心功能）

### 3. 新积分规则：月度消费额度制（简化版）

#### 3.1 规则变更说明

| 项目 | 旧规则 | 新规则（v1.3） |
|------|--------|---------------|
| **400 分上限含义** | 每月最多赚取 400 分 | 每月最多消费 400 分 |
| **积分获取** | 有上限（400 分/月） | **无上限**，可无限赚取 |
| **积分清零** | 不清零，可累积 | **积分不清零**，可累积到下月 |
| **消费额度** | 无明确额度概念 | **每月 1 号重置为 400 分** |
| **额度结转** | 不适用 | **不结转**，月底清零 |
| **超额消费** | 不允许 | **允许**，记录为"欠费" |

#### 3.2 欠费记录机制（简化版）

**规则**:
- 每月消费额度：400 分
- 平时消费：**不检查额度**，正常记录
- 每月 1 号：检查上月总支出
- 如果超额：记录"欠费"，从本月额度中扣除
- **无惩罚系数**：1:1 结转欠费

**计算公式**:
```
本月可用额度 = 400 - 上月欠费
```

**示例**:
```
场景：3 月消费了 450 分（超额 50 分）

4 月 1 日重置时：
- 本月新额度：400 分
- 上月欠费：50 分
- 实际可用：400 - 50 = 350 分

提示：
📊 4 月积分额度重置
   本月额度：400 分
   上月欠费：-50 分
   实际可用：350 分
```

---

### 4. 需要修改的文件清单

#### 4.1 核心逻辑文件

| 文件 | 修改内容 | 优先级 |
|------|----------|--------|
| `scripts/handler.js` | 新增 `checkMonthlyOverdraft()` 函数（每月 1 号检查欠费） | 🔴 高 |
| `scripts/handler.js` | 修改 `createMonthlyLog()` 添加欠费字段 | 🔴 高 |
| `config/rules.json` | 添加 `monthlySpendingLimit: 400` 配置 | 🔴 高 |

#### 4.2 报表生成文件

| 文件 | 修改内容 | 优先级 |
|------|----------|--------|
| `scripts/generate-daily-report.js` | 显示"本月可用额度"（400 - 上月欠费） | 🟡 中 |
| `scripts/generate-daily-report.js` | 添加"上月欠费"字段（如有） | 🟡 中 |

#### 4.3 文档文件

| 文件 | 修改内容 | 优先级 |
|------|----------|--------|
| `SKILL.md` | 更新版本号为 v1.3，添加更新说明 | 🟡 中 |
| `RULES.md` | 重写"基本规则"章节，说明新额度制 | 🟡 中 |
| `README.md` | 更新核心机制说明 | 🟡 中 |

---

### 5. 详细修改方案

#### 5.1 `config/rules.json` 修改

```json
{
  "version": "1.3",
  "lastUpdated": "2026-03-23",
  "rules": {
    "tasks": { ... },
    "limits": {
      "monthlySpendingLimit": 400,
      "monthlyEarningLimit": null,
      "resetDay": 1
    },
    "schedule": { ... }
  }
}
```

#### 5.2 `scripts/handler.js` 新增函数

```javascript
/**
 * 检查并记录上月欠费
 * 在每月 1 号调用，从上月账本读取总支出，计算欠费
 */
function checkMonthlyOverdraft() {
  const lastMonthStr = getLastMonthStr();  // 获取上月月份 (YYYY-MM)
  const currentMonthStr = getMonthStr();   // 当前月份
  
  // 读取上月账本
  const lastMonthLog = loadMonthlyLog(lastMonthStr);
  const expenseMatch = lastMonthLog.match(/总支出 \| (\d+) 分/);
  
  if (!expenseMatch) return null;  // 上月无支出记录
  
  const lastMonthExpense = parseInt(expenseMatch[1]);
  const spendingLimit = 400;
  const overdraft = Math.max(0, lastMonthExpense - spendingLimit);
  
  if (overdraft > 0) {
    // 记录欠费到本月账本
    const currentLog = loadMonthlyLog(currentMonthStr);
    // 在 currentLog 中添加欠费记录
    // ...
    
    return {
      lastMonthExpense,
      spendingLimit,
      overdraft,
      availableLimit: spendingLimit - overdraft
    };
  }
  
  return null;  // 无欠费
}

/**
 * 获取上月月份字符串
 */
function getLastMonthStr() {
  const now = new Date();
  const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  return `${lastMonth.getFullYear()}-${String(lastMonth.getMonth() + 1).padStart(2, '0')}`;
}
```

#### 5.3 每月 1 号自动检查

**方案 A**: 定时任务（推荐）
```bash
# crontab 配置
0 8 1 * * cd ~/.openclaw/agents/kids-study/workspace && node scripts/check-overdraft.js
```

**方案 B**: 懒加载（首次查询时检查）
```javascript
// 在 generateDailyReport() 中检查
function generateDailyReport() {
  const today = getTodayStr();
  const isMonthStart = today.endsWith('-01');  // 每月 1 号
  
  if (isMonthStart) {
    const overdraft = checkMonthlyOverdraft();
    if (overdraft) {
      // 显示欠费提示
    }
  }
  // ...
}
```

---

### 6. 测试用例

#### 6.1 正常月份测试
```bash
# 3 月消费 350 分（未超额）
# 4 月 1 日检查
# 预期：无欠费，4 月可用额度 400 分
```

#### 6.2 超额月份测试
```bash
# 3 月消费 450 分（超额 50 分）
# 4 月 1 日检查
# 预期：欠费 50 分，4 月可用额度 350 分
```

#### 6.3 边界测试
```bash
# 3 月消费 400 分（刚好）
# 4 月 1 日检查
# 预期：无欠费，4 月可用额度 400 分
```

---

### 7. 发布前检查清单

#### 代码层面
- [ ] `handler.js` 添加 `checkMonthlyOverdraft()` 函数
- [ ] `handler.js` 添加 `getLastMonthStr()` 函数
- [ ] `handler.js` 修改 `createMonthlyLog()` 添加欠费字段
- [ ] `config/rules.json` 更新配置
- [ ] `generate-daily-report.js` 更新显示逻辑
- [ ] 所有测试用例通过

#### 文档层面
- [ ] `SKILL.md` 更新版本号和更新说明
- [ ] `RULES.md` 重写基本规则章节
- [ ] `README.md` 更新核心机制

#### 测试层面
- [ ] 正常月份测试
- [ ] 超额月份测试
- [ ] 边界条件测试（刚好 400 分）
- [ ] 月度重置测试（模拟 4 月 1 日）

---

### 8. ClawHub 发布信息

```bash
clawhub publish ./skills/kids-points \
  --slug kids-points \
  --name "孩子积分管理" \
  --version 1.3.0 \
  --changelog "v1.3: 月度消费额度制 + 欠费自动结转 + 修复消费识别/语音播报 bug"
```

**更新说明**:
```markdown
## v1.3.0 重大更新

### 🎯 核心机制变更
- **月度消费额度制**: 400 分从"赚取上限"改为"消费额度"
- **积分无上限**: 可以无限赚取积分，累积到下月
- **额度月清**: 每月 1 号重置消费额度，不结转

### 💰 欠费结转
- 超额消费不收取惩罚
- 欠费自动结转到下月
- 从下月额度中扣除

### 🐛 Bug 修复
- 修复"积分消费"识别失败问题（正则表达式空格 bug）
- 修复"积分消费"无语音播报问题

### 📊 报表优化
- 日报显示"本月可用额度"和"上月欠费"
- 月度账本添加欠费记录字段
```

---

## 9. 用户确认项

✅ **已确认**:
1. 超额倍率：**无惩罚**（1:1 结转欠费）
2. 月度重置日：每月 1 号
3. 额度结转：不结转（月底清零）
4. 实现方式：每月 1 号检查欠费并记录

---

## 10. 实现状态

### ✅ 已完成
| 功能 | 状态 | 测试 |
|------|------|------|
| Bug 修复：消费识别失败 | ✅ 完成 | ✅ 通过 |
| Bug 修复：消费无语音播报 | ✅ 完成 | ✅ 通过 |
| 配置更新：rules.json v1.3 | ✅ 完成 | ✅ 通过 |
| 新增函数：checkMonthlyOverdraft() | ✅ 完成 | ✅ 通过 |
| 新增函数：getLastMonthStr() | ✅ 完成 | ✅ 通过 |
| 日报更新：显示可用额度 | ✅ 完成 | ✅ 通过 |
| 脚本：check-overdraft.js | ✅ 完成 | ✅ 通过 |
| 文档：SKILL.md v1.3 | ✅ 完成 | - |
| 文档：RULES.md v1.3 | ✅ 完成 | - |
| 测试脚本：test-v1.3.js | ✅ 完成 | ✅ 通过 |

### 📋 测试用例结果
| 测试项 | 结果 |
|--------|------|
| 配置检查 | ✅ 通过 |
| 函数导出 | ✅ 通过 |
| 月份计算 | ✅ 通过 |
| 消费识别（3 个用例） | ✅ 通过 |
| 语音配置 | ✅ 通过 |
| 月度账本结构 | ✅ 通过 |
| 欠费检查逻辑 | ✅ 通过 |

---

## 11. ClawHub 发布命令

```bash
# 登录 ClawHub
clawhub login

# 发布 v1.3
clawhub publish ./skills/kids-points \
  --slug kids-points \
  --name "孩子积分管理" \
  --version 1.3.0 \
  --changelog "v1.3: 月度消费额度制 + 欠费自动结转 + 修复消费识别/语音播报 bug"
```

---

_最后更新：2026-03-23 09:15_
