---
name: fortune-telling
description: "Complete fortune-telling service with interactive divination sessions. Supports Chinese methods (I Ching, Ba Zi, Zi Wei, Palmistry, Face Reading, Feng Shui, Plum Blossom, Divination Lots) and Western methods (Tarot, Astrology, Numerology, Palmistry, Runes, Crystal Gazing, Oracle Cards). When user wants to: (1) Get a fortune reading, (2) Ask about their destiny/career/love, (3) Make a decision using divination, (4) Learn about fortune-telling methods. Follow the interaction workflow and generate beautiful HTML reports."
---

# Fortune-Telling Service

Comprehensive divination service with interactive sessions and beautiful HTML reports.

## Core Principle

**玄学推算 ≠ 现实分析**

- ❌ 绝对不要使用用户提供的现实信息（简历、职位、经历等）作为分析依据
- ✅ 完全依靠玄学工具（卦象、命盘、六爻）进行推算
- ✅ 用传统命理理论解读，而非逻辑推理
- ✅ 从卦象/命盘本身获取信息，不掺杂用户背景

---

## Interaction Workflow

### Step 1: Greeting & Method Selection

When user requests fortune-telling:

1. **Greet warmly** and explain available methods
2. **Present method options** in a table with difficulty and required info
3. **Let user choose** which method they want to use

#### Method Quick Reference

| Method | Info Required | Difficulty | Best For |
|--------|--------------|------------|----------|
| I Ching | Question + 3 coins | Medium | Decision making, future trends |
| Ba Zi | Birth date/time/place | Hard | Deep destiny analysis |
| Zi Wei | Birth date/time/place | Hard | Chinese astrology |
| Tarot | Question + cards | Medium | Life guidance |
| Numerology | Name + birth date | Easy | Personality insights |
| Palmistry | Palm photo | Medium | Character reading |
| Runes | Question + intent | Easy | Quick guidance |

---

### Step 2: Collect Required Information

**For divination methods ONLY:**
- **I Ching**: User's question (must be about future)
- **Tarot**: One clear question
- **Ba Zi/Zi Wei**: Birth data
- **Numerology**: Name + birth date
- **Palmistry**: Palm photos

**IMPORTANT**: Do NOT ask for or use user's real-world background information such as:
- Employment status
- Career history
- Specific job details
- Personal circumstances
- Resume content

The divination tools themselves provide the information - we don't need user context.

---

### Step 3: Conduct Divination (纯玄学推算)

#### For I Ching (Coin Method):
1. Ask user to focus on their question
2. Perform 6 coin tosses (use random number generation)
3. Record results: 6=yin, 7=yang, 8=yin, 9=yang (9 and 6 are moving lines)
4. Determine the hexagram (from bottom to top)
5. Identify any changing lines (6 and 9)

#### For Tarot:
1. Ask user to think of their question while shuffling
2. Use appropriate spread (3-card or Celtic Cross)
3. Interpret cards using symbolic meaning

#### For Ba Zi:
1. Calculate the Four Pillars from birth data
2. Determine Five Elements distribution
3. Analyze the energy patterns and luck cycles
4. Use traditional Ba Zi theory for interpretation

---

### Step 4: 玄学解读 (Pure 玄学 Theory)

**Critical**: ALL information comes from the divination, NOT from user input.

#### Examples of WRONG approach:
- "你之前的工作经历显示..." ❌
- "根据你的简历分析..." ❌
- "从你描述的情况来看..." ❌
- "你的背景显示..." ❌

#### Examples of CORRECT approach:
- "卦象推算，乾卦主阳气旺盛..."
- "八字中木气为用，代表..."
- "命盘显示官星入命，利于..."
- "变爻指向坎宫，水象主变动..."
- "从卦象看，财爻持世，财运佳..."

### 玄学解读要点：

1. **纯卦象分析** - 完全根据卦象本身解读
2. **五行流转** - 用五行生克理论
3. **宫位含义** - 根据所在宫位
4. **神煞参考** - 辅助参考
5. **不问背景** - 玄学本身就告诉你答案

### 解读模板：

```
【卦象/命盘推算】
  ↓
  本卦/变卦显示...
  用神/主星状态...
  五行生克关系...
  ↓
【玄学结论】
  → 根据卦象/命盘推算的结果
  → 不依赖任何现实信息
```

---

### Step 5: Generate HTML Report

Create a beautiful HTML card:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>易经卦象解读</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Serif SC', serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .card {
            max-width: 600px;
            margin: 0 auto;
            background: linear-gradient(145deg, #1e1e32 0%, #252545 100%);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 100px rgba(255, 215, 0, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.2);
        }
        
        .title { font-size: 28px; color: #ffd700; text-align: center; margin-bottom: 8px; }
        .subtitle { color: #8b8b9e; font-size: 14px; text-align: center; margin-bottom: 30px; }
        
        .question-box {
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .question-label { color: #ffd700; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
        .question-text { color: #fff; font-size: 18px; }
        
        .hexagrams { display: flex; justify-content: center; gap: 40px; margin-bottom: 30px; }
        .hexagram { text-align: center; }
        .hexagram-name { color: #ffd700; font-size: 20px; margin-bottom: 10px; }
        .hexagram-symbol { font-size: 48px; }
        
        .divider { text-align: center; margin: 20px 0; color: #666; }
        
        .result-box {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .result-main { color: #4ade80; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 15px; }
        .result-detail { color: #ccc; font-size: 14px; line-height: 1.8; }
        
        .advice-box {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 165, 0, 0.1) 100%);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 12px;
            padding: 20px;
        }
        
        .advice-title { color: #ffa500; font-size: 14px; margin-bottom: 10px; }
        
        .advice-list { list-style: none; }
        .advice-list li { color: #ddd; font-size: 14px; padding: 8px 0; padding-left: 24px; position: relative; }
        .advice-list li::before { content: '✓'; position: absolute; left: 0; color: #ffd700; }
        
        .quote { color: #ffd700; font-size: 18px; text-align: center; margin: 20px 0; font-style: italic; }
        
        .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1); }
        .footer-text { color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <!-- Fill in the content based on divination results -->
    </body>
</html>
```

---

### Step 6: Present the Report

1. **Send the HTML file** to the user
2. **Explain using 玄学 theory only** - do not reference user's real background
3. **Invite follow-up questions**

---

## Important Rules

### 绝对禁止 ❌

| 禁止行为 | 原因 |
|----------|------|
| 使用用户简历信息 | 不是玄学推算 |
| 分析用户职位背景 | 逻辑推理，非玄学 |
| 引用用户工作经历 | 现实信息，非卦象 |
| 询问用户现实情况 | 玄学本身就能告诉你 |

### 正确方式 ✅

| 正确行为 | 说明 |
|----------|------|
| 完全根据卦象/命盘 | 纯玄学推算 |
| 使用五行生克理论 | 传统命理 |
| 解读卦象象征意义 | 经典理论 |
| 从变爻看变化 | 卦象本身的信息 |

### What I Ching CAN Answer:
- ✅ Future decisions
- ✅ Trend analysis (from 卦象, not user context)
- ✅ Action guidance (from 玄学 theory)
- ✅ Relationship guidance (from 命盘)

---

## Reference Files

For detailed method information, see:
- [Chinese Methods](references/chinese-methods.md)
- [Western Methods](references/western-methods.md)
- [Preparation Guide](references/preparation.md)
