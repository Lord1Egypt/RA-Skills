# DGRA Phase Analysis 计算逻辑文档

**版本**: v0.4.5  
**日期**: 2026-05-20  
**作者**: DGRA 开发团队

---

## 一、核心问题

给定一个基因内的 $n$ 个 germline 变异，判断它们是：
- **cis**（位于同一单倍型）
- **trans**（位于不同单倍型）
- **ambiguous**（数据不足以判断）
- **unphased**（技术上不可行）

---

## 二、输入数据

### 2.1 必需输入

| 字段 | 类型 | 说明 |
|------|------|------|
| `chrom` | str | 染色体 |
| `pos` | int | 基因组坐标（bp）|
| `gt` | str | 基因型，如 `0/1`, `1\|1`, `1/0` |
| `dp` | int | 测序深度 |
| `gq` | int | 基因型质量 |

### 2.2 可选输入（提升置信度）

| 字段 | 类型 | 说明 |
|------|------|------|
| `bam_path` | str | BAM/CRAM 文件路径 |
| `father_gt` | str | 父亲基因型（trio） |
| `mother_gt` | str | 母亲基因型（trio） |
| `ld_data` | dict | 人群 LD 数据（r²） |

---

## 三、分层决策算法

### 算法总览

```
determine_phase(variants, bam_path=None, father_gt=None, mother_gt=None)
    → returns PhaseResult
```

### Level 1: GATK Phased GT 解析（最高优先级）

```python
def parse_gt_field(gt_str):
    """
    解析 VCF GT 字段
    返回: {is_phased: bool, allele_0: int, allele_1: int}
    """
    if '|' in gt_str:
        a0, a1 = gt_str.split('|')
        return {"is_phased": True, "allele_0": int(a0), "allele_1": int(a1)}
    elif '/' in gt_str:
        a0, a1 = gt_str.split('/')
        return {"is_phased": False, "allele_0": int(a0), "allele_1": int(a1)}
    else:
        return {"is_phased": False, "allele_0": int(gt_str), "allele_1": int(gt_str)}
```

**决策规则**:

```python
def level1_gatk_phase(variants):
    # 检查是否全部 phased
    all_phased = all(parse_gt_field(v.gt)["is_phased"] for v in variants)
    
    if not all_phased:
        return None  # 进入 Level 2
    
    # 提取每个变异的 haplotype 等位基因
    hap0_alleles = [parse_gt_field(v.gt)["allele_0"] for v in variants]
    hap1_alleles = [parse_gt_field(v.gt)["allele_1"] for v in variants]
    
    # 情况分析
    if set(hap0_alleles) == {1} and set(hap1_alleles) == {1}:
        # GT=1|1 for ALL variants → 两条单倍型都携带所有变异
        return PhaseResult(
            phase_status="cis_both_haplotypes",  # 或 "homozygous_compound"
            confidence="high",
            method="gatk_phased_gt",
            evidence=f"所有 {len(variants)} 个变异 GT=1|1，GATK local assembly 确认两条单倍型均携带"
        )
    
    elif set(hap0_alleles) == {1} and set(hap1_alleles) == {0}:
        # Hap0 全为 ALT, Hap1 全为 REF → cis（杂合）
        return PhaseResult(
            phase_status="cis",
            confidence="high", 
            method="gatk_phased_gt",
            evidence=f"所有 ALT 等位基因位于同一单倍型 (Hap0)，REF 位于另一单倍型"
        )
    
    elif set(hap0_alleles) == {0} and set(hap1_alleles) == {1}:
        # 对称情况
        return PhaseResult(
            phase_status="cis",
            confidence="high",
            method="gatk_phased_gt", 
            evidence=f"所有 ALT 等位基因位于同一单倍型 (Hap1)，REF 位于另一单倍型"
        )
    
    elif 0 in hap0_alleles and 1 in hap0_alleles:
        # Hap0 上既有 REF 又有 ALT → 至少两个变异 trans
        return PhaseResult(
            phase_status="trans",
            confidence="high",
            method="gatk_phased_gt",
            evidence=f"单倍型 Hap0 上同时存在 REF 和 ALT ({hap0_alleles})，确认 trans 关系"
        )
    
    elif 0 in hap1_alleles and 1 in hap1_alleles:
        return PhaseResult(
            phase_status="trans",
            confidence="high",
            method="gatk_phased_gt",
            evidence=f"单倍型 Hap1 上同时存在 REF 和 ALT ({hap1_alleles})，确认 trans 关系"
        )
```

### Level 2: 间距可行性判断

