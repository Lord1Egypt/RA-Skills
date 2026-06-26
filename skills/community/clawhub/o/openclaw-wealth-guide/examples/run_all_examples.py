#!/usr/bin/env python3
"""
运行所有示例程序
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# 添加src目录到Python路径
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

def run_example(script_name, description):
    """运行单个示例"""
    print(f"\n{'='*60}")
    print(f"运行示例: {description}")
    print(f"{'='*60}")
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"错误: 脚本不存在: {script_path}")
        return False
    
    try:
        # 创建输出目录
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # 运行脚本
        start_time = time.time()
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        execution_time = time.time() - start_time
        
        print(f"执行时间: {execution_time:.2f}秒")
        print(f"退出代码: {result.returncode}")
        
        if result.stdout:
            print("\n输出:")
            print(result.stdout[:1000])  # 限制输出长度
        
        if result.stderr:
            print("\n错误:")
            print(result.stderr[:1000])  # 限制输出长度
        
        if result.returncode == 0:
            print(f"\n✅ {description} 执行成功!")
            return True
        else:
            print(f"\n❌ {description} 执行失败!")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {description} 执行超时!")
        return False
    except Exception as e:
        print(f"❌ {description} 执行异常: {e}")
        return False

def create_example_configs():
    """创建示例配置文件"""
    print(f"\n{'='*60}")
    print("创建示例配置文件")
    print(f"{'='*60}")
    
    config_dir = Path("config") / "examples"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"配置文件目录: {config_dir}")
    print("已创建的配置文件:")
    
    for config_file in config_dir.glob("*.yaml"):
        print(f"  - {config_file.name}")
    
    return True

def check_dependencies():
    """检查依赖"""
    print(f"\n{'='*60}")
    print("检查Python依赖")
    print(f"{'='*60}")
    
    try:
        import requests
        import pandas
        import beautifulsoup4
        import APScheduler
        import pydantic
        import yaml
        
        print("✅ 主要依赖检查通过")
        
        # 检查版本
        print(f"\n版本信息:")
        print(f"  requests: {requests.__version__}")
        print(f"  pandas: {pandas.__version__}")
        print(f"  pydantic: {pydantic.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 依赖缺失: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print("智能数据采集器 - 示例运行器")
    print("开始运行所有示例...")
    
    # 切换到示例目录
    original_cwd = os.getcwd()
    examples_dir = Path(__file__).parent
    os.chdir(examples_dir)
    
    try:
        # 确保输出目录存在
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # 检查依赖
        if not check_dependencies():
            print("❌ 依赖检查失败，停止执行")
            return 1
        
        # 创建配置文件
        if not create_example_configs():
            print("⚠️ 配置文件创建可能有问题")
        
        # 运行示例
        examples = [
            ("basic_usage.py", "基础使用示例"),
            ("openclaw_integration.py", "OpenClaw集成示例"),
        ]
        
        results = []
        for script_name, description in examples:
            success = run_example(script_name, description)
            results.append((description, success))
        
        # 显示总结
        print(f"\n{'='*60}")
        print("示例运行总结")
        print(f"{'='*60}")
        
        total = len(results)
        passed = sum(1 for _, success in results if success)
        failed = total - passed
        
        print(f"总共: {total} 个示例")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        
        if failed == 0:
            print("\n🎉 所有示例运行成功!")
        else:
            print("\n详细信息:")
            for description, success in results:
                status = "✅ 通过" if success else "❌ 失败"
                print(f"  {description}: {status}")
        
        # 显示输出文件
        print(f"\n{'='*60}")
        print("生成的输出文件")
        print(f"{'='*60}")
        
        if output_dir.exists():
            output_files = list(output_dir.rglob("*"))
            if output_files:
                for file_path in sorted(output_files):
                    if file_path.is_file():
                        file_size = file_path.stat().st_size
                        print(f"  {file_path.relative_to(output_dir)} ({file_size} 字节)")
            else:
                print("  没有输出文件")
        else:
            print("  输出目录不存在")
        
        return 0 if failed == 0 else 1
        
    finally:
        # 恢复原始工作目录
        os.chdir(original_cwd)

if __name__ == "__main__":
    sys.exit(main())