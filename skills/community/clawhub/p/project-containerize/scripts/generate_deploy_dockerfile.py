#!/usr/bin/env python3
"""
生成部署用 Dockerfile - 阶段3
"""

import os


def generate_python_deploy(project_path, use_non_root=False):
    """生成 Python 部署 Dockerfile"""
    # 从打包 Dockerfile 检测版本
    from generate_build_dockerfile import detect_python_version
    version = detect_python_version(project_path)

    user_section = ""
    if use_non_root:
        user_section = '''
# 创建非 root 用户（项目要求）
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser
'''

    dockerfile = f'''# Python 项目部署 Dockerfile
FROM python:{version}-slim

WORKDIR /app

# 只安装运行必需的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libpq5 \\
    && rm -rf /var/lib/apt/lists/*

# 从制品目录复制 Python 包和源码
COPY artifacts/python-packages /usr/local
COPY artifacts/source /app

{user_section}

# 暴露端口（根据项目调整）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 启动命令（根据项目调整）
CMD ["python", "-m", "app"]
'''
    return dockerfile


def generate_nodejs_frontend_deploy(project_path):
    """生成 Node.js 前端部署 Dockerfile"""
    # 前端使用 nginx 部署静态文件
    dockerfile = '''# Node.js 前端项目部署 Dockerfile
FROM nginx:alpine

# 复制构建产物到 nginx 目录
COPY artifacts/dist /usr/share/nginx/html

# 复制自定义 nginx 配置（如果有）
# COPY config/nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# nginx 默认在前台运行
'''
    return dockerfile


def generate_nodejs_backend_deploy(project_path, use_non_root=False):
    """生成 Node.js 后端部署 Dockerfile"""
    from generate_build_dockerfile import detect_node_version
    version = detect_node_version(project_path)

    user_section = ""
    if use_non_root:
        user_section = '''
# 创建非 root 用户（项目要求）
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -s /bin/sh -D appuser
USER appuser
'''

    dockerfile = f'''# Node.js 后端项目部署 Dockerfile
FROM node:{version}-alpine

WORKDIR /app

# 从制品目录复制依赖和代码
COPY artifacts/node_modules ./node_modules
COPY artifacts/package*.json ./

# 如果项目需要特定脚本或文件，在此复制
# COPY artifacts/some-script.js ./

{user_section}

# 暴露端口（根据项目调整）
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"

# 启动命令（根据项目调整）
CMD ["node", "server.js"]
'''
    return dockerfile


def generate_java_deploy(project_path, use_non_root=False):
    """生成 Java 部署 Dockerfile"""
    from generate_build_dockerfile import detect_java_version
    jdk_version = detect_java_version(project_path)

    user_section = ""
    if use_non_root:
        user_section = '''
# 创建非 root 用户（项目要求）
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -s /bin/sh -D appuser
USER appuser
'''

    dockerfile = f'''# Java 项目部署 Dockerfile
FROM eclipse-temurin:{jdk_version}-jre-alpine

WORKDIR /app

# 从制品目录复制 JAR 文件
COPY artifacts/app.jar app.jar

{user_section}

# 暴露端口（根据项目调整）
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \\
    CMD wget --quiet --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# JVM 参数可通过环境变量传递
ENV JAVA_OPTS="-Xmx512m -Xms256m"

# 启动命令
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
'''
    return dockerfile


def generate_go_deploy(project_path, use_non_root=False):
    """生成 Go 部署 Dockerfile"""
    user_section = ""
    if use_non_root:
        user_section = '''
# 使用非 root 用户（项目要求）
USER nonroot:nonroot
'''

    dockerfile = f'''# Go 项目部署 Dockerfile
FROM gcr.io/distroless/static:nonroot

WORKDIR /app

# 从制品目录复制二进制文件
COPY artifacts/app /app/app

{user_section}

# 暴露端口（根据项目调整）
EXPOSE 8080

# 启动命令
ENTRYPOINT ["/app/app"]
'''
    return dockerfile


def main():
    import sys
    if len(sys.argv) < 3:
        print("用法: python generate_deploy_dockerfile.py <项目路径> <项目类型> [--non-root]")
        print("项目类型: python, nodejs-frontend, nodejs-backend, java, go")
        sys.exit(1)

    project_path = sys.argv[1]
    project_type = sys.argv[2]
    use_non_root = '--non-root' in sys.argv

    generators = {
        'python': generate_python_deploy,
        'nodejs-frontend': generate_nodejs_frontend_deploy,
        'nodejs-backend': generate_nodejs_backend_deploy,
        'java': generate_java_deploy,
        'go': generate_go_deploy,
    }

    if project_type not in generators:
        print(f"不支持的项目类型: {project_type}")
        sys.exit(1)

    if project_type == 'nodejs-frontend':
        dockerfile = generators[project_type](project_path)
    else:
        dockerfile = generators[project_type](project_path, use_non_root)

    output_path = os.path.join(project_path, 'deploy', 'Dockerfile')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(dockerfile)

    print(f"部署 Dockerfile 已生成: {output_path}")
    if use_non_root:
        print("注意：已配置非 root 用户运行")
    else:
        print("注意：使用默认 root 用户运行")


if __name__ == '__main__':
    main()
