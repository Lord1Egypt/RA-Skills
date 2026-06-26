---
name: "Weibo, Baidu, Douyin Hot Search List - 微博百度热搜榜单"
description: 获取微博、百度、抖音等平台热搜榜单与链接等。当用户说：今天微博热搜前十？百度热搜有什么？或类似热搜榜单问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🔥", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据微博/百度/抖音热搜榜单（Jisu Hotsearch）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

支持查询三大平台热搜：

- **微博热搜** — 实时微博热门话题
- **百度热搜** — 百度搜索热点
- **抖音热搜** — 抖音热门视频话题

返回每条热搜的排名、标题、链接、指数、更新时间，可用于回答「现在微博/百度/抖音上有什么热搜」「帮我列出当前前 10 条热搜标题和链接」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [微博百度热搜榜单 API](https://www.jisuapi.com/api/hotsearch/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/hotsearch/hotsearch.py`

## 使用方式

### 1. 微博热搜（/hotsearch/weibo）

```bash
python3 skills/hotsearch/hotsearch.py weibo
```

### 2. 百度热搜（/hotsearch/baidu）

```bash
python3 skills/hotsearch/hotsearch.py baidu
```

### 3. 抖音热搜（/hotsearch/douyin）

```bash
python3 skills/hotsearch/hotsearch.py douyin
```

无需额外 JSON 参数，脚本直接输出接口 `result` 数组。

## 返回结果示例（节选）

```json
[
  {
    "sequence": "1",
    "title": "部分男性对丁真的态度",
    "link": "https://s.weibo.com/weibo?q=...",
    "score": "4103153",
    "updatetime": "2020-12-09 16:59:46"
  }
]
```

常见字段说明：

| 字段名      | 类型     | 说明           |
|-------------|----------|----------------|
| sequence    | string/int | 排名          |
| title       | string   | 标题           |
| link / linkurl | string | 标题链接（字段名视接口而略有差异） |
| score       | string   | 热度/指数      |
| updatetime  | string   | 更新时间       |

## 常见错误码

业务错误码（参考官网错误码参照，常见含义为「没有信息」等）：  
接口可能返回 `status != 0`，此时脚本会包装为：

```json
{
  "error": "api_error",
  "code": 210,
  "message": "没有信息"
}
```

通用系统错误码与其它极速数据接口一致（101–108）。详见 [极速数据热搜文档](https://www.jisuapi.com/api/hotsearch/)。

## 推荐用法

1. 用户提问：「现在微博/百度/抖音上有什么热搜？」  
2. 代理按平台调用对应命令，比如微博热搜：`python3 skills/hotsearch/hotsearch.py weibo`。  
3. 从返回数组中选取前 N 条（如前 10 条），读取 `title`、`link/linkurl`、`score`，用自然语言总结热点内容，并附上若干可点击的链接。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

