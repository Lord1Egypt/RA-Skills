# 南昌嘉宝莉 Skill · Nanchang Carpoly 🎨

南昌嘉宝莉（江西陶乐嘉实业有限公司）——嘉宝莉南昌总代智能客服 Skill。

## 安装

### 方式一：一句话安装（推荐）

对 AI 说：

> 安装南昌嘉宝莉 skill

### 方式二：命令行安装

```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/Liubuq-sys/nanchang-jbl-skill/main/install.sh | bash
```

```powershell
# Windows
powershell -c "irm https://raw.githubusercontent.com/Liubuq-sys/nanchang-jbl-skill/main/install.ps1 | iex"
```

### 方式三：ClawHub 安装

```bash
npx clawhub install nanchang-jbl
```

## 触发关键词

说这些词即可自动触发：
- 南昌嘉宝莉、嘉宝莉、油漆、涂料、乳胶漆、艺术漆、防水涂料
- 装修、刷墙、翻新、陶乐嘉、买漆、墙面施工

## 能力

| 场景 | 说明 |
|------|------|
| 🏪 门店基础咨询 | 地址、电话、营业时间、交通指引 |
| 🛒 商品查询与库存 | 嘉宝莉全系列产品信息、价格 |
| 🎯 商品推荐与导购 | 按场景（儿童房/厨卫/翻新等）推荐 |
| 💰 促销与会员权益 | 优惠活动、会员办理、积分规则 |
| 🔧 售后处理与服务 | 退换货政策、保修、投诉渠道 |
| 🏠 到店引导与体验 | 预约看色卡、样板间、试刷 |
| 🛠️ 施工/安装服务 | 包工包料、施工流程、报价 |
| 🌟 品牌与信任背书 | 公司资质、荣誉、案例 |
| 📍 门店位置推荐 | 根据顾客位置智能推荐最近门店 |

## 文件结构

```
nanchang-jbl/
├── SKILL.md                    # 核心技能文件
├── references/
│   ├── business-info.md        # 门店基础信息
│   ├── services.md             # 商品信息
│   ├── recommendations.md      # 推荐逻辑
│   ├── promotions.md           # 促销活动
│   ├── after-sales.md          # 售后政策
│   ├── experience.md           # 到店体验
│   ├── construction.md         # 施工服务
│   ├── brand.md                # 品牌文化
│   └── stores.md               # 渠道商门店目录
├── version.json
├── CHANGELOG.md
├── install.sh
├── install.ps1
└── .gitignore
```
