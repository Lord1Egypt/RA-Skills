# Link 数据库设计指南

## 数据库概览

| 数据库 | 引擎 | 用途 | 连接配置 |
|--------|------|------|----------|
| linkbase | MySQL 8.0.30 | 业务主库 | `mysql.base:3306/linkbase` |
| linkadmin | MySQL 8.0.30 | 管理库 | 独立数据源 |
| linkloyalty | ClickHouse | 会员分析库 | 分析型查询 |

### 缓存与检索

| 技术 | 版本 | 用途 | 配置 |
|------|------|------|------|
| Redis | Jedis 2.9.1 | 缓存（单机/集群双模式） | `hone-redis-cluster.base:6379` |
| Elasticsearch | 7.16.3 | 全文检索 | - |
| Kafka | Spring Kafka | 消息队列（审计追踪） | `172.23.16.83:9092` |

## 多数据源配置

### 数据源模式

`application.yml` 中配置：

```yaml
link:
  datasource:
    mode: readwrite  # readwrite | normal | cluster
    url: jdbc:mysql://mysql.base:3306/linkbase     # 主库
    url1: jdbc:mysql://mysql-slave1.base:3306/linkbase  # 从库1
    url2: jdbc:mysql://mysql-slave2.base:3306/linkbase  # 从库2
    username: xxx
    password: xxx  # AES 加密
```

| 模式 | 说明 |
|------|------|
| `readwrite` | 读写分离（写主库，读从库） |
| `normal` | 单数据源 |
| `cluster` | 集群模式 |

### AES 加密

密码使用 AES 加密，密钥：`Aebh12oyqh97cyhw`（配置在 `jasypt-spring-boot-starter`）

## MyBatis 配置

### 全局配置

```yaml
mybatis:
  type-aliases-package: com.link.**.model
  mapper-locations: classpath*:com/link/**/sqlMap/*MapperMySql.xml
```

### MyBatis 插件

| 插件 | 用途 |
|------|------|
| `ResultInterceptor` | 结果集拦截处理 |
| `SqlInterceptor` | SQL 拦截（审计追踪） |
| `MyBatisMysqlExecutorInterceptor` | MySQL 执行器拦截 |
| `MybatisSqlInterceptor` | 字段审计（记录变更到 Kafka KT_FIELD_TRACK 主题） |

### MyBatis 设置

```xml
<settings>
    <setting name="jdbcTypeForNull" value="NULL"/>
    <setting name="localCacheScope" value="STATEMENT"/>
</settings>
```

- `localCacheScope=STATEMENT`：禁用一级缓存（每次查询独立）
- `jdbcTypeForNull=NULL`：null 参数映射为 JDBC NULL

## 表设计规范

### 表命名

| 类型 | 前缀/规则 | 示例 |
|------|-----------|------|
| 业务表 | `LNK_` + 大写下划线 | `LNK_KB_DOCUMENT` |
| 扩展表 | `LNK_*_EXT` | `LNK_ORG_EXT` |
| 关联表 | `LNK_INTER_*` | `LNK_INTER_ACCNT_POSTN` |
| 日志表 | `LNK_*_LOG` | `LNK_SYNC_LOG` |

### 字段命名

- 大写下划线命名法
- 示例：`DOCUMENT_NAME`、`CREATE_TIME`、`OBJECT_VERSION_NUMBER`

### 必备字段

每个表必须包含以下字段：

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `ID` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| `CREATED_BY` | VARCHAR(64) | NOT NULL | 创建人 |
| `CREATION_DATE` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `LAST_UPDATED_BY` | VARCHAR(64) | | 最后更新人 |
| `LAST_UPDATE_DATE` | TIMESTAMP | | 最后更新时间 |
| `OBJECT_VERSION_NUMBER` | BIGINT | NOT NULL, DEFAULT 1 | 乐观锁版本号 |

### 建表示例

