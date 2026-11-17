# Link 测试指南

## 测试现状

Link 项目测试覆盖较为薄弱：

| 维度 | 现状 |
|------|------|
| 单元测试 | 极少（仅 2 个启动测试） |
| 集成测试 | 无 |
| 测试执行 | `maven-surefire-plugin` skip=true |
| 主要测试方式 | 手动 curl + 数据库验证 |
| 测试依赖 | spring-boot-starter-test（test scope） |

### 现有测试文件

1. `link-auth/src/test/java/com/link/authservice/AuthServiceApplicationTests.java`
2. `link-gateway/src/test/java/com/link/gateway/LinkcrmCloudgatewayApplicationTests.java`

均为 Spring Boot 启动测试（`@SpringBootTest`），无业务逻辑测试。

## 测试策略

### 策略一：接口冒烟测试（推荐）

使用 curl 命令逐个测试接口。参考 `knowledge-api-curl.md` 中的 18 个端点完整 curl 命令。

### 策略二：批量冒烟脚本

参考 `tmp/test_kb_endpoints.sh` 批量测试脚本。

### 策略三：数据库验证

执行 SQL 确认数据正确性。参考 `addressbook-optimization-guide.md` 中的验证 SQL。

## 签名过滤器问题与解决方案

### 问题

link-mvc 框架内置入站签名过滤器，所有请求需携带签名头。直接 curl 不带签名头会返回 **475**（签名校验失败）。

### 解决方案

#### 方案一：通过网关访问（推荐）

通过 link-gateway 访问，网关已配置签名处理：

```bash
# 通过网关访问（网关处理签名）
curl -X POST http://{gateway-host}:8888/linkcrm/ai/aiAssistant/kbDocument/queryByExamplePage \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"page": 1, "pageSize": 10}'
```

#### 方案二：配置签名头

从 link-auth 获取 Token，在请求头中携带签名：

```bash
# 1. 登录获取 Token
TOKEN=$(curl -s -X POST http://{gateway-host}:8888/linkcrm/login/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"xxx"}' | jq -r '.result.token')

# 2. 带 Token 访问
curl -X POST http://{service-host}:8888/link/aiAssistant/kbDocument/queryByExamplePage \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"page": 1, "pageSize": 10}'
```

#### 方案三：本地开发禁用签名校验

在 `application-dev.yml` 中配置：

```yaml
link:
  mvc:
    security:
      sign-check: false  # 本地开发禁用签名校验
```

## curl 测试模板

### 分页查询

```bash
curl -X POST http://{host}:{port}/link/aiAssistant/kbDocument/queryByExamplePage \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "entity": {
      "documentName": "测试",
      "status": 1
    },
    "page": 1,
    "pageSize": 10
  }'
```

### 按 ID 查询

```bash
curl -X POST http://{host}:{port}/link/aiAssistant/kbDocument/queryById \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"id": 123}'
```

### 新增

```bash
curl -X POST http://{host}:{port}/link/aiAssistant/kbDocument/insert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "documentName": "测试文档",
    "documentType": "pdf",
    "description": "测试描述",
    "status": 0
  }'
```

### 更新

```bash
curl -X POST http://{host}:{port}/link/aiAssistant/kbDocument/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "id": 123,
    "documentName": "更新后的名称",
    "objectVersionNumber": 1
  }'
```

### 删除

```bash
curl -X POST http://{host}:{port}/link/aiAssistant/kbDocument/deleteById \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"id": 123}'
```

## 批量冒烟测试脚本模板

```bash
#!/bin/bash
# link 接口冒烟测试脚本

BASE_URL="http://{host}:{port}"
TOKEN="{your-token}"
MODULE="aiAssistant/kbDocument"
PASS=0
FAIL=0

# 测试函数
test_endpoint() {
    local name=$1
    local path=$2
    local data=$3

    echo "=== 测试: $name ==="
    response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/link/${MODULE}/${path}" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${TOKEN}" \
        -d "${data}")

    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        success=$(echo "$body" | jq -r '.success')
        if [ "$success" = "true" ]; then
            echo "  PASS (HTTP $http_code)"
            PASS=$((PASS + 1))
        else
            echo "  FAIL (HTTP $http_code, success=false)"
            echo "  Response: $body"
            FAIL=$((FAIL + 1))
        fi
    else
        echo "  FAIL (HTTP $http_code)"
        echo "  Response: $body"
        FAIL=$((FAIL + 1))
    fi
    echo ""
}

# 执行测试
test_endpoint "分页查询" "queryByExamplePage" '{"page":1,"pageSize":10}'
test_endpoint "按ID查询" "queryById" '{"id":1}'
test_endpoint "计数" "queryCount" '{}'

# 汇总
echo "=========================="
echo "总计: $((PASS + FAIL)), 通过: $PASS, 失败: $FAIL"
echo "=========================="
```

