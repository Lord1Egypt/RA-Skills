---
title: "项目容器化适配"
description: "对项目进行完整的容器化适配。自动检测分析项目代码和文档，配置和优化代码容器化打包方案，生成专用Dockerfile，生成专用compose.yaml用于快捷部署，输出说明文档，最终生成适配项目的容器化部署方案。触发词：容器化、Docker、docker run、docker-compose、Dockerfile、容器部署、镜像打包、生成 Dockerfile、创建 Dockerfile、自动 Dockerfile、项目容器化、容器化适配、容器化改造"
author: "AI Assistant"
version: "4.0"
---

# 项目容器化适配

本 Skill 用于分析项目代码结构，生成代码打包和容器化部署所需的完整方案。

## 工作流程

### 阶段1：分析项目代码

**目标**：全面了解项目结构、技术栈、文档和现有配置

1. **分析项目结构**
   - 使用 `list_dir` 查看项目根目录结构
   - 识别项目类型（Python/Node.js/Java/Go/Rust/PHP/Ruby/其他）
   - 检测是否为多组件/微服务项目
   - 识别各组件目录（如 `services/`、`apps/`、`packages/`、`src/` 等）

2. **分析项目文档**
   - 读取 `README.md` 了解项目概述
   - 查找并分析部署相关文档：
     - `DEPLOY.md`、`deploy.md`、`部署指南.md`
     - `INSTALL.md`、`install.md`、`安装说明.md`
     - `docs/deploy*`、`docs/install*`
   - 查找配置参考文档：
     - `CONFIG.md`、`config.md`、`配置说明.md`
     - `.env.example`、`.env.template`
     - `application*.yml`、`application*.yaml`、`application*.properties`（Java）
     - `config/` 目录下的配置文件

3. **分析现有 Dockerfile**
   - 搜索项目中的 Dockerfile：`search_file` 查找 `**/Dockerfile*`
   - 读取每个 Dockerfile 内容
   - **分类 Dockerfile 用途**：
     - **打包用**：包含 `FROM maven`、`FROM node`、`pip install`、`npm install`、`mvn build` 等构建指令
     - **部署用**：仅包含 `COPY`、`ADD` 制品、设置运行环境
     - **开发用**：包含 `VOLUME`、调试工具、热重载配置
     - **其他**：如数据库初始化、工具镜像等
   - 记录现有 Dockerfile 的基础镜像、暴露端口、环境变量等关键信息

4. **分析配置文件**
   - 识别各组件使用的配置文件：
     - 环境变量文件：`.env*`、`config.env`
     - 应用配置文件：`*.yml`、`*.yaml`、`*.json`、`*.properties`、`*.conf`
     - 专用配置目录：`config/`、`conf/`、`settings/`
   - 记录配置文件路径和用途
   - 分析配置文件中哪些需要外部化（数据库连接、API 密钥等）

5. **输出分析报告**
   - 创建 `deploy/analysis-report.md`，包含：
     - 项目类型和技术栈
     - 组件结构（如果是多组件项目）
     - 现有 Dockerfile 分析（类型、用途、可复用性）
     - 配置文件清单及挂载建议
     - 部署依赖（数据库、缓存、消息队列等）

---

### 阶段2：项目代码打包

**目标**：创建打包环境，生成可部署的制品

1. **确定制品类型**
   根据项目语言确定打包产物：

   | 语言 | 制品类型 | 制品路径示例 |
     |------|---------|-------------|
   | Java (Maven) | JAR 文件 | `target/*.jar` |
   | Java (Gradle) | JAR 文件 | `build/libs/*.jar` |
   | Node.js (前端) | 静态文件 | `dist/`、`build/` |
   | Node.js (后端) | 源码+依赖 | `node_modules/` + `src/` |
   | Python | 源码+依赖 | `*.py` + `requirements.txt` |
   | Go | 二进制文件 | `bin/`、`*` (可执行文件) |
   | Rust | 二进制文件 | `target/release/*` |
   | PHP | 源码 | `*.php`、`public/` |
   | Ruby | 源码+Gem | `*.rb`、`Gemfile*` |

2. **创建打包 Dockerfile**
   - 文件路径：`deploy/Dockerfile.build`
   - 基础镜像选择项目实际使用的版本：
     - Python：`python:{version}-slim`
     - Node.js：`node:{version}-alpine`
     - Java：`maven:{version}-eclipse-temurin-{jdk}-alpine` 或 `gradle:{version}-jdk{jdk}-alpine`
     - Go：`golang:{version}-alpine`
     - Rust：`rust:{version}-alpine`
   - 包含完整的构建步骤
   - 使用多阶段构建，最终阶段只保留制品

3. **创建打包 Compose 文件**
   - 文件路径：`deploy/compose.build.yaml`
   - 配置 volume 将制品导出到本地 `deploy/artifacts/` 目录
   - 示例：
     ```yaml
     services:
       builder:
         build:
           context: ..
           dockerfile: deploy/Dockerfile.build
         volumes:
           - ./artifacts:/output
     ```

