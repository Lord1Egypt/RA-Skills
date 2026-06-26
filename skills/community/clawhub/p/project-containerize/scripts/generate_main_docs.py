#!/usr/bin/env python3
"""
生成主文档 - 阶段6
生成 CONTAINERIZATION.md 等完整说明文档
"""

import os


def generate_containerization_md(project_path, project_type, app_port=8080):
    """生成主文档 CONTAINERIZATION.md"""

    # 检测是否有配置文件
    config_dir = os.path.join(project_path, 'deploy', 'config')
    has_configs = os.path.exists(config_dir) and os.listdir(config_dir)

    content = f'''# 项目容器化说明文档

本文档详细说明如何对项目进行代码打包、构建容器镜像和部署。

---

## 1. 项目概述

### 1.1 项目信息

- **项目类型**: {project_type}
- **默认端口**: {app_port}
- **容器化方案版本**: 4.0

### 1.2 目录结构说明

```
deploy/
├── Dockerfile                    # 部署用 Dockerfile（仅制品，无源码）
├── Dockerfile.build              # 打包用 Dockerfile
├── compose.yaml                  # 部署编排（含配置挂载）
├── compose.build.yaml            # 打包编排
├── docker-run.sh                 # 部署脚本
├── .env                          # 环境变量配置
├── artifacts/                    # 打包制品目录
├── config/                       # 配置文件目录
│   └── [项目原有配置文件]
├── CONTAINERIZATION.md           # 本文档
├── QUICKSTART.md                 # 快速参考
├── BUILD.md                      # 打包说明
├── DEPLOY.md                     # 部署说明
├── CONFIG.md                     # 配置说明
└── analysis-report.md            # 项目分析报告
```

---

## 2. 代码打包

### 2.1 打包流程

代码打包使用专门的打包 Dockerfile（`Dockerfile.build`），将源代码编译/构建为可部署的制品。

### 2.2 执行打包

```bash
# 进入部署目录
cd deploy

# 执行打包
docker compose -f compose.build.yaml up --build
```

打包完成后，制品将存放在 `deploy/artifacts/` 目录。

### 2.3 制品说明

根据项目类型不同，制品内容有所差异：

| 项目类型 | 制品内容 | 制品路径 |
|---------|---------|---------|
| Java | JAR 文件 | `artifacts/app.jar` |
| Node.js 前端 | 静态文件 | `artifacts/dist/` |
| Node.js 后端 | 依赖+源码 | `artifacts/node_modules/` |
| Python | 源码+依赖 | `artifacts/source/` |
| Go | 二进制文件 | `artifacts/app` |

### 2.4 详细说明

详见 [BUILD.md](BUILD.md)

---

## 3. 容器镜像构建

### 3.1 部署 Dockerfile 说明

部署用的 Dockerfile（`Dockerfile`）遵循以下原则：

1. **仅复制制品**：禁止将源代码复制到容器内
2. **最小依赖**：只安装运行软件所必需的额外软件
3. **用户权限**：默认使用 **root** 用户运行组件
4. **遵循项目要求**：如果项目文档明确要求使用非 root 用户，请参考 DEPLOY.md 进行调整

### 3.2 构建镜像

```bash
# 进入部署目录
cd deploy

# 构建镜像
docker build -t myapp:latest -f Dockerfile ..
```

### 3.3 详细说明

详见 [DEPLOY.md](DEPLOY.md)

---

## 4. 配置管理

### 4.1 配置文件清单

'''

    if has_configs:
        content += "项目原有的配置文件已复制到 `deploy/config/` 目录：\n\n"
        for item in os.listdir(config_dir):
            content += f"- `config/{item}`\n"
        content += "\n"
    else:
        content += "项目未检测到专用配置文件。\n\n"

    content += f'''### 4.2 配置文件挂载

在部署时，配置文件将挂载到容器内的指定路径：

| 本地路径 | 容器内路径 | 说明 |
|---------|-----------|------|
'''

    if has_configs:
        for item in os.listdir(config_dir):
            if os.path.isfile(os.path.join(config_dir, item)):
                if 'application' in item.lower():
                    container_path = f"/app/config/{item}"
                elif 'nginx' in item.lower():
                    container_path = f"/etc/nginx/conf.d/{item}"
                else:
                    container_path = f"/app/config/{item}"
                content += f"| `config/{item}` | `{container_path}` | 应用配置 |\n"

    content += f'''
### 4.3 环境变量

环境变量配置在 `.env` 文件中，主要包括：

- `APP_NAME` - 应用名称
- `APP_PORT` - 应用端口（默认 {app_port}）
- `LOG_LEVEL` - 日志级别
- 数据库、缓存、消息队列等连接配置

### 4.4 详细说明

详见 [CONFIG.md](CONFIG.md)

---

## 5. 部署指南

### 5.1 使用 Docker Compose 部署（推荐）

```bash
# 进入部署目录
cd deploy

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

### 5.2 使用 docker run 部署

```bash
# 进入部署目录
cd deploy

# 执行部署脚本
./docker-run.sh

# 或手动运行
docker run -d \\
  --name myapp \\
  -p "{app_port}:{app_port}" \\
'''

    if has_configs:
        for item in os.listdir(config_dir):
            if os.path.isfile(os.path.join(config_dir, item)):
                if 'application' in item.lower():
                    container_path = f"/app/config/{item}"
                elif 'nginx' in item.lower():
                    container_path = f"/etc/nginx/conf.d/{item}"
                else:
                    container_path = f"/app/config/{item}"
                content += f"  -v \"./config/{item}:{container_path}:ro" + "\\" + f"""
'''

    content += f'''  --env-file .env \\
  myapp:latest
```

### 5.3 验证部署

```bash
# 检查容器状态
docker ps

# 查看应用日志
docker logs -f myapp

# 测试健康检查端点
curl http://localhost:{app_port}/health
```

### 5.4 详细说明

详见 [DEPLOY.md](DEPLOY.md)

---

## 6. 快速参考

### 6.1 常用命令

```bash
# 代码打包
docker compose -f compose.build.yaml up --build

# 构建部署镜像
docker build -t myapp:latest -f Dockerfile ..

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 重新构建并启动
docker compose up -d --build
```

### 6.2 故障排查

| 问题 | 排查方法 |
|-----|---------|
| 容器无法启动 | `docker logs myapp` 查看错误日志 |
| 配置未生效 | 检查配置文件挂载路径是否正确 |
| 端口冲突 | 修改 `.env` 中的 `APP_PORT` |
| 权限问题 | 检查配置文件是否有读取权限 |

---

## 7. 注意事项

1. **制品管理**：`artifacts/` 目录包含打包产物，不应提交到版本控制
2. **敏感信息**：`.env` 文件可能包含敏感信息，不应提交到版本控制
3. **配置文件**：`config/` 目录下的配置文件使用只读挂载（`:ro`），容器内无法修改
4. **重新打包**：代码修改后需要重新执行打包流程
5. **用户权限**：默认使用 root 用户运行，如需非 root 用户请参考项目文档调整

---

## 8. 相关文档

- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [BUILD.md](BUILD.md) - 代码打包详细说明
- [DEPLOY.md](DEPLOY.md) - 部署详细说明
- [CONFIG.md](CONFIG.md) - 配置管理说明
- [analysis-report.md](analysis-report.md) - 项目分析报告
'''

    return content


def generate_build_md(project_path, project_type):
    """生成打包说明文档"""
    content = f'''# 代码打包说明

本文档说明如何对项目进行代码打包。

## 打包流程

代码打包使用 `Dockerfile.build` 和 `compose.build.yaml`，将源代码构建为可部署的制品。

## 前置条件

- Docker 已安装
- Docker Compose 已安装
- 项目源代码完整

## 执行打包

```bash
# 进入部署目录
cd deploy

# 执行打包
docker compose -f compose.build.yaml up --build
```

打包完成后，制品将存放在 `artifacts/` 目录。

## 制品说明

项目类型：**{project_type}**

'''

    if 'java' in project_type.lower():
        content += '''制品内容：
- `artifacts/app.jar` - 可运行的 JAR 文件

制品检查：
```bash
# 检查 JAR 文件是否存在
ls -lh artifacts/app.jar

# 查看 JAR 内容
jar tf artifacts/app.jar | head -20
```
'''
    elif 'node' in project_type.lower():
        content += '''制品内容：
- `artifacts/dist/` - 前端构建产物（静态文件）
- 或 `artifacts/node_modules/` - Node.js 依赖

制品检查：
```bash
# 检查构建产物
ls -la artifacts/dist/

# 检查文件大小
du -sh artifacts/dist/
```
'''
    elif 'python' in project_type.lower():
        content += '''制品内容：
- `artifacts/source/` - Python 源码
- `artifacts/python-packages/` - Python 依赖包

制品检查：
```bash
# 检查源码
ls -la artifacts/source/

# 检查依赖
ls artifacts/python-packages/lib/python*/site-packages/ | head -20
```
'''
    elif 'go' in project_type.lower():
        content += '''制品内容：
- `artifacts/app` - 编译后的二进制文件

制品检查：
```bash
# 检查二进制文件
ls -lh artifacts/app
file artifacts/app
```
'''
    else:
        content += '''制品内容：
- 请查看 `artifacts/` 目录了解具体制品

制品检查：
```bash
ls -la artifacts/
```
'''

    content += '''
## 常见问题

### 打包失败

1. 检查 Docker 服务是否正常运行
2. 检查网络连接（需要下载基础镜像和依赖）
3. 查看详细的构建日志：`docker compose -f compose.build.yaml build --no-cache --progress=plain`

### 制品缺失

1. 检查 `Dockerfile.build` 中的构建命令是否正确
2. 检查 `compose.build.yaml` 中的 volume 挂载配置
3. 检查构建日志中是否有错误

### 重新打包

```bash
# 清理旧制品
rm -rf artifacts/*

# 重新打包
docker compose -f compose.build.yaml up --build
```
'''

    return content


def generate_deploy_md(project_path, project_type, app_port=8080):
    """生成部署说明文档"""
    content = f'''# 部署说明

本文档说明如何部署容器化应用。

## 前置条件

1. 已完成代码打包（`artifacts/` 目录存在制品）
2. 已配置环境变量（`.env` 文件）
3. 已准备配置文件（`config/` 目录）

## 构建部署镜像

```bash
# 进入部署目录
cd deploy

# 构建镜像
docker build -t myapp:latest -f Dockerfile ..
```

## 部署方式

### 方式一：Docker Compose（推荐）

```bash
# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

### 方式二：docker run

```bash
# 使用脚本部署
./docker-run.sh

# 或手动运行（根据实际配置调整）
docker run -d \\
  --name myapp \\
  -p "{app_port}:{app_port}" \\
  --env-file .env \\
  myapp:latest
```

## 用户权限说明

**默认配置**：容器内使用 **root** 用户运行组件。

如果项目文档明确要求使用非 root 用户运行，请修改 `Dockerfile`：

```dockerfile
# 在 Dockerfile 中添加
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -s /bin/sh -D appuser
USER appuser
```

然后重新构建镜像：
```bash
docker build -t myapp:latest -f Dockerfile ..
```

## 验证部署

```bash
# 检查容器状态
docker ps

# 查看应用日志
docker logs -f myapp

# 测试健康检查端点
curl http://localhost:{app_port}/health

# 进入容器内部（调试用）
docker exec -it myapp sh
```

## 环境变量

主要环境变量说明：

| 变量名 | 默认值 | 说明 |
|-------|-------|------|
| `APP_NAME` | myapp | 应用名称 |
| `APP_PORT` | {app_port} | 应用端口 |
| `LOG_LEVEL` | info | 日志级别 |

详见 `.env` 文件。

## 端口映射

默认端口映射：`{app_port}:{app_port}`

如需修改，编辑 `.env` 文件：
```bash
APP_PORT=9090
```

然后重新部署。

## 配置文件挂载

配置文件通过 volume 挂载到容器内：

- 本地 `config/` 目录下的文件挂载到容器内的指定路径
- 挂载使用只读模式（`:ro`），容器内无法修改配置
- 修改本地配置文件后，需要重启容器生效

## 常见问题

### 容器无法启动

1. 检查日志：`docker logs myapp`
2. 检查端口是否被占用：`netstat -tlnp | grep {app_port}`
3. 检查环境变量配置是否正确

### 配置未生效

1. 检查配置文件挂载路径是否正确
2. 检查配置文件格式是否正确
3. 重启容器：`docker restart myapp`

### 权限问题

1. 检查配置文件是否有读取权限
2. 检查 `artifacts/` 目录下的制品权限
3. 如需非 root 用户，参考上面的用户权限说明

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

    return content


def main():
    import sys
    if len(sys.argv) < 3:
        print("用法: python generate_main_docs.py <项目路径> <项目类型> [应用端口]")
        sys.exit(1)

    project_path = sys.argv[1]
    project_type = sys.argv[2]
    app_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080

    deploy_dir = os.path.join(project_path, 'deploy')
    os.makedirs(deploy_dir, exist_ok=True)

    # 生成主文档
    main_doc = generate_containerization_md(project_path, project_type, app_port)
    main_doc_path = os.path.join(deploy_dir, 'CONTAINERIZATION.md')
    with open(main_doc_path, 'w', encoding='utf-8') as f:
        f.write(main_doc)
    print(f"CONTAINERIZATION.md 已生成: {main_doc_path}")

    # 生成打包说明
    build_doc = generate_build_md(project_path, project_type)
    build_doc_path = os.path.join(deploy_dir, 'BUILD.md')
    with open(build_doc_path, 'w', encoding='utf-8') as f:
        f.write(build_doc)
    print(f"BUILD.md 已生成: {build_doc_path}")

    # 生成部署说明
    deploy_doc = generate_deploy_md(project_path, project_type, app_port)
    deploy_doc_path = os.path.join(deploy_dir, 'DEPLOY.md')
    with open(deploy_doc_path, 'w', encoding='utf-8') as f:
        f.write(deploy_doc)
    print(f"DEPLOY.md 已生成: {deploy_doc_path}")


if __name__ == '__main__':
    main()
