# 数据库操作参考

## 目录
- [配置](#配置)
- [查询方法](#查询方法)
- [增删改操作](#增删改操作)
- [分页查询](#分页查询)
- [事务处理](#事务处理)
- [多数据源](#多数据源)
- [动态 SQL](#动态-sql)

## 配置

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: password
    driver-class-name: com.mysql.cj.jdbc.Driver
```

## 查询方法

### select - 查询列表

```javascript
// 查询全部
var list = db.select("select * from user");

// 带参数
var list = db.select("select * from user where status = ?", 1);

// 多参数
var list = db.select("select * from user where status = ? and age > ?", 1, 18);
```

### selectOne - 查询单条

```javascript
var user = db.selectOne("select * from user where id = ?", 1);
// 返回: {id: 1, name: "张三", age: 25}
// 无数据返回 null
```

### selectValue - 查询单值

```javascript
// 查询计数
var count = db.selectValue("select count(*) from user");

// 查询单字段
var name = db.selectValue("select name from user where id = ?", 1);
```

## 增删改操作

### insert - 插入

```javascript
// 方式1: SQL 语句
db.update("insert into user(name, age) values(?, ?)", "张三", 25);

// 方式2: Map 方式（推荐）
db.insert("user", {
    name: "张三",
    age: 25,
    create_time: new Date()
});

// 返回自增 ID
var id = db.insert("user", {name: "张三"}, true);
```

### update - 更新

```javascript
// 方式1: SQL 语句
db.update("update user set name = ? where id = ?", "李四", 1);

// 方式2: Map 方式（推荐）
db.update("user", {
    name: "李四",
    update_time: new Date()
}, "id = ?", 1);
```

### delete - 删除

```javascript
// 方式1: SQL 语句
db.update("delete from user where id = ?", 1);

// 方式2: delete 方法（推荐）
db.delete("user", "id = ?", 1);
```

## 分页查询

```javascript
// 基本分页
var result = db.page("select * from user", 1, 10);
// 返回: {list: [...], total: 100, pageSize: 10, pageNumber: 1}

// 带参数分页
var result = db.page("select * from user where status = ?", 1, 10, 1);

// 获取分页数据
return {
    code: 200,
    data: result.list,
    total: result.total,
    pageSize: result.pageSize,
    pageNumber: result.pageNumber
};
```

## 事务处理

### 自动事务

```javascript
db.transaction(() => {
    var orderId = db.insert("orders", order, true);

    db.insert("order_item", {
        order_id: orderId,
        product_id: 1
    });

    db.update("product", {stock: stock - 1}, "id = ?", productId);
});
// 自动提交，异常自动回滚
```

### 手动事务

```javascript
try {
    db.beginTransaction();

    db.update("update account set balance = balance - 100 where id = 1");
    db.update("update account set balance = balance + 100 where id = 2");

    db.commit();
} catch (e) {
    db.rollback();
    return {code: 500, msg: "转账失败"};
}
```

## 多数据源

### 配置

```yaml
spring:
  datasource:
    dynamic:
      primary: master
      datasource:
        master:
          url: jdbc:mysql://localhost:3306/main_db
          username: root
          password: password
        slave:
          url: jdbc:mysql://localhost:3306/slave_db
          username: root
          password: password
```

### 使用

```javascript
// 切换数据源
var list = db.use("slave").select("select * from user");

// 或在 select 中指定
var list = db.select("select * from user", "slave");
```

## 动态 SQL

```javascript
var sql = "select * from user where 1=1";
var params = [];

// 条件拼接
if (request.name) {
    sql += " and name like ?";
    params.push("%" + request.name + "%");
}

if (request.status != null) {
    sql += " and status = ?";
    params.push(request.status);
}

if (request.startTime) {
    sql += " and create_time >= ?";
    params.push(request.startTime);
}

// 排序
sql += " order by create_time desc";

// 使用展开运算符传参
var list = db.select(sql, ...params);
```

## 最佳实践

### SQL 注入防护

```javascript
// ✅ 正确：参数化查询
db.select("select * from user where name = ?", request.name);

// ❌ 错误：字符串拼接
db.select("select * from user where name = '" + request.name + "'");
```

### NULL 值处理

```javascript
var user = db.selectOne("select * from user where id = ?", id);
if (user == null) {
    return {code: 404, msg: "用户不存在"};
}
```

### 批量操作

```javascript
db.transaction(() => {
    for (var item in dataList) {
        db.insert("user", item);
    }
});
```