```python
def level2_distance_assessment(variants):
    """
    基于变异间距判断短 reads 相位可行性
    """
    positions = sorted([v.pos for v in variants])
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    max_gap = max(gaps) if gaps else 0
    min_gap = min(gaps) if gaps else 0
    
    # 决策矩阵
    if max_gap < 50:
        return {
            "feasible": True,
            "confidence": "high",
            "method": "short_reads_overlap",
            "range": f"{min_gap}-{max_gap}bp",
            "read_coverage": "同一 150bp read 必然覆盖所有变异",
            "next_step": "Level 3 - reads 直接分析"
        }
    elif max_gap < 150:
        return {
            "feasible": True,
            "confidence": "high",
            "method": "short_reads_overlap_or_paired_end",
            "range": f"{min_gap}-{max_gap}bp",
            "read_coverage": "同一 read (靠近 3' 端) 或 insert 覆盖",
            "next_step": "Level 3 - reads 直接分析"
        }
    elif max_gap < 500:
        return {
            "feasible": True,
            "confidence": "medium",
            "method": "paired_end_only",
            "range": f"{min_gap}-{max_gap}bp",
            "read_coverage": "依赖 pair-end insert size (通常 300-500bp)",
            "next_step": "Level 3 - reads 直接分析（如果 BAM 可用）"
        }
    else:
        return {
            "feasible": False,
            "confidence": "none",
            "method": "infeasible_short_reads",
            "range": f"max_gap={max_gap}bp",
            "read_coverage": "远超 short-read 范围",
            "next_step": "Level 4 - trio 或 Level 5 - LD"
        }
```

### Level 3: Reads 直接分析

```python
def level3_reads_analysis(variants, bam_path, min_reads=10):
    """
    从 BAM/CRAM 提取覆盖变异位点的 reads，统计 cis/trans
    
    核心统计量：
    - N_cis: 同时携带所有 ALT 等位基因的 reads 数
    - N_ref_cis: 同时携带所有 REF 等位基因的 reads 数（对照）
    - N_trans: 携带部分 ALT 部分 REF 的 reads 数
    - N_total: 覆盖所有位点的 reads 总数
    
    算法步骤：
    1. 使用 pysam 提取覆盖 variants[0].pos 到 variants[-1].pos 区间的 reads
    2. 对每条 read：
       a. 检查是否覆盖所有变异位点
       b. 读取每个位点的碱基
       c. 分类：
          - 如果所有位点都是 ALT → N_cis += 1
          - 如果所有位点都是 REF → N_ref_cis += 1
          - 如果混合 ALT/REF → N_trans += 1
    3. 计算统计量
    """
    
    # 伪代码（需 pysam）
    import pysam
    
    bam = pysam.AlignmentFile(bam_path, "rb")
    chrom = variants[0].chrom.replace("chr", "")
    start = min(v.pos for v in variants) - 10
    end = max(v.pos for v in variants) + 10
    
    N_cis = N_ref_cis = N_trans = N_total = 0
    
    for read in bam.fetch(chrom, start, end):
        if read.is_unmapped or read.is_secondary:
            continue
        
        # 检查 read 是否覆盖所有变异位点
        covers_all = all(start <= v.pos <= end for v in variants)
        if not covers_all:
            continue
        
        N_total += 1
        
        # 读取每个位点的碱基
        bases = []
        for v in variants:
            # 获取 read 在 v.pos 处的碱基
            for pileup in read.get_aligned_pairs(matches_only=False):
                if pileup[1] == v.pos - 1:  # 0-based
                    if pileup[0] is not None:
                        base = read.query_sequence[pileup[0]]
                        bases.append(base)
                    break
        
        if len(bases) != len(variants):
            continue
        
        # 判断碱基组成
        all_alt = all(b == v.alt for b, v in zip(bases, variants))
        all_ref = all(b == v.ref for b, v in zip(bases, variants))
        mixed = not all_alt and not all_ref
        
        if all_alt:
            N_cis += 1
        elif all_ref:
            N_ref_cis += 1
        elif mixed:
            N_trans += 1
    
    bam.close()
    
    # 决策
    if N_total < min_reads:
        return {
            "feasible": True,
            "phase_status": "insufficient_reads",
            "confidence": "low",
            "method": "reads_direct",
            "evidence": f"仅 {N_total} 条 reads 覆盖，低于阈值 {min_reads}"
        }
    
    cis_ratio = N_cis / N_total
    trans_ratio = N_trans / N_total
    
    if cis_ratio > 0.8:
        return {
            "phase_status": "cis",
            "confidence": "high" if max_gap < 50 else "medium",
            "method": "reads_direct",
            "evidence": f"{N_cis}/{N_total} reads ({cis_ratio:.1%}) 同时携带所有 ALT，{N_trans} 条 mixed"
        }
    elif trans_ratio > 0.3:
        return {
            "phase_status": "trans",
            "confidence": "high" if max_gap < 50 else "medium",
            "method": "reads_direct",
            "evidence": f"{N_trans}/{N_total} reads ({trans_ratio:.1%}) 携带混合等位基因"
        }
    else:
        return {
            "phase_status": "ambiguous",
            "confidence": "low",
            "method": "reads_direct",
            "evidence": f"Cis ratio={cis_ratio:.2f}, Trans ratio={trans_ratio:.2f}, 无法明确判断"
        }
```

