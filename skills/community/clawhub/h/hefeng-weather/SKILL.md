# 和风天气查询技能

> 🤖 支持平台：飞书 / 微信（文字）
> 
> 查询实时天气、逐小时预报、每日预报、分钟级降水等

---

## ⚠️ 首次使用必读

**使用前必须配置和风天气 API Key**，否则无法运行！

配置方式：
1. 获取 Key：https://www.minimaxi.com/
2. 设置环境变量：`export HEFENG_WEATHER_API_KEY="your-key"`
   或创建配置文件：`cp config.example.txt config.txt` 并填入 Key
3. 验证：`python3 scripts/weather_query.py "北京" --type now`

详见下方「首次使用配置」章节。

---

## 功能

当用户询问天气时，自动调用和风天气 API：
1. 解析用户需求（城市、时间范围）
2. 调用对应的和风天气 API
3. 格式化返回结果

## 触发方式

用户发送以下任一方式都会触发：
- `北京天气怎么样`
- `今天会下雨吗`
- `上海明天温度`
- `深圳空气质量`
- `广州逐小时预报`
- `天气查询 北京`

---

## 首次使用配置

### 1. 获取和风天气 API Key

1. 注册和风天气开放平台：https://id.qweather.com/
2. 在控制台创建项目，获取 API Key
3. 设置环境变量（推荐）：
   ```bash
   export HEFENG_WEATHER_API_KEY="your-api-key-here"
   ```

### 2. 配置文件方式（可选）

如果不想设置环境变量，可以创建配置文件：

```bash
cp config.example.txt config.txt
# 编辑 config.txt，填入你的 API Key
```

### 3. 验证

```bash
python3 scripts/weather_query.py "北京" --type now
```

---

## 使用方式

### 命令行参数

```bash
# 实时天气
python3 scripts/weather_query.py "北京" --type now

# 逐小时预报（24小时）
python3 scripts/weather_query.py "北京" --type hourly

# 每日预报（3天）
python3 scripts/weather_query.py "北京" --type daily

# 分钟级降水（未来2小时）
python3 scripts/weather_query.py "北京" --type minutely
```

### 返回格式

输出 JSON 格式，便于后续处理。

---

## 技术细节

### API 端点

| 类型 | 端点 | 说明 |
|------|------|------|
| 实时天气 | `/v7/weather/now` | 温度/风力/湿度等 |
| 逐小时 | `/v7/weather/24h` | 未来24小时 |
| 每日预报 | `/v7/weather/7d` | 未来3-7天 |
| 分钟降水 | `/v7/minutely/15m` | 未来2小时 |

### 依赖
- Python 3.8+
- `requests` 库：`pip install requests`

---

## 文件结构

```
hefeng_weather/
├── SKILL.md              # 本文件
├── config.example.txt    # 配置示例
├── scripts/             # 脚本目录
│   └── weather_query.py # 主脚本
└── references/         # 参考文档
    └── README.md        # 详细说明
```

---

## 常见问题

### Q: 提示"网络请求失败"
A: 检查 API Key 是否正确配置，网络是否畅通

### Q: 提示"API返回错误"
A: 检查 API Key 是否有对应接口权限

### Q: 提示"城市不存在"
A: 检查城市名称是否正确，可使用城市 ID（如北京=101010100）

---

## 城市 ID

常用城市 ID：
| 城市 | ID |
|------|-----|
| 北京 | 101010100 |
| 上海 | 101020100 |
| 广州 | 101280101 |
| 深圳 | 101280601 |
| 成都 | 101270101 |
| 武汉 | 101200101 |
| 杭州 | 101210101 |

---

## 贡献

欢迎提交 Issue 和 PR！
