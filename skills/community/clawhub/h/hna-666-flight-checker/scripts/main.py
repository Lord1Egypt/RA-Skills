#!/usr/bin/env python3
"""
海航 666Plus 权益往返航班自动查询脚本 - 主入口
"""

import argparse
from flight_checker import HNAFlightChecker


def main():

    
    parser = argparse.ArgumentParser(description='海航 666Plus 权益往返航班查询')
    parser.add_argument('--out', required=True, help='去程日期 YYYYMMDD')
    parser.add_argument('--ret', required=True, help='返程日期 YYYYMMDD')
    parser.add_argument('--headless', action='store_true', help='无头模式')
    parser.add_argument('--debug', action='store_true')  # 新增
    
    args = parser.parse_args()
    if args.debug:
        from debug import set_debug
        set_debug(True)
        print("🔧 调试模式已开启")
    if len(args.out) != 8 or len(args.ret) != 8:
        print("❌ 日期格式错误，请使用 YYYYMMDD 格式")
        return
    if not (args.out.isdigit() and args.ret.isdigit()):
        print("❌ 日期必须为数字")
        return
    
    print("\n" + "="*60)
    print("🔧 初始化浏览器...")
    
    checker = HNAFlightChecker(headless=args.headless)
    results = []
    
    try:
        results = checker.find_round_trip_cities(args.out, args.ret)
    except Exception as e:
        print(f"\n⚠️ 运行过程中出现异常: {e}")
        print("但已获取部分结果，继续输出...")
    finally:
        checker.close()
        
        # 输出结果汇总
        print("\n" + "="*60)
        print("📊 查询结果汇总")
        print("="*60)
        
        if results:
            print(f"\n✅ 找到 {len(results)} 个可往返的目的地：")
            for code, name in results:
                print(f"   ✈️  {name} ({code})")
        else:
            print("\n❌ 没有找到可往返的目的地")
            print("\n💡 建议：")
            print("   • 检查日期是否正确")
            print("   • 尝试其他日期")
            print("   • 确认 666Plus 权益是否有效")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    main()