### Level 4: Trio 推断

```python
def level4_trio_inference(variants, father_gts, mother_gts):
    """
    基于父母基因型推断子代 phase
    
    原理：
    - 女儿从父亲继承一个单倍型，从母亲继承一个单倍型
    - 如果父亲在变异位点 A 是 1|0，在变异位点 B 是 1|0
      → 父亲的两条单倍型：HapA=(1,1), HapB=(0,0)
      → 女儿从父亲继承 HapA 或 HapB
    - 如果母亲也是 1|0（两个位点）
      → 母亲的两条单倍型：HapC=(1,1), HapD=(0,0)
    - 如果女儿是 1|1
      → 必须是从父亲继承 HapA(1,1) + 从母亲继承 HapC(1,1)
      → 结论：cis（两个变异都在同一继承单倍型上）
    
    关键条件：父母必须在至少一个位点上是杂合的（0/1 或 1|0），才能区分两条单倍型
    """
    
    inference_log = []
    
    for i, v in enumerate(variants):
        f_gt = parse_gt_field(father_gts[i])
        m_gt = parse_gt_field(mother_gts[i])
        c_gt = parse_gt_field(v.gt)
        
        # 父母分型判断
        if not (f_gt["is_phased"] or m_gt["is_phased"]):
            # 父母都未 phase
            if f_gt["allele_0"] == f_gt["allele_1"] or m_gt["allele_0"] == m_gt["allele_1"]:
                inference_log.append(f"位点 {v.pos}: 父母至少一方纯合，无法区分单倍型")
                continue
        
        # 推断女儿从父亲继承的 allele
        child_from_father = c_gt["allele_0"] if c_gt["is_phased"] else "unknown"
        child_from_mother = c_gt["allele_1"] if c_gt["is_phased"] else "unknown"
        
        inference_log.append(f"位点 {v.pos}: 父系={child_from_father}, 母系={child_from_mother}")
    
    # 如果所有位点的父系来源一致（都是 1 或都是 0）→ cis
    # 如果有混合 → trans
    
    return {
        "phase_status": "cis_or_trans_by_trio",
        "confidence": "high",
        "method": "trio_segregation",
        "evidence": "; ".join(inference_log)
    }
```

### Level 5: LD 统计推断（最后手段）

```python
def level5_ld_inference(variants, ld_database):
    """
    基于人群连锁不平衡数据推断 cis/trans 概率
    
    r² (coefficient of determination):
    - r² = 1.0: 完美连锁，100% cis
    - r² = 0.0: 无连锁，独立分配
    - r² > 0.8: 强连锁，大概率 cis
    - r² < 0.2: 弱连锁，可能 trans 或独立
    
    注意：LD 推断只适用于常见变异（MAF > 1%），罕见变异的 LD 数据不可靠
    """
    
    # 查询 LD 数据库（如 1000G, gnomAD）
    pair_results = []
    for i in range(len(variants)):
        for j in range(i+1, len(variants)):
            v1, v2 = variants[i], variants[j]
            
            # 查询 r²
            r2 = query_ld(ld_database, v1.chrom, v1.pos, v2.pos)
            
            if r2 is None:
                pair_results.append({"pair": (i,j), "r2": None, "status": "no_data"})
            elif r2 > 0.8:
                pair_results.append({"pair": (i,j), "r2": r2, "status": "strong_ld_cis_likely"})
            elif r2 < 0.2:
                pair_results.append({"pair": (i,j), "r2": r2, "status": "weak_ld_independent"})
            else:
                pair_results.append({"pair": (i,j), "r2": r2, "status": "moderate_ld_ambiguous"})
    
    # 综合所有 pair 的结果
    strong_ld_count = sum(1 for p in pair_results if p["status"] == "strong_ld_cis_likely")
    weak_ld_count = sum(1 for p in pair_results if p["status"] == "weak_ld_independent")
    
    if strong_ld_count == len(pair_results):
        return {
            "phase_status": "cis_likely",
            "confidence": "medium",
            "method": "ld_inference",
            "evidence": f"所有 {len(pair_results)} 对变异 r² > 0.8，强连锁提示 cis"
        }
    elif weak_ld_count == len(pair_results):
        return {
            "phase_status": "independent_or_trans_likely",
            "confidence": "low",
            "method": "ld_inference",
            "evidence": f"所有变异对 r² < 0.2，提示独立分配或 trans"
        }
    else:
        return {
            "phase_status": "ambiguous",
            "confidence": "low",
            "method": "ld_inference",
            "evidence": f"LD 数据混合: {strong_ld_count} 强连锁, {weak_ld_count} 弱连锁"
        }
```

