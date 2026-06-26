# ClawHub 定时任务配置指南

**配置时间：** 2026-03-19 20:20  
**状态：** ✅ 已配置

---

## 📋 定时任务配置

### Crontab 配置

```bash
# ClawHub 投资框架技能包自动发布 - 2026-03-19
# 每小时发布一批，避开速率限制（每小时最多 5 个技能）

# 第 2 批（21:15）- industry-analyst, future-forecaster, cycle-locator, stock-picker, portfolio-designer
15 21 19 3 * /tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh 2 >> /tmp/investment-framework-skill/publish.log 2>&1

# 第 3 批（22:15）- global-allocator, simple-investor, bias-detector, second-level-thinker, qiu-guolu
15 22 19 3 * /tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh 3 >> /tmp/investment-framework-skill/publish.log 2>&1

# 第 4 批（23:15）- duan-yongping, li-lu, wu-jun, + 2 个子技能
15 23 19 3 * /tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh 4 >> /tmp/investment-framework-skill/publish.log 2>&1

# 第 5 批（次日 00:15）- 5 个子技能
15 0 20 3 * /tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh 5 >> /tmp/investment-framework-skill/publish.log 2>&1

# 第 6 批（次日 01:15）- 最后 1 个子技能
15 1 20 3 * /tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh 6 >> /tmp/investment-framework-skill/publish.log 2>&1
```

---

## 📅 发布计划

| 批次 | 时间 | 技能数 | 技能列表 |
|------|------|--------|---------|
| **第 1 批** | 20:10 | 5 个 | ✅ 已完成（value-analyzer, moat-evaluator, intrinsic-value-calculator, decision-checklist, asset-allocator） |
| **第 2 批** | 21:15 | 5 个 | industry-analyst, future-forecaster, cycle-locator, stock-picker, portfolio-designer |
| **第 3 批** | 22:15 | 5 个 | global-allocator, simple-investor, bias-detector, second-level-thinker, qiu-guolu-investor |
| **第 4 批** | 23:15 | 5 个 | duan-yongping-investor, li-lu-investor, wu-jun-investor, qiu-valuation, qiu-quality |
| **第 5 批** | 00:15 | 5 个 | duan-culture, duan-longterm, li-civilization, li-china, wu-ai |
| **第 6 批** | 01:15 | 1 个 | wu-data |
| **总计** | - | **26** | - |

---

## 📂 相关文件

| 文件 | 说明 | 位置 |
|------|------|------|
| `auto-publish-clawhub.sh` | 自动发布脚本 | `/tmp/investment-framework-skill/scripts/` |
| `publish.log` | 发布日志 | `/tmp/investment-framework-skill/` |
| `CLAWHUB_PUBLISH_STATUS.md` | 发布状态报告 | `/tmp/investment-framework-skill/` |
| `CLAWHUB_PUBLISH_GUIDE.md` | 发布操作指南 | `/tmp/investment-framework-skill/` |

---

## 🔍 监控命令

### 查看发布日志

```bash
tail -f /tmp/investment-framework-skill/publish.log
```

### 查看定时任务

```bash
crontab -l | grep clawhub
```

### 手动触发发布

```bash
# 手动执行第 2 批
/tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh 2

# 自动模式（根据当前时间决定）
/tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh auto
```

### 检查发布状态

```bash
# 访问 ClawHub 主页
curl -s https://clawhub.ai/lj22503 | grep -o "投资框架" | wc -l
```

---

## ⚠️ 注意事项

### 速率限制

- **限制：** 每小时最多发布 5 个新技能
- **原因：** ClawHub API 限制
- **解决：** 每小时发布一批，每批 5 个技能

### 登录状态

- **Token：** 已配置在脚本中
- **有效期：** 长期有效（除非手动撤销）
- **检查：** `clawhub login --check`

### 错误处理

脚本会自动：
1. 检查登录状态
2. 记录所有操作到日志
3. 失败时返回错误码

---

## 📊 预期完成时间

| 批次 | 计划时间 | 预计完成 | 状态 |
|------|---------|---------|------|
| 第 1 批 | 20:10 | 20:12 | ✅ 已完成 |
| 第 2 批 | 21:15 | 21:17 | ⏳ 等待中 |
| 第 3 批 | 22:15 | 22:17 | ⏳ 等待中 |
| 第 4 批 | 23:15 | 23:17 | ⏳ 等待中 |
| 第 5 批 | 00:15 | 00:17 | ⏳ 等待中 |
| 第 6 批 | 01:15 | 01:16 | ⏳ 等待中 |

**全部完成：** 2026-03-20 01:16

---

## 🔗 相关链接

- **ClawHub 主页：** https://clawhub.ai/lj22503
- **GitHub 仓库：** https://github.com/lj22503/investment-framework-skill
- **发布状态：** `/tmp/investment-framework-skill/CLAWHUB_PUBLISH_STATUS.md`

---

## 📞 故障排除

### 问题 1：发布失败

**症状：** 日志显示 "Rate limit"

**解决：** 等待 1 小时后重试

### 问题 2：登录失效

**症状：** 日志显示 "Not logged in"

**解决：** 重新登录
```bash
clawhub login --token "YOUR_TOKEN"
```

### 问题 3：脚本权限

**症状：** "Permission denied"

**解决：** 添加执行权限
```bash
chmod +x /tmp/investment-framework-skill/scripts/auto-publish-clawhub.sh
```

---

**配置完成！** 🎉

**下次检查：** 21:15 查看第 2 批发布日志
