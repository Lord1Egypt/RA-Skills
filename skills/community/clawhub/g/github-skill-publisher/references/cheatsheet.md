# GitHub Skill Publisher Cheatsheet

## 5 分钟快查

### 标准发布流程

```bash
# 1. 脱敏检查
python3 ../github-skill-publisher/scripts/publish.py <owner> <repo> <local-dir> "<description>"

# 2. 单独补 topics
python3 -c "
import sys; sys.path.insert(0, '../github-skill-publisher/scripts')
from publish import set_topics
import os
set_topics(os.environ['GH_TOKEN'], '<owner>', '<repo>', ['topic1', 'topic2', ...])
"

# 3. 单独补 release
python3 -c "
import sys; sys.path.insert(0, '../github-skill-publisher/scripts')
from publish import create_release
import os
create_release(os.environ['GH_TOKEN'], '<owner>', '<repo>', 'v1.0.0', 'v1.0.0', '## 首发版本\n...')
"
```

### 私有改公开流程

```bash
# 1. 拉全量内容到本地（GitHub API 私有仓要 PAT）
# 2. 跑脱敏检查
python3 -c "
import sys; sys.path.insert(0, '../github-skill-publisher/scripts')
from publish import privacy_scan
issues = privacy_scan('/path/to/repo')
print(issues)
"

# 3. 修复 issues
# 4. 推回原文件
# 5. 改 visibility
python3 -c "
import sys; sys.path.insert(0, '../github-skill-publisher/scripts')
from publish import set_visibility
import os
set_visibility(os.environ['GH_TOKEN'], '<owner>', '<repo>', private=False)
"

# 6. 清理残留的 private topic
python3 -c "
import sys; sys.path.insert(0, '../github-skill-publisher/scripts')
from publish import set_topics
import os
set_topics(os.environ['GH_TOKEN'], '<owner>', '<repo>', ['new', 'topics'])
"
```

## 必查项

| 检查 | 工具 |
|------|------|
| 绝对路径 | `privacy_scan()` |
| 邮箱/手机号 | `privacy_scan()` |
| 硬编码密钥 | `privacy_scan()` |
| README 链接是否完整 | `WebFetch` 主页验证 |
| topic 残留 | 看 `topics` 列表 |
| description 一致性 | description / topics / README 三者对照 |

## description 改写模板

```
[人群][卡点场景]?[具体方式],[具体结果]。
```

例：
- 口播博主每条视频卡开头 10 分钟？5 套钩子公式轮换，30 秒出能拍的脚本。
- 囤了一堆素材不知道先拍哪条？5 维评分表，1 分钟排出 A/B/C 优先级。

禁忌词：开源/灵活/可扩展/智能/什么场景/一站式/全方位

## topics 选 6 个

按 [技术领域] + [内容领域] + [工具类型] 配：

例：
- chinese, content-marketing, hook-formula, script-writing, short-video, sop

## release notes 必含

```
## 首发版本

[一句话描述]

### 包含内容
- ...

### 脱敏保证
- ...
```

## 不修（收益低）

- `chinese` topic 多仓重复
- 缺 Issues 模板
- commit message 风格统一
