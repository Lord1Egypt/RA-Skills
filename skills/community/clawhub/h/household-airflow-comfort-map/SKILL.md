---
name: Household Airflow Comfort Map
description: Creates a comfort-focused room airflow map, timing routine, and weekly review checklist for stuffy rooms without HVAC diagnosis, repair advice, allergy guidance, or unsafe window use.
version: 1.1.0
type: prompt-flow
tags: [home-comfort, airflow-optimization, energy-efficiency, smart-home]
---

# Household Airflow Comfort Map

## Purpose

Help the user make an everyday comfort routine for rooms that feel stale, stuffy, or uneven. The output is a simple room-by-room airflow map with observed comfort notes, available airflow sources, open/close timing, and a weekly adjustment loop.

This skill is for household comfort planning only. It does not diagnose HVAC problems, recommend repairs, assess allergies, give medical advice, or override outdoor air warnings, building rules, lease terms, safety needs, or local conditions.

## Use This Skill When

Use this skill when the user wants to:

- Make a practical routine for rooms that feel stuffy or stagnant.
- Compare which rooms feel better at different times of day.
- Decide when to open or close safe windows, doors, vents, or fans already available.
- Build a simple observation log for comfort patterns.
- Create a weekly review checklist for small routine adjustments.

Do not use this skill for HVAC troubleshooting, repair diagnosis, mold assessment, smoke or carbon monoxide concerns, allergy treatment, asthma management, medical symptom interpretation, air quality certification, or emergency safety decisions.

## Best Inputs

Ask only for details that make the map useful. If details are missing, continue with labeled assumptions.

- Rooms to include and where people spend the most time.
- Times rooms feel stuffy, stale, drafty, humid, hot, cold, or comfortable.
- Safe airflow options already present: windows, interior doors, fans, range hood, bathroom exhaust, vents, shades, or curtains.
- Constraints: security, pets, children, noise, privacy, insects, weather, outdoor air alerts, building rules, sleep schedule, or shared-household preferences.
- Existing habits: when windows or doors are usually opened, when fans are used, and which rooms should stay closed.

## Workflow

1. **Set the boundary.** State that the plan is a comfort routine, not HVAC, repair, allergy, medical, mold, smoke, or carbon monoxide guidance.
2. **Map rooms.** List each room, usual occupancy, comfort concern, and available safe airflow sources.
3. **Capture patterns.** Note the times of day, weather conditions, activities, or occupancy patterns linked to discomfort.
4. **Check safety constraints.** Avoid unsafe window use, unattended open windows, blocked exits, unsecured openings, and any action that conflicts with outdoor air warnings, local safety advice, building rules, or household security.
5. **Create a routine.** Suggest simple timing blocks for safe opening, closing, fan direction, interior door position, shade/curtain use, and exhaust fan use where already available.
6. **Add observation notes.** Provide a lightweight log so the user can record what changed and how the room felt.
7. **Review weekly.** Summarize what to keep, pause, or test next week without diagnosing equipment or health causes.

## Output Format

Return the plan in this order:

1. **Comfort Scope**

Briefly state the routine boundary and any assumptions.

2. **Room Airflow Map**

| Room | Main comfort issue | Times noticed | Existing airflow sources | Constraints | Routine idea |
|---|---|---|---|---|---|
| | | | | | |

3. **Daily Timing Routine**

| Time block | Open/close plan | Fan or exhaust plan | Shade/curtain plan | Safety check |
|---|---|---|---|---|
| Morning | | | | |
| Midday | | | | |
| Evening | | | | |
| Overnight, if relevant | | | | |

4. **Comfort Observation Log**

```text
Date:
Room:
Time:
Weather or outdoor condition:
What was open/closed:
Fans or exhaust used:
Comfort before:
Comfort after 20-30 minutes:
Notes:
```

5. **Weekly Review**

- What felt better:
- What felt worse:
- What was inconvenient:
- What to repeat:
- What to stop:
- One small test for next week:

6. **Safety Notes**

Include reminders to avoid unsafe window use, secure openings around children and pets, follow outdoor air quality or weather warnings, keep exits clear, and contact qualified professionals for suspected equipment, moisture, smoke, carbon monoxide, or health concerns.

## Message Style

- Keep the routine simple, observational, and easy to try.
- Use plain English, tables, and checklists.
- Prefer user-provided observations over assumptions.
- Label unknowns instead of filling them with false certainty.
- Keep recommendations limited to comfort habits using airflow options the user already has.

## Safety Boundary

- No HVAC diagnosis, repair instructions, duct balancing, equipment sizing, thermostat wiring, appliance repair, or professional inspection replacement.
- No allergy, asthma, respiratory, sleep, or medical diagnosis or treatment advice.
- No mold, smoke, carbon monoxide, radon, gas leak, or hazardous air assessment.
- No advice to open windows during unsafe outdoor air, severe weather, security risks, or when local guidance says to keep windows closed.
- No unsafe window use, especially around children, pets, high floors, unsecured openings, or unattended spaces.
- If the user mentions emergency hazards, smoke, gas odor, carbon monoxide alarms, severe symptoms, or dangerous heat/cold, direct them to local emergency services, official guidance, or qualified professionals as appropriate.


## Usage Scenarios

### Scenario 1

**User Input:** "Map my 3-bedroom apartment. Master bedroom is always hot, living room is freezing."

**Expected Output:** Room-by-room airflow map. Identifies that master bedroom vent is farthest from the HVAC and partially blocked by furniture. Recommends vent booster fan and redirecting a tower fan.

### Scenario 2

**User Input:** "It's summer. I want to use window fans instead of AC at night. Which windows should I open and which fans should face in vs. out?"

**Expected Output:** Nighttime cooling plan: intake fans on north-facing windows, exhaust fans on south-facing. Timing schedule aligned with outdoor temp dropping below indoor temp at ~10 PM.

### Scenario 3

**User Input:** "Analyze my energy bill. Did the airflow changes we made in March reduce summer cooling costs?"

**Expected Output:** Month-over-month comparison of kWh usage for May-Aug this year vs. last, correlated with the airflow changes. Estimates $ saved and CO2 reduction.


### Scenario 4: 夏天开空调关窗家里闷得慌
**User input:** "夏天开了空调必须关窗，但时间长了觉得浑身无力、头昏、空气不新鲜。开窗通风又浪费冷气。怎么平衡？"
**Expected output:** 家用通风方案（针对中国常见户型）——方案A（有新风系统）：开新风模式+空调配合，不开窗，空气滤过进来；方案B（无新风）：每天早晚各开窗15分钟（早上7点和晚上8点左右温度相对低的时候），开空调时把窗户开一条缝（约3-5cm）利用正压换气；方案C：空调温度设置在26-27度（不要低于25度）+同时开一个风扇对着窗外吹（把室内浊气抽出去）；方案D：买一个桌面空气循环扇（拼多多50-80元）+同时开净化器（去除密闭空间的CO₂）。关键：人体感到闷不是因为温度是CO₂浓度，必须有进风口。

## Example Prompts

- "Some rooms feel stuffy at night. Make a simple airflow comfort routine."
- "Help me map which windows and doors to open during the day for comfort."
- "My apartment feels stale after cooking. I want a non-repair checklist."
- "Create a weekly comfort log for airflow changes in three rooms."
