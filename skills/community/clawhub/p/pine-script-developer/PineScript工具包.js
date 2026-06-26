// Pine Script开发工具包
// 作者：盘眼（交易结构解析AI）
// 日期：2026-02-28

const fs = require('fs');
const path = require('path');

class PineScript工具包 {
  constructor() {
    this.模板目录 = path.join(__dirname, "模板");
    this.项目目录 = path.join(__dirname, "项目");
    this.确保目录存在();
    
    // Pine Script模板库
    this.模板库 = {
      // 基本指标模板
      移动平均线: this.生成移动平均线模板(),
      布林带: this.生成布林带模板(),
      RSI指标: this.生成RSI模板(),
      MACD指标: this.生成MACD模板(),
      
      // 交易策略模板
      双均线策略: this.生成双均线策略模板(),
      突破策略: this.生成突破策略模板(),
      网格策略: this.生成网格策略模板(),
      
      // 高级功能模板
      缠论指标: this.生成缠论指标模板(),
      ICT指标: this.生成ICT指标模板(),
      价格行为: this.生成价格行为模板(),
      
      // 工具模板
      调试工具: this.生成调试工具模板(),
      性能监控: this.生成性能监控模板(),
      数据导出: this.生成数据导出模板()
    };
  }
  
  确保目录存在() {
    [this.模板目录, this.项目目录].forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }
  
  // 生成移动平均线模板
  生成移动平均线模板() {
    return `//@version=5
indicator("多周期移动平均线", overlay=true, shorttitle="MA System")

// === 输入参数 ===
ma1Length = input.int(10, "快速均线", minval=1, group="均线设置")
ma2Length = input.int(20, "中期均线", minval=1, group="均线设置")
ma3Length = input.int(50, "慢速均线", minval=1, group="均线设置")
ma4Length = input.int(200, "长期均线", minval=1, group="均线设置")

source = input.source(close, "数据源", group="计算设置")
maType = input.string("SMA", "均线类型", options=["SMA", "EMA", "WMA"], group="计算设置")

// === 计算函数 ===
getMA(src, len, type) =>
    switch type
        "SMA" => ta.sma(src, len)
        "EMA" => ta.ema(src, len)
        "WMA" => ta.wma(src, len)

// === 计算均线 ===
ma1 = getMA(source, ma1Length, maType)
ma2 = getMA(source, ma2Length, maType)
ma3 = getMA(source, ma3Length, maType)
ma4 = getMA(source, ma4Length, maType)

// === 绘制 ===
p1 = plot(ma1, "MA" + str.tostring(ma1Length), color=color.new(#2196F3, 0), linewidth=2)
p2 = plot(ma2, "MA" + str.tostring(ma2Length), color=color.new(#4CAF50, 0), linewidth=2)
p3 = plot(ma3, "MA" + str.tostring(ma3Length), color=color.new(#FF9800, 0), linewidth=2)
p4 = plot(ma4, "MA" + str.tostring(ma4Length), color=color.new(#9C27B0, 0), linewidth=2)

// === 均线排列判断 ===
bullishAlignment = ma1 > ma2 and ma2 > ma3 and ma3 > ma4
bearishAlignment = ma1 < ma2 and ma2 < ma3 and ma3 < ma4

// === 背景色 ===
bgcolor(bullishAlignment ? color.new(#4CAF50, 90) : bearishAlignment ? color.new(#F44336, 90) : na, title="趋势背景")

// === 交叉信号 ===
goldenCross = ta.crossover(ma1, ma2)
deathCross = ta.crossunder(ma1, ma2)

plotshape(goldenCross, "金叉", location.belowbar, color=color.green, size=size.small)
plotshape(deathCross, "死叉", location.abovebar, color=color.red, size=size.small)

// === 警报 ===
alertcondition(goldenCross, "金叉信号", "快速均线上穿中期均线")
alertcondition(deathCross, "死叉信号", "快速均线下穿中期均线")

// === 表格显示 ===
var table infoTable = table.new(position.top_right, 2, 5, bgcolor=color.new(#000000, 80), 
                               border_width=1, border_color=color.gray)

if barstate.islast
    table.cell(infoTable, 0, 0, "当前价格", text_color=color.white, text_size=size.small)
    table.cell(infoTable, 1, 0, str.tostring(close, format.mintick), text_color=color.yellow)
    
    table.cell(infoTable, 0, 1, "MA" + str.tostring(ma1Length), text_color=color.white)
    table.cell(infoTable, 1, 1, str.tostring(ma1, format.mintick), text_color=color.new(#2196F3, 0))
    
    table.cell(infoTable, 0, 2, "MA" + str.tostring(ma2Length), text_color=color.white)
    table.cell(infoTable, 1, 2, str.tostring(ma2, format.mintick), text_color=color.new(#4CAF50, 0))
    
    table.cell(infoTable, 0, 3, "趋势", text_color=color.white)
    table.cell(infoTable, 1, 3, bullishAlignment ? "多头排列" : bearishAlignment ? "空头排列" : "震荡", 
              text_color=bullishAlignment ? color.green : bearishAlignment ? color.red : color.gray)
    
    table.cell(infoTable, 0, 4, "距离MA2", text_color=color.white)
    table.cell(infoTable, 1, 4, str.tostring((close - ma2) / ma2 * 100, format.percent) + "%", 
              text_color=close > ma2 ? color.green : color.red)`;
  }
  
