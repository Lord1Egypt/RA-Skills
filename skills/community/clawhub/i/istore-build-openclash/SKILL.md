---
name: istore-build-openclash
description: 创建 OpenClash GitHub Actions 构建 workflow 并直接推送到用户 GitHub 仓库。触发词：构建 OpenClash、istore-build-openclash、创建 OpenClash workflow
---

# istore-build-openclash

将 OpenClash 构建 workflow 直接推送到用户的 GitHub 仓库。

## 工作流程

1. **收集配置** — 请求用户的 GitHub 仓库地址和 Personal Access Token
2. **写入 workflow** — 通过 GitHub API 直接创建 `.github/workflows/build-openclash.yml`
3. **设置 Workflow permissions** — 通过 GitHub API 开启 Read and write permissions

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

### 1. 通过 GitHub API 创建 workflow 文件

```bash
# 从 references/build-openclash.yml 读取内容，然后通过 API 创建文件
curl -s -X PUT \
  -H "Authorization: token <TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/<USER>/<REPO>/contents/.github/workflows/build-openclash.yml \
  -d '{
    "message": "Add OpenClash build workflow",
    "content": "<BASE64_encoded_content>"
  }'
```

### 2. 设置 Workflow permissions

```bash
curl -s -X PUT \
  -H "Authorization: token <TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<USER>/<REPO>/actions/permissions/workflow \
  -d '{"default_workflow_permissions":"write","can_approve_pull_request_reviews":true}'
```

## 推送后告诉用户

- OpenClash workflow 已推送到仓库
- 可在 GitHub Actions 页面手动触发构建
- 选择架构后等待构建完成
- 下载 `.run` 文件到路由器执行即可
