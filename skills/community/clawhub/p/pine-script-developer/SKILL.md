---
name: pine-script-developer
description: "专业Pine Script开发技能，专门用于TradingView指标和策略的编写、调试和优化。包含Pine Script v5语法、最佳实践、指标开发、策略回测、性能优化等。"
metadata:
  {
    "openclaw": { "emoji": "📈", "category": "trading" },
  }
---

# Pine Script开发技能

专门用于TradingView Pine Script代码的编写、修改、调试和优化。

## 🎯 适用场景

使用此技能当您需要：
1. 编写新的TradingView指标
2. 修改现有的Pine Script代码
3. 调试Pine Script错误
4. 优化指标性能
5. 创建交易策略
6. 添加警报功能
7. 实现复杂的图表绘制
8. 进行策略回测

## 📚 Pine Script核心知识

### 版本信息
- **Pine Script v5**：最新版本，推荐使用
- **Pine Script v4**：兼容旧版本
- 关键区别：v5有更严格的类型检查，更好的性能

### 基本结构
```pinescript
//@version=5
indicator("My Indicator", overlay=true)

// 输入参数
length = input.int(14, "Length", minval=1)

// 计算
sma = ta.sma(close, length)

// 绘制
plot(sma, color=color.blue, linewidth=2)
```

### 常用函数
- `ta.sma()` - 简单移动平均
- `ta.ema()` - 指数移动平均
- `ta.rsi()` - RSI指标
- `ta.macd()` - MACD指标
- `ta.stoch()` - 随机指标
- `ta.bb()` - 布林带
- `ta.atr()` - 平均真实波幅

## 🔧 开发工作流

### 1. 需求分析
- 明确指标功能
- 确定输入参数
- 选择计算逻辑
- 设计输出显示

### 2. 代码编写
- 使用正确的版本声明
- 添加详细的注释
- 实现错误处理
- 优化性能

### 3. 测试调试
- 在TradingView中测试
- 检查边界条件
- 验证计算结果
- 优化代码性能

### 4. 部署优化
- 添加用户友好的参数
- 优化图表显示
- 添加警报功能
- 编写使用说明

## 💡 最佳实践

### 代码结构
```pinescript
//@version=5
indicator("专业指标", overlay=true, shorttitle="ProInd")

// === 输入参数 ===
length = input.int(20, "计算周期", minval=1, group="基本参数")
source = input.source(close, "数据源", group="基本参数")

// === 计算逻辑 ===
smaValue = ta.sma(source, length)
emaValue = ta.ema(source, length)

// === 条件判断 ===
bullish = close > smaValue
bearish = close < smaValue

// === 绘制 ===
plot(smaValue, "SMA", color=color.blue, linewidth=2)
plot(emaValue, "EMA", color=color.red, linewidth=2)

// === 背景色 ===
bgcolor(bullish ? color.new(color.green, 90) : bearish ? color.new(color.red, 90) : na)

// === 警报条件 ===
alertcondition(bullish, "看涨信号", "价格上穿SMA")
alertcondition(bearish, "看跌信号", "价格下穿SMA")
```

### 性能优化
1. **避免重复计算**：缓存常用计算结果
2. **使用内置函数**：优先使用TradingView内置函数
3. **减少绘图数量**：过多的绘图会影响性能
4. **优化循环**：避免在每根K线上进行复杂循环

### 错误处理
```pinescript
// 检查数据有效性
if not na(close) and not na(volume)
    // 安全计算
    volumeAvg = ta.sma(volume, 20)
else
    volumeAvg := na
```

## 🎨 图表绘制技巧

### 线条绘制
```pinescript
// 基本线条
plot(series, title, color, linewidth, style)

// 样式选项
plot.style_line       // 实线
plot.style_linebr     // 虚线  
plot.style_circles    // 圆点
plot.style_cross      // 十字
plot.style_area       // 面积图
```

### 形状标记
```pinescript
// 标记点
plotshape(condition, title, location, color, style, size)

// 位置选项
location.abovebar     // K线上方
location.belowbar     // K线下方
location.top          // 图表顶部
location.bottom       // 图表底部
```

### 背景色
```pinescript
// 条件背景色
bgcolor(condition ? color.new(color.green, 90) : na)
```

### 表格显示
```pinescript
// 创建表格
var table myTable = table.new(position.top_right, 1, 1)

// 更新表格
table.cell(myTable, 0, 0, str.tostring(close, format.volume))
```

