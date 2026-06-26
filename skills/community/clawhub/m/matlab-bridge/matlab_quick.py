#!/usr/bin/env python3
"""
MATLAB Quick Exec - 一句话执行MATLAB代码
用法: python matlab_quick.py "你的MATLAB代码"
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.matlab_bridge.matlab_bridge import matlab_exec


def main():
    if len(sys.argv) < 2:
        print("用法: python matlab_quick.py \"MATLAB代码\"")
        print("示例: python matlab_quick.py \"t=0:0.1:10; plot(t,sin(t)); saveas(gcf,'sine.png');\"")
        sys.exit(1)
    
    # 获取命令行传入的代码
    code = sys.argv[1]
    
    print(f"正在执行 MATLAB 代码...")
    print(f"代码: {code[:80]}{'...' if len(code) > 80 else ''}")
    print("-" * 50)
    
    try:
        result = matlab_exec(code)
        
        if result['success']:
            print("✅ 执行成功!")
            if result['stdout']:
                print("\nMATLAB 输出:")
                print(result['stdout'])
            print(f"\n结果保存至: matlab-outputs/")
        else:
            print("❌ 执行失败")
            if result['stderr']:
                print("\n错误信息:")
                print(result['stderr'])
                
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
