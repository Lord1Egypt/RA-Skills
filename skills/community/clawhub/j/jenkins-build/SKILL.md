---
name: jenkins-build
description: 自动化触发 Jenkins 构建任务，支持师傅端和用户端项目打包。
metadata: {"clawdbot":{"emoji":"🔨","triggers":["打个师傅包","师傅包","打师傅包","打个用户包","用户包","打用户包","触发构建","Jenkins 构建"]}}
---

# Jenkins Build

自动化触发 Jenkins 构建任务，支持师傅端和用户端项目打包。

## 功能

自动化触发 Jenkins 构建任务，支持师傅端和用户端项目打包。

## 触发条件

用户提到以下任一短语时激活：
- "打个师傅包" / "师傅包" / "打师傅包"
- "打个用户包" / "用户包" / "打用户包"
- "触发构建" / "Jenkins 构建"

## 项目映射

| 项目 | Jenkins 任务名 | 路径 | 描述 |
|------|-------------|------|------|
| 师傅端 | `worker` | `/Users/chengzongxin/worker-rn` | 师傅端热更包 |
| 用户端 | `user` | `/Users/chengzongxin/user` | 用户端包 |

## 实现方式

### 首选：浏览器自动化

利用用户已登录的浏览器 session，通过 browser 工具点击 Jenkins 界面的"立即构建"按钮。

步骤：
1. 用 `browser action=open` 打开项目页面：`http://localhost:8080/job/{任务名}/`
2. 用 `browser action=snapshot` 获取页面元素
3. 找到"立即构建"链接（aria ref 包含"立即构建"或"Build Now"）
4. 用 `browser action=act kind=click` 触发构建
5. 再次 snapshot 确认构建已触发，返回构建编号和状态

### 备选：API 方式（需配置）

如果浏览器不可用，可尝试 API 方式，但需要解决 CSRF crumb 问题。

## 输出

构建触发后，向用户反馈：
- 构建编号
- 当前状态（执行中/排队中）
- 预计时间（如有）
- Jenkins 页面链接

## 注意事项

- Jenkins 地址：`http://localhost:8080`
- 默认账号密码：`admin/admin`（如需要 API 方式）
- 构建触发后无需等待完成，异步通知即可
- 如构建失败，检查 Jenkins 服务状态和登录状态

## 扩展

未来可支持：
- 查看构建日志
- 获取构建产物下载链接
- 构建失败自动通知
- 支持更多项目（通过配置映射表）
