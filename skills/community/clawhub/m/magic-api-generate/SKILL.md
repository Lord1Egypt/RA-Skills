---
name: magic-api
description: magic-api 国产接口快速开发框架。通过 Web UI 编写脚本自动映射为 HTTP 接口，无需 Controller/Service/Dao。当用户提到 magic-api、接口快速开发、低代码接口、动态接口生成、magic-script 时触发此技能。适用于 Spring Boot 集成、数据库操作、脚本语法、RESTful 接口开发等场景。
license: MIT
---

# magic-api 技能

magic-api 是基于 Java 的接口快速开发框架，通过 Web UI 编写脚本自动生成 HTTP 接口，无需定义 Controller、Service、Dao、Mapper、XML、VO 等 Java 对象。

## 快速开始

### Maven 依赖

```xml
<dependency>
    <groupId>org.ssssssss</groupId>
    <artifactId>magic-api-spring-boot-starter</artifactId>
    <version>2.2.2</version>
</dependency>
```

### application.yml 配置

```yaml
server:
  port: 9999

magic-api:
  web: /magic/web              # Web UI 入口
  resource:
    location: /data/magic-api  # 脚本存储位置（可改为 classpath: 只读模式）
```

### 访问 Web UI

```
http://localhost:9999/magic/web
```

## 核心概念

### 内置对象

| 对象 | 说明 | 示例 |
|------|------|------|
| `request` | HTTP 请求参数 | `request.name` |
| `path` | URL 路径参数 | `path.id` |
| `body` | 请求体 JSON | `body.name` |
| `db` | 数据库操作 | `db.select()` |
| `log` | 日志输出 | `log.info()` |
| `cache` | 缓存操作 | `cache.set()` |
| `response` | HTTP 响应 | `response.setHeader()` |

### 脚本语法

magic-api 使用 magic-script 脚本语言，语法类似 JavaScript：

```javascript
// 变量定义
var name = request.name;
var id = path.id;

// 条件判断
if (name) {
    log.info("用户名: " + name);
}

// 返回结果
return {code: 200, data: list};
```

## 数据库操作

### 查询

```javascript
// 查询列表
var list = db.select("select * from user");

// 带参数查询
var list = db.select("select * from user where status = ?", 1);

// 查询单条
var user = db.selectOne("select * from user where id = ?", id);

// 查询单值
var count = db.selectValue("select count(*) from user");

// 分页查询
var page = db.page("select * from user", 1, 10);
// 返回: {list: [...], total: 100, pageSize: 10, pageNumber: 1}
```

### 增删改

```javascript
// 插入（返回影响行数）
var affected = db.insert("user", {name: "张三", age: 25});

// 插入并返回自增ID
var id = db.insert("user", {name: "张三"}, true);

// 更新
var affected = db.update("user", {name: "李四"}, "id = ?", 1);

// 删除
var affected = db.delete("user", "id = ?", 1);
```

### 事务

```javascript
db.transaction(() => {
    var orderId = db.insert("orders", order, true);
    db.update("product", {stock: stock - 1}, "id = ?", productId);
});
```

## HTTP 接口配置

### 请求方法映射

| 方法 | 用途 | 示例路径 |
|------|------|----------|
| GET | 查询 | `/api/user/:id` |
| POST | 新增 | `/api/user` |
| PUT | 更新 | `/api/user/:id` |
| DELETE | 删除 | `/api/user/:id` |

### 参数获取

```javascript
// URL 路径参数: /api/user/:id
var id = path.id;

// Query 参数: /api/user?name=xxx
var name = request.name;

// 请求体 JSON
var body = request.body;
var username = body.username;

// 请求头
var token = request.header("Authorization");
```

## 常用模式

### RESTful CRUD

```javascript
// GET /api/user/:id - 查询单个
var user = db.selectOne("select * from user where id = ?", path.id);
return user ? {code: 200, data: user} : {code: 404, msg: "用户不存在"};

// GET /api/user - 查询列表
return {code: 200, data: db.select("select * from user")};

// POST /api/user - 新增
var id = db.insert("user", body, true);
return {code: 200, data: {id: id}, msg: "创建成功"};

// PUT /api/user/:id - 更新
db.update("user", body, "id = ?", path.id);
return {code: 200, msg: "更新成功"};

// DELETE /api/user/:id - 删除
db.delete("user", "id = ?", path.id);
return {code: 200, msg: "删除成功"};
```

### 条件查询

```javascript
var sql = "select * from user where 1=1";
var params = [];

if (request.name) {
    sql += " and name like ?";
    params.push("%" + request.name + "%");
}
if (request.status) {
    sql += " and status = ?";
    params.push(request.status);
}

return db.select(sql, ...params);
```

### 登录认证

```javascript
// 登录
var user = db.selectOne("select * from user where username = ?", body.username);
if (!user || user.password != body.password) {
    return {code: 401, msg: "用户名或密码错误"};
}

var token = "token_" + user.id + "_" + Date.now();
cache.set("token:" + token, user.id, 86400);
return {code: 200, data: {token: token, user: user}};

// 认证拦截（放在需要登录的接口开头）
var token = request.header("Authorization");
var userId = cache.get("token:" + token);
if (!userId) return {code: 401, msg: "请先登录"};
```

## 高级功能

详见参考文档：
- **[语法参考](references/syntax.md)** - 完整语法、内置函数、模块导入
- **[数据库操作](references/database.md)** - 多数据源、分页、事务
- **[业务示例](references/examples.md)** - 登录认证、文件上传、导出等

## 注意事项

1. **安全性** - 生产环境关闭 Web UI 或限制 IP 访问
2. **版本控制** - 脚本目录建议 Git 管理
3. **密码加密** - 使用 MD5/BCrypt，不要明文存储
4. **SQL 注入** - 使用参数化查询 `?` 占位符
5. **性能** - 复杂逻辑拆分多个接口，避免单脚本过长

## 官方资源

- 文档：https://www.ssssssss.org/magic-api/
- GitHub：https://github.com/ssssssss-team/magic-api
- Gitee：https://gitee.com/ssssssss-team/magic-api
- 在线演示：https://magic-api.ssssssss.org.cn