4. **执行打包**
   - 使用 `execute_command` 运行：`docker compose -f deploy/compose.build.yaml up --build`
   - 确认制品已生成在 `deploy/artifacts/` 目录

5. **创建打包说明文档**
   - 文件路径：`deploy/BUILD.md`
   - 包含：
     - 打包前置条件
     - 打包命令
     - 制品说明
     - 常见问题排查

---

### 阶段3：创建项目组件部署用的 Dockerfile

**目标**：创建仅用于运行制品的最小化 Dockerfile

**核心原则**：
1. **仅复制制品**：禁止将源代码复制到容器内
2. **最小依赖**：只安装运行软件所必需的额外软件
3. **遵循项目要求**：如果项目明确要求使用非 root 用户，则配置非 root 用户；**默认使用 root 用户**
4. **保留必要脚本**：如果项目要求必须使用特定脚本或文件，按要求复制到容器中

1. **创建部署 Dockerfile**
   - 文件路径：`deploy/Dockerfile`
   - 基础镜像选择运行时用镜像：
     - Java：`eclipse-temurin:{jdk}-jre-alpine`
     - Node.js：`node:{version}-alpine`
     - Python：`python:{version}-slim`
     - Go：`gcr.io/distroless/static:nonroot` 或 `alpine:latest`
     - 前端静态：`nginx:alpine`
   - **用户配置策略**：
     - 检查阶段1分析结果中是否有用户运行要求
     - 如果项目文档明确要求非 root 运行，添加：
       ```dockerfile
       RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -s /bin/sh -D appuser
       USER appuser
       ```
     - **否则，默认使用 root 用户运行**
   - 只从 `artifacts/` 复制制品
   - 暴露必要的端口
   - 设置健康检查（如果适用）

2. **创建部署说明文档**
   - 文件路径：`deploy/DEPLOY.md`
   - 包含：
     - 镜像构建命令
     - 运行命令
     - 环境变量说明
     - 端口映射说明

---

### 阶段4：生成模板配置文件

**目标**：根据阶段1的分析，准备配置文件模板

1. **分析配置需求**
   - 参考阶段1的分析报告中的配置文件清单
   - 识别需要外部化的配置项（数据库连接、API 密钥、服务地址等）

2. **复制原有配置文件**
   - 如果组件有专用的配置文件（如 `application.yml`、`config.json`、`.env` 等）：
     - 将原有配置文件复制到 `deploy/config/` 目录
     - 保持原有文件结构和命名
   - 示例：
     ```
     deploy/config/
     ├── application.yml          # 从项目 src/main/resources/ 复制
     ├── logback.xml             # 从项目 src/main/resources/ 复制
     └── nginx.conf              # 如果是前端项目
     ```

3. **创建环境变量模板**
   - 文件路径：`deploy/.env`
   - 包含所有需要外部化的配置项
   - 示例：
     ```bash
     # 数据库配置
     DB_HOST=localhost
     DB_PORT=3306
     DB_NAME=myapp
     DB_USER=root
     DB_PASSWORD=changeme

     # 应用配置
     APP_PORT=8080
     LOG_LEVEL=info
     ```

4. **创建配置说明文档**
   - 文件路径：`deploy/CONFIG.md`
   - 包含：
     - 配置文件清单及用途
     - 每个配置项的说明
     - 如何修改配置
     - 配置热加载说明（如果支持）

---

### 阶段5：生成标准部署方案

**目标**：生成完整的部署脚本和编排文件，包含配置文件挂载

1. **生成 docker-run 脚本**
   - 文件路径：`deploy/docker-run.sh`
   - 包含完整的 `docker run` 命令
   - **必须包含配置文件挂载**：
     ```bash
     docker run -d \
       --name myapp \
       -p 8080:8080 \
       -v "$(pwd)/config/application.yml:/app/config/application.yml:ro" \
       -v "$(pwd)/config/logback.xml:/app/config/logback.xml:ro" \
       --env-file .env \
       myapp:latest
     ```

2. **生成 Compose 文件**
   - 文件路径：`deploy/compose.yaml`
   - 包含：
     - 应用服务配置
     - **配置文件挂载**（参考阶段1分析结果）
     - 环境变量文件引用
     - 端口映射
     - 健康检查
     - 资源限制（可选）
   - 示例：
     ```yaml
     services:
       app:
         build:
           context: ..
           dockerfile: deploy/Dockerfile
         container_name: myapp
         ports:
           - "${APP_PORT:-8080}:8080"
         env_file:
           - .env
         volumes:
           # 挂载配置文件到容器内指定路径
           - ./config/application.yml:/app/config/application.yml:ro
           - ./config/logback.xml:/app/config/logback.xml:ro
         healthcheck:
           test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
           interval: 30s
           timeout: 10s
           retries: 3
         restart: unless-stopped
     ```

