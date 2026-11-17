---
name: kes-docker
description: KingbaseES Docker 部署 — 测试用例
---

# KingbaseES Docker 部署测试用例

## 测试用例 1: Docker 快速启动

**场景**：用户需要快速启动一个金仓数据库容器

**输入问题**："金仓数据库怎么用 Docker 启动？"

**期望答案要点**：
- `docker load -i` 导入镜像
- `docker run` 启动命令，包含端口映射、数据挂载、环境变量
- 验证容器状态和数据库连接

**验证方法**：答案包含完整的 docker run 命令和验证步骤

---

## 测试用例 2: License 配置

**场景**：Docker 容器中 License 绑定失败

**输入问题**："Docker 里金仓数据库 License 怎么配置？"

**期望答案要点**：
- Docker 无网卡 MAC，需申请 Docker 版 License
- `docker cp` 复制 License 文件
- 容器内替换 license.dat 并修改权限
- `get_license_validdays()` 验证

**验证方法**：答案包含 License 替换完整流程

---

## 测试用例 3: 容器故障排查

**场景**：容器启动后立即退出

**输入问题**："金仓 Docker 容器启动后立即退出怎么办？"

**期望答案要点**：
- 检查数据目录权限（需 755）
- 查看容器日志 `docker logs kingbase`
- 检查内存是否不足（OOM）
- 验证镜像是否完整

**验证方法**：答案提供故障排查步骤
