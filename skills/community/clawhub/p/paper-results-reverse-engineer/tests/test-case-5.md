# Test Case 5: PDF File Upload — Auto-Extract Results

## Scenario
User uploads a PDF file of a paper. The agent must:
1. Extract text with `pdftotext`
2. Auto-detect the Results section boundary
3. Confirm with user
4. Proceed with full A–G modules

## Input
User message: "帮我拆这篇论文的 Results"
Attachment: `Hauner_et_al_2013_TMR_fear_extinction.pdf`

## Expected Agent Behavior

### Step 1: Extract text from the PDF

Agent runs:
```bash
pdftotext -layout "<path/to/uploaded/Hauner_et_al_2013_TMR_fear_extinction.pdf>" /tmp/paper_extracted.txt
```

If successful, reads `/tmp/paper_extracted.txt`. If the PDF is scanned (image-only, pdftotext returns empty), agent responds:
> `该 PDF 为扫描版，无法提取文字。请提供可选中文字的 PDF，或直接粘贴 Results 部分的文本。`

### Step 2: Scan for Results section

Agent searches for section markers. In this paper, the structure is:
```
Introduction
Materials and Methods
Results
  3.1 Fear acquisition
  3.2 Effects of TMR on fear extinction
  3.3 Sleep architecture and TMR efficacy
Discussion
References
```

Agent identifies:
- Start: `Results` heading
- End: `Discussion` heading
- Content: 3 sub-sections with clear headings

### Step 3: Confirm with user

Agent prints:
```
✅ 已从 PDF 提取全文并自动识别 Results 部分：
  - 小节数：3
  - 小节标题：3.1 Fear acquisition / 3.2 Effects of TMR on fear extinction / 3.3 Sleep architecture and TMR efficacy
  - 字数：约 1240 字
  - 涉及图表：Figure 2A, Figure 3A

如需调整提取范围，请告知。否则开始完整 A–G 模块分析。
```

### Step 4: Modules A–G (expected output markers)

**Module A:**
- 研究主题: TMR during SWS for attenuating conditioned fear
- 样本: from Methods section (extracted): N = 36, 18 female, M_age = 23.4
- IV: Cue (cued vs. uncued CS+, within-subjects); SWS duration (continuous)
- DV: SCR to CS+ (μS), TMR efficacy index

**Module B structure map:**
- 3.1: Fear acquisition check — did conditioning work for everyone?
- 3.2: Main effect — does TMR reduce fear to cued stimuli?
- 3.3: Individual differences — does SWS amount predict TMR benefit?

**Module C — key annotations:**
- 3.1 S1: "All participants successfully acquired conditioned fear..." → Label 3 + 6 (overview + stats)
- 3.2 S1: "To test whether TMR during SWS enhances..." → Label 1
- 3.2: "As shown in Figure 2A" → Label 4
- 3.2: "Importantly, this TMR benefit was specific to the cued CS+" → Label 7 + specificity framing
- 3.3: "We next examined whether individual differences..." → Label 1
- 3.3: "Consistent with the active systems consolidation model" → Label 9
- 3.3: "We note that the modest sample size..." → Label 12

**Module D:**
- Figure 2A: No screenshot available → agent flags "⚠️ 未提供图表截图，以下仅基于 caption 和正文推断。建议上传图表截图以获得更准确分析。"
- Still provides: question, inferred axes, key pattern, 1-min narration from text

**Module F — critical checks:**
- [ ] 结果与讨论混杂: Clean — no Discussion in Results
- [x] 统计报告: t, df, p, d, r, partial r all reported
- [ ] 选择性强调: CS− null result reported as "did not differ (p = .612)" but without descriptive stats or effect size
- [ ] 过度解释: "suggesting that TMR selectively reduced fear without generalizing" — null on CS− is taken as positive evidence for specificity

**Module G:**
- 写作逻辑: Ladder structure (acquisition → main effect → mechanism/individual differences)
- 最值得模仿: (1) Specificity framing with null results; (2) Theoretical anchoring before stats; (3) Control analysis (partial r) for robustness
- 需警惕: (1) Null ≠ evidence of absence for CS− specificity claim; (2) N = 36 for individual difference correlations; (3) "Consistent with [model]" is post-hoc alignment

## Edge Cases Tested

1. **pdftotext extraction** — handles real PDF binary, not just pasted text
2. **Scanned PDF detection** — agent checks if extraction returns empty/garbled, offers fallback
3. **Section boundary detection** — `Results` → `Discussion` with numbered sub-sections
4. **Cross-section information gathering** — pulling sample info from Methods to fill Module A
5. **Missing figures** — agent flags and falls back to caption+text analysis
6. **Mixed case headings** — handles `Results` / `RESULTS` / `Results and Discussion`
