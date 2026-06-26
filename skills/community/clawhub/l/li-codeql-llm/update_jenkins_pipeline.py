#!/usr/bin/env python3
"""
自动更新 Jenkins Pipeline 配置
添加 mkdir -p 命令来创建输出目录
"""

import requests
from pathlib import Path

# 加载配置
config_file = Path('.env')
config = {}
if config_file.exists():
    with open(config_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

jenkins_url = config.get('JENKINS_URL', 'http://localhost:8080')
jenkins_user = config.get('JENKINS_USER', 'devops')
jenkins_token = config.get('JENKINS_TOKEN', '')
job_name = config.get('JENKINS_JOB_NAME', 'codeql-security-scan')

# 获取 crumb
print("🔑 获取 Jenkins crumb...")
crumb_response = requests.get(
    f"{jenkins_url}/crumbIssuer/api/json",
    auth=(jenkins_user, jenkins_token),
    timeout=10
)

if crumb_response.status_code != 200:
    print(f"❌ 获取 crumb 失败：{crumb_response.status_code}")
    exit(1)

crumb_data = crumb_response.json()
crumb_header = {crumb_data['crumbRequestField']: crumb_data['crumb']}
print(f"✅ Crumb 获取成功")

# 读取 Jenkinsfile
jenkinsfile_path = Path('Jenkinsfile')
if not jenkinsfile_path.exists():
    print(f"❌ Jenkinsfile 不存在：{jenkinsfile_path}")
    exit(1)

with open(jenkinsfile_path, 'r', encoding='utf-8') as f:
    pipeline_script = f.read()

print(f"📖 已读取 Jenkinsfile ({len(pipeline_script)} 字节)")

# 检查是否包含 mkdir -p
if 'mkdir -p' in pipeline_script:
    print("✅ Jenkinsfile 已包含 mkdir -p 命令")
else:
    print("⚠️  Jenkinsfile 不包含 mkdir -p 命令")
    print("   请先更新 Jenkinsfile")
    exit(1)

# 创建任务配置 XML
job_config_xml = f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>CodeQL 安全扫描器 - 支持参数化构建，可指定扫描目录</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>SCAN_TARGET</name>
          <defaultValue>{config.get('JENKINS_SCAN_TARGET', '/root/devsecops-python-web')}</defaultValue>
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
        <hudson.model.StringParameterDefinition>
          <name>OUTPUT_DIR</name>
          <defaultValue>./codeql-scan-output</defaultValue>
          <description>输出目录 / Output directory</description>
        </hudson.model.StringParameterDefinition>
        <hudson.model.BooleanParameterDefinition>
          <name>SECURITY_CHECK</name>
          <defaultValue>true</defaultValue>
          <description>扫描前安全检查 / Pre-scan security check</description>
        </hudson.model.BooleanParameterDefinition>
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

# 更新任务配置
print(f"\n🔄 更新 Jenkins Pipeline: {job_name}...")

update_url = f"{jenkins_url}/job/{job_name}/config.xml"

headers = {
    'Content-Type': 'application/xml'
}
headers.update(crumb_header)

response = requests.post(
    update_url,
    data=job_config_xml.encode('utf-8'),
    headers=headers,
    auth=(jenkins_user, jenkins_token),
    timeout=30
)

if response.status_code == 200:
    print(f"✅ Pipeline 更新成功！")
    print(f"\n📋 任务信息:")
    print(f"   名称：{job_name}")
    print(f"   URL: {jenkins_url}/job/{job_name}")
    print(f"\n💡 下一步:")
    print(f"   1. 访问：{jenkins_url}/job/{job_name}")
    print(f"   2. 点击 '立即构建' (Build Now)")
    print(f"   3. 查看控制台输出")
else:
    print(f"❌ 更新失败：{response.status_code}")
    print(f"响应：{response.text[:300]}")
    exit(1)
