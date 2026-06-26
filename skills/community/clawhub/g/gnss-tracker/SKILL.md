---
name: gnss-tracker
description: 识别智能设备二维码并查询定位位置。触发场景：用户发送包含设备二维码的图片、查询设备定位、识别设备二维码获取位置、根据IMEI查询设备最后定位。
---

# GNSS 设备定位查询 Skill

## 功能
识别智能设备二维码，提取IMEI号，查询设备最后一次定位位置。

## 触发条件
当用户发送包含设备二维码的图片，或者明确要求查询设备定位时触发。

## 使用流程

1. **识别二维码**：如果用户提供了图片，使用 zbarimg 识别二维码内容
2. **提取IMEI**：从二维码的 dev_info.imei 字段提取设备IMEI号
3. **查询定位**：调用 API 获取定位信息
4. **返回结果**：格式化返回定位地址和时间，没有数据则提示查不到记录

## 核心脚本
使用 `scripts/query_gnss.py` 完成查询：

```python
import sys
import json
import requests

def query_location(imei):
    url = f"https://search.iwown.com/hpmservice/ai/vendor/gnss/latest?deviceid={imei}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ReturnCode") != 0:
            return None, None, None
            
        record_time = data["Data"]["record_time"]
        address = data["Data"]["address"]
        return record_time, address, data["Data"]
    except Exception as e:
        print(f"查询失败: {e}", file=sys.stderr)
        return None, None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python query_gnss.py <imei>")
        sys.exit(1)
    
    imei = sys.argv[1]
    record_time, address, raw_data = query_location(imei)
    
    if address:
        print(json.dumps({
            "status": "success",
            "record_time": record_time,
            "address": address,
            "raw": raw_data
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "status": "error",
            "message": "查不到定位记录"
        }, ensure_ascii=False))
```

## 结果返回格式
定位成功：
设备最后定位位置：广东省深圳市南山区南山街道自贸大街香江金融中心
定位时间：2026-03-11 14:52:12

定位失败：
查不到该设备的定位记录
