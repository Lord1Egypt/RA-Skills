#!/usr/bin/env python3
"""
Jenkins Pipeline 自动创建工具
自动获取 API Token 并创建 Pipeline 任务
"""

import os
import sys
import requests
from pathlib import Path
from config_loader import get_config


def get_jenkins_crumb(jenkins_url, user, token):
    """获取 Jenkins CSRF crumb"""
    try:
        response = requests.get(
            f"{jenkins_url}/crumbIssuer/api/json",
            auth=(user, token),
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return {
                data['crumbRequestField']: data['crumb']
            }
    except Exception as e:
        print(f"⚠️  获取 crumb 失败：{e}")
    return {}


def generate_api_token(jenkins_url, user, password, token_name="CodeQL_Scanner"):
    """
    生成 Jenkins API Token
    
    注意：这需要管理员权限或使用现有密码
    对于自动化，建议使用已有的 API Token
    """
    print(f"💡 提示：自动生成 API Token 需要管理员权限")
    print(f"   请手动生成或提供现有的 API Token")
    print(f"\n📋 手动生成步骤:")
    print(f"   1. 访问：{jenkins_url}/user/{user}/security")
    print(f"   2. 登录：{user} / {'*' * len(password)}")
    print(f"   3. 点击 'Add new Token'")
    print(f"   4. 输入名称：{token_name}")
    print(f"   5. 点击 'Generate'")
    print(f"   6. 复制生成的 Token")
    print(f"   7. 更新 .env 文件：JENKINS_TOKEN=<your-token>")
    return None


def create_jenkins_pipeline(config):
    """创建 Jenkins Pipeline 任务"""
    
    jenkins_url = config.get('JENKINS_URL')
    jenkins_user = config.get('JENKINS_USER')
    jenkins_token = config.get('JENKINS_TOKEN')
    job_name = config.get('JENKINS_JOB_NAME')
    scan_target = config.get('JENKINS_SCAN_TARGET')
    
    # Jenkinsfile 路径
    jenkinsfile_path = Path(__file__).parent / 'Jenkinsfile'
    
    if not jenkinsfile_path.exists():
        print(f"❌ Jenkinsfile 不存在：{jenkinsfile_path}")
        return False
    
    # 读取 Jenkinsfile
    with open(jenkinsfile_path, 'r', encoding='utf-8') as f:
        pipeline_script = f.read()
    
    # 获取 CSRF crumb
    print("🔑 获取 Jenkins crumb...")
    crumb_headers = get_jenkins_crumb(jenkins_url, jenkins_user, jenkins_token)
    
    if not crumb_headers:
        print("❌ 无法获取 crumb，请检查用户名和密码/Token")
        return False
    
    print(f"✅ Crumb 获取成功")
    
    headers = {
        'Content-Type': 'application/xml'
    }
    headers.update(crumb_headers)
    
    # 创建任务的 XML
    job_config_xml = f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>CodeQL 安全扫描器 - 支持参数化构建，可指定扫描目录</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>SCAN_TARGET</name>
          <defaultValue>{scan_target}</defaultValue>
          <description>要扫描的项目目录 / Project directory to scan</description>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>CODEQL_LANGUAGE</name>
          <defaultValue>python</defaultValue>
          <description>编程语言 / Programming language</description>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>CODEQL_SUITE</name>
          <defaultValue>python-security-extended.qls</defaultValue>
          <description>查询套件 / Query suite</description>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
    <script>{pipeline_script}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
"""
    
    # 检查任务是否已存在
    check_url = f"{jenkins_url}/job/{job_name}/api/json"
    
    try:
        print(f"🔍 检查任务是否存在：{job_name}...")
        response = requests.get(check_url, auth=(jenkins_user, jenkins_token), timeout=10)
        
        if response.status_code == 200:
            print(f"✅ 任务已存在，跳过创建")
            print(f"   URL: {jenkins_url}/job/{job_name}")
            
            # 显示任务信息
            data = response.json()
            print(f"\n📋 任务信息:")
            print(f"   名称：{data.get('name')}")
            print(f"   描述：{data.get('description', 'N/A')[:60]}...")
            print(f"   可构建：{data.get('buildable', False)}")
            print(f"   最后构建：{data.get('lastBuild', {}).get('number', '无')}")
            
            # 询问是否更新配置
            print(f"\n💡 如需更新配置，请手动修改或重新创建任务")
            return True
        else:
            print(f"📦 创建新任务：{job_name}...")
            create_url = f"{jenkins_url}/createItem?name={job_name}"
            response = requests.post(create_url,
                                    data=job_config_xml.encode('utf-8'),
                                    headers=headers,
                                    auth=(jenkins_user, jenkins_token),
                                    timeout=30)
        
        if response.status_code in [200, 201]:
            print(f"\n✅ Jenkins Pipeline 创建成功！")
            print(f"\n📋 任务信息:")
            print(f"   名称：{job_name}")
            print(f"   URL: {jenkins_url}/job/{job_name}")
            print(f"   默认扫描目录：{scan_target}")
            print(f"\n💡 下一步:")
            print(f"   1. 访问：{jenkins_url}/job/{job_name}")
            print(f"   2. 点击 '立即构建' (Build Now)")
            print(f"   3. 可以修改参数后构建")
            return True
        else:
            print(f"❌ 创建失败：{response.status_code}")
            print(f"响应：{response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        import traceback
        traceback.print_exc()
        return False


def check_env_token(config):
    """检查 .env 中的 Token 配置"""
    
    jenkins_token = config.get('JENKINS_TOKEN', '')
    
    # 检查是否是密码（短字符串）还是 API Token（长字符串）
    if len(jenkins_token) < 20:
        print(f"⚠️  警告：当前 JENKINS_TOKEN 可能是密码而不是 API Token")
        print(f"   当前值：{'*' * len(jenkins_token)}")
        print(f"   API Token 通常长度 > 30 字符")
        print(f"\n💡 建议生成 API Token 以获得更好的安全性")
        return False
    else:
        print(f"✅ JENKINS_TOKEN 看起来是有效的 API Token")
        return True


def main():
    """主函数"""
    print("=" * 60)
    print("  Jenkins Pipeline 自动创建工具")
    print("  自动化配置和创建 CodeQL 扫描 Pipeline")
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
    
    # 检查 Token
    print("🔍 检查 .env 配置...")
    token_valid = check_env_token(config)
    print()
    
    # 创建 Pipeline
    print("🚀 开始创建 Jenkins Pipeline...")
    success = create_jenkins_pipeline(config)
    
    if success:
        print("\n" + "=" * 60)
        print("  ✅ 创建完成！")
        print("=" * 60)
        
        # 尝试触发一次构建
        print("\n🧪 是否要立即运行一次扫描测试？")
        print(f"   扫描目标：{config.get('JENKINS_SCAN_TARGET')}")
        print(f"\n   访问：{config.get('JENKINS_URL')}/job/{config.get('JENKINS_JOB_NAME')}/build")
    else:
        print("\n" + "=" * 60)
        print("  ❌ 创建失败")
        print("=" * 60)
        
        if not token_valid:
            print("\n💡 建议:")
            print("   1. 生成 Jenkins API Token")
            print("   2. 更新 .env 文件")
            print("   3. 重新运行此脚本")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
