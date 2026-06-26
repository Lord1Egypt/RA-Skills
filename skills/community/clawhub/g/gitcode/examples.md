# GitCode API 示例

`YOUR_TOKEN` 即环境变量 `GITCODE_TOKEN` 或用户直接提供的 token。

## Example 1: 获取仓库详情（含 star/fork 数量）

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"

url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}"
response = requests.get(url, headers={'PRIVATE-TOKEN': token})

if response.status_code == 200:
    data = response.json()
    print(f"Stars: {data.get('stargazers_count', 0)}")
    print(f"Forks: {data.get('forks_count', 0)}")
    print(f"Watchers: {data.get('watchers_count', 0)}")
elif response.status_code == 401:
    print("Token 无效或缺失")
elif response.status_code == 404:
    print("仓库不存在或无访问权限")
```

---

## Example 2: 列出当前用户的仓库（需认证）

```python
import requests

token = "YOUR_TOKEN"
url = "https://api.gitcode.com/api/v5/user/repos?per_page=20&page=1"
response = requests.get(url, headers={'PRIVATE-TOKEN': token})

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(f"{repo['full_name']}: {repo.get('description', 'No description')}")
elif response.status_code == 401:
    print("Token 无效或缺失")
```

---

## Example 3: 列出仓库的 Issues（支持分页）

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"
state = "open"  # open, closed, or all

all_issues = []
page = 1
per_page = 20

while True:
    url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues"
    params = {'state': state, 'per_page': per_page, 'page': page}
    response = requests.get(url, headers={'PRIVATE-TOKEN': token}, params=params)
    
    if response.status_code != 200:
        print(f"错误: HTTP {response.status_code}")
        break
    
    issues = response.json()
    if not issues:
        break
    
    all_issues.extend(issues)
    page += 1

print(f"共找到 {len(all_issues)} 个 Issues")
for issue in all_issues:
    print(f"#{issue['number']}: {issue['title']}")
```

---

## Example 4: 创建 Issue

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"

# 官方路径为 /repos/{owner}/issues，repo 在 body 中传递
url = f"https://api.gitcode.com/api/v5/repos/{owner}/issues"
data = {
    "repo": repo,
    "title": "Bug: 功能异常",
    "body": "详细描述问题...",
    "labels": ["bug", "high-priority"],
    "assignee": "username"
}

response = requests.post(
    url,
    headers={'PRIVATE-TOKEN': token, 'Content-Type': 'application/json'},
    json=data
)

if response.status_code == 201:
    issue = response.json()
    print(f"Issue created successfully: #{issue['number']}")
elif response.status_code == 400:
    print("参数错误")
elif response.status_code == 401:
    print("Token 无效或无权限")
```

---

## Example 5: 创建 Pull Request

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"

url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls"
data = {
    "title": "修复 bug #123",
    "body": "修复了 xxx 问题",
    "head": "feature-branch",
    "base": "main"
}

response = requests.post(
    url,
    headers={'PRIVATE-TOKEN': token, 'Content-Type': 'application/json'},
    json=data
)

if response.status_code == 201:
    pr = response.json()
    print(f"PR created successfully: #{pr['number']}")
elif response.status_code == 400:
    print("参数错误或分支不存在")
elif response.status_code == 401:
    print("Token 无效或无权限")
```

---

## Example 6: 获取 Issue 关联的分支和 PR

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"
issue_number = 42

# 获取关联的分支
branches_url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{issue_number}/related_branches"
branches_response = requests.get(branches_url, headers={'PRIVATE-TOKEN': token})

# 获取关联的 PR
prs_url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{issue_number}/pull_requests"
prs_response = requests.get(prs_url, headers={'PRIVATE-TOKEN': token})

if branches_response.status_code == 200:
    branches = branches_response.json()
    print(f"关联的分支: {branches}")

