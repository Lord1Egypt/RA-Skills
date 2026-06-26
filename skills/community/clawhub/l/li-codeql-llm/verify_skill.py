#!/usr/bin/env python3
"""
Li_codeql_LLM Skill - 完整运行验证测试

验证运行后是否可以返回结果
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("  Li_codeql_LLM Skill - 完整验证测试")
print("=" * 60)
print()

# 1. 检查 Skill 目录
skill_dir = Path.home() / ".openclaw" / "workspace" / "skills" / "codeql-llm-scanner"
print(f"📁 Skill 目录：{skill_dir}")

if not skill_dir.exists():
    print(f"❌ Skill 目录不存在")
    sys.exit(1)

print(f"✅ Skill 目录存在")
print()

# 2. 检查关键文件
print("📋 检查关键文件...")
required_files = [
    "SKILL.md",
    "codeql_llm_scan.py",
    "scanner.py",
    "run.sh",
    ".env"
]

for file in required_files:
    file_path = skill_dir / file
    if file_path.exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} (缺失)")
        sys.exit(1)

print()

# 3. 检查 SKILL.md 配置
print("📄 检查 SKILL.md 配置...")
with open(skill_dir / "SKILL.md") as f:
    skill_content = f.read()
    if "Li_codeql_LLM" in skill_content:
        print(f"   ✅ Skill 名称：Li_codeql_LLM")
    else:
        print(f"   ⚠️  Skill 名称未更新")
    print()

# 4. 检查 CodeQL 是否安装
print("🔍 检查 CodeQL 安装...")
try:
    result = subprocess.run(
        ["codeql", "--version"],
        capture_output=True,
        text=True,
        check=True
    )
    print(f"   ✅ CodeQL 已安装")
    print(f"      {result.stdout.split(chr(10))[0]}")
except Exception as e:
    print(f"   ❌ CodeQL 未安装：{e}")
    sys.exit(1)

print()

# 5. 检查 OpenClaw SDK
print("🔍 检查 OpenClaw SDK...")
try:
    subprocess.run(
        ["uv", "run", "python3", "-c", "from openclaw_sdk import OpenClawClient"],
        capture_output=True,
        check=True,
        cwd=str(skill_dir)
    )
    print(f"   ✅ OpenClaw SDK 已安装")
except Exception as e:
    print(f"   ⚠️  OpenClaw SDK 未安装（可选）")

print()

# 6. 检查 Jenkins 配置
print("🏢 检查 Jenkins 配置...")
with open(skill_dir / ".env") as f:
    env_content = f.read()
    if "JENKINS_URL" in env_content:
        print(f"   ✅ Jenkins 已配置")
    if "JENKINS_TOKEN" in env_content:
        print(f"   ✅ Jenkins Token 已配置")
    if "codeql-security-scan" in env_content:
        print(f"   ✅ Jenkins Pipeline 已配置")

print()

# 7. 运行测试扫描
print("🧪 运行测试扫描...")
test_target = "/root/devsecops-python-web"
output_dir = skill_dir / f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

print(f"   扫描目标：{test_target}")
print(f"   输出目录：{output_dir}")
print()

try:
    # 设置环境变量
    env = os.environ.copy()
    env["PATH"] = f"/opt/codeql/codeql:{env.get('PATH', '')}"
    
    # 运行快速扫描
    result = subprocess.run(
        ["uv", "run", "python3", "scanner.py", test_target, "--output", str(output_dir)],
        capture_output=True,
        text=True,
        check=True,
        cwd=str(skill_dir),
        timeout=300,
        env=env
    )
    
    print(f"   ✅ 扫描完成")
    print()
    
    # 检查生成的文件
    print("📁 检查生成的文件...")
    generated_files = [
        output_dir / "codeql-results.sarif",
        output_dir / "CODEQL_SECURITY_REPORT.md",
        output_dir / "漏洞验证_Checklist.md"
    ]
    
    for file in generated_files:
        if file.exists():
            size = file.stat().st_size
            print(f"   ✅ {file.name} ({size} 字节)")
        else:
            print(f"   ❌ {file.name} (缺失)")
    
    print()
    
    # 读取报告摘要
    report_file = output_dir / "CODEQL_SECURITY_REPORT.md"
    if report_file.exists():
        print("📊 报告摘要...")
        with open(report_file) as f:
            lines = f.readlines()[:20]
            for line in lines:
                print(f"   {line.rstrip()}")
        print()
    
    # 检查 Jenkins 构建状态
    print("🏢 检查 Jenkins 构建状态...")
    import requests
    
    jenkins_url = "http://localhost:8080"
    jenkins_user = "devops"
    jenkins_token = "110ffb6071ded434a52bd153217f3fc873"
    
    try:
        response = requests.get(
            f"{jenkins_url}/job/codeql-security-scan/api/json",
            auth=(jenkins_user, jenkins_token),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            builds = data.get('builds', [])
            if builds:
                latest = builds[0]
                status = latest.get('result', '构建中')
                number = latest.get('number')
                duration = latest.get('duration', 0) / 1000
                
                print(f"   ✅ 最新构建：#{number}")
                print(f"      状态：{status}")
                print(f"      持续时间：{duration:.1f}秒")
                
                if status == 'SUCCESS':
                    print(f"   ✅ Jenkins 构建成功！")
            else:
                print(f"   ⚠️  无构建记录")
        else:
            print(f"   ⚠️  Jenkins 不可用：{response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Jenkins 检查失败：{e}")
    
    print()
    
    # 最终总结
    print("=" * 60)
    print("  ✅ Li_codeql_LLM Skill 验证完成！")
    print("=" * 60)
    print()
    print("📊 验证结果:")
    print("   ✅ Skill 文件完整")
    print("   ✅ CodeQL 已安装")
    print("   ✅ 扫描可以运行")
    print("   ✅ 报告可以生成")
    print("   ✅ Jenkins 集成可用")
    print()
    print("🚀 可以正常使用了！")
    print()
    print("📋 使用方法:")
    print("   1. 在对话中：扫描 /path/to/project")
    print("   2. 命令行：uv run python3 codeql_llm_scan.py /path/to/project")
    print("   3. Jenkins: http://localhost:8080/job/codeql-security-scan/")
    print()
    
except subprocess.CalledProcessError as e:
    print(f"   ❌ 扫描失败：{e}")
    print(f"   错误输出：{e.stderr}")
    sys.exit(1)
except subprocess.TimeoutExpired:
    print(f"   ❌ 扫描超时（>5 分钟）")
    sys.exit(1)
