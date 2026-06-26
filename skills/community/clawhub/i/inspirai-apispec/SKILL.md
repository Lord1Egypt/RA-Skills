---
name: inspirai-apispec
description: "API 规范管理工具 - 跨项目 API 文档的初始化、更新、查询与搜索。Triggers: 'API文档', 'API规范', '接口文档', '路由解析', 'apispec', 'API lookup', 'API search'."
version: 1.0.0
license: MIT
---

# API 规范管理工具

跨项目 API 文档的初始化、更新、查询与搜索。包含四个功能模块：init（初始化）、lookup（查询）、search（搜索）、update（更新）。

---

## 1. Init - 初始化项目 API 文档配置

初始化当前后端项目的 API 文档配置，生成 `.api-spec.yaml` 文件。

### 使用方式

```
apispec init
```

### 执行步骤

#### Step 1: 检测项目类型

检查项目结构，识别后端框架：

```bash
# Go 项目
if [ -f "go.mod" ]; then
    PROJECT_TYPE="go"
    ROUTES_FILE=$(find . -name "routes.go" -o -name "router.go" | head -1)
fi

# Node.js 项目
if [ -f "package.json" ]; then
    PROJECT_TYPE="node"
    ROUTES_FILE=$(find . -name "routes.ts" -o -name "routes.js" -o -name "router.ts" | head -1)
fi

# Python 项目
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="python"
    ROUTES_FILE=$(find . -name "urls.py" -o -name "routes.py" | head -1)
fi
```

#### Step 2: 收集项目信息

使用 AskUserQuestion 工具询问以下信息（如果无法自动检测）：

1. **项目名称** - 用于在 API 规范仓库中创建目录
2. **Base URL** - 生产环境的 API 地址
3. **路由文件位置** - 如果自动检测不准确

#### Step 3: 生成配置文件

在项目根目录创建 `.api-spec.yaml`：

```yaml
# API 规范配置
project_name: {project_name}
description: {description}
base_url: {base_url}

# API 规范仓库位置
spec_repo: ~/.apispec/registry

# 路由文件位置（用于解析 API）
routes_file: {routes_file}

# 项目类型
project_type: {go|node|python}
```

#### Step 4: 确认配置

显示生成的配置文件内容，询问用户确认。

### 输出

- 在项目根目录创建 `.api-spec.yaml` 文件
- 将 `.api-spec.yaml` 添加到 `.gitignore`（可选）

### 注意事项

- 如果 `.api-spec.yaml` 已存在，询问是否覆盖
- spec_repo 默认为 `~/.apispec/registry`
- 需确保 API specs 仓库已 clone 到该目录

---

## 2. Lookup - 查询 API 文档

查询项目的 API 文档，支持列出所有项目、查看项目 API 列表、查看具体 API 详情。

### 使用方式

```
apispec lookup                              # 列出所有项目
apispec lookup {project}                    # 显示项目的所有 API
apispec lookup {project} {module}           # 显示模块下的 API
apispec lookup {project} {module}/{api}     # 显示具体 API 详情
```

### 示例

```
apispec lookup                              # 列出所有项目
apispec lookup myapp                        # 显示 myapp 的所有 API
apispec lookup myapp auth                   # 显示 auth 模块的 API
apispec lookup myapp auth/sms-login         # 显示 sms-login 的详细文档
```

### 执行步骤

#### Step 1: 定位规范仓库

默认路径：`~/.apispec/registry`

如果目录不存在，提示用户 clone 仓库：
```bash
mkdir -p ~/.apispec
git clone <your-api-specs-repo> ~/.apispec/registry
```

#### Step 2: 拉取最新

```bash
cd {spec_repo}
git pull origin main --quiet
```

#### Step 3: 根据参数查询

**无参数 - 列出所有项目：**

读取 `meta.yaml`，格式化输出：

```
API Specifications Registry

Projects:
  myapp          用户中心服务 - 认证、会员、支付    20 APIs
  another-app    其他项目描述                      12 APIs
```

**一个参数 - 显示项目 API 列表：**

读取 `{project}/meta.yaml`，格式化输出：

```
myapp - 用户中心服务
Base URL: https://api.example.com
Updated: 2026-01-22

APIs (20):
  METHOD  ENDPOINT                        AUTH  SUMMARY
  POST    /api/v1/auth/sms/send           -     发送短信验证码
  POST    /api/v1/auth/sms/login          -     短信验证码登录
  GET     /api/v1/user/profile            *     获取用户信息
  PUT     /api/v1/user/profile            *     更新用户信息

* = 需要认证
```

**两个参数（模块）- 显示模块 API：**

筛选显示指定模块的 API。

**完整路径 - 显示 API 详情：**

读取 `{project}/{module}/{api}.yaml`，格式化输出完整的请求/响应信息。

### 输出格式

- 简洁的文本格式，便于快速理解
- 字段对齐，易于阅读
- 只显示必要信息，减少 token 消耗

### 注意事项

- 每次查询前自动 `git pull` 获取最新文档
- 如果项目或 API 不存在，给出友好提示并建议使用 `apispec search` 模糊查找

---

## 3. Search - 模糊搜索 API 文档

跨项目模糊搜索 API 文档，支持按关键词、路径、方法、字段名等维度匹配。

### 使用方式

```
apispec search {keyword}                    # 全局模糊搜索
apispec search --project {name} {keyword}   # 在指定项目中搜索
apispec search --method POST {keyword}      # 按 HTTP 方法过滤
apispec search --field {fieldname}          # 按请求/响应字段名搜索
```

### 示例