  // 生成布林带模板
  生成布林带模板() {
    return `//@version=5
indicator("布林带策略", overlay=true, shorttitle="BB Strategy")

// === 输入参数 ===
bbLength = input.int(20, "布林带周期", minval=1, group="布林带设置")
bbStdDev = input.float(2.0, "标准差倍数", minval=0.5, maxval=5, step=0.1, group="布林带设置")
source = input.source(close, "数据源", group="布林带设置")

// === 计算布林带 ===
basis = ta.sma(source, bbLength)
dev = ta.stdev(source, bbLength)
upper = basis + bbStdDev * dev
lower = basis - bbStdDev * dev

// === 绘制 ===
p1 = plot(basis, "中线", color=color.blue, linewidth=2)
p2 = plot(upper, "上轨", color=color.red, linewidth=1)
p3 = plot(lower, "下轨", color=color.green, linewidth=1)

// 填充区域
fill(p2, p3, color=color.new(color.blue, 90), title="布林带区域")

// === 价格位置判断 ===
pricePosition = (close - lower) / (upper - lower) * 100

// === 突破信号 ===
breakoutUp = close[1] < upper[1] and close > upper
breakoutDown = close[1] > lower[1] and close < lower

// === 回归信号 ===
reversionFromTop = close[1] > upper[1] and close < upper
reversionFromBottom = close[1] < lower[1] and close > lower

// === 标记信号 ===
plotshape(breakoutUp, "上破", location.belowbar, color=color.red, shape=shape.triangleup, size=size.small)
plotshape(breakoutDown, "下破", location.abovebar, color=color.green, shape=shape.triangledown, size=size.small)
plotshape(reversionFromTop, "上轨回归", location.abovebar, color=color.orange, shape=shape.circle, size=size.small)
plotshape(reversionFromBottom, "下轨回归", location.belowbar, color=color.orange, shape=shape.circle, size=size.small)

// === 背景色 ===
bgcolor(pricePosition > 80 ? color.new(color.red, 90) : pricePosition < 20 ? color.new(color.green, 90) : na, 
        title="超买超卖背景")

// === 宽度指标 ===
bbWidth = (upper - lower) / basis * 100
bbWidthSma = ta.sma(bbWidth, 20)
isSqueeze = bbWidth < bbWidthSma

plot(bbWidth, "带宽%", color=color.purple, display=display.data_window)
hline(bbWidthSma, "平均带宽", color=color.gray, linestyle=hline.style_dashed)

// === 警报 ===
alertcondition(breakoutUp, "布林带上破", "价格突破布林带上轨")
alertcondition(breakoutDown, "布林带下破", "价格突破布林带下轨")
alertcondition(isSqueeze and barstate.isconfirmed, "布林带收缩", "布林带宽度低于平均水平")

// === 表格信息 ===
var table bbTable = table.new(position.top_right, 2, 6, bgcolor=color.new(#000000, 80))

if barstate.islast
    table.cell(bbTable, 0, 0, "布林带状态", text_color=color.white, text_size=size.normal)
    table.cell(bbTable, 1, 0, "", text_color=color.white)
    
    table.cell(bbTable, 0, 1, "上轨", text_color=color.white)
    table.cell(bbTable, 1, 1, str.tostring(upper, format.mintick), text_color=color.red)
    
    table.cell(bbTable, 0, 2, "中线", text_color=color.white)
    table.cell(bbTable, 1, 2, str.tostring(basis, format.mintick), text_color=color.blue)
    
    table.cell(bbTable, 0, 3, "下轨", text_color=color.white)
    table.cell(bbTable, 1, 3, str.tostring(lower, format.mintick), text_color=color.green)
    
    table.cell(bbTable, 0, 4, "位置%", text_color=color.white)
    table.cell(bbTable, 1, 4, str.tostring(pricePosition, format.percent), 
              text_color=pricePosition > 70 ? color.red : pricePosition < 30 ? color.green : color.yellow)
    
    table.cell(bbTable, 0, 5, "收缩", text_color=color.white)
    table.cell(bbTable, 1, 5, isSqueeze ? "是" : "否", 
              text_color=isSqueeze ? color.orange : color.gray)`;
  }
  
