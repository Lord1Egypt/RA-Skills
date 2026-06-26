#!/usr/bin/env python3
"""
完整的 IRED 序列质量控制分析
基于 protein-qc-strict skill
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from Bio import SeqIO, AlignIO
from collections import Counter
import numpy as np
import re

# 工作目录
WORK_DIR = Path("/root/autodl-tmp/ou_a1d19d5984eecd78f231c50f774eddb0/ChemRxiv_QC_analysis")
INPUT_FASTA = Path("/root/autodl-tmp/ou_a1d19d5984eecd78f231c50f774eddb0/ChemRxiv_QC_analysis/input/all_ired_merged.fasta")

# 创建日志
LOG_FILE = WORK_DIR / "logs" / f"qc_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# 确保目录存在
WORK_DIR.mkdir(parents=True, exist_ok=True)
(WORK_DIR / "logs").mkdir(exist_ok=True)
(WORK_DIR / "sequences").mkdir(exist_ok=True)
(WORK_DIR / "alignment").mkdir(exist_ok=True)
(WORK_DIR / "analysis").mkdir(exist_ok=True)

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

def run_command(cmd, description):
    """运行命令并记录"""
    log(f"开始: {description}")
    log(f"命令: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        log(f"❌ 失败: {description}")
        log(f"错误: {result.stderr}")
        return False
    
    log(f"✅ 完成: {description}")
    if result.stdout:
        log(f"输出: {result.stdout[:500]}")
    
    return True

# ============================================================
# 阶段 1: 长度过滤
# ============================================================
def stage1_length_filter():
    """阶段 1: 长度过滤 (200-500 aa)"""
    log("\n" + "="*60)
    log("阶段 1: 长度过滤")
    log("="*60)
    
    sequences = list(SeqIO.parse(INPUT_FASTA, "fasta"))
    log(f"输入序列: {len(sequences)} 条")
    
    filtered = []
    removed_short = 0
    removed_long = 0
    removed_bad_chars = 0
    
    for seq in sequences:
        length = len(seq.seq)
        
        # 长度检查
        if length < 200:
            removed_short += 1
            continue
        if length > 500:
            removed_long += 1
            continue
        
        # 非标准字符检查
        seq_str = str(seq.seq)
        bad_chars = set(seq_str) - set('ACDEFGHIKLMNPQRSTVWY')
        if bad_chars:
            removed_bad_chars += 1
            continue
        
        filtered.append(seq)
    
    # 保存
    output_file = WORK_DIR / "sequences" / "01_length_filtered.fasta"
    SeqIO.write(filtered, output_file, "fasta")
    
    log(f"输出序列: {len(filtered)} 条")
    log(f"移除 < 200 aa: {removed_short} 条")
    log(f"移除 > 500 aa: {removed_long} 条")
    log(f"移除非标准字符: {removed_bad_chars} 条")
    log(f"保留率: {len(filtered)/len(sequences)*100:.1f}%")
    
    return output_file

# ============================================================
# 阶段 2: CD-HIT 去冗余
# ============================================================
def stage2_cdhit(input_file):
    """阶段 2: CD-HIT 去冗余 (90%)"""
    log("\n" + "="*60)
    log("阶段 2: CD-HIT 去冗余")
    log("="*60)
    
    output_file = WORK_DIR / "sequences" / "02_cdhit_90.fasta"
    cluster_file = output_file.with_suffix(".fasta.clstr")
    
    cmd = f"""
    cd-hit -i {input_file} \
           -o {output_file} \
           -c 0.90 \
           -n 5 \
           -M 0 \
           -T 8
    """
    
    if not run_command(cmd, "CD-HIT 去冗余"):
        return None
    
    # 统计
    input_count = len(list(SeqIO.parse(input_file, "fasta")))
    output_count = len(list(SeqIO.parse(output_file, "fasta")))
    
    log(f"输入序列: {input_count} 条")
    log(f"输出序列: {output_count} 条")
    log(f"去冗余率: {(input_count - output_count)/input_count*100:.1f}%")
    
    return output_file

# ============================================================
# 阶段 3: 复杂度检查
# ============================================================
def calculate_complexity(seq_str):
    """计算 Shannon 熵"""
    if len(seq_str) == 0:
        return 0
    
    counts = Counter(seq_str)
    total = len(seq_str)
    
    entropy = 0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log2(p)
    
    return entropy

def stage3_complexity(input_file):
    """阶段 3: 复杂度检查 (熵 >= 2.0)"""
    log("\n" + "="*60)
    log("阶段 3: 复杂度检查")
    log("="*60)
    
    sequences = list(SeqIO.parse(input_file, "fasta"))
    
    filtered = []
    low_complexity = []
    
    for seq in sequences:
        complexity = calculate_complexity(str(seq.seq))
        
        if complexity >= 2.0:
            filtered.append(seq)
        else:
            low_complexity.append((seq.id, complexity))
    
    # 保存
    output_file = WORK_DIR / "sequences" / "03_complexity_filtered.fasta"
    SeqIO.write(filtered, output_file, "fasta")
    
    log(f"输入序列: {len(sequences)} 条")
    log(f"复杂度 >= 2.0: {len(filtered)} 条")
    log(f"低复杂度: {len(low_complexity)} 条")
    
    if low_complexity:
        log("低复杂度序列:")
        for seq_id, comp in low_complexity[:10]:
            log(f"  {seq_id}: {comp:.3f}")
    
    return output_file

# ============================================================
# 阶段 4: Motif 验证
# ============================================================
def stage4_motif(input_file):
    """阶段 4: Motif 验证 (Rossmann fold)"""
    log("\n" + "="*60)
    log("阶段 4: Motif 验证")
    log("="*60)
    
    # Rossmann fold pattern: G-X-G-X-X-G
    rossmann_pattern = re.compile(r'G.G..G')
    
    sequences = list(SeqIO.parse(input_file, "fasta"))
    
    with_motif = []
    without_motif = []
    
    for seq in sequences:
        if rossmann_pattern.search(str(seq.seq)):
            with_motif.append(seq)
        else:
            without_motif.append(seq)
    
    # 保存所有序列（包括不含 motif 的）
    output_file = WORK_DIR / "sequences" / "04_motif_checked.fasta"
    SeqIO.write(sequences, output_file, "fasta")
    
    log(f"总序列: {len(sequences)} 条")
    log(f"包含 Rossmann fold: {len(with_motif)} 条 ({len(with_motif)/len(sequences)*100:.1f}%)")
    log(f"不包含: {len(without_motif)} 条 ({len(without_motif)/len(sequences)*100:.1f}%)")
    
    if len(with_motif) / len(sequences) > 0.5:
        log("✅ Motif 覆盖率良好 (> 50%)")
    else:
        log("⚠️ Motif 覆盖率偏低 (< 50%)")
    
    return output_file

# ============================================================
# 阶段 5: 多序列比对
# ============================================================
def stage5_alignment(input_file):
    """阶段 5: MAFFT 多序列比对"""
    log("\n" + "="*60)
    log("阶段 5: 多序列比对")
    log("="*60)
    
    output_file = WORK_DIR / "alignment" / "05_aligned.fasta"
    log_file = WORK_DIR / "logs" / "mafft.log"
    
    cmd = f"""
    mafft --localpair \
          --maxiterate 1000 \
          --thread 8 \
          {input_file} 1> {output_file} 2> {log_file}
    """
    
    if not run_command(cmd, "MAFFT 多序列比对"):
        return None
    
    # 检查输出
    alignment = AlignIO.read(output_file, "fasta")
    log(f"序列数: {len(alignment)}")
    log(f"比对长度: {alignment.get_alignment_length()}")
    
    return output_file

# ============================================================
# 阶段 6: 比对修剪
# ============================================================
def stage6_trim(input_file):
    """阶段 6: trimAl 比对修剪"""
    log("\n" + "="*60)
    log("阶段 6: 比对修剪")
    log("="*60)
    
    output_file = WORK_DIR / "alignment" / "06_trimmed.fasta"
    
    cmd = f"""
    trimal -in {input_file} \
           -out {output_file} \
           -automated1
    """
    
    if not run_command(cmd, "trimAl 比对修剪"):
        return None
    
    # 比较修剪前后
    before = AlignIO.read(input_file, "fasta")
    after = AlignIO.read(output_file, "fasta")
    
    log(f"修剪前长度: {before.get_alignment_length()}")
    log(f"修剪后长度: {after.get_alignment_length()}")
    log(f"保留率: {after.get_alignment_length()/before.get_alignment_length()*100:.1f}%")
    
    return output_file

# ============================================================
# 主函数
# ============================================================
def main():
    log("="*60)
    log("IRED 序列质量控制分析")
    log("="*60)
    log(f"工作目录: {WORK_DIR}")
    log(f"输入文件: {INPUT_FASTA}")
    
    # 阶段 1: 长度过滤
    stage1_output = stage1_length_filter()
    if not stage1_output:
        log("❌ 阶段 1 失败")
        return
    
    # 阶段 2: CD-HIT 去冗余
    stage2_output = stage2_cdhit(stage1_output)
    if not stage2_output:
        log("❌ 阶段 2 失败")
        return
    
    # 阶段 3: 复杂度检查
    stage3_output = stage3_complexity(stage2_output)
    if not stage3_output:
        log("❌ 阶段 3 失败")
        return
    
    # 阶段 4: Motif 验证
    stage4_output = stage4_motif(stage3_output)
    if not stage4_output:
        log("❌ 阶段 4 失败")
        return
    
    # 阶段 5: 多序列比对
    stage5_output = stage5_alignment(stage4_output)
    if not stage5_output:
        log("❌ 阶段 5 失败")
        return
    
    # 阶段 6: 比对修剪
    stage6_output = stage6_trim(stage5_output)
    if not stage6_output:
        log("❌ 阶段 6 失败")
        return
    
    log("\n" + "="*60)
    log("✅ 质量控制分析完成！")
    log("="*60)
    log(f"最终序列: {stage6_output}")
    log(f"日志文件: {LOG_FILE}")

if __name__ == "__main__":
    main()
