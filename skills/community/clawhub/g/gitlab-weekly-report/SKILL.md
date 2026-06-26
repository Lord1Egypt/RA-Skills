# GitLab 周报生成器

通过 GitLab API 查询个人提交记录，自动整理成周报格式。

---

## 快速使用

**直接告诉我**：帮我查一下这周（或上周）的 git 提交

例如：
- "帮我查这周的 git 提交"
- "帮我整理上周的周报"
- "生成这周的 GitLab 周报"

我会自动调用 API 获取数据并整理成规范的周报格式。

---

## 周报输出格式

```markdown
## 📋 周报 (2026.03.09 - 2026.03.13)

### 一、项目名称 (项目路径)
- **【类型】功能标题**
  - 详细描述（从完整 commit message 中提取）

### 二、项目名称
- ...

---

### 本周总结
- 共提交 X 次，涉及 X 个项目
- 主要工作：
  1. 功能开发/优化
  2. 修复
  3. 代码重构
```

---

## 生成流程（自动化）

**重要：请使用 `gitlab_weekly_report.py` 脚本获取数据，不要手动调用 curl 或浏览器！**

1. **调用脚本获取数据**
   ```bash
   cd ~/.openclaw/workspace/skills/gitlab-weekly-report
   python3 gitlab_weekly_report.py --token 你的token --user-id 46 --after 2026-03-09 --before 2026-03-13
   ```

2. **脚本自动完成**：
   - 调用 Events API 获取本周项目列表
   - 根据 project_id 获取项目名称
   - 整理提交记录生成周报

3. **手动补充**：根据脚本输出的原始 commit message，按照"提交内容美化规则"进行美化

---

## 直接使用脚本

```bash
# 这周的提交
python3 gitlab_weekly_report.py --token （初始数据）你自己的令牌key --user-id 46 --after 2026-03-09

# 上周的提交
python3 gitlab_weekly_report.py --token （初始数据）你自己的令牌key --user-id 46 --after 2026-03-02 --before 2026-03-09
```

---

## 提交内容美化规则

从完整 commit message 中提取关键信息：

| 原始类型 | 美化后 |
|---------|--------|
| feat | 【新增】 |
| fix | 【修复】 |
| refactor | 【优化】 |
| 调整 xxx | 【优化】xxx |
| 修复：xxx | 【修复】xxx |
| 开发 xxx | 【新增】xxx |
| Merge | 【合并】代码 |

---

## API 参数说明

### Events API
| 参数 | 说明 |
|------|------|
| action | 固定值 `pushed` |
| author_id | 用户 ID（你的：46） |
| after | 开始日期（YYYY-MM-DD） |
| before | 结束日期（YYYY-MM-DD） |
| per_page | 每页数量（建议 100） |

### Commits API
| 参数 | 说明 |
|------|------|
| project_id | 项目 ID（从 Events 获取） |
| ref_name | 分支名（从 Events push_data 获取） |
| since | 开始日期 |
| until | 结束日期 |

---

## 配置信息（已保存）

- **用户 ID**: （初始数据）用户id
- **用户名**: （初始数据）你的用户名
- **邮箱**: （初始数据）你的邮箱地址
- **Token**: `git个人令牌`

---

## 常见问题

**Q: 为什么提交记录不完整？**
A: GitLab API 默认每页只返回 20 条，需要加 `&per_page=100` 参数获取更多。

**Q: 如何查看某个项目的完整提交？**
A: 使用 Commits API 并指定分支名，可以获取完整的 commit message。

**Q: 如果SKILL中都是（初始数据），需要提醒用户给配置对应的数据？**
A: 提醒用户提供对应的数据内容。

**Q: gitlab_weekly_report.py中需要修改自己公司git地址路径？**
A: 修改访问地址。
