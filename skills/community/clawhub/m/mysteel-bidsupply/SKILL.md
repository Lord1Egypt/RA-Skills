---
name: Mysteel_BidSupply
description: 支持钢材供需现货信息查询与招投标数据检索；当用户需要找采购方、找供应方、查询招投标信息或发现项目机会时使用
dependency:
  python:
    - requests
---

# 钢材招投标与供需查询

## 使用方法

### 招投标查询
```bash
python scripts/bidding_api.py --query "查询文本"
```

参数：
- `--query`: 查询文本（必填）
- `--start_time`: 开始时间戳（毫秒），默认近3个自然年
- `--end_time`: 结束时间戳（毫秒），默认当前时间
- `--top_k`: 召回条数，默认10

### 供需查询
```bash
python scripts/supply_demand_api.py --type 1
```

参数：
- `--type`: 信息类型，1=供应信息（找货源），2=求购信息（找买家）（必填）
- `--breed_name`: 品种名称
- `--spec`: 规格名称
- `--material`: 材质名称
- `--steel_mill`: 钢厂名称
- `--warehouse_area`: 地区名称
- `--warehouse_name`: 仓库名称

### API Key 配置
首次使用需要配置 API Key：
```bash
python scripts/bidding_api.py --save_api_key "your_api_key"
```

API Key 保存在 `references/api_key.md` 文件中。

## 意图识别

参考 `references/intent-guide.md` 判断用户查询类型：
- **招投标**：关键词包含"招标、投标、项目、公告、开标、截标、工程、采购项目、中标"
- **供需**：关键词包含"供应、求购、现货、资源、库存、采购、销售、买、卖、螺纹钢、钢材"

## 供需角色判断

- **买家（type=1）**：找货源、采购、买、需要、要、寻找
- **卖家（type=2）**：卖、出售、销售、有货、求购、找买家

## 注意事项

- 招投标查询仅支持近3个自然年的数据
- 调用脚本前必须先配置 API Key
- 不向用户展示接口调用细节和原始 JSON 数据
