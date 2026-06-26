---
name: gt7-tuner
version: 1.0.0
description: AI tuning assistant for Gran Turismo 7. Send a photo of your GT7 settings screen → get a complete optimized tune via GT Pro Tune calculator. Supports all 581 cars, every track, and any driving style.
author: tristan-labs
tags: [gaming, gran-turismo, gt7, tuning, racing, playstation]
metadata:
  openclaw:
    emoji: "🏎️"
---

# GT7 Tuner — Gran Turismo 7 AI Tuning Assistant

> Turn any GT7 car into a weapon. Send a screenshot, get a pro tune.

## Prerequisites

⚠️ **You need a GT Pro Tune account** (https://app.gtprotune.com/)
- Free accounts have limited features
- **Pro account recommended** ($4.99/month) — unlocks full suspension/transmission calculations, Image Analyzer, and Race Engineer
- Sign up at https://app.gtprotune.com/register
- Store your credentials securely (never log or echo them)

## When to Use
- User wants to tune a car in Gran Turismo 7
- User sends a screenshot/photo of their GT7 car settings
- User mentions GT Pro Tune, car setup, suspension, gearing, or tuning
- User says something like "tune my [car] for [track]"
- Any Gran Turismo 7 tuning-related request

## How It Works

### The Quick Flow
1. **User sends a photo** of their GT7 settings screen (from TV/monitor)
2. **Agent reads the values** using vision (OCR) — PP, weight, HP, tire compound, etc.
3. **Agent confirms values** with user (confidence check — only use values that are clearly readable)
4. **Agent fills GT Pro Tune** via agent-browser automation
5. **Agent reads the calculated tune** and reports it back
6. **User applies the tune** in GT7

### Photo OCR Pipeline
When the user sends a GT7 screenshot (photo of TV screen):

1. Read the image with vision capabilities
2. Extract all visible values: PP, weight (kg or lbs), HP, torque, tire compound, etc.
3. For each value, assess confidence:
   - **High confidence (>95%)**: use directly
   - **Low confidence**: ask user to confirm or re-send a clearer photo
4. Convert units if needed (kg → lbs, kW → HP, Nm → ft-lb)
5. Present extracted values to user for confirmation before proceeding

**Tips for better photos:**
- Take the photo straight-on (reduce angle)
- Minimize screen glare/reflections
- Ensure the full settings screen is visible
- PS5 screenshots via Share button → PS App are ideal (pixel-perfect)

## GT Pro Tune Web App

### Login
```bash
agent-browser open "https://app.gtprotune.com/login"
# Fill email and password fields, click Login
# Credentials must be stored securely — NEVER log, echo, or display them
```

### Important: Angular Input Handling
GT Pro Tune is built with Angular 17. When filling form fields:
- **Use `agent-browser fill @ref "value"` followed by `agent-browser press "Tab"`** — this triggers Angular's change detection
- **Do NOT use eval/DOM manipulation** to set values — Angular's reactive forms won't detect the changes
- **For dropdowns (ngb-typeahead)**: type the search text, wait for results, then use eval to click the matching option
- **For select elements**: use `agent-browser select @ref "value"`

### App Structure

#### Tab 1: Car/Track Settings
| Field | Type | Notes |
|---|---|---|
| Vehicle | Typeahead search | 581 cars, type to filter |
| Performance Points | Number | PP rating |
| Weight | Number | In pounds (lbs) |
| Track | Typeahead search | Type to filter |
| Tire Size | Number | In inches |
| Front Tires | Dropdown | Comfort/Sport/Racing × Hard/Medium/Soft |
| Rear Tires | Dropdown | Same options as front |

#### Tab 2: Suspension Settings
| Section | Fields |
|---|---|
| Base Performance | Front-Rear Weight Balance (%) |
| Stability | Low Speed, High Speed (text: understeer/oversteer) |
| Rotational G | G at 40mph, 75mph, 150mph |
| Suspension | Body Height Front/Rear (mm), Oversteer/Understeer slider |
| Aerodynamics | Downforce Front/Rear |
| Race/Track Parameters | Spring Stiffness, ARB Stiffness, Tire Wear multiplier |
| Other Adjustments | Corner Entry/Exit balance, Offset Spring Frequency |

#### Tab 3: Transmission Settings
| Section | Fields |
|---|---|
| Engine Data | HP, RPM (min/max/peak), Max Torque (ft-lb) |
| Differential | LSD Setting |
| Gears | Top Speed (MPH), Number of Gears (3-9), Final Gear, Gear Ratios |
| Corner Speed | Min Corner Speed (MPH), Min Corner Speed Gear |

### Vehicle Selection (Angular Typeahead)
```bash
agent-browser click @e15                    # Focus vehicle search
agent-browser keyboard type "F8 Tributo"    # Type car name (spaces may cause CDP errors — use partial names)
sleep 2                                     # Wait for dropdown
agent-browser eval "(function(){var items=document.querySelectorAll('ngb-typeahead-window button');var match=Array.from(items).find(function(e){return e.textContent.includes('F8 Tributo')});if(match){match.click();return 'selected'}return 'not found'})()"
```

### Reading Results
After filling all three tabs, the app calculates:

**Suspension output table:**
- Anti-Roll Bar (Front/Rear)
- Damper Compression (Front/Rear)
- Damper Extension (Front/Rear)
- Spring Rate (Front/Rear)
- Camber Angle (Front/Rear)
- Toe Angle (Front/Rear)

**Transmission output table:**
- Final Gear Ratio
- Individual Gear Ratios (1st through 7th+)

**Differential output table:**
- Initial Torque (Front/Rear)
- Acceleration (Front/Rear)
- Deceleration (Front/Rear)

### Image Analyzer (Premium Feature)
GT Pro Tune has a built-in Image Analyzer that can extract dyno data from GT7 screenshots:
```bash
agent-browser click @e7  # Image Analyzer button
# Upload a screenshot of the dyno/power graph from GT7
```

## Driving Style Presets

When the user describes a driving style, translate to suspension parameters:

| Style | Oversteer Bias | LSD | Spring Stiffness | Notes |
|---|---|---|---|---|
| **Aggressive / Verstappen** | +2 oversteer | +2 LSD | +1 stiff | Late braking, throttle steering, rotate on entry |
| **Balanced / Hamilton** | 0 neutral | 0 | 0 | All-round consistency, predictable |
| **Safe / Defensive** | -1 understeer | -1 LSD | -1 soft | Stability first, forgiving on corner entry |
| **Drift** | +3 oversteer | +3 LSD | -2 soft rear | Maximum rotation, rear slides freely |

## Unit Conversions
- Weight: 1 kg = 2.20462 lbs
- Torque: 1 kgf·m = 7.233 ft-lb / 1 Nm = 0.7376 ft-lb
- Power: 1 PS ≈ 0.9863 HP (close enough to use interchangeably for GT7)

## GT7 Tuning Knowledge
See `references/gt7-tuning-knowledge.md` for:
- Latest patch changes affecting tuning (1.55, 1.66)
- Current meta (post-patch suspension, tire, LSD guidelines)
- GT7-specific physics quirks vs real-world racing
- Track-specific tuning workflows

## Notes
- All 581 GT7 cars are supported
- Units: weight in lb, height in mm, speed in MPH, torque in ft-lb
- The app calculates optimal settings — we input specs, it outputs the tune
- GT7 Race Engineer (AI feature) requires a separate subscription tier
- Always verify calculated tunes with a few laps in-game and adjust based on feel