  // 生成缠论指标模板
  生成缠论指标模板() {
    return `//@version=5
indicator("缠论结构分析", overlay=true, shorttitle="Chan Theory")

// === 输入参数 ===
biSensitivity = input.float(0.5, "笔敏感度", minval=0.1, maxval=2, step=0.1, group="缠论设置")
showBi = input.bool(true, "显示笔", group="显示设置")
showDuan = input.bool(true, "显示线段", group="显示设置")
showZhongshu = input.bool(true, "显示中枢", group="显示设置")

// === 顶底分型识别 ===
// 顶分型：高中低，中间K线最高
isTopFenxing(high, low) =>
    high[2] < high[1] and high[1] > high[0] and
    low[2] < low[1] and low[1] > low[0]

// 底分型：低中高，中间K线最低  
isBottomFenxing(high, low) =>
    low[2] > low[1] and low[1] < low[0] and
    high[2] > high[1] and high[1] < high[0]

// === 笔识别 ===
var bool isBiUp = false
var bool isBiDown = false
var float biStartPrice = na
var float biEndPrice = na

// 识别向上笔
if isBottomFenxing(high, low) and not isBiUp
    isBiUp := true
    isBiDown := false
    biStartPrice := low[1]
    
if isBiUp and isTopFenxing(high, low)
    isBiUp := false
    biEndPrice := high[1]
    // 绘制向上笔
    if showBi
        line.new(bar_index[2], biStartPrice, bar_index[1], biEndPrice, 
                color=color.green, width=2, style=line.style_solid)

// 识别向下笔
if isTopFenxing(high, low) and not isBiDown
    isBiDown := true
    isBiUp := false
    biStartPrice := high[1]
    
if isBiDown and isBottomFenxing(high, low)
    isBiDown := false
    biEndPrice := low[1]
    // 绘制向下笔
    if showBi
        line.new(bar_index[2], biStartPrice, bar_index[1], biEndPrice,
                color=color.red, width=2, style=line.style_solid)

// === 标记分型 ===
plotshape(isTopFenxing(high, low), "顶分型", location.abovebar, 
          color=color.red, shape=shape.triangledown, size=size.small)
plotshape(isBottomFenxing(high, low), "底分型", location.belowbar,
          color=color.green, shape=shape.triangleup, size=size.small)

// === 中枢识别（简化版） ===
// 中枢：至少3笔重叠的区域
var float[] zhongshuHighs = array.new_float(0)
var float[] zhongshuLows = array.new_float(0)

// === 当前笔方向 ===
currentBiDirection = isBiUp ? 1 : isBiDown ? -1 : 0

// === 表格信息 ===
var table chanTable = table.new(position.top_right, 2, 4, bgcolor=color.new(#000000, 80))

if barstate.islast
    table.cell(chanTable, 0, 0, "缠论分析", text_color=color.yellow, text_size=size.normal)
    table.cell(chanTable, 1, 0, "", text_color=color.yellow)
    
    table.cell(chanTable, 0, 1, "当前笔", text_color=color.white)
    table.cell(chanTable, 1, 1, currentBiDirection == 1 ? "向上笔" : currentBiDirection == -1 ? "向下笔" : "无",
              text_color=currentBiDirection == 1 ? color.green : currentBiDirection == -1 ? color.red : color.gray)
    
    table.cell(chanTable, 0, 2, "分型数量", text_color=color.white)
    table.cell(chanTable, 1, 2, str.tostring(bar_index), text_color=color.white)
    
    table.cell(chanTable, 0, 3, "状态", text_color=color.white)
    table.cell(chanTable, 1, 3, "监控中", text_color=color.blue)

// === 背景色 ===
bgcolor(currentBiDirection == 1 ? color.new(color.green, 90) : 
        currentBiDirection == -1 ? color.new(color.red, 90) : na,
        title="笔方向背景")

// 注：这是一个简化的缠论指标，实际缠论分析更复杂
// 需要更多逻辑来处理线段、中枢、背驰等概念`;
  }
  
