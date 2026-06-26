# NutriCoach Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

一个全面的个人健康数据管理与智能饮食推荐系统。

## 功能亮点

- 📊 **体重趋势追踪** - 30天数据可视化
- 🍽️ **饮食日志** - 自动计算营养，支持569种中餐食物
- 📷 **OCR 拍照识别** - 扫描食品包装自动提取营养信息
- 🥬 **Pantry 食材管理** - 库存追踪、过期提醒、分类管理
- 🤖 **智能菜谱推荐** - 基于库存和营养缺口生成菜谱
- 🌐 **Web 仪表板** - 奢华精致风格，响应式设计
- 📤 **数据导出** - JSON/CSV 格式

## 系统要求

| 平台 | 状态 | 说明 |
|------|------|------|
| **macOS** | ✅ 完全支持 | 主开发平台，所有功能可用 |
| Linux | ❌ 未测试 | 理论可行，但未验证 |
| Windows | ❌ 不支持 | 暂未适配 |

> **注意**：OCR 功能中的 macOS Vision 引擎仅在 macOS 上可用。其他平台可使用 Kimi Vision 引擎（需配置 API Key）。

## 功能模块

| 模块 | 状态 | 说明 |
|-----|------|------|
| 用户档案管理 | ✅ | 身高、体重、年龄、BMR/TDEE 计算 |
| 身体数据记录 | ✅ | 体重、BMI、体脂率时间序列 |
| 饮食日志 | ✅ | 每日三餐记录，支持中文食物 |
| 食材数据库 | ✅ | 内置 569 种中餐食物，支持扩展 |
| 饮食推荐 | ✅ | 基于目标和剩余预算的推荐 |
| 数据分析 | ✅ | 周报、营养分析、趋势统计 |
| OCR 拍照识别 | ✅ | 双引擎（Kimi + macOS），条形码优先匹配 |
| Pantry 食材管理 | ✅ | 库存追踪、过期提醒、分类管理 |
| 智能菜谱推荐 | ✅ | 基于库存和营养缺口的菜谱生成 |
| Web 评估面板 | ✅ | 可视化仪表盘，支持页签导航 |
| 数据导出 | ✅ | JSON/CSV 格式导出 |
| 数据备份 | ✅ | 自动备份与恢复 |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
# 1. 初始化数据库
python3 scripts/init_db.py --user robert

# 2. 设置用户档案
python3 scripts/user_profile.py --user robert set \
  --name "Robert" \
  --gender male \
  --birth-date 1994-05-15 \
  --height-cm 175 \
  --target-weight-kg 70 \
  --activity-level moderate \
  --goal-type maintain

# 3. 记录体重
python3 scripts/body_metrics.py --user robert log-weight --weight 72.5

# 4. 记录饮食
python3 scripts/meal_logger.py --user robert log \
  --meal-type lunch \
  --foods "米饭:150g, 鸡胸肉:100g, 西兰花:100g"

# 5. 查看每日摘要
python3 scripts/meal_logger.py --user robert daily-summary

# 6. 获取饮食推荐
python3 scripts/diet_recommender.py --user robert recommend --meal-type dinner

# 7. 生成报告
python3 scripts/report_generator.py --user robert nutrition --days 7
```

## 技术架构

```
nutricoach/
├── SKILL.md                    # Skill 入口文档（OpenClaw 使用）
├── README.md                   # 本文件（GitHub 展示）
├── requirements.txt            # Python 依赖
├── references/
│   ├── ARCHITECTURE.md         # 系统架构设计
│   ├── DATABASE_SCHEMA.md      # 数据库设计
│   ├── FEATURE_GUIDE.md        # 用户功能手册
│   └── DEVELOPER_GUIDE.md      # 开发者 API 参考
├── scripts/
│   ├── init_db.py              # 数据库初始化
│   ├── user_profile.py         # 用户档案管理
│   ├── body_metrics.py         # 身体数据记录
│   ├── meal_logger.py          # 饮食日志
│   ├── diet_recommender.py     # 饮食推荐
│   ├── food_analyzer.py        # 食物分析 + OCR 扫描
│   ├── food_ocr.py             # OCR 引擎封装
│   ├── food_matcher.py         # 食物匹配引擎
│   ├── pantry_manager.py       # 食材库存管理
│   ├── smart_recipe.py         # 智能菜谱推荐
│   ├── launch_dashboard.py     # 启动 Web 面板
│   ├── web_server.py           # Web 服务（页签式面板）
│   ├── report_generator.py     # 报告生成
│   ├── export_data.py          # 数据导出
│   ├── backup_db.py            # 数据库备份
│   ├── migrate_db.py           # 数据库迁移
│   └── logger.py               # 日志工具
└── data/
    ├── <username>.db           # 用户隔离的 SQLite 数据库
    └── backups/                # 自动备份目录
