#!/usr/bin/env python3
import sys
import random
import subprocess
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from protein_key_fragment_analysis import (
    parse_fasta, extract_consensus, find_conserved_blocks,
    analyze_key_fragments, generate_report, generate_summary_report,
    run_clustalo, THRESHOLD
)

WORK_DIR = Path(__file__).parent
INPUT_DIR = WORK_DIR / 'input_clean'
OUTPUT_DIR = WORK_DIR / 'results'

# 小物种处理（≤80条，快速完成）
SMALL_SPECIES = [
    '02_Acinonyx_jubatus_猎豹',
    '03_Antechinus_flavipes_黄足代鼩', 
    '04_Bos_taurus_家牛',
    '05_Canis_lupus_dingo_澳洲野犬',
    '07_Cercocebus_atys_灰白眉猴',
    '08_Equus_asinus_驴',
    '09_Equus_caballus_家马',
    '10_Equus_przewalskii_普氏野马',
    '11_Leopardus_geoffroyi_乔氏猫',
    '14_Neofelis_nebulosa_云豹',
    '15_Panthera_pardus_豹',
    '16_Papio_anubis_东非狒狒',
    '17_Prionailurus_viverrinus_渔猫',
    '19_Rhinopithecus_roxellana_川金丝猴',
    '20_Sus_scrofa_野猪'
]

# 中等物种（50-120条，合理耗时）
MEDIUM_SPECIES = [
    '06_Canis_lupus_familiaris_家犬',
    '12_Macaca_nemestrina_豚尾猴',
    '13_Mus_musculus_小鼠',
    '18_Rattus_norvegicus_大鼠'
]

# 大物种（智人，需要特殊处理）
LARGE_SPECIES = ['01_Homo_sapiens_智人']

def analyze_species_smart(species_name, fasta_path, output_dir, description=""):
    """智能分析物种，提供进度信息"""
    print(f"\n{'='*60}", flush=True)
    print(f"分析：{species_name} {description}", flush=True)
    print(f"{'='*60}", flush=True)

    fasta_path = Path(fasta_path)
    output_dir = Path(output_dir)
    species_dir = output_dir / species_name
    species_dir.mkdir(exist_ok=True)

    sequences = parse_fasta(fasta_path)
    total_seq = len(sequences)
    print(f"[Step1] 读取序列：{total_seq} 条", flush=True)

    for i, (name, seq) in enumerate(sequences.items(), 1):
        print(f"    {i:2d}/{total_seq} {name} ({len(seq)} aa)")
        if i > 5:
            break

    if len(sequences) < 2:
        print("  序列不足2条，直接使用单序列", flush=True)
        consensus_seq = list(sequences.values())[0]
        conservation_scores = [1.0] * len(consensus_seq)
    else:
        tmp_fasta = species_dir / f"{species_name}_input.fasta"
        with open(tmp_fasta, 'w') as f:
            for name, seq in sequences.items():
                f.write(f">{name}\n")
                for i in range(0, len(seq), 60):
                    f.write(seq[i:i+60] + "\n")

        aln_path = species_dir / f"{species_name}_aligned.fasta"
        print(f"[Step2] 运行ClustalOmega MSA...", flush=True)
        success = run_clustalo(tmp_fasta, aln_path)
        if not success:
            print("  MSA失败，跳过", flush=True)
            return None

        aligned_seqs = parse_fasta(aln_path)
        result = extract_consensus(aligned_seqs, THRESHOLD)
        if isinstance(result, tuple):
            consensus_seq, conservation_scores = result
        else:
            consensus_seq = result
            conservation_scores = [1.0] * len(consensus_seq)

    clean_len = len([aa for aa in consensus_seq if aa != '-'])
    print(f"[Step3] 共识序列：{clean_len} aa", flush=True)

    clean_consensus = "".join(aa for aa in consensus_seq if aa != '-')
    with open(species_dir / f"{species_name}_consensus.fasta", 'w') as f:
        f.write(f">{species_name}_consensus\n")
        for i in range(0, len(clean_consensus), 60):
            f.write(clean_consensus[i:i+60] + "\n")

    print("[Step4] 分析关键功能片段...", flush=True)
    key_fragments, _ = analyze_key_fragments(
        consensus_seq, conservation_scores, list(sequences.keys())
    )
    print(f"  检测到 {len(key_fragments)} 个关键片段", flush=True)

    fragments_path = species_dir / f"{species_name}_key_fragments.json"
    with open(fragments_path, 'w', encoding='utf-8') as f:
        json.dump({
            "species": species_name,
            "date": datetime.now().strftime("%Y%m%d"),
            "total_sequences": total_seq,
            "consensus_length": len(clean_consensus),
            "key_fragments": key_fragments
        }, f, ensure_ascii=False, indent=2)

    report_path = generate_report(
        species_name, sequences, consensus_seq,
        conservation_scores, key_fragments, species_dir
    )
    print(f"[Step5] 报告已生成：{report_path.name}", flush=True)

    return {
        "species": species_name,
        "n_sequences": total_seq,
        "consensus_length": len(clean_consensus),
        "key_fragments_count": len(key_fragments),
        "report_path": str(report_path)
    }