```sql
CREATE TABLE LNK_KB_DOCUMENT (
    ID                  BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
    DOCUMENT_NAME       VARCHAR(255) NOT NULL COMMENT '文档名称',
    DOCUMENT_TYPE       VARCHAR(64)  COMMENT '文档类型',
    DESCRIPTION         TEXT         COMMENT '描述',
    STATUS              INT          DEFAULT 0 COMMENT '状态: 0-草稿, 1-发布, 2-归档',
    KNOWLEDGE_BASE_ID   BIGINT       COMMENT '所属知识库ID',
    FILE_URL            VARCHAR(512) COMMENT '文件URL',
    FILE_SIZE           BIGINT       COMMENT '文件大小(字节)',
    CREATED_BY          VARCHAR(64)  NOT NULL COMMENT '创建人',
    CREATION_DATE       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    LAST_UPDATED_BY     VARCHAR(64)  COMMENT '最后更新人',
    LAST_UPDATE_DATE    TIMESTAMP    COMMENT '最后更新时间',
    OBJECT_VERSION_NUMBER BIGINT     NOT NULL DEFAULT 1 COMMENT '乐观锁版本号',
    PRIMARY KEY (ID),
    INDEX IDX_KB_DOC_NAME (DOCUMENT_NAME),
    INDEX IDX_KB_DOC_STATUS (STATUS),
    INDEX IDX_KB_DOC_KB_ID (KNOWLEDGE_BASE_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识库文档表';
```

## Mapper 文件分布

| 模块 | Mapper 数量 | 说明 |
|------|-------------|------|
| link-ai | 5 | AiAgentConf、Conversation、ConversationHistory、GuidedPurchaseTrain、GuidedPurchaseTrainItem |
| link-base | 数百个 | 覆盖数十个业务域 |
| link-gateway | ~10 | AllowUrl、Authclient、Duty、Enterprise、UrlInfo、User 等 |
| link-auth | 3 | FunctionTime、Authclient、User |

## Mapper XML 规范

### 文件命名与位置

- `XxxMapper.xml` — 通用 SQL
- `XxxMapperMySql.xml` — MySQL 变体（实际使用）
- 位置：`com/link/{module}/{domain}/dao/mybatis/sqlMap/`

### resultMap 定义

```xml
<resultMap id="BaseResultMap" type="com.link.{module}.{domain}.model.Xxx">
    <id     column="ID"                  property="id"                  jdbcType="DECIMAL"/>
    <result column="DOCUMENT_NAME"       property="documentName"        jdbcType="VARCHAR"/>
    <result column="STATUS"              property="status"              jdbcType="DECIMAL"/>
    <result column="CREATED_BY"          property="createdBy"           jdbcType="VARCHAR"/>
    <result column="CREATION_DATE"       property="creationDate"        jdbcType="TIMESTAMP"/>
    <result column="LAST_UPDATED_BY"     property="lastUpdatedBy"       jdbcType="VARCHAR"/>
    <result column="LAST_UPDATE_DATE"    property="lastUpdateDate"      jdbcType="TIMESTAMP"/>
    <result column="OBJECT_VERSION_NUMBER" property="objectVersionNumber" jdbcType="DECIMAL"/>
</resultMap>
```

### 常用 SQL 片段

```xml
<!-- 基础字段 -->
<sql id="Base_Column_List">
    ID, DOCUMENT_NAME, DOCUMENT_TYPE, DESCRIPTION, STATUS,
    KNOWLEDGE_BASE_ID, FILE_URL, FILE_SIZE,
    CREATED_BY, CREATION_DATE, LAST_UPDATED_BY, LAST_UPDATE_DATE, OBJECT_VERSION_NUMBER
</sql>

<!-- 条件查询 -->
<sql id="Where_Clause">
    <where>
        <if test="entity != null">
            <if test="entity.documentName != null and entity.documentName != ''">
                AND DOCUMENT_NAME LIKE CONCAT('%', #{entity.documentName}, '%')
            </if>
            <if test="entity.status != null">
                AND STATUS = #{entity.status}
            </if>
            <if test="entity.knowledgeBaseId != null">
                AND KNOWLEDGE_BASE_ID = #{entity.knowledgeBaseId}
            </if>
        </if>
    </where>
</sql>
```

### CRUD SQL 模板

