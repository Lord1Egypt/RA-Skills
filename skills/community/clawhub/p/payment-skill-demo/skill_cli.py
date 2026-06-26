#!/usr/bin/env python3
"""
支付 Skill 命令行入口 (v2 - 使用命令行参数)

龙虾通过 exec 工具调用此脚本来执行支付操作。

用法:
    python skill_cli.py create_payment --amount=299.00 --currency=CNY --merchant_id=taobao_001
    python skill_cli.py query_payment --transaction_id=txn_001
    python skill_cli.py refund_payment --transaction_id=txn_001 --amount=100.00
"""

import sys
import json
import os
import asyncio
import logging
import argparse
from pathlib import Path

# 配置日志：写入文件而不是 stdout，避免污染 JSON 输出
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(log_dir / "skill.log"),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment():
    """
    检查环境是否完整
    
    检查项：
    1. 虚拟环境是否存在
    2. 必需的依赖是否安装
    """
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"
    
    # 检查虚拟环境
    if not venv_path.exists():
        print("❌ 错误: 虚拟环境未初始化", file=sys.stderr)
        print("\n请运行以下命令初始化环境:", file=sys.stderr)
        print("  Linux/Mac: ./scripts/setup.sh", file=sys.stderr)
        print("  Windows:   scripts\\setup.bat", file=sys.stderr)
        print("\n或者手动执行:", file=sys.stderr)
        print("  python -m venv venv", file=sys.stderr)
        print("  pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
    
    # 检查必需的依赖
    try:
        import aiohttp
        import pydantic
    except ImportError as e:
        print(f"❌ 错误: 缺少依赖 - {e}", file=sys.stderr)
        print("\n请运行以下命令安装依赖:", file=sys.stderr)
        print("  Linux/Mac: ./scripts/setup.sh", file=sys.stderr)
        print("  Windows:   scripts\\setup.bat", file=sys.stderr)
        print("\n或者手动执行:", file=sys.stderr)
        print("  pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='支付 Skill 命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建支付
  python skill_cli.py create_payment --amount=299.00 --currency=CNY --merchant_id=taobao_001 --description="购买鼠标"
  
  # 查询支付
  python skill_cli.py query_payment --transaction_id=txn_20260315_001
  
  # 发起退款
  python skill_cli.py refund_payment --transaction_id=txn_20260315_001 --amount=100.00 --reason="商品质量问题"

环境变量:
  PAYMENT_API_KEY     - API 密钥（必需）
  PAYMENT_API_SECRET  - API 密钥（必需）
  PAYMENT_API_URL     - API 地址（可选）
  PAYMENT_ENV         - 环境 (development/production，默认 development)
        """
    )
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # create_payment 命令
    create_parser = subparsers.add_parser('create_payment', help='创建支付请求')
    create_parser.add_argument('--amount', type=float, required=True, help='支付金额（元）')
    create_parser.add_argument('--currency', type=str, default='CNY', help='货币代码（默认 CNY）')
    create_parser.add_argument('--merchant_id', type=str, required=True, help='商户 ID')
    create_parser.add_argument('--description', type=str, help='支付描述')
    
    # query_payment 命令
    query_parser = subparsers.add_parser('query_payment', help='查询支付状态')
    query_parser.add_argument('--transaction_id', type=str, required=True, help='交易 ID')
    
    # refund_payment 命令
    refund_parser = subparsers.add_parser('refund_payment', help='发起退款')
    refund_parser.add_argument('--transaction_id', type=str, required=True, help='原交易 ID')
    refund_parser.add_argument('--amount', type=float, help='退款金额（元，可选）')
    refund_parser.add_argument('--reason', type=str, help='退款原因')
    
    # 全局参数
    parser.add_argument('--env', type=str, choices=['development', 'production'], 
                       help='环境（默认从 PAYMENT_ENV 读取，或 development）')
    
    return parser


async def execute_tool(tool_name: str, params: dict, env: str = "development") -> dict:
    """
    执行工具
    
    Args:
        tool_name: 工具名称
        params: 工具参数
        env: 环境名称 (development 或 production)
    
    Returns:
        执行结果
    """
    # 延迟导入 PaymentSkill，确保环境检查已通过
    src_dir = Path(__file__).parent / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    from payment_skill import PaymentSkill
    
    skill = None
    try:
        # 初始化 Skill
        skill = PaymentSkill(env=env)
        await skill.initialize()
        
        # 执行工具
        result = await skill.execute(tool_name, params)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"执行失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        # 清理资源
        if skill:
            try:
                await skill.cleanup()
            except:
                pass


def main():
    """主函数"""
    # 检查环境
    check_environment()
    
    parser = create_parser()
    args = parser.parse_args()
    
    # 检查是否提供了命令
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 确定环境
    env = args.env or os.getenv("PAYMENT_ENV", "development")
    
    # 构造参数字典
    params = {}
    if args.command == 'create_payment':
        params = {
            'amount': args.amount,
            'currency': args.currency,
            'merchant_id': args.merchant_id,
        }
        if args.description:
            params['description'] = args.description
    
    elif args.command == 'query_payment':
        params = {
            'transaction_id': args.transaction_id
        }
    
    elif args.command == 'refund_payment':
        params = {
            'transaction_id': args.transaction_id
        }
        if args.amount:
            params['amount'] = args.amount
        if args.reason:
            params['reason'] = args.reason
    
    # 执行工具
    try:
        # 兼容 Python 3.6 的异步执行方式
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(execute_tool(args.command, params, env))
        
        # 输出结果（JSON 格式）
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 根据结果设置退出码
        sys.exit(0 if result["success"] else 1)
        
    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
