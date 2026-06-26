---
name: pigxserver-skill
version: 1.0.0
description: PigX 企业级微服务平台后端开发指南 - Spring Cloud Alibaba + Java 17。当用户提到 PigX Server、PigX 后端、lhb-server 项目、Spring Cloud 微服务开发、PigX 微服务架构时使用此技能。
---

# PigX Server 后端开发 Skill

> PigX 企业级微服务平台开发指南 - Spring Cloud Alibaba + Java 17

## 项目信息

| 属性 | 值 |
|------|-----|
| Java 版本 | Java 17 |
| Spring Boot | 3.5.9 |
| Spring Cloud | 2025.0.1 |
| Spring Cloud Alibaba | 2023.0.3.3 |
| AI/ML | LangChain4j 1.6.0, Spring AI 1.0.2 |
| 数据库 | MySQL + PostgreSQL (pgvector) |
| ORM | MyBatis-Plus |
| 服务发现 | Nacos |
| 构建工具 | Maven |
| 版本 | 5.11.0 |

## 本地项目路径

```
D:\WorkSpace\my_workspace\lhb\lhb-server
```

## 官方文档

- 文档入口: https://docs.pig4cloud.com（需要微信扫码登录）

---

## 常用命令

```bash
# 构建项目（微服务模式）
mvn clean install

# 构建单体模式
mvn clean install -P boot

# 构建指定模块
mvn clean install -pl pigx-knowledge

# 跳过测试
mvn clean install -DskipTests

# 格式化代码
mvn spring-javaformat:apply

# 运行单体模式
cd pigx-boot && mvn spring-boot:run
```

---

## 项目结构

```
lhb-server/
├── pigx-boot/           # 单体部署启动器
├── pigx-auth/           # 认证模块
├── pigx-upms/           # 用户权限管理模块
├── pigx-gateway/        # API 网关
├── pigx-register/       # Nacos 注册中心
├── pigx-visual/         # 可视化管理模块
├── pigx-common/         # 公共模块
├── db/                  # 数据库初始化脚本
└── docker-compose.yml   # Docker 编排配置
```

---

## 公共模块说明

| 模块 | 功能 |
|------|------|
| pigx-common-bom | 依赖版本管理 |
| pigx-common-core | 核心工具类 |
| pigx-common-security | 安全认证 |
| pigx-common-oss | 对象存储 |
| pigx-common-excel | Excel 处理 |
| pigx-common-feign | Feign 远程调用 |
| pigx-common-gateway | 网关配置 |
| pigx-common-job | 定时任务 |
| pigx-common-log | 日志处理 |
| pigx-common-swagger | API 文档 |
| pigx-common-websocket | WebSocket 支持 |
| pigx-common-seata | 分布式事务 |
| pigx-common-sentinel | 限流熔断 |

---

## 核心开发规范

### 1. 包命名规范

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| Controller | 后缀 `Controller` | `AiDatasetController` |
| Service 接口 | 无后缀 | `EmbeddingStoreService` |
| Service 实现 | 后缀 `Impl` | `EmbeddingStoreServiceImpl` |
| Mapper | 后缀 `Mapper` | `AiDatasetMapper` |
| Entity | 后缀 `Entity` | `AiDatasetEntity` |
| DTO | 后缀 `DTO` | `AiMultimodalEmbeddingArkDTO` |
| Enum | 后缀 `Enums` | `EmbedBizTypeEnums` |

### 2. Controller 示例

```java
@RestController
@RequestMapping("/xxx")
@RequiredArgsConstructor
public class XxxController {

    private final XxxService xxxService;

    @GetMapping("/page")
    public R<IPage<XxxEntity>> page(Page page, XxxEntity entity) {
        return R.ok(xxxService.page(page, entity));
    }

    @PostMapping
    public R<Boolean> save(@RequestBody XxxEntity entity) {
        return R.ok(xxxService.save(entity));
    }

    @DeleteMapping("/{id}")
    public R<Boolean> deleteById(@PathVariable Long id) {
        return R.ok(xxxService.removeById(id));
    }
}
```

### 3. Service 示例

```java
public interface XxxService extends IService<XxxEntity> {}

@Service
@RequiredArgsConstructor
public class XxxServiceImpl implements XxxService {
    private final XxxMapper xxxMapper;

    @Override
    public IPage<XxxEntity> page(Page page, XxxEntity entity) {
        return xxxMapper.selectPage(page, entity);
    }
}
```

### 4. Entity 示例

```java
@Data
@TableName("xxx_table")
public class XxxEntity implements Serializable {
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;
    private String name;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}
```

---

## AI/RAG 开发

### 向量存储工厂模式

```java
@Component
public class QdrantEmbeddingStoreFactory implements EmbeddingStoreFactory {
    @Override
    public boolean support(String storeType) {
        return "QDRANT".equals(storeType);
    }

    @Override
    public EmbeddingStore createEmbeddingStore(EmbedStoreEntity store, DatasetEntity dataset) {
        // 创建向量存储实例
    }
}
```

### 支持的向量存储

Qdrant、Milvus、Chroma、PGVector、Neo4j

---

## 数据库配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/pigxx_boot
    username: postgres
    password: postgres
  redis:
    host: 127.0.0.1
    database: 5
  cloud:
    nacos:
      server-addr: pigx-register:8848
```

---

## 注意事项

1. **代码格式化**：提交前运行 `mvn spring-javaformat:apply`
2. **安全配置**：配置文件已加密，密码为 `pigx`
3. **Git 分支**：主分支 `dev`
4. **版本**：Java 17+，Spring Boot 3.5.9

---

## 参考文档

- Spring Cloud Alibaba: https://sca.aliyun.com
- MyBatis-Plus: https://baomidou.com
- LangChain4j: https://docs.langchain4j.dev

## 参考资料

更多后端文档请参考 `references/` 目录下的文档文件。