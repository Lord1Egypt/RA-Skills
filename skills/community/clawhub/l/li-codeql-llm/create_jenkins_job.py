#!/usr/bin/env python3
"""
Jenkins Pipeline 创建工具
创建或更新 Jenkins CodeQL 扫描任务
"""

import os
import sys
import requests
from pathlib import Path
from config_loader import get_config


def get_crumb(jenkins_url, user, token):
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
        print(f"⚠️  获取 crumb 失败 / Get crumb failed: {e}")
    return {}


def create_jenkins_job(config):
    """创建或更新 Jenkins Pipeline 任务"""
    
    jenkins_url = config.get('JENKINS_URL', 'http://localhost:8080')
    jenkins_user = config.get('JENKINS_USER', 'devops')
    jenkins_token = config.get('JENKINS_TOKEN', '')
    job_name = config.get('JENKINS_JOB_NAME', 'codeql-security-scan')
    scan_target = config.get('JENKINS_SCAN_TARGET', '/root/devsecops-python-web')
    
    # Jenkinsfile 路径
    jenkinsfile_path = Path(__file__).parent / 'Jenkinsfile'
    
    if not jenkinsfile_path.exists():
        print(f"❌ Jenkinsfile 不存在 / Jenkinsfile not found: {jenkinsfile_path}")
        return False
    
    # 读取 Jenkinsfile
    with open(jenkinsfile_path, 'r', encoding='utf-8') as f:
        pipeline_script = f.read()
    
    # 获取 CSRF crumb
    crumb_headers = get_crumb(jenkins_url, jenkins_user, jenkins_token)
    
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
        # 检查任务是否存在
        response = requests.get(check_url, auth=(jenkins_user, jenkins_token), timeout=10)
        
        if response.status_code == 200:
            print(f"ℹ️  任务已存在，更新配置 / Job exists, updating config: {job_name}")
            # 更新现有任务
            update_url = f"{jenkins_url}/job/{job_name}/config.xml"
            response = requests.post(update_url, 
                                    data=job_config_xml.encode('utf-8'),
                                    headers=headers,
                                    auth=(jenkins_user, jenkins_token),
                                    timeout=30)
        else:
            print(f"📦 创建新任务 / Creating new job: {job_name}")
            # 创建新任务
            create_url = f"{jenkins_url}/createItem?name={job_name}"
            response = requests.post(create_url,
                                    data=job_config_xml.encode('utf-8'),
                                    headers=headers,
                                    auth=(jenkins_user, jenkins_token),
                                    timeout=30)
        
        if response.status_code in [200, 201]:
            print(f"✅ Jenkins 任务创建成功 / Jenkins job created successfully")
            print(f"\n📋 任务信息 / Job Info:")
            print(f"   名称 / Name: {job_name}")
            print(f"   URL: {jenkins_url}/job/{job_name}")
            print(f"   默认扫描目录 / Default Scan Target: {scan_target}")
            print(f"\n💡 下一步 / Next steps:")
            print(f"   1. 访问 Jenkins: {jenkins_url}/job/{job_name}")
            print(f"   2. 点击 '立即构建' (Build Now)")
            print(f"   3. 可以修改 SCAN_TARGET 参数后构建")
            return True
        else:
            print(f"❌ 创建失败 / Failed: {response.status_code}")
            print(f"响应 / Response: {response.text[:300]}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 无法连接 Jenkins / Cannot connect to Jenkins: {e}")
        print(f"\n💡 请检查:")
        print(f"   1. Jenkins 是否运行：curl {jenkins_url}")
        print(f"   2. 用户名密码是否正确")
        print(f"   3. Jenkins URL 是否正确")
        return False
    except Exception as e:
        print(f"❌ 异常 / Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("  Jenkins Pipeline 创建工具")
    print("  Jenkins Pipeline Creator")
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
    
    # 创建任务
    success = create_jenkins_job(config)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
