#!/usr/bin/env python3
"""
项目分析脚本 - 阶段1
分析项目结构、文档、配置和现有 Dockerfile
"""

import os
import json
from pathlib import Path


def detect_project_type(project_path):
    """检测项目类型"""
    indicators = {
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
        'nodejs': ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
        'java_maven': ['pom.xml'],
        'java_gradle': ['build.gradle', 'settings.gradle', 'gradlew'],
        'go': ['go.mod', 'go.sum'],
        'rust': ['Cargo.toml', 'Cargo.lock'],
        'php': ['composer.json', 'index.php'],
        'ruby': ['Gemfile', 'Gemfile.lock'],
        'dotnet': ['*.csproj', '*.sln'],
    }

    detected = []
    for ptype, files in indicators.items():
        for f in files:
            if '*' in f:
                import glob
                if glob.glob(os.path.join(project_path, f)):
                    detected.append(ptype)
                    break
            elif os.path.exists(os.path.join(project_path, f)):
                detected.append(ptype)
                break

    return detected


def find_dockerfiles(project_path):
    """查找所有 Dockerfile"""
    dockerfiles = []
    for root, dirs, files in os.walk(project_path):
        # 跳过 node_modules 等目录
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'target', 'build', 'dist']]
        for f in files:
            if 'dockerfile' in f.lower() or f.lower().endswith('.dockerfile'):
                dockerfiles.append(os.path.join(root, f))
    return dockerfiles


