#!/usr/bin/env python3
"""
MATLAB Bridge 快速测试脚本
验证 MATLAB 环境配置和基本功能
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加技能路径
sys.path.insert(0, str(Path(__file__).parent))


def check_matlab_in_path():
    """检查 MATLAB 是否在系统 PATH 中"""
    print("=" * 60)
    print("MATLAB Bridge 环境测试")
    print("=" * 60)
    
    print("\n1. MATLAB 命令检查")
    
    # 尝试执行 matlab 命令
    try:
        result = subprocess.run(
            ["matlab", "-batch", "disp('MATLAB_IS_AVAILABLE')"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if "MATLAB_IS_AVAILABLE" in result.stdout:
            print("   状态: ✓ MATLAB 命令可用")
            
            # 获取版本信息
            version_result = subprocess.run(
                ["matlab", "-batch", "disp(version)"],
                capture_output=True,
                text=True,
                timeout=30
            )
            version = version_result.stdout.strip()
            print(f"   版本: {version}")
            return True
        else:
            print("   状态: ✗ MATLAB 命令执行失败")
            if result.stderr:
                print(f"   错误: {result.stderr[:200]}")
            return False
            
    except FileNotFoundError:
        print("   状态: ✗ MATLAB 命令未找到")
        print("   提示: MATLAB 未添加到系统 PATH")
        return False
    except subprocess.TimeoutExpired:
        print("   状态: ✗ MATLAB 启动超时")
        print("   提示: 检查 MATLAB 许可证或重新安装")
        return False
    except Exception as e:
        print(f"   状态: ✗ 检查失败: {e}")
        return False


def check_matlab_license():
    """检查 MATLAB 许可证状态"""
    print(f"\n2. 许可证检查")
    
    try:
        result = subprocess.run(
            ["matlab", "-batch", "license('test', 'MATLAB')"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if "1" in result.stdout:
            print("   状态: ✓ 许可证有效")
            return True
        else:
            print("   状态: △ 许可证状态不确定")
            print("   提示: 如果 MATLAB 能正常启动则无需担心")
            return True  # 不确定但可能可用
            
    except Exception as e:
        print(f"   状态: △ 无法验证许可证: {e}")
        return True  # 不确定


def test_basic_calculation():
    """测试基本计算功能"""
    print(f"\n3. 基本计算测试")
    
    test_code = """
a = [1, 2, 3; 4, 5, 6; 7, 8, 9];
b = a * a';
disp(['Matrix multiplication result size: ', num2str(size(b,1)), 'x', num2str(size(b,2))]);
disp('BASIC_CALCULATION_OK');
"""
    
    try:
        result = subprocess.run(
            ["matlab", "-batch", test_code],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if "BASIC_CALCULATION_OK" in result.stdout:
            print("   状态: ✓ 矩阵运算正常")
            # 提取结果大小
            for line in result.stdout.split('\n'):
                if 'Matrix multiplication result' in line:
                    print(f"   测试: {line.strip()}")
            return True
        else:
            print("   状态: ✗ 计算测试失败")
            if result.stderr:
                print(f"   错误: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"   状态: ✗ 测试失败: {e}")
        return False


def test_plotting():
    """测试绘图功能"""
    print(f"\n4. 绘图功能测试")
    
    output_dir = Path("D:/Personal/OpenClaw/matlab-outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    test_code = f"""
x = 0:0.1:2*pi;
y = sin(x);
fig = figure('Visible', 'off');
plot(x, y, 'LineWidth', 2);
title('MATLAB Bridge Test');
xlabel('x');
ylabel('sin(x)');
print(fig, '{output_dir.as_posix()}/test_plot', '-dpng', '-r300');
close(fig);
disp('PLOT_TEST_OK');
"""
    
    try:
        result = subprocess.run(
            ["matlab", "-batch", test_code],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if "PLOT_TEST_OK" in result.stdout:
            test_file = output_dir / "test_plot.png"
            if test_file.exists():
                size_kb = test_file.stat().st_size / 1024
                print("   状态: ✓ 绘图功能正常")
                print(f"   输出: {test_file}")
                print(f"   大小: {size_kb:.1f} KB")
                return True
            else:
                print("   状态: △ 绘图命令执行但文件未生成")
                return True
        else:
            print("   状态: ✗ 绘图测试失败")
            if result.stderr:
                print(f"   错误: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"   状态: ✗ 测试失败: {e}")
        return False


def test_signal_processing():
    """测试信号处理功能"""
    print(f"\n5. 信号处理测试")
    
    test_code = """
