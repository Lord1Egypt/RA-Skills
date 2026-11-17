# -*- coding: utf-8 -*-
"""
自动运行新闻摘要任务
阶段 1（抓取）→ 阶段 2（处理）→ 阶段 2.5（发改广播站刷新+比对+补充）→ 阶段 2.6（LLM 总结）→ 阶段 3（输出）
飞书发送由心跳脚本自动完成

注意：FGB 比对在 LLM 之前运行，LLM 阶段会自动排除 FGB 已采用的文章（matched_article_id IS NOT NULL）
"""

import sys
import os
import io
import time
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_digest_v2.stage1_fetch import main as stage1_main
from news_digest_v2.stage2_process import main as stage2_main
from news_digest_v2.stage2_5_llm_summary import main as stage2_5_main
from news_digest_v2.stage2_6_fgb import main as stage2_6_main
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
    print(f"  阶段 1/4：新闻抓取")
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
    print(f"  阶段 2/4：新闻处理（去重 + 关键词）")
    print(f"{'='*70}\n")
    
    try:
        stage2_result = stage2_main()
    except Exception as e:
        print(f"\n[ERROR] 阶段 2 失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    time.sleep(1)
    
    # ========== 阶段 2.5：发改广播站（刷新 + 比对 + 补充）==========
    # 放在 Stage 2 之后、LLM 之前：
    # - Stage 2 完成后 articles 已去重，比对结果准确
    # - FGB 匹配结果写入 matched_article_id 后，LLM 阶段自动排除
    # - 未匹配的 FGB 新闻补充到 articles，可进入 LLM 和输出流程
    # - 本阶段完全隔离在 try 块中，失败不影响主流程
    print(f"\n{'='*70}")
    print(f"  阶段 2.5/4：发改广播站（刷新 + 比对 + 补充）")
    print(f"{'='*70}\n")
    
    try:
        stage2_6_main()
    except Exception as e:
        print(f"\n  [FGB] ⚠️ 发改广播站处理失败: {e}")
        print(f"  [FGB] 不影响主流程，继续执行后续阶段")
        import traceback
        traceback.print_exc()
    
    time.sleep(1)
    
    # ========== 阶段 2.6：LLM 批量总结 ==========
    # LLM 阶段的 SQL 查询自动排除 FGB 已采用的文章（matched_article_id IS NOT NULL）
    # 确保摘要输出与发改广播站不重复
    print(f"\n{'='*70}")
    print(f"  阶段 2.6/4：LLM 批量总结")
    print(f"{'='*70}\n")
    
    try:
        stage2_5_main()
    except Exception as e:
        print(f"\n[WARN] LLM 批量总结失败，使用原始摘要：{e}")
        import traceback
        traceback.print_exc()
        # 不中断流程，继续用原始摘要输出
    
    time.sleep(1)
    
    # ========== 阶段 3：生成摘要输出 ==========
    print(f"\n{'='*70}")
    print(f"  阶段 3/4：生成摘要输出")
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
    print(f"  阶段 2.5（发改广播站）：已完成")
    print(f"  阶段 2.6（LLM 总结）：已完成（自动排除 FGB 已采用文章）")
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
