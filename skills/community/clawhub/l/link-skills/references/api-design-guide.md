# Link 接口设计指南

## API 风格

Link 系统采用 REST 风格（基于 Spring MVC，非严格 RESTful），统一 POST 请求，JSON 请求体传参。

## 路由设计

### 网关层路由

link-gateway 统一入口，前缀 `/linkcrm/`：

| 路由前缀 | 目标服务 | StripPrefix |
|----------|----------|-------------|
| `/linkcrm/ai/**` | link-ai | 1 |
| `/linkcrm/action/**` | link-base | 1 |
| `/linkcrm/login/**` | link-login | 1 |
| `/linkcrm/ai/websocket/**` | ai-websocket | - |

外部请求路径：`/linkcrm/{module}/{resource}/{action}`

网关 StripPrefix=1 去掉第一段前缀（`linkcrm`），转发到服务时路径变为 `/link/{module}/{resource}/{action}`。

### 服务层路由

Controller `@RequestMapping` 路径格式：`/link/{module}/{resource}`

| 服务 | 路由前缀 | 示例 |
|------|----------|------|
| link-ai | `/link/aiAssistant/{resource}` | `/link/aiAssistant/kbDocument/queryPage` |
| link-ai | `/link/cozeChat` | `/link/cozeChat/sendMessage` |
| link-base | `/link/corpwx/sync` | `/link/corpwx/sync/contactList` |
| link-base | `/link/base/{domain}` | `/link/base/accnt/queryById` |

### 路由命名约定

- 资源名：小写驼峰（如 `kbDocument`、`cozeChat`）
- 操作名：
  - `queryByExamplePage` — 分页查询
  - `queryById` — 按 ID 查询
  - `queryCount` — 计数
  - `insert` / `batchInsert` — 新增
  - `update` / `batchUpdate` — 修改
  - `deleteById` / `batchDelete` — 删除
  - `export` — 导出
  - `import` — 导入

## 请求方式

### 统一 POST

多数接口使用 `@RequestMapping` 不限定 method，但 `@JsonParam` 走 JSON 请求体，实际以 POST 为主。

### 参数接收

| 注解 | 用途 | 示例 |
|------|------|------|
| `@JsonParam` | 接收 JSON 请求体（link-core 提供） | `@JsonParam Xxx entity` |
| `@RequestParam` | URL 参数 | `@RequestParam(defaultValue="1") int page` |
| `@RequestBody` | 标准 Spring JSON 体（偶尔使用） | `@RequestBody Map<String, Object> params` |
| `@PathVariable` | 路径变量 | `@PathVariable("id") Long id` |

## 响应格式

### 统一响应信封

```json
{
  "success": true,
  "code": "200",
  "result": {},
  "rows": [],
  "total": 100,
  "detailMessage": ""
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | Boolean | 操作是否成功 |
| `code` | String | 状态码（字符串类型） |
| `result` | Object | 单对象结果 |
| `rows` | Array | 列表结果 |
| `total` | Number | 总记录数（分页查询时） |
| `detailMessage` | String | 详细消息（错误时为错误描述） |

### 成功响应示例

```json
{
  "success": true,
  "code": "200",
  "result": {
    "id": 123,
    "name": "测试文档"
  }
}
```

分页查询：
```json
{
  "success": true,
  "code": "200",
  "rows": [
    {"id": 1, "name": "文档1"},
    {"id": 2, "name": "文档2"}
  ],
  "total": 56
}
```

### 错误响应示例

```json
{
  "success": false,
  "code": "400",
  "detailMessage": "必填字段缺失: name"
}
```

## 错误码体系

| code | HTTP 含义 | 场景 |
|------|-----------|------|
| 200 | 成功 | 操作成功 |
| 400 | 参数错误 | 必填字段缺失、参数格式错误 |
| 401 | 未认证 | 未登录或 Token 过期 |
| 403 | 无权限 | 已登录但无操作权限 |
| 404 | 未找到 | 资源不存在 |
| 409 | 状态冲突 | 资源状态不允许当前操作 |
| 412 | 乐观锁冲突 | OBJECT_VERSION_NUMBER 不匹配 |
| 429 | 限流 | 请求频率超限 |
| 475 | 签名校验失败 | link 框架入站签名校验失败（特殊码） |
| 500 | 服务端错误 | 内部异常 |
| 1001 | 业务错误 | 必填字段缺失（业务层） |

### 475 特殊说明

link-mvc 框架内置入站签名过滤器，所有请求需携带签名头。直接 curl 不带签名头会返回 475。解决方案见 `testing-guide.md`。

## Controller 代码模式

### 标准 CRUD Controller

```java
@Api(tags = {"知识库文档接口"})
@Controller
@RequestMapping("/link/aiAssistant/kbDocument")
@Slf4j
public class KbDocumentController extends BasicController<KbDocument> {

