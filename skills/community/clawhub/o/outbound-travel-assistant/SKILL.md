---
name: outbound-travel-assistant
display_name: "出境游旅行助手"
description: "零配置即装即用，提供出境游一站式全链路服务，支持搜索国际机票和酒店并获取含佣金预订链接、查询签证要求和材料清单、查看目的地安全评级和风险提示、查询插头类型电压标准和转换器推荐、计算购物退税金额含手续费明细、实时汇率换算、查询航班座位布局和选座价格、查询航班行李额度和超重费用、查看酒店房型价格和退改政策、紧急求助电话和使领馆联系方式，基于RG云端代理和本地知识数据库"
tags: [出境游, 旅行助手, outbound-travel, 签证, 安全, 退税, 汇率, 机票, 酒店]
features: "搜索国际机票和酒店并获取含佣金预订链接;查询签证要求和材料清单;查看目的地安全评级和风险提示;查询插头类型电压标准和转换器推荐;计算购物退税金额含手续费明细;实时汇率换算;查询航班座位布局和选座价格;查询航班行李额度和超重费用;查看酒店房型价格和退改政策;紧急求助电话和使领馆联系方式"
examples: "6月20号北京飞东京的机票;泰国旅游需要签证吗;日本安全吗去旅游;去英国需要带什么转换插头;在日本买了5万日元的东西能退多少税;1000人民币换多少日元;CA1234航班的座位图;北京飞曼谷可以带多少行李;东京希尔顿的房型和价格;在泰国护照丢了怎么办"
limitations: "签证政策随时变动请以使领馆最新公告为准;预订链接需用户自行完成支付;安全评级仅供参考不构成出行建议;退税金额为估算实际以退税公司为准;汇率实时波动换算结果仅供参考"
tips: "搜索机票时建议提供具体日期和城市三字码;搜索酒店时建议提供城市名加入住离店日期;签证查询结果请与使领馆官网二次确认;紧急求助请优先拨打当地紧急电话;退税时保留所有购物小票和退税单"
tools:
  - name: search_flights
    description: 搜索国际机票，输入出发城市、到达城市和日期，返回航班信息和含佣金预订链接
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_hotels
    description: 搜索酒店，输入城市、入住和离店日期，返回酒店信息和含佣金预订链接
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: flight_seats
    description: 查询航班座位布局和选座价格，输入航班号和日期
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: flight_baggage
    description: 查询航班行李额度和超重费用，输入航班号和日期
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: hotel_detail
    description: 查看酒店房型价格和退改政策，输入酒店ID和入住离店日期
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: check_visa
    description: 查询签证要求和材料清单，输入目的地和出行目的，覆盖34个出境游热门国家
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: check_safety
    description: 查看目的地安全评级和风险提示，返回5维评分和出行建议，覆盖34个国家
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: check_plug
    description: 查询插头类型电压标准和转换器推荐，覆盖34个出境游热门国家
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: emergency_help
    description: 紧急求助电话和使领馆联系方式，支持7大紧急场景行动指南，覆盖护照丢失、航班取消、医疗急救、被盗被抢、自然灾害、交通事故、法律纠纷
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: calc_tax_refund
    description: 计算购物退税金额含手续费明细，覆盖15个退税热门国家
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: exchange_rate
    description: 实时汇率换算，基于免费汇率API，无需Token
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用免费API，无需Token）
        required: false
---

# 出境游旅行助手

出境游一站式全链路助手，11个工具覆盖从签证到退税的完整出境需求。

## 能做什么

- **search_flights**：搜索国际机票，输入出发城市、到达城市和日期，返回航班号、出发到达时间、价格和含佣金预订链接
- **search_hotels**：搜索酒店，输入城市和入住离店日期，返回酒店名、星级、最低价和含佣金预订链接
- **flight_seats**：查询航班座位布局和选座价格，输入航班号和日期
- **flight_baggage**：查询航班行李额度和超重费用，输入航班号和日期
- **hotel_detail**：查看酒店房型价格和退改政策，输入酒店ID和入住离店日期
- **check_visa**：查询签证要求和材料清单，覆盖34个出境游热门国家
- **check_safety**：查看目的地安全评级和风险提示，返回5维评分（犯罪、恐怖、自然灾害、健康、交通）和出行建议
- **check_plug**：查询插头类型、电压标准和转换器推荐，覆盖34个国家
- **emergency_help**：紧急求助电话和使领馆联系方式，支持7大紧急场景行动指南
- **calc_tax_refund**：计算购物退税金额含手续费明细，覆盖15个退税热门国家
- **exchange_rate**：实时汇率换算，输入源币种、目标币种和金额

## 不能做什么

- 签证政策随时变动请以使领馆最新公告为准
- 预订链接需用户自行完成支付
- 安全评级仅供参考不构成出行建议
- 退税金额为估算实际以退税公司为准
- 汇率实时波动换算结果仅供参考

## 使用示例

1. "6月20号北京飞东京的机票" → search_flights
2. "泰国旅游需要签证吗" → check_visa
3. "日本安全吗去旅游" → check_safety
4. "去英国需要带什么转换插头" → check_plug
5. "在日本买了5万日元的东西能退多少税" → calc_tax_refund
6. "1000人民币换多少日元" → exchange_rate
7. "CA1234航班的座位图" → flight_seats
8. "北京飞曼谷可以带多少行李" → flight_baggage
9. "东京希尔顿的房型和价格" → hotel_detail
10. "在泰国护照丢了怎么办" → emergency_help

## 注意事项

- 机票和酒店搜索（search_flights/search_hotels/flight_seats/flight_baggage/hotel_detail）通过RG云端代理获取实时数据，需要PROXY_TOKEN环境变量
- 签证、安全、插头、紧急求助和退税计算使用本地知识数据库，无需网络请求
- 汇率查询使用免费公开API（open.er-api.com），无需Token
- **数据流向**：RG代理工具通过云端代理转发到API，代理不存储用户数据；本地数据工具纯本地运行，无数据外传

## 使用提示

- 搜索机票时建议提供具体日期和城市三字码
- 搜索酒店时建议提供城市名加入住离店日期
- 签证查询结果请与使领馆官网二次确认
- 紧急求助请优先拨打当地紧急电话
- 退税时保留所有购物小票和退税单