if prs_response.status_code == 200:
    prs = prs_response.json()
    print(f"关联的 PR: {[pr['number'] for pr in prs]}")
```

---

## Example 7: 搜索仓库

```python
import requests

token = "YOUR_TOKEN"
url = "https://api.gitcode.com/api/v5/search/repositories"
params = {
    'q': 'python language:python',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 10
}

response = requests.get(url, headers={'PRIVATE-TOKEN': token}, params=params)

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(f"{repo['full_name']}: {repo.get('stargazers_count', 0)} stars")
```

---

## Example 8: 获取仓库文件内容

```python
import requests
import base64

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"
path = "README.md"

# 获取文件内容（Base64 编码）
url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{path}"
response = requests.get(url, headers={'PRIVATE-TOKEN': token})

if response.status_code == 200:
    data = response.json()
    if data.get('encoding') == 'base64':
        content = base64.b64decode(data['content']).decode('utf-8')
        print(content)

# 获取 raw 文件内容（原始文本）
raw_url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/raw/{path}"
raw_response = requests.get(raw_url, headers={'PRIVATE-TOKEN': token})

if raw_response.status_code == 200:
    print(raw_response.text)
```

---

## Example 9: 错误处理示例

```python
import requests

def api_request(url, token, method='GET', **kwargs):
    """统一的 API 请求处理"""
    headers = {'PRIVATE-TOKEN': token}
    response = requests.request(method, url, headers=headers, **kwargs)
    
    error_map = {
        200: "成功",
        201: "创建成功",
        204: "删除成功",
        400: "参数错误",
        401: "Token 无效或缺失",
        403: "无权限访问",
        404: "资源不存在",
        409: "资源冲突",
        422: "参数校验失败",
        429: "请求限流，请稍后重试"
    }
    
    status = response.status_code
    if status in [200, 201, 204]:
        return response.json(), None
    
    error_msg = error_map.get(status, f"未知错误: HTTP {status}")
    return None, error_msg

# 使用示例
token = "YOUR_TOKEN"
url = "https://api.gitcode.com/api/v5/repos/OWNER/REPO"

data, error = api_request(url, token)
if error:
    print(f"错误: {error}")
else:
    print(f"成功: {data}")
```

---

## Example 10: 批量获取所有 Issues（分页处理）

```python
import requests

def get_all_issues(owner, repo, token, state='open'):
    """获取所有 Issues（自动分页）"""
    all_issues = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues"
        params = {'state': state, 'per_page': per_page, 'page': page}
        response = requests.get(url, headers={'PRIVATE-TOKEN': token}, params=params)
        
        if response.status_code != 200:
            print(f"获取失败: HTTP {response.status_code}")
            break
        
        issues = response.json()
        if not issues:
            break
        
        all_issues.extend(issues)
        page += 1
    
    return all_issues

# 使用示例
token = "YOUR_TOKEN"
issues = get_all_issues("OWNER", "REPO", token)
print(f"共找到 {len(issues)} 个 Issues")
```

---

## Example 11: 获取项目自定义角色列表

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"

url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/customized_roles"
response = requests.get(url, headers={'PRIVATE-TOKEN': token})

if response.status_code == 200:
    roles = response.json()
    for role in roles:
        print(f"{role['role_name']}: {role['role_id']}")
elif response.status_code == 401:
    print("Token 无效或缺失")
```

---

## Example 12: 添加项目成员

```python
import requests

token = "YOUR_TOKEN"
owner = "OWNER"
repo = "REPO"
username = "target_username"
role_id = "ROLE_ID"  # 从 customized_roles 接口获取

url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/collaborators/{username}"
data = {"role_id": role_id}

response = requests.put(
    url,
    headers={'PRIVATE-TOKEN': token, 'Content-Type': 'application/json'},
    json=data
)

if response.status_code == 200:
    member = response.json()
    print(f"成员添加成功: {member['login']}")
elif response.status_code == 403:
    print("无权限访问")
```
