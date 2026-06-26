# NutriCoach 功能手册

> 面向用户的完整功能说明，非开发文档。

---

## 1. 用户档案管理

### 功能
记录身体基本信息，自动计算代谢率。

### 数据项
| 字段 | 说明 | 用途 |
|-----|------|------|
| 身高 | cm | BMI 计算 |
| 体重 | kg | TDEE 计算 |
| 年龄 | 自动计算 | BMR 计算 |
| 性别 | male/female | BMR 公式选择 |
| 活动水平 | 久坐/轻度/中度/高度/极高 | TDEE 乘数 |
| 目标 | 减脂/维持/增肌 | 热量目标调整 |

### 自动计算
- **BMR**（基础代谢率）：Mifflin-St Jeor 公式
- **TDEE**（每日总消耗）：BMR × 活动系数

### 使用
```bash
# 设置档案
python3 scripts/user_profile.py --user <name> set \
  --gender male --birth-date 1994-05-15 \
  --height-cm 175 --activity-level moderate --goal-type maintain

# 查看档案
python3 scripts/user_profile.py --user <name> get
```

---

## 2. 身体数据记录

### 功能
记录体重、体脂等身体指标，追踪趋势。

### 自动计算
- **BMI**：体重(kg) / 身高(m)²
- **趋势**：7天/30天变化

### 使用
```bash
# 记录体重
python3 scripts/body_metrics.py --user <name> log-weight \
  --weight 72.5 --body-fat 18.5

# 查看趋势
python3 scripts/body_metrics.py --user <name> trend --days 30
```

---

## 3. 饮食日志

### 功能
记录每日三餐，自动计算营养。

### 食物格式
```
米饭:150g, 鸡胸肉:100g, 西兰花:100g
```

### 自动计算
- 每道菜的热量、蛋白质、碳水、脂肪
- 每日总计
- 剩余可摄入（vs TDEE）

### 使用
```bash
# 记录一餐
python3 scripts/meal_logger.py --user <name> log \
  --meal-type lunch \
  --foods "米饭:150g, 鸡胸肉:100g"

# 查看今日摘要
python3 scripts/meal_logger.py --user <name> daily-summary
```

---

## 4. 食材数据库

### 内置数据
- **569 种中餐食物**：主食、肉蛋、蔬菜、水果、零食等
- **营养数据**：每100g的热量、蛋白质、碳水、脂肪、纤维

### 自定义添加
```bash
# 手动添加
python3 scripts/food_analyzer.py --user <name> add-custom \
  --name "红烧肉" --calories 350 --protein 15 --carbs 20 --fat 25

# AI 助手识别添加（见第6章）

# OCR 扫描添加（见第6章）
```

### 搜索
```bash
python3 scripts/food_analyzer.py --user <name> search --query "牛肉"
```

---

## 5. 饮食推荐

### 功能
基于目标和剩余热量，推荐餐食组合。

### 推荐逻辑
- 根据 TDEE 计算每餐目标热量
- 从数据库选择食材组合
- 平衡蛋白质、碳水、脂肪

### 使用
```bash
# 推荐晚餐
python3 scripts/diet_recommender.py --user <name> recommend \
  --meal-type dinner --count 3

# 生成全天计划
python3 scripts/diet_recommender.py --user <name> daily-plan
```

---

## 6. OCR 食品识别

### 功能概述
通过拍照识别食品包装上的营养成分表，自动提取数据并与数据库匹配。

### 三种使用方式

| 方式 | 适用场景 | 配置 | 精度 |
|-----|---------|------|------|
| **AI 助手识别** | 有 AI 助手（如 OpenClaw） | 零配置 | ⭐⭐⭐⭐⭐ |
| **本地 OCR** | 命令行，macOS 用户 | 零配置 | ⭐⭐⭐ |
| **云端 OCR** | 命令行，需高精度 | 需 API key | ⭐⭐⭐⭐⭐ |

### 方式一：AI 助手识别（推荐）

直接向 AI 助手发送食品包装图片：

```
[发送图片]
"录入这个食材，生产日期 2025-01-15，共 3 盒"
```

助手会直接识别图片内容并录入数据库，**无需任何配置**。

**优势：**
- 零配置，开箱即用
- 识别精度高
- 支持对话式录入

### 方式二：本地 OCR（命令行）

使用 macOS 内置 Vision 框架：

```bash
python3 scripts/food_analyzer.py --user <name> scan --image chips.jpg --engine macos
```

**特点：**
- 完全免费
- 无需网络
- 隐私安全

### 方式三：云端 OCR（命令行）

配置云端 Vision API 获得更高精度：

**步骤 1：创建配置文件**
```bash
cp data/user_config.example.yaml data/user_config.yaml
```

**步骤 2：填入 API key**
```yaml
vision:
  api_key: "your-api-key"
  base_url: "https://api.moonshot.cn/v1"
  model: "kimi-k2.5"
```

**步骤 3：使用**
```bash
python3 scripts/food_analyzer.py --user <name> scan --image chips.jpg
```

**支持的 API 提供商：**
- Moonshot (Kimi)
- OpenAI
- 阿里 DashScope
- 其他兼容 OpenAI 接口的服务

### 工作流程

```
拍照 → OCR识别 → 数据库匹配 → 差异对比 → 用户确认 → 添加到数据库
```

### 核心特性
- **条形码优先匹配**：精准识别同款商品
- **静默模式**：小差异自动处理，大差异才提示
- **数据积累**：扫描过的商品自动入库

