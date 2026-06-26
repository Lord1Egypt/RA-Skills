#!/usr/bin/env python3
"""
生成打包用 Dockerfile - 阶段2
"""

import os
import json
from pathlib import Path


def detect_python_version(project_path):
    """检测 Python 版本"""
    # 尝试从 runtime.txt 读取
    runtime_file = os.path.join(project_path, 'runtime.txt')
    if os.path.exists(runtime_file):
        with open(runtime_file, 'r') as f:
            content = f.read().strip()
            if content.startswith('python-'):
                return content.replace('python-', '')

    # 尝试从 .python-version 读取
    pyversion_file = os.path.join(project_path, '.python-version')
    if os.path.exists(pyversion_file):
        with open(pyversion_file, 'r') as f:
            return f.read().strip()

    # 尝试从 pyproject.toml 读取
    pyproject_file = os.path.join(project_path, 'pyproject.toml')
    if os.path.exists(pyproject_file):
        import re
        with open(pyproject_file, 'r') as f:
            content = f.read()
            match = re.search(r'requires-python\s*=\s*["\'](>=|~|=|==)?([\d.]+)', content)
            if match:
                return match.group(2)

    return "3.11"  # 默认版本


def detect_node_version(project_path):
    """检测 Node.js 版本"""
    pkg_file = os.path.join(project_path, 'package.json')
    if os.path.exists(pkg_file):
        with open(pkg_file, 'r') as f:
            pkg = json.load(f)
            engines = pkg.get('engines', {})
            if 'node' in engines:
                version = engines['node']
                # 提取版本号
                import re
                match = re.search(r'(\d+)', version)
                if match:
                    return match.group(1)

    # 尝试从 .nvmrc 读取
    nvmrc_file = os.path.join(project_path, '.nvmrc')
    if os.path.exists(nvmrc_file):
        with open(nvmrc_file, 'r') as f:
            version = f.read().strip()
            if version.startswith('v'):
                version = version[1:]
            return version.split('.')[0]  # 返回主版本号

    return "20"  # 默认版本


def detect_java_version(project_path):
    """检测 Java 版本"""
    # 从 pom.xml 读取
    pom_file = os.path.join(project_path, 'pom.xml')
    if os.path.exists(pom_file):
        import re
        with open(pom_file, 'r') as f:
            content = f.read()
            # 查找 java.version 或 maven.compiler.target
            match = re.search(r'<(java\.version|maven\.compiler\.target|maven\.compiler\.source)>(\d+)', content)
            if match:
                return match.group(2)

    # 从 gradle 读取
    gradle_file = os.path.join(project_path, 'build.gradle')
    if os.path.exists(gradle_file):
        import re
        with open(gradle_file, 'r') as f:
            content = f.read()
            match = re.search(r'sourceCompatibility\s*=\s*[\'"]?(\d+)', content)
            if match:
                return match.group(1)

    return "17"  # 默认版本


def detect_go_version(project_path):
    """检测 Go 版本"""
    go_mod = os.path.join(project_path, 'go.mod')
    if os.path.exists(go_mod):
        import re
        with open(go_mod, 'r') as f:
            content = f.read()
            match = re.search(r'go\s+(\d+\.\d+)', content)
            if match:
                return match.group(1)
    return "1.21"


def generate_python_build(project_path):
    """生成 Python 打包 Dockerfile"""
    version = detect_python_version(project_path)

    dockerfile = f'''# Python 项目打包 Dockerfile
FROM python:{version}-slim AS builder

WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc \\
    libc6-dev \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖到指定目录
RUN pip install --no-cache-dir --user -r requirements.txt

# 复制源码
COPY . .

# 导出阶段 - 收集所有制品
FROM alpine:latest AS exporter

WORKDIR /output

# 复制 Python 依赖和源码
COPY --from=builder /root/.local /output/python-packages
COPY --from=builder /build /output/source

# 创建制品清单
RUN echo "Python {version} Project Artifacts" > /output/ARTIFACTS.txt && \\
    echo "Packages: /python-packages" >> /output/ARTIFACTS.txt && \\
    echo "Source: /source" >> /output/ARTIFACTS.txt

VOLUME ["/output"]
CMD ["cp", "-r", "/output/.", "/artifacts/"]
'''
    return dockerfile


