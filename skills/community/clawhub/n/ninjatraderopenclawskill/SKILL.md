---
name: "ninjatrader-dev"
description: "NinjaTrader 8 NinjaScript development reference: using directives, lifecycle, indicators, order mgmt, compile errors, deployment"
---

# NinjaTrader 8 NinjaScript Development Skill

A practical reference skill for coding, validating, and deploying NinjaTrader 8 strategies and indicators. Use this before every NT8 coding session.

---

## 1. PRE-DEPLOY CHECKLIST

Run this checklist **before** writing or deploying any strategy `.cs` file:

- [ ] Are ALL required `using` directives present? (see §2 template)
- [ ] Is every indicator called in code instantiated? (SMA, EMA, ATR, RSI, Bollinger, etc.)
- [ ] Are `Draw.*` methods backed by `using NinjaTrader.NinjaScript.DrawingTools;`?
- [ ] Are multi-timeframe indexes (`BarsInProgress`, `CurrentBars[]`, `Closes[]`, `Times[]`) all valid?
- [ ] Is `AddDataSeries()` called in `State.Configure` with hardcoded arguments (not runtime variables)?
- [ ] Is `AddChartIndicator()` called ONLY from `State.DataLoaded`?
- [ ] Is `State.SetDefaults` kept lean — only defaults and `AddPlot`/`AddLine`?
- [ ] Are class-level mutable variables reset in `State.Configure` or `State.DataLoaded`?
- [ ] Are `SetStopLoss`/`SetProfitTarget` using `CalculationMode.Ticks` (not `.Price`) unless intentional?
- [ ] Is `EntriesPerDirection` + `EntryHandling` configured explicitly in `State.SetDefaults`?
- [ ] When using OrderFlowVolumeProfile: are you calling it as an indicator method, not a standalone type?
- [ ] Does the file name match the class name exactly?
- [ ] Backup the existing file before overwriting

---

## 2. STANDARD USING DIRECTIVES TEMPLATE

### For Strategies (complete block):

```csharp
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Xml.Serialization;
using NinjaTrader.Cbi;
using NinjaTrader.Gui;
using NinjaTrader.Gui.Chart;
using NinjaTrader.Gui.SuperDom;
using NinjaTrader.Gui.Tools;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.Core;
using NinjaTrader.NinjaScript.Indicators;
using NinjaTrader.NinjaScript.DrawingTools;
```

### Minimum for strategies that compile clean:

```csharp
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Windows.Media;
using System.Xml.Serialization;
using NinjaTrader.Cbi;              // Order, Execution, Position types
using NinjaTrader.Gui.Chart;         // ChartControl, ChartPanel
using NinjaTrader.Data;              // Bars, BarsPeriod, TradingHours
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.Indicators;    // SMA, EMA, ATR, RSI, etc.
using NinjaTrader.NinjaScript.DrawingTools;  // Draw.HorizontalLine, Draw.Dot, etc.
```

### 🔥 CRITICAL: Missing using = silent compile failure

| What you're using | Required `using` | Error if missing |
|---|---|---|
| `Draw.HorizontalLine()`, `Draw.Dot()`, `Draw.Text()` | `NinjaTrader.NinjaScript.DrawingTools` | "The name 'Draw' does not exist" |
| `SMA(20)`, `EMA(14)`, `RSI(14,3)` | `NinjaTrader.NinjaScript.Indicators` | Indicator not recognized |
| `Order`, `Execution`, `Position` | `NinjaTrader.Cbi` | Type not found |
| `BarsPeriod`, `TradingHours` | `NinjaTrader.Data` | Type not found |
| `Brushes.Blue` | `System.Windows.Media` | "The name 'Brushes' does not exist" |

---

## 3. NINJASCRIPT LIFECYCLE — STATE MANAGEMENT

### State Order for Strategies

```
State.SetDefaults     → UI defaults (keep lean!)
State.Configure       → AddDataSeries, custom resources
State.DataLoaded      → Instantiate indicators, Series<T>, Bars/Instrument access
State.Historical      → Processing historical bars
State.Transition      → Historical → Realtime handoff
State.Realtime        → Live data
State.Terminated      → Cleanup/dispose
```

### Where to Place Resources

| Resource | Earliest safe state | Notes |
|---|---|---|
| `AddDataSeries()` | `State.Configure` | Hardcoded args only |
| `SMA()`, `EMA()`, indicators | `State.DataLoaded` | Depend on bars being loaded |
| `Series<T>` construction | `State.DataLoaded` | Needs `this` |
| `AddChartIndicator()` | `State.DataLoaded` ONLY | Won't work elsewhere |
| `Bars`, `Instrument`, `TickSize` | `State.DataLoaded` | Null before this |

### Key Gotcha: UI Instance Pollution
Every time the Indicators/Strategies dialog opens, ALL scripts go through `SetDefaults → Terminated`. Keep `State.SetDefaults` lean — it runs constantly.

---

## 4. MULTI-TIMEFRAME PATTERNS

