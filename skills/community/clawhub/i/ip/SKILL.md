---
name: "IP Address Query - IP查询"
description: 根据 IP 查归属地与运营商类型。当用户说：这个 IP 是哪里的？是不是机房 IP？或类似 IP 归属问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📡", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据 IP 查询（Jisu IP）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。
根据 IP 地址查询其归属地与运营商类型。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [IP 查询 API](https://www.jisuapi.com/api/ip/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/ip/ip.py`

## 使用方式

### 查询 IP 归属地与运营商

```bash
python3 skills/ip/ip.py '{"ip":"122.224.186.100"}'
```

请求 JSON 示例：

```json
{
  "ip": "122.224.186.100"
}
```

## 请求参数

| 字段名 | 类型   | 必填 | 说明   |
|--------|--------|------|--------|
| ip     | string | 是   | IP 地址 |

## 返回结果示例

脚本直接输出接口的 `result` 字段，结构与官网示例一致（参考 [`https://www.jisuapi.com/api/ip/`](https://www.jisuapi.com/api/ip/)）：

```json
{
  "area": "浙江省杭州市",
  "type": "电信"
}
```

当出现错误（如没有该 IP 信息）时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据 IP 文档](https://www.jisuapi.com/api/ip/)：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户提供 IP：「查一下 IP `122.224.186.100` 是哪里的」。  
2. 代理构造 JSON：`{"ip":"122.224.186.100"}` 并调用：  
   `python3 skills/ip/ip.py '{"ip":"122.224.186.100"}'`  
3. 从返回结果中读取 `area` 和 `type` 字段，为用户总结 IP 所在的省市及运营商类型。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