  // 生成ICT指标模板
  生成ICT指标模板() {
    return `//@version=5
indicator("ICT概念指标", overlay=true, shorttitle="ICT Concepts")

// === 输入参数 ===
showFVG = input.bool(true, "显示FVG", group="ICT设置")
showOB = input.bool(true, "显示OB", group="ICT设置")
showSession = input.bool(true, "显示SESSION", group="ICT设置")

// === SESSION时间 ===
// 亚洲SESSION: 00:00-08:00 GMT
asiaSessionStart = timestamp("GMT", 0, 0, 0, 0)
asiaSessionEnd = timestamp("GMT", 8, 0, 0, 0)

// 伦敦SESSION: 08:00-16:00 GMT
londonSessionStart = timestamp("GMT", 8, 0, 0, 0)
londonSessionEnd = timestamp("GMT", 16, 0, 0, 0)

// 纽约SESSION: 13:00-21:00 GMT
nySessionStart = timestamp("GMT", 13, 0, 0, 0)
nySessionEnd = timestamp("GMT", 21, 0, 0, 0)

// 重叠SESSION: 13:00-16:00 GMT
overlapSessionStart = timestamp("GMT", 13, 0, 0, 0)
overlapSessionEnd = timestamp("GMT", 16, 0, 0, 0)

// === 当前SESSION判断 ===
isAsiaSession = time >= asiaSessionStart and time < asiaSessionEnd
isLondonSession = time >= londonSessionStart and time < londonSessionEnd
isNySession = time >= nySessionStart and time < nySessionEnd
isOverlapSession = time >= overlapSessionStart and time < overlapSessionEnd

// === FVG识别 ===
// 上涨FVG: 前一根K线最低价 > 再前一根K线最高价
bullishFVG = low[1] > high[2]
// 下跌FVG: 前一根K线最高价 < 再前一根K线最低价
bearishFVG = high[1] < low[2]

// === OB识别 ===
// Order Block: 强趋势中的回调K线
identifyOB() =>
    // 简化的OB识别逻辑
    isStrongUp = close[3] < close[2] and close[2] < close[1] and close > close[1]
    isStrongDown = close[3] > close[2] and close[2] > close[1] and close < close[1]
    
    if isStrongUp and close < open
        // 上涨趋势中的阴线可能是OB
        1
    else if isStrongDown and close > open
        // 下跌趋势中的阳线可能是OB
        -1
    else
        0

obType = identifyOB()

// === 绘制SESSION背景 ===
if showSession
    bgcolor(isAsiaSession ? color.new(color.blue, 90) : 
            isLondonSession ? color.new(color.green, 90) :
            isNySession ? color.new(color.red, 90) :
            isOverlapSession ? color.new(color.purple, 90) : na,
            title="SESSION背景")

// === 绘制FVG ===
if showFVG
    // 上涨FVG区域
    if bullishFVG
        box.new(bar_index[2], high[2], bar_index[1], low[1], 
               bgcolor=color.new(color.green, 80), border_color=color.green)
    
    // 下跌FVG区域
    if bearishFVG
        box.new(bar_index[2], low[2], bar_index[1], high[1],
               bgcolor=color.new(color.red, 80), border_color=color.red)

// === 绘制OB ===
if showOB
    plotshape(obType == 1, "看涨OB", location.belowbar, 
              color=color.new(color.green, 0), shape=shape.square, size=size.small)
    plotshape(obType == -1, "看跌OB", location.abovebar,
              color=color.new(color.red, 0), shape=shape.square, size=size.small)

// === 流动性水平 ===
// 近期高点作为上方流动性
recentHigh = ta.highest(high, 20)
recentLow = ta.lowest(low, 20)

plot(recentHigh, "上方流动性", color=color.red, style=plot.style_circles)
plot(recentLow, "下方流动性", color=color.green, style=plot.style_circles)

// === 表格信息 ===
var table ictTable = table.new(position.top_right, 2, 6, bgcolor=color.new(#000000, 80))

if barstate.islast
    table.cell(ictTable, 0, 0, "ICT分析", text_color=color.yellow)
    table.cell(ictTable, 1, 0, "", text_color=color.yellow)
    
    table.cell(ictTable, 0, 1, "当前SESSION", text_color=color.white)
    currentSession = isAsiaSession ? "亚洲" : isLondonSession ? "伦敦" : 
                    isNySession ? "纽约" : isOverlapSession ? "重叠" : "其他"
    table.cell(ictTable, 1, 1, currentSession, 
              text_color=isOverlapSession ? color.purple : isNySession ? color.red : 
                         isLondonSession ? color.green : color.blue)
    
    table.cell(ictTable, 0, 2, "FVG", text_color=color.white)
    fvgStatus = bullishFVG ? "上涨FVG" : bearishFVG ? "下跌FVG" : "无"
    table.cell(ictTable, 1, 2, fvgStatus,
              text_color=bullishFVG ? color.green : bearishFVG ? color.red : color.gray)
    
    table.cell(ictTable, 0, 3, "OB", text_color=color.white)
    obStatus = obType == 1 ? "看涨OB" : obType == -1 ? "看跌OB" : "无"
    table.cell(ictTable, 1, 3, obStatus,
              text_color=obType == 1 ? color.green : obType == -1 ? color.red : color.gray)
    
    table.cell(ictTable, 0, 4, "上方流动性", text_color=color.white)
    table.cell(ictTable, 1, 4, str.tostring(recentHigh, format.mintick), text_color=color.red)
    
    table.cell(ictTable, 0, 5, "下方流动性", text_color=color.white)
    table.cell(ictTable, 1, 5, str.tostring(recentLow, format.mintick), text_color=color.green)

// === 警报 ===
alertcondition(bullishFVG, "上涨FVG", "出现上涨FVG")
alertcondition(bearishFVG, "下跌FVG", "出现下跌FVG")
alertcondition(isOverlapSession and barstate.isconfirmed, "重叠SESSION", "进入重叠SESSION时段")`;
  }
  
