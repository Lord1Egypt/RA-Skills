# 接口定义标准格式

本文档定义了从 Java 项目提取的接口文档标准 JSON 格式。

## 基础结构

每个接口定义遵循以下格式：

```json
{
  "name": "接口中文名称",
  "path": "/api/路径",
  "method": "GET|POST|PUT|DELETE",
  "description": "接口描述",
  "requestParams": [],
  "responseSchema": {}
}
```

## 字段说明

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 接口中文名称 |
| path | string | 是 | 接口路径 |
| method | string | 是 | HTTP 方法：GET, POST, PUT, DELETE |
| description | string | 是 | 接口功能描述 |
| requestParams | array | 是 | 请求参数数组 |
| responseSchema | object | 是 | 响应数据 Schema |

### 请求参数 (requestParams)

```json
{
  "name": "参数名",
  "type": "String|Integer|Boolean|...",
  "required": true,
  "description": "参数说明"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 参数名称 |
| type | string | 是 | 参数类型（Java 类型） |
| required | boolean | 是 | 是否必填 |
| description | string | 是 | 参数描述 |

### 响应 Schema (responseSchema)

```json
{
  "type": "object",
  "properties": {
    "字段名": {
      "type": "string|integer|boolean|number|object|array",
      "description": "字段说明"
    }
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 是 | 固定为 "object" |
| properties | object | 是 | 返回数据的属性定义 |

### 属性定义 (properties 中的值)

```json
{
  "字段名": {
    "type": "string",
    "description": "字段说明"
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 是 | 字段类型 |
| description | string | 是 | 字段描述 |

## 完整示例

```json
[
  {
    "name": "创建用户",
    "path": "/api/user",
    "method": "POST",
    "description": "创建新用户",
    "requestParams": [
      {
        "name": "userName",
        "type": "String",
        "required": true,
        "description": "用户名"
      },
      {
        "name": "email",
        "type": "String",
        "required": true,
        "description": "邮箱"
      },
      {
        "name": "password",
        "type": "String",
        "required": true,
        "description": "密码"
      }
    ],
    "responseSchema": {
      "type": "object",
      "properties": {
        "userId": {
          "type": "string",
          "description": "创建的用户 ID"
        }
      }
    }
  },
  {
    "name": "获取用户详情",
    "path": "/api/user/{id}",
    "method": "GET",
    "description": "根据 ID 获取用户详细信息",
    "requestParams": [
      {
        "name": "id",
        "type": "String",
        "required": true,
        "description": "用户 ID"
      }
    ],
    "responseSchema": {
      "type": "object",
      "properties": {
        "userId": {
          "type": "string",
          "description": "用户 ID"
        },
        "userName": {
          "type": "string",
          "description": "用户名"
        },
        "email": {
          "type": "string",
          "description": "邮箱"
        },
        "createdAt": {
          "type": "string",
          "description": "创建时间"
        }
      }
    }
  }
]
```

## Java 注解映射

### 请求方法

| Java 注解 | method 值 |
|-----------|-----------|
| `@GetMapping` | GET |
| `@PostMapping` | POST |
| `@PutMapping` | PUT |
| `@DeleteMapping` | DELETE |
| `@PatchMapping` | PATCH |
| `@RequestMapping(method = GET)` | GET |

### 参数类型

| Java 注解 | 参数位置 |
|-----------|----------|
| `@PathVariable` | path |
| `@RequestParam` | query |
| `@RequestHeader` | header |
| `@RequestBody` | body |

### 描述信息

| Java 注解 | 用途 |
|-----------|------|
| `@ApiOperation("描述")` | 接口描述（Swagger 2） |
| `@Operation(summary = "描述")` | 接口描述（OpenAPI 3） |
| `@ApiParam("描述")` | 参数描述（Swagger 2） |
| `@Parameter(description = "描述")` | 参数描述（OpenAPI 3） |
| `@Tag(name = "模块名")` | 模块标签 |

## 类型映射

### Java 类型 → JSON Schema 类型

| Java 类型 | JSON Schema 类型 |
|-----------|------------------|
| String | string |
| Integer, int | integer |
| Long, long | integer |
| Boolean, boolean | boolean |
| Double, double | number |
| Float, float | number |
| Date, LocalDateTime | string (date-time) |
| List<T> | array |
| Map<K,V> | object |
| Object | object |

## 提取规则

### 接口路径

1. 类级别 `@RequestMapping("/api/user")` + 方法级别 `@GetMapping("/{id}")` = `/api/user/{id}`
2. 仅方法级别 `@PostMapping("/create")` = `/create`
3. 无任何路径 = `/`

### 接口名称

1. 优先使用 `@ApiOperation` 或 `@Operation` 的 summary
2. 其次从方法名推断（驼峰转中文）
3. 最后使用 "未命名接口"

### 请求参数

1. `@PathVariable` → 路径参数（required=true）
2. `@RequestParam` → 查询参数（required 根据注解）
3. `@RequestBody` → 展开 DTO 字段

### 响应 Schema

1. 从方法返回类型推断
2. `ResponseEntity<T>` 或 `Result<T>` → 展开 T 的字段
3. 简单类型 → 使用基础类型

## 最佳实践

### 1. 添加 Swagger 注解

```java
@Tag(name = "用户管理")
@RestController
@RequestMapping("/api/user")
public class UserController {
    
    @PostMapping
    @Operation(summary = "创建用户")
    public Result<UserVO> create(
        @RequestBody @Valid CreateUserRequest request
    ) {
        // ...
    }
}
```

### 2. 参数描述完整

```java
public Result<UserVO> get(
    @PathVariable @Parameter(description = "用户 ID") String id,
    @RequestParam(required = false) @Parameter(description = "是否包含详情") Boolean includeDetail
) {
    // ...
}
```

### 3. DTO 类字段清晰

```java
public class CreateUserRequest {
    @NotBlank(message = "用户名不能为空")
    private String userName;
    
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @Size(min = 6, message = "密码至少 6 位")
    private String password;
}
```

## 检查清单

提取后检查：

- [ ] 所有接口都有 name, path, method, description
- [ ] path 格式正确（以 / 开头，无 //）
- [ ] method 是有效的 HTTP 方法
- [ ] requestParams 包含所有参数
- [ ] 参数 type 正确映射
- [ ] responseSchema 结构完整
- [ ] JSON 格式有效

## 相关文件

- 模版文件：`D:\working\接口文档数据模版.json`
- 提取脚本：`../scripts/extract_java_api.py`
- 推送脚本：`../api-push-product-platform/scripts/push_api_to_product_platform.py`
