# 技术栈检测方法

> 如何自动识别项目使用的技术栈

## 检测流程

```
1. 扫描项目根目录
2. 识别配置文件
3. 解析依赖声明
4. 推断技术栈
5. 生成技术清单
```

---

## 配置文件识别

### 前端项目

| 文件 | 技术栈 | 解析方式 |
|------|--------|----------|
| `package.json` | Node.js/前端 | 读取 dependencies |
| `pnpm-lock.yaml` | pnpm | 确认包管理器 |
| `yarn.lock` | Yarn | 确认包管理器 |
| `vite.config.*` | Vite | 构建工具 |
| `webpack.config.*` | Webpack | 构建工具 |
| `tsconfig.json` | TypeScript | 语言 |
| `vue.config.js` | Vue CLI | Vue 项目 |
| `next.config.js` | Next.js | React SSR |
| `nuxt.config.js` | Nuxt.js | Vue SSR |

**package.json 关键字段**:
```json
{
  "dependencies": {
    "vue": "前端框架",
    "react": "前端框架",
    "angular": "前端框架",
    "naive-ui": "UI 组件库",
    "element-plus": "UI 组件库",
    "ant-design-vue": "UI 组件库",
    "pinia": "状态管理",
    "vuex": "状态管理",
    "axios": "HTTP 客户端"
  },
  "devDependencies": {
    "typescript": "类型系统",
    "vite": "构建工具",
    "eslint": "代码检查"
  }
}
```

### 后端项目

| 文件 | 技术栈 | 解析方式 |
|------|--------|----------|
| `pom.xml` | Maven/Java | 读取 dependencies |
| `build.gradle` | Gradle/Java | 读取 dependencies |
| `requirements.txt` | Python | 读取依赖列表 |
| `pyproject.toml` | Python | 读取 dependencies |
| `Cargo.toml` | Rust | 读取 dependencies |
| `go.mod` | Go | 读取 require |
| `Gemfile` | Ruby | 读取 gem |
| `composer.json` | PHP | 读取 require |

**pom.xml 关键依赖识别**:
```xml
<!-- Spring Boot -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    → Spring Boot 框架
</dependency>

<!-- 数据库 -->
<dependency>
    <groupId>mysql</groupId>
    → MySQL 数据库
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    → PostgreSQL 数据库
</dependency>

<!-- 中间件 -->
<dependency>
    <groupId>org.springframework.kafka</groupId>
    → Kafka 消息队列
</dependency>
<dependency>
    <groupId>org.springframework.boot:spring-boot-starter-data-redis</groupId>
    → Redis 缓存
</dependency>
<dependency>
    <groupId>io.minio</groupId>
    → MinIO 对象存储
</dependency>

<!-- 搜索引擎 -->
<dependency>
    <groupId>co.elastic.clients</groupId>
    → Elasticsearch
</dependency>
```

---

## 框架识别规则

### Java 框架

```python
def detect_java_framework(pom_content):
    frameworks = []
    
    if "spring-boot" in pom_content:
        frameworks.append("Spring Boot")
    if "spring-cloud" in pom_content:
        frameworks.append("Spring Cloud")
    if "mybatis" in pom_content:
        frameworks.append("MyBatis")
    if "hibernate" in pom_content:
        frameworks.append("Hibernate/JPA")
    if "dubbo" in pom_content:
        frameworks.append("Dubbo")
    
    return frameworks
```

### 前端框架

```python
def detect_frontend_framework(package_json):
    deps = {**package_json.get("dependencies", {}), 
            **package_json.get("devDependencies", {})}
    
    frameworks = []
    
    if "vue" in deps:
        frameworks.append(f"Vue {deps['vue']}")
    if "react" in deps:
        frameworks.append(f"React {deps['react']}")
    if "angular" in deps:
        frameworks.append("Angular")
    if "svelte" in deps:
        frameworks.append("Svelte")
    
    return frameworks
```

---

## 中间件检测

### 数据库

| 依赖关键词 | 数据库类型 |
|------------|-----------|
| `mysql-connector` | MySQL |
| `postgresql` | PostgreSQL |
| `mongodb-driver` | MongoDB |
| `oracle` | Oracle |
| `sqlserver` | SQL Server |

### 缓存

| 依赖关键词 | 缓存类型 |
|------------|----------|
| `spring-boot-starter-data-redis` | Redis |
| `spring-boot-starter-cache` | Spring Cache |
| `memcached` | Memcached |
| `ehcache` | Ehcache |

### 消息队列

| 依赖关键词 | 消息队列 |
|------------|----------|
| `spring-kafka` | Kafka |
| `spring-boot-starter-amqp` | RabbitMQ |
| `rocketmq` | RocketMQ |
| `activemq` | ActiveMQ |

### 搜索引擎

| 依赖关键词 | 搜索引擎 |
|------------|----------|
| `elasticsearch` | Elasticsearch |
| `solr` | Solr |
| `meilisearch` | Meilisearch |

### 对象存储

| 依赖关键词 | 对象存储 |
|------------|----------|
| `minio` | MinIO |
| `aliyun-oss` | 阿里云 OSS |
| `aws-s3` | AWS S3 |
| `qiniu` | 七牛云 |

---

## 版本提取

### Maven 版本提取

```python
import re

def extract_maven_version(pom_content, artifact_id):
    pattern = rf'<{artifact_id}\.version>(.*?)</{artifact_id}\.version>'
    match = re.search(pattern, pom_content)
    if match:
        return match.group(1)
    
    # 尝试从 dependencyManagement 提取
    pattern = rf'<artifactId>{artifact_id}</artifactId>\s*<version>(.*?)</version>'
    match = re.search(pattern, pom_content, re.DOTALL)
    return match.group(1) if match else "unknown"
```

### npm 版本提取

```python
def extract_npm_version(package_json, package_name):
    deps = {**package_json.get("dependencies", {}), 
            **package_json.get("devDependencies", {})}
    
    version = deps.get(package_name, "unknown")
    # 移除版本范围符号
    version = version.lstrip("^~")
    return version
```

---

## 生成技术清单

**输出格式**:

```markdown
# 技术栈总览

## 核心框架

| 技术 | 版本 | 用途 |
|------|------|------|
| Spring Boot | 3.4.x | 后端框架 |
| Vue | 3.5.x | 前端框架 |
| TypeScript | 5.8.x | 类型系统 |

## 数据存储

| 技术 | 版本 | 用途 |
|------|------|------|
| MySQL | 8.0 | 关系型数据库 |
| Redis | 7.0 | 缓存 |
| Elasticsearch | 8.10 | 搜索引擎 |

## 中间件

| 技术 | 版本 | 用途 |
|------|------|------|
| Kafka | 3.2 | 消息队列 |
| MinIO | 8.5 | 对象存储 |

## 工具库

| 技术 | 版本 | 用途 |
|------|------|------|
| Lombok | 1.18 | 代码简化 |
| MapStruct | 1.5 | 对象映射 |
```