  // 生成其他模板的方法（简化）
  生成RSI模板() {
    return `//@version=5
indicator("RSI指标", overlay=false, shorttitle="RSI")
// RSI指标模板代码...`;
  }
  
  生成MACD模板() {
    return `//@version=5
indicator("MACD指标", overlay=false, shorttitle="MACD")
// MACD指标模板代码...`;
  }
  
  生成双均线策略模板() {
    return `//@version=5
strategy("双均线策略", overlay=true)
// 双均线策略模板代码...`;
  }
  
  生成突破策略模板() {
    return `//@version=5
strategy("突破策略", overlay=true)
// 突破策略模板代码...`;
  }
  
  生成网格策略模板() {
    return `//@version=5
strategy("网格交易策略", overlay=true)
// 网格策略模板代码...`;
  }
  
  生成价格行为模板() {
    return `//@version=5
indicator("价格行为模式", overlay=true)
// 价格行为模板代码...`;
  }
  
  生成调试工具模板() {
    return `//@version=5
indicator("调试工具", overlay=true)
// 调试工具模板代码...`;
  }
  
  生成性能监控模板() {
    return `//@version=5
indicator("性能监控", overlay=false)
// 性能监控模板代码...`;
  }
  
  生成数据导出模板() {
    return `//@version=5
indicator("数据导出", overlay=false)
// 数据导出模板代码...`;
  }
  
