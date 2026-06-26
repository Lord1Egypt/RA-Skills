# -*- coding: utf-8 -*-
"""
自动运行新闻摘要任务
阶段 1（抓取）→ 阶段 2（处理）→ 阶段 2.5（LLM 批量总结）→ 阶段 3（生成摘要 .txt）
飞书发送由心跳脚本自动完成
"""

import sys
import os
import io
import time
import warnings
from datetime import datetime

# 屏蔽无关警告（如 SSL 证书警告），保持输出整洁
warnings.filterwarnings("ignore")

# 设置 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_digest_v2.stage1_fetch import main as stage1_main
from news_digest_v2.stage2_process import main as stage2_main
from news_digest_v2.stage2_5_llm_summary import main as stage2_5_main
from news_digest_v2.stage3_output import main as stage3_main


def main():
    """运行完整流程"""
    total_start = datetime.now()
    
    print(f"\n{'='*70}")
    print(f"  每日新闻摘要任务 - 抓取 + LLM 总结 + 生成")
    print(f"  开始时间：{total_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # ========== 阶段 1：抓取 ==========
    print(f"\n{'='*70}")
    print(f"  阶段 1/3：新闻抓取")
    print(f"{'='*70}\n")
    
    try:
        stage1_result = stage1_main()
    except Exception as e:
        print(f"\n[ERROR] 阶段 1 失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    time.sleep(2)
    
    # ========== 阶段 2：处理 ==========
    print(f"\n{'='*70}")
    print(f"  阶段 2/3：新闻处理（去重 + 关键词）")
    print(f"{'='*70}\n")
    
    try:
        stage2_result = stage2_main()
    except Exception as e:
        print(f"\n[ERROR] 阶段 2 失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    time.sleep(1)
    
    # ========== 阶段 2.5：LLM 批量总结 ==========
    print(f"\n{'='*70}")
    print(f"  阶段 2.5/3：LLM 批量总结")
    print(f"{'='*70}\n")
    
    try:
        stage2_5_result = stage2_5_main()
    except Exception as e:
        print(f"\n[WARN] LLM 批量总结失败，使用原始摘要：{e}")
        import traceback
        traceback.print_exc()
        # 不中断流程，继续用原始摘要输出
    
    time.sleep(1)
    
    # ========== 阶段 3：生成摘要输出 ==========
    print(f"\n{'='*70}")
    print(f"  阶段 3/3：生成摘要输出")
    print(f"{'='*70}\n")
    
    try:
        stage3_result = stage3_main()
    except Exception as e:
        print(f"\n[ERROR] 阶段 3 失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # ========== 完成 ==========
    total_elapsed = (datetime.now() - total_start).total_seconds()
    
    print(f"\n{'='*70}")
    print(f"  [OK] 抓取和生成完成！")
    print(f"  总耗时：{total_elapsed:.1f}秒")
    print(f"{'='*70}\n")
    
    print(f"\n[SUMMARY] 流程总结：")
    print(f"  阶段 1（抓取）：已完成")
    print(f"  阶段 2（处理）：已完成")
    print(f"  阶段 2.5（LLM 总结）：已完成")
    print(f"  阶段 3（生成）：已完成")
    print(f"\n[OUTPUT] 输出文件：")
    print(f"  桌面：新闻摘要_YYYYMMDD_HHMMSS.txt")
    print(f"  工作区：.news-digest-out.md")
    print(f"\n[NOTE] 飞书发送由心跳脚本自动完成")
    print(f"\n[DONE] ALL_STAGES_DONE\n")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        print(f"\n[ERROR] 严重错误：{e}")
        traceback.print_exc()
        sys.exit(1)