if __name__ == "__main__":
    random.seed(42)
    all_results = []
    completed = 0
    total = 0
    
    # 处理小物种组
    print(f"\n{'*'*60}")
    print("处理小型物种组（≤80条序列）")
    print(f"{'*'*60}")
    
    for species_name in SMALL_SPECIES:
        total += 1
        if (OUTPUT_DIR / species_name / f"{species_name}_分析报告.md").exists():
            print(f"[跳过-已完成] {species_name}")
            all_results.append({
                "species": species_name,
                "n_sequences": "已完成",
                "consensus_length": "已完成",
                "key_fragments_count": "已完成"
            })
            completed += 1
            continue
            
        result = analyze_species_smart(species_name, 
                                    INPUT_DIR / f"{species_name}.fasta",
                                    OUTPUT_DIR, 
                                    f"(快速批次)")
        if result:
            all_results.append(result)
            completed += 1
        else:
            print(f"❌ {species_name} 分析失败")

    # 处理中等物种组
    print(f"\n{'*'*60}")
    print("处理中型物种组（50-120条序列）")
    print(f"{'*'*60}")
    
    for species_name in MEDIUM_SPECIES:
        total += 1
        if (OUTPUT_DIR / species_name / f"{species_name}_分析报告.md").exists():
            print(f"[跳过-已完成] {species_name}")
            all_results.append({
                "species": species_name,
                "n_sequences": "已完成", 
                "consensus_length": "已完成",
                "key_fragments_count": "已完成"
            })
            completed += 1
            continue
            
        result = analyze_species_smart(species_name,
                                    INPUT_DIR / f"{species_name}.fasta", 
                                    OUTPUT_DIR,
                                    f"(常规批次)")
        if result:
            all_results.append(result)
            completed += 1
        else:
            print(f"❌ {species_name} 分析失败")

    # 处理大物种（智人）
    print(f"\n{'*'*60}")
    print("处理大型物种：智人（466条，采样150条）")
    print(f"{'*'*60}")
    
    species_name = LARGE_SPECIES[0]
    total += 1
    
    # 智人特殊处理：先采样，再分析
    sequences = parse_fasta(INPUT_DIR / f"{species_name}.fasta")
    sampled_seqs = dict(list(sequences.items())[:150])  # 简单取前150条
    print(f"采样150条序列进行分析...")
    
    # 创建临时文件
    tmp_fasta = OUTPUT_DIR / species_name / f"{species_name}_sampled.fasta"
    with open(tmp_fasta, 'w') as f:
        for name, seq in sampled_seqs.items():
            f.write(f">{name}\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i:i+60] + "\n")

    result = analyze_species_smart(species_name, str(tmp_fasta),
                                OUTPUT_DIR, f"(智人-采样150条)")
    if result:
        all_results.append(result)
        completed += 1
    else:
        print(f"❌ 智人分析失败")

    # 生成汇总报告
    print(f"\n{'='*60}")
    print(f"最终汇总：已完成 {completed}/{total} 个物种")
    print(f"{'='*60}")
    
    with open(OUTPUT_DIR / "汇总分析报告.md", 'w', encoding='utf-8') as f:
        f.write(f"# 蛋白质关键片段预测 — 完整分析报告\n\n")
        f.write(f"**分析日期：** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**分析物种总数：** {len(all_results)}  \n\n")
        f.write("## 各物种分析摘要\n\n")
        f.write("| # | 物种 | 序列数 | 共识序列长度 | 关键片段数 |\n")
        f.write("|---|------|--------|-------------|-----------|\n")
        for i, r in enumerate(all_results, 1):
            f.write(f"| {i} | {r['species']} | {r['n_sequences']} | {r['consensus_length']} aa | {r['key_fragments_count']} |\n")
        f.write(f"\n---\n*详细报告见 `results/` 目录*\n")

    print("✅ 分析完成！")