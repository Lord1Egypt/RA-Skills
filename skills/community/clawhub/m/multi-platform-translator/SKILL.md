---
name: multi-platform-translator
description: 支持讯飞翻译、豆包、腾讯元宝、DeepL、金山词霸5个平台的中英互译功能，自动识别源语言，可指定目标语言和翻译引擎
version: 1.0.0
author: Paudy
parameters:
  - name: text
    description: 需要翻译的文本内容（支持中文/英文，单条最多5000字）
    required: true
  - name: target_lang
    description: 目标语言，可选值：zh/中文、en/英文，默认自动识别并互译
    required: false
    default: auto
  - name: engine
    description: 翻译引擎，可选值：
      - xfyun/讯飞（默认，无需登录，速度快）
      - doubao/豆包（支持上下文，更准确，需提前登录）
      - yuanbao/元宝（腾讯出品，专业术语准确，需提前登录）
      - deepl/DeepL（专业翻译，语义准确，需境外网络）
      - iciba/金山词霸（适合单词/短句翻译）
    required: false
    default: xfyun
triggers:
  - 翻译
  - 英译中
  - 中译英
  - 翻译成英文
  - 翻译成中文
---

## 使用示例
```
# 基础使用（默认讯飞翻译，自动识别语言）
翻译 "智能制造是未来工业发展的核心方向"

# 指定目标语言
英译中 "Artificial intelligence will revolutionize manufacturing industry"
翻译 "你好世界" target_lang=en

# 指定翻译引擎
翻译 "机器人自动化生产线的核心技术参数" engine=deepl
翻译 "合同条款内容" engine=doubao
```

## 执行逻辑
### 1. 引擎适配逻辑
根据用户选择的引擎，自动执行对应操作：

#### ✅ 讯飞翻译（默认，无需登录）
```
> 打开网页：https://fanyi.xfyun.cn/console/trans/text
> 等待加载完成，定位输入框
> 清空内容，输入待翻译文本 {{text}}
{% if target_lang != "auto" %}
> 选择目标语言：{{target_lang == "zh" ? "中文" : "英文"}}
{% endif %}
> 点击「翻译」按钮
> 提取右侧翻译结果区域内容返回
```

#### ✅ DeepL翻译（专业级）
```
> 打开网页：https://www.deepl.com/zh/translator
> 等待加载完成，清空源文本输入框
> 输入待翻译文本 {{text}}
{% if target_lang != "auto" %}
> 选择目标语言：{{target_lang == "zh" ? "中文（简体）" : "英语（美国）"}}
{% endif %}
> 等待翻译完成，提取目标文本结果返回
```

#### ✅ 金山词霸（单词/短句翻译）
```
> 打开网页：https://www.iciba.com/
> 在搜索框输入待翻译文本 {{text}} 并回车
> 提取翻译结果区域的核心释义返回
```

#### ✅ 豆包翻译（AI增强，需提前登录）
```
> 打开网页：https://www.doubao.com/chat
> 在输入框输入指令：
  "请将以下内容翻译成{{target_lang == 'zh' ? '中文' : '英文'}}，仅返回翻译结果，不需要额外解释：\n{{text}}"
> 发送消息等待回复，提取AI返回的翻译结果
```

#### ✅ 腾讯元宝翻译（专业术语准确，需提前登录）
```
> 打开网页：https://yuanbao.tencent.com/chat/naQivTmsDa
> 在输入框输入指令：
  "翻译以下内容为{{target_lang == 'zh' ? '中文' : '英文'}}，只返回结果：\n{{text}}"
> 发送消息等待回复，提取AI返回的翻译结果
```

### 2. 异常处理逻辑
> 如果当前引擎翻译失败/无响应，自动切换下一个引擎重试，优先级：讯飞→DeepL→金山词霸→豆包→元宝
> 所有引擎均失败时，提示用户检查网络连接/浏览器登录状态
> 翻译内容过长时，自动分段翻译后合并结果

## 注意事项
1. 📢 豆包、腾讯元宝需要提前在浏览器中登录账号，否则无法使用
2. 🌐 DeepL访问需要境外网络环境支持，否则请选择其他引擎
3. 🔒 所有翻译内容仅在本地浏览器中传输，不会上传到第三方服务器
4. 💡 专业文档、法律条文等重要内容建议使用DeepL/豆包引擎，翻译准确性更高
