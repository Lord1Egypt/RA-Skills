# Meituan Skill

美团上最难的不是“选哪家”，而是“这一单现在到底该不该点”。

这个 skill 是一个公开可见信息决策助手：它把商家、配送时效、门槛优惠、配送费、包装费、评论风险、退款摩擦放到一起，直接给出行动建议。

## 适合什么问题

- “这两家美团哪家更值？”
- “为了满减再凑一个菜划算吗？”
- “这家更便宜，但要晚 25 分钟，值不值？”
- “这家店评论一般，要不要冒险试试？”
- “团购券看着便宜，有没有隐藏门槛？”
- “这一单现在点，还是换一家更稳？”

## 它会怎么帮用户

默认收敛到一个动作：

- 现在点这家
- 换另一家
- 不要为了门槛硬凑单
- 加一个真正有用的小项
- 多花一点买更快更稳的配送
- 直接跳过这家店

## 决策重点

- 真实到手价：小计、配送费、包装费、服务费、门槛差额一起看
- 时间价值：午饭、赶会、工作间隙时，ETA 经常比几块钱更重要
- 商家风险：差评里的延迟、错送、分量、卫生、退款摩擦要单独扣分
- 凑单质量：只有加购项真的有用、净省仍成立，才建议冲门槛
- 证据边界：只使用公开页面、截图、用户复制的信息，不读取账号态数据

## 安全边界

这个版本有意做成 Markdown-only skill。

它不会登录，不读取订单，不读取账号券，不领取红包，不保存 cookie，不改地址，不改购物车，不提交订单，不付款。

如果最终价格、地址时效、账号券、库存或支付方式需要进入账号/结算页确认，它会把这些列为用户自己核对的事项。

## 典型输出

- `Recommended Move`
- `Checkout Reality`
- `Risk Check`
- `Confidence And Gaps`
- `Before You Order`

## 安装

```bash
clawhub install meituan
```

## 发布 2.2.0

```bash
clawhub publish /Users/jianghaidong/Library/Mobile\ Documents/com~apple~CloudDocs/codex/openclaw-edit-staging/meituan \
  --slug meituan \
  --owner harrylabsj \
  --version 2.2.0 \
  --tags "latest,meituan,local-life,food-delivery,delivery,decision,waimai,china,no-login,public-data" \
  --changelog "Ship a Markdown-only public Meituan decision skill with stronger checkout-reality math, confidence gaps, and no account-state package surface."
```
