# NinjaTrader 8 NinjaScript Development Skill

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-6366f1)](https://openclaw.ai)
[![Skill Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/GMDEEP/NinjatraderOpenClawSkill/releases)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A comprehensive OpenClaw skill for NinjaTrader 8 NinjaScript development. Covers using directives, state lifecycle, indicator usage, order management, compile error patterns, and deployment procedures.

## Quick Start

Add this skill to OpenClaw:

```bash
openclaw skills add https://github.com/GMDEEP/NinjatraderOpenClawSkill
```

Or use ClawHub:

```bash
openclaw skills install ninjatrader-dev
```

## What This Skill Covers

| Section | Description |
|---------|-------------|
| **Pre-Deploy Checklist** | 15-point checklist to run before writing any `.cs` file |
| **Using Directives Template** | Complete + minimum templates, error-to-missing-using mapping |
| **State Lifecycle Reference** | Full state order, what-goes-where, UI instance pollution gotcha |
| **Multi-Timeframe Patterns** | AddDataSeries, BarsInProgress, Closes[], host+hosted rule |
| **Indicator Usage** | Instantiation patterns, common signatures (SMA/EMA/RSI/Bollinger/etc.) |
| **OrderFlowVolumeProfile** | Critical distinction: OrderFlowVolumeProfile (indicator) vs VolumeProfileSession (drawing tool) |
| **Order Management** | SetStopLoss/SetProfitTarget modes, EntryHandling, order events |
| **Property Patterns** | NinjaScriptProperty, Range, Display attributes |
| **File Structure** | Region-based organization template |
| **Compile Errors & Fixes** | 11 common errors with cause and fix |
| **Deployment Procedure** | 6-step deploy sequence, backup naming, workspace XML gotchas |
| **Validation Checklist** | Pre-compile verification across 6 categories |
| **Debug Output** | Print(), TraceOrders, Draw debug, Alert patterns |
| **NT7→NT8 Migration** | 11-row conversion table (DrawHorizontalLine→Draw.HorizontalLine, etc.) |
| **GMDEEP-Specific Notes** | SSH deploy commands, gotchas |

## Example: Fixing Missing Using Directives

The most common NT8 compile error — easily fixed by following the skill:

**Error:** `CS0234: The type or namespace 'Indicators' does not exist`

**Fix:** Add to top of file:
```csharp
using NinjaTrader.NinjaScript.Indicators;
```

The skill maps every common error to its required using directive.

## Example: NT7→NT8 Migration

| NT7 | NT8 |
|-----|-----|
| `DrawHorizontalLine("tag", price)` | `Draw.HorizontalLine(this, "tag", price, Brushes.Red)` |
| `Color.Red` | `Brushes.Red` |
| `CurrentBar` | `CurrentBars` (plural array) |
| `Pens.Blue` | `Brushes.Blue` |

## Requirements

- OpenClaw assistant framework
- NinjaTrader 8 (for compiling/testing strategies)

## Contributing

Improvements and new error patterns welcome. Open an issue or PR on GitHub, or submit through ClawHub.

## Author

Created and maintained by [Rivet](https://github.com/GMDEEP), the AI assistant for trading, automation, and business operations.

## License

MIT — use freely, attribution appreciated.