```

## 数据库设计

- **多用户隔离**: 每个用户独立 SQLite 文件
- **时间序列**: 体重、饮食支持历史追踪
- **营养计算**: 自动计算卡路里和宏量营养素
- **库存管理**: Pantry 表追踪食材剩余量和过期时间
- **可扩展**: 支持自定义食物添加

## Pantry 食材管理

```bash
# 添加食材（自动检测储藏位置）
python3 scripts/pantry_manager.py --user robert add \
  --food "鸡胸肉" --quantity 500 --expiry 2026-04-05

# 记录使用（自动扣减剩余）
python3 scripts/pantry_manager.py --user robert use \
  --item-id 1 --amount 200 --notes "做沙拉"

# 查看剩余库存
python3 scripts/pantry_manager.py --user robert remaining

# 查看快过期食材
python3 scripts/pantry_manager.py --user robert list --expiring 3
```

**储藏位置分类**:
- ❄️ 冰箱：冷藏食材
- 🧊 冷冻：冷冻肉类
- 📦 干货区：常温干燥食材
- 🌡️ 台面：室温短期存放

## 智能菜谱推荐

```bash
# 基于库存推荐菜谱
python3 scripts/smart_recipe.py --user robert --count 3
```

**推荐逻辑**:
1. 分析营养缺口（对比近期摄入 vs 目标）
2. 优先使用快过期食材
3. 动态调整库存阈值
4. 平衡蛋白质、碳水、脂肪

## Web 评估面板 (v2)

```bash
# 启动面板（自动打开浏览器）
python3 scripts/launch_dashboard.py --user robert

# 访问 http://127.0.0.1:5000
```

**页签功能**:
- 📊 **概览**: 今日数据、体重趋势、营养趋势、身体数据
- 🥬 **食材管理**: 按储藏位置分组的 pantry，支持使用/添加操作
- ⚖️ **体重记录**: 体重历史记录

## OCR 食品识别

```bash
# 静默扫描（自动处理）
python3 scripts/food_analyzer.py --user robert scan --image chips.jpg

# 使用特定引擎
python3 scripts/food_analyzer.py --user robert scan --image chips.jpg --engine macos

# 主动更新条形码数据
python3 scripts/food_analyzer.py --user robert update-by-barcode \
  --barcode 6941234567890 --calories 550 --protein 6.5
```

**支持的 OCR 引擎**:
- **Kimi Vision** (默认): 高精度，需要 API key
- **macOS Vision**: 本地免费，无需网络

## 数据管理

```bash
# 导出数据
python3 scripts/export_data.py --user robert --format json
python3 scripts/export_data.py --user robert --format csv -o ./exports

# 备份数据库
python3 scripts/backup_db.py --user robert backup
python3 scripts/backup_db.py --user robert list
python3 scripts/backup_db.py --user robert restore --file robert_20260327_164628.db
```

## 文档

| 文档 | 说明 |
|-----|------|
| [SKILL.md](SKILL.md) | OpenClaw Skill 入口文档 |
| [FEATURE_GUIDE.md](references/FEATURE_GUIDE.md) | 用户功能手册（详细使用说明） |
| [DEVELOPER_GUIDE.md](references/DEVELOPER_GUIDE.md) | 开发者 API 参考 |
| [ARCHITECTURE.md](references/ARCHITECTURE.md) | 系统架构设计 |
| [DATABASE_SCHEMA.md](references/DATABASE_SCHEMA.md) | 数据库设计 |

## 待完成

- [ ] 更多推荐算法（低碳、16:8 轻断食等）
- [ ] 周报/月报 HTML 模板
- [ ] 数据同步（多设备）
- [ ] 移动端适配

## 测试状态

所有核心脚本已通过测试：
- ✅ init_db.py - 数据库初始化
- ✅ user_profile.py - 用户档案创建/查询
- ✅ body_metrics.py - 体重记录/BMI计算
- ✅ meal_logger.py - 饮食记录/营养计算
- ✅ diet_recommender.py - 饮食推荐
- ✅ food_analyzer.py - 食物搜索/OCR扫描
- ✅ pantry_manager.py - 食材库存管理
- ✅ smart_recipe.py - 智能菜谱推荐
- ✅ launch_dashboard.py - Web 面板启动
- ✅ report_generator.py - 营养分析报告
- ✅ export_data.py - 数据导出
- ✅ backup_db.py - 数据库备份

---

*Last updated: 2026-03-28 (v2.0)*