```csharp
// In State.Configure — hardcoded arguments only
AddDataSeries(BarsPeriodType.Minute, 5);  // 5-min secondary

// In OnBarUpdate
if (CurrentBars[0] < 20 || CurrentBars[1] < 20) return;
if (BarsInProgress == 0)
{
    double secondaryClose = Closes[1][0];  // 5-min close
    // Times[1][0], Highs[1][0], Lows[1][0], Opens[1][0]
}
```

### 🔥 Host + Hosted Rule
If Strategy A hosts Indicator B and B calls `AddDataSeries()`, Strategy A must ALSO call the SAME `AddDataSeries()`. Otherwise: `"A hosted indicator tried to load additional data..."` error.

---

## 5. INDICATOR USAGE IN STRATEGIES

```csharp
// Declare at class level
private SMA mySMA;

// Instantiate in State.DataLoaded
mySMA = SMA(20);

// Use in OnBarUpdate
double smaVal = mySMA[0];
double priorSma = mySMA[1];
```

### Common Signatures
```csharp
SMA(int period)
EMA(int period)
ATR(int period)
RSI(int period, int smooth)              // RSI(14, 3) standard
Bollinger(int period, double stdDev)     // Bollinger(20, 2)
MIN(int period) / MAX(int period)
PriorDayOHLC()
Stochastics(int d, int k, int smooth)    // Stochastics(14, 3, 3)
MACD(int fast, int slow, int smooth)     // MACD(12, 26, 9)
```

### AddChartIndicator (display-only, State.DataLoaded only)
```csharp
AddChartIndicator(SMA(20));
// ⚠️ Must also reference in OnBarUpdate if you want historical processing
```

---

## 6. ORDERFLOW VOLUME PROFILE CORRECT USAGE

### Critical Distinction
| Type | Purpose | Namespace |
|---|---|---|
| **OrderFlowVolumeProfile** | Indicator — read values programmatically | `NinjaTrader.NinjaScript.Indicators` |
| **VolumeProfileSession** | Drawing tool — visual only | `NinjaTrader.NinjaScript.DrawingTools` |

### Correct Usage in Strategies
```csharp
private OrderFlowVolumeProfile volProfile;

// In State.DataLoaded:
volProfile = OrderFlowVolumeProfile(
    NinjaTrader.NinjaScript.Indicators.ProfileDisplayMode.Price,
    NinjaTrader.NinjaScript.Indicators.ProfileResolution.Monthly,
    NinjaTrader.NinjaScript.Indicators.ProfilePeriod.One,
    NinjaTrader.NinjaScript.Indicators.ProfileTpoCount.Eight,
    NinjaTrader.NinjaScript.Indicators.ProfileValueArea.Seventy,
    NinjaTrader.NinjaScript.Indicators.ProfileSessionType.UseInstrumentSetting,
    0, 0
);

// In OnBarUpdate:
double poc = volProfile.POC[0];
double vah = volProfile.VAH[0];
double val = volProfile.VAL[0];
```

---

## 7. ORDER MANAGEMENT

```csharp
// Stop loss / profit target (use Ticks mode by default)
SetStopLoss(CalculationMode.Ticks, 20);
SetProfitTarget(CalculationMode.Ticks, 40);

// Entry handling
EntriesPerDirection = 2;
EntryHandling = EntryHandling.AllEntries;

// Entry methods
EnterLong() / EnterShort()
EnterLongLimit(price) / EnterShortLimit(price)
```

---

## 8. PROPERTY PATTERNS

```csharp
[NinjaScriptProperty]
[Range(1, int.MaxValue)]
[Display(Name = "Fast Period", Order = 1, GroupName = "Strategy Parameters")]
public int FastPeriod { get; set; }

[Browsable(false)]
public bool InternalFlag { get; set; }
```

---

## 9. FILE STRUCTURE

```csharp
namespace NinjaTrader.NinjaScript.Strategies
{
    public class MyStrategy : Strategy
    {
        #region Parameters
        // [NinjaScriptProperty] user inputs
        #endregion
        #region State Management
        // OnStateChange()
        #endregion
        #region Core Logic
        // OnBarUpdate()
        #endregion
        #region Order Events
        // OnExecutionUpdate, OnOrderUpdate, OnPositionUpdate
        #endregion
        #region Helpers
        #endregion
    }
}
```

---

## 10. COMMON COMPILE ERRORS & FIXES

| Error | Cause | Fix |
|---|---|---|
| `CS0234: 'Indicators' does not exist` | Missing using | Add `using NinjaTrader.NinjaScript.Indicators` |
| `CS0234: 'DrawingTools' does not exist` | Missing using | Add `using NinjaTrader.NinjaScript.DrawingTools` |
| `CS0103: 'Draw' does not exist` | Missing DrawingTools using | Add using |
| `CS0117: 'Draw.HorizontalLine' not found` | Old NT7 syntax | Use `Draw.HorizontalLine(this, tag, price, brush)` |
| `"Indicator not recognized"` | Not instantiated or missing using | Instantiate in DataLoaded + add Indicators using |
| `"Hosted indicator tried to load data"` | Missing AddDataSeries in host | Add matching AddDataSeries() |
| `"Object reference not set"` | Accessing before DataLoaded | Move to correct lifecycle state |
| `"Unable to load bars series"` | Dynamic AddDataSeries args | Hardcode all arguments |

