---
name: weather-cn
version: 1.0.0
description: >
  中国天气查询技能，使用墨迹天气和 MSN 天气作为数据源，支持国内城市天气查询。
  当用户询问天气、温度、预报时使用此技能。
  覆盖内置 weather 技能，强制使用国内数据源，避免 wttr.in 等国外 API 的访问问题。
metadata:
  author: 尹德斌(Paudy)
  category: utility
  tags: [weather, china, 天气, 墨迹, msn, browser]
---

# 天气查询 — 中国数据源版

⚠️ **本技能覆盖内置 weather 技能，强制使用国内数据源，解决 wttr.in/Open-Meteo 在国内的访问问题。**

---

## 🎯 什么时候使用

**立即触发：**
- 用户问"今天天气怎么样"、"明天会下雨吗"
- 用户提到城市名 + "天气"、"温度"、"下雨"
- 用户问"需要带伞吗"、"适合出门吗"
- 用户需要多日天气预报

**不要触发：**
- 历史天气数据查询
- 气象学专业分析
- 国外城市天气（内置 weather 技能可以处理）

---

## ⛔ 禁止事项

- ❌ 禁止使用 `wttr.in`、`Open-Meteo` 或任何国外天气 API
- ❌ 禁止用 `curl` 直接获取天气数据
- ❌ 禁止凭记忆或猜测生成天气数据
- ❌ 禁止回复未经验证的天气信息

---

## ✅ 数据源

### 1. 墨迹天气（首选）

| 项目 | 内容 |
|------|------|
| 首页 | `https://tianqi.moji.com/` |
| 城市页 | `https://tianqi.moji.com/weather/省份/城市/区县` |

**URL 规则：**
- 省份、城市、区县名称使用**拼音小写**
- 用 `/` 分隔，最多三级：`/weather/province/city/district`
- 如果区县级查不到，降级到城市级

**常用城市 URL 示例：**

| 城市 | URL |
|------|-----|
| 佛山顺德 | `https://tianqi.moji.com/weather/guangdong/foshan/shunde` |
| 上海闵行 | `https://tianqi.moji.com/weather/shanghai/shanghai/minhang` |
| 北京 | `https://tianqi.moji.com/weather/beijing/beijing` |
| 广州 | `https://tianqi.moji.com/weather/guangdong/guangzhou` |
| 深圳 | `https://tianqi.moji.com/weather/guangdong/shenzhen` |
| 杭州 | `https://tianqi.moji.com/weather/zhejiang/hangzhou` |
| 成都 | `https://tianqi.moji.com/weather/sichuan/chengdu` |
| 武汉 | `https://tianqi.moji.com/weather/hubei/wuhan` |
| 南京 | `https://tianqi.moji.com/weather/jiangsu/nanjing` |
| 重庆 | `https://tianqi.moji.com/weather/chongqing/chongqing` |

### 2. MSN 天气（备选/交叉验证）

| 项目 | 内容 |
|------|------|
| 地址 | `https://www.msn.cn/zh-cn/weather/` |
| 用途 | 墨迹天气数据异常时的备选源 |
| 特点 | 需要浏览器渲染，数据来自 AccuWeather |

---

## 🔄 操作流程

### 标准查询流程

```
用户问天气 → 构造墨迹天气 URL → browser 打开 → 截图/提取数据 → 整理回复
```

**Step 1: 构造 URL**
根据用户提到的城市，构造墨迹天气 URL：
- 将中文城市名转换为拼音
- 格式：`https://tianqi.moji.com/weather/{province}/{city}/{district}`
- 不确定区县时，只用省市两级

**Step 2: 浏览器获取数据**
```
browser → open → {URL}
browser → snapshot → 提取天气信息
```

如果需要可视化截图：
```
browser → screenshot → 发送给户
```

**Step 3: 整理回复**
提取以下关键信息：
- 当前温度、天气状况（晴/阴/雨/雪）
- 今日最高/最低温度
- 空气质量指数（AQI）
- 风力风向
- 未来 3-5 天预报（如有）

**Step 4: 回复用户**
格式参考：
```
📍 {城市} 天气
🌡️ 当前: {温度}°C {天气状况}
📊 今日: {最低}°C ~ {最高}°C
💨 风力: {风力描述}
🌫️ AQI: {空气质量指数} {等级}

📅 未来几天:
明天: {温度范围} {天气}
后天: {温度范围} {天气}
```

### 降级流程

如果墨迹天气无法访问或数据异常：
1. 打开 MSN 天气 `https://www.msn.cn/zh-cn/weather/`
2. 搜索目标城市
3. 获取数据并回复
4. 备注"数据来源：MSN 天气"

---

## 💡 使用技巧

**拼音转换规则：**
- 常用城市拼音可直接记忆（如 beijing, shanghai, guangzhou）
- 多音字注意：重庆 → `chongqing`（不是 zhongqing）
- 自治区：内蒙古 → `neimenggu`，新疆 → `xinjiang`

**常见城市拼音速查：**

| 中文 | 拼音 | 省级拼音 |
|------|------|---------|
| 北京 | beijing | beijing |
| 上海 | shanghai | shanghai |
| 广州 | guangzhou | guangdong |
| 深圳 | shenzhen | guangdong |
| 成都 | chengdu | sichuan |
| 杭州 | hangzhou | zhejiang |
| 南京 | nanjing | jiangsu |
| 武汉 | wuhan | hubei |
| 重庆 | chongqing | chongqing |
| 西安 | xian | shaanxi |
| 长沙 | changsha | hunan |
| 青岛 | qingdao | shandong |
| 大连 | dalian | liaoning |
| 厦门 | xiamen | fujian |
| 苏州 | suzhou | jiangsu |

---

## 📝 示例对话

**用户：** 北京今天天气怎么样？

**操作：**
1. 打开 `https://tianqi.moji.com/weather/beijing/beijing`
2. 用 browser snapshot 提取数据
3. 整理回复

**回复：**
```
📍 北京 天气
🌡️ 当前: 22°C 晴
📊 今日: 15°C ~ 25°C
💨 风力: 南风 3级
🌫️ AQI: 65 良

空气质量不错，适合户外活动！
```

---

**用户：** 上海明天会下雨吗？

**操作：**
1. 打开 `https://tianqi.moji.com/weather/shanghai/shanghai`
2. 查看未来几天预报
3. 回复降水概率

---

**用户：** 佛山顺德区现在多少度？

**操作：**
1. 打开 `https://tianqi.moji.com/weather/guangdong/foshan/shunde`
2. 提取当前温度
3. 回复

---

## ⚠️ 注意事项

1. **数据来源声明：** 回复末尾注明"数据来源：墨迹天气"或"数据来源：MSN 天气"
2. **时效性：** 天气数据会变化，回复时注明查询时间
3. **降级策略：** 墨迹天气 404 时，先尝试去掉区县再查，最后用 MSN
4. **截图分享：** 用户说"截图给我看"时，用 browser screenshot 发送
5. **多城市查询：** 用户同时问多个城市时，依次查询后汇总回复

---

_本技能专为解决国内网络环境下天气查询问题而设计，适用于所有需要查询中国城市天气的场景。_
