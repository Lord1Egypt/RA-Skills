#!/usr/bin/env python3
"""
蛋白质关键序列片段预测分析流程
适用于任何蛋白质家族

流程：
1. 读取各物种FASTA序列
2. 多序列比对（ClustalOmega）
3. 共识序列提取（保守性阈值）
4. 关键功能片段识别与注释
5. 生成分析报告
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from collections import Counter

# ── 配置 ──────────────────────────────────────────────
THRESHOLD = 0.5          # 共识序列保守性阈值
WORK_DIR = Path(__file__).parent
DATE_STR = datetime.now().strftime("%Y%m%d")

# ── 已知功能域定义 ───────────────────────────────────
# 分析新蛋白家族时，在此补充对应的Pfam保守域特征序列
# 来源：Pfam / InterPro / UniProt

KNOWN_MOTIFS = {
    # 示例：可在此添加目标蛋白家族的保守基序
    # "功能域名称": {
    #     "pattern": ["氨基酸模式"],
    #     "context_note": "功能描述",
    #     "function": "具体功能",
    #     "criticality": "重要性级别"
    # }
    "保守半胱氨酸": {
        "pattern": ["C"],
        "context_note": "保守半胱氨酸残基",
        "function": "形成二硫键，稳定蛋白三维结构",
        "criticality": "结构关键"
    }
}

# ── 保守序列标志 ─────────────────────────────────────
# 高度保守的序列块（来自Pfam注释）
# 分析新蛋白家族时，在此补充对应的保守序列
CONSERVED_BLOCKS = {
    # 示例：
    # "保守块名称": "序列模式"
}


def run_clustalo(input_fasta, output_aln):
    """运行ClustalOmega多序列比对"""
    cmd = [
        "clustalo",
        "-i", str(input_fasta),
        "-o", str(output_aln),
        "--outfmt=fasta",
        "--force",
        "-v"
    ]
    print(f"\n[MSA] 运行 ClustalOmega...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  错误：{result.stderr}")
        return False
    print(f"  完成：{output_aln}")
    return True


def parse_fasta(fasta_path):
    """解析FASTA文件，返回 {序列名: 序列} 字典"""
    sequences = {}
    current_name = None
    current_seq = []
    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_name:
                    sequences[current_name] = "".join(current_seq).upper()
                current_name = line[1:].split()[0]
                current_seq = []
            else:
                current_seq.append(line)
    if current_name:
        sequences[current_name] = "".join(current_seq).upper()
    return sequences


def extract_consensus(aligned_sequences, threshold=THRESHOLD):
    """
    从比对序列中提取共识序列
    threshold: 某位置最高频氨基酸占比 >= threshold 则写入，否则标X
    """
    if not aligned_sequences:
        return ""
    seqs = list(aligned_sequences.values())
    length = len(seqs[0])
    consensus = []
    conservation_scores = []

    for i in range(length):
        col = [s[i] for s in seqs if i < len(s)]
        # 排除gap
        non_gap = [aa for aa in col if aa != '-']
        if not non_gap:
            consensus.append('-')
            conservation_scores.append(0.0)
            continue
        counter = Counter(non_gap)
        most_common_aa, most_common_count = counter.most_common(1)[0]
        conservation = most_common_count / len(non_gap)
        conservation_scores.append(conservation)
        if conservation >= threshold:
            consensus.append(most_common_aa)
        else:
            consensus.append('X')

    return "".join(consensus), conservation_scores


def find_conserved_blocks(consensus_seq):
    """在共识序列中搜索已知保守块"""
    found = {}
    clean_consensus = consensus_seq.replace('-', '').replace('X', '?')

    for block_name, pattern in CONSERVED_BLOCKS.items():
        # 允许X位置匹配任意氨基酸
        idx = clean_consensus.find(pattern)
        if idx != -1:
            found[block_name] = {
                "position": idx,
                "matched_seq": clean_consensus[idx:idx+len(pattern)],
                "pattern": pattern
            }

    return found


def analyze_key_fragments(consensus_seq, conservation_scores, species_list):
    """
    分析共识序列中的关键片段
    返回关键片段列表，每个包含：位置、序列、功能注释
    """
    clean_consensus = "".join(aa for aa in consensus_seq if aa != '-')
    key_fragments = []

    # 1. 搜索已知保守块
    found_blocks = find_conserved_blocks(clean_consensus)
    for block_name, info in found_blocks.items():
        key_fragments.append({
            "fragment_id": block_name,
            "sequence": info["matched_seq"],
            "position_in_consensus": f"{info['position']+1}-{info['position']+len(info['matched_seq'])}",
            "matched_pattern": info["pattern"],
            "criticality": "极关键",
            "function": get_block_function(block_name),
            "evidence": "保守序列块匹配（Pfam注释）"
        })

    # 2. 搜索高保守区段：找连续保守性≥0.9的区域，合并相邻窗口，避免冗余
    non_gap_scores = []
    non_gap_consensus = []
    for aa, score in zip(consensus_seq, conservation_scores):
        if aa != '-':
            non_gap_scores.append(score)
            non_gap_consensus.append(aa)

    # 找出所有保守率≥0.9且非X的连续区段（最少6aa）
    MIN_LEN = 6
    HIGH_CONSERVATION = 0.90
    in_region = False
    region_start = 0

    for i, (aa, score) in enumerate(zip(non_gap_consensus, non_gap_scores)):
        is_conserved = (score >= HIGH_CONSERVATION and aa != 'X')
        if is_conserved and not in_region:
            in_region = True
            region_start = i
        elif (not is_conserved or i == len(non_gap_consensus) - 1) and in_region:
            region_end = i if not is_conserved else i + 1
            in_region = False
            region_len = region_end - region_start
            if region_len >= MIN_LEN:
                frag_seq = "".join(non_gap_consensus[region_start:region_end])
                avg_conservation = sum(non_gap_scores[region_start:region_end]) / region_len
                # 检查是否已被已知块覆盖
                already_found = any(
                    frag.get("matched_pattern", "") and
                    (frag["sequence"] in frag_seq or frag_seq in frag["sequence"])
                    for frag in key_fragments
                )
                if not already_found and 'X' not in frag_seq:
                    composition = analyze_fragment_composition(frag_seq)
                    key_fragments.append({
                        "fragment_id": f"高保守连续区_{region_start+1}_{region_end}",
                        "sequence": frag_seq,
                        "position_in_consensus": f"{region_start+1}-{region_end}",
                        "length": region_len,
                        "avg_conservation": f"{avg_conservation:.2%}",
                        "criticality": "高保守（功能待确认）",
                        "function": "高度保守连续区域，可能涉及结构稳定或功能活性位点",
                        "evidence": f"连续{region_len}aa保守性分析（平均{avg_conservation:.2%}）",
                        "composition": composition
                    })

    # 3. 搜索Cys残基（潜在二硫键）
    cys_positions = [i+1 for i, aa in enumerate(non_gap_consensus) if aa == 'C']
    if len(cys_positions) >= 2:
        key_fragments.append({
            "fragment_id": "保守半胱氨酸_二硫键",
            "sequence": f"C×{len(cys_positions)}（位置：{', '.join(map(str, cys_positions[:6]))}{'...' if len(cys_positions)>6 else ''}）",
            "position_in_consensus": "多位置",
            "criticality": "结构关键",
            "function": "形成二硫键，维持蛋白三维构象稳定性",
            "evidence": f"共识序列中检测到{len(cys_positions)}个保守Cys残基"
        })

    return key_fragments, clean_consensus


# ── 氨基酸分类（用于片段理化性质分析）────────────────────
# 注意：此处 A/G/P 重新归入 Hydrophobic（与氨基酸对分析的分类方案不同）
AA_CATEGORIES = {
    'Hydrophobic': set('VLIMAG P'.replace(' ', '')),  # V, L, I, M, A, G, P
    'Nucleophilic': set('STC'),
    'Aromatic':    set('FYW'),
    'Amide':       set('NQ'),
    'Acidic':      set('DE'),
    'Cationic':    set('HKR'),
}
# X 不参与统计

# 理化性质判断规则（主导类别 → 理化性质描述）
PROPERTY_DESCRIPTIONS = {
    'Hydrophobic': '疏水性（Hydrophobic）——倾向埋藏于蛋白质疏水核心，参与疏水堆积/折叠',
    'Nucleophilic': '亲核性（Nucleophilic）——富含 Ser/Thr/Cys，具有强亲核反应能力，常见于催化活性位点或翻译后修饰位点',
    'Aromatic':    '芳香性（Aromatic）——含 Phe/Tyr/Trp，可参与π-π堆叠、阳离子-π作用及疏水核心稳定',
    'Amide':       '酰胺类（Amide）——富含 Asn/Gln，侧链具有极性但不带电，常参与氢键网络及底物识别',
    'Acidic':      '酸性（Acidic）——富含 Asp/Glu，带负电，参与盐桥、金属离子结合及活性位点催化',
    'Cationic':    '阳离子性（Cationic）——富含 His/Lys/Arg，带正电，参与底物识别、催化位点及DNA/RNA结合',
    'Mixed':       '混合型（Mixed）——无单一主导类别（最高占比 < 35%），理化性质复合，可能涉及多功能结合界面',
}


def analyze_fragment_composition(fragment_seq):
    """
    对片段序列进行各类氨基酸比例分析，判断主要理化性质。

    参数：
        fragment_seq: 片段氨基酸序列（字符串，可含X）

    返回：dict，包含：
        - category_counts: {类别: 计数}
        - category_ratios: {类别: 比例（%）}
        - total_valid: 有效氨基酸总数（排除X）
        - dominant_category: 主导类别名称（或 'Mixed'）
        - dominant_ratio: 主导类别占比（%）
        - physicochemical_property: 理化性质描述
    """
    # 只统计非X氨基酸
    valid_aas = [aa for aa in fragment_seq.upper() if aa != 'X']
    total_valid = len(valid_aas)

    if total_valid == 0:
        return {
            "category_counts": {},
            "category_ratios": {},
            "total_valid": 0,
            "dominant_category": "Unknown",
            "dominant_ratio": 0.0,
            "physicochemical_property": "无有效氨基酸（全为X），无法判断"
        }

    counts = {cat: 0 for cat in AA_CATEGORIES}
    unclassified = 0
    for aa in valid_aas:
        classified = False
        for cat, members in AA_CATEGORIES.items():
            if aa in members:
                counts[cat] += 1
                classified = True
                break
        if not classified:
            unclassified += 1

    ratios = {cat: round(cnt / total_valid * 100, 1) for cat, cnt in counts.items()}

    # 找主导类别（最高占比，且 ≥ 35% 才称为主导）
    top_cat = max(counts, key=lambda c: counts[c])
    top_ratio = ratios[top_cat]
    dominant = top_cat if top_ratio >= 35.0 else 'Mixed'

    return {
        "category_counts": counts,
        "category_ratios": ratios,
        "total_valid": total_valid,
        "unclassified_count": unclassified,
        "dominant_category": dominant,
        "dominant_ratio": top_ratio,
        "physicochemical_property": PROPERTY_DESCRIPTIONS.get(dominant, "未知")
    }


def get_block_function(block_name):
    """根据保守块名称返回功能描述"""
    # 分析新蛋白家族时，在此补充对应功能描述
    functions = {
        # 示例：
        # "block_name": "功能描述"
    }
    return functions.get(block_name, "已知保守功能块")


def generate_report(species_name, sequences, consensus_seq, conservation_scores,
                    key_fragments, output_dir):
    """生成分析报告（Markdown格式）"""
    report_path = output_dir / f"{species_name}_分析报告.md"
    clean_consensus = "".join(aa for aa in consensus_seq if aa != '-')

    # 统计
    x_count = clean_consensus.count('X')
    total_len = len(clean_consensus)
    conservation_rate = (total_len - x_count) / total_len if total_len > 0 else 0

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 蛋白质关键片段预测分析报告\n\n")
        f.write(f"**物种/类群：** {species_name}  \n")
        f.write(f"**分析日期：** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**输入序列数：** {len(sequences)}  \n")
        f.write(f"**共识序列长度：** {total_len} aa  \n")
        f.write(f"**共识序列保守率：** {conservation_rate:.1%}（阈值≥{THRESHOLD}）  \n\n")

        f.write("---\n\n")
        f.write("## 1. 共识序列\n\n")
        f.write("```\n")
        # 每60个字符换行
        for i in range(0, len(clean_consensus), 60):
            f.write(f"{i+1:>4} {clean_consensus[i:i+60]}\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## 2. 关键功能片段\n\n")

        if not key_fragments:
            f.write("未检测到显著关键片段（可能需要更多序列或调整阈值）。\n\n")
        else:
            for frag in key_fragments:
                criticality_emoji = {
                    "极关键": "🔴",
                    "关键": "🟠",
                    "结构关键": "🟡",
                    "高保守（功能待确认）": "🔵"
                }.get(frag["criticality"], "⚪")

                f.write(f"### {criticality_emoji} {frag['fragment_id']}\n\n")
                f.write(f"| 属性 | 内容 |\n|------|------|\n")
                f.write(f"| **片段序列** | `{frag['sequence']}` |\n")
                f.write(f"| **位置** | {frag.get('position_in_consensus', 'N/A')} |\n")
                f.write(f"| **重要性** | {frag['criticality']} |\n")
                f.write(f"| **功能** | {frag['function']} |\n")
                f.write(f"| **证据** | {frag.get('evidence', 'N/A')} |\n")
                if 'avg_conservation' in frag:
                    f.write(f"| **平均保守率** | {frag['avg_conservation']} |\n")

                # 氨基酸组成与理化性质（仅高保守连续区片段有此字段）
                comp = frag.get('composition')
                if comp and comp.get('total_valid', 0) > 0:
                    ratios = comp['category_ratios']
                    # 按比例从高到低排列
                    sorted_cats = sorted(ratios.items(), key=lambda x: -x[1])
                    ratio_str = " | ".join(
                        f"{cat}: {pct}%" for cat, pct in sorted_cats if pct > 0
                    )
                    f.write(f"| **氨基酸组成** | {ratio_str} |\n")
                    f.write(f"| **主导类别** | {comp['dominant_category']}（{comp['dominant_ratio']}%） |\n")
                    f.write(f"| **主要理化性质** | {comp['physicochemical_property']} |\n")

                f.write("\n")

        f.write("---\n\n")
        f.write("## 3. 输入序列列表\n\n")
        for name, seq in sequences.items():
            f.write(f"- **{name}**（{len(seq)} aa）\n")

        f.write("\n---\n\n")
        f.write("## 4. 分析方法说明\n\n")
        f.write("1. **MSA**：使用 ClustalOmega 1.2.4 进行多序列比对\n")
        f.write(f"2. **共识序列**：各位置最高频氨基酸占比 ≥ {THRESHOLD} 则写入，否则标X\n")
        f.write("3. **关键片段识别**：\n")
        f.write("   - 匹配已知保守块（Pfam注释特征序列）\n")
        f.write("   - 连续保守区检测（保守率 ≥ 90%，长度 ≥ 6aa）\n")
        f.write("   - 检测保守Cys残基（潜在二硫键）\n")
        f.write("4. **片段氨基酸组成分析（新）**：对每个高保守连续区段统计各功能类别氨基酸比例\n")
        f.write("   - 分类方案（含A/G/P归入疏水类）：\n")
        f.write("     Hydrophobic(V/L/I/M/A/G/P) | Nucleophilic(S/T/C) | Aromatic(F/Y/W)\n")
        f.write("     Amide(N/Q) | Acidic(D/E) | Cationic(H/K/R)；X不参与统计\n")
        f.write("   - 主导类别判定：最高占比 ≥ 35% 则为该类别主导，否则为 Mixed\n")
        f.write("5. **功能注释**：基于Pfam/InterPro已知蛋白结构-功能数据库\n\n")
        f.write("---\n\n")
        f.write("*本报告由自动化分析pipeline生成，关键片段功能解读基于已知蛋白家族注释。*\n")

    return report_path


def analyze_species(species_name, fasta_path, output_dir, precomputed_aligned=None):
    """对单个物种/类群执行完整分析流程
    
    Args:
        species_name: 物种名称
        fasta_path: 原始FASTA文件路径
        output_dir: 输出目录
        precomputed_aligned: 预计算的比对FASTA路径（共享缓存，跳过MSA步骤）
    """
    print(f"\n{'='*60}")
    print(f"分析：{species_name}")
    print(f"{'='*60}")

    species_dir = Path(output_dir) / species_name
    species_dir.mkdir(exist_ok=True)

    # Step 1: 解析输入序列
    sequences = parse_fasta(fasta_path)
    print(f"[Step1] 读取序列：{len(sequences)} 条")
    for name, seq in sequences.items():
        print(f"  - {name}（{len(seq)} aa）")

    if len(sequences) < 2:
        print("  ⚠️  序列数不足2条，跳过MSA，直接使用单条序列作为共识序列")
        consensus_seq = list(sequences.values())[0]
        conservation_scores = [1.0] * len(consensus_seq)
    else:
        # Step 2: MSA（若提供预计算比对则跳过）
        aln_path = species_dir / f"{species_name}_aligned.fasta"
        if precomputed_aligned and Path(precomputed_aligned).exists():
            import shutil
            shutil.copy2(precomputed_aligned, aln_path)
            print(f"[Step2] 使用共享比对缓存：{precomputed_aligned}")
        else:
            success = run_clustalo(fasta_path, aln_path)
            if not success:
                print("  MSA失败，终止")
                return None

        # Step 3: 提取共识序列
        aligned_seqs = parse_fasta(aln_path)
        consensus_seq, conservation_scores = extract_consensus(aligned_seqs, THRESHOLD)
        print(f"[Step3] 共识序列提取完成（长度：{len([aa for aa in consensus_seq if aa!='-'])} aa）")

    # 保存共识序列
    consensus_path = species_dir / f"{species_name}_consensus.fasta"
    clean_consensus = "".join(aa for aa in consensus_seq if aa != '-')
    with open(consensus_path, 'w') as f:
        f.write(f">{species_name}_consensus\n")
        for i in range(0, len(clean_consensus), 60):
            f.write(clean_consensus[i:i+60] + "\n")
    print(f"[Step3] 共识序列已保存：{consensus_path}")

    # Step 4: 关键片段分析
    print(f"[Step4] 分析关键功能片段...")
    key_fragments, clean_consensus = analyze_key_fragments(
        consensus_seq, conservation_scores, list(sequences.keys())
    )
    print(f"  检测到 {len(key_fragments)} 个关键片段/区域")

    # 保存片段数据（JSON）
    fragments_path = species_dir / f"{species_name}_key_fragments.json"
    with open(fragments_path, 'w', encoding='utf-8') as f:
        json.dump({
            "species": species_name,
            "date": DATE_STR,
            "consensus_length": len(clean_consensus),
            "key_fragments": key_fragments
        }, f, ensure_ascii=False, indent=2)

    # Step 5: 生成报告
    report_path = generate_report(
        species_name, sequences, consensus_seq,
        conservation_scores, key_fragments, species_dir
    )
    print(f"[Step5] 报告已生成：{report_path}")

    return {
        "species": species_name,
        "n_sequences": len(sequences),
        "consensus_length": len(clean_consensus),
        "key_fragments_count": len(key_fragments),
        "report_path": str(report_path)
    }


def generate_summary_report(all_results, output_dir):
    """生成跨物种汇总报告"""
    summary_path = output_dir / "汇总分析报告.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# 蛋白质关键片段预测 — 跨物种汇总报告\n\n")
        f.write(f"**分析日期：** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**分析物种数：** {len(all_results)}  \n\n")
        f.write("---\n\n")
        f.write("## 各物种分析摘要\n\n")
        f.write("| 物种/类群 | 输入序列数 | 共识序列长度 | 检出关键片段数 |\n")
        f.write("|---------|----------|------------|-------------|\n")
        for r in all_results:
            f.write(f"| {r['species']} | {r['n_sequences']} | {r['consensus_length']} aa | {r['key_fragments_count']} |\n")
        f.write("\n---\n\n")
        f.write("## 关键说明\n\n")
        f.write("- 各物种详细报告见对应子目录\n")
        f.write("- 关键片段重要性分级：🔴极关键 > 🟠关键 > 🟡结构关键 > 🔵高保守待确认\n")
        f.write("- 功能注释基于Pfam/InterPro蛋白家族数据库\n")
    print(f"\n[汇总] 跨物种汇总报告：{summary_path}")
    return summary_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="蛋白质关键片段预测分析流程")
    parser.add_argument("species_name", nargs="?", help="物种名称")
    parser.add_argument("fasta_file", nargs="?", help="FASTA文件路径")
    parser.add_argument("--precomputed-aligned", default=None,
                        help="预计算的比对FASTA路径（共享缓存，跳过MSA步骤）")
    parser.add_argument("--output-dir", default=None, help="输出目录（默认：脚本目录/results）")
    args = parser.parse_args()

    print("蛋白质关键片段预测分析流程")
    print(f"工作目录：{WORK_DIR}")

    if args.species_name and args.fasta_file:
        fasta = Path(args.fasta_file)
        out_dir = Path(args.output_dir) if args.output_dir else WORK_DIR / "results"
        out_dir.mkdir(exist_ok=True)
        result = analyze_species(args.species_name, fasta, out_dir,
                                 precomputed_aligned=args.precomputed_aligned)
        if result:
            generate_summary_report([result], out_dir.parent if args.output_dir else WORK_DIR)
    else:
        print("\n请将各物种FASTA文件放入 input/ 目录，然后重新运行。")
        print("或通过命令行参数指定：python serine_protease_analysis.py <species_name> <fasta_file>")
        print("  可选：--precomputed-aligned <aligned.fasta>  使用共享MSA缓存跳过比对步骤")
