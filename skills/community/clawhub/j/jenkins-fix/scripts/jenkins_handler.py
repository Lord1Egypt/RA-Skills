#!/usr/bin/env python3
"""
Jenkins 构建助手
支持：列出项目、触发构建、获取构建结果
"""
import sys
import json
import requests
import base64
import time
import re
import os

# Jenkins 配置 - 从环境变量读取（推荐），支持回退到硬编码（仅开发环境）
JENKINS_URL = os.getenv("JENKINS_URL", "http://jks.huimei-inc.com")
USERNAME = os.getenv("JENKINS_USERNAME", "jiaofu")
API_TOKEN = os.getenv("JENKINS_API_TOKEN", "")  # 优先使用 API Token
PASSWORD = os.getenv("JENKINS_PASSWORD", "")    # API Token 过期时回退

# 创建 session 来维护 cookie
session = requests.Session()

def get_auth(try_api_token_first=True):
    """获取认证对象

    优先使用 API Token，失败时回退到用户名密码
    认证信息从环境变量读取，环境变量为空则尝试回退到硬编码（仅开发环境）
    """
    # 检查是否配置了有效凭据
    if not USERNAME:
        return None
    
    if try_api_token_first and API_TOKEN:
        # 先尝试 API Token
        try:
            test_url = f"{JENKINS_URL}/api/json"
            response = session.get(test_url, auth=(USERNAME, API_TOKEN), timeout=10)
            if response.status_code == 200:
                return (USERNAME, API_TOKEN)
        except Exception:
            pass

    # 回退到用户名密码
    if PASSWORD:
        return (USERNAME, PASSWORD)
    
    # 都没有配置，返回空
    return None

def get_crumb():
    """获取 Jenkins CSRF Crumb"""
    auth = get_auth()
    try:
        url = f"{JENKINS_URL}/crumbIssuer/api/json"
        response = session.get(url, auth=auth, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("crumbRequestField", ""), data.get("crumb", "")
    except:
        return None, None

def get_auth_headers():
    """获取认证头"""
    auth = get_auth()
    crumb_field, crumb_value = get_crumb()
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{auth[0]}:{auth[1]}'.encode()).decode()}"
    }
    if crumb_field and crumb_value:
        headers[crumb_field] = crumb_value
    return headers

# 认证（延迟初始化，避免启动时暴露敏感信息）
AUTH = None
AUTH_HEADER = None

def init_auth():
    """初始化认证信息和认证头（延迟调用，避免启动时暴露凭据）"""
    global AUTH, AUTH_HEADER
    AUTH = get_auth(try_api_token_first=True)
    if AUTH:
        AUTH_HEADER = get_auth_headers()
    else:
        AUTH_HEADER = {}