## 📊 策略开发

### 策略模板
```pinescript
//@version=5
strategy("My Strategy", overlay=true, margin_long=100, margin_short=100)

// 输入参数
fastLength = input.int(12, "快线周期")
slowLength = input.int(26, "慢线周期")

// 计算指标
fastMA = ta.sma(close, fastLength)
slowMA = ta.sma(close, slowLength)

// 交易条件
longCondition = ta.crossover(fastMA, slowMA)
shortCondition = ta.crossunder(fastMA, slowMA)

// 执行交易
if (longCondition)
    strategy.entry("Long", strategy.long)
    
if (shortCondition)
    strategy.entry("Short", strategy.short)

// 止损止盈
strategy.exit("Exit Long", "Long", stop=close * 0.95, limit=close * 1.05)
strategy.exit("Exit Short", "Short", stop=close * 1.05, limit=close * 0.95)
```

### 仓位管理
```pinescript
// 固定仓位
strategy.entry("Long", strategy.long, qty=1)

// 基于资金的仓位
capital = strategy.equity
riskPercent = 0.02  // 2%风险
stopLossPips = 100
positionSize = (capital * riskPercent) / stopLossPips
strategy.entry("Long", strategy.long, qty=positionSize)
```

### 回测设置
```pinescript
// 回测时间范围
strategy(title="My Strategy", 
         overlay=true,
         initial_capital=10000,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=100,
         commission_type=strategy.commission.percent,
         commission_value=0.1)
```

## 🔔 警报系统

### 基本警报
```pinescript
// 简单警报
alertcondition(close > open, "阳线警报", "出现阳线")

// 复杂条件
bullishAlert = close > ta.sma(close, 20) and volume > ta.sma(volume, 20)
alertcondition(bullishAlert, "看涨放量警报", "价格上穿20日均线且放量")
```

### 策略警报
```pinescript
// 策略中的警报
if longCondition
    alert("买入信号: " + syminfo.ticker, alert.freq_once_per_bar)
    
if shortCondition
    alert("卖出信号: " + syminfo.ticker, alert.freq_once_per_bar)
```

### 自定义消息
```pinescript
// 详细警报消息
alertMessage = "品种: " + syminfo.ticker + 
               "\n价格: " + str.tostring(close) +
               "\n时间: " + str.tostring(time, "yyyy-MM-dd HH:mm")
alertcondition(bullishAlert, "详细警报", alertMessage)
```

## 🛠️ 调试技巧

### 打印调试
```pinescript
// 使用表格显示调试信息
var table debugTable = table.new(position.bottom_right, 2, 5)
table.cell(debugTable, 0, 0, "Close: " + str.tostring(close))
table.cell(debugTable, 1, 0, "SMA: " + str.tostring(ta.sma(close, 20)))
```

### 条件调试
```pinescript
// 只在特定条件下显示调试信息
debugCondition = bar_index % 100 == 0  // 每100根K线显示一次
if debugCondition
    label.new(bar_index, high, "Close: " + str.tostring(close), 
              color=color.yellow, style=label.style_label_down)
```

### 性能监控
```pinescript
// 计算执行时间
var int startTime = na
if barstate.isfirst
    startTime := timenow
    
if barstate.islast
    executionTime = timenow - startTime
    label.new(bar_index, high, "执行时间: " + str.tostring(executionTime) + "ms")
```

## 📈 高级功能

### 自定义函数
```pinescript
// 自定义指标函数
myCustomIndicator(src, length) =>
    sum = 0.0
    for i = 0 to length - 1
        sum := sum + src[i]
    sum / length

// 使用自定义函数
customSMA = myCustomIndicator(close, 14)
plot(customSMA, "Custom SMA")
```

### 数组操作
```pinescript
// 创建数组
var float[] pricesArray = array.new_float(0)

// 添加数据
array.push(pricesArray, close)

// 访问数据
if array.size(pricesArray) > 0
    firstPrice = array.get(pricesArray, 0)
```

### 时间处理
```pinescript
// 时间判断
isLondonSession = time(timeframe.period, "0800-1600")
isNewYorkSession = time(timeframe.period, "1300-2100")

// 日期判断
isMonday = dayofweek == dayofweek.monday
isFirstDayOfMonth = dayofmonth == 1
```

