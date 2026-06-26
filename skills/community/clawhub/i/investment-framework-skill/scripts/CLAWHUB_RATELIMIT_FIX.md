#  ClawHub 定时任务修复 - 2026-03-20 09:51

## 问题根因

**定时任务未执行的原因**：
1. ❌ 脚本路径错误：定时任务指向 `/tmp/investment-framework-skill/` 但实际在 `~/.openclaw/workspace/investment-framework-skill/`
2. ❌ 登录检查逻辑错误：脚本检查 `clawhub publish --help` 失败但 CLI 实际已安装

## 已修复

1. ✅ 修复脚本路径：使用动态路径 `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
2. ✅ 修复登录检查：改用 `command -v clawhub`
3. ✅ 手动执行第 2 批发布（5 个技能成功）
4. ✅ 手动执行第 3 批发布（5 个技能成功）

## 速率限制

**ClawHub 限制**：每小时最多 5 个新技能

**已发布**：10 个技能（第 2 批 + 第 3 批）

**下次可发布**：2026-03-20 10:50 后

## 剩余技能（17 个）

### 第 4 批（5 个）- 10:50 执行
- duan-yongping-investor
- li-lu-investor
- wu-jun-investor
- qiu-valuation
- qiu-quality

### 第 5 批（5 个）- 11:50 执行
- duan-culture
- duan-longterm
- li-civilization
- li-china
- wu-ai

### 第 6 批（2 个）- 12:50 执行
- wu-data
- （预留缓冲）

## 新定时任务配置

```bash
# 删除旧配置
crontab -l | grep -v "auto-publish-clawhub" | crontab -

# 添加新配置（每小时执行一批）
(crontab -l 2>/dev/null; echo "50 10 * * * /home/admin/.openclaw/workspace/investment-framework-skill/scripts/auto-publish-clawhub.sh 4 >> /home/admin/.openclaw/workspace/investment-framework-skill/scripts/publish.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "50 11 * * * /home/admin/.openclaw/workspace/investment-framework-skill/scripts/auto-publish-clawhub.sh 5 >> /home/admin/.openclaw/workspace/investment-framework-skill/scripts/publish.log 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "50 12 * * * /home/admin/.openclaw/workspace/investment-framework-skill/scripts/auto-publish-clawhub.sh 6 >> /home/admin/.openclaw/workspace/investment-framework-skill/scripts/publish.log 2>&1") | crontab -
```

## 已发布技能列表（10 个）

### 第 2 批（21:15）✅
1. industry-analyst（行业分析师）
2. future-forecaster（未来预测师）
3. cycle-locator（周期定位师）
4. stock-picker（选股专家）
5. portfolio-designer（组合设计师）

### 第 3 批（22:15）✅
6. global-allocator（全球配置师）
7. simple-investor（简单投资者）
8. bias-detector（认知偏差检测器）
9. second-level-thinker（第二层思维者）
10. qiu-guolu-investor（邱国鹭投资智慧）

## 待发布技能（17 个）

等待速率限制解除后继续发布。

---

*更新时间：2026-03-20 09:51*
