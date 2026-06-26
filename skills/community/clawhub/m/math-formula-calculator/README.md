# 🧮 Math Formula Calculator

**Version**: 1.0.0  
**Author**: 小竟（OpenClaw）  
**License**: MIT  
**Category**: Tools / Calculation

---

## 📋 Description

专业数学公式计算工具，支持 Excel 公式解析、分步计算、边界验证。

适用于招投标价格分计算、工程预算、财务分析等场景。

---

## ✨ Features

### 核心功能

1. **Excel 公式解析**
   - 支持 IF/ROUND/MAX/MIN/ABS 等常用函数
   - 支持嵌套函数解析
   - 支持条件逻辑处理

2. **分步计算**
   - 由内向外逐步计算
   - 记录每步中间结果
   - 便于验证和调试

3. **边界验证**
   - 除零检查
   - 负数检查
   - 溢出检查

4. **结果校验**
   - 合理性验证
   - 趋势分析
   - 对比验证

---

## 🎯 Use Cases

### 场景 1：招投标价格分计算

```excel
=ROUND(IF(报价<基准价，MAX(0,30-ABS(报价 - 基准价)/基准价*100*0.6),
   IF(报价=基准价，30,MAX(0,30-ABS(报价 - 基准价)/基准价*100*0.9))),2)
```

**计算步骤**：
1. 判断报价与基准价关系
2. 计算差额比例
3. 应用扣分系数（低价 0.6，高价 0.9）
4. 确保结果不为负（MAX(0,...)）
5. 四舍五入保留 2 位小数

---

### 场景 2：工程预算计算

```excel
=SUM(材料费 + 人工费 + 管理费) * (1 + 利润率)
```

---

### 场景 3：财务分析

```excel
=IF(ROE>15%, "优秀", IF(ROE>10%, "良好", "一般"))
```

---

## 🔧 Installation

### 方式 1：ClawHub 安装（推荐）

```bash
npx clawhub@latest install math-formula-calculator
```

### 方式 2：手动安装

```bash
git clone https://github.com/YOUR_USERNAME/math-formula-calculator.git
cp -r math-formula-calculator ~/.openclaw/workspace/skills/
```

---

## 📖 Usage

### 基本用法

```
用户："计算这个公式：=ROUND(IF(A1<B1,MAX(0,30-ABS(A1-B1)/B1*100*0.6),30),2)，A1=200, B1=220"

Math Formula Calculator:
📊 公式解析

外层函数：ROUND(..., 2)
中间层：IF 条件判断
内层：MAX(0, 30-ABS(差额)/B1*100*0.6)

📝 分步计算

步骤 1: 判断条件 A1<B1
  200 < 220 → TRUE

步骤 2: 计算差额
  ABS(200-220) = 20

步骤 3: 计算差额比例
  20/220*100 = 9.09

步骤 4: 应用扣分系数
  9.09*0.6 = 5.45

步骤 5: 计算得分
  30-5.45 = 24.55

步骤 6: 边界验证
  MAX(0, 24.55) = 24.55 ✅

步骤 7: 四舍五入
  ROUND(24.55, 2) = 24.55

✅ 最终结果：24.55
```

---

### 高级用法

#### 批量计算

```
用户："批量计算以下报价的得分：
基准价：220 万
报价列表：[200, 210, 220, 230, 240]
公式：综合评分法价格分"

Math Formula Calculator:
📊 批量计算结果

| 报价 | 得分 | 说明 |
|------|------|------|
| 200 万 | 24.55 | 低价 9.09 折 |
| 210 万 | 27.27 | 低价 9.55 折 |
| 220 万 | 30.00 | 等于基准价 |
| 230 万 | 26.09 | 高价 4.55% |
| 240 万 | 22.17 | 高价 9.09% |

最佳报价：220 万（满分 30 分）
```

---

## ⚠️ Best Practices

### 1. 公式原文抄录
- ❌ 不要修改任何字符
- ✅ 保持原样，包括括号、逗号

### 2. 公式结构拆解
- 识别外层函数
- 识别中间层函数
- 识别内层函数

### 3. 变量代入
- 明确每个变量的含义
- 明确每个变量的值
- 检查单位是否一致

### 4. 由内向外计算
- 先计算最内层函数
- 记录每步中间结果
- 便于验证和调试

### 5. 边界验证
- 检查除零风险
- 检查负数风险
- 检查溢出风险

### 6. 结果校验
- 合理性验证（是否符合常识）
- 趋势分析（是否符合预期）
- 对比验证（与已知结果对比）

---

## 🐛 Common Pitfalls

### 陷阱 1：分母混淆

❌ 错误：`差额/报价`  
✅ 正确：`差额/基准价`

### 陷阱 2：系数混淆

❌ 错误：低价用 0.9，高价用 0.6  
✅ 正确：低价用 0.6（鼓励），高价用 0.9（惩罚）

### 陷阱 3：忽略边界

❌ 错误：`30-扣分`（可能为负）  
✅ 正确：`MAX(0, 30-扣分)`

### 陷阱 4：未四舍五入

❌ 错误：直接输出小数  
✅ 正确：`ROUND(..., 2)`

---

## 📚 Advanced Features

### 支持的函数

| 函数类型 | 函数 | 说明 |
|---------|------|------|
| 逻辑函数 | IF, AND, OR, NOT | 条件判断 |
| 数学函数 | ROUND, MAX, MIN, ABS, SUM | 基本计算 |
| 文本函数 | CONCATENATE, LEFT, RIGHT | 文本处理 |
| 统计函数 | AVERAGE, COUNT, SUM | 统计分析 |

### 自定义函数

支持添加自定义计算规则：

```javascript
// 示例：综合评分法价格分计算
function calculatePriceScore(bidPrice, benchmarkPrice) {
  if (bidPrice < benchmarkPrice) {
    const diff = Math.abs(bidPrice - benchmarkPrice) / benchmarkPrice * 100;
    return Math.max(0, 30 - diff * 0.6);
  } else if (bidPrice === benchmarkPrice) {
    return 30;
  } else {
    const diff = Math.abs(bidPrice - benchmarkPrice) / benchmarkPrice * 100;
    return Math.max(0, 30 - diff * 0.9);
  }
}
```

---

## 🔗 Related Skills

- `local-rag-search` - 本地 RAG 搜索
- `markdown-converter` - Markdown 转换
- `stock-agent-pro` - 股票分析（使用数学计算）

---

## 📝 Changelog

### v1.0.0 (2026-03-11)
- ✅ 初始版本
- ✅ Excel 公式解析
- ✅ 分步计算
- ✅ 边界验证
- ✅ 结果校验

---

## 📞 Support

- **Issues**: https://github.com/YOUR_USERNAME/math-formula-calculator/issues
- **Discord**: https://discord.gg/clawd
- **Docs**: https://github.com/YOUR_USERNAME/math-formula-calculator/wiki

---

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

**Happy Calculating!** 🧮✨
