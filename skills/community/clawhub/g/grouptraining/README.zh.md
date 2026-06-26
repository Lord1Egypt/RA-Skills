# Likes Training Planner Skill 🏃

[English](README.en.md) | 中文

**My Likes 平台一站式训练计划解决方案**

数据获取 → 分析 → 生成 → 预览 → 确认 → 推送。一个 Skill 搞定所有！

---

## ⚠️ 重要：安装位置

**必须安装到正确目录才能正常工作：**

✅ **正确位置：**
```
~/.openclaw/workspace/skills/likes-training-planner/
```

❌ **错误位置（不会显示 API Key 输入框）：**
```
~/.openclaw/workspace/likes-training-planner/          # 错误：workspace 根目录
~/.openclaw/skills/likes-training-planner/            # 错误：缺少 workspace
/opt/homebrew/.../openclaw/skills/likes-training-planner/  # 错误：内置目录
```

---

## 🚀 快速开始

### 安装

**方式 1：一键安装（推荐）**
```bash
curl -fsSL https://gitee.com/chenyinshu/likes-training-planner/raw/main/install.sh | bash
```

**方式 2：手动安装**
```bash
# 1. 下载
cd ~/.openclaw/workspace/skills
curl -L -o likes-training-planner.skill \
  https://gitee.com/chenyinshu/likes-training-planner/releases/latest/download/likes-training-planner.skill

# 2. 解压（必须在 workspace/skills/ 目录）
unzip -q likes-training-planner.skill
rm likes-training-planner.skill

# 3. 重启 OpenClaw
openclaw gateway restart
```

### 配置

**OpenClaw Skill Center（推荐）：**
1. 打开 http://127.0.0.1:18789 → **Skills**
2. 找到 **likes-training-planner** 🏃
3. 点击 **Configure**，输入你的 Likes API Key
4. 保存

**注意：** API Key 输入框始终可见（保存后显示 `********`），方便随时查看或修改。

获取 API Key：https://my.likes.com.cn → 设置 → API 文档

### 使用

直接对 OpenClaw 说：
> "分析我过去30天的运动数据"
> 
> "根据我的记录，生成下周的训练计划"
> 
> "帮我制定一个8周马拉松备赛计划"

---

## 📋 完整工作流程

### 1. 获取数据
```bash
cd ~/.openclaw/workspace/skills/likes-training-planner
node scripts/fetch_activities.cjs --days 30 --output data.json
```

### 2. 分析
```bash
node scripts/analyze_data.cjs data.json
```

输出示例：
```json
{
  "period": { "days": 30, "start": "2026-02-01", "end": "2026-03-01" },
  "summary": {
    "totalRuns": 45,
    "totalKm": 156.5,
    "avgDailyKm": 5.2,
    "frequency": 1.5
  },
  "characteristics": "高频次、中等距离、有氧基础",
  "recommendations": ["可以适当增加间歇训练", "周末尝试更长距离"]
}
```

### 3. 生成计划
创建计划 JSON 文件：
```json
{
  "plans": [
    {
      "name": "40min@(HRR+1.0~2.0)",
      "title": "轻松有氧",
      "start": "2026-03-10",
      "weight": "q3",
      "type": "qingsong",
      "sports": 1
    }
  ]
}
```

### 4. 预览确认 ⭐ (v1.4)

**推送前务必预览！**

```bash
node scripts/preview_plan.cjs plans.json
```

显示内容：
- 📅 每日训练详情
- 📊 每周汇总
- 🏃 训练类型分布
- ⚡ 强度分布

交互选项：
- `[Y]` 确认并推送
- `[N]` 取消
- `[E]` 编辑计划文件

### 5. 推送到日历

确认后：

```bash
node scripts/push_plans.cjs plans.json
```

**一键预览+推送：**
```bash
# 先预览
node scripts/preview_plan.cjs plans.json && node scripts/push_plans.cjs plans.json
```

---

## 📚 脚本参考

| 脚本 | 功能 | 用法 |
|------|------|------|
| `fetch_activities.cjs` | 下载训练历史 | `--days 30 --output data.json` |
| `get_activity_detail.cjs` | 获取单个活动详情（含GPS） | `--id 12345 --mode detailed` |
| `analyze_data.cjs` | 分析模式 | `analyze_data.cjs data.json` |
| `fetch_plans.cjs` | 获取日历计划（42天） | `--start 2026-03-01` |
| `fetch_feedback.cjs` | 获取训练反馈（含教练点评状态） | `--start 2026-03-01 --end 2026-03-07` |
| `add_feedback_comment.cjs` | 添加教练点评 | `--feedback-id 123 --content "点评内容"` |
| `fetch_games.cjs` | 列出你的训练营 | `--output camps.json` |
| `fetch_game.cjs` | 获取训练营详情和成员 | `--game-id 973` |
| `fetch_ability.cjs` | 运动能力查询（能力值/预测成绩/配速区间） | `--runforce 51` 或 `--time-5km 32:28` |
| `preview_plan.cjs` | ⭐ 预览计划（v1.4） | `preview_plan.cjs plans.json` |
| `push_plans.cjs` | 推送计划（支持批量、覆盖） | `push_plans.cjs plans.json` |
| `configure.cjs` | 交互式配置 | `configure.cjs` |
| `set-config.cjs` | 快速配置 | `set-config.cjs API_KEY` |

