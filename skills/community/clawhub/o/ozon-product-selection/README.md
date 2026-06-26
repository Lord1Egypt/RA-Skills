# Ozon 电商选品 SKILL

根据用户指定的品类，自动搜索 Ozon 平台市场趋势、提取热门细分关键词，并从 1688 找到最优货源推荐。

更多有趣的电商SKILL，可以通过https://skill.alphashop.cn/获取，安全可靠的企业级别SKILL HUB

## ✨ 核心特性

- 🔍 **市场趋势分析** - 自动搜索 Ozon 平台热门趋势
- 🏷️ **细分关键词提取** - AI 提取 5-8 个有潜力的细分市场关键词
- 📦 **1688 货源匹配** - 逐个关键词搜索 1688，找到最优商品
- 💰 **智能定价建议** - 3 倍定价 + SKU 明细展示

## 🚀 快速开始

### 配置密钥

在 OpenClaw config 中配置：

```json5
{
  skills: {
    entries: {
      "ozon-product-selection": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

密钥获取：访问 https://www.alphashop.cn/seller-center/apikey-management 申请。

## 🎯 使用方法

### 基础搜索

```bash
python3 scripts/search_products.py "关键词"
```

### 带筛选条件

```bash
python3 scripts/search_products.py "连衣裙" \
  --max-price 50 --max-moq 10 \
  --min-ship-rate-48h 80 --min-sales 100
```

### 使用示例

在 Claude Code 中直接说：

```
"帮我找 Ozon 上玩具品类的蓝海商品"
"Ozon 选品，品类是家居"
```

## 📁 项目结构

```
ozon-product-selection/
├── SKILL.md                          # SKILL 配置文件
├── README.md                         # 本文档
├── requirements.txt                  # Python 依赖
└── scripts/
    └── search_products.py            # 选品搜索脚本
```

## 📝 注意事项

1. **最多 3 个商品** - 累计找到 3 个有效商品后自动停止搜索
2. **关键词为中文** - 用于 1688 搜索，必须是中文关键词
3. **筛选条件** - 仅在用户明确要求时才添加
4. **后续铺货** - 选品后可使用 `1688-Product-to-Ozon` skill 铺货到 Ozon
5. **AlphaShop 欠费** - 如返回欠费错误，需前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分

---

**最后更新**: 2026-03-19
