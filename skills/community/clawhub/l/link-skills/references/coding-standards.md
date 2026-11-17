# Link 编码规范参考

## Checkstyle 配置

配置文件：各模块根目录 `checkstyle.xml`，Maven validate 阶段强制执行。违反任何规则即构建失败（severity=error）。

### 核心规则

| 规则 | 要求 | 示例 |
|------|------|------|
| 行长度 | ≤ 150 字符（package/import/URL 例外） | - |
| 缩进 | 4 空格，**禁止 Tab 字符** | `FileTabCharacter` |
| 编码 | UTF-8 | - |
| 大括号 | 必须使用（NeedBraces），即使单行 | `if (x) { doSomething(); }` |
| switch | 必须有 default 分支 | `MissingSwitchDefault` |
| import | 禁止未使用的 import | `UnusedImports` |
| 空 catch | 异常变量名必须为 `expected` | `catch (Exception expected) {}` |

### 命名规则

| 类型 | 正则 | 示例 |
|------|------|------|
| 包名 | `^[a-z]+(\.[a-zA-Z][a-zA-Z0-9]*)*$` | `com.link.base.knowledge.kbdocument.controller` |
| 类名/类型名 | `^[A-Z][a-zA-Z0-9]*$` | `KbDocumentController` |
| 方法名 | `^[a-zA-Z][a-z0-9]\|[a-zA-Z0-9_]*$` | `queryByExamplePage` |
| 成员/参数/局部变量 | `^[a-zA-Z_0-9]*$` | `documentName` |
| 泛型类型参数 | `(^[A-Z][0-9]?)$\|([A-Z][a-zA-Z0-9]*[T]$)` | `T`, `KT` |

### Javadoc 规则

- 单行 Javadoc 必须符合规范（`SingleLineJavadoc`）
- 注解顺序：`@author` → `@param` → `@return` → `@throws` → `@deprecated`

## 分层架构规范

每个业务域严格三层分包：

```
{domain}/
├── controller/     # 控制层
├── service/        # 服务层（接口 + Impl）
├── dao/mybatis/
│   ├── mapper/     # MyBatis Mapper 接口
│   └── sqlMap/     # XML 映射文件（含 MySql 变体）
└── model/          # 实体模型
```

### 包命名约定

```
com.link.{module}.{domain}.controller
com.link.{module}.{domain}.service
com.link.{module}.{domain}.dao.mybatis.mapper
com.link.{module}.{domain}.dao.mybatis.sqlMap
com.link.{module}.{domain}.model
```

示例：`com.link.base.knowledge.kbdocument.controller`

## Controller 规范

### 基本模式

```java
@Api(tags = {"xxx接口"})
@Controller
@RequestMapping("/link/{module}/{resource}")
@Slf4j
public class XxxController extends BasicController<Xxx> {

    @Resource
    private XxxService xxxService;

    @RequestMapping({"/queryByExamplePage"})
    @ResponseBody
    public Map<String, Object> queryByExamplePage(@JsonParam QueryParams qps,
                                                   @JsonParam Xxx entity,
                                                   @RequestParam(defaultValue = "1") int page,
                                                   @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            List<Xxx> rows = xxxService.queryByExamplePage(entity, page, pageSize);
            int total = xxxService.queryCount(entity);
            result.put("success", true);
            result.put("code", "200");
            result.put("rows", rows);
            result.put("total", total);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            result.put("success", false);
            result.put("code", "400");
            result.put("detailMessage", "操作失败");
        }
        return result;
    }
}
```

### 关键约定

| 约定 | 说明 |
|------|------|
| 注解 | `@Controller` + `@ResponseBody`（非 `@RestController`，link 框架约定） |
| 继承 | `extends BasicController<T>`（link-core 提供） |
| 路由 | `@RequestMapping("/link/{module}/{resource}")` |
| 依赖注入 | `@Resource`（非 `@Autowired`） |
| 参数接收 | `@JsonParam`（link-core 提供，接收 JSON 请求体） |
| 返回类型 | `Map<String, Object>`（统一信封） |
| 异常处理 | 双层 catch：`BasicServiceException` + `Exception` |
| 日志 | `@Slf4j`（Lombok） |
| API 文档 | `@Api(tags={"xxx接口"})` + `@ApiOperation(value="xxx")` |

## Service 规范

### 接口

