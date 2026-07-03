---
name: outbound-travel-assistant
display_name: 出境游旅行助手
description: 出境游一站式全链路助手，11个工具覆盖国际机票酒店搜索、签证查询、安全评级、插头电压、退税计算、汇率换算、航班座位行李、紧急求助，零配置即装即用。
tags: [出境游, 签证查询, 退税计算, 国际机票, 旅行安全]
tools:
  - name: search_flights
    description: 搜索国际机票，输入出发城市、到达城市和日期，返回航班信息和预订链接
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: search_hotels
    description: 搜索酒店，输入城市、入住和离店日期，返回酒店信息和预订链接
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: flight_seats
    description: 查询航班座位布局和选座价格，输入航班号和日期
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: flight_baggage
    description: 查询航班行李额度和超重费用，输入航班号和日期
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: hotel_detail
    description: 查看酒店房型价格和退改政策，输入酒店ID和入住离店日期
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
  - name: check_visa
    description: 查询签证要求和材料清单，输入目的地和出行目的，覆盖34个出境游热门国家
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: check_safety
    description: 查看目的地安全评级和风险提示，返回5维评分和出行建议，覆盖34个国家
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: check_plug
    description: 查询插头类型电压标准和转换器推荐，覆盖34个出境游热门国家
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: emergency_help
    description: 紧急求助电话和使领馆联系方式，支持7大紧急场景行动指南
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: calc_tax_refund
    description: 计算购物退税金额含手续费明细，覆盖15个退税热门国家
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用本地数据，无需Token）
        required: false
  - name: exchange_rate
    description: 实时汇率换算，基于免费汇率API，无需Token
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（本工具使用免费API，无需Token）
        required: false
---

# 出境游旅行助手 — 11个工具，从签证到退税全覆盖

> 国际机票酒店搜索、签证查询、安全评级、插头电压、退税计算、汇率换算、航班座位行李、紧急求助，一站式搞定出境需求。

🔥 **核心亮点：**
- **34国签证数据** — 覆盖主流出境游国家的签证要求和材料清单
- **5维安全评估** — 犯罪/恐怖/自然/健康/交通全面评分
- **退税计算器** — 15国退税金额含手续费明细，自动识别无退税国家
- **航班座位+行李** — 查座位布局、选座价格、行李额度和超重费用
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "泰国旅游需要签证吗"
2. "6月20号北京飞东京的机票"
3. "在日本买了5万日元的东西能退多少税"

## 核心能力

1. **国际机票搜索** — 搜索国际机票，返回航班号、价格和预订链接
2. **酒店搜索** — 搜索全球酒店，返回价格、星级和预订链接
3. **签证查询** — 34国签证要求和材料清单，含免签/落地签/电子签
4. **安全评级** — 5维评分+风险提示+安全建议+紧急电话
5. **插头电压** — 34国插头类型、电压标准和转换器推荐
6. **退税计算** — 15国退税金额计算，含手续费明细和人民币换算
7. **航班座位** — 查询座位布局和选座价格
8. **航班行李** — 查询行李额度和超重费用
9. **汇率换算** — 实时汇率换算
10. **紧急求助** — 7大紧急场景行动指南+使领馆联系方式
11. **酒店详情** — 查看房型价格和退改政策

## 能做什么

- 搜索国际机票和酒店并获取预订链接
- 查询34国签证要求和材料清单
- 查看目的地安全评级和5维评分
- 查询插头类型电压和转换器推荐
- 计算购物退税金额含手续费明细
- 实时汇率换算
- 查询航班座位布局和行李额度
- 紧急求助电话和使领馆联系方式

## 不能做什么

- 签证政策随时变动请以使领馆最新公告为准
- 预订链接需用户自行完成支付
- 安全评级仅供参考不构成出行建议
- 退税金额为估算实际以退税公司为准

## 使用提示

- 搜索机票时建议提供具体日期和城市三字码
- 签证查询结果请与使领馆官网二次确认
- 紧急求助请优先拨打当地紧急电话
- 退税时保留所有购物小票和退税单
- 英国已于2021年取消退税，别在英国大额购物

## 🔗 搭配使用

- **签证聪明办** — 更详细的签证办理攻略和材料清单
- **旅行购物退税计算器** — 专项退税计算，覆盖更多国家
- **旅行插头电压查询** — 专项插头电压查询，含电器安全检查

## 数据流向

机票/酒店/航班工具通过RG云端代理获取实时数据；签证/安全/插头/退税/紧急求助为本地知识数据库；汇率使用免费公开API。代理服务不存储用户数据。
