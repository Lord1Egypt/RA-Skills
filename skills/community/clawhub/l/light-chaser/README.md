# Light Chaser · 使用前配置

使用本技能前，建议先配置 `config.env` 中的和风天气 API 信息，以获取精准的实时天气数据。

## 获取 Host 和 Key

1. 前往 [和风天气开发平台](https://dev.qweather.com/) 注册并登录
2. 创建应用，选择「Web API」
3. 在应用详情中获取：
   - **API Host**：自定义域名（如 `xxxxx.re.qweatherapi.com`）
   - **API Key**：鉴权密钥

## 填写配置

编辑同目录下的 `config.env`：

```
QWEATHER_HOST=你的API域名
QWEATHER_KEY=你的APIKey
```

## 未配置时的行为

若 `config.env` 中的值为空，技能会自动降级为通过网络搜索获取天气信息，精度较低，输出中会注明「数据来源：网络搜索，仅供参考」。
