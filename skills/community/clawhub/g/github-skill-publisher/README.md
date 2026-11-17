# GitHub Skill Publisher

本地 Agent / Skill / 工具包想发到 GitHub 公开仓库？不想每次踩一遍 auto_init 覆盖、中文路径 404、private topic 残留这些坑？跑这一套，10 分钟发完 6 文件 + topics + release。

## 适合谁用

- 经常把本地 skill / agent / 工具包开源化的开发者
- 想给多个 GitHub 仓库做统一 description / topics 同步的人
- 需要把私有仓改公开、又怕误发个人信息的协作者

## 快速开始

### 一键发布

```bash
export GH_TOKEN='ghp_xxx'  # 从 https://github.com/settings/tokens 生成,选 Contents 读写权限

python3 scripts/publish.py <owner> <repo-name> <本地目录> "口播博主卡开头？5 套钩子公式，30 秒出脚本"
```

脚本会自动：脱敏检查 → 建空仓 → 逐文件上传 → 打印完成链接。

### 单独调用 API 函数

```python
import sys, os
sys.path.insert(0, 'scripts')
from publish import privacy_scan, create_repo, upload_dir, set_topics, create_release, set_visibility

# 脱敏检查
issues = privacy_scan('/path/to/skill')
if not issues:
    create_repo(token, 'my-skill', '一句话描述', private=False, topics=['chinese', 'tool', 'github'])
    upload_dir(token, '<owner>', 'my-skill', '/path/to/skill')
    create_release(token, '<owner>', 'my-skill', 'v1.0.0', 'v1.0.0', '首发版本说明...')
```

## 文件说明

```
github-skill-publisher/
├── SKILL.md                    # 完整工作流定义（含脱敏标准、踩坑清单、挑刺项）
├── README.md                   # 本文件,使用文档
├── LICENSE                     # MIT
├── .gitignore                  # Python / 编辑器 / 运行产物
├── scripts/
│   └── publish.py              # 核心脚本,6 个 API 封装函数
└── references/
    └── cheatsheet.md           # 5 分钟快查表
```

## 核心 API 函数

| 函数 | 用途 |
|------|------|
| `privacy_scan(local_dir, ignore_files)` | 脱敏检查,扫绝对路径/邮箱/手机号/硬编码密钥 |
| `create_repo(token, name, desc, private, topics)` | 建空仓 |
| `upload_dir(token, owner, repo, local_dir, file_order)` | 递归上传整个目录 |
| `set_topics(token, owner, repo, topics)` | 改 topics |
| `set_visibility(token, owner, repo, private)` | 改公开/私有 |
| `create_release(token, owner, repo, tag, name, body)` | 发 release |

## 推荐流程

1. **脱敏检查**（绝对不能跳）→ 用 `privacy_scan()` 扫源目录
2. **建仓** → `create_repo(auto_init=True)`
3. **上传文件** → `upload_dir()` 自动处理 sha 校验
4. **补 topics** → 6 个,按"技术领域 + 内容领域 + 工具类型"配
5. **发 release** → v1.0.0 + 脱敏保证说明
6. **WebFetch 验证** → 看 GitHub 主页 README 渲染正常
7. **凭据清理** → `unset GH_TOKEN` + `rm -rf /tmp/*-review`

## 踩过的坑（已封装,不用再踩）

- `auto_init` 创建的 README 覆盖必须先 GET 拿 sha 再 PUT,否则 422
- 中文路径 URL 要 `urllib.parse.quote(path, safe='/')`,否则 404
- 私有改公开后 `private` topic 残留,要立即重设
- 清理绝对路径时容易把 `[text](path)` 链接语法误删,渲染成空白
- zsh 提交含中文逗号 commit message 显示"nothing to commit" 是误报,实际成功
- description 拼接中英混排会显得"缝合",必须纯中文

## description 改写规则

**四块信息必到**（谁用 / 卡在啥时 / 怎么干 / 拿到啥）：

- 问号起头抛出卡点
- 数字要实在（5 套、30 秒、1 分钟、100+）
- 句尾给具体物（脚本 / 清单 / HTML / Markdown）
- 禁忌词：开源/灵活/可扩展/智能/一站式

## 反馈

用着有问题？去 GitHub Issues 提。
