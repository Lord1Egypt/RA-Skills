# 更新检查

> ⚠️ **用户数据安全**：`~/.myknowledge/` 与 Skill 文件分离，更新/重装不会影响你的知识库、配置和需求记录。

---

## 触发方式

### 自动触发（每次调用 MyKnowledge 时）
- 在 `core/main.md` 的"使用前检查"步骤 3 中自动执行
- 检查 `skill-state.yaml` 中的 `update_check.last_check` 字段
- 计算距离今天的天数：
  - 如果 `last_check` 不存在或距离 ≥ `interval_days`（默认 7 天）→ 执行更新检查
  - 如果距离 < `interval_days` → 跳过检查
- 检查完成后，更新 `last_check` 为今天日期

### 手动触发
- 用户主动问："检查更新"、"有新版本吗"

---

## 各安装源检查策略

| 安装源 | 检查方式 | 升级方式 |
|--------|---------|---------|
| skillhub_web | 无自动通知，需手动检查 | 在 SkillHub 中搜索 my-knowledge 并重新安装，或对 AI 说"安装 my-knowledge 技能" |
| skillhub_cli | `skillhub list` 查看可用版本 | `skillhub upgrade myknowledge` |
| clawhub | `clawhub list --outdated` | `clawhub update myknowledge` |
| github_zip | 访问 https://github.com/CoderMoray/MyKnowledge/releases | 下载新版 ZIP 解压覆盖 |
| github_clone | `git fetch origin` + 检查远程版本 | `git pull origin main` |
| manual/unknown | 访问 https://github.com/CoderMoray/MyKnowledge/releases | 手动下载覆盖 |

---

## 检查实现

### 日期计算逻辑
```
1. 读取 skill-state.yaml 中的 update_check.last_check（格式：YYYY-MM-DD）
2. 获取今天日期（YYYY-MM-DD 格式）
3. 计算两个日期之间的天数差：
   - 使用 Python: `(datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(last_check, "%Y-%m-%d")).days`
   - 或让 AI 模型直接计算日期差
4. 如果天数差 ≥ interval_days（默认 7）→ 执行检查
5. 如果天数差 < interval_days → 跳过检查
```

### GitHub 安装源（github_clone / github_zip）
```bash
# 获取远程最新版本
git ls-remote --tags https://github.com/CoderMoray/MyKnowledge.git

# 或访问 GitHub API
curl -s https://api.github.com/repos/CoderMoray/MyKnowledge/releases/latest
```

### SkillHub / ClawHub 安装源
```bash
# SkillHub CLI
skillhub list

# ClawHub CLI
clawhub list --outdated
```

---

## 配置

在 `skill-state.yaml` 中（由 MyKnowledge 自动维护）：

```yaml
update_check:
  source: "github_clone"      # 安装源（首次检测后写入）
  last_check: "2026-06-05"    # 最后检查日期（YYYY-MM-DD）
  interval_days: 7             # 检查间隔（可从 settings.yaml 覆盖）
  enabled: true                # 是否启用自动检查
```

在 `settings.yaml` 中（默认配置）：

```yaml
update_check:
  enabled: true
  interval_days: 7  # 7 天检查一次
```

---

## 检查流程

```
1. 读取 skill-state.yaml 中的 update_check 配置
2. 获取今天日期（YYYY-MM-DD 格式）
3. 计算距离 last_check 的天数：
   - 如果 last_check 不存在 → 视为需要检查（首次）
   - 如果 last_check 存在 → 计算天数差
4. 如果天数差 ≥ interval_days → 执行检查
5. 根据安装源执行对应的检查策略
6. 如果发现新版本 → 礼貌提示用户
   - 示例："发现新版本 v1.4.8，当前版本 v1.4.71。要不要更新？"
   - 提供更新命令或操作步骤
7. 如果检查失败 → 自动忽略，不影响正常使用
8. 更新 last_check 为今天日期（无论检查成功失败）
```
