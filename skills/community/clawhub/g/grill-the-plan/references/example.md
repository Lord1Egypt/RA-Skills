# Pre-Flight 检查表示例

任务：把本地 FastAPI 服务部署到公司内网 K8s。

## 🎯 任务目标

把 `svc-order` FastAPI 服务部署到 sit 环境 K8s，对外暴露 `/api/v1/orders`。

## 📋 节点表

| # | 节点 | 关键参数 | 风险点 | 出错影响 | 依赖 | 状态 |
|---|------|----------|--------|----------|------|------|
| 1 | Python 版本锁定 | 3.11.9（与 sit 一致） | 与本地 3.12 不一致可能漏兼容问题 | 中 | - | ⏳ |
| 2 | requirements.txt 冻结 | `pip freeze` + 手工裁剪 dev 依赖 | 漏掉 torch pin 导致镜像膨胀 | 中 | #1 | ⏳ |
| 3 | Dockerfile | python:3.11-slim · 非 root 用户 · 端口 8000 | 缺健康检查路径被 K8s 踢 | 高 | #2 | ⏳ |
| 4 | K8s manifest | replica=2 · CPU 0.5/1 · mem 512Mi/1Gi | HPA 没设导致流量尖峰打挂 | 高 | #3 | ⏳ |
| 5 | ConfigMap / Secret | DB_URL · REDIS_URL · JWT_SECRET 走 Secret | 明文写进 yaml 被提交 | 致命 | #4 | ⏳ |
| 6 | 灰度发布 | 先 10% 流量 · 观察 5min 错误率 < 0.5% | 直接全量上线炸了回滚慢 | 高 | #5 | ⏳ |

## ⚠️ 全局风险 Top 3

1. **JWT_SECRET 误提交** → 仓库历史永久泄露。缓解：`.gitignore` + pre-commit hook。
2. **镜像体积失控** → 拉取慢、启动慢。缓解：多阶段构建 + slim base。
3. **DB 连接池没配** → sit 压测时连接打满。缓解：`pool_size=20, max_overflow=10`。

## 🛑 阻断检查点

- [x] 所有参数都有具体值，无 TBD
- [ ] 回滚方案：`kubectl rollout undo deployment/svc-order`（已写但未演练）
- [x] 无歧义

## ✅ 建议执行顺序

1 → 2 → 3 → 4 → 5 → 6（全串行，#3 和 #4 可并行构建镜像但建议先验证 Dockerfile 单独跑通）
