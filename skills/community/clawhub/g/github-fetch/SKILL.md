# github-fetch 技能 v2.0

## 描述

稳定获取 GitHub 项目内容的技能。解决国内 GitHub 连接不稳定问题，提供多层备选方案。

**v2.0 优化**：
1. SSH 预检测有效性（节省 ~60s）
2. 浅克隆默认化（速度快 10x）
3. 分支自动探测（main/master）
4. 目标目录防覆盖
5. 多 CDN fallback
6. 细化错误信息
7. Git LFS 提示

## 使用场景

当用户提到：
- "克隆 xxx 项目"
- "从 GitHub 获取"
- "GitHub 不通"
- "git clone 失败"
- "下载 GitHub 项目"

时自动启用。

## 优先级策略

| 优先级 | 方案 | 端口 | 说明 |
|--------|------|------|------|
| 1 | SSH clone | 22 | 已配置有效 SSH key 时最稳定 |
| 2 | ghproxy 镜像 | 443 | 国内加速镜像（多站点轮换） |
| 3 | 原 HTTPS | 443 | 最后尝试 |

## 脚本

### github-clone.sh

```bash
# 浅克隆（默认，--depth 1）
github-clone.sh https://github.com/d9g/page-build.git

# 指定目录
github-clone.sh https://github.com/d9g/page-build.git ~/projects

# 完整克隆
github-clone.sh https://github.com/d9g/page-build.git ~/projects --full
```

**优化点**：

| 功能 | 说明 |
|------|------|
| SSH 预检测 | `ssh -T git@github.com` 验证 key 有效性，无效则跳过 |
| 浅克隆默认 | `--depth 1` 减少下载量，完整克隆需 `--full` |
| 目录检查 | 目标已存在则自动加时间戳后缀 |
| 分支探测 | 调用 GitHub API 探测 main/master |
| 错误分类 | 区分：超时/拒绝/key无效/仓库不存在/目录已存在 |
| LFS 提示 | 检测 `.gitattributes` 中的 lfs 标记 |

### github-fetch-file.sh

```bash
# 获取单个文件（自动探测分支）
github-fetch-file.sh d9g/page-build README.md

# 指定分支
github-fetch-file.sh d9g/page-build config.yml master

# 指定输出路径
github-fetch-file.sh d9g/page-build src/main.py main output.py
```

**CDN fallback 顺序**：

| CDN | 限制 | 说明 |
|-----|------|------|
| jsdelivr | 50MB | 全球 CDN，速度快 |
| ghproxy | - | 国内加速镜像 |
| raw.githubusercontent.com | - | GitHub 原始文件 |

**优化点**：

| 功能 | 说明 |
|------|------|
| 分支探测 | 调用 GitHub API 或尝试 main→master |
| CDN fallback | jsdelivr → ghproxy → raw 依次尝试 |
| 文件大小警告 | >50MB 时提示 jsdelivr 可能失败 |
| 错误分类 | 区分：404/503/超时 |

## URL 转换规则

### HTTPS → SSH

```
https://github.com/d9g/page-build.git
→ git@github.com:d9g/page-build.git
```

### HTTPS → ghproxy

```
https://github.com/d9g/page-build.git
→ https://ghproxy.com/https://github.com/d9g/page-build.git
```

### GitHub → jsdelivr

```
https://github.com/d9g/page-build/blob/main/README.md
→ https://cdn.jsdelivr.net/gh/d9g/page-build@main/README.md
```

## 错误类型对照表

| 错误 | 类型 | 建议 |
|------|------|------|
| Connection timed out | 超时 | 检查网络或稍后重试 |
| Connection refused | 拒绝 | 端口被防火墙阻断 |
| Host key verification failed | SSH host key | `ssh-keyscan github.com >> ~/.ssh/known_hosts` |
| Permission denied | key 未绑定 | 检查 GitHub Settings → SSH Keys |
| Repository not found | 仓库不存在 | 检查仓库地址 |
| already exists | 目录已存在 | 删除或换目录 |
| HTTP 404 | 文件不存在 | 检查路径或分支名 |
| HTTP 503 | CDN 过载 | 稍后重试或换 CDN |

## 配置 SSH Key

```bash
# 生成 SSH key
ssh-keygen -t ed25519 -C "your@email.com"

# 查看公钥（添加到 GitHub）
cat ~/.ssh/id_ed25519.pub

# 验证连接
ssh -T git@github.com
# 成功: Hi xxx! You've successfully authenticated...
```

## 记录

每次成功获取后，在 TOOLS.md 中记录：

```markdown
### GitHub 连接（实测 YYYY-MM-DD）

- SSH（端口 22）：✅ 稳定（key 已绑定）
- HTTPS（端口 443）：⚠️ 不稳定
- ghproxy 镜像：⚠️ 部分可用
- jsdelivr CDN：✅ 稳定（单文件，<50MB）

推荐：优先使用 SSH clone
```

---

*v2.0 - 2026-04-13*