---

## 🔧 训练代码格式

Likes `name` 字段格式：

```
# 简单任务
duration@(type+range)
30min@(HRR+1.0~2.0)

# 间歇组
{task1;task2}xN
{5min@(HRR+3.0~4.0);1min@(rest)}x3

# 完整训练
10min@(HRR+1.0~2.0);{1000m@(VDOT+4.0~5.0);2min@(rest)}x4;10min@(HRR+1.0~2.0)
```

完整指南见 [references/code-format.md](likes-training-planner/references/code-format.md)

---

## 📁 文件结构

```
~/.openclaw/workspace/skills/likes-training-planner/  ← 必须在这里！
├── SKILL.md                    # 主文档
├── references/
│   ├── api-docs.md            # API 文档
│   ├── code-format.md         # 代码格式参考
│   └── sport-examples.md      # 训练示例
└── scripts/
    ├── fetch_activities.cjs   # ⭐ 下载数据
    ├── get_activity_detail.cjs # ⭐ 活动详情（含GPS）
    ├── analyze_data.cjs       # ⭐ 分析模式
    ├── fetch_plans.cjs        # 获取计划
    ├── fetch_feedback.cjs     # 获取反馈
    ├── add_feedback_comment.cjs # 添加点评
    ├── fetch_games.cjs        # 列出训练营
    ├── fetch_game.cjs         # 训练营详情
    ├── fetch_ability.cjs      # 运动能力（能力值/预测成绩/配速区间）
    ├── preview_plan.cjs       # ⭐ 预览确认（v1.4）
    ├── push_plans.cjs         # 推送计划
    ├── configure.cjs          # 配置向导
    └── set-config.cjs         # 快速配置
```

---

## 🆕 更新日志

### v1.7.0 - 运动能力查询
- ✅ 新增 `fetch_ability.cjs` - 调用 GET /api/open/ability
- ✅ 支持按能力值（runforce）查预测成绩与配速区间（E/M/T/A/I/R）
- ✅ 支持按各距离成绩（time_5km / time_10km / time_hm / time_fm 等）反查能力值

### v1.6.0 - 活动详情与计划覆盖
- ✅ 新增 `get_activity_detail.cjs` - 获取单个活动详情（支持GPS轨迹）
- ✅ `push_plans` 新增 `overwrite` 参数 - 覆盖现有计划避免重复

### v1.5.0 - 完整 API 支持
- ✅ 新增 `fetch_plans.cjs` - 获取日历计划
- ✅ 新增 `fetch_feedback.cjs` - 获取训练反馈（含教练点评状态）
- ✅ 新增 `add_feedback_comment.cjs` - 添加教练点评
- ✅ 新增 `fetch_games.cjs` - 列出训练营
- ✅ 新增 `fetch_game.cjs` - 获取训练营详情和成员

### v1.4 - 预览与确认流程 ⭐
- ✅ 新增 `preview_plan.cjs` - 推送前预览
- ✅ 强制确认流程：预览 → 确认 → 推送
- ✅ 清晰的周计划可视化
- ✅ 用户确认后才推送

### v1.3 - 完整解决方案
- ✅ 新增 `fetch_activities.cjs` - 自动下载数据
- ✅ 新增 `analyze_data.cjs` - 智能训练分析
- ✅ 一个 Skill 完成所有：获取 → 分析 → 生成 → 推送
- ✅ 无需单独的 MCP 服务器

### v1.2 - Skill Center 集成
- ✅ OpenClaw Skill Center 支持
- ✅ 图形化配置界面
- ✅ .cjs 脚本兼容 ES Module

### v1.1 - 配置支持
- ✅ 配置向导
- ✅ 多种认证方式

### v1.0 - 初始版本
- ✅ 基础计划生成和推送

---

## 📝 许可证

MIT

---

## 🔗 链接

- **仓库**：https://gitee.com/chenyinshu/likes-training-planner
- **发布**：https://gitee.com/chenyinshu/likes-training-planner/releases
- **My Likes**：https://my.likes.com.cn

---

## ❓ 故障排除

### API Key 输入框不显示？

**检查安装位置：**
```bash
# 应该显示：~/.openclaw/workspace/skills/likes-training-planner/
ls ~/.openclaw/workspace/skills/likes-training-planner/

# 如果安装在其他位置，移动它：
mv ~/.openclaw/workspace/likes-training-planner ~/.openclaw/workspace/skills/
openclaw gateway restart
```

### Skill 没有出现在 Skill Center？

1. 检查目录结构：
   ```bash
   ls ~/.openclaw/workspace/skills/
   # 应该显示：likes-training-planner/
   ```

2. 验证 SKILL.md 存在：
   ```bash
   cat ~/.openclaw/workspace/skills/likes-training-planner/SKILL.md | head -10
   ```

3. 重启 OpenClaw：
   ```bash
   openclaw gateway restart
   ```

4. 强制刷新浏览器（Cmd+Shift+R）
