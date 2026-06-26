#!/usr/bin/env python3
"""
验证预测准确率

用法：
  python3 verify.py --issue 2026034 --actual 3,6,13,21,28,29,6
"""

import json
import argparse

def verify(issue: str, predicted_reds: list, predicted_blues: list, actual_reds: list, actual_blue: int):
    """验证准确率"""
    red_matches = len(set(predicted_reds) & set(actual_reds))
    blue_match = 1 if actual_blue in predicted_blues else 0
    
    result = {
        "issue": issue,
        "red_matches": red_matches,
        "blue_match": blue_match,
        "accuracy": {
            "red_rate": f"{red_matches}/{len(predicted_reds)} ({red_matches/len(predicted_reds)*100:.1f}%)",
            "blue_hit": "✅" if blue_match else "❌"
        },
        "prize_level": get_prize_level(red_matches, blue_match)
    }
    
    return result

def get_prize_level(red_matches: int, blue_match: int) -> str:
    """判断中奖等级"""
    if red_matches == 6 and blue_match:
        return "🏆 一等奖"
    elif red_matches == 6:
        return "🥈 二等奖"
    elif red_matches == 5 and blue_match:
        return "🥉 三等奖"
    elif red_matches == 5 or (red_matches == 4 and blue_match):
        return "四等奖"
    elif red_matches == 4 or (red_matches == 3 and blue_match):
        return "五等奖"
    elif red_matches == 2 and blue_match or red_matches == 1 and blue_match or red_matches == 0 and blue_match:
        return "六等奖"
    else:
        return "未中奖"

def main():
    parser = argparse.ArgumentParser(description="验证预测准确率")
    parser.add_argument("--issue", type=str, required=True, help="期号")
    parser.add_argument("--predicted-reds", type=str, help="预测红球（逗号分隔）")
    parser.add_argument("--predicted-blues", type=str, help="预测蓝球（逗号分隔）")
    parser.add_argument("--actual", type=str, required=True, help="实际开奖号码（格式：红球 1,红球 2,...,蓝球）")
    
    args = parser.parse_args()
    
    actual_parts = [int(x) for x in args.actual.split(',')]
    actual_blue = actual_parts[-1]
    actual_reds = actual_parts[:-1]
    
    predicted_reds = [int(x) for x in args.predicted_reds.split(',')] if args.predicted_reds else []
    predicted_blues = [int(x) for x in args.predicted_blues.split(',')] if args.predicted_blues else []
    
    result = verify(args.issue, predicted_reds, predicted_blues, actual_reds, actual_blue)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
