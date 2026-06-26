---
name: "ISBN Book Number Query - ISBN图书书号查询"
description: 用 ISBN 查图书详情，或按书名关键字搜书。当用户说：9787 开头这本书是什么？帮我搜书名里带 Python 的书，或类似图书 ISBN 问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据 ISBN 图书书号查询（Jisu ISBN）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **ISBN 精确查询**：通过 10 位或 13 位 ISBN 查询图书详细信息；
- **关键字搜索**：通过书名关键字搜索图书列表，获取书名、作者、封面及 ISBN。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [ISBN 图书书号查询 API](https://www.jisuapi.com/api/isbn/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/isbn/isbn.py`

## 使用方式

### 1. 按 ISBN 查询图书信息

```bash
python3 skills/isbn/isbn.py '{"isbn":"9787212058937"}'
```

请求 JSON：

```json
{
  "isbn": "9787212058937"
}
```

### 2. 按关键字搜索图书（/isbn/search）

```bash
python3 skills/isbn/isbn.py search '{"keyword":"老人与海","pagenum":1}'
```

请求 JSON：

```json
{
  "keyword": "老人与海",
  "pagenum": 1
}
```

其中 `pagenum` 为可选，默认第一页，每页 20 条。

## 请求参数

### ISBN 查询

| 字段名 | 类型   | 必填 | 说明         |
|--------|--------|------|--------------|
| isbn   | string | 是   | 10 位或 13 位 ISBN |

### 关键字搜索

| 字段名   | 类型   | 必填 | 说明                        |
|----------|--------|------|-----------------------------|
| keyword  | string | 是   | 书名关键字                  |
| pagenum  | int    | 否   | 页码（默认第一页，一页 20 条） |

## 返回结果示例

### ISBN 查询返回（简化）

脚本直接输出接口 `result` 字段，结构与官网示例一致（参考 [`https://api.jisuapi.com/api/isbn/`](https://www.jisuapi.com/api/isbn/)）：

```json
{
  "title": "有理想就有疼痛",
  "subtitle": "中国当代文化名人访谈录",
  "pic": "http://api.jisuapi.com/isbn/upload/96/033c435b3f0f30.jpg",
  "author": "高晓春",
  "summary": "……",
  "publisher": "安徽人民出版社",
  "pubplace": "合肥",
  "pubdate": "2013-01",
  "page": 256,
  "price": "29.00",
  "binding": "",
  "isbn": "9787212058937",
  "isbn10": "7212058939",
  "keyword": "名人－访问记－中国－现代",
  "cip": "2012280296",
  "edition": "1版",
  "impression": "1",
  "language": "",
  "format": "23×18",
  "class": "K820.76",
  "sellerlist": [
    {
      "seller": "当当",
      "price": "20.80",
      "link": "http://product.dangdang.com/22921241.html"
    }
  ]
}
```

### 关键字搜索返回（简化）

```json
{
  "keyword": "老人与海",
  "total": 10000,
  "pagenum": 1,
  "pagesize": 20,
  "list": [
    {
      "title": "老人与海",
      "author": " (美) 海明威, 著",
      "pic": "https://api.jisuapi.com/isbn//upload/99/780099.jpg",
      "isbn": "9787511024817"
    }
  ]
}
```

当出现错误（如 ISBN 不正确或无数据）时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 202,
  "message": "ISBN不正确"
}
```

## 常见错误码

来源于 [极速数据 ISBN 文档](https://www.jisuapi.com/api/isbn/)：

| 代号 | 说明        |
|------|-------------|
| 201  | ISBN 为空   |
| 202  | ISBN 不正确 |
| 205  | 没有信息    |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户提供 ISBN：「帮我查一下 ISBN `9787212058937` 这本书的信息」。  
2. 代理构造 JSON：`{"isbn":"9787212058937"}` 并调用：  
   `python3 skills/isbn/isbn.py '{"isbn":"9787212058937"}'`  
3. 从返回结果中提取书名、作者、出版社、出版时间、定价、摘要等字段，为用户生成简要介绍；  
4. 如果用户只有书名大致关键字，可先调用搜索接口：  
   `python3 skills/isbn/isbn.py search '{"keyword":"老人与海","pagenum":1}'`，  
   在结果列表中选出最符合的图书，再用其 ISBN 进行精确查询。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