  // 创建新项目
  创建新项目(项目名称, 模板类型 = "移动平均线") {
    console.log(`📁 创建新项目: ${项目名称}`);
    
    const 项目路径 = path.join(this.项目目录, 项目名称);
    if (!fs.existsSync(项目路径)) {
      fs.mkdirSync(项目路径, { recursive: true });
    }
    
    // 获取模板
    const 模板代码 = this.模板库[模板类型] || this.模板库["移动平均线"];
    
    // 创建主文件
    const 主文件路径 = path.join(项目路径, `${项目名称}.pine`);
    fs.writeFileSync(主文件路径, 模板代码);
    
    // 创建配置文件
    const 配置 = {
      项目名称: 项目名称,
      创建时间: new Date().toISOString(),
      模板类型: 模板类型,
      文件: {
        主文件: `${项目名称}.pine`,
        说明文件: "README.md",
        测试文件: "test.pine"
      }
    };
    
    const 配置路径 = path.join(项目路径, "project.json");
    fs.writeFileSync(配置路径, JSON.stringify(配置, null, 2));
    
    // 创建说明文件
    const 说明内容 = `# ${项目名称} - Pine Script项目

## 项目描述
基于${模板类型}模板创建的TradingView指标

## 文件说明
- \`${项目名称}.pine\` - 主Pine Script文件
- \`project.json\` - 项目配置
- \`README.md\` - 本说明文件

## 使用方法
1. 复制 \`${项目名称}.pine\` 中的代码
2. 在TradingView中创建新指标
3. 粘贴代码并保存
4. 添加到图表进行测试

## 参数说明
请查看代码中的输入参数部分

## 更新记录
- ${new Date().toLocaleDateString('zh-CN')} - 项目创建`;
    
    const 说明路径 = path.join(项目路径, "README.md");
    fs.writeFileSync(说明路径, 说明内容);
    
    console.log(`✅ 项目创建完成: ${项目路径}`);
    console.log(`📄 主文件: ${主文件路径}`);
    
    return {
      项目路径: 项目路径,
      主文件: 主文件路径,
      配置: 配置
    };
  }
  
