---
name: istore-build-passwall
description: 克隆 istoreos 仓库，创建 PassWall GitHub Actions 构建 workflow 并推送到指定 GitHub 仓库。触发词：构建 PassWall、istore-build-passwall、创建 PassWall workflow
---

# istore-build-passwall

将 PassWall 构建 workflow 添加到用户的 istoreos fork 仓库。

## 工作流程

1. **收集配置** — 请求用户的 GitHub 仓库地址和 Personal Access Token
2. **克隆 istoreos 官方仓库** — 从 https://github.com/istoreos/istoreos.git 克隆完整内容
3. **添加 remote** — 将用户的 fork 添加为 origin
4. **写入 workflow** — 创建 `.github/workflows/build-passwall.yml`
5. **推送** — 提交并强制推送到用户的仓库（覆盖原有内容）
6. **设置 Workflow permissions** — 通过 GitHub API 开启 Read and write permissions 和 Allow GitHub Actions to create and approve pull requests

## 使用前提

- 已在 GitHub 上 fork `istoreos/istoreos`
- 生成了 Personal Access Token（需开启 `repo` 权限）

## 获取 GitHub Token

1. 访问 https://github.com/settings/tokens/new
2. 选择 `Generate new token (classic)`
3. 勾选 `repo` 权限
4. 生成后复制 Token

## 提示用户输入

当用户触发此 skill 时，要求提供：

- **GitHub 仓库地址**：格式 `https://github.com/YOUR_USER/istoreos.git`
- **Personal Access Token**：用于推送代码和设置仓库权限

---

## 执行步骤

### 1. 克隆官方仓库（完整历史）

```bash
git clone https://github.com/istoreos/istoreos.git <临时目录>
cd <临时目录>
```

### 2. 添加用户 fork 为 origin

```bash
git remote add origin https://github.com/<USER>/istoreos.git
# 或如果 origin 已存在则修改 URL
git remote set-url origin https://<TOKEN>@github.com/<USER>/istoreos.git
```

### 3. 写入 workflow 文件

从 `references/build-passwall.yml` 复制到 `.github/workflows/build-passwall.yml`

### 4. 提交并推送

```bash
git add .
git commit -m "Add PassWall build workflow"
git push -u origin main --force
```

### 5. 设置 Workflow permissions（通过 GitHub API）

```bash
# 设置 default_workflow_permissions 为 write
curl -s -X PUT \
  -H "Authorization: token <TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<USER>/istoreos/actions/permissions/workflow \
  -d '{"default_workflow_permissions":"write","can_approve_pull_request_reviews":true}'
```

## 推送后告诉用户

- istoreos 官方仓库内容 + PassWall workflow 已推送
- 可在 GitHub Actions 页面手动触发构建
- 选择架构后等待构建完成
- 下载 `.run` 文件到路由器执行即可