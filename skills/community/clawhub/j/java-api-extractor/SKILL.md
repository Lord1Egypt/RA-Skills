---
name: java-api-extractor
description: 从 Java 项目中提取 Controller 层接口定义为 JSON 数据。
---

# Java API Extractor

从 Java Spring Boot 项目中自动提取 Controller 层的接口定义，按照标准 JSON 模版格式输出，用于推送到产品部数据平台或前端数据接口平台。

## 触发场景

- 需要从 Java 项目生成接口文档
- 批量提取 Controller 接口定义
- 接口文档自动化生成
- 推送接口定义前的数据准备

## 核心功能

- 扫描 Java 项目中的 Controller 类
- 解析 Spring MVC 注解（@GetMapping, @PostMapping, @PutMapping, @DeleteMapping 等）
- 提取接口路径、请求方法、参数定义、响应类型
- 解析 Swagger/OpenAPI 注解（@ApiOperation, @ApiParam, @Tag 等）
- 按照标准 JSON 模版格式输出接口数组

## 输出格式

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
  }
]
```

## 工作流程

1. 指定 Java 项目根目录
2. 扫描 `src/main/java` 下的 Controller 类
3. 解析每个 Controller 的接口注解
4. 提取参数信息和响应类型
5. 生成标准 JSON 格式输出
6. 可选：直接推送到产品部数据平台

## 使用方式

**自然语言**（推荐）：直接告诉我需求

**脚本方式**：
```bash
# 提取整个项目
py scripts/extract_java_api.py --project "D:\working\coding\msa-icmp-dev-manage" --output api-definitions.json

# 提取指定包
py scripts/extract_java_api.py --project "D:\working\coding\msa-icmp-dev-manage" --package "com.example.user.controller" --output user-api.json

# 提取并直接推送
py scripts/extract_java_api.py --project "D:\working\coding\msa-icmp-dev-manage" --prdid "PRD-2026-001" --push

# 详细模式
py scripts/extract_java_api.py --project "..." --output api.json --verbose
```

# 提取指定包
node scripts/extract_java_api.js --project "D:\working\coding\msa-icmp-dev-manage" --package "com.example.user.controller" --output user-api.json

# 提取并直接推送
node scripts/extract_java_api.js --project "D:\working\coding\msa-icmp-dev-manage" --prdid "PRD-2026-001" --push
```

**详细模式**：
```bash
python3 scripts/extract_java_api.py --project "..." --output api.json --verbose
```

## 支持的注解

### 请求映射

| 注解 | 说明 |
|------|------|
| `@GetMapping` | GET 请求映射 |
| `@PostMapping` | POST 请求映射 |
| `@PutMapping` | PUT 请求映射 |
| `@DeleteMapping` | DELETE 请求映射 |
| `@PatchMapping` | PATCH 请求映射 |
| `@RequestMapping` | 通用请求映射 |
| `@RestController` | REST 控制器标识 |
| `@Controller` | 控制器标识 |

### 参数注解

| 注解 | 说明 |
|------|------|
| `@PathVariable` | 路径参数 |
| `@RequestParam` | 查询参数 |
| `@RequestHeader` | 请求头参数 |
| `@RequestBody` | 请求体 |
| `@ModelAttribute` | 模型属性 |

### 文档注解

| 注解 | 说明 |
|------|------|
| `@ApiOperation` | 接口描述（Swagger 2） |
| `@Operation` | 接口描述（OpenAPI 3） |
| `@ApiParam` | 参数描述（Swagger 2） |
| `@Parameter` | 参数描述（OpenAPI 3） |
| `@Tag` | 模块标签 |
| `@Api` | 类级别描述 |

## 参数类型映射

| Java 类型 | JSON 类型 |
|-----------|-----------|
| String | string |
| Integer, int, Long, long | integer |
| Boolean, boolean | boolean |
| Double, double, Float, float | number |
| Date, LocalDateTime | string (date-time) |
| List<T> | array |
| Object | object |

## 相关文档

- [接口定义规范](references/api-definition-standard.md)
- [推送脚本](../api-push-product-platform/scripts/push_api_to_product_platform.py)

## 技术说明

**首选 Python 版本**：

- **Python 版本** (`extract_java_api.py`)：**默认和首选**，功能更完整，提取的接口更多（82 vs 47）
- **Node.js 版本** (`extract_java_api.js`)：备用选项，适合没有 Python 环境的场景

两个版本输出格式完全一致，可互换使用。

## 最佳实践

- **提取前检查**：确保项目已编译，依赖完整
- **Swagger 优先**：有 Swagger 注解时优先使用其描述
- **类级别路径**：正确处理 `@RequestMapping` 在类级别的定义
- **参数推断**：无注解描述时从字段名和类型推断
- **响应分析**：从 Controller 方法返回类型推断响应结构

## 错误处理

- 语法错误：跳过无法解析的类，记录警告
- 类型缺失：使用 Object 类型占位
- 循环依赖：检测并避免无限递归
- 文件编码：自动检测 UTF-8/GBK