```
apispec search login                        # 搜索包含 "login" 的 API
apispec search 验证码                        # 中文关键词搜索
apispec search --method POST user           # 搜索 POST 方法中包含 "user" 的 API
apispec search --field token                # 搜索请求或响应中包含 token 字段的 API
apispec search --project myapp auth         # 在 myapp 项目中搜索 "auth"
```

### 执行步骤

#### Step 1: 定位规范仓库

默认路径：`~/.apispec/registry`

如果目录不存在，提示用户先执行 `apispec init` 并 clone 仓库。

#### Step 2: 拉取最新

```bash
cd {spec_repo}
git pull origin main --quiet
```

#### Step 3: 搜索匹配

搜索范围（按优先级）：

1. **endpoint 路径** - URL 路径中包含关键词
2. **summary/description** - API 描述中包含关键词
3. **请求/响应字段名** - field name 匹配
4. **模块/文件名** - 目录或文件名匹配

搜索逻辑：
```bash
# 遍历所有项目的 meta.yaml 和 API 文件
for project_dir in {spec_repo}/*/; do
    # 读取 meta.yaml 中的 API 列表快速匹配
    # 如果 meta 匹配不够，深入读取具体 API 文件
done
```

支持多关键词（AND 逻辑）：
```
apispec search POST login    # 匹配同时包含 POST 和 login 的 API
```

#### Step 4: 格式化输出

**匹配结果格式：**

```
搜索 "login" - 找到 3 个匹配：

  METHOD  PROJECT      ENDPOINT                     SUMMARY
  POST    myapp        /api/v1/auth/sms/login       短信验证码登录
  POST    myapp        /api/v1/auth/wechat/login    微信登录
  POST    another-app  /api/v1/login                密码登录

提示：使用 apispec lookup myapp auth/sms-login 查看详情
```

**无匹配时：**

```
搜索 "xyz" - 未找到匹配的 API

建议：
  - 尝试更短的关键词
  - 使用 apispec lookup 浏览项目列表
  - 检查拼写是否正确
```

**字段搜索结果：**

```
搜索字段 "token" - 找到 5 个匹配：

  METHOD  PROJECT  ENDPOINT                   字段位置     字段类型
  POST    myapp    /api/v1/auth/sms/login     response    string
  POST    myapp    /api/v1/auth/wechat/login  response    string
  POST    myapp    /api/v1/auth/refresh       request     string
  GET     myapp    /api/v1/user/profile       request.header  string
  DELETE  myapp    /api/v1/auth/logout        request.header  string

提示：使用 apispec lookup myapp auth/sms-login 查看完整 API 定义
```

### 注意事项

- 搜索不区分大小写
- 支持中英文关键词
- 结果按相关度排序（endpoint 匹配 > summary 匹配 > field 匹配）
- 最多显示 20 条结果，超出时提示缩小搜索范围
- 每次搜索前自动 `git pull` 获取最新文档

---

## 4. Update - 更新 API 文档

解析当前项目的路由和 handler，生成/更新 API 文档到规范仓库。

### 使用方式

```
apispec update              # 更新所有 API
apispec update auth         # 只更新 auth 模块
```

### 前置条件

- 项目已执行 `apispec init`，存在 `.api-spec.yaml` 配置文件
- API specs 仓库已 clone 到本地

### 执行步骤

#### Step 1: 读取配置

```bash
if [ ! -f ".api-spec.yaml" ]; then
    echo "错误：未找到 .api-spec.yaml，请先执行 apispec init"
    exit 1
fi
```

#### Step 2: 解析路由文件

根据项目类型解析路由：

**Go 项目：**
- 解析 `routes.go` 中的 `mux.HandleFunc` 和 `mux.Handle` 调用
- 提取 HTTP 方法、路径、handler 函数名
- 读取对应的 handler 文件，提取请求/响应结构体

**Node.js 项目：**
- 解析 `router.get/post/put/delete` 调用
- 提取路由和 handler

**Python 项目：**
- 解析 `urlpatterns` 或 Flask/FastAPI 路由装饰器

#### Step 3: 生成 API 文档

为每个 API 生成 YAML 文件：

```
{spec_repo}/{project_name}/
├── meta.yaml           # 项目索引
├── auth/
│   ├── sms-send.yaml
│   └── sms-login.yaml
├── user/
│   └── get-profile.yaml
└── ...
```

**meta.yaml 格式：**
```yaml
project: {project_name}
description: {description}
base_url: {base_url}
updated_at: {timestamp}
apis:
  - path: auth/sms-send
    method: POST
    endpoint: /api/v1/auth/sms/send
    auth: false
    summary: 发送短信验证码
```

**单个 API 文件格式：**
```yaml
endpoint: /api/v1/auth/sms/login
method: POST
summary: 短信验证码登录
auth: false
description: 使用手机号和短信验证码登录

request:
  content_type: application/json
  fields:
    - name: phone
      type: string
      required: true
      description: 手机号

response:
  success:
    status: 200
    fields:
      - name: token
        type: string
        description: JWT token
  errors:
    - status: 400
      error: invalid_code
      description: 验证码错误
```

#### Step 4: 更新全局索引

更新 `{spec_repo}/meta.yaml`：

```yaml
projects:
  {project_name}:
    description: {description}
    base_url: {base_url}
    api_count: {count}
    updated_at: {timestamp}
```

#### Step 5: 提交并推送

```bash
cd {spec_repo}
git add -A
git commit -m "docs: update {project_name} API specs"
git push origin main
```

### 输出

- 更新 `{spec_repo}/{project_name}/` 目录下的所有 API 文档
- 自动 commit 并 push 到远程仓库
- 显示更新摘要（新增/修改/删除的 API 数量）