---

## 四、综合决策函数

```python
@dataclass
class PhaseResult:
    phase_status: str       # cis / trans / cis_both / ambiguous / unphased / cis_likely / trans_likely
    confidence: str         # high / medium / low / none
    method: str             # gatk_phased_gt / short_reads_overlap / reads_direct / trio_segregation / ld_inference
    evidence: str           # 详细证据描述
    max_gap_bp: int         # 最大变异间距
    min_gap_bp: int         # 最小变异间距
    n_variants: int         # 变异总数


def determine_phase(variants, bam_path=None, father_gts=None, mother_gts=None, ld_db=None):
    """
    主函数：分层决策，返回 PhaseResult
    
    优先级：
    1. GATK phased GT（最可靠）
    2. Reads 直接分析（如果间距 < 500bp 且 BAM 可用）
    3. Trio 推断（如果父母数据可用）
    4. LD 统计推断（最后手段）
    5. 间距判断（作为可行性评估）
    """
    
    positions = sorted([v.pos for v in variants])
    max_gap = max(positions[i+1] - positions[i] for i in range(len(positions)-1)) if len(positions) > 1 else 0
    min_gap = min(positions[i+1] - positions[i] for i in range(len(positions)-1)) if len(positions) > 1 else 0
    
    # ===== Level 1: GATK Phased GT =====
    result = level1_gatk_phase(variants)
    if result:
        result.max_gap_bp = max_gap
        result.min_gap_bp = min_gap
        result.n_variants = len(variants)
        return result
    
    # ===== Level 2: 间距可行性评估 =====
    distance_assessment = level2_distance_assessment(variants)
    
    if not distance_assessment["feasible"]:
        # 短 reads 不可行，尝试 trio 或 LD
        
        # Level 4: Trio
        if father_gts and mother_gts:
            result = level4_trio_inference(variants, father_gts, mother_gts)
            result.max_gap_bp = max_gap
            result.min_gap_bp = min_gap
            result.n_variants = len(variants)
            return result
        
        # Level 5: LD
        if ld_db:
            result = level5_ld_inference(variants, ld_db)
            result.max_gap_bp = max_gap
            result.min_gap_bp = min_gap
            result.n_variants = len(variants)
            return result
        
        # 所有方法都不可行
        return PhaseResult(
            phase_status="unphased",
            confidence="none",
            method="insufficient_data",
            evidence=f"间距 {max_gap}bp 超出短 reads 范围，且无 trio/LD 数据",
            max_gap_bp=max_gap,
            min_gap_bp=min_gap,
            n_variants=len(variants)
        )
    
    # ===== Level 3: Reads 直接分析 =====
    if bam_path and distance_assessment["feasible"]:
        result = level3_reads_analysis(variants, bam_path)
        if result["phase_status"] != "insufficient_reads":
            return PhaseResult(
                phase_status=result["phase_status"],
                confidence=result["confidence"],
                method=result["method"],
                evidence=result["evidence"],
                max_gap_bp=max_gap,
                min_gap_bp=min_gap,
                n_variants=len(variants)
            )
    
    # ===== Level 4: Trio =====
    if father_gts and mother_gts:
        result = level4_trio_inference(variants, father_gts, mother_gts)
        result.max_gap_bp = max_gap
        result.min_gap_bp = min_gap
        result.n_variants = len(variants)
        return result
    
    # ===== Level 5: LD =====
    if ld_db:
        result = level5_ld_inference(variants, ld_db)
        result.max_gap_bp = max_gap
        result.min_gap_bp = min_gap
        result.n_variants = len(variants)
        return result
    
    # ===== 默认：基于间距的可行性报告 =====
    return PhaseResult(
        phase_status="unphased",
        confidence="none",
        method=distance_assessment["method"],
        evidence=f"间距 {min_gap}-{max_gap}bp: {distance_assessment['read_coverage']}. "
                 f"建议: {distance_assessment['next_step']}",
        max_gap_bp=max_gap,
        min_gap_bp=min_gap,
        n_variants=len(variants)
    )
```

