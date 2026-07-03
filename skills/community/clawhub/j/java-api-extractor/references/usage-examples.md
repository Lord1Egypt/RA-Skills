# 使用示例

## 基础用法

### 1. 提取整个项目

```bash
python3 scripts/extract_java_api.py \
  --project "D:\working\coding\msa-icmp-dev-manage" \
  --output api-definitions.json
```

输出：
```
🔍 开始提取 Java 项目接口定义...
   项目路径：D:\working\coding\msa-icmp-dev-manage
📂 找到 15 个 Controller 类
  ✓ 提取接口：GET /api/users
  ✓ 提取接口：POST /api/users
  ✓ 提取接口：PUT /api/users/{id}
  ✓ 提取接口：DELETE /api/users/{id}
  ...

✅ 共提取 45 个接口定义
📄 已保存到：api-definitions.json
```

### 2. 提取指定包

```bash
python3 scripts/extract_java_api.py \
  --project "D:\working\coding\msa-icmp-dev-manage" \
  --package "com.example.user.controller" \
  --output user-api.json
```

### 3. 详细模式

```bash
python3 scripts/extract_java_api.py \
  --project "D:\working\coding\msa-icmp-dev-manage" \
  --output api-definitions.json \
  --verbose
```

### 4. 提取并直接推送

```bash
python3 scripts/extract_java_api.py \
  --project "D:\working\coding\msa-icmp-dev-manage" \
  --prdid "PRD-2026-001" \
  --push \
  --verbose
```

## 自然语言使用

直接告诉我需求即可：

**示例 1：提取接口**
> "帮我把用户管理模块的接口定义提取出来，项目路径是 D:\working\coding\msa-icmp-dev-manage"

**示例 2：提取并推送**
> "提取研发开放平台的接口文档，推送到产品部数据平台，PRD ID 是 PRD-2026-001"

**示例 3：查看接口列表**
> "看看这个项目有哪些接口定义"

## 输出示例

### 输入：Java Controller

```java
package com.example.user.controller;

import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.*;
import io.swagger.v3.oas.annotations.tags.*;
import io.swagger.v3.oas.annotations.parameters.*;

@Tag(name = "用户管理")
@RestController
@RequestMapping("/api/user")
public class UserController {
    
    @PostMapping
    @Operation(summary = "创建用户")
    public Result<UserVO> create(@RequestBody @Valid CreateUserRequest request) {
        // ...
        return Result.success(userVO);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "获取用户详情")
    public Result<UserVO> get(
        @PathVariable @Parameter(description = "用户 ID") String id,
        @RequestParam(required = false) @Parameter(description = "是否包含详情") Boolean includeDetail
    ) {
        // ...
        return Result.success(userVO);
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "更新用户信息")
    public Result<UserVO> update(
        @PathVariable String id,
        @RequestBody CreateUserRequest request
    ) {
        // ...
        return Result.success(userVO);
    }
    
    @DeleteMapping("/{id}")
    @Operation(summary = "删除用户")
    public Result<Void> delete(@PathVariable String id) {
        // ...
        return Result.success();
    }
}
```

### 输出：JSON 数组

