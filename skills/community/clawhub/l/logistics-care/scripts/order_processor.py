#!/usr/bin/env python3
"""
电商物流延迟检测 & 安抚短信 — 一站式订单处理器
组装 logistics_checker + sms_sender 流程
"""

import json
import os
import sys
import argparse
import subprocess
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")


def run_step(name: str, cmd: list):
    """执行一个子步骤"""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"⚠️  步骤失败 (exit code: {result.returncode})")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="物流延迟检测 & 安抚短信 — 一站式处理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 仅检测物流延迟（dry-run）
  python order_processor.py --input orders.csv

  # 检测并预览短信
  python order_processor.py --input orders.csv --preview

  # 检测 + 预览 + 发送（需配置短信API）
  python order_processor.py --input orders.csv --send --provider aliyun --config sms_config.json

  # 单号查询
  python order_processor.py --tracking SF1234567890 --phone 1234
        """,
    )
    
    # 输入
    parser.add_argument("--input", "-i", help="订单CSV文件路径")
    parser.add_argument("--tracking", "-t", help="单号查询: 快递单号")
    parser.add_argument("--carrier", "-c", default="", help="单号查询: 快递公司编码")
    parser.add_argument("--phone", "-p", default="", help="单号查询: 收件人手机尾号4位")
    
    # 模式
    parser.add_argument("--validate", action="store_true", help="仅验证CSV格式")
    parser.add_argument("--preview", action="store_true", help="检测+短信预览（默认dry-run）")
    parser.add_argument("--send", action="store_true", help="检测+预览+确认后发送短信")
    parser.add_argument("--provider", choices=["aliyun", "tencent"], default="aliyun", help="短信服务商")
    
    # 配置
    parser.add_argument("--config", help="短信配置JSON文件路径")
    parser.add_argument("--shop-name", default="小店", help="店铺名称")
    parser.add_argument("--contact-phone", default="400-000-0000", help="客服电话")
    parser.add_argument("--output-dir", "-o", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_json = os.path.join(args.output_dir, f"logistics_results_{timestamp}.json")
    preview_html = os.path.join(args.output_dir, f"sms_preview_{timestamp}.html")
    
    # 单号查询模式
    if args.tracking:
        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "logistics_checker.py"),
            "--single", args.tracking,
        ]
        if args.carrier:
            cmd += ["--carrier", args.carrier]
        if args.phone:
            cmd += ["--phone", args.phone]
        run_step("🔍 单号物流查询", cmd)
        return
    
    # CSV批量模式
    if not args.input:
        print("❌ 请提供 --input orders.csv 或 --tracking 单号")
        sys.exit(1)
    
    # Step 1: 验证CSV
    validate_cmd = [
        sys.executable,
        os.path.join(SCRIPTS_DIR, "logistics_checker.py"),
        "--input", args.input,
        "--validate",
    ]
    run_step("📋 Step 1/3: 验证订单数据", validate_cmd)
    
    if args.validate:
        return
    
    # Step 2: 查询物流
    check_cmd = [
        sys.executable,
        os.path.join(SCRIPTS_DIR, "logistics_checker.py"),
        "--input", args.input,
        "--output", results_json,
    ]
    if not run_step("🔍 Step 2/3: 查询物流轨迹", check_cmd):
        print("❌ 物流查询失败，请检查API配置")
        sys.exit(1)
    
    # Step 3: 生成短信
    sms_mode = "send" if args.send else "dry-run"
    sms_cmd = [
        sys.executable,
        os.path.join(SCRIPTS_DIR, "sms_sender.py"),
        "--input", results_json,
        "--mode", sms_mode,
        "--provider", args.provider,
        "--output", preview_html,
        "--shop-name", args.shop_name,
        "--contact-phone", args.contact_phone,
    ]
    if args.config:
        sms_cmd += ["--config", args.config]
    
    if not run_step("📱 Step 3/3: 生成安抚短信", sms_cmd):
        print("⚠️  短信处理部分失败")
    
    # 最终摘要
    print(f"\n{'='*60}")
    print(f"  ✅ 处理完成!")
    print(f"{'='*60}")
    print(f"  物流结果: {results_json}")
    print(f"  短信预览: {preview_html}")
    
    if args.send:
        print(f"\n  📱 短信已发送，请在阿里云/腾讯云控制台查看发送详情")
    else:
        print(f"\n  💡 提示：短信为预览模式，未真实发送")
        print(f"    确认无误后，使用 --send 参数发送短信")
        print(f"    python {os.path.basename(__file__)} --input {args.input} --send --config sms_config.json")


if __name__ == "__main__":
    main()