### 匹配结果类型

| 结果 | 说明 | 动作 |
|-----|------|------|
| ✅ **数据一致** | 条形码匹配，营养差异 <10% | 直接使用，无提示 |
| ⚠️ **建议更新** | 条形码匹配，营养差异 >10% | 提示更新命令 |
| ❌ **新商品** | 无条形码匹配 | 自动添加到数据库 |

### 注意事项
1. **拍照质量**：光线充足、文字清晰、避免反光
2. **角度**：尽量正对包装，避免倾斜
3. **完整性**：确保营养成分表完整入镜

### 配置示例

**user_config.yaml：**
```yaml
vision:
  api_key: "sk-xxxxx"
  base_url: "https://api.moonshot.cn/v1"
  model: "kimi-k2.5"
```

**说明：**
- 配置文件仅在使用命令行 + 云端 OCR 时需要
- AI 助手模式无需配置
- 本地 OCR 无需配置

---

## 7. 食材库存管理（Pantry）

### 功能
管理家中食材，追踪剩余量，过期提醒。

### 核心概念
| 概念 | 说明 |
|-----|------|
| 初始量 | 购买时的重量 |
| 剩余量 | 当前实际剩余（自动扣减） |
| 过期时间 | 到期自动提醒 |
| 使用记录 | 每次用量可追溯 |

### 使用
```bash
# 添加食材（过期日期可选，会自动计算）
python3 scripts/pantry_manager.py --user <name> add \
  --food "鸡胸肉" --quantity 500

# 手动指定过期日期
python3 scripts/pantry_manager.py --user <name> add \
  --food "鸡胸肉" --quantity 500 --expiry 2026-04-05

# 记录使用（自动扣减剩余）
python3 scripts/pantry_manager.py --user <name> use \
  --item-id 1 --amount 200 --notes "做沙拉"

# 查看剩余
python3 scripts/pantry_manager.py --user <name> remaining

# 查看快过期
python3 scripts/pantry_manager.py --user <name> list --expiring 3
```

### 自动过期日期计算
如果不指定 `--expiry`，系统会自动计算：
1. **优先**: 查询食物数据库中的默认保质期（如鸡胸肉2天、鸡蛋28天、燕麦365天）
2. ** fallback**: 按储藏位置使用默认值：
   - 冰箱: 7天 | 冷冻: 90天 | 干货区: 30天 | 台面: 5天

### 修改食材信息
```bash
# 修改生产日期和过期日期
python3 scripts/pantry_manager.py --user <name> update \
  --item-id 1 --purchase 2026-03-25 --expiry 2026-04-01

# 修改储藏位置
python3 scripts/pantry_manager.py --user <name> update \
  --item-id 1 --location freezer

# 添加备注
python3 scripts/pantry_manager.py --user <name> update \
  --item-id 1 --notes "已开封"
```

---

## 8. 智能菜谱推荐

### 功能
基于库存食材和营养缺口，推荐可做的菜。

### 推荐逻辑
1. **营养缺口分析**：对比近期摄入 vs 目标
2. **库存检查**：优先使用快过期食材
3. **动态阈值**：
   - 充足（≥3种 >50g）：正常推荐
   - 不足（<3种 >50g）：降级到>20g，提示补货
   - 极少（<3种 >0g）：包含所有，提示严重不足

### 使用
```bash
python3 scripts/smart_recipe.py --user <name> --count 3
```

**输出示例**：
```
🍳 推荐菜谱 (基于库存)

1. 番茄炒蛋
   可用食材: 鸡蛋x2, 番茄200g
   营养: 320卡 | 蛋白质 18g | 碳水 12g
   缺口: 需购买 葱

2. 鸡胸肉沙拉
   可用食材: 鸡胸肉150g, 生菜100g
   ...
```

---

## 9. 数据管理

### 备份
```bash
# 创建备份
python3 scripts/backup_db.py --user <name> backup

# 列出备份
python3 scripts/backup_db.py --user <name> list

# 恢复备份
python3 scripts/backup_db.py --user <name> restore --file backup_20260327_164628.db
```

### 导出
```bash
# 导出为 JSON
python3 scripts/export_data.py --user <name> --format json

# 导出为 CSV
python3 scripts/export_data.py --user <name> --format csv
```

---

## 10. Web 仪表盘

### 功能
可视化查看健康数据趋势。

### 启动
```bash
python3 scripts/launch_dashboard.py --user <name>
```

自动打开浏览器访问 `http://127.0.0.1:5000`

### 功能模块
- **概览**：体重趋势、今日营养、周统计
- **食材库**：库存管理、过期提醒
- **历史记录**：餐食记录、体重记录

---

## 快速命令参考

| 任务 | 命令 |
|-----|------|
| 初始化用户 | `python3 scripts/init_db.py --user <name>` |
| 设置档案 | `python3 scripts/user_profile.py --user <name> set ...` |
| 记录体重 | `python3 scripts/body_metrics.py --user <name> log-weight ...` |
| 记录餐食 | `python3 scripts/meal_logger.py --user <name> log ...` |
| 查看 pantry | `python3 scripts/pantry_manager.py --user <name> list` |
| 添加食材 | `python3 scripts/pantry_manager.py --user <name> add ...` |
| 启动 dashboard | `python3 scripts/launch_dashboard.py --user <name>` |

---

*完整 API 参考见 [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)*