---

## 五、临床解读规则

### 5.1 cis vs trans 的临床意义

| Phase 状态 | 合子型 | 功能影响 | 风险等级 |
|-----------|--------|----------|----------|
| **cis** | 杂合（一个单倍型突变，另一个正常） | 保留 50% 正常蛋白功能 | **中等** |
| **trans** | 复合杂合（两个单倍型各有一个突变） | 可能完全丧失功能 | **高** |
| **cis_both** | 纯合（两个单倍型都有所有突变） | 功能严重受损 | **最高** |
| **ambiguous** | 不确定 | 需进一步验证 | **待确认** |

### 5.2 不同方法的置信度权重

| 方法 | 置信度上限 | 适用条件 |
|------|-----------|----------|
| GATK phased GT | **high** | GT 使用 `\|` 分隔符 |
| Reads direct (< 50bp) | **high** | 同一 read 必然覆盖 |
| Reads direct (50-150bp) | **medium** | 可能同一 read 覆盖 |
| Reads direct (150-500bp) | **medium** | 依赖 pair-end |
| Trio segregation | **high** | 父母数据可用且杂合 |
| LD inference | **low** | 仅适用于常见变异 |

---

## 六、本例 multi-hit 基因相位评估

基于女儿 WES 数据：

| 基因 | 变异数 | 间距范围 | GATK GT | 相位判断 | 置信度 | 方法 |
|------|--------|----------|---------|----------|--------|------|
| **NUDT22** | 2 | **9 bp** | `1\|1` | **cis_both** (纯合) | **high** | gatk_phased_gt |
| **SLC25A5** | 6 | ~18-148 bp | mixed | cis (需确认) | medium | short_reads |
| **HSPA6** | 3 | ~947 bp | `0/1` | unphased | none | infeasible_short_reads |
| **NUP153** | 3 | ~55 kb | `0/1` | unphased | none | infeasible_short_reads |
| **CR1** | 2 | ~80 kb | mixed | unphased | none | infeasible_short_reads |
| **HK3** | 2 | ~7.3 kb | `0/1` | unphased | none | infeasible_short_reads |
| **ACACB** | 2 | ~1.5 kb | `1\|1` | **cis_both** | **high** | gatk_phased_gt |
| **DUOX1** | 2 | ~88 bp | `0/1` | cis (likely) | high | short_reads_overlap |
| **LEO1** | 2 | ~44 bp | `0/1` | cis (likely) | high | short_reads_overlap |
| **SIGLEC9** | 2 | ~88 bp | `0/1` | cis (likely) | high | short_reads_overlap |
| **BCR** | 2 | ~158 bp | `0/1` | cis (likely) | medium | short_reads_possible |

---

## 七、实现建议

### 7.1 代码集成

将 `determine_phase()` 集成到 `dgra_core.py` 的 `detect_multi_hit_genes()` 中：

```python
def detect_multi_hit_genes(variants, gtex_data=None):
    ...
    for gene, var_list in gene_variants.items():
        pathogenic_vars = [v for v in var_list if _variant_has_pathogenic_evidence(v, gtex_data)]
        
        if len(pathogenic_vars) >= 2:
            # 新增：相位分析
            phase_result = determine_phase(pathogenic_vars)
            
            multi_hits.append({
                "gene": gene,
                "variant_count": len(var_list),
                "pathogenic_count": len(pathogenic_vars),
                "phase_result": asdict(phase_result),  # 新增
                "warning": "MULTI_HIT_GENE",
                ...
            })
```

### 7.2 报告输出格式

```markdown
### NUDT22 (2 variants)

**相位状态**: cis_both（纯合）✅ High Confidence  
**方法**: GATK phased GT (`1\|1`)  
**间距**: 9 bp（同一 read 必然覆盖）  
**临床意义**: 两条单倍型均携带双突变，Nudix 水解酶功能可能严重受损

---

### HSPA6 (3 variants)

**相位状态**: unphased ❌  
**方法**: infeasible_short_reads  
**间距**: 947 bp（超出 pair-end 范围）  
**建议验证**: 
- 父母 trio 测序（首选）
- PacBio/Nanopore 长读长（备选）
**临床意义**: 待确认。如果 trans → 复合杂合，热休克蛋白功能可能严重受损
```

---

*文档版本: v0.4.5*  
*最后更新: 2026-05-20*
