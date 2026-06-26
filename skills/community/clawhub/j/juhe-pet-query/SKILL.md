---
name: juhe-pet-query
description: 宠物大全查询。查询猫、狗、水族、小宠、爬虫等各类宠物品种信息，包括基本信息、详细介绍、饲养知识等。使用场景：用户说"查一下哈士奇"、"想知道金毛的特点"、"推荐适合新手养的宠物"、"猫咪品种大全"、"狗狗饲养知识"等。通过聚合数据（juhe.cn）API 实时查询，免费注册每天免费调用。
homepage: https://www.juhe.cn/docs/api/id/755
metadata: {"openclaw":{"emoji":"🐾","requires":{"bins":["python3"],"env":["JUHE_PET_QUERY_KEY"]},"primaryEnv":"JUHE_PET_QUERY_KEY"}}
---

# 宠物大全查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

查询各类宠物品种信息：**狗狗、猫咪、水族、小宠、爬虫**等，支持搜索和详情查询。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [宠物大全 API](https://www.juhe.cn/docs/api/id/755) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_PET_QUERY_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_PET_QUERY_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/pet_query.py --key 你的AppKey 哈士奇
```

> 免费额度：每天免费调用，具体次数以官网为准。

---

## 使用方法

### 搜索宠物（按名称）

```bash
python scripts/pet_query.py 哈士奇
```

输出示例：

```
🐾 宠物搜索结果

#1 哈士奇
   类别：狗狗
   别名：西伯利亚雪橇犬
   产地：俄罗斯
   体重：4-8kg
   身高：23-30cm
   寿命：14-15 年
   特征：中小型犬，友善，活泼
```

### 按类别搜索

```bash
# 搜索狗狗品种
python scripts/pet_query.py --category dog

# 搜索猫咪品种
python scripts/pet_query.py --category cat

# 搜索水族
python scripts/pet_query.py --category shuizu

# 搜索小宠
python scripts/pet_query.py --category xiaochong

# 搜索爬虫
python scripts/pet_query.py --category pachong
```

### 查看宠物详情

```bash
python scripts/pet_query.py --detail 哈士奇
```

### 直接调用 API（无需脚本）

```
# 搜索宠物
GET https://apis.juhe.cn/fapigx/pet/search?key=YOUR_KEY&q=哈士奇

# 查询详情
GET https://apis.juhe.cn/fapigx/pet/detail?key=YOUR_KEY&hash_id=95ea875290486c02
```

---

## AI 使用指南

当用户查询宠物相关信息时，按以下步骤操作：

1. **识别需求** — 确定用户是想搜索还是查看特定宠物详情
2. **调用搜索接口** — 先用名称搜索获取宠物列表
3. **调用详情接口** — 根据 hash_id 获取详细信息
4. **展示结果** — 清晰展示宠物信息，包括特征、饲养知识等



### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `name` | 宠物名称 | 哈士奇 |
| `alias` | 别名 | 西伯利亚雪橇犬 |
| `category` | 类别 | dog/cat/shuizi/xiaochong/pachong |
| `origin` | 原产地 | 俄罗斯 |
| `weight` | 体重 | 4-8kg |
| `height` | 身高 | 23-30cm |
| `life_span` | 寿命 | 14-15 年 |
| `fur_color` | 毛色 | 黑白色 |
| `functions` | 用途 | 伴侣犬 |
| `introduction` | 介绍 | 详细介绍... |
| `history` | 历史 | 品种历史... |
| `care_knowledge` | 饲养知识 | 饲养要点... |
| `common_diseases` | 常见疾病 | 疾病预防... |
| `fur_care` | 毛发护理 | 护理方法... |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/755) 重新申请 |
| `error_code` 10012 | 当日免费次数已用尽，建议升级套餐 |
| 参数错误 | 参数错误，检查参数格式 |
| 无搜索结果 | 告知用户未找到相关宠物，建议更换搜索词 |

---

## 脚本位置

`scripts/pet_query.py` — 封装了 API 调用、搜索、详情查询和结果格式化。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **宠物大全**：猫、狗、水族、小宠、爬虫等品种查询
- **物流快递**：100+ 快递公司实时追踪
- **身份核验**：手机号实名认证、身份证实名验证

注册即可免费使用，适合个人开发者和企业接入。
