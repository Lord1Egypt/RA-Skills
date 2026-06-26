#!/usr/bin/env python3
"""
测试运行器 - 自动化测试和反馈收集
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
import sys

class TestRunner:
    def __init__(self):
        self.test_results = []
        self.test_dir = Path("test_results")
        self.test_dir.mkdir(exist_ok=True)
        
    def run_basic_test(self, test_name, test_dir):
        """运行基础测试"""
        print(f"\n🔧 运行测试: {test_name}")
        print("-" * 40)
        
        # 创建测试目录结构
        test_path = Path(test_dir)
        test_path.mkdir(exist_ok=True)
        
        # 创建测试文件
        test_files = [
            ("document1.pdf", "Test document content"),
            ("image1.jpg", "Test image"),
            ("video1.mp4", "Test video"),
            ("music1.mp3", "Test audio"),
            ("archive1.zip", "Test archive"),
            ("script1.py", "Test code"),
        ]
        
        for filename, content in test_files:
            filepath = test_path / filename
            filepath.write_text(content)
            print(f"  📄 创建测试文件: {filename}")
        
        # 运行整理命令
        cmd = [
            sys.executable, "scripts/organize.py",
            "--path", str(test_path),
            "--rename",
            "--preview"
        ]
        
        result = {
            "test_name": test_name,
            "test_time": datetime.now().isoformat(),
            "test_files": len(test_files),
            "command": " ".join(cmd)
        }
        
        try:
            print(f"  🚀 执行命令: {' '.join(cmd)}")
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            result["success"] = process.returncode == 0
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            result["returncode"] = process.returncode
            
            if process.returncode == 0:
                print(f"  ✅ 测试通过")
                # 分析输出
                lines = process.stdout.split('\n')
                organized_count = 0
                for line in lines:
                    if "整理文件:" in line:
                        organized_count = int(line.split(":")[1].strip())
                
                result["organized_files"] = organized_count
            else:
                print(f"  ❌ 测试失败")
                print(f"    错误: {process.stderr[:100]}")
            
        except subprocess.TimeoutExpired:
            result["success"] = False
            result["error"] = "Timeout"
            print(f"  ⏰ 测试超时")
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            print(f"  ❌ 测试异常: {e}")
        
        # 保存结果
        self.test_results.append(result)
        self._save_result(result)
        
        return result
    
    def run_performance_test(self, test_name, file_count=100):
        """运行性能测试"""
        print(f"\n⚡ 运行性能测试: {test_name}")
        print("-" * 40)
        
        test_path = Path(f"perf_test_{file_count}")
        test_path.mkdir(exist_ok=True)
        
        print(f"  📁 创建 {file_count} 个测试文件...")
        for i in range(file_count):
            filename = f"test_file_{i:04d}.txt"
            filepath = test_path / filename
            filepath.write_text(f"Test content for file {i}")
        
        import time
        start_time = time.time()
        
        cmd = [
            sys.executable, "scripts/organize.py",
            "--path", str(test_path),
            "--preview"
        ]
        
        result = {
            "test_name": test_name,
            "test_time": datetime.now().isoformat(),
            "file_count": file_count,
            "command": " ".join(cmd)
        }
        
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            result["success"] = process.returncode == 0
            result["elapsed_time"] = elapsed
            result["files_per_second"] = file_count / elapsed if elapsed > 0 else 0
            result["stdout"] = process.stdout[:500]  # 只保存前500字符
            result["returncode"] = process.returncode
            
            print(f"  ⏱️  耗时: {elapsed:.2f}秒")
            print(f"  📊 速度: {result['files_per_second']:.1f} 文件/秒")
            
            if process.returncode == 0:
                print(f"  ✅ 性能测试通过")
            else:
                print(f"  ❌ 性能测试失败")
                
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            print(f"  ❌ 性能测试异常: {e}")
        
        self.test_results.append(result)
        self._save_result(result)
        
        # 清理测试文件
        import shutil
        shutil.rmtree(test_path, ignore_errors=True)
        
        return result
    
    def run_error_test(self, test_name, error_scenario):
        """运行错误场景测试"""
        print(f"\n🐛 运行错误测试: {test_name}")
        print("-" * 40)
        
        result = {
            "test_name": test_name,
            "test_time": datetime.now().isoformat(),
            "scenario": error_scenario
        }
        
        test_cases = {
            "invalid_path": ["--path", "/nonexistent/path"],
            "no_permission": ["--path", "/root"],  # 可能需要特殊权限
            "large_file": ["--path", "."],  # 需要先创建大文件
            "invalid_config": ["--path", ".", "--config", "invalid.json"]
        }
        
        if error_scenario not in test_cases:
            print(f"  ❌ 未知测试场景: {error_scenario}")
            return None
        
        cmd = [sys.executable, "scripts/organize.py"] + test_cases[error_scenario]
        result["command"] = " ".join(cmd)
        
        try:
            print(f"  🚀 执行命令: {' '.join(cmd)}")
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 错误测试期望返回非零代码
            result["success"] = process.returncode != 0
            result["returncode"] = process.returncode
            result["stderr"] = process.stderr
            
            if process.returncode != 0:
                print(f"  ✅ 错误处理正常 (返回码: {process.returncode})")
                print(f"     错误信息: {process.stderr[:100]}")
            else:
                print(f"  ⚠️  错误处理异常 (应该失败但成功了)")
                
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            print(f"  ❌ 错误测试异常: {e}")
        
        self.test_results.append(result)
        self._save_result(result)
        
        return result
    
    def _save_result(self, result):
        """保存测试结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_result_{result['test_name']}_{timestamp}.json"
        filepath = self.test_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"  💾 结果保存: {filepath}")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("📊 测试报告摘要")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.get("success", False))
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"通过率: {passed_tests/total_tests*100:.1f}%")
        
        # 性能统计
        perf_tests = [r for r in self.test_results if "files_per_second" in r]
        if perf_tests:
            avg_speed = sum(r["files_per_second"] for r in perf_tests) / len(perf_tests)
            print(f"平均处理速度: {avg_speed:.1f} 文件/秒")
        
        # 生成详细报告
        report_file = self.test_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 智能文件整理助手 - 测试报告\n\n")
            f.write(f"生成时间: {datetime.now().isoformat()}\n")
            f.write(f"测试总数: {total_tests}\n")
            f.write(f"通过测试: {passed_tests}\n")
            f.write(f"失败测试: {failed_tests}\n")
            f.write(f"通过率: {passed_tests/total_tests*100:.1f}%\n\n")
            
            f.write("## 详细结果\n\n")
            for i, result in enumerate(self.test_results, 1):
                f.write(f"### 测试 {i}: {result['test_name']}\n")
                f.write(f"- 时间: {result['test_time']}\n")
                f.write(f"- 状态: {'✅ 通过' if result.get('success') else '❌ 失败'}\n")
                if 'elapsed_time' in result:
                    f.write(f"- 耗时: {result['elapsed_time']:.2f}秒\n")
                if 'files_per_second' in result:
                    f.write(f"- 速度: {result['files_per_second']:.1f} 文件/秒\n")
                f.write(f"- 命令: `{result.get('command', 'N/A')}`\n")
                if 'error' in result:
                    f.write(f"- 错误: {result['error']}\n")
                f.write("\n")
        
        print(f"\n📄 详细报告已生成: {report_file}")
        return report_file

def main():
    runner = TestRunner()
    
    # 运行基础功能测试
    runner.run_basic_test("basic_functionality", "test_basic")
    
    # 运行性能测试
    runner.run_performance_test("performance_100_files", 100)
    runner.run_performance_test("performance_500_files", 500)
    
    # 运行错误测试
    runner.run_error_test("error_invalid_path", "invalid_path")
    runner.run_error_test("error_invalid_config", "invalid_config")
    
    # 生成报告
    runner.generate_report()
    
    print("\n🎉 所有测试完成!")
    print("💡 下一步: 分析测试结果，优化产品")

if __name__ == "__main__":
    main()