```xml
<!-- 分页查询 -->
<select id="queryByExamplePage" resultMap="BaseResultMap">
    SELECT <include refid="Base_Column_List"/>
    FROM LNK_KB_DOCUMENT
    <include refid="Where_Clause"/>
    ORDER BY CREATION_DATE DESC
    LIMIT #{page}, #{pageSize}
</select>

<!-- 计数 -->
<select id="queryCount" resultType="int">
    SELECT COUNT(1)
    FROM LNK_KB_DOCUMENT
    <include refid="Where_Clause"/>
</select>

<!-- 按ID查询 -->
<select id="queryById" resultMap="BaseResultMap">
    SELECT <include refid="Base_Column_List"/>
    FROM LNK_KB_DOCUMENT
    WHERE ID = #{id}
</select>

<!-- 新增 -->
<insert id="insert" parameterType="com.link.{module}.{domain}.model.Xxx" useGeneratedKeys="true" keyProperty="id">
    INSERT INTO LNK_KB_DOCUMENT (
        DOCUMENT_NAME, DOCUMENT_TYPE, DESCRIPTION, STATUS,
        KNOWLEDGE_BASE_ID, FILE_URL, FILE_SIZE,
        CREATED_BY, CREATION_DATE, OBJECT_VERSION_NUMBER
    ) VALUES (
        #{documentName}, #{documentType}, #{description}, #{status},
        #{knowledgeBaseId}, #{fileUrl}, #{fileSize},
        #{createdBy}, NOW(), 1
    )
</insert>

<!-- 更新（乐观锁） -->
<update id="update" parameterType="com.link.{module}.{domain}.model.Xxx">
    UPDATE LNK_KB_DOCUMENT
    SET DOCUMENT_NAME = #{documentName},
        DOCUMENT_TYPE = #{documentType},
        DESCRIPTION = #{description},
        STATUS = #{status},
        LAST_UPDATED_BY = #{lastUpdatedBy},
        LAST_UPDATE_DATE = NOW(),
        OBJECT_VERSION_NUMBER = OBJECT_VERSION_NUMBER + 1
    WHERE ID = #{id}
      AND OBJECT_VERSION_NUMBER = #{objectVersionNumber}
</update>

<!-- 删除 -->
<delete id="deleteById">
    DELETE FROM LNK_KB_DOCUMENT WHERE ID = #{id}
</delete>
```

## 数据安全警告

### SQL 注入防护

**禁止**使用 `${}` 拼接用户输入：

```xml
<!-- 危险！SQL 注入风险 -->
<select id="queryByOrder">
    SELECT * FROM LNK_KB_DOCUMENT ORDER BY ${orderField}  <!-- 禁止 -->
</select>
```

**正确做法**：白名单校验排序字段：

```xml
<!-- 安全：使用 $ 但在 Java 层做白名单校验 -->
<select id="queryByOrder">
    SELECT * FROM LNK_KB_DOCUMENT
    ORDER BY
    <choose>
        <when test="orderField == 'name'">DOCUMENT_NAME</when>
        <when test="orderField == 'date'">CREATION_DATE</when>
        <otherwise>CREATION_DATE</otherwise>
    </choose>
    <if test="orderDirection == 'asc'">ASC</if>
    <otherwise>DESC</otherwise>
</select>
```

### 敏感数据

- 数据库密码 AES 加密存储
- 用户 Token 通过 RSA 公钥加密
- 审计日志通过 Kafka `KT_FIELD_TRACK` 主题记录字段变更

## 数据中转模式（特殊）

link-ai 知识库模块采用**数据中转模式**：不落本地库，Service 层直接代理第三方 API。

### 配置

```yaml
# 第三方知识库 API 配置
knowledge-base:
  third-party:
    base-url: https://knowledge-api.example.com
    rsa-public-key: ${KNOWLEDGE_RSA_KEY}
    token-expire-seconds: 3600
```

### Token 自动注入

```java
@Component
public class KnowledgeHttpHelper {

    @Resource
    private KnowledgeProperties properties;

    /**
     * 自动生成 Token 并注入请求头
     */
    private HttpHeaders buildHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        // RSA 公钥加密生成 Token
        String token = RsaUtil.encrypt(
            properties.getRsaPublicKey(),
            UUID.randomUUID().toString() + "|" + System.currentTimeMillis()
        );
        headers.set("Authorization", "Bearer " + token);
        return headers;
    }

    public <T> List<T> post(String url, Map<String, Object> params, Class<T> clazz) {
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(params, buildHeaders());
        ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
        // 解析响应...
    }
}
```

### 已知数据表

| 表名 | 用途 | 所属模块 |
|------|------|----------|
| `LNK_EMP_INFO` | 员工信息 | link-base |
| `LNK_ORG_EXT` | 组织扩展 | link-base |
| `LNK_POSTN_EXT` | 岗位扩展 | link-base |
| `LNK_INTER_ACCNT_POSTN` | 账户岗位关联 | link-base |
| `LNK_SYNC_LOG` | 同步日志 | link-base |

## 数据库迁移

项目**无 Flyway/Liquibase 迁移文件**，Schema 通过以下方式管理：

1. 手动执行 DDL 脚本
2. 数据库管理工具直接操作
3. 迁移脚本需自行维护版本记录

**建议**：新功能开发时，将 DDL 脚本保存在模块目录下（如 `link-ai/sql/V1__create_kb_document.sql`），便于版本管理。
