---
name: jenkins-executor
version: 1.0.0
author: OpenClaw Developer
description: Jenkins 任务全生命周期管理工具，支持任务列表获取、远程构建、构建状态实时查询、构建日志全文获取、运行中构建强制终止，适用于 CI/CD 自动化、发布流水线、运维自动化场景。
permissions:
  - network:allow
---

# Jenkins Executor Skill
# 功能完整、可直接对接 Jenkins API 进行任务管理
# 依赖：Python 3.x + requests 库
# 必须配置：JENKINS_URL、JENKINS_USER、JENKINS_TOKEN

## 核心功能
1. **获取 Jenkins 任务列表**
   - 列出所有任务名称、URL、是否可构建、当前状态
   - 支持分页与全量拉取

2. **触发 Jenkins 任务构建**
   - 支持参数化构建
   - 支持无参任务直接触发
   - 返回构建队列编号与构建URL

3. **查询任务最新构建状态**
   - 支持查询：构建号、状态、结果、执行时间、执行人
   - 支持 SUCCESS / FAILURE / ABORTED / BUILDING 状态

4. **获取构建日志**
   - 支持获取完整控制台日志
   - 支持增量日志与全文日志
   - 自动处理编码与换行格式

5. **停止运行中的构建**
   - 强制终止正在执行的构建
   - 支持根据任务名 + 构建号精确停止
   - 返回停止结果与状态变更

## 配置要求
在环境变量中配置以下信息：
- JENKINS_URL：Jenkins 地址（例如 http://192.168.1.100:8080）
- JENKINS_USER：Jenkins 登录用户名
- JENKINS_TOKEN：Jenkins 用户 Token（密码也可，但不推荐）

## 接口说明
所有功能通过 Jenkins REST API 实现，使用 HTTP Basic Auth 鉴权，支持 Jenkins 2.250+ 所有版本。

## 异常处理
- 网络不可达：返回连接失败提示
- 鉴权失败：返回 401 未授权
- 任务不存在：返回 404 任务不存在
- 构建已结束：无法停止，返回状态提示