#!/usr/bin/env python3
"""
生成标准部署方案 - 阶段5
生成 docker-run.sh 和 compose.yaml，包含配置文件挂载
"""

import os
import glob


def get_config_mounts(deploy_config_dir):
    """获取配置文件挂载列表"""
    mounts = []

    if not os.path.exists(deploy_config_dir):
        return mounts

    for root, dirs, files in os.walk(deploy_config_dir):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, deploy_config_dir)

            # 确定容器内路径
            if 'application' in file.lower():
                container_path = f"/app/config/{file}"
            elif 'nginx' in file.lower():
                container_path = f"/etc/nginx/conf.d/{file}"
            elif 'logback' in file.lower() or 'log4j' in file.lower():
                container_path = f"/app/{file}"
            else:
                container_path = f"/app/config/{file}"

            mounts.append({
                'local': f"./config/{rel_path}",
                'container': container_path,
                'file': file
            })

    return mounts


def generate_docker_run_script(project_path, app_port=8080):
    """生成 docker-run.sh 脚本"""
    deploy_config_dir = os.path.join(project_path, 'deploy', 'config')
    mounts = get_config_mounts(deploy_config_dir)

    mount_commands = ""
    for mount in mounts:
        mount_commands += f'  -v "$(pwd)/{mount["local"]}:{mount["container"]}:ro" \\\\\n'

    script = f'''#!/bin/bash
# 项目容器化部署脚本
# 生成时间: {__import__('datetime').datetime.now().isoformat()}

set -e

# 加载环境变量
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 镜像名称
IMAGE_NAME="${{APP_NAME:-myapp}}:latest"
CONTAINER_NAME="${{APP_NAME:-myapp}}"
APP_PORT="${{APP_PORT:-{app_port}}}"

echo "=== 构建部署镜像 ==="
docker build -t $IMAGE_NAME -f Dockerfile ..

echo "=== 停止现有容器 ==="
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "=== 启动新容器 ==="
docker run -d \\\\
  --name $CONTAINER_NAME \\\\
  -p "$APP_PORT:$APP_PORT" \\\\
{mount_commands}  --env-file .env \\\\
  --restart unless-stopped \\\\
  $IMAGE_NAME

echo "=== 等待服务启动 ==="
sleep 5

echo "=== 检查服务状态 ==="
if docker ps | grep -q $CONTAINER_NAME; then
    echo "✓ 容器运行正常"
    docker logs --tail 20 $CONTAINER_NAME
else
    echo "✗ 容器启动失败"
    docker logs $CONTAINER_NAME
    exit 1
fi

echo ""
echo "=== 部署完成 ==="
echo "服务地址: http://localhost:$APP_PORT"
echo "查看日志: docker logs -f $CONTAINER_NAME"
echo "停止服务: docker stop $CONTAINER_NAME"
'''

    return script


def generate_compose_yaml(project_path, app_port=8080):
    """生成 compose.yaml 文件"""
    deploy_config_dir = os.path.join(project_path, 'deploy', 'config')
    mounts = get_config_mounts(deploy_config_dir)

    # 构建 volumes 配置
    volumes_yaml = ""
    if mounts:
        volumes_yaml = "    volumes:\n"
        for mount in mounts:
            volumes_yaml += f"      - {mount['local']}:{mount['container']}:ro\n"

    compose = f'''version: "3.8"

services:
  app:
    build:
      context: ..
      dockerfile: deploy/Dockerfile
    image: ${{APP_NAME:-myapp}}:latest
    container_name: ${{APP_NAME:-myapp}}
    ports:
      - "${{APP_PORT:-{app_port}}}:${{APP_PORT:-{app_port}}}"
    env_file:
      - .env
{volumes_yaml}    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:${{APP_PORT:-{app_port}}}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
'''

    return compose


def generate_build_compose(project_path):
    """生成 compose.build.yaml 文件"""
    compose = '''version: "3.8"

services:
  builder:
    build:
      context: ..
      dockerfile: deploy/Dockerfile.build
    image: myapp-builder:latest
    volumes:
      - ./artifacts:/artifacts
    command: cp -r /output/. /artifacts/

# 使用方法:
# docker compose -f compose.build.yaml up --build
# 制品将输出到 deploy/artifacts/ 目录
'''
    return compose


def generate_quickstart(project_path):
    """生成快速开始文档"""
    content = '''# 快速开始

## 一键部署命令

```bash
# 1. 进入部署目录
cd deploy

# 2. 代码打包
docker compose -f compose.build.yaml up --build

# 3. 启动服务
docker compose up -d

# 4. 查看日志
docker compose logs -f
```

## 分步操作

### 代码打包

```bash
cd deploy
docker compose -f compose.build.yaml up --build
```

打包完成后，制品将存放在 `deploy/artifacts/` 目录。

### 构建部署镜像

```bash
cd deploy
docker build -t myapp:latest -f Dockerfile ..
```

### 启动容器

使用 Docker Compose：
```bash
cd deploy
docker compose up -d
```

或使用 docker run：
```bash
cd deploy
./docker-run.sh
```

## 验证部署

```bash
# 检查容器状态
docker ps

# 查看应用日志
docker compose logs -f
# 或
docker logs -f myapp

# 测试健康检查端点
curl http://localhost:8080/health
```

## 停止服务

```bash
# 使用 Docker Compose
docker compose down

# 或使用 docker run 的停止命令
docker stop myapp
docker rm myapp
```

## 重新部署

```bash
# 1. 停止现有服务
docker compose down

# 2. 重新打包（如果需要）
docker compose -f compose.build.yaml up --build

# 3. 重新构建镜像
docker compose build --no-cache

# 4. 启动服务
docker compose up -d
```
'''

    quickstart_path = os.path.join(project_path, 'deploy', 'QUICKSTART.md')
    with open(quickstart_path, 'w') as f:
        f.write(content)

    return quickstart_path


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python generate_deployment.py <项目路径> [应用端口]")
        sys.exit(1)

    project_path = sys.argv[1]
    app_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

    deploy_dir = os.path.join(project_path, 'deploy')
    os.makedirs(deploy_dir, exist_ok=True)

    # 生成 docker-run.sh
    docker_run = generate_docker_run_script(project_path, app_port)
    docker_run_path = os.path.join(deploy_dir, 'docker-run.sh')
    with open(docker_run_path, 'w') as f:
        f.write(docker_run)

    # 添加执行权限（在类 Unix 系统上）
    try:
        os.chmod(docker_run_path, 0o755)
    except:
        pass

    print(f"docker-run.sh 已生成: {docker_run_path}")

    # 生成 compose.yaml
    compose = generate_compose_yaml(project_path, app_port)
    compose_path = os.path.join(deploy_dir, 'compose.yaml')
    with open(compose_path, 'w') as f:
        f.write(compose)

    print(f"compose.yaml 已生成: {compose_path}")

    # 生成 compose.build.yaml
    build_compose = generate_build_compose(project_path)
    build_compose_path = os.path.join(deploy_dir, 'compose.build.yaml')
    with open(build_compose_path, 'w') as f:
        f.write(build_compose)

    print(f"compose.build.yaml 已生成: {build_compose_path}")

    # 生成快速开始文档
    quickstart_path = generate_quickstart(project_path)
    print(f"QUICKSTART.md 已生成: {quickstart_path}")


if __name__ == '__main__':
    main()
