# Extraction Patterns for Paper-to-Table

## Core Philosophy

**Extract what is there. Do not invent what is not.**

Every extraction must be grounded in the actual paper text. When in doubt, mark as "N/A" with a note about what was ambiguous.

---

## LLM Prompt Template

### Primary Extraction Prompt

```
You are extracting information from an academic paper to populate a literature review table.

## QUALITY RULES (STRICT)
1. EXTRACT ONLY what is explicitly stated in the paper
2. NEVER hallucinate or infer information not present
3. NEVER combine information from multiple sources into one field unless explicitly stated
4. Use "N/A" for information that cannot be found after thorough search
5. Rate confidence for each field: HIGH (explicitly stated), MEDIUM (implied but clear), LOW (inferred or ambiguous)
6. If a field contains multiple items, separate with semicolons
7. Preserve the original language of the paper

## TABLE HEADERS (Columns to fill)
{headers}

## HEADER DEFINITIONS
{header_definitions}

## PAPER CONTENT
{paper_text}

## EXTRACTION INSTRUCTIONS
For each header:
1. Search the paper content thoroughly for explicit mentions
2. Extract the exact or closely paraphrased information
3. Assign confidence score
4. If not found, use "N/A"

## OUTPUT FORMAT
Return ONLY a JSON object with this structure:
{{
  "Header1": {{
    "value": "extracted value or N/A",
    "confidence": "HIGH/MEDIUM/LOW",
    "source": "brief note on where in paper this was found"
  }},
  "Header2": {{ ... }},
  ...
}}
```

---

## Header Definitions by Domain

### Universal Fields (All Domains)

| Header | Definition | Extraction Rules | Examples |
|--------|-----------|------------------|----------|
| **Title/标题** | Full paper title | Extract exactly as published; include subtitle if present | "The Role of Dopamine in Reward Prediction" |
| **Authors/作者** | All authors in order | List all; use "et al." only if more than 10; preserve order | "Smith, J., Jones, M., et al." |
| **Year/年份** | Publication year | 4-digit year only; check header/footer/citation info | 2024 |
| **Journal/期刊** | Publication venue | Full journal name; include volume/issue if in header | "Nature Neuroscience, 45(3)" |
| **DOI** | Digital object identifier | Extract complete DOI string | "10.1038/s41593-024-01623-4" |
| **Objective/研究目标** | Main research question or hypothesis | State in authors' own words or close paraphrase; distinguish primary from secondary objectives | "To investigate whether dopamine signals encode reward prediction errors" |
| **Method/研究方法** | Overall study design | Summarize in 1-2 sentences; specify type (experimental, observational, computational, etc.) | "Randomized controlled trial with double-blind design" |
| **Sample Size/样本量** | Number of participants/samples | Extract exact numbers; note attrition if reported | "N = 120 (final N = 108 after attrition)" |
| **Key Findings/主要发现** | Main results | 2-3 bullet points or sentences; include effect sizes if reported | "1. Dopamine neurons showed phasic responses to reward cues (Cohen's d = 0.82)" |
| **Conclusion/结论** | Authors' main conclusion | Direct quote or close paraphrase; distinguish from speculation | "These results support the hypothesis that dopamine encodes reward prediction errors" |
| **Limitations/局限性** | Study limitations mentioned | List explicitly mentioned limitations; do not add your own | "Small sample size; cross-sectional design limits causal inference" |

---

### Psychology-Specific Fields

