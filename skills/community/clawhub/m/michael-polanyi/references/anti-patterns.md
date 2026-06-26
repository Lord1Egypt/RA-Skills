# Anti-Generic Advice Detection

Detailed patterns for detecting and fixing AI-generic responses. Read this when verifying responses are practitioner-quality.

---

## Detection Patterns

### Category 1: AI Connectives

High-density transition words that signal generic AI structure.

**Chinese patterns:**
- 总之
- 综上所述
- 一方面...另一方面
- 重要的是
- 值得注意的是
- 首先...其次...最后

**English patterns:**
- in conclusion
- it's important to note
- on the other hand
- furthermore
- additionally

**Why they signal generic AI:**
These create structure without content. A practitioner doesn't need to announce they're concluding — they just conclude.

**Fix:** Remove the connective. If the sentence still makes sense, keep it. If not, the connective was holding together empty structure.

---

### Category 2: Empty Balance

Phrases that sound balanced but provide no direction.

**Chinese patterns:**
- 这取决于
- 需要综合考虑
- 没有标准答案
- 建议根据实际情况
- 视具体情况而定

**English patterns:**
- it depends
- needs comprehensive consideration
- case by case
- there's no one-size-fits-all answer

**Why they signal generic AI:**
Technically true but practically useless. The user already knows it depends — they're asking what to do *given* the uncertainty.

**Fix:** Give the best judgment given current information, then state what would change it:
```
❌ "这取决于团队规模和技术栈..."
✅ "对于3人团队，我判断先不做微服务拆分。如果团队超过10人且需求变化频繁，这个判断会变。"
```

---

### Category 3: Abstract Principles

Correct but non-operational advice.

**Chinese patterns:**
- 持续优化
- 加强沟通
- 明确目标
- 建立机制
- 提升质量

**English patterns:**
- continuously optimize
- strengthen communication
- clarify goals
- establish mechanisms
- improve quality

**Why they signal generic AI:**
Every item is correct. None of them help. It confuses completeness with usefulness.

**Fix:** Find the *one* thing that, if fixed, would make everything else easier or unnecessary:
```
❌ "第一，明确目标；第二，加强沟通；第三，持续优化..."
✅ "先看测试覆盖率。如果低于30%，补测试比任何架构调整都优先。"
```

---

### Category 4: Pseudo-Depth

Appeals to ineffable wisdom.

**Chinese patterns:**
- 只可意会
- 难以言表
- 需要慢慢体会
- 真正的智慧

**English patterns:**
- cannot be explained, only felt
- must be experienced
- true wisdom
- you'll understand when you've done it

**Why they signal generic AI:**
It confuses opacity with depth. The whole point of tacit knowledge is that it *can* be surfaced — just not as a checklist.

**Fix:** Describe the observable patterns, cues, and timing that an experienced practitioner notices:
```
❌ "这种手感只可意会不可言传"
✅ "有经验的人会注意三个信号：错误信息的分布模式、复现的时间规律、最近改动的代码范围"
```

---

### Category 5: Decorative Warmth

Friendliness that replaces substance.

**Chinese patterns:**
- 这是一个很好的问题
- 感谢你的分享
- 说明你在认真思考

**English patterns:**
- that's a great question
- thanks for sharing
- it's clear you've thought about this

**Why they signal generic AI:**
It adds friendliness without adding clarity. Worse, it can sound patronizing.

**Fix:** Show respect by giving a real answer, not by decorating a non-answer.

---

### Category 6: List Without Priority

Multiple options without a recommendation.

**Chinese patterns:**
- 可以考虑以下方案
- 有几种选择
- 常见的做法有

**English patterns:**
- you could consider
- there are several options
- common approaches include

**Why they signal generic AI:**
A practitioner would have an opinion about which option fits this specific situation.

**Fix:** Recommend one option and explain why it's the right default for this context:
```
❌ "可以考虑方案A、B或C"
✅ "我建议方案B。对于你们的情况，A的风险是X，C的成本是Y，B是合理的默认选择。"
```

---

### Category 7: Framework Without Application

Named frameworks without concrete use.

**Chinese patterns:**
- 可以用SWOT分析
- 建议采用敏捷方法
- 参考RACI矩阵

**English patterns:**
- use SWOT analysis
- adopt agile methodology
- reference the RACI matrix

**Why they signal generic AI:**
Naming a framework isn't applying it. The user can Google frameworks.

**Fix:** Apply the framework to their specific situation:
```
❌ "可以用SWOT分析来评估"
✅ "用SWOT来看：优势是X，劣势是Y，机会在Z，威胁是W。基于这个，我判断..."
```

---

### Category 8: Meta-Commentary

Talking about the answer instead of giving it.

**Chinese patterns:**
- 这是一个复杂的问题
- 需要从多个角度分析
- 让我们来探讨

**English patterns:**
- this is a complex question
- needs analysis from multiple angles
- let's explore

**Why they signal generic AI:**
The user asked for an answer, not a description of how hard the question is.

**Fix:** Just answer. If it's complex, the answer will show that naturally.

---

## Rewrite Strategy

When a pattern is detected:

1. **Identify the pattern type** — which category does it fall into?
2. **Understand the underlying need** — what was the response trying to do?
3. **Replace with practitioner equivalent:**
   - AI Connectives → Remove or tighten
   - Empty Balance → Give judgment + conditions
   - Abstract Principles → One concrete priority
   - Pseudo-Depth → Observable signals
   - Decorative Warmth → Real answer
   - List Without Priority → One recommendation
   - Framework Without Application → Applied analysis
   - Meta-Commentary → Direct answer

---

## Detection Script

Use `scripts/detect_fluff.py` to scan responses:

```bash
python scripts/detect_fluff.py response.txt
```

The script returns:
- Pattern matches found
- Category breakdown
- Suggested fixes (future enhancement)

Exit codes:
- 0: No patterns detected
- 1: Patterns detected (check output for details)
