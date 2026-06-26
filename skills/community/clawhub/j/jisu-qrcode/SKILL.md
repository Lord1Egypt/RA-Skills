---
name: "QR Code Generation And Recognition - 二维码生成识别"
description: 按文本生成带模板样式的二维码（base64），或识别二维码内容及模板列表。当用户说：把这段链接生成二维码、识别图里二维码内容，或类似二维码 API 问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🔲", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据二维码生成识别（Jisu QRCode）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- 根据文本/URL 生成二维码图片（base64），可选颜色、纠错等级、模板、LOGO 等参数；
- 识别二维码内容（支持二维码图片 URL 或 base64）；
- 获取官方提供的二维码模板样例列表。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [二维码生成识别 API](https://www.jisuapi.com/api/qrcode/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/qrcode/qrcode.py`

## 使用方式

当前脚本提供 3 个子命令：

- `generate`：二维码生成（/qrcode/generate）
- `read`：二维码识别（/qrcode/read）
- `template`：获取二维码模板样例（/qrcode/template）

### 1. 二维码生成（/qrcode/generate）

```bash
python3 skills/qrcode/qrcode.py generate '{
  "text": "https://www.jisuapi.com/api/sms",
  "width": 300,
  "tempid": 1,
  "margin": 10,
  "bgcolor": "FFFFFF",
  "fgcolor": "000000",
  "oxlevel": "L",
  "logo": "https://www.jisuapi.com/static/images/icon/qrcode.png"
}'
```

请求字段：

| 字段名  | 类型   | 必填 | 说明 |
|---------|--------|------|------|
| text    | string | 是   | 二维码内容（文本或 URL） |
| bgcolor | string | 否   | 背景色，默认 `FFFFFF`（白色） |
| fgcolor | string | 否   | 前景色，默认 `000000`（黑色） |
| oxlevel | string | 否   | 纠错等级 `L/M/Q/H`，默认 `L` |
| width   | int    | 否   | 宽度（像素），默认 `300` |
| margin  | int    | 否   | 边距（包含在宽度内），默认 `0` |
| logo    | string | 否   | LOGO 地址（HTTP 链接） |
| tempid  | int    | 否   | 模板 ID（参考模板接口返回） |

返回字段（`result`）：

| 字段名 | 类型     | 说明 |
|--------|----------|------|
| qrcode | string   | 二维码图片 base64 内容（可直接用作 `img` 的 data URI） |

### 2. 二维码识别（/qrcode/read）

```bash
python3 skills/qrcode/qrcode.py read '{
  "qrcode": "https://api.jisuapi.com/qrcode/static/images/sample/1.png"
}'
```

请求字段：

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| qrcode | string | 是   | 支持 base64 或可访问的二维码图片 URL |

返回字段：

| 字段名 | 类型   | 说明       |
|--------|--------|------------|
| text   | string | 解码后的内容 |

### 3. 获取二维码模板样例（/qrcode/template）

```bash
python3 skills/qrcode/qrcode.py template '{}'
```

返回字段：

`result` 为字符串数组，每个元素为一个模板样例图片 URL。

## 常见错误码

业务错误码（来源于官网文档）：

| 代号 | 说明         |
|------|--------------|
| 201  | 二维码内容为空 |
| 202  | 背景颜色不正确 |
| 203  | 前景颜色不正确 |
| 204  | 纠错等级不正确 |
| 205  | logo 地址不正确 |
| 206  | 模板 ID 不正确 |
| 209  | 二维码地址不正确 |

系统错误码：

| 代号 | 说明             |
|------|------------------|
| 101  | APPKEY 为空或不存在 |
| 102  | APPKEY 已过期    |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制   |
| 105  | IP 被禁止       |
| 106  | IP 请求超过限制   |
| 107  | 接口维护中       |
| 108  | 接口已停用       |

## 推荐用法

1. 用户提问：「帮我给这个活动页生成一个二维码图片」「帮我识别这个二维码里是什么链接」。  
2. 对于生成需求：构造包含活动页 URL 的 `text` 字段，调用 `generate` 获取 `qrcode` base64，并在回答中提示用户可直接嵌入到前端页面或转存为图片；  
3. 对于识别需求：将二维码图片 URL 或 base64 作为 `qrcode` 参数调用 `read`，从返回的 `text` 字段中读取内容，并结合其它技能（如 `jisu` 统一入口或 `qrcode2` 本地生成/识别）进行后续处理或安全检查。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

