# Jenkins 构建配置

## 项目映射

```json
{
  "师傅端": {
    "jobName": "worker",
    "path": "/Users/chengzongxin/worker-rn",
    "description": "师傅端热更包"
  },
  "用户端": {
    "jobName": "user",
    "path": "/Users/chengzongxin/user",
    "description": "用户端包"
  }
}
```

## Jenkins 信息

- **地址**: http://localhost:8080
- **账号**: admin
- **密码**: admin

## 触发方式

1. **浏览器自动化**（首选）- 利用已登录 session 点击"立即构建"
2. **API 方式** - 需要处理 CSRF crumb，目前稳定性不如浏览器方式

## 触发关键词

| 关键词 | 项目 |
|--------|------|
| 师傅包 / 打个师傅包 / 打师傅包 | worker |
| 用户包 / 打个用户包 / 打用户包 | user |