## 🔗 与您的交易系统集成

### 缠论指标
```pinescript
// 缠论笔识别
identifyBi(high, low) =>
    // 笔识别逻辑
    // 顶分型、底分型判断
    // 笔的起点和终点
    
biDirection = identifyBi(high, low)
plot(biDirection, "缠论笔", color=biDirection > 0 ? color.green : color.red)
```

### ICT概念指标
```pinescript
// ICT SESSION识别
londonSession = time(timeframe.period, "0800-1600")
newYorkSession = time(timeframe.period, "1300-2100")

// FVG识别
identifyFVG(high, low, close, open) =>
    // FVG识别逻辑
    // 上涨FVG、下跌FVG
    
fvgType = identifyFVG(high, low, close, open)
plotshape(fvgType == 1, "上涨FVG", location.belowbar, color.green, shape.triangleup)
plotshape(fvgType == -1, "下跌FVG", location.abovebar, color.red, shape.triangledown)
```

### 价格行为模式
```pinescript
// Pin Bar识别
isPinBar(high, low, close, open) =>
    bodySize = math.abs(close - open)
    upperWick = high - math.max(close, open)
    lowerWick = math.min(close, open) - low
    bodySize < (upperWick + lowerWick) * 0.3 and
    (upperWick > bodySize * 2 or lowerWick > bodySize * 2)

pinBarBullish = isPinBar(high, low, close, open) and close > open
pinBarBearish = isPinBar(high, low, close, open) and close < open
```

## 📋 代码审查清单

### 代码质量
- [ ] 正确的版本声明 (`//@version=5`)
- [ ] 有意义的指标名称
- [ ] 详细的输入参数说明
- [ ] 适当的错误处理
- [ ] 性能优化考虑

### 功能完整
- [ ] 所有需求功能已实现
- [ ] 输入参数范围合理
- [ ] 计算结果准确
- [ ] 图表显示清晰

### 用户体验
- [ ] 参数分组合理
- [ ] 颜色搭配协调
- [ ] 警报功能完善
- [ ] 有使用说明

## 🚀 快速开始

### 模板1：基本指标
```pinescript
//@version=5
indicator("基本移动平均线", overlay=true)

// 输入参数
length1 = input.int(20, "快速均线", group="均线设置")
length2 = input.int(50, "慢速均线", group="均线设置")
source = input.source(close, "数据源", group="均线设置")

// 计算
ma1 = ta.sma(source, length1)
ma2 = ta.sma(source, length2)

// 绘制
plot(ma1, "快速均线", color=color.blue)
plot(ma2, "慢速均线", color=color.red)

// 交叉信号
crossUp = ta.crossover(ma1, ma2)
crossDown = ta.crossunder(ma1, ma2)

plotshape(crossUp, "金叉", location.belowbar, color.green, shape.triangleup)
plotshape(crossDown, "死叉", location.abovebar, color.red, shape.triangledown)
```

### 模板2：交易策略
```pinescript
//@version=5
strategy("双均线策略", overlay=true, initial_capital=10000)

// 参数
fastLen = input.int(12, "快线周期")
slowLen = input.int(26, "慢线周期")

// 计算
fastMA = ta.ema(close, fastLen)
slowMA = ta.ema(close, slowLen)

// 信号
longCond = ta.crossover(fastMA, slowMA)
shortCond = ta.crossunder(fastMA, slowMA)

// 交易
if (longCond)
    strategy.entry("Long", strategy.long)
    
if (shortCond)
    strategy.entry("Short", strategy.short)

// 绘制
plot(fastMA, "快线", color=color.blue)
plot(slowMA, "慢线", color=color.red)
```

## 📞 技术支持

### 常见问题
1. **编译错误**：检查语法、变量名、函数参数
2. **逻辑错误**：使用调试表格验证中间结果
3. **性能问题**：优化循环，减少不必要的计算
4. **显示问题**：调整绘图参数和颜色

### 资源链接
- [Pine Script v5手册](https://www.tradingview.com/pine-script-docs/en/v5/)
- [TradingView社区](https://www.tradingview.com/scripts/)
- [Pine Script最佳实践](https://www.tradingview.com/script/)

---

**💡 提示**：在修改现有代码时，先备份原代码，逐步测试每个修改。使用TradingView的"添加到图表"功能实时测试代码效果。