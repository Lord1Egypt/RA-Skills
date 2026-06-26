# API 接口规范参考

## 通用接口说明

### 基础信息

- **Base URL**: 需根据环境替换
  - 测试环境：`https://test-api.gz-cmc.com`（示例，请以实际配置为准）
  - 预发布环境：`https://staging-api.gz-cmc.com`
- **数据格式**: JSON
- **鉴权方式**: Bearer Token（登录后获取）
- **编码**: UTF-8

### 通用响应结构

```json
// 成功
{
  "code": 200,
  "message": "success",
  "data": { ... }
}

// 失败
{
  "code": 400 | 401 | 403 | 404 | 500,
  "message": "错误描述",
  "data": null
}
```

### 鉴权

```
Header: Authorization: Bearer <token>
```

---

## 典型接口清单

### 新闻模块

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/news/list | GET | 获取新闻列表 | page, size |
| /api/news/detail/{id} | GET | 获取新闻详情 | id |
| /api/news/search | GET | 搜索新闻 | keyword |
| /api/news/category | GET | 获取新闻分类 | - |

### 用户认证

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/user/login | POST | 账号密码登录 | username, password |
| /api/user/wx-login | POST | 微信登录 | code |
| /api/user/logout | POST | 登出 | token |
| /api/user/info | GET | 获取用户信息 | token |

### 任务管理

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/task/list | GET | 任务列表 | page, size, status |
| /api/task/detail/{id} | GET | 任务详情 | id |
| /api/task/create | POST | 创建任务 | title, content, assignee |
| /api/task/update-status | POST | 更新任务状态 | id, status |

### 互动模块

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/comment/list | GET | 评论列表 | news_id, page, size |
| /api/comment/add | POST | 添加评论 | news_id, content |
| /api/collect/add | POST | 收藏新闻 | news_id |
| /api/collect/list | GET | 收藏列表 | page, size |

### 服务功能

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/service/list | GET | 服务列表 | - |
| /api/service/medical/query | POST | 寻医问诊查询 | keywords |
| /api/service/waste/query | POST | 垃圾分类查询 | waste_name |

### 活动接口

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/act/list | GET | 活动列表 | page, size |
| /api/act/detail/{id} | GET | 活动详情 | id |
| /api/act/join | POST | 活动报名 | act_id, name, phone |
| /api/act/cancel | POST | 取消报名 | act_id |

### 上传接口

| 接口 | 方法 | 说明 | 必填参数 |
|------|------|------|---------|
| /api/upload/image | POST | 上传图片 | file (multipart) |
| /api/upload/video | POST | 上传视频 | file (multipart) |

---

## 接口测试重点关注点

### 1. 响应码验证
- HTTP状态码是否为2xx/4xx/5xx正确分类
- 业务code是否与HTTP状态码一致

### 2. 数据校验
- 必填字段缺失时的错误提示
- 字段类型/格式校验（手机号、邮箱、ID）
- 边界值测试（分页size=0，size=9999）

### 3. 安全性
- SQL注入：`' OR 1=1 --`
- XSS：`"><script>alert(1)</script>`
- 越权访问：使用A用户token访问B用户数据
- 敏感信息泄露：响应中不应包含密码明文/Token

### 4. 性能
- 响应时间 P99 ≤ 1s
- 并发测试：100QPS，持续5分钟
- 大数据量：列表接口分页加载10+页

### 5. 弱网容错
- 超时处理（设置合理的timeout）
- 重试机制是否正常工作
- 离线状态提示

---

## 常用测试工具

| 工具 | 适用场景 |
|------|---------|
| Postman / Apifox | 手工接口测试 |
| curl | 快速验证接口 |
| JMeter | 性能压测、并发测试 |
| Charles / Fiddler | 抓包、Mock |
| swagger-ui | 接口文档查阅 |