def generate_nodejs_build(project_path, is_frontend=True):
    """生成 Node.js 打包 Dockerfile"""
    version = detect_node_version(project_path)
    pkg_file = os.path.join(project_path, 'package.json')

    # 检测包管理器
    if os.path.exists(os.path.join(project_path, 'pnpm-lock.yaml')):
        pkg_manager = 'pnpm'
        install_cmd = 'npm install -g pnpm && pnpm install'
        build_cmd = 'pnpm run build'
    elif os.path.exists(os.path.join(project_path, 'yarn.lock')):
        pkg_manager = 'yarn'
        install_cmd = 'npm install -g yarn && yarn install'
        build_cmd = 'yarn build'
    else:
        pkg_manager = 'npm'
        install_cmd = 'npm ci'
        build_cmd = 'npm run build'

    if is_frontend:
        dockerfile = f'''# Node.js 前端项目打包 Dockerfile
FROM node:{version}-alpine AS builder

WORKDIR /build

# 复制依赖文件
COPY package*.json ./
{'' if pkg_manager == 'npm' else f'RUN npm install -g {pkg_manager}'}

# 安装依赖
RUN {install_cmd}

# 复制源码
COPY . .

# 构建
RUN {build_cmd}

# 导出阶段
FROM alpine:latest AS exporter

WORKDIR /output

# 复制构建产物
COPY --from=builder /build/dist /output/dist

# 创建制品清单
RUN echo "Node.js {version} Frontend Artifacts" > /output/ARTIFACTS.txt && \\
    echo "Build output: /dist" >> /output/ARTIFACTS.txt

VOLUME ["/output"]
CMD ["cp", "-r", "/output/.", "/artifacts/"]
'''
    else:
        dockerfile = f'''# Node.js 后端项目打包 Dockerfile
FROM node:{version}-alpine AS builder

WORKDIR /build

# 复制依赖文件
COPY package*.json ./
{'' if pkg_manager == 'npm' else f'RUN npm install -g {pkg_manager}'}

# 安装生产依赖
RUN {install_cmd} --production

# 导出阶段
FROM alpine:latest AS exporter

WORKDIR /output

# 复制依赖和源码
COPY --from=builder /build/node_modules /output/node_modules
COPY --from=builder /build/package*.json /output/

# 创建制品清单
RUN echo "Node.js {version} Backend Artifacts" > /output/ARTIFACTS.txt && \\
    echo "Dependencies: /node_modules" >> /output/ARTIFACTS.txt

VOLUME ["/output"]
CMD ["cp", "-r", "/output/.", "/artifacts/"]
'''
    return dockerfile


def generate_java_build(project_path):
    """生成 Java 打包 Dockerfile"""
    jdk_version = detect_java_version(project_path)

    if os.path.exists(os.path.join(project_path, 'pom.xml')):
        # Maven 项目
        dockerfile = f'''# Java Maven 项目打包 Dockerfile
FROM maven:3.9-eclipse-temurin-{jdk_version}-alpine AS builder

WORKDIR /build

# 复制 pom.xml 先下载依赖（利用缓存）
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 复制源码
COPY src ./src

# 打包
RUN mvn clean package -DskipTests -B

# 导出阶段
FROM alpine:latest AS exporter

WORKDIR /output

# 复制 JAR 文件
COPY --from=builder /build/target/*.jar /output/app.jar

# 创建制品清单
RUN echo "Java {jdk_version} Maven Artifacts" > /output/ARTIFACTS.txt && \\
    echo "JAR: /app.jar" >> /output/ARTIFACTS.txt

VOLUME ["/output"]
CMD ["cp", "-r", "/output/.", "/artifacts/"]
'''
    else:
        # Gradle 项目
        dockerfile = f'''# Java Gradle 项目打包 Dockerfile
FROM gradle:8-jdk{jdk_version}-alpine AS builder

WORKDIR /build

# 复制 Gradle 文件
COPY build.gradle settings.gradle ./
COPY gradle ./gradle

# 下载依赖
RUN gradle dependencies --no-daemon

# 复制源码
COPY src ./src

# 打包
RUN gradle bootJar --no-daemon

# 导出阶段
FROM alpine:latest AS exporter

WORKDIR /output

# 复制 JAR 文件
COPY --from=builder /build/build/libs/*.jar /output/app.jar

# 创建制品清单
RUN echo "Java {jdk_version} Gradle Artifacts" > /output/ARTIFACTS.txt && \\
    echo "JAR: /app.jar" >> /output/ARTIFACTS.txt

VOLUME ["/output"]
CMD ["cp", "-r", "/output/.", "/artifacts/"]
'''
    return dockerfile


def generate_go_build(project_path):
    """生成 Go 打包 Dockerfile"""
    version = detect_go_version(project_path)

    dockerfile = f'''# Go 项目打包 Dockerfile
FROM golang:{version}-alpine AS builder

WORKDIR /build

# 安装构建工具
RUN apk add --no-cache git

# 复制依赖文件
COPY go.mod go.sum ./
RUN go mod download

# 复制源码
COPY . .

# 构建静态二进制文件
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# 导出阶段
FROM alpine:latest AS exporter

WORKDIR /output

# 复制二进制文件
COPY --from=builder /build/app /output/app

# 创建制品清单
RUN echo "Go {version} Artifacts" > /output/ARTIFACTS.txt && \\
    echo "Binary: /app" >> /output/ARTIFACTS.txt

VOLUME ["/output"]
CMD ["cp", "-r", "/output/.", "/artifacts/"]
'''
    return dockerfile


def main():
    import sys
    if len(sys.argv) < 3:
        print("用法: python generate_build_dockerfile.py <项目路径> <项目类型>")
        print("项目类型: python, nodejs-frontend, nodejs-backend, java, go")
        sys.exit(1)

    project_path = sys.argv[1]
    project_type = sys.argv[2]

    generators = {
        'python': generate_python_build,
        'nodejs-frontend': lambda p: generate_nodejs_build(p, True),
        'nodejs-backend': lambda p: generate_nodejs_build(p, False),
        'java': generate_java_build,
        'go': generate_go_build,
    }

    if project_type not in generators:
        print(f"不支持的项目类型: {project_type}")
        sys.exit(1)

    dockerfile = generators[project_type](project_path)

    output_path = os.path.join(project_path, 'deploy', 'Dockerfile.build')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(dockerfile)

    print(f"打包 Dockerfile 已生成: {output_path}")


if __name__ == '__main__':
    main()
