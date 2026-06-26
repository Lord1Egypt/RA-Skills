#!/usr/bin/env python3
"""
打卡记录更新脚本
向腾讯文档追加今日打卡记录

使用方法:
    python update_record.py --file-id DWm5ReEZVeWdabUV6 --steps 10698 --weight 70.9

依赖:
    需要配置环境变量 TENCENT_DOCS_TOKEN
    需要安装mcporter
"""

import argparse
import os
import json
import subprocess
from datetime import datetime


def run_mcporter(service, tool, args):
    """执行mcporter命令"""
    cmd = f'mcporter call {service} {tool} --args \'{json.dumps(args)}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr


def append_content(file_id, content):
    """向文档追加内容"""
    args = {
        "action": "INSERT_AFTER",
        "content": content,
        "file_id": file_id,
        "id": ""
    }
    stdout, stderr = run_mcporter('tencent-docs', 'smartcanvas.edit', args)

    try:
        result = json.loads(stdout)
        return {'success': result.get('error') == ''}
    except:
        return {'success': False, 'error': stdout + stderr}


def calc_calories(steps, weight=70):
    """计算卡路里消耗"""
    step_cal = steps * 0.04
    # 快走消耗
    distance = steps * 0.00075  # km
    walking_cal = 0.05 * weight * distance * 60  # 约5MET
    return int(step_cal + walking_cal)


def main():
    parser = argparse.ArgumentParser(description='更新健康打卡记录')
    parser.add_argument('--file-id', '-f', required=True, help='腾讯文档ID')
    parser.add_argument('--steps', '-s', type=int, default=0, help='今日步数')
    parser.add_argument('--weight', '-w', type=float, default=70, help='体重(kg)')
    parser.add_argument('--date', '-d', default='', help='日期（默认今天）')
    parser.add_argument('--drinks', type=bool, default=False, help='是否饮酒')

    args = parser.parse_args()

    # 检查Token
    token = os.environ.get('TENCENT_DOCS_TOKEN')
    if not token:
        print("⚠️ 未配置TENCENT_DOCS_TOKEN，请先配置环境变量")
        return

    # 默认今天
    if not args.date:
        args.date = datetime.now().strftime('%Y-%m-%d')

    print("=" * 50)
    print("📝 更新打卡记录")
    print("=" * 50)
    print(f"文档ID：{args.file_id}")
    print(f"日期：{args.date}")

    if args.steps > 0:
        calories = calc_calories(args.steps, args.weight)
        distance = args.steps * 0.00075
        duration = int(args.steps / 100)  # 约100步/分钟

        content = f"""## 📅 {args.date} 打卡记录

| 项目 | 数据 | 状态 |
|------|------|------|
| 日期 | {args.date} | ✅ |
| 步数 | {args.steps:,}步 | ✅ 达标 |
| 距离 | 约{distance:.1f}km | - |
| 时长 | 约{duration}分钟 | - |
| 消耗 | 约{calories}卡 | 🔥 |
| 饮酒 | {'是 ❌' if args.drinks else '否 ✅'} | - |

**运动评价：** 今日完成中等强度有氧运动，达到减脂目标。

---"""

        print(f"\n🔥 今日数据：")
        print(f"   步数：{args.steps:,}步")
        print(f"   消耗：约{calories}卡")

        print(f"\n📝 正在更新文档...")
        result = append_content(args.file_id, content)

        if result['success']:
            print("✅ 打卡记录已更新！")
        else:
            print(f"❌ 更新失败：{result.get('error', '未知错误')}")

    else:
        print("⚠️ 请提供步数 --steps")

    print("=" * 50)


if __name__ == "__main__":
    main()