  // 分析现有代码
  分析PineScript代码(代码内容) {
    console.log("🔍 分析Pine Script代码...");
    
    const 分析结果 = {
      版本: this.提取版本(代码内容),
      指标类型: this.判断指标类型(代码内容),
      输入参数: this.提取输入参数(代码内容),
      计算函数: this.提取计算函数(代码内容),
      绘图指令: this.提取绘图指令(代码内容),
      警报条件: this.提取警报条件(代码内容),
      问题: this.检查问题(代码内容),
      建议: this.提供建议(代码内容)
    };
    
    return 分析结果;
  }
  
  提取版本(代码) {
    const 版本匹配 =代码.match(/\/\/@version=(\d+)/);
    return 版本匹配 ? 版本匹配[1] : "未知";
  }
  
  判断指标类型(代码) {
    if (代码.includes("strategy(")) return "交易策略";
    if (代码.includes("indicator(")) return "技术指标";
    if (代码.includes("library(")) return "函数库";
    return "未知类型";
  }
  
  提取输入参数(代码) {
    const 参数列表 = [];
    const 参数匹配 =代码.matchAll(/input\.(\w+)\([^)]*"([^"]*)"[^)]*\)/g);
    
    for (const 匹配 of 参数匹配) {
      参数列表.push({
        类型: 匹配[1],
        名称: 匹配[2]
      });
    }
    
