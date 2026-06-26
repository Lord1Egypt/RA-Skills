---
name: obtain-takeout-coupon
description: 获取外卖优惠券（隐藏券、大额券）的技能，支持平台： 美团（Meituan），淘宝闪购（饿了么，taobao）。A skill for obtaining takeout coupons (hidden coupons, large-value coupons), supported platforms: Meituan, Taobao Flash Sale (Ele.me, Taobao)..
metadata:
  {
    "openclaw":
      {
        "emoji": "🎁",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {"id": "uv-brew", "kind": "brew", "formula": "uv", "bins": ["uv"], "label": "Install uv (brew)"},
            {"id": "uv-pip", "kind": "pip", "formula": "uv", "bins": ["uv"], "label": "Install uv (pip)"},
            {"id": "pip-aiohttp", "kind": "pip", "formula": "aiohttp", "label": "Install aiohttp (pip)"},
            {"id": "pip-argparse", "kind": "pip", "formula": "argparse", "label": "Install argparse (pip)"},
            {"id": "pip-PyYAML", "kind": "pip", "formula": "PyYAML", "label": "Install PyYAML (pip)"},
          ],
      },
  }
---

# 获取最新的外卖优惠券 Obtain Takeout Coupons
获取中国在线购物平台的外卖优惠券（大额券，隐藏券），统一使用 `/coupon/takeout` 接口获取。

```yaml
# 参数解释
source:
  1: 美团优惠券
  2: 淘宝闪购优惠券
  3: 饿了么优惠券
```

## 获取优惠券口令(字符串格式，不要更改接口返回的内容，否则会失效)  
```shell
uv run scripts/route.py search --source={source}
```

**注意**: 所有平台现在都使用统一的 API 接口 `/coupon/takeout`，不再区分平台端点。

## 隐私提示 Privacy Tips
本技能提供的脚本不会读写本地文件，可放心使用 The scripts provided by this skill do not read or write local files, so you can use them with confidence.