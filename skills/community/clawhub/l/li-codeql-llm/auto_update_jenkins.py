#!/usr/bin/env python3
"""
使用 Jenkins Script API 自动化更新 Pipeline
"""

import requests
from pathlib import Path
import json

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

print("=" * 60)
print("  Jenkins Pipeline 自动化更新")
print("=" * 60)
print()

# 读取 Jenkinsfile
jenkinsfile_path = Path('Jenkinsfile')
if not jenkinsfile_path.exists():
    print(f"❌ Jenkinsfile 不存在：{jenkinsfile_path}")
    exit(1)

with open(jenkinsfile_path, 'r', encoding='utf-8') as f:
    pipeline_script = f.read()

print(f"✅ 已读取 Jenkinsfile ({len(pipeline_script)} 字节)")
print()

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
print(f"✅ Crumb: {crumb_data['crumb'][:20]}...")
print()

# 使用 Script API 执行 Groovy 脚本
print(f"🔄 执行 Groovy 脚本更新 Pipeline...")

script_url = f"{jenkins_url}/scriptText"

# Groovy 脚本来更新 Pipeline
groovy_script = f"""
def jobName = '{job_name}'
def job = Jenkins.instance.getItemByFullName(jobName, org.jenkinsci.plugins.workflow.job.WorkflowJob.class)

if (job) {{
    println "✅ 找到任务：${{jobName}}"
    
    // 读取 Jenkinsfile
    def jenkinsfile = new File('/root/.openclaw/workspace/skills/codeql-llm-scanner/Jenkinsfile').text
    
    // 检查是否包含 mkdir -p
    if (jenkinsfile.contains('mkdir -p')) {{
        println "✅ Jenkinsfile 包含 mkdir -p 命令"
    }} else {{
        println "⚠️ Jenkinsfile 不包含 mkdir -p 命令"
    }}
    
    // 更新 Pipeline 定义
    def definition = new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(jenkinsfile, true)
    job.definition = definition
    job.save()
    
    println "✅ Pipeline 已更新"
    println "✅ 下次构建将使用新脚本"
}} else {{
    println "❌ 任务不存在：${{jobName}}"
    System.exit(1)
}}
"""

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
headers.update(crumb_header)

data = {
    'script': groovy_script
}

try:
    response = requests.post(
        script_url,
        data=data,
        headers=headers,
        auth=(jenkins_user, jenkins_token),
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅ Groovy 脚本执行成功")
        print()
        
        # 解析响应
        response_text = response.text
        if 'Pipeline 已更新' in response_text:
            print("✅ Pipeline 更新成功！")
            print()
            print("📋 更新信息:")
            print(f"   任务：{job_name}")
            print(f"   URL: {jenkins_url}/job/{job_name}/")
            print()
            print("💡 下一步:")
            print(f"   1. 访问：{jenkins_url}/job/{job_name}/")
            print(f"   2. 点击 '立即构建' (Build Now)")
            print(f"   3. 查看控制台输出")
            
            # 触发构建
            print()
            print("🚀 自动触发构建...")
            
            build_url = f"{jenkins_url}/job/{job_name}/build"
            build_data = {
                'json': json.dumps({
                    'parameter': [
                        {'name': 'SCAN_TARGET', 'value': '/root/devsecops-python-web'},
                        {'name': 'CODEQL_LANGUAGE', 'value': 'python'},
                        {'name': 'CODEQL_SUITE', 'value': 'python-security-extended.qls'},
                        {'name': 'OUTPUT_DIR', 'value': './codeql-scan-output'},
                        {'name': 'SECURITY_CHECK', 'value': 'true'}
                    ]
                })
            }
            
            build_response = requests.post(
                build_url,
                data=build_data,
                headers=headers,
                auth=(jenkins_user, jenkins_token),
                timeout=30
            )
            
            if build_response.status_code in [200, 201, 302]:
                print("✅ 构建已触发！")
                print()
                print("⏳ 等待构建完成...")
                
                # 等待构建
                import time
                time.sleep(5)
                
                # 获取最新构建号
                api_url = f"{jenkins_url}/job/{job_name}/api/json"
                api_response = requests.get(api_url, auth=(jenkins_user, jenkins_token), timeout=10)
                
                if api_response.status_code == 200:
                    api_data = api_response.json()
                    builds = api_data.get('builds', [])
                    if builds:
                        latest_build = builds[0]
                        build_number = latest_build.get('number')
                        print(f"📋 构建号：#{build_number}")
                        print()
                        print(f"📄 查看构建：{jenkins_url}/job/{job_name}/{build_number}/console")
                    else:
                        print("⚠️ 未找到构建记录")
            else:
                print(f"⚠️ 构建触发响应：{build_response.status_code}")
        else:
            print("⚠️ 响应中未找到成功信息")
            print(f"响应：{response_text[:500]}")
    else:
        print(f"❌ 脚本执行失败：{response.status_code}")
        print(f"响应：{response.text[:500]}")
        
except Exception as e:
    print(f"❌ 异常：{e}")
    import traceback
    traceback.print_exc()