def get_jobs():
    """获取所有 Jenkins job"""
    try:
        init_auth()  # 确保认证已初始化
        url = f"{JENKINS_URL}/api/json?tree=jobs[name,url,color]"
        response = session.get(url, auth=AUTH, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("jobs", [])
    except Exception as e:
        return {"error": str(e)}

def get_job_info(job_name):
    """获取指定 job 的详细信息"""
    try:
        init_auth()  # 确保认证已初始化
        encoded_name = requests.utils.quote(job_name, safe='')
        url = f"{JENKINS_URL}/job/{encoded_name}/api/json"
        response = session.get(url, auth=AUTH, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_default_params(job_name):
    """获取 job 的默认参数"""
    try:
        init_auth()  # 确保认证已初始化
        encoded_name = requests.utils.quote(job_name, safe='')
        url = f"{JENKINS_URL}/job/{encoded_name}/api/json"
        response = session.get(url, auth=AUTH, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        params = {}
        for prop in data.get('property', []):
            if 'parameterDefinitions' in prop:
                for p in prop['parameterDefinitions']:
                    name = p['name']
                    default_val = p.get('defaultParameterValue', {}).get('value', '')
                    if default_val or p.get('type') == 'StringParameterDefinition':
                        params[name] = default_val
        return params
    except Exception as e:
        return {}

def trigger_build(job_name, parameters=None, branch=None):
    """触发构建"""
    try:
        init_auth()  # 确保认证已初始化
        if not AUTH:
            return {"error": "未配置 Jenkins 认证信息。请设置环境变量 JENKINS_USERNAME 和 JENKINS_PASSWORD 或 JENKINS_API_TOKEN"}
        
        encoded_name = requests.utils.quote(job_name, safe='')
        
        # 如果没有提供参数，自动获取默认参数
        if not parameters:
            parameters = get_default_params(job_name)
            print(f"   使用默认参数: {list(parameters.keys())}")
        
        # 如果指定了分支，覆盖默认的 BRANCH_TAG
        if branch:
            parameters['BRANCH_TAG'] = branch
            print(f"   🔀 指定分支: {branch}")
        
        if parameters:
            # 带参数构建
            url = f"{JENKINS_URL}/job/{encoded_name}/buildWithParameters"
        else:
            url = f"{JENKINS_URL}/job/{encoded_name}/build"
        
        # 使用 session + auth
        response = session.post(url, params=parameters, auth=AUTH, timeout=30)
        
        if response.status_code in [200, 201]:
            return {"success": True}
        else:
            return {"error": f"构建触发失败: {response.status_code} - {response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}

def get_last_build_info(job_name):
    """获取最后一次构建的信息"""
    try:
        init_auth()  # 确保认证已初始化
        encoded_name = requests.utils.quote(job_name, safe='')
        url = f"{JENKINS_URL}/job/{encoded_name}/lastBuild/api/json"
        response = session.get(url, auth=AUTH, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_build_console_output(job_name, build_number):
    """获取构建日志"""
    try:
        init_auth()  # 确保认证已初始化
        encoded_name = requests.utils.quote(job_name, safe='')
        url = f"{JENKINS_URL}/job/{encoded_name}/{build_number}/consoleText"
        response = session.get(url, auth=AUTH, timeout=30)
        response.raise_for_status()
        return response.text[-5000:]  # 返回最后 5000 字符
    except Exception as e:
        return f"获取日志失败: {str(e)}"

def wait_for_build_complete(job_name, timeout=300):
    """等待构建完成"""
    start_time = time.time()
    last_build = None
    
    while time.time() - start_time < timeout:
        build_info = get_last_build_info(job_name)
        
        if "error" in build_info:
            return {"error": build_info["error"]}
        
        # 检查构建是否还在进行中
        if build_info.get("building"):
            last_build = build_info
            time.sleep(5)
            continue
        
        # 构建完成
        return {
            "building": False,
            "number": build_info.get("number"),
            "result": build_info.get("result"),
            "timestamp": build_info.get("timestamp"),
            "duration": build_info.get("duration"),
            "url": build_info.get("url")
        }
    
    return {"error": "构建超时"}

def find_artifacts(job_name, build_number):
    """查找构建产物"""
    try:
        init_auth()  # 确保认证已初始化
        encoded_name = requests.utils.quote(job_name, safe='')
        url = f"{JENKINS_URL}/job/{encoded_name}/{build_number}/api/json?tree=artifacts[fileName,relativePath,url]"
        response = session.get(url, auth=AUTH, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("artifacts", [])
    except Exception as e:
        return []

def find_oss_links(job_name, build_number):
    """从构建日志中查找 OSS 下载链接"""
    try:
        init_auth()  # 确保认证已初始化
        encoded_name = requests.utils.quote(job_name, safe='')
        url = f"{JENKINS_URL}/job/{encoded_name}/{build_number}/consoleText"
        response = session.get(url, auth=AUTH, timeout=30)
        response.raise_for_status()
        log = response.text
        
        # 查找 OSS 链接
        oss_pattern = r'http://ovf\.oss-cn-hangzhou\.aliyuncs\.com[^\s<>"\']+'
        matches = re.findall(oss_pattern, log)
        return matches
    except Exception as e:
        return []

def format_job_list(jobs):
    """格式化 job 列表输出"""
    if "error" in jobs:
        return f"❌ 获取项目列表失败: {jobs['error']}"
    
    if not jobs:
        return "📭 没有找到任何 Jenkins 项目"
    
    lines = ["## 🤖 Jenkins 项目列表\n"]
    lines.append(f"共 **{len(jobs)}** 个项目：\n")
    
    for job in jobs:
        name = job.get("name", "Unknown")
        url = job.get("url", "")
        color = job.get("color", "grey")
        
        # 状态图标
        if color == "blue":
            status = "✅ 成功"
        elif color == "red":
            status = "❌ 失败"
        elif color == "yellow":
            status = "⚠️ 不稳定"
        elif color == "grey" or color == "aborted":
            status = "⏸️ 未构建"
        elif color == "anime":
            status = "🔄 构建中"
        else:
            status = "❓ 未知"
        
        lines.append(f"- **{name}** - {status}")
    
    lines.append("\n回复 `构建 <项目名>` 触发构建")
    return "\n".join(lines)

def format_build_result(job_name, build_info, console_output=None):
    """格式化构建结果"""
    if "error" in build_info:
        return f"❌ 获取构建信息失败: {build_info['error']}"
    
    result = build_info.get("result", "UNKNOWN")
    number = build_info.get("number", "?")
    duration = build_info.get("duration", 0) / 1000  # 转换为秒
    
    lines = []
    
    if result == "SUCCESS":
        lines.append(f"✅ **{job_name}** 构建成功！")
        lines.append(f"   构建号: **#{number}**")
        lines.append(f"   耗时: **{duration:.1f}秒**")
        
        # 查找产物
        artifacts = find_artifacts(job_name, number)
        if artifacts:
            lines.append("\n📦 **程序包下载地址：**")
            for art in artifacts[:5]:  # 最多显示 5 个
                path = art.get("relativePath", "")
                url = art.get("url", "")
                lines.append(f"- [{path}]({JENKINS_URL}{url})")
        else:
            # 从日志中查找 OSS 链接
            oss_links = find_oss_links(job_name, number)
            if oss_links:
                lines.append("\n📦 **程序包下载地址：**")
                for i, link in enumerate(oss_links[:3], 1):
                    lines.append(f"{i}. {link}")
            else:
                lines.append("\n💡 未找到程序包，请查看 Jenkins 页面获取下载链接")
    else:
        lines.append(f"❌ **{job_name}** 构建失败！")
        lines.append(f"   构建号: **#{number}**")
        lines.append(f"   耗时: **{duration:.1f}秒**")
        
        if console_output:
            lines.append("\n📋 **失败日志（最后 2000 字符）：**")
            lines.append("```")
            lines.append(console_output[-2000:])
            lines.append("```")
    
    return "\n".join(lines)

def parse_command(text):
    """解析用户命令"""
    text = text.strip()
    
    # 列出项目
    if any(kw in text.lower() for kw in ["项目列表", "job列表", "列出", "list"]):
        return {"action": "list"}
    
    # 触发构建：支持多种格式
    # 格式1: 构建 <项目名> <分支名>
    # 格式2: 构建 <项目名> 分支=<分支名>
    # 格式3: 触发 <项目名> 构建
    build_match = re.search(r"构建\s+(.+)", text)
    if build_match or "触发" in text:
        content = build_match.group(1) if build_match else ""
        if "触发" in text:
            trigger_match = re.search(r"触发\s*(.+?)\s*构建", text)
            if trigger_match:
                content = trigger_match.group(1)
        
        # 解析项目名和分支
        parts = content.strip().split()
        project_name = parts[0] if parts else ""
        
        # 检查是否有分支参数
        branch = None
        for part in parts[1:]:
            if part.startswith("分支=") or part.startswith("branch="):
                branch = part.split("=", 1)[1].strip()
            elif len(part) > 3 and not "=" in part:
                # 可能是分支名（没有等号的参数）
                branch = part
        
        return {"action": "build", "project": project_name.strip(), "branch": branch}
    
    # 构建状态
    status_match = re.search(r"(.+)\s*构建状态", text)
    if status_match:
        return {"action": "status", "project": status_match.group(1).strip()}
    
    return {"action": "help"}

def main():
    input_text = ""
    
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        try:
            input_text = sys.stdin.read()
        except:
            pass
    
    if not input_text:
        print("## Jenkins 构建助手\n")
        print("用法：")
        print("- `Jenkins 项目列表` - 查看所有项目")
        print("- `构建 <项目名>` - 触发构建")
        print("- `<项目名> 构建状态` - 查看构建结果")
        print("\n**⚠️ 注意：** 需要配置 Jenkins 认证信息才能使用。")
        print("请设置以下环境变量（至少其一）：")
        print("  - `JENKINS_USERNAME` + `JENKINS_API_TOKEN`（推荐）")
        print("  - `JENKINS_USERNAME` + `JENKINS_PASSWORD`")
        print("  - `JENKINS_URL`（可选，默认 http://jks.huimei-inc.com）")
        return
    
    # 初始化认证（延迟加载，仅在需要时）
    init_auth()
    
    cmd = parse_command(input_text)
    
    if cmd["action"] == "list":
        jobs = get_jobs()
        print(format_job_list(jobs))
    
    elif cmd["action"] == "build":
        project = cmd.get("project", "")
        if not project:
            print("❌ 请指定项目名称，例如：`构建 my-project`")
            return
        
        # 先获取 job 列表，找到匹配的项目
        jobs = get_jobs()
        if "error" in jobs:
            print(f"❌ 获取项目列表失败: {jobs['error']}")
            return
        
        # 查找匹配的项目
        matched = None
        for job in jobs:
            if project.lower() in job.get("name", "").lower():
                matched = job.get("name")
                break
        
        if not matched:
            # 精确匹配
            for job in jobs:
                if project.lower() == job.get("name", "").lower():
                    matched = job.get("name")
                    break
        
        if not matched:
            print(f"❌ 未找到项目: {project}")
            print("可用项目：")
            for job in jobs:
                print(f"  - {job.get('name')}")
            return
        
        # 触发构建
        print(f"🔄 正在触发 **{matched}** 构建...")
        branch = cmd.get("branch")
        result = trigger_build(matched, branch=branch)
        
        if "error" in result:
            print(f"❌ 构建失败: {result['error']}")
            return
        
        print(f"✅ 构建已触发，等待构建完成...")
        print("   (最多等待 5 分钟)\n")
        
        # 等待构建完成
        build_info = wait_for_build_complete(matched, timeout=300)
        
        if "error" in build_info:
            print(f"❌ 获取构建结果失败: {build_info['error']}")
            return
        
        # 获取日志（如果失败）
        console_output = None
        if build_info.get("result") != "SUCCESS":
            console_output = get_build_console_output(matched, build_info.get("number"))
        
        print(format_build_result(matched, build_info, console_output))
    
    elif cmd["action"] == "status":
        project = cmd.get("project", "")
        if not project:
            print("❌ 请指定项目名称")
            return
        
        build_info = get_last_build_info(project)
        console_output = None
        
        if build_info.get("result") != "SUCCESS":
            console_output = get_build_console_output(project, build_info.get("number"))
        
        print(format_build_result(project, build_info, console_output))
    
    else:
        print("## Jenkins 构建助手\n")
        print("用法：")
        print("- `Jenkins 项目列表` - 查看所有项目")
        print("- `构建 <项目名>` - 触发构建（使用默认分支）")
        print("- `构建 <项目名> <分支名>` - 触发构建并指定分支")
        print("- `构建 <项目名> 分支=<分支名>` - 触发构建并指定分支")
        print("- `<项目名> 构建状态` - 查看构建结果")
        print("")
        print("示例：")
        print("- 构建 hospital__go_crf_service cloud_251230_release")
        print("- 构建 hospital__go_crf_service 分支=cloud_251230_release")

if __name__ == "__main__":
    main()
