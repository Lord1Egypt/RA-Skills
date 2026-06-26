# 刘雨鑫-美食探店 (Local Guide)

> 本地通推荐技能 - 利用互联网全域搜索，绕过商业评价平台，挖掘真正受当地人认可的地道去处。

## ✨ 功能特点

- 🔍 **深度搜索**：多轮搜索官方推荐、本地口碑，避开商业平台
- 🍜 **多类型支持**：美食、小吃、甜品、酒店、景点、温泉、停车场等
- 📋 **完整信息**：位置、电话、导航地址、营业时间、人均消费
- ✅ **真实可靠**：推荐理由 + 避雷参考，信息透明
- 🎨 **飞书卡片**：支持飞书渠道卡片消息输出

## 📦 安装

将 `刘雨鑫-美食探店.skill` 文件放入 OpenClaw skills 目录：

```bash
# Linux/Mac
cp 刘雨鑫-美食探店.skill ~/.openclaw/skills/

# 或解压后放置
unzip 刘雨鑫-美食探店.skill -d ~/.openclaw/skills/local-guide
```

## ⚙️ 配置

使用前需配置以下环境变量：

### EXA 搜索引擎（必需）

```bash
# 1. 注册获取 API Key：https://exa.ai
# 2. 配置环境变量

# Linux/Mac
export EXA_API_KEY=your-api-key-here

# Windows
set EXA_API_KEY=your-api-key-here

# 添加到 ~/.bashrc 或 ~/.zshrc 永久保存
echo 'export EXA_API_KEY=your-api-key-here' >> ~/.bashrc
```

### 飞书卡片（可选）

如需飞书卡片输出功能：

```bash
export FEISHU_APP_ID=your-feishu-app-id
export FEISHU_APP_SECRET=your-feishu-app-secret
```

## 🚀 使用示例

```
# 美食推荐
本地通 美食 南海桂城
本地通推荐 小吃 佛山市南海区桂城
本地通 糖水 广州天河

# 景点推荐
本地通 好玩 佛山南海
本地通推荐 景点 广州市番禺区
本地通 小众景点 深圳

# 停车场推荐
本地通 停车 佛山南海千灯湖公园
本地通推荐 停车场 广州天河城
本地通 停车位 广东省中医院

# 温泉推荐
本地通 温泉 广州从化
本地通推荐 泡温泉 佛山三水

# 酒店推荐
本地通 酒店 佛山南海
本地通推荐 性价比酒店 广州越秀
```

## 📝 触发词

| 格式 | 示例 |
|------|------|
| 本地通推荐 [类型] [地名] | 本地通推荐 美食 广州天河 |
| 本地通 [类型] [地名] | 本地通 小吃 佛山南海 |
| [地名] 本地通 [类型] | 南海桂城 本地通 温泉 |

**支持的类型**：
- 美食 / 小吃 / 甜品 / 糖水
- 酒店 / 住宿 / 民宿
- 好玩 / 景点 / 玩乐
- 温泉 / 泡温泉
- 购物 / 商场
- 啡 / 咖啡馆
- 酒吧 / 夜生活
- 停车 / 停车场 / 停车位

## ⚠️ 注意事项

1. **数据来源**：优先官方推荐（文旅局、旅游局），排除大众点评、美团、携程等商业平台
2. **信息时效**：营业状态可能变化，建议前往前电话确认
3. **真实缺点**：每个推荐都包含避雷参考，增加可信度
4. **数量要求**：每个分类至少推荐 10 个地方

## 📁 文件结构

```
local-guide/
├── SKILL.md              # 技能说明文档
├── README.md             # 本文件
└── scripts/
    ├── search_module.py       # 搜索模块（EXA）
    ├── feishu_card.py         # 飞书卡片模块
    └── send_feishu_card.py    # 飞书卡片发送脚本
```

## 🔗 相关链接

- [OpenClaw 官网](https://openclaw.ai)
- [ClawHub 技能市场](https://clawhub.ai)
- [EXA 搜索引擎](https://exa.ai)

## 📄 License

MIT License

---

**作者**：刘雨鑫  
**技能名称**：美食探店 - 本地通推荐  
**版本**：1.0.0