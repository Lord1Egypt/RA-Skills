---
name: pollen-monitor
version: 1.0.0
description: 中国天气网花粉浓度监测技能。查询中国大陆城市花粉浓度等级和防护建议。
homepage: https://m.weather.com.cn/huafen/
metadata: {"clawdbot":{"emoji":"🌸","requires":{"bins":["curl","python3"]}}}
---

# 花粉监测 (Pollen Monitor) v1.0.0

调用中国天气网 & 全国多家医院联合发布的花粉监测数据，无需 API 密钥。

> ⚠️ **支持范围：仅支持中国大陆城市**

## 快速使用

### 查询北京花粉浓度
```bash
python3 ~/.openclaw/workspace/skills/pollen-monitor/pollen.py
```

### 查询其他城市
```bash
python3 ~/.openclaw/workspace/skills/pollen-monitor/pollen.py beijing 北京
python3 ~/.openclaw/workspace/skills/pollen-monitor/pollen.py shanghai 上海
```

## 支持的城市（53 个）

| 城市 | 拼音 | 城市 | 拼音 | 城市 | 拼音 |
|------|------|------|------|------|------|
| 北京 | beijing | 上海 | shanghai | 天津 | tianjin |
| 重庆 | chongqing | 广州 | guangzhou | 深圳 | shenzhen |
| 成都 | chengdu | 杭州 | hangzhou | 南京 | nanjing |
| 武汉 | wuhan | 西安 | xian | 郑州 | zhengzhou |
| 济南 | jinan | 沈阳 | shenyang | 长春 | changchun |
| 哈尔滨 | haerbin | 石家庄 | shijiazhuang | 太原 | taiyuan |
| 兰州 | lanzhou | 西宁 | xining | 银川 | yinchuan |
| 乌鲁木齐 | wulumuqi | 呼和浩特 | huhehaote | 包头 | baotou |
| 鄂尔多斯 | eerduosi | 赤峰 | chifeng | 大连 | dalian |
| 烟台 | yantai | 淄博 | zibo | 聊城 | liaocheng |
| 承德 | chengde | 沧州 | cangzhou | 保定 | baoding |
| 泊头 | botou | 福州 | fuzhou | 合肥 | hefei |
| 南昌 | nanchang | 长沙 | changsha | 南宁 | nanning |
| 海口 | haikou | 昆明 | kunming | 贵阳 | guiyang |
| 拉萨 | lasa | 西宁 | xining | 南充 | nanchong |
| 扬州 | yangzhou | 无锡 | wuxi | 乌海 | wuhai |
| 乌兰浩特 | wulanhaote | 延安 | yanan | 咸阳 | xianyang |
| 榆林 | yulin | 六盘水 | liupanshui |

> 💡 查询链接：https://m.weather.com.cn/huafen/index.html?id=101010100

## API 接口

```
GET https://graph.weatherdt.com/ty/pollen/v2/hfindex.html
```

### 参数
| 参数 | 说明 | 示例 |
|------|------|------|
| eletype | 固定为 1（花粉） | `1` |
| city | 城市拼音（见上表） | `beijing` |
| start | 开始日期（7 天前） | `2026-03-16` |
| end | 结束日期（今天） | `2026-03-23` |
| predictFlag | 是否包含预报 | `true` |

## 返回数据解析

### 花粉等级 (seasonLevel)
| levelCode | level | 数值范围 | 说明 |
|-----------|-------|----------|------|
| -1 | 未检测到 | - | 数据异常或无数据 |
| 0 | 未检测到花粉 | 0 | 暂无花粉 |
| 1 | 很低 | 1-70 | 不易引发过敏反应 |
| 2 | 低 | 71-150 | 易引发轻度过敏，适当防护对症用药 |
| 3 | 中 | 151-290 | 易引发过敏，加强防护，对症用药 |
| 4 | 高 | 291-520 | 易引发过敏，加强防护，规范用药 |
| 5 | 很高 | ≥521 | 极易引发过敏，减少外出，持续规范用药 |

### 数据结构
```json
{
  "seasonLevel": [...],  // 等级说明
  "dataList": [          // 每日数据
    {
      "levelCode": "5",      // 等级代码
      "level": "很高",        // 等级名称
      "addTime": "2026-03-23", // 日期
      "week": "星期一",        // 星期
      "levelMsg": "极易引发过敏，减少外出，持续规范用药" // 防护建议
    }
  ],
  "seasonLevelName": "春季"  // 花粉季名称
}
```

## 完整查询脚本

### Python 版本（推荐）

```bash
# 查询北京（默认）
python3 pollen.py

# 查询指定城市
python3 pollen.py beijing 北京
python3 pollen.py shanghai 上海
```

### Bash 版本（需要 jq）

```bash
#!/bin/bash
CITY="${1:-beijing}"
START=$(date -d '-7 days' +%Y-%m-%d)
END=$(date +%Y-%m-%d)

RESPONSE=$(curl -s "https://graph.weatherdt.com/ty/pollen/v2/hfindex.html?eletype=1&city=${CITY}&start=${START}&end=${END}&predictFlag=true")

TODAY=$(echo "$RESPONSE" | jq -r '.dataList | sort_by(.addTime) | .[-2]')
TOMORROW=$(echo "$RESPONSE" | jq -r '.dataList | sort_by(.addTime) | .[-1]')

echo "🌸 ${CITY} 花粉浓度报告"
echo "今天：$(echo "$TODAY" | jq -r '.level') - $(echo "$TODAY" | jq -r '.levelMsg')"
echo "明天：$(echo "$TOMORROW" | jq -r '.level') - $(echo "$TOMORROW" | jq -r '.levelMsg')"
```

## 注意事项

1. **支持范围**：仅支持中国大陆城市，不支持港澳台及海外城市
2. **数据更新**：每日 08:00 发布实况数据
3. **数据来源**：中国天气网 & 全国多家医院联合监测
4. **预报时效**：包含未来 1-2 天预报
5. **春季花粉季**：3 月中旬至 5 月（树木花粉为主）
6. **秋季花粉季**：8 月至 9 月（草本花粉为主）
7. **城市限制**：目前 API 仅支持 53 个中国大陆城市

## 已知问题

1. 部分城市可能无花粉监测数据（返回"暂无"或"很低"）
2. 预报数据可能存在 1-2 天延迟
3. 城市拼音需严格匹配（如 `xian` 不是 `xi'an`）

## 相关链接

- 中国天气网花粉频道：https://m.weather.com.cn/huafen/
- 花粉监测预报小程序（微信）
- 城市选择页面：https://m.weather.com.cn/huafen/cityChoose.html