    @Resource
    private KbDocumentService kbDocumentService;

    @ApiOperation("分页查询文档")
    @RequestMapping({"/queryByExamplePage"})
    @ResponseBody
    public Map<String, Object> queryByExamplePage(
            @JsonParam Map<String, Object> params,
            @JsonParam KbDocument entity,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            List<KbDocument> rows = kbDocumentService.queryByExamplePage(entity, page, pageSize);
            int total = kbDocumentService.queryCount(entity);
            result.put("success", true);
            result.put("code", "200");
            result.put("rows", rows);
            result.put("total", total);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("查询文档失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }

    @ApiOperation("根据ID查询文档")
    @RequestMapping({"/queryById"})
    @ResponseBody
    public Map<String, Object> queryById(@RequestParam("id") Long id) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            KbDocument doc = kbDocumentService.queryById(id);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", doc);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("查询文档失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }

    @ApiOperation("新增文档")
    @RequestMapping({"/insert"})
    @ResponseBody
    public Map<String, Object> insert(@JsonParam KbDocument entity) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            int count = kbDocumentService.insert(entity);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", count);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("新增文档失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }
}
```

### 数据中转 Controller（知识库模式）

```java
@Api(tags = {"知识库文档接口"})
@Controller
@RequestMapping("/link/aiAssistant/kbDocument")
@Slf4j
public class KbDocumentController extends BasicController<KbDocument> {

    @Resource
    private KbDocumentService kbDocumentService;

    // 重写父类方法，代理第三方 API
    @Override
    @RequestMapping({"/queryByExamplePage"})
    @ResponseBody
    public Map<String, Object> queryByExamplePage(@JsonParam KbDocument entity,
                                                   @RequestParam int page,
                                                   @RequestParam int pageSize) {
        // 直接调用 Service，Service 内部代理第三方知识库 API
        Map<String, Object> result = new HashMap<>(8);
        try {
            Object response = kbDocumentService.queryByExamplePage(entity, page, pageSize);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", response);
        } catch (Exception e) {
            log.error("查询失败", e);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", e.getMessage());
        }
        return result;
    }
}
```

## API 文档

### Swagger/Knife4j

- 访问地址：`/swagger-ui.html`
- 配置开关：`swagger.enable`（application.yml）
- 注解要求：
  - Controller 类：`@Api(tags={"xxx接口"})`
  - 接口方法：`@ApiOperation(value="xxx")`
  - 字段说明：`@ApiModelProperty(value="xxx")`

### 接口规范文档

知识库接口规范：`.dumate/inbox/知识库服务接口文档.md`（85KB，极其详尽）

包含：
- 接口列表（18 个端点）
- 请求/响应格式
- 错误码定义
- 业务流程说明
- Token 认证机制

## Feign 跨服务调用

### 定义 Feign 客户端

```java
@FeignClient(name = "link-base", fallback = BaseClientFallback.class)
public interface BaseClient {

    @RequestMapping(value = "/link/base/org/queryById", method = RequestMethod.POST)
    Map<String, Object> queryOrgById(@RequestParam("id") Long id);

    @RequestMapping(value = "/link/base/accnt/queryList", method = RequestMethod.POST)
    List<Map<String, Object>> queryAccntList(@RequestBody Map<String, Object> params);
}
```

### Fallback 降级

```java
@Component
public class BaseClientFallback implements BaseClient {
    @Override
    public Map<String, Object> queryOrgById(Long id) {
        Map<String, Object> fallback = new HashMap<>();
        fallback.put("success", false);
        fallback.put("code", "500");
        fallback.put("detailMessage", "服务降级");
        return fallback;
    }
}
```

## WebSocket 接口

### AI 实时对话

- 路径：`/websocket/ai`
- 基于 Netty + link-websocket-starter
- 用途：AI 对话流式输出、ASR 语音识别实时传输

## API 安全

### 签名校验

link-mvc 框架入站签名过滤器：
- 所有请求需携带签名头
- 签名算法：RSA/HMAC（link-core 内部实现）
- 无签名头 → 返回 475

### 鉴权流程

```
客户端请求 → link-gateway（网关层鉴权）
           → link-auth（认证授权）
           → 目标服务（接口权限校验）
```

### Token 管理

- 知识库模块：RSA 公钥加密自动生成 Token
- 普通 API：通过 link-auth 服务获取 Token
