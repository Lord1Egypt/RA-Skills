# Test Case 7: Branch F — fMRI / Neuroimaging Study

## Scenario

User provides a Results section from an fMRI experiment examining neural correlates of successful memory encoding. The paper uses ROI analysis, whole-brain corrected activation, RSA, and brain-behavior correlations.

This test validates:
1. Three-axis classification correctly identifies Axis 1 = Experiment, Axis 3 = fMRI activation + RSA
2. Branch F rules applied: ROI pre-definition status, multiple comparison correction, brain-behavior wording
3. Mechanism-wording guardrail: "mediates/mediation" forbidden unless formal mediation model reported
4. G0 source verification fields for neuroimaging
5. Sham-control distinction (Branch A Rule 5) and closed-loop guardrails (Rule 4) are NOT triggered for non-sleep fMRI

## Input

```
Results

3.1 Behavioral Results

Recognition memory performance was assessed using a remember/know/new procedure. Overall recognition accuracy (hit rate minus false alarm rate) was above chance, M = 0.72, SD = 0.14, t(31) = 17.85, p < .001, d = 3.16. Subsequent memory analyses were based on the contrast between subsequently remembered (R) and subsequently forgotten (F) items during the encoding phase.

3.2 ROI Analysis: Hippocampal Subsequent Memory Effect

We defined three anatomical ROIs a priori based on previous literature: left hippocampus, right hippocampus, and bilateral parahippocampal gyrus. ROI masks were derived from the Automated Anatomical Labeling (AAL) atlas. Mean parameter estimates were extracted for the R > F contrast.

A 2 (Subsequent Memory: R, F) × 3 (ROI: left HC, right HC, PHG) repeated-measures ANOVA on parameter estimates revealed a significant main effect of Subsequent Memory, F(1, 31) = 24.63, p < .001, ηp² = .44, and a significant Subsequent Memory × ROI interaction, F(2, 62) = 7.41, p = .001, ηp² = .19. Follow-up paired t-tests showed significant subsequent memory effects in left hippocampus, t(31) = 5.12, p < .001, d = 0.91, 95% CI [0.52, 1.29], and right hippocampus, t(31) = 3.87, p < .001, d = 0.69, 95% CI [0.31, 1.06], but not in parahippocampal gyrus, t(31) = 1.54, p = .134, d = 0.27, 95% CI [-0.08, 0.62].

3.3 Whole-Brain Analysis

Whole-brain voxelwise analysis (cluster-defining threshold p < .001 uncorrected; cluster-level FWE-corrected p < .05) revealed three significant clusters for the R > F contrast. The largest cluster was centered in the left anterior hippocampus (MNI: -24, -14, -18; cluster size = 487 voxels; cluster-level p_FWE = .002), extending into the amygdala. A second cluster was identified in the left ventrolateral prefrontal cortex (MNI: -42, 32, -8; cluster size = 312 voxels; cluster-level p_FWE = .018). A third cluster in the right dorsolateral prefrontal cortex approached but did not survive correction (MNI: 38, 24, 34; cluster size = 243 voxels; cluster-level p_FWE = .094).

No significant clusters were found for the reverse contrast (F > R).

3.4 Representational Similarity Analysis (RSA)

To examine whether encoded items formed category-level neural representations, we performed a searchlight RSA (radius = 3 voxels) using a model based on item category labels (faces, scenes, objects). The searchlight map was thresholded at p < .001 (uncorrected) for visualization; cluster-level FWE correction at p < .05 was applied for inference.

A significant cluster for category-level representation was identified in the right fusiform gyrus (MNI: 36, -48, -22; cluster size = 186 voxels; cluster-level p_FWE = .031). No significant clusters were observed in early visual cortex or prefrontal regions.

3.5 Brain-Behavior Correlation

To link neural subsequent memory effects with behavioral performance, we correlated the hippocampal ROI subsequent memory effect (R > F parameter estimates, averaged across left and right hippocampus) with recognition accuracy (Pr = hit rate − false alarm rate). The correlation was significant, r(30) = .48, p = .005, 95% CI [0.16, 0.71], indicating that individuals with greater hippocampal subsequent memory effects also showed better recognition memory.

A follow-up exploratory analysis examined whether hippocampal activation mediated the relationship between age and memory performance. A bootstrapped mediation analysis (PROCESS, 5000 samples) revealed a significant indirect effect, ab = -0.12, 95% CI [-0.24, -0.02], suggesting that age-related differences in hippocampal activation were associated with age-related differences in recognition performance.
```

## Expected Output Structure

### Study Profile / Three-Axis Classification

```
| Axis 1 | Experiment | [原文Methods] |
| Axis 2 | Cognitive Neuroscience / fMRI | [原文推断] |
| Axis 3 | fMRI activation + RSA + brain-behavior correlation | [原文Methods] |
| Primary Branch | Branch F (Neuroimaging) | [基于三轴分类] |
```

### Key Branch F Assertions

#### Must contain

- "Branch F" or "Neuroimaging" in classification
- "ROI" and identify as "a priori defined / anatomically defined"
- "AAL atlas" noted as ROI source
- "FWE" correction method extracted for whole-brain analysis
- "cluster-defining threshold p < .001" extracted
- "cluster-level FWE p < .05" extracted
- "RSA" or "Representational Similarity Analysis" identified in Module B
- "searchlight" method noted (radius = 3 voxels)
- "MNI coordinates" preserved (-24, -14, -18 etc.)
- Brain-behavior correlation: r(30) = .48 correctly reported with df = 30 (not N = 32)
- Mediation analysis correctly identified: PROCESS with bootstrap
- "mediates/mediated/mediation" is ALLOWED in this case because formal mediation model IS reported
- G0 fields populated for neuroimaging: correction method, ROI source, cluster thresholds

#### Must NOT contain

- "closed-loop" / "TMR" / "sleep phase" terms — these are irrelevant to this fMRI paper
- "sham" mislabeled as "active control"
- "mediates" flagged as error (formal mediation IS reported — mechanism-wording guardrail applies only when NO formal mediation)
- ROI labeled as "exploratory" (they are a priori)
- Whole-brain clusters with p_FWE = .094 described as "significant"
- "N = 62" from interaction df (N = 32 from t-test df + 1)
- Conflating t(31) with r(30) degrees of freedom

#### Module B structure check

Expected order for fMRI experiment:
1. Behavioral results (3.1)
2. ROI analysis (3.2)
3. Whole-brain analysis (3.3)
4. RSA / MVPA analysis (3.4)
5. Brain-behavior correlation (3.5)

#### Module D Figure/Chart type detection

- fMRI activation maps (whole-brain) → brain map type
- RSA searchlight map → RSA matrix / searchlight map type
- Bar plot for ROI parameter estimates → bar chart type
- Scatter plot for brain-behavior correlation → scatter plot type

#### Module E boundary check

- Brain-behavior correlation r = .48 → correlation, not causal direct link
- "indicating that individuals with greater..." → this is interpretation, not raw result — flag as Results-Discussion boundary
- RSA results → representational structure, not activation strength — note distinction
- Mediation: formal bootstrap test reported → DON'T flag as "correlation treated as causation"; instead note "temporal precedence not established in cross-trial fMRI design"
- p_FWE = .094 cluster → correctly noted as "did not survive correction"

#### G0 Source Verification

- N = 32 (from t(31) df + 1)
- ROI: anatomical, AAL atlas, a priori — fully sourced
- Whole-brain: cluster-defining p < .001, FWE p < .05 — correction method sourced
- RSA: searchlight radius = 3, correction method sourced
- Mediation: PROCESS, 5000 bootstrap samples — sourced