```json
[
  {
    "name": "创建用户",
    "path": "/api/user",
    "method": "POST",
    "description": "创建用户",
    "requestParams": [
      {
        "name": "request",
        "type": "CreateUserRequest",
        "required": true,
        "description": "请求体"
      }
    ],
    "responseSchema": {
      "type": "object",
      "properties": {
        "code": {
          "type": "integer",
          "description": "状态码"
        },
        "message": {
          "type": "string",
          "description": "响应消息"
        },
        "data": {
          "type": "object",
          "description": "UserVO 类型数据"
        }
      }
    }
  },
  {
    "name": "获取用户详情",
    "path": "/api/user/{id}",
    "method": "GET",
    "description": "获取用户详情",
    "requestParams": [
      {
        "name": "id",
        "type": "String",
        "required": true,
        "description": "用户 ID"
      },
      {
        "name": "includeDetail",
        "type": "Boolean",
        "required": false,
        "description": "是否包含详情"
      }
    ],
    "responseSchema": {
      "type": "object",
      "properties": {
        "code": {
          "type": "integer",
          "description": "状态码"
        },
        "message": {
          "type": "string",
          "description": "响应消息"
        },
        "data": {
          "type": "object",
          "description": "UserVO 类型数据"
        }
      }
    }
  },
  {
    "name": "更新用户信息",
    "path": "/api/user/{id}",
    "method": "PUT",
    "description": "更新用户信息",
    "requestParams": [
      {
        "name": "id",
        "type": "String",
        "required": true,
        "description": "用户 ID"
      },
      {
        "name": "request",
        "type": "CreateUserRequest",
        "required": true,
        "description": "请求体"
      }
    ],
    "responseSchema": {
      "type": "object",
      "properties": {
        "code": {
          "type": "integer",
          "description": "状态码"
        },
        "message": {
          "type": "string",
          "description": "响应消息"
        },
        "data": {
          "type": "object",
          "description": "UserVO 类型数据"
        }
      }
    }
  },
  {
    "name": "删除用户",
    "path": "/api/user/{id}",
    "method": "DELETE",
    "description": "删除用户",
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
        "code": {
          "type": "integer",
          "description": "状态码"
        },
        "message": {
          "type": "string",
          "description": "响应消息"
        },
        "data": {
          "type": "object",
          "description": "Void 类型数据"
        }
      }
    }
  }
]
```

## 常见问题

### Q: 提取结果为空？

**可能原因：**
- 项目路径不正确
- Controller 类没有 `@RestController` 或 `@Controller` 注解
- 文件编码问题（目前支持 UTF-8）

**解决方法：**
```bash
# 使用详细模式查看
python3 scripts/extract_java_api.py --project "..." --verbose

# 检查项目结构
ls -R src/main/java
```

### Q: 参数提取不完整？

**可能原因：**
- 参数使用了自定义注解
- DTO 类在其他文件中定义

**解决方法：**
- 确保使用标准的 `@PathVariable`, `@RequestParam`, `@RequestBody` 注解
- 手动补充 DTO 字段信息

### Q: 路径拼接错误？

**示例：** 类路径 `/api` + 方法路径 `/user` = `/api/user`（正确）

如果路径有重复斜杠，脚本会自动清理。

### Q: 如何自定义输出格式？

修改 `D:\working\接口文档数据模版.json` 文件，脚本会基于该模版生成输出。

## 与工作流集成

### 1. Git Hook（pre-push）

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "📋 检查接口变更..."

python3 scripts/extract_java_api.py \
  --project "." \
  --output api-definitions.json \
  --prdid "PRD-2026-001" \
  --push

if [ $? -eq 0 ]; then
  echo "✅ 接口文档已更新并推送"
else
  echo "❌ 接口文档更新失败"
  exit 1
fi
```

### 2. CI/CD（GitHub Actions）

```yaml
name: Extract and Push API Docs

on:
  push:
    branches: [main]
    paths:
      - 'src/main/java/**/controller/**'

jobs:
  extract-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Extract API definitions
        run: |
          python3 scripts/extract_java_api.py \
            --project "." \
            --output api-definitions.json \
            --verbose
      
      - name: Push to platform
        run: |
          python3 scripts/push_api_to_product_platform.py \
            --prdid "${{ secrets.PRD_ID }}" \
            --file api-definitions.json
```

### 3. Maven 插件集成

```xml
<plugin>
  <groupId>org.codehaus.mojo</groupId>
  <artifactId>exec-maven-plugin</artifactId>
  <version>3.1.0</version>
  <executions>
    <execution>
      <id>extract-api-docs</id>
      <phase>compile</phase>
      <goals>
        <goal>exec</goal>
      </goals>
      <configuration>
        <executable>python3</executable>
        <arguments>
          <argument>scripts/extract_java_api.py</argument>
          <argument>--project</argument>
          <argument>${project.basedir}</argument>
          <argument>--output</argument>
          <argument>${project.build.directory}/api-definitions.json</argument>
        </arguments>
      </configuration>
    </execution>
  </executions>
</plugin>
```

## 相关文档

- [接口定义标准格式](api-definition-standard.md)
- [推送脚本](../api-push-product-platform/scripts/push_api_to_product_platform.py)
- [SKILL.md](../SKILL.md)