---

## 11. FILE DEPLOYMENT PROCEDURE

### File Location
```
Documents\NinjaTrader 8\bin\Custom\Strategies\MyStrategy.cs
```

### Standard Deploy Steps
1. **Backup** old file (`.bak.cs` or timestamped)
2. **Write** new file
3. **Verify** using directives and class name match filename
4. **Compile** in NT8 Editor (F5)
5. **If errors**: fix first error only (subsequent errors cascade)
6. **Test** on chart with strategy enabled

### Backup Naming
```
MyStrategy.cs            ← Current active
MyStrategy.bak.cs        ← Previous version
MyStrategy_20260618.cs   ← Timestamped backup
```

---

## 12. VALIDATION CHECKLIST (Pre-Compile)

### Indicators
- [ ] All indicators instantiated in `State.DataLoaded`
- [ ] `using NinjaTrader.NinjaScript.Indicators` present
- [ ] Bollinger uses `.Upper[n]`, `.Lower[n]`, `.Middle[n]`

### Drawing Tools
- [ ] `using NinjaTrader.NinjaScript.DrawingTools` present
- [ ] NT8 syntax: `Draw.HorizontalLine(this, tag, price, brush)` NOT `DrawHorizontalLine(tag, price, Color.Red)`
- [ ] Tag names unique

### Multi-Timeframe
- [ ] `AddDataSeries()` in `State.Configure` with hardcoded args
- [ ] `CurrentBars[1]` guarded before accessing `Closes[1][0]`
- [ ] Host strategy includes AddDataSeries for hosted indicators

### Order Management
- [ ] `SetStopLoss`/`SetProfitTarget` via `CalculationMode.Ticks`
- [ ] `EntriesPerDirection` and `EntryHandling` set explicitly

### State Management
- [ ] No indicators in `State.SetDefaults`
- [ ] No `Bars`/`Instrument` in `State.SetDefaults` or `State.Configure`
- [ ] `AddChartIndicator()` ONLY in `State.DataLoaded`

### General
- [ ] Filename matches class name exactly
- [ ] Namespace: `NinjaTrader.NinjaScript.Strategies`
- [ ] Class inherits from `Strategy`
- [ ] No `public` fields (use properties)

---

## 13. DEBUG OUTPUT

```csharp
Print($"Close: {Close[0]} | SMA: {mySMA[0]}");
TraceOrders = true;  // In State.SetDefaults
Draw.Dot(this, "entry" + CurrentBar, true, 0, Low[0] - TickSize, Brushes.Green);
```

---

## 14. NT7 → NT8 QUICK REFERENCE

| NT7 | NT8 |
|---|---|
| `DrawHorizontalLine(tag, price)` | `Draw.HorizontalLine(this, tag, price, Brushes.Red)` |
| `Color.Red` | `Brushes.Red` |
| `CurrentBar` (singular) | `CurrentBars` (plural array) |
| `Close[0]` | `Close[0]` + `Closes[1][0]` (multi-series) |
| `SetStopLoss(ticks)` | `SetStopLoss(CalculationMode.Ticks, ticks)` |
| `CalculateOnBarClose = true` | `Calculate = Calculate.OnBarClose` |

---

## 15. GMDEEP-SPECIFIC NOTES

```bash
# SSH deploy
scp MyStrategy.cs gmdeep:"C:/Users/stewa/Documents/NinjaTrader 8/bin/Custom/Strategies/"

# Verify arrival
ssh gmdeep "dir \"C:\Users\stewa\Documents\NinjaTrader 8\bin\Custom\Strategies\MyStrategy.cs\""
```

### ⚠️ SSH Gotchas
- Windows cmd.exe interprets `&&` and `|` before PowerShell
- Split chained commands into separate SSH calls
- NT8 Editor must be open for compilation (no CLI-only compile)

---

## 16. SKILL USAGE

When doing NT8 NinjaScript work:
1. **Read this skill first** before writing `.cs` code
2. **Always start with the using directives template** (§2)
3. **Run the pre-deploy checklist** (§1) before writing a file
4. **Run the validation checklist** (§12) before compilation
5. **Always backup** before overwriting (§11)
6. **Use the state lifecycle reference** (§3) for correct code placement
7. **For VolumeProfile**: use `OrderFlowVolumeProfile` indicator, not `VolumeProfileSession` drawing tool (§6)

### Standard Coding Sequence
```
1. Paste using directives template
2. Write State.SetDefaults (lean, parameters only)
3. Write State.Configure (AddDataSeries if needed)
4. Write State.DataLoaded (instantiate indicators)
5. Write OnBarUpdate core logic
6. Run validation checklist
7. Deploy → Compile → Fix → Repeat
```