def analyze_dockerfile(dockerfile_path):
    """分析 Dockerfile 用途"""
    with open(dockerfile_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()

    # 判断 Dockerfile 用途
    is_build = any(kw in content for kw in [
        'from maven', 'from gradle', 'from node',
        'pip install', 'npm install', 'yarn install',
        'mvn ', 'gradle ', 'go build', 'cargo build',
        'npm run build', 'yarn build'
    ])

    is_deploy = any(kw in content for kw in [
        'copy --from=builder', 'copy --from=build',
        'artifacts/', 'dist/', 'target/', 'build/'
    ])

    is_dev = any(kw in content for kw in [
        'volume', 'cmd ["npm", "run", "dev"]', 'debug',
        'hot reload', 'nodemon', 'air '
    ])

    if is_build and not is_deploy:
        return 'build'
    elif is_deploy:
        return 'deploy'
    elif is_dev:
        return 'dev'
    else:
        return 'unknown'


def find_configs(project_path):
    """查找配置文件"""
    configs = {
        'env_files': [],
        'app_configs': [],
        'config_dirs': []
    }

    # 环境变量文件
    for f in ['.env', '.env.example', '.env.template', '.env.local', 'config.env']:
        if os.path.exists(os.path.join(project_path, f)):
            configs['env_files'].append(f)

    # 应用配置文件
    config_patterns = [
        'application*.yml', 'application*.yaml', 'application*.properties',
        'config*.yml', 'config*.yaml', 'config*.json',
        '*.config.js', '*.config.ts', '*.config.json',
        'nginx.conf', 'httpd.conf', 'apache2.conf'
    ]

    import glob
    for pattern in config_patterns:
        matches = glob.glob(os.path.join(project_path, '**', pattern), recursive=True)
        configs['app_configs'].extend([os.path.relpath(m, project_path) for m in matches])

    # 配置目录
    for d in ['config', 'conf', 'settings', 'configuration']:
        if os.path.isdir(os.path.join(project_path, d)):
            configs['config_dirs'].append(d)

    return configs


def find_docs(project_path):
    """查找项目文档"""
    docs = {
        'readme': None,
        'deploy_docs': [],
        'install_docs': [],
        'config_docs': []
    }

    # README
    for f in ['README.md', 'readme.md', 'Readme.md', 'README.rst']:
        if os.path.exists(os.path.join(project_path, f)):
            docs['readme'] = f
            break

    # 部署文档
    deploy_names = ['DEPLOY', 'deploy', '部署指南', '部署说明', 'DEPLOYMENT']
    for name in deploy_names:
        for ext in ['.md', '.rst', '.txt', '']:
            f = f"{name}{ext}"
            if os.path.exists(os.path.join(project_path, f)):
                docs['deploy_docs'].append(f)
            docs_path = os.path.join(project_path, 'docs')
            if os.path.exists(docs_path):
                for df in os.listdir(docs_path):
                    if name.lower() in df.lower():
                        docs['deploy_docs'].append(f"docs/{df}")

    # 安装文档
    install_names = ['INSTALL', 'install', '安装说明', '安装指南', 'SETUP', 'setup']
    for name in install_names:
        for ext in ['.md', '.rst', '.txt', '']:
            f = f"{name}{ext}"
            if os.path.exists(os.path.join(project_path, f)):
                docs['install_docs'].append(f)

    # 配置文档
    config_names = ['CONFIG', 'config', '配置说明', '配置指南', 'CONFIGURATION']
    for name in config_names:
        for ext in ['.md', '.rst', '.txt', '']:
            f = f"{name}{ext}"
            if os.path.exists(os.path.join(project_path, f)):
                docs['config_docs'].append(f)

    return docs


def generate_report(project_path, output_path):
    """生成分析报告"""
    report = []
    report.append("# 项目容器化分析报告\n")
    report.append(f"**分析路径**: {project_path}\n")
    report.append(f"**分析时间**: {__import__('datetime').datetime.now().isoformat()}\n\n")

    # 1. 项目类型
    report.append("## 1. 项目类型分析\n")
    types = detect_project_type(project_path)
    if types:
        report.append(f"**检测到的项目类型**: {', '.join(types)}\n")
    else:
        report.append("**未识别到明确的项目类型**\n")

    # 2. Dockerfile 分析
    report.append("\n## 2. Dockerfile 分析\n")
    dockerfiles = find_dockerfiles(project_path)
    if dockerfiles:
        report.append(f"**发现 {len(dockerfiles)} 个 Dockerfile**:\n\n")
        for df in dockerfiles:
            purpose = analyze_dockerfile(df)
            purpose_desc = {
                'build': '打包用（构建制品）',
                'deploy': '部署用（运行制品）',
                'dev': '开发用（调试/热重载）',
                'unknown': '用途不明'
            }.get(purpose, '未知')
            rel_path = os.path.relpath(df, project_path)
            report.append(f"- `{rel_path}` → **{purpose_desc}**\n")
    else:
        report.append("**未发现现有 Dockerfile**\n")

    # 3. 配置文件分析
    report.append("\n## 3. 配置文件分析\n")
    configs = find_configs(project_path)
    if configs['env_files']:
        report.append(f"**环境变量文件**: {', '.join(configs['env_files'])}\n")
    if configs['app_configs']:
        report.append(f"**应用配置文件**: {len(configs['app_configs'])} 个\n")
        for cfg in configs['app_configs'][:10]:  # 最多显示10个
            report.append(f"  - `{cfg}`\n")
        if len(configs['app_configs']) > 10:
            report.append(f"  - ... 等共 {len(configs['app_configs'])} 个\n")
    if configs['config_dirs']:
        report.append(f"**配置目录**: {', '.join(configs['config_dirs'])}\n")

    # 4. 文档分析
    report.append("\n## 4. 项目文档分析\n")
    docs = find_docs(project_path)
    if docs['readme']:
        report.append(f"**README**: `{docs['readme']}`\n")
    if docs['deploy_docs']:
        report.append(f"**部署文档**: {', '.join(docs['deploy_docs'])}\n")
    if docs['install_docs']:
        report.append(f"**安装文档**: {', '.join(docs['install_docs'])}\n")
    if docs['config_docs']:
        report.append(f"**配置文档**: {', '.join(docs['config_docs'])}\n")

    # 5. 建议
    report.append("\n## 5. 容器化建议\n")
    if 'java' in types or 'java_maven' in types or 'java_gradle' in types:
        report.append("- **制品类型**: JAR 文件\n")
        report.append("- **打包基础镜像**: maven/gradle + eclipse-temurin\n")
        report.append("- **部署基础镜像**: eclipse-temurin-jre-alpine\n")
    elif 'nodejs' in types:
        # 检查是否为前端项目
        pkg_path = os.path.join(project_path, 'package.json')
        if os.path.exists(pkg_path):
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)
            deps = list(pkg.get('dependencies', {}).keys())
            if any(d in deps for d in ['react', 'vue', 'angular', '@angular/core']):
                report.append("- **项目类型**: 前端项目\n")
                report.append("- **制品类型**: dist/ 目录（静态文件）\n")
                report.append("- **打包基础镜像**: node:alpine\n")
                report.append("- **部署基础镜像**: nginx:alpine\n")
            else:
                report.append("- **项目类型**: Node.js 后端项目\n")
                report.append("- **制品类型**: node_modules/ + 源码\n")
                report.append("- **打包/部署基础镜像**: node:alpine\n")
    elif 'python' in types:
        report.append("- **制品类型**: 源码 + 依赖\n")
        report.append("- **打包/部署基础镜像**: python:slim\n")
    elif 'go' in types:
        report.append("- **制品类型**: 二进制文件\n")
        report.append("- **打包基础镜像**: golang:alpine\n")
        report.append("- **部署基础镜像**: gcr.io/distroless/static 或 alpine\n")

    # 写入报告
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(report)

    print(f"分析报告已生成: {output_path}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("用法: python analyze_project.py <项目路径>")
        sys.exit(1)

    project_path = sys.argv[1]
    output_path = os.path.join(project_path, 'deploy', 'analysis-report.md')
    generate_report(project_path, output_path)