## 数据库验证

### 验证数据写入

```sql
-- 验证新增数据
SELECT * FROM LNK_KB_DOCUMENT
WHERE DOCUMENT_NAME = '测试文档'
ORDER BY CREATION_DATE DESC
LIMIT 1;

-- 验证更新数据
SELECT ID, DOCUMENT_NAME, LAST_UPDATED_BY, LAST_UPDATE_DATE, OBJECT_VERSION_NUMBER
FROM LNK_KB_DOCUMENT
WHERE ID = 123;

-- 验证删除
SELECT COUNT(*) FROM LNK_KB_DOCUMENT WHERE ID = 123;
-- 预期: 0
```

### 验证同步日志

```sql
-- 查看同步日志
SELECT * FROM LNK_SYNC_LOG
WHERE SYNC_TYPE = 'CORPWX_CONTACT'
ORDER BY CREATION_DATE DESC
LIMIT 10;
```

## 日志检查

### 日志位置

| 类型 | 路径 |
|------|------|
| 应用日志 | `logs/` 目录 |
| GC 日志 | `logs/gc.log`（容器内 `/app/logs/gc.log`） |
| K8s 日志 | `kubectl logs -n cdfai -l app=link-ai` |

### 关键日志检查点

```bash
# 检查 ERROR 日志
grep -c "ERROR" logs/link-ai.log

# 检查特定接口调用
grep "kbDocument" logs/link-ai.log | tail -20

# 检查数据库连接
grep -i "datasource\|connection" logs/link-ai.log | tail -10

# 检查 Apollo 配置加载
grep -i "apollo" logs/link-ai.log | head -20
```

## Swagger 验证

访问 Swagger UI 确认接口注册：

```bash
# 确认 Swagger 可访问
curl http://{host}:{port}/swagger-ui.html

# 获取 API 文档 JSON
curl http://{host}:{port}/v2/api-docs
```

检查项：
- [ ] 新增 Controller 已注册
- [ ] 接口路径正确
- [ ] 请求参数完整
- [ ] 响应模型正确

## 测试环境限制

### 已知限制

| 限制 | 影响 | 解决方案 |
|------|------|----------|
| 本地 Maven 环境异常 | 无法 `mvn compile` | 使用 Docker 构建 |
| link-core 不在本地 .m2 | 编译失败 | 配置 settings.xml 指向内部 Nexus |
| 签名过滤器 | 直接 curl 返回 475 | 通过网关访问或禁用签名 |
| 无测试数据库 | 无法执行集成测试 | 使用独立测试环境或 Docker MySQL |

### 本地开发环境搭建建议

1. **配置 Maven settings.xml**：指向内部 Nexus 仓库
2. **拉取私有依赖**：link-core、link-mvc 等
3. **本地 MySQL**：Docker 启动 MySQL 8.0.30
4. **本地 Redis**：Docker 启动 Redis
5. **禁用签名校验**：开发环境配置
6. **Eureka 单节点**：使用 `eurekasingle` profile

```bash
# 本地 MySQL
docker run -d --name link-mysql -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=linkbase \
  mysql:8.0.30

# 本地 Redis
docker run -d --name link-redis -p 6379:6379 redis:6
```

## 单元测试建议

虽然项目目前测试覆盖低，但新增功能建议补充单元测试：

### Service 层测试

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class KbDocumentServiceTest {

    @Resource
    private KbDocumentService kbDocumentService;

    @Test
    public void testQueryByExamplePage() {
        KbDocument query = new KbDocument();
        query.setDocumentName("test");

        List<KbDocument> result = kbDocumentService.queryByExamplePage(query, 1, 10);

        assertNotNull(result);
        // 进一步断言...
    }
}
```

### Controller 层测试

```java
@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class KbDocumentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testQueryByExamplePage() throws Exception {
        mockMvc.perform(post("/link/aiAssistant/kbDocument/queryByExamplePage")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"page\":1,\"pageSize\":10}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true));
    }
}
```