```java
public interface XxxService extends BasicService<Xxx> {
    List<Xxx> queryByExamplePage(Xxx entity, int page, int pageSize);
    int queryCount(Xxx entity);
    Xxx queryById(Long id);
    int insert(Xxx entity);
    int update(Xxx entity);
    int deleteById(Long id);
}
```

### 实现

```java
@Service
@Slf4j
public class XxxServiceImpl extends BasicServiceImpl<Xxx> implements XxxService {

    @Resource
    private XxxMapper xxxMapper;

    @Override
    public List<Xxx> queryByExamplePage(Xxx entity, int page, int pageSize) {
        return xxxMapper.queryByExamplePage(entity, page, pageSize);
    }

    @Override
    public int queryCount(Xxx entity) {
        return xxxMapper.queryCount(entity);
    }
}
```

### 关键约定

| 约定 | 说明 |
|------|------|
| 接口 | 继承 `BasicService<T>`（link-core 提供） |
| 实现 | `@Service` + 继承 `BasicServiceImpl<T>` |
| 注入 Mapper | `@Resource` 注入 |
| 日志 | `@Slf4j` |
| 事务 | `@Transactional` 注解（如需要） |

## Mapper 规范

### 接口

```java
public interface XxxMapper extends BasicMapper<Xxx> {
    List<Xxx> queryByExamplePage(@Param("entity") Xxx entity,
                                  @Param("page") int page,
                                  @Param("pageSize") int pageSize);
    int queryCount(@Param("entity") Xxx entity);
    Xxx queryById(@Param("id") Long id);
    int insert(Xxx entity);
    int update(Xxx entity);
    int deleteById(@Param("id") Long id);
}
```

### 关键约定

| 约定 | 说明 |
|------|------|
| 继承 | `BasicMapper<T>`（link-core 提供，含基础 CRUD） |
| 参数 | `@Param` 注解绑定参数 |
| 位置 | `dao/mybatis/mapper/` 目录 |

## Model 规范

```java
@Data
public class Xxx extends BasicModel {
    private Long id;
    private String name;
    private String description;
    private Integer status;
    private String createdBy;
    private Date creationDate;
    private String lastUpdatedBy;
    private Date lastUpdateDate;
    private Long objectVersionNumber;
}
```

### 关键约定

| 约定 | 说明 |
|------|------|
| 继承 | `BasicModel`（link-core 提供，含基础字段） |
| 注解 | `@Data`（Lombok，自动生成 getter/setter） |
| 字段 | 驼峰命名，对应数据库大写下划线字段 |

## MyBatis XML 规范

### 文件命名

- `XxxMapper.xml` — 通用 SQL
- `XxxMapperMySql.xml` — MySQL 变体（实际使用的）

### 文件位置

`src/main/resources/com/link/{module}/{domain}/sqlMap/` 或 `src/main/java/com/link/{module}/{domain}/dao/mybatis/sqlMap/`

