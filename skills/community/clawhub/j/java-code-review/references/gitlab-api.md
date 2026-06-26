# GitLab API 参考

## 基础配置

| 配置项       | 默认值                                   |
| --------- | ------------------------------------- |
| GitLab 地址 | https://git.xxx.com                   |
| 认证方式      | PRIVATE-TOKEN 或 Authorization: Bearer |

## 常用 API

### 1. 获取项目信息

```
GET /api/v4/projects/{project_id}
```

或使用 URL 编码的项目路径：

```
GET /api/v4/projects/server%2Fctg-travel-order
```

### 2. 获取分支列表

```
GET /api/v4/projects/{project_id}/repository/branches
```

### 3. 获取分支对比（差异 commits）

```
GET /api/v4/projects/{project_id}/repository/compare?from={基准分支}&to={目标分支}
```

返回：

- `commits` - 差异 commit 列表
- `diffs` - 文件差异列表
- `commit` - 基础 commit 信息

### 4. 获取 commit 详情

```
GET /api/v4/projects/{project_id}/repository/commits/{sha}
```

### 5. 获取 commit diff

```
GET /api/v4/projects/{project_id}/repository/commits/{sha}/diff
```

### 6. 获取分支 commits

```
GET /api/v4/projects/{project_id}/repository/commits?ref_name={branch_name}&since={ISO时间}&until={ISO时间}
```

分页参数：

- `per_page` - 每页数量（默认 20，最大 100）
- `page` - 页码

### 7. 创建 Merge Request

```
POST /api/v4/projects/{project_id}/merge_requests
{
  "source_branch": "feature-branch",
  "target_branch": "master",
  "title": "Merge feature into master",
  "description": "CR 报告摘要..."
}
```

### 8. 接受 Merge Request

```
PUT /api/v4/projects/{project_id}/merge_requests/{mr_iid}/merge
{
  "merge_commit_message": "Merge branch 'feature' into 'master'",
  "should_remove_source_branch": true
}
```

### 9. 直接合并分支（无 MR）

```
POST /api/v4/projects/{project_id}/repository/commits
{
  "branch": "target-branch",
  "commit_message": "Merge branch 'source-branch'",
  "start_branch": "source-branch",
  "actions": []
}
```

## 项目 ID 参考

| 项目名     | 项目 ID | URL 路径 |
| ------- | ----- | ------ |
| openapi | 1     | -      |
|         |       |        |
|         |       |        |
|         |       |        |
|         |       |        |
|         |       |        |

## 认证方式

### 方式一：PRIVATE-TOKEN Header

```
PRIVATE-TOKEN: glpat-xxxxxxx
```

### 方式二：Authorization Bearer

```
Authorization: Bearer glpat-xxxxxxx
```

## PowerShell 调用示例

```powershell
$headers = @{ 'Authorization' = 'Bearer glpat-xxxxxxx' }
$uri = 'https://git.xxx.com/api/v4/projects/1/repository/compare?from=master&to=release/release-20260324'
$response = Invoke-RestMethod -Uri $uri -Headers $headers
```

## 错误处理

| 状态码 | 含义    | 处理方式        |
| --- | ----- | ----------- |
| 200 | 成功    | 继续处理        |
| 401 | 未授权   | 检查 Token    |
| 403 | 禁止访问  | 检查权限        |
| 404 | 未找到   | 检查项目 ID/分支名 |
| 409 | 冲突    | 检查合并冲突      |
| 500 | 服务器错误 | 稍后重试        |
