#!/usr/bin/env python3
"""
MeterSphere Skills 安装验证脚本

此脚本帮助用户验证技能安装的正确性和安全性配置。
运行前请确保已设置必要的环境变量。
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def print_check(description, status, details=None):
    """打印检查结果"""
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {description}")
    if details:
        print(f"   {details}")

def check_environment_variables():
    """检查环境变量"""
    print_header("1. 环境变量检查")
    
    required_vars = [
        'METERSPHERE_BASE_URL',
        'METERSPHERE_ACCESS_KEY', 
        'METERSPHERE_SECRET_KEY'
    ]
    
    optional_vars = [
        'METERSPHERE_PROJECT_ID',
        'METERSPHERE_ORGANIZATION_ID',
        'METERSPHERE_HEADERS_JSON',
        'METERSPHERE_PROTOCOLS_JSON',
        'METERSPHERE_DEFAULT_TEMPLATE_ID',
        'METERSPHERE_DEFAULT_VERSION_ID'
    ]
    
    # 检查必需变量
    missing_required = []
    for var in required_vars:
        if var in os.environ and os.environ[var]:
            print_check(f"{var} 已设置", True, f"值: {os.environ[var][:10]}...")
        else:
            print_check(f"{var} 未设置", False)
            missing_required.append(var)
    
    # 检查可选变量
    print("\n可选环境变量:")
    for var in optional_vars:
        if var in os.environ and os.environ[var]:
            print_check(f"{var} 已设置", True, f"值: {os.environ[var][:20]}...")
        else:
            print_check(f"{var} 未设置", True, "（可选）")
    
    # 检查硬编码ID覆盖
    print("\n硬编码ID覆盖检查:")
    if 'METERSPHERE_DEFAULT_TEMPLATE_ID' in os.environ:
        print_check("模板ID覆盖已设置", True, "将避免使用硬编码值")
    else:
        print_check("模板ID覆盖未设置", False, "警告：将使用硬编码模板ID")
    
    if 'METERSPHERE_DEFAULT_VERSION_ID' in os.environ:
        print_check("版本ID覆盖已设置", True, "将避免使用硬编码值")
    else:
        print_check("版本ID覆盖未设置", False, "警告：将使用硬编码版本ID")
    
    return len(missing_required) == 0

def check_binaries():
    """检查必需的二进制文件"""
    print_header("2. 二进制文件检查")
    
    binaries = ['python3', 'openssl', 'curl']
    all_ok = True
    
    for binary in binaries:
        try:
            result = subprocess.run(
                ['which', binary],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # 获取版本信息
                version_cmd = [binary, '--version']
                if binary == 'openssl':
                    version_cmd = ['openssl', 'version']
                
                version_result = subprocess.run(
                    version_cmd,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                version = version_result.stdout.split('\n')[0][:50]
                print_check(f"{binary} 已安装", True, f"路径: {result.stdout.strip()}\n   版本: {version}")
            else:
                print_check(f"{binary} 未找到", False)
                all_ok = False
        except Exception as e:
            print_check(f"{binary} 检查失败", False, f"错误: {str(e)}")
            all_ok = False
    
    return all_ok

def check_env_file():
    """检查.env文件"""
    print_header("3. .env文件检查")
    
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / '.env'
    env_example = skill_dir / '.env.example'
    
    if env_file.exists():
        print_check(".env文件存在", True, f"路径: {env_file}")
        
        # 检查文件权限（仅限Unix）
        if hasattr(os, 'stat'):
            stat_info = os.stat(env_file)
            mode = stat_info.st_mode & 0o777
            if mode <= 0o600:
                print_check(".env文件权限安全", True, f"权限: {oct(mode)}")
            else:
                print_check(".env文件权限不安全", False, f"权限: {oct(mode)} - 建议设置为600")
        
        # 检查文件内容
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                print_check(f".env文件包含{len(lines)}个配置项", True)
                
                # 检查是否有明显的敏感信息泄露
                sensitive_patterns = ['password', 'secret', 'token', 'key']
                for line in lines:
                    for pattern in sensitive_patterns:
                        if pattern in line.lower() and '=' in line:
                            var_name = line.split('=')[0].strip()
                            if var_name not in ['METERSPHERE_SECRET_KEY', 'METERSPHERE_ACCESS_KEY']:
                                print_check(f"发现可能的敏感信息: {var_name}", False, "请确认是否必要")
        except Exception as e:
            print_check("读取.env文件失败", False, f"错误: {str(e)}")
    else:
        print_check(".env文件不存在", False, "请从.env.example创建")
    
    if env_example.exists():
        print_check(".env.example模板存在", True, f"路径: {env_example}")
    else:
        print_check(".env.example模板不存在", False)
    
    return env_file.exists()

def check_skill_metadata():
    """检查技能元数据"""
    print_header("4. 技能元数据检查")
    
    skill_dir = Path(__file__).parent.parent
    metadata_file = skill_dir / 'skill-metadata.json'
    
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            print_check("skill-metadata.json存在", True)
            
            # 检查必需字段
            required_fields = ['name', 'description', 'requiredEnvVars', 'requiredBinaries']
            for field in required_fields:
                if field in metadata:
                    print_check(f"{field}字段存在", True)
                else:
                    print_check(f"{field}字段缺失", False)
            
            # 检查环境变量配置
            if 'requiredEnvVars' in metadata:
                required_vars = metadata['requiredEnvVars']
                print_check(f"元数据要求{len(required_vars)}个必需环境变量", True)
                
                # 验证与实际环境变量的一致性
                missing_in_env = []
                for var in required_vars:
                    if var not in os.environ or not os.environ[var]:
                        missing_in_env.append(var)
                
                if missing_in_env:
                    print_check("环境变量与元数据不匹配", False, f"缺失: {', '.join(missing_in_env)}")
                else:
                    print_check("环境变量与元数据匹配", True)
            
            # 检查安全说明
            if 'securityNotes' in metadata:
                print_check(f"包含{len(metadata['securityNotes'])}条安全说明", True)
            
        except json.JSONDecodeError as e:
            print_check("skill-metadata.json格式错误", False, f"错误: {str(e)}")
            return False
        except Exception as e:
            print_check("读取skill-metadata.json失败", False, f"错误: {str(e)}")
            return False
    else:
        print_check("skill-metadata.json不存在", False)
        return False
    
    return True

def check_network_connectivity():
    """检查网络连接"""
    print_header("5. 网络连接检查")
    
    base_url = os.environ.get('METERSPHERE_BASE_URL', '')
    if not base_url:
        print_check("METERSPHERE_BASE_URL未设置", False, "无法测试连接")
        return False
    
    try:
        # 测试基本连接
        print(f"测试连接到: {base_url}")
        
        # 使用curl测试连接
        curl_cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-I', f'{base_url}/system/status', '--connect-timeout', '10']
        
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0 and result.stdout.strip().isdigit():
            status_code = int(result.stdout.strip())
            if status_code == 200:
                print_check("MeterSphere连接成功", True, f"HTTP状态码: {status_code}")
                return True
            else:
                print_check("MeterSphere连接异常", False, f"HTTP状态码: {status_code}")
                return False
        else:
            print_check("MeterSphere连接失败", False, f"错误: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print_check("MeterSphere连接超时", False, "请检查网络或BASE_URL配置")
        return False
    except Exception as e:
        print_check("网络连接测试失败", False, f"错误: {str(e)}")
        return False

def check_hardcoded_ids():
    """检查硬编码ID"""
    print_header("6. 硬编码ID检查")
    
    scripts_dir = Path(__file__).parent
    hardcoded_ids = {
        '1163437937827840': '项目ID',
        '1163437937827890': '模板ID', 
        '1163437937827887': '版本ID'
    }
    
    found_ids = {}
    
    # 搜索脚本中的硬编码ID
    for script_file in scripts_dir.glob('*.py'):
        try:
            with open(script_file, 'r') as f:
                content = f.read()
                for id_value, id_type in hardcoded_ids.items():
                    if id_value in content:
                        if id_type not in found_ids:
                            found_ids[id_type] = []
                        found_ids[id_type].append(script_file.name)
        except Exception:
            pass
    
    for script_file in scripts_dir.glob('*.sh'):
        try:
            with open(script_file, 'r') as f:
                content = f.read()
                for id_value, id_type in hardcoded_ids.items():
                    if id_value in content:
                        if id_type not in found_ids:
                            found_ids[id_type] = []
                        found_ids[id_type].append(script_file.name)
        except Exception:
            pass
    
    if found_ids:
        print_check("发现硬编码ID", True if 'METERSPHERE_DEFAULT_TEMPLATE_ID' in os.environ and 'METERSPHERE_DEFAULT_VERSION_ID' in os.environ else False)
        for id_type, files in found_ids.items():
            file_list = ', '.join(set(files))
            print(f"   {id_type}: 在 {file_list} 中发现")
        
        # 检查是否有环境变量覆盖
        if 'METERSPHERE_DEFAULT_TEMPLATE_ID' in os.environ:
            print_check("模板ID覆盖已设置", True)
        else:
            print_check("模板ID覆盖未设置", False, "警告：数据可能被错误归属")
        
        if 'METERSPHERE_DEFAULT_VERSION_ID' in os.environ:
            print_check("版本ID覆盖已设置", True)
        else:
            print_check("版本ID覆盖未设置", False, "警告：数据可能被错误归属")
    else:
        print_check("未发现硬编码ID", True)
    
    return 'METERSPHERE_DEFAULT_TEMPLATE_ID' in os.environ and 'METERSPHERE_DEFAULT_VERSION_ID' in os.environ

def main():
    """主函数"""
    print_header("MeterSphere Skills 安装验证")
    print("此脚本将验证技能安装的正确性和安全性配置。")
    print("请确保已设置必要的环境变量。")
    
    results = {
        '环境变量': check_environment_variables(),
        '二进制文件': check_binaries(),
        '.env文件': check_env_file(),
        '技能元数据': check_skill_metadata(),
        '网络连接': check_network_connectivity(),
        '硬编码ID': check_hardcoded_ids()
    }
    
    print_header("验证结果摘要")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"通过检查: {passed}/{total}")
    
    for check_name, passed_check in results.items():
        status = "✅ 通过" if passed_check else "❌ 失败"
        print(f"{status} {check_name}")
    
    print_header("后续步骤")
    
    if passed == total:
        print("✅ 所有检查通过！技能已正确安装。")
        print("建议:")
        print("1. 在非生产环境进行测试运行")
        print("2. 监控网络流量确认只连接到预期的BASE_URL")
        print("3. 验证数据归属正确性")
    else:
        print("⚠️  部分检查未通过，请解决以下问题:")
        for check_name, passed_check in results.items():
            if not passed_check:
                print(f"  - {check_name}")
        
        print("\n必须解决的问题:")
        if not results['环境变量']:
            print("  - 设置所有必需的环境变量")
        if not results['二进制文件']:
            print("  - 安装缺失的二进制文件 (python3, openssl, curl)")
        if not results['网络连接']:
            print("  - 检查网络连接和BASE_URL配置")
        
        print("\n建议解决的问题:")
        if not results['硬编码ID']:
            print("  - 设置METERSPHERE_DEFAULT_TEMPLATE_ID和METERSPHERE_DEFAULT_VERSION_ID环境变量")
        if not results['.env文件']:
            print("  - 创建.env文件并设置适当权限")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n验证被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n验证过程中发生错误: {str(e)}")
        sys.exit(1)