# 业务场景示例

## 目录
- [用户注册登录](#用户注册登录)
- [条件查询与分页](#条件查询与分页)
- [文件上传下载](#文件上传下载)
- [调用外部接口](#调用外部接口)
- [数据导出](#数据导出)
- [定时任务](#定时任务)

## 用户注册登录

### 用户表结构

```sql
CREATE TABLE `user` (
  `id` bigint AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(50) NOT NULL UNIQUE,
  `password` varchar(100) NOT NULL,
  `email` varchar(100),
  `status` tinyint DEFAULT 1,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP
);
```

### 注册接口

```javascript
// POST /api/auth/register
var body = request.body;

// 参数校验
if (!body.username || !body.password) {
    return {code: 400, msg: "用户名和密码不能为空"};
}

// 检查用户名是否存在
var exists = db.selectValue("select count(*) from user where username = ?", body.username);
if (exists > 0) {
    return {code: 400, msg: "用户名已存在"};
}

// 密码加密
var MessageDigest = import('java.security.MessageDigest');
var md = MessageDigest.getInstance("MD5");
var encryptedPwd = bytesToHex(md.digest(body.password.getBytes()));

// 插入用户
var userId = db.insert("user", {
    username: body.username,
    password: encryptedPwd,
    email: body.email,
    status: 1
}, true);

return {code: 200, data: {userId: userId}, msg: "注册成功"};

function bytesToHex(bytes) {
    var hex = "";
    for (var i = 0; i < bytes.length; i++) {
        var h = (bytes[i] & 0xFF).toString(16);
        hex += h.length == 1 ? "0" + h : h;
    }
    return hex;
}
```

### 登录接口

```javascript
// POST /api/auth/login
var body = request.body;

// 查询用户
var user = db.selectOne("select * from user where username = ?", body.username);
if (!user) {
    return {code: 401, msg: "用户名或密码错误"};
}

// 验证密码
var MessageDigest = import('java.security.MessageDigest');
var md = MessageDigest.getInstance("MD5");
var encryptedPwd = bytesToHex(md.digest(body.password.getBytes()));

if (user.password != encryptedPwd) {
    return {code: 401, msg: "用户名或密码错误"};
}

if (user.status != 1) {
    return {code: 403, msg: "账号已被禁用"};
}

// 生成 token
var UUID = import('java.util.UUID');
var token = UUID.randomUUID().toString().replace("-", "");

// 缓存 token（24小时）
cache.set("token:" + token, user.id, 86400);

// 更新登录时间
db.update("user", {last_login: new Date()}, "id = ?", user.id);

return {
    code: 200,
    data: {
        token: token,
        expiresIn: 86400,
        user: {
            id: user.id,
            username: user.username,
            email: user.email
        }
    }
};

function bytesToHex(bytes) {
    var hex = "";
    for (var i = 0; i < bytes.length; i++) {
        var h = (bytes[i] & 0xFF).toString(16);
        hex += h.length == 1 ? "0" + h : h;
    }
    return hex;
}
```

### 认证拦截

```javascript
// 放在需要登录的接口开头
var token = request.header("Authorization");
if (!token) {
    return {code: 401, msg: "请先登录"};
}

var userId = cache.get("token:" + token);
if (!userId) {
    return {code: 401, msg: "登录已过期"};
}

var user = db.selectOne("select * from user where id = ?", userId);
if (!user || user.status != 1) {
    return {code: 403, msg: "账号已被禁用"};
}

// 后续代码可使用 user 变量
```

## 条件查询与分页

```javascript
// GET /api/user/search
var sql = "select * from user where 1=1";
var params = [];
var pageSize = request.pageSize || 10;
var pageNumber = request.pageNumber || 1;

// 用户名模糊查询
if (request.username) {
    sql += " and username like ?";
    params.push("%" + request.username + "%");
}

// 状态筛选
if (request.status != null) {
    sql += " and status = ?";
    params.push(request.status);
}

// 时间范围
if (request.startTime) {
    sql += " and create_time >= ?";
    params.push(request.startTime);
}
if (request.endTime) {
    sql += " and create_time <= ?";
    params.push(request.endTime);
}

// 排序
sql += " order by create_time desc";

// 分页查询
var result = db.page(sql, pageNumber, pageSize, ...params);

return {
    code: 200,
    data: result.list,
    total: result.total,
    pageSize: pageSize,
    pageNumber: pageNumber
};
```

## 文件上传下载

### 上传

```javascript
// POST /api/upload
var file = request.file("file");

if (!file) {
    return {code: 400, msg: "请选择文件"};
}

var fileName = file.getOriginalFilename();
var fileSize = file.getSize();
var contentType = file.getContentType();

// 限制大小（5MB）
if (fileSize > 5 * 1024 * 1024) {
    return {code: 400, msg: "文件不能超过5MB"};
}

// 限制类型
var allowed = ["image/jpeg", "image/png", "image/gif"];
var allowFlag = false;
for (var t in allowed) {
    if (t == contentType) {
        allowFlag = true;
        break;
    }
}
if (!allowFlag) {
    return {code: 400, msg: "只支持 JPG/PNG/GIF"};
}

// 保存文件
var ext = fileName.substring(fileName.lastIndexOf("."));
var newFileName = Date.now() + ext;
var savePath = "/uploads/" + newFileName;

file.transferTo(new java.io.File(savePath));

return {
    code: 200,
    data: {
        url: "/uploads/" + newFileName,
        name: fileName,
        size: fileSize
    }
};
```

## 调用外部接口

```javascript
// 使用 Hutool HTTP 工具
var HttpUtil = import('cn.hutool.http.HttpUtil');

// GET 请求
var result = HttpUtil.get("https://api.example.com/users");

// POST 请求
var json = JSON.stringify({name: "张三", age: 25});
var result = HttpUtil.post("https://api.example.com/users", json);

// 解析响应
var data = JSON.parse(result);
return data;
```

## 数据导出

```javascript
// GET /api/user/export
var list = db.select("select * from user");

// 构建 CSV
var csv = "id,用户名,邮箱,状态,创建时间\n";

for (var user in list) {
    csv += user.id + ",";
    csv += user.username + ",";
    csv += user.email + ",";
    csv += (user.status == 1 ? "正常" : "禁用") + ",";
    csv += user.create_time + "\n";
}

// 设置响应头
response.setHeader("Content-Disposition", "attachment;filename=users.csv");
response.setHeader("Content-Type", "text/csv;charset=UTF-8");

// 添加 BOM 解决中文乱码
return "\uFEFF" + csv;
```

## 定时任务

```javascript
// GET /api/task/cleanup
// 配置定时器调用此接口

var expireTime = Date.now() - 7 * 24 * 60 * 60 * 1000;

// 清理过期数据
var affected = db.delete("temp_data", "create_time < ?", new Date(expireTime));

log.info("清理完成，删除 " + affected + " 条记录");

return {code: 200, msg: "清理完成", affected: affected};
```
