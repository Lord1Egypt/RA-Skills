#!/usr/bin/env python3
"""
运行测试并检查 Jenkins 流水线
智能检测：如果流水线已存在，不重复创建
"""

import os
import sys
import requests
import subprocess
from pathlib import Path
from config_loader import get_config


def check_jenkins_pipeline(config):
    """检查 Jenkins Pipeline 是否存在"""
    
    jenkins_url = config.get('JENKINS_URL')
    jenkins_user = config.get('JENKINS_USER')
    jenkins_token = config.get('JENKINS_TOKEN')
    job_name = config.get('JENKINS_JOB_NAME')
    
    check_url = f"{jenkins_url}/job/{job_name}/api/json"
    
    try:
        print(f"🔍 检查 Jenkins Pipeline: {job_name}...")
        response = requests.get(check_url, auth=(jenkins_user, jenkins_token), timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pipeline 已存在")
            print(f"\n📋 任务信息:")
            print(f"   名称：{data.get('name')}")
            print(f"   URL: {check_url}")
            print(f"   可构建：{data.get('buildable', False)}")
            print(f"   最后构建：{data.get('lastBuild', {}).get('number', '无')}")
            print(f"   构建次数：{data.get('builds', []) and len(data.get('builds', [])) or 0}")
            return True
        else:
            print(f"⚠️  Pipeline 不存在")
            return False
            
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        return False


def create_if_needed(config):
    """如果 Pipeline 不存在，则创建"""
    
    from create_jenkins_pipeline import create_jenkins_pipeline
    
    print("\n📦 开始创建 Pipeline...")
    return create_jenkins_pipeline(config)


def run_local_test(config):
    """运行本地测试扫描"""
    
    print("\n" + "=" * 60)
    print("  运行本地测试扫描")
    print("=" * 60)
    
    script_dir = Path(__file__).parent
    test_script = script_dir / "test_scan.sh"
    
    if not test_script.exists():
        print("❌ 测试脚本不存在")
        return False
    
    try:
        result = subprocess.run(
            ["bash", str(test_script)],
            cwd=str(script_dir),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ 本地测试完成")
            return True
        else:
            print("\n❌ 本地测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False


def trigger_jenkins_build(config):
    """触发 Jenkins 构建"""
    
    jenkins_url = config.get('JENKINS_URL')
    jenkins_user = config.get('JENKINS_USER')
    jenkins_token = config.get('JENKINS_TOKEN')
    job_name = config.get('JENKINS_JOB_NAME')
    scan_target = config.get('JENKINS_SCAN_TARGET')
    
    print("\n" + "=" * 60)
    print("  触发 Jenkins 构建")
    print("=" * 60)
    
    build_url = f"{jenkins_url}/job/{job_name}/build"
    
    # 参数化构建
    params = {
        'SCAN_TARGET': scan_target,
        'CODEQL_LANGUAGE': 'python',
        'CODEQL_SUITE': 'python-security-extended.qls'
    }
    
    json_data = {
        'parameter': [
            {'name': key, 'value': value}
            for key, value in params.items()
        ]
    }
    
    import json
    try:
        print(f"📤 触发构建...")
        print(f"   扫描目标：{scan_target}")
        print(f"   语言：python")
        
        response = requests.post(
            build_url,
            auth=(jenkins_user, jenkins_token),
            data={
                'json': json.dumps(json_data)
            },
            timeout=30
        )
        
        if response.status_code in [200, 201, 302]:
            print(f"✅ 构建已触发")
            print(f"\n💡 查看构建:")
            print(f"   {jenkins_url}/job/{job_name}/")
            return True
        else:
            print(f"⚠️  构建触发响应：{response.status_code}")
            # 即使返回 302 也是成功的（重定向）
            if response.status_code == 302:
                print(f"✅ 构建已触发（重定向到构建页面）")
                return True
            return False
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("  Jenkins Pipeline 测试工具")
    print("  智能检测 + 自动创建 + 运行测试")
    print("=" * 60)
    print()
    
    # 加载配置
    config = get_config()
    
    # 验证必要配置
    if not config.get('JENKINS_URL'):
        print("❌ JENKINS_URL 未配置")
        sys.exit(1)
    
    if not config.get('JENKINS_TOKEN'):
        print("❌ JENKINS_TOKEN 未配置")
        sys.exit(1)
    
    # 1. 检查 Pipeline 是否存在
    print("📋 步骤 1: 检查 Jenkins Pipeline")
    print("-" * 60)
    pipeline_exists = check_jenkins_pipeline(config)
    
    # 2. 如果不存在，创建它
    if not pipeline_exists:
        print("\n📋 步骤 2: 创建 Pipeline")
        print("-" * 60)
        create_if_needed(config)
    else:
        print("\n✅ Pipeline 已存在，跳过创建")
    
    # 3. 运行本地测试
    print("\n📋 步骤 3: 运行本地测试")
    print("-" * 60)
    run_local_test(config)
    
    # 4. 触发 Jenkins 构建
    print("\n📋 步骤 4: 触发 Jenkins 构建")
    print("-" * 60)
    trigger_jenkins_build(config)
    
    # 5. 总结
    print("\n" + "=" * 60)
    print("  测试完成总结")
    print("=" * 60)
    print()
    print("✅ 所有步骤完成！")
    print()
    print("📋 查看结果:")
    print(f"   Jenkins: {config.get('JENKINS_URL')}/job/{config.get('JENKINS_JOB_NAME')}/")
    print(f"   本地报告：ls -lh test-*/")
    print()
    
    sys.exit(0)


if __name__ == '__main__':
    main()
