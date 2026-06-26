# 和风天气查询技能 for OpenClaw

查询实时天气、逐小时预报、每日预报、分钟级降水

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key

**方式一：环境变量（推荐）**
```bash
export HEFENG_WEATHER_API_KEY="your-api-key-here"
```

**方式二：配置文件**
```bash
cp config.example.txt config.txt
# 编辑 config.txt，填入你的 API Key
```

### 3. 测试

```bash
# 实时天气
python3 scripts/weather_query.py "北京" --type now

# 逐小时预报
python3 scripts/weather_query.py "北京" --type hourly

# 每日预报
python3 scripts/weather_query.py "北京" --type daily

# 分钟级降水
python3 scripts/weather_query.py "北京" --type minutely
```

### 4. 集成到 OpenClaw

在 OpenClaw 的 `SOUL.md` 或 `AGENTS.md` 中添加触发指令。

## 目录结构

```
hefeng_weather/
├── SKILL.md              # 技能说明（OpenClaw 读取）
├── config.example.txt    # 配置示例
├── scripts/             # 脚本目录
│   └── weather_query.py # 主脚本
└── references/          # 参考文档
    └── README.md        # 本文件
```

## 获取和风天气 API Key

1. 访问 https://id.qweather.com/
2. 注册/登录账号
3. 进入控制台 → 创建项目
4. 获取 API Key

注意：基础服务每月前5万次免费，采用后付费模式。

## 常用城市 ID

| 城市 | ID |
|------|-----|
| 北京 | 101010100 |
| 上海 | 101020100 |
| 广州 | 101280101 |
| 深圳 | 101280601 |
| 成都 | 101270101 |
| 武汉 | 101200101 |
| 杭州 | 101210101 |

## 常见问题

**Q: 提示"网络请求失败"**
- 检查 API Key 是否正确
- 检查网络连接

**Q: 提示"API返回错误"**
- 检查 API Key 是否有对应接口权限

**Q: 提示"城市不存在"**
- 检查城市名称是否正确
- 可使用城市 ID 直接查询

## License

MIT