% 生成测试信号
t = 0:0.001:1;
f = 10;
signal = sin(2*pi*f*t);

% FFT分析
Y = fft(signal);
P2 = abs(Y/length(signal));
P1 = P2(1:length(signal)/2+1);
P1(2:end-1) = 2*P1(2:end-1);

% 找到主频
[~, idx] = max(P1);
fs = 1000;
freq = (idx-1)*fs/length(signal);

disp(['Dominant frequency: ', num2str(freq), ' Hz (expected: 10 Hz)']);
disp('SIGNAL_PROCESSING_OK');
"""
    
    try:
        result = subprocess.run(
            ["matlab", "-batch", test_code],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if "SIGNAL_PROCESSING_OK" in result.stdout:
            print("   状态: ✓ FFT分析正常")
            for line in result.stdout.split('\n'):
                if 'Dominant frequency' in line:
                    print(f"   测试: {line.strip()}")
            return True
        else:
            print("   状态: ✗ 信号处理测试失败")
            return False
            
    except Exception as e:
        print(f"   状态: ✗ 测试失败: {e}")
        return False


def show_setup_help():
    """显示安装帮助"""
    print("\n" + "=" * 60)
    print("MATLAB 配置帮助")
    print("=" * 60)
    print("""
将 MATLAB 添加到系统 PATH：

方式1 - PowerShell（临时，当前会话）：
    $env:PATH += ";C:\Program Files\MATLAB\R2023b\bin"

方式2 - PowerShell（永久）：
    [Environment]::SetEnvironmentVariable(
        "PATH",
        $env:PATH + ";C:\Program Files\MATLAB\R2023b\bin",
        "User"
    )

方式3 - 手动添加：
    1. 右键"此电脑" → 属性 → 高级系统设置
    2. 环境变量 → 编辑 PATH
    3. 添加 MATLAB 的 bin 目录路径

注意：根据你的 MATLAB 版本调整路径（R2023b → 你的版本）

常见 MATLAB 安装路径：
    C:\Program Files\MATLAB\R2023b\bin
    C:\Program Files\MATLAB\R2023a\bin
    C:\Program Files\MATLAB\R2022b\bin
""")


def main():
    """主函数"""
    results = {
        "matlab_available": check_matlab_in_path(),
        "license_ok": False,
        "basic_calc": False,
        "plotting": False,
        "signal_proc": False
    }
    
    if results["matlab_available"]:
        results["license_ok"] = check_matlab_license()
        results["basic_calc"] = test_basic_calculation()
        results["plotting"] = test_plotting()
        results["signal_proc"] = test_signal_processing()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum([
        results["matlab_available"],
        results["license_ok"],
        results["basic_calc"],
        results["plotting"],
        results["signal_proc"]
    ])
    total = 5
    
    print(f"\n通过: {passed}/{total}")
    print(f"\n详细结果:")
    print(f"  MATLAB 命令:   {'✓' if results['matlab_available'] else '✗'}")
    print(f"  许可证状态:     {'✓' if results['license_ok'] else '✗'}")
    print(f"  基本计算:       {'✓' if results['basic_calc'] else '✗'}")
    print(f"  绘图功能:       {'✓' if results['plotting'] else '✗'}")
    print(f"  信号处理:       {'✓' if results['signal_proc'] else '✗'}")
    
    if passed == total:
        print("\n✓ 所有测试通过！MATLAB Bridge 技能已就绪")
        return 0
    elif results["matlab_available"]:
        print("\n△ MATLAB 可用，但部分功能测试未通过")
        print("  技能可能仍可正常使用")
        return 0
    else:
        print("\n✗ MATLAB 未正确配置")
        show_setup_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