### XML 模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.link.{module}.{domain}.dao.mybatis.mapper.XxxMapper">

    <resultMap id="BaseResultMap" type="com.link.{module}.{domain}.model.Xxx">
        <id column="ID" property="id" jdbcType="DECIMAL"/>
        <result column="NAME" property="name" jdbcType="VARCHAR"/>
        <result column="DESCRIPTION" property="description" jdbcType="VARCHAR"/>
        <result column="STATUS" property="status" jdbcType="DECIMAL"/>
        <result column="CREATED_BY" property="createdBy" jdbcType="VARCHAR"/>
        <result column="CREATION_DATE" property="creationDate" jdbcType="TIMESTAMP"/>
        <result column="LAST_UPDATED_BY" property="lastUpdatedBy" jdbcType="VARCHAR"/>
        <result column="LAST_UPDATE_DATE" property="lastUpdateDate" jdbcType="TIMESTAMP"/>
        <result column="OBJECT_VERSION_NUMBER" property="objectVersionNumber" jdbcType="DECIMAL"/>
    </resultMap>

    <sql id="Base_Column_List">
        ID, NAME, DESCRIPTION, STATUS, CREATED_BY, CREATION_DATE,
        LAST_UPDATED_BY, LAST_UPDATE_DATE, OBJECT_VERSION_NUMBER
    </sql>

    <select id="queryByExamplePage" resultMap="BaseResultMap">
        SELECT <include refid="Base_Column_List"/>
        FROM {TABLE_NAME}
        <where>
            <if test="entity != null">
                <if test="entity.name != null and entity.name != ''">
                    AND NAME LIKE CONCAT('%', #{entity.name}, '%')
                </if>
                <if test="entity.status != null">
                    AND STATUS = #{entity.status}
                </if>
            </if>
        </where>
        ORDER BY CREATION_DATE DESC
        LIMIT #{page}, #{pageSize}
    </select>

</mapper>
```

### 安全警告

- **禁止使用 `${}` 拼接用户输入**（SQL 注入风险）
- 排序字段如需动态拼接，使用白名单校验
- 使用 `#{}` 参数化查询

## 数据库表命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| 业务表 | `LNK_` | `LNK_KB_DOCUMENT`, `LNK_EMP_INFO` |
| 扩展表 | `LNK_*_EXT` | `LNK_ORG_EXT`, `LNK_POSTN_EXT` |
| 关联表 | `LNK_INTER_*` | `LNK_INTER_ACCNT_POSTN` |
| 日志表 | `LNK_*_LOG` | `LNK_SYNC_LOG` |

### 必备字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `ID` | BIGINT | 主键 |
| `CREATED_BY` | VARCHAR(64) | 创建人 |
| `CREATION_DATE` | TIMESTAMP | 创建时间 |
| `LAST_UPDATED_BY` | VARCHAR(64) | 最后更新人 |
| `LAST_UPDATE_DATE` | TIMESTAMP | 最后更新时间 |
| `OBJECT_VERSION_NUMBER` | BIGINT | 乐观锁版本号 |

## 配置规范

### application.yml 关键配置项

```yaml
# 数据源
link:
  datasource:
    mode: readwrite  # readwrite | normal | cluster
    url: jdbc:mysql://mysql.base:3306/linkbase
    url1: jdbc:mysql://mysql.base:3306/linkbase  # 从库
    url2: jdbc:mysql://mysql.base:3306/linkbase  # 从库2

# MyBatis
mybatis:
  configuration:
    map-underscore-to-camel-case: true
  type-aliases-package: com.link.**.model
  mapper-locations: classpath*:com/link/**/sqlMap/*MapperMySql.xml

# Apollo
apollo:
  appid: cdfai-link-ai
  cluster: LOCAL
  namespaces: ops,biz,stability
```

## 特殊代码模式

### 数据中转模式（知识库模块）

Service 层不操作本地数据库，直接代理第三方 API：

```java
@Service
@Slf4j
public class KbDocumentServiceImpl extends BasicServiceImpl<KbDocument> implements KbDocumentService {

    @Resource
    private KnowledgeProperties knowledgeProperties;

    @Resource
    private KnowledgeHttpHelper httpHelper;

    @Override
    public List<KbDocument> queryByExamplePage(KbDocument entity, int page, int pageSize) {
        // 不查本地库，直接调第三方 API
        String url = knowledgeProperties.getBaseUrl() + "/documents/query";
        Map<String, Object> params = new HashMap<>();
        params.put("page", page);
        params.put("pageSize", pageSize);
        // Token 自动注入（RSA 公钥加密）
        return httpHelper.post(url, params, KbDocument.class);
    }
}
```

### Coze AI 对话集成

```java
// 非流式对话
CozeChatRequest request = new CozeChatRequest();
request.setBotId(botId);
request.setUserId(userId);
request.setContent(userMessage);
CozeChatResponse response = cozeClient.chat(request);

// 流式对话（WebFlux + SSE）
return webClient.post()
    .uri(cozeApiUrl + "/chat/stream")
    .body(BodyInserters.fromValue(request))
    .retrieve()
    .bodyToFlux(String.class)
    .map(response -> response);
```

### Feign 客户端

```java
@FeignClient(name = "link-base", fallback = BaseClientFallback.class)
public interface BaseClient {
    @RequestMapping(value = "/link/base/org/queryById", method = RequestMethod.POST)
    Map<String, Object> queryOrgById(@RequestParam("id") Long id);
}
```

## 已知代码质量问题

（来源：code-review-report.md）

1. MyBatis `${}` 拼接排序字段存在 SQL 注入风险
2. 下载接口 Range 解析脆弱，大文件 OOM 风险
3. `LinkAiApplication.java` 第 19 行调用 `CoreApplication.class`（疑似 bug）
4. 通用异常泄露内部信息
5. Fastjson 1.2.83 历史漏洞风险
