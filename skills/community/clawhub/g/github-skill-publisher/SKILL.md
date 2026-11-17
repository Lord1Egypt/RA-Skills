---
name: github-skill-publisher
description: |-
  把本地 Agent / Skill / 工具包标准化发布到 GitHub 公开仓库。当用户要把本地文件转成开源 skill 上传时触发。
  完整工作流：脱敏检查 → 文件结构对齐 github-project-radar 标准 → 建空仓 → 逐文件推送 →
  补 topics / description / release。封装了今天踩过的所有坑（auto_init README 覆盖、URL 转码、
  私改公开、topic 清理）。一次成功不再返工。
agent_created: true
---

# GitHub Skill Publisher

## Purpose

把本地任意 Agent / Skill / 工具包按统一标准发布到 GitHub 公开仓库。

触发条件：
- 用户说"把这个上传到 GitHub / 发布到 GitHub / 推到我的 GitHub"
- 任何本地 skill / agent / 工具包要开源化
- 用户提到"参考 github-project-radar 的格式"

## 标准化输出

每个发布的仓库必须满足（这是用户在 7 个仓库上验证过的标准）：

| 维度 | 要求 |
|------|------|
| 文件结构 | `SKILL.md` + `README.md` + `LICENSE`（MIT）+ `.gitignore` + `references/` + `assets/` |
| 语言 | **中文优先**，5 段结构（项目说明 / 适合谁用 / 快速开始 / 文件说明 / 推荐流程） |
| description | 用「卡点+方案+结果」口语化结构，**不写书名号**、**不写"X 的人"死板定义** |
| topics | 6 个，覆盖技术领域 + 内容领域 + 工具类型 |
| release | v1.0.0 发布，notes 写明脱敏保证 |
| commit message | 中文允许（zsh 提交含中文逗号"nothing to commit"是误报，实际成功） |

**description 改写规则**（来自 ~/.workbuddy/MEMORY.md）：
- 四块信息必到：谁用 + 卡在啥时 + 怎么干 + 拿到啥
- 问号起头、逗号接方案、句尾具体物
- 数字实在（5 套、30 秒、1 分钟、100+）
- 不写：开源/灵活/可扩展/智能/什么场景/一站式

## 标准工作流

### Step 1: 脱敏检查（**绝对不能跳过**）

发布前**逐文件扫描**以下高风险模式：

```bash
patterns=(
  '<USER_DIR>/'           # 本地绝对路径（用户根目录 = 个人身份）
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'  # 邮箱
  '1[3-9][0-9]{9}'   # 手机号
  'sk-[A-Za-z0-9]{20,}'  # OpenAI key
  'ghp_[A-Za-z0-9]{20,}'  # GitHub PAT
  'github_pat_[A-Za-z0-9]{20,}'  # 新版 PAT
  'api[_-]?key|secret|password|token'  # 凭据关键词
  '<YOUR_NAME>|<OTHER_NAME>'  # 真实人名（按需调整）
)
grep -rEn "${patterns[@]}" <本地源目录>
```

**注意**：`privacy_scan()` 默认会跳过规则定义自身(`publish.py` 和 `SKILL.md`),否则会自匹配。

**判断标准**：
- 任何 API key / token / secret / 邮箱 / 手机号 / 真实人名 / 直播间 ID → 标记为不能公开
- 通用脚本代码 + 通用 README + 配置文件（无密钥） → 可公开
- 内部编号（S01-S23 之类）→ 改成占位符（`{material_id}`）
- 硬性排除规则（如"排除施言"）→ 改成可配置参数（`speaker_filter`）
- 引流句（如"关注施言"）→ 改成参数（`{creator_name}`）

**报告 → 用户拍板 → 再执行**。绝不自己拿主意开公开。

### Step 2: 文件结构对齐

最小集（参考 github-project-radar）：

```
<repo-name>/
├── README.md           # 中文,5 段结构
├── SKILL.md            # 可复用的技能说明
├── LICENSE             # MIT
├── .gitignore          # Python/编辑器/运行产物
├── references/         # 深度文档
│   └── *.md
└── assets/             # 模板/示例
    └── *.md
```

### Step 3: GitHub 操作（核心封装）

完整 Python 脚本，封装了**今天踩过的所有坑**：