| Header | Definition | Extraction Rules | Examples |
|--------|-----------|------------------|----------|
| **Participants/被试** | Demographic and sampling details | Age range, gender distribution, recruitment method, inclusion/exclusion criteria | "University students (N=85), age 18-25, 62% female" |
| **Experimental Design/实验设计** | Design type and structure | Between-subjects, within-subjects, mixed; number of conditions | "2×3 mixed design: Group (control/experimental) × Time (pre/post/follow-up)" |
| **Measures/测量工具** | Psychometric instruments or behavioral measures | Name of scale, number of items, reliability (Cronbach's α) if reported | "Beck Depression Inventory-II (BDI-II; α = .92)" |
| **Manipulation/实验操纵** | Independent variable manipulation | How IV was manipulated; check manipulation validation | "Participants wrote about a negative experience for 15 minutes" |
| **Effect Size/效应量** | Reported effect sizes | Extract exact values with confidence intervals if available | "Cohen's d = 0.65, 95% CI [0.32, 0.98]" |
| **Preregistration/预注册** | Whether study was preregistered | Extract preregistration platform and ID if available | "OSF: https://osf.io/abc123" |

---

### Cognitive Neuroscience-Specific Fields

| Header | Definition | Extraction Rules | Examples |
|--------|-----------|------------------|----------|
| **Imaging Modality/成像模态** | Neuroimaging method | fMRI, EEG, MEG, PET, etc.; include scanner specifications | "3T Siemens Prisma MRI" |
| **Preprocessing/预处理** | Data preprocessing pipeline | Software used, main preprocessing steps | "SPM12: realignment, coregistration, normalization (MNI), smoothing (8mm FWHM)" |
| **Task Paradigm/任务范式** | Experimental task details | Task name, trial structure, timing parameters | "Delayed match-to-sample task; 2s stimulus, 3s delay, 2s probe" |
| **Brain Regions/脑区** | Regions of interest or significant clusters | Use standard anatomical names; include MNI coordinates for peak voxels | "Left dorsolateral prefrontal cortex (MNI: -42, 18, 34)" |
| **Analysis Type/分析类型** | Statistical analysis approach | GLM, MVPA, connectivity, etc.; software package | "GLM with FSL FEAT; group-level mixed-effects analysis" |
| **Behavioral-Neural Correlation/行为-神经关联** | Relationship between behavior and neural measures | Report correlation coefficients and significance | "r(28) = .54, p < .001 between accuracy and hippocampal activation" |

---

### Computer Science-Specific Fields

| Header | Definition | Extraction Rules | Examples |
|--------|-----------|------------------|----------|
| **Algorithm/算法** | Proposed or evaluated algorithm | Name and brief description; distinguish from baseline methods | "Transformer-XL with recurrence mechanism" |
| **Model Architecture/模型架构** | Neural network or model structure | Layer types, dimensions, key components | "6-layer encoder-decoder, 512-dim embeddings, 8 attention heads" |
| **Dataset/数据集** | Training/evaluation datasets | Dataset name, size, source; distinguish train/validation/test | "ImageNet-1K (1.28M train, 50K validation); COCO 2017" |
| **Training Details/训练细节** | Training procedure | Optimizer, learning rate, batch size, epochs, hardware | "AdamW, lr=1e-4, batch=256, 100 epochs, 8×V100" |
| **Metrics/评估指标** | Evaluation metrics | Primary and secondary metrics with values | "Accuracy: 94.2%; F1: 0.891; Inference: 12ms/sample" |
| **Code Availability/代码可用性** | Code or model availability | GitHub link, license, reproducibility statement | "https://github.com/user/repo; MIT License" |
| **Ablation Results/消融实验** | Ablation study findings | Key ablation comparisons and their impact | "Removing attention mechanism: -3.2% accuracy" |

---

### Brain Science-Specific Fields

| Header | Definition | Extraction Rules | Examples |
|--------|-----------|------------------|----------|
| **Species/物种** | Animal species or model organism | Full species name; strain if relevant | "Mus musculus (C57BL/6J)" |
| **Brain Region/脑区** | Target brain region | Standard anatomical nomenclature; laterality | "Hippocampal CA1 region, bilateral" |
| **Recording Method/记录方法** | Neural recording technique | Electrophysiology, calcium imaging, etc.; probe details | "Silicon probe recording (64-channel, 25μm spacing)" |
| **Stimulation/刺激** | Stimulation parameters if applicable | Type, frequency, intensity, duration | "Optogenetic stimulation: 473nm, 20Hz, 5ms pulses, 10s duration" |
| **Cell Type/细胞类型** | Targeted cell population | Genetic markers, morphological classification | "Parvalbumin-positive interneurons (PV-Cre mice)" |
| **Behavioral Task/行为任务** | Associated behavioral paradigm | Task name and key parameters | "Morris water maze: 90s trials, 4 trials/day, 5 days" |

---

## Extraction Strategies

### Strategy 1: Structured Sections (Preferred)

When the paper has clear sections, extract systematically:

1. **Abstract** → Title, Authors, Objective, Key Findings (brief)
2. **Introduction** → Objective, Hypothesis, Theoretical Background
3. **Methods** → Method, Sample Size, Participants, Measures, Task Paradigm, Imaging Modality
4. **Results** → Key Findings, Effect Sizes, Metrics, Brain Regions
5. **Discussion/Conclusion** → Conclusion, Limitations, Implications

### Strategy 2: Unstructured Content

When sections are unclear:
1. First 500 words → Title, Authors, Objective, Hypothesis
2. Middle sections → Look for methodology keywords ("participants", "stimuli", "procedure", "analysis")
3. Final 500 words → Conclusions, limitations, future directions
4. Tables/Figures captions → Sample sizes, key results, statistical values

### Strategy 3: Citation and Metadata

Always check:
- **Header/footer** → Journal, year, volume, DOI
- **First page** → Complete author list, affiliations
- **Acknowledgments/Funding** → Sometimes contains preregistration info
- **Supplementary materials reference** → Additional datasets, code

---

## Multi-Language Handling

### English Papers
- Extract as-is
- Maintain English for all fields unless user requests translation
- Keep technical terms in English even if translating

### Chinese Papers
- Extract as-is
- Maintain Chinese for all fields unless user requests translation
- Keep proper nouns (names, places) in original form

### Mixed Content
- Preserve the language of the original text for each field
- If a field contains both languages, include both with clear separation

---

## Confidence Scoring Guide

### HIGH Confidence
- Information is explicitly stated in the paper
- Direct quotes or clear paraphrases available
- Located in standard sections (Abstract, Methods, Results)

### MEDIUM Confidence
- Information is implied but clearly inferable
- Located in Discussion or supplementary materials
- Requires minor synthesis of multiple statements

### LOW Confidence
- Information is ambiguous or contradictory
- Requires significant inference
- Located in non-standard sections or footnotes
- Mark as LOW and provide reasoning

---

## Common Pitfalls to Avoid

1. **Don't confuse correlation with causation** → If the paper says "associated with", don't extract "causes"
2. **Don't report planned analysis as completed** → Distinguish preregistered plans from actual results
3. **Don't mix up sample sizes** → Distinguish between recruited, final, and per-analysis N
4. **Don't report predictions as findings** → Hypotheses go in Objective, results go in Key Findings
5. **Don't extract from abstracts alone for complex fields** → Always check Methods for details