3. **创建快速参考文档**
   - 文件路径：`deploy/QUICKSTART.md`
   - 包含一键部署命令

---

### 阶段6：输出标准文档

**目标**：生成完整的容器化说明文档

1. **创建主文档 CONTAINERIZATION.md**
   - 文件路径：`deploy/CONTAINERIZATION.md`
   - 包含以下章节：

   **1. 项目概述**
   - 项目名称、类型、技术栈
   - 组件结构说明

   **2. 代码打包**
   - 如何执行代码打包
   - 打包命令详解
   - 制品说明
   - 打包 Dockerfile 说明

   **3. 容器镜像构建**
   - 如何构建部署镜像
   - 部署 Dockerfile 说明
   - 用户权限说明（root 或非 root）

   **4. 配置管理**
   - 配置文件清单
   - 配置文件挂载路径说明
   - 如何修改配置
   - 环境变量说明

   **5. 部署指南**
   - 使用 docker run 部署
   - 使用 docker compose 部署
   - 验证部署成功的方法

   **6. 目录结构说明**
   ```
   deploy/
   ├── Dockerfile              # 部署用 Dockerfile
   ├── Dockerfile.build        # 打包用 Dockerfile
   ├── compose.yaml            # 部署编排
   ├── compose.build.yaml      # 打包编排
   ├── docker-run.sh           # 部署脚本
   ├── .env                    # 环境变量
   ├── artifacts/              # 打包制品
   ├── config/                 # 配置文件目录
   │   ├── application.yml     # 应用配置
   │   └── ...
   ├── CONTAINERIZATION.md     # 本文档
   ├── QUICKSTART.md           # 快速参考
   ├── BUILD.md                # 打包说明
   ├── DEPLOY.md               # 部署说明
   ├── CONFIG.md               # 配置说明
   └── analysis-report.md      # 分析报告
   ```

2. **创建快速开始文档**
   - 文件路径：`deploy/QUICKSTART.md`
   - 包含一键命令：
     ```bash
     # 1. 代码打包
     cd deploy && docker compose -f compose.build.yaml up --build

     # 2. 启动服务
     docker compose up -d
     ```

3. **汇总所有文档**
   - 确保所有文档相互引用，形成完整的文档体系

---

## 输出文件清单

执行本 Skill 后，将在项目目录下创建以下结构：

```
deploy/
├── Dockerfile                    # 部署用 Dockerfile（仅制品）
├── Dockerfile.build              # 打包用 Dockerfile
├── compose.yaml                  # 部署编排（含配置挂载）
├── compose.build.yaml            # 打包编排
├── docker-run.sh                 # 部署脚本
├── .env                          # 环境变量
├── artifacts/                    # 打包制品目录
├── config/                       # 配置文件目录
│   ├── .env.template
│   └── [项目原有配置文件]
├── CONTAINERIZATION.md           # ⭐ 完整容器化说明
├── QUICKSTART.md                 # 快速参考
├── BUILD.md                      # 打包说明
├── DEPLOY.md                     # 部署说明
├── CONFIG.md                     # 配置说明
└── analysis-report.md            # 阶段1分析报告
```

---

## 制品类型参考

| 项目类型 | 打包制品 | 部署基础镜像 | 备注 |
|---------|---------|-------------|------|
| Java (Maven/Gradle) | JAR 文件 | `eclipse-temurin:{jdk}-jre-alpine` | 多阶段构建 |
| Node.js 前端 | `dist/` 或 `build/` | `nginx:alpine` | 静态文件服务 |
| Node.js 后端 | `node_modules/` + 源码 | `node:{version}-alpine` | 包含依赖 |
| Python | 源码 + 依赖 | `python:{version}-slim` | pip 安装依赖 |
| Go | 二进制文件 | `gcr.io/distroless/static` 或 `alpine` | 静态编译 |
| Rust | 二进制文件 | `debian:slim` 或 `alpine` | 静态链接 |
| PHP | 源码 | `php:{version}-apache` 或 `nginx:alpine` | 预装扩展 |
| Ruby | 源码 + Gem | `ruby:{version}-slim` | bundle 安装 |

---

## 用户权限策略

- **默认情况**：容器内使用 **root** 用户运行组件
- **非 root 情况**：仅在项目文档明确要求时使用非 root 用户
- 在 `DEPLOY.md` 和 `CONTAINERIZATION.md` 中明确说明使用的用户权限

---

## 配置文件挂载策略

1. **分析阶段**：识别所有配置文件及其在容器内的预期路径
2. **准备阶段**：将原有配置文件复制到 `deploy/config/` 目录
3. **部署阶段**：在 compose.yaml 和 docker-run.sh 中挂载配置文件
4. **文档阶段**：在 `CONFIG.md` 和 `CONTAINERIZATION.md` 中详细说明：
   - 配置文件清单
   - 容器内挂载路径
   - 如何修改配置
   - 配置生效方式（重启/热加载）