    return 参数列表;
  }
  
  提取计算函数(代码) {
    const 函数列表 = [];
    const 函数匹配 =代码.matchAll(/(\w+)\s*=\s*(ta\.\w+|math\.\w+|str\.\w+)/g);
    
    for (const 匹配 of 函数匹配) {
      函数列表.push({
        变量: 匹配[1],
        函数: 匹配[2]
      });
    }
    
    return 函数列表;
  }
  
  提取绘图指令(代码) {
    const 绘图列表 = [];
    const 绘图匹配 =代码.matchAll(/(plot|plotshape|plotchar|hline|bgcolor|fill)\(/g);
    
    for (const 匹配 of 绘图匹配) {
      绘图列表.push(匹配[1]);
    }
    
    return [...new Set(绘图列表)]; // 去重
  }
  
  提取警报条件(代码) {
    const 警报列表 = [];
    const 警报匹配 =代码.matchAll(/alertcondition\(([^,]+),/g);
    
    for (const 匹配 of 警报匹配) {
      警报列表.push(匹配[1]);
    }
    
    return 警报列表;
  }
  
  检查问题(代码) {
    const 问题列表 = [];
    
    // 检查版本声明
    if (!代码.includes("//@version=")) {
      问题列表.push("缺少版本声明");
    }
    
    // 检查指标名称
    if (!代码.includes("indicator(") && !代码.includes("strategy(")) {
      问题列表.push("缺少指标或策略声明");
    }
    
    // 检查绘图数量（性能警告）
    const 绘图数量 = (代码.match(/plot\(/g) || []).length;
    if (绘图数量 > 10) {
      问题列表.push(`绘图数量过多 (${绘图数量})，可能影响性能`);
    }
    
    return 问题列表;
  }
  
  提供建议(代码) {
    const 建议列表 = [];
    
    // 版本建议
    if (代码.includes("//@version=4")) {
      建议列表.push("考虑升级到Pine Script v5以获得更好的性能和功能");
    }
    
    // 性能建议
    if (代码.includes("for ")) {
      建议列表.push("循环可能影响性能，考虑使用内置函数替代");
    }
    
    // 用户体验建议
    if (!代码.includes("group=")) {
      建议列表.push("考虑使用group参数对输入参数进行分组");
    }
    
    if (!代码.includes("alertcondition")) {
      建议列表.push("考虑添加警报功能");
    }
    
    return 建议列表;
  }
  
  // 优化代码
  优化PineScript代码(代码内容) {
    console.log("⚡ 优化Pine Script代码...");
    
    let 优化代码 = 代码内容;
    
    // 1. 确保版本声明
    if (!优化代码.includes("//@version=")) {
      优化代码 = "//@version=5\n" + 优化代码;
    }
    
    // 2. 添加注释头
    if (!优化代码.includes("作者：") && !优化代码.includes("Author:")) {
      const 注释头 = `// ============================================
// 指标名称: [请填写]
// 作者: [请填写]
// 版本: 1.0
// 描述: [请填写]
// ============================================\n\n`;
      优化代码 = 注释头 + 优化代码;
    }
    
    // 3. 优化输入参数分组
    if (优化代码.includes("input.") && !优化代码.includes("group=")) {
      // 简化的分组优化
      优化代码 = 优化代码.replace(
        /input\.(\w+)\(([^)]*)"([^"]*)"([^)]*)\)/g,
        (匹配, 类型, 前文, 名称, 后文) => {
          let 分组 = "";
          if (名称.includes("周期") || 名称.includes("长度")) {
            分组 = " group=\"参数设置\"";
          } else if (名称.includes("颜色") || 名称.includes("样式")) {
            分组 = " group=\"显示设置\"";
          } else if (名称.includes("警报") || 名称.includes("提醒")) {
            分组 = " group=\"警报设置\"";
          }
          return `input.${类型}(${前文}"${名称}"${后文}${分组})`;
        }
      );
    }
    
    // 4. 添加性能提示
    const 循环数量 = (优化代码.match(/for\s+/g) || []).length;
    if (循环数量 > 0) {
      const 性能提示 = `\n\n// ⚠️ 性能提示: 检测到 ${循环数量} 个循环
// 建议: 考虑使用内置函数替代循环以提高性能
// 例如: 使用 ta.sma() 替代手动计算移动平均`;
      优化代码 += 性能提示;
    }
    
    return 优化代码;
  }
  
  // 演示功能
  演示() {
    console.log("🎬 Pine Script工具包演示");
    console.log("=".repeat(50));
    
    console.log("📚 可用模板:");
    Object.keys(this.模板库).forEach((模板, 索引) => {
      console.log(`  ${索引 + 1}. ${模板}`);
    });
    
    console.log("\n🛠️ 创建示例项目...");
    const 项目 = this.创建新项目("示例移动平均线", "移动平均线");
    
    console.log("\n🔍 分析模板代码...");
    const 分析结果 = this.分析PineScript代码(this.模板库["移动平均线"]);
    
    console.log("\n📊 分析结果:");
    console.log(`   版本: Pine Script v${分析结果.版本}`);
    console.log(`   类型: ${分析结果.指标类型}`);
    console.log(`   输入参数: ${分析结果.输入参数.length} 个`);
    console.log(`   计算函数: ${分析结果.计算函数.length} 个`);
    console.log(`   绘图指令: ${分析结果.绘图指令.join(", ")}`);
    console.log(`   警报条件: ${分析结果.警报条件.length} 个`);
    
    if (分析结果.问题.length > 0) {
      console.log("\n⚠️ 发现问题:");
      分析结果.问题.forEach(问题 => console.log(`   - ${问题}`));
    }
    
    if (分析结果.建议.length > 0) {
      console.log("\n💡 优化建议:");
      分析结果.建议.forEach(建议 => console.log(`   - ${建议}`));
    }
    
    console.log("\n✅ 演示完成!");
    console.log("=".repeat(50));
    
    console.log("\n💡 您现在可以:");
    console.log("   1. 使用模板创建新指标");
    console.log("   2. 分析现有Pine Script代码");
    console.log("   3. 优化代码性能");
    console.log("   4. 添加警报和高级功能");
    
    return 项目;
  }
}

// 导出模块
module.exports = {
  PineScript工具包
};

// 如果直接运行，执行演示
if (require.main === module) {
  const 工具包 = new PineScript工具包();
  
  try {
    工具包.演示();
    
    console.log("\n📁 目录结构:");
    console.log(`   模板目录: ${工具包.模板目录}`);
    console.log(`   项目目录: ${工具包.项目目录}`);
    
  } catch (错误) {
    console.error("演示失败:", 错误);
  }
}