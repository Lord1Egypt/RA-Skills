name: kuaidi100
description: 使用快递100 API 查询快递物流轨迹、签收状态，支持自动识别快递公司及多家主流快递公司查询。
metadata: { "openclaw": { "emoji": "📦", "requires": { "bins": ["python3"], "env": ["KUAIDI100_KEY", "KUAIDI100_CUSTOMER"] }, "primaryEnv": "KUAIDI100_KEY" } }
快递100查询（KuaiDi100）
基于 快递100 API 的 OpenClaw 技能，用于查询快递物流轨迹、签收状态等信息，支持自动识别快递公司。

使用技能前需要申请授权Key，申请地址：https://www.kuaidi100.com/manager/v2/query/overview

环境变量配置
# Linux / macOS
export KUAIDI100_KEY="your_key_here"
export KUAIDI100_CUSTOMER="your_customer_id"

# Windows PowerShell
$env:KUAIDI100_KEY="your_key_here"
$env:KUAIDI100_CUSTOMER="your_customer_id"
脚本路径
脚本文件：skills/kuaidi100/kuaidi100.py

使用方式
1. 自动识别快递公司查询
python3 skills/kuaidi100/kuaidi100.py '{"number":"JDxxxxx"}'
2. 指定快递公司查询
python3 skills/kuaidi100/kuaidi100.py '{"number":"JDxxxxx","com":"jd"}'
3. 查询支持的快递公司列表
python3 skills/kuaidi100/kuaidi100.py companies
返回值为数组，每项形如：

{
  "comCode": "shunfeng",
  "name": "顺丰速运"
}
请求参数（查询时传入 JSON）
字段名    类型    必填    说明
number    string    是    快递单号
com    string    否    快递公司代号，不填则自动识别
phone    string    否    收/寄件人手机号后四位（部分快递需要）
示例：

{
  "number": "JDxxxxx",
  "com": "jd"
}
返回结果示例
脚本直接输出接口返回的 JSON，典型结构：

{
  "message": "ok",
  "nu": "JDxxxxx",
  "com": "jd",
  "state": "3",
  "data": [
    {
      "time": "2024-01-15 14:30:00",
      "context": "已签收，签收人：本人"
    },
    {
      "time": "2024-01-15 08:20:00",
      "context": "配送员正在为您派送中"
    },
    {
      "time": "2024-01-14 20:15:00",
      "context": "快件到达【北京朝阳区东城分部】
    }
  ]
}
状态码说明（state 字段）：

代号    说明
0    在途中
1    已揽收
2    异常
3    已签收
4    退签
5    派送中
6    退回
错误时输出示例：

{
  "error": "api_error",
  "message": "快递公司代码错误",
  "status": "0"
}
支持的快递公司
代号    名称
shunfeng    顺丰速运
yuantong    圆通速递
zhongtong    中通快递
yunda    韵达快运
shentong    申通快递
jtexpress    极兔速递
tiantian    天天快递
ems    EMS
youzhengguonei    中国邮政
debang    德邦快递
jd    京东快递
suning    苏宁快递
在 OpenClaw 中的推荐用法
用户例如：「帮我查一下京东快递 JDxxxxx」
代理构造：python3 skills/kuaidi100/kuaidi100.py '{"number":"JDxxxxx","com":"jd"}'。
解析返回的 JSON，为用户总结：当前状态、是否签收、最近几条轨迹等。
OpenClaw 技能配置
在 OpenClaw 配置文件中添加：

{
  "skills": {
    "kuaidi100": {
      "enabled": true
    }
  }
}
设置环境变量后即可使用。