```python
# scripts/publish.py
"""
GitHub Skill Publisher - 标准化发布脚本
封装了 auto_init 覆盖、URL 转码、PUT 必传 sha 等坑
"""
import base64, json, os, sys, urllib.request, urllib.parse

GITHUB_API = 'https://api.github.com'

def auth_headers(token):
    return {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github+json',
    }

def create_repo(token, name, description, private=False):
    """建空仓。auto_init=True,后续上传时记得带 sha。"""
    payload = {
        'name': name,
        'description': description,
        'private': private,
        'auto_init': True,
    }
    req = urllib.request.Request(
        f'{GITHUB_API}/user/repos',
        data=json.dumps(payload).encode('utf-8'),
        headers=auth_headers(token),
        method='POST',
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def upload_file(token, owner, repo, path, local_path, message=None):
    """上传单个文件。

    关键坑：auto_init 仓里的 README 必须先 GET 拿 sha 再 PUT,否则 422。
    """
    with open(local_path, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode('utf-8')

    # 先 GET 拿 sha（如果文件已存在）
    sha = None
    url = f'{GITHUB_API}/repos/{owner}/{repo}/contents/{urllib.parse.quote(path, safe="/")}'
    try:
        req = urllib.request.Request(url, headers=auth_headers(token))
        with urllib.request.urlopen(req) as r:
            sha = json.loads(r.read())['sha']
    except urllib.error.HTTPError:
        pass  # 新文件,无 sha

    payload = {
        'message': message or f'feat: 上传 {path}',
        'content': content_b64,
    }
    if sha:
        payload['sha'] = sha

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=auth_headers(token),
        method='PUT',
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def set_topics(token, owner, repo, topics):
    """改 topics（注意：accept header 要带 mercy-preview）"""
    url = f'{GITHUB_API}/repos/{owner}/{repo}/topics'
    req = urllib.request.Request(
        url,
        data=json.dumps({'names': topics}).encode('utf-8'),
        headers={
            **auth_headers(token),
            'Accept': 'application/vnd.github.mercy-preview+json',
        },
        method='PUT',
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def set_visibility(token, owner, repo, private=False):
    """改公开/私有。"""
    url = f'{GITHUB_API}/repos/{owner}/{repo}'
    req = urllib.request.Request(
        url,
        data=json.dumps({'private': private}).encode('utf-8'),
        headers=auth_headers(token),
        method='PATCH',
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def create_release(token, owner, repo, tag, name, body):
    """发 release。"""
    url = f'{GITHUB_API}/repos/{owner}/{repo}/releases'
    req = urllib.request.Request(
        url,
        data=json.dumps({
            'tag_name': tag,
            'name': name,
            'body': body,
            'draft': False,
            'prerelease': False,
        }).encode('utf-8'),
        headers=auth_headers(token),
        method='POST',
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())
```

### Step 4: 验证 + 报告

发布后必须做：
1. `WebFetch` 仓库主页，确认 README 渲染正常（**特别检查**没有空链接、没有未脱敏信息）
2. 用上面的脱敏 grep 再扫一遍远端文件（因为 base64 编码后再解码可能有隐藏字符）
3. 输出结构化报告：哪些仓库、文件清单、topics、release 链接

## 踩过的坑（必看）

| 坑 | 现象 | 解决 |
|----|------|------|
| `auto_init` README 覆盖 | PUT 返回 422 "sha wasn't supplied" | 先 GET 拿 sha 再 PUT |
| 中文路径 URL | `urllib.error.HTTPError 404` | `urllib.parse.quote(path, safe='/')` |
| 清理绝对路径时误删链接语法 | 渲染后 5 个目录链接空白 | 重写 README,补完整 `[text](path)` |
| 私有仓改公开 | `private` topic 残留 | 改完 visibility 立即重设 topics |
| 描述拼接中英混排 | 仓库主页"中英缝合感" | 全部用纯中文一句话 |
| commit message 中文逗号 | zsh 显示"nothing to commit" 误报 | 实际成功,看 git log 确认 |
| 凭据来源失效 | Keychain PAT 读不到、gh CLI 未登录 | 必问用户贴 PAT,只用一次立即清空 |

## 客观挑刺清单（必做项）

发布完 7 个仓库后，**用户专门要求挑刺**总结的常见遗漏项：

| 类型 | 常见问题 | 必查 |
|------|---------|------|
| 隐私 | 绝对路径 / 邮箱 / 手机号 / 硬编码密钥 | 必查 |
| 隐私 | 旧版本 `private` / `wip` / `archived` topic 残留 | 改完 visibility 必查 |
| 链接 | README 清理时把 `[text](path)` 语法误删 | 必查 |
| 元数据 | description / topics / release 三者一致 | 必查 |
| 元数据 | `chinese` topic 多仓重复 | 收益低,不修 |
| 流程 | commit message / Issues 模板 | 收益低,不修 |

## 收尾规范

发布完一个项目后，必须：
1. `unset GH_TOKEN` —— 凭据立即从环境清空
2. 临时文件 `rm -rf /tmp/xxx-review` —— 不留痕
3. 写 memory：今天推了几个仓、commit hash、踩了什么坑
4. 主动挑刺 + 报告，让用户决定是否继续

## 适用场景

- 本地 Agent / Skill / 工具包的开源化
- 私有仓改公开（必带逐文件脱敏审查）
- 旧仓库中文化 / 重写
- 批量仓库的 description / topics 同步
