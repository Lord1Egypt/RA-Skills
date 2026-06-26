---
name: juhe-speech-generate
description: AI语音合成（文本转语音）。将指定文本合成为语音文件并返回下载链接。使用场景：用户说"把这段文字转成语音"、"帮我生成一段语音"、"用甜美的声音朗读这段话"、"把这个文案合成音频"、"用英文女声读一下这句话"等。通过聚合数据（juhe.cn）API实时合成，支持多种拟人音色、多语言及方言，可选下载音频文件。
homepage: https://www.juhe.cn/docs/api/id/830
metadata: {"openclaw":{"emoji":"🔊","requires":{"bins":["python3"],"env":["JUHE_SPEECH_KEY"]},"primaryEnv":"JUHE_SPEECH_KEY"}}
---

# AI语音合成（文本转语音）

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP查询等 200+ 免费/低价 API。

将文本内容合成为语音文件：**支持多种拟人音色、多语言及方言，自适应语气，流畅处理复杂文本**。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [AI语音合成TTS API](https://www.juhe.cn/docs/api/id/830) 页面，点击「申请使用」
3. 审核通过后在「我的API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_SPEECH_KEY=你的AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_SPEECH_KEY=你的AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/speech_generate.py --key 你的AppKey "今天天气真好！"
```

---

## 使用方法

### 基本合成

```bash
python scripts/speech_generate.py "今天天气真好，我想去公园散步。"
```

输出示例：

```
🔊 语音合成成功！

音色: Cherry（随机）
语种: Auto
文本: 今天天气真好，我想去公园散步。

音频链接（24小时内有效）:
https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/...wav
```

### 指定音色

```bash
# 用甜美港妹音色
python scripts/speech_generate.py --voice Kiki "你好，欢迎使用聚合数据语音合成服务！"

# 用御姐音色
python scripts/speech_generate.py --voice Katerina "本次会议正式开始，请各位嘉宾就坐。"

# 用幽默台湾哥仔音色
python scripts/speech_generate.py --voice Roy "欸，今天吃什么好呢？"
```

### 指定语种

```bash
# 英文
python scripts/speech_generate.py --voice Jennifer --language English "Hello, welcome to Juhe Data!"

# 日文
python scripts/speech_generate.py --language Japanese "こんにちは、今日もいい天気ですね。"

# 自动识别（默认）
python scripts/speech_generate.py --language Auto "今天 is a good day!"
```

### 下载音频文件

```bash
# 合成并自动下载到当前目录
python scripts/speech_generate.py --download "这段话将被保存为音频文件。"

# 合成并保存到指定路径
python scripts/speech_generate.py --output /tmp/my_audio.wav "指定保存位置。"
```

### 从文件读取文本

```bash
# 从文本文件读取内容（不超过500字符）
python scripts/speech_generate.py --file my_text.txt --voice Cherry
```

### 列出所有可用音色

```bash
python scripts/speech_generate.py --list-voices
```

---

## 可用音色列表

| 音色名     | 风格描述                         | 适用场景         |
|------------|----------------------------------|------------------|
| Cherry     | 阳光积极、亲切自然小姐姐         | 客服、播报、通用  |
| Ethan      | 标准普通话，阳光温暖，北方口音   | 新闻播报、教育   |
| Nofish     | 不会翘舌音的设计师               | 创意内容、趣味   |
| Jennifer   | 品牌级电影质感美语女声           | 英文内容、品牌   |
| Ryan       | 节奏拉满，戏感炸裂               | 短视频、广告     |
| Katerina   | 御姐音色，韵律回味十足           | 高端品牌、旁白   |
| Elias      | 严谨学术，知识叙事               | 教育、科普       |
| Jada       | 风风火火的沪上阿姐               | 上海方言、趣味   |
| Dylan      | 北京胡同里长大的少年             | 北京话、青春感   |
| Sunny      | 甜到你心里的川妹子               | 四川方言、萌系   |
| Li         | 耐心的瑜伽老师                   | 冥想、养生、舒缓 |
| Marcus     | 面宽话短，心实声沉，老陕的味道   | 陕西味、质朴感   |
| Roy        | 诙谐直爽、市井活泼的台湾哥仔     | 台湾腔、娱乐     |
| Peter      | 天津相声，专业捧哏               | 天津话、搞笑     |
| Rocky      | 幽默风趣的阿强，在线陪聊         | 陪伴、娱乐       |
| Kiki       | 甜美的港妹闺蜜                   | 粤语、甜系       |
| Eric       | 跳脱市井的四川成都男子           | 成都话、潮流感   |

---

## 支持语种

| 语种代码    | 说明        |
|-------------|-------------|
| Auto        | 自动识别（默认） |
| Chinese     | 中文        |
| English     | 英文        |
| German      | 德文        |
| Italian     | 意大利文    |
| Portuguese  | 葡萄牙文    |
| Spanish     | 西班牙文    |
| Japanese    | 日文        |
| Korean      | 韩文        |
| French      | 法文        |
| Russian     | 俄文        |

---

## AI 使用指南

当用户要求合成语音时，按以下步骤操作：

1. **提取合成信息** — 从用户消息中识别文本内容、偏好音色和语种
2. **检查文本长度** — 文本不超过 500 字符，超出需提示用户截断
3. **调用脚本** — 根据用户需求决定是否加 `--voice`、`--language`、`--download` 参数
4. **展示结果** — 输出音频链接；若用户需要下载文件，使用 `--download` 或 `--output` 参数

### 参数说明

| 参数           | 必填 | 说明                                  | 示例                  |
|----------------|------|---------------------------------------|-----------------------|
| `text`         | 是   | 要合成的文本，最多500字符             | "你好世界"            |
| `--voice`      | 否   | 音色名称，不指定则随机                | Cherry、Kiki          |
| `--language`   | 否   | 语种，默认 Auto                       | Chinese、English      |
| `--download`   | 否   | 合成后自动下载到当前目录              | —                     |
| `--output`     | 否   | 指定下载保存路径                      | /tmp/output.wav       |
| `--file`       | 否   | 从文件读取文本内容                    | my_text.txt           |
| `--list-voices`| 否   | 列出所有可用音色                      | —                     |
| `--key`        | 否   | 临时指定 API Key                      | abc123                |

### 返回字段说明

| 字段         | 含义                              | 示例                              |
|--------------|-----------------------------------|-----------------------------------|
| `error_code` | 状态码，0 为成功                  | 0                                 |
| `reason`     | 状态提示                          | 成功                              |
| `orderid`    | 订单号                            | JH83025121914072892mDt            |
| `audio_url`  | 音频文件下载链接（24小时有效）    | https://dashscope-result-bj...wav |

### 错误处理

| 情况                    | 处理方式                                                                     |
|-------------------------|------------------------------------------------------------------------------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/830) 重新申请 |
| `error_code` 10012      | 当日免费次数已用尽，建议升级套餐                                             |
| 文本超过500字符         | 提示用户截断文本后重试                                                       |
| 音频链接过期            | 链接有效期24小时，提示用户重新生成                                           |
| 请求超时                | 接口生成耗时可能较长，超时设置建议60s以上，重试一次后仍失败则提示网络问题   |

---

## 脚本位置

`scripts/speech_generate.py` — 封装了 API 调用、参数校验、音频下载和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **AI 能力**：语音合成、图像生成、图像理解、文本翻译
- **交通出行**：火车时刻查询、航班动态、快递追踪
- **生活服务**：天气预报、万年历、节假日查询
- **身份核验**：手机号归属地、身份证实名验证
- **金融数据**：汇率、股票、黄金价格

注册即可免费使用，适合个人开发者和企业接入。
