# Gmail 过滤器网上公认做法调研(2026-09-26)

> 由调研 agent 汇总,只查资料未动邮箱。每条关键结论附出处。

**Gmail 过滤器"黄金标准"调研摘要(2025–2026)**

有两处要先说明:
- 中文关键词的匹配方式,我没有找到 Google 官方说明,也没有找到中文实测。结论是由日文实测推断的(第 5 节)。
- 过滤器数量上限各来源说法矛盾,没有官方数字。

我只查了网上资料,没有动 用户的邮箱和任何设置。

---

### 1. 过滤器里哪些运算符可靠

**可以用**(均来自 Google 官方运算符页):
- `from:` `to:` `cc:` `subject:` `list:` `deliveredto:` `has:attachment` `filename:` `larger:` `size:` `category:`
- `{a b}` 等于 a 或 b,`-` 表示排除,`( )` 分组,`+word` 精确匹配(不做词形变化)
- 新增的 `header:`,例如 `header:X-Google-Calendar-Notification:rsvpAccepted`
- `category:` 现在还多了 `reservations` 和 `purchases` 两类
- 来源:https://support.google.com/mail/answer/7190?hl=en

**`category:` 在过滤器里确认能用。** Google 自己的 Workspace 教程就教人建 `category:promotion`、`category:social`、`category:update`、`category:forum` 四条过滤器,动作是"加标签 + 跳过收件箱"。注意官方教程用的是单数写法。来源:https://support.google.com/a/users/answer/9300019?hl=en

**不要用在过滤器里的:** Gmail 会弹窗警告:"Filter searches containing 'label:', 'in:', 'is:', or stars criteria will never match incoming mail"。原因是新邮件到达时还没有这些状态。
- 来源:https://news.ycombinator.com/item?id=4621698 、https://zapier.com/blog/gmail-filters/
- `before:` / `after:` 这类日期条件同理(推论)。
- `has:nouserlabels` 有人报告"搜索能用、放进过滤器失效":https://support.google.com/mail/thread/175216397

**执行顺序:**
- 所有命中的过滤器都会执行,没有"命中后停止"。
- 执行顺序按创建先后;在网页界面编辑一条过滤器,它会被移到最后。
- 想模拟"停止",只能在后面的过滤器里写排除条件。
- 来源:https://www.draconianoverlord.com/2017/02/04/gmail-filter-tips.html/

**一个关键推论:** 动作里没有"放回收件箱"。所以一旦某条过滤器把邮件归档了,没有其他过滤器能把它救回来。保护重要邮件只有两个办法:
- 在每一条会归档的过滤器里写排除组 `-{...}`;
- 或者开启 Priority Inbox 的"Override filters",让标记为重要的邮件留在收件箱。

**每条过滤器只能加一个用户标签和一个分类。** 要加多个标签就得拆成多条。来源:https://github.com/taers232c/GAMADV-XTD3/wiki/Users-Gmail-Filters

**"Doesn't have"(不包含)字段** 最终会变成一个排除查询(API 里叫 negatedQuery)。多个词之间是"且"还是"或",没有找到可靠说明。建议直接在"包含字词"里写 `-{a b c}`,意思明确:不含 a、b、c 中任何一个。

**上限:**
- 单条查询约 1,500 字符。实测在 1,469–1,488 之间,超出会报 "The specified filter is too long"。来源:https://www.spudart.org/blog/character-limit-for-gmail-filter/
- 过滤器数量:第三方分别说 500、1,000、10,000,没有官方出处。对一个人用来说不会碰到。

**其他行为:**
- 过滤器只作用于新邮件。
- 勾"同时应用于匹配的会话"时,不会补做转发动作。
- 回信只有自己也符合条件才会被过滤。
- 来源:https://support.google.com/mail/answer/6579?hl=en

### 2. 最常被推荐的配方和对应动作

| 类型 | 查询 | 动作 |
|---|---|---|
| Newsletter(最流行) | `unsubscribe`,或 linuz90 版:`unsubscribe OR from:noreply OR from:no-reply OR "this email was sent to" …`,并带排除组 `-{"confirm your" subject:urgent subject:alert}` | 跳过收件箱 + 标签 |
| 促销(Google 官方) | `category:promotion` / `social` / `update` / `forum` | 标签 + 跳过收件箱 |
| 日历邀请 | `invite.ics`(Google 官方);已接受的回复:`filename:invite.ics AND accepted`(Jeff Su) | 跳过收件箱 + 标为已读 |
| 日历回复(官方) | `header:X-Google-Calendar-Notification:rsvpAccepted OR …` | 归档或加标签 |
| GitHub 噪音 | `from:notifications@github.com -cc:(mention@noreply.github.com OR author@noreply.github.com OR assign@noreply.github.com)` | 标签 + 跳过收件箱 |
| GitHub 要处理的 | `from:notifications@github.com cc:(mention@noreply.github.com OR review_requested@noreply.github.com OR assign@noreply.github.com)` | 标签 + 标为重要 |
| 收据 | `subject:(receipt OR invoice OR order)` | 标签 Finance/Receipts,可选跳过收件箱 |
| 安全 / 2FA | "verification code"、"new sign-in"、"password reset" 这类短语 | 标签 + 星标 + 永不进垃圾箱,**不要归档** |
| 抄送 / 待回 | 自己 BCC `you+waiting@gmail.com` | 加 Waiting 标签 + 跳过收件箱 + 标为已读 |

各行来源:
- Newsletter:https://zapier.com/blog/gmail-filters/ 、https://github.com/linuz90/gmail-newsletters-filter
- 日历回复:https://support.google.com/calendar/answer/17366804
- GitHub:https://docs.github.com/en/subscriptions-and-notifications/reference/email-notification-headers 。GitHub 抄送地址按原因区分,一共 13 种:assign、author、ci_activity、comment、manual、mention、push、review_requested、security_alert、state_change、subscribed、team_mention、your_activity。有作者称用这套方法把 GitHub 通知噪音砍掉 91%:https://www.tglyn.ch/blog/reducing_github_noise_email_solution/
- 安全 / 2FA:https://roihacks.com/how-to-create-gmail-filter-for-security-emails/ 。该文警告不要只用"security"一个词,会误中营销邮件。
- 抄送 / 待回:https://www.jeffsu.org/inbox-zero-tutorial-for-gmail/

### 3. 标签体系

- **Jeff Su 方案(流传最广):** 只用 4 个动作型标签:Follow Up、Waiting、Read Through、Calendar。收件箱类型改为 Multiple Inboxes,按标签分区;"Filtered mail"设为"Don't override filters";重要性标记关掉。
- **Multiple Inboxes 最多 5 个分区**,每区一条查询。它和默认的分类标签页是两种互斥的收件箱类型,不能同时用。来源:https://support.google.com/mail/answer/9694882?hl=en
- **"Override filters"是个开关:** 开着时,被标为重要的邮件即使命中"跳过收件箱"也会留在收件箱。追求 inbox zero 的人通常关掉它;反过来,把它开着也可以当作重要邮件的保护网。来源:https://www.getinboxzero.com/blog/post/gmail-filters-not-working-troubleshooting-guide
- **Gmail 自带的新功能:**
  - 2025 年 7 月上线 Manage subscriptions(集中退订):https://blog.google/products-and-platforms/products/gmail/new-manage-subscriptions-unsubscribe/
  - 2025 年 9 月上线 Purchases 视图:https://9to5google.com/2025/09/11/gmail-purchases/
  - 这两个可以替代一部分手写的 Newsletter 和收据过滤器。

### 4. 常见坑

- **`unsubscribe` 会大面积误伤。** 银行账单、收据、SaaS 通知的页脚都有这个词。linuz90 的 README 自己也提醒,批量应用到旧邮件之前要先检查。
- **动作叠加没法撤回。** 因为没有"放回收件箱"的动作(见第 1 节),每条会归档的过滤器都要附同一个保护排除组(安全、验证码、账单、VIP),不能指望另写一条"保护"过滤器。
- **上线前先测。** 先在搜索框跑查询,范围选"所有邮件"而不是收件箱。上线后先只加标签观察约一周,确认没误伤再加"跳过收件箱"。"同时应用于匹配的会话"会一次处理大量历史邮件,要看清命中数量再勾。
- **过滤器本身是攻击面。** Google 现在对创建或导入过滤器、新增转发地址会要求二次验证,因为攻击者常用过滤器把安全提醒藏起来。应定期检查已有过滤器和转发设置。来源:https://www.phonearena.com/news/google-gmail-update-stronger-protection_id150079

### 5. 中文关键词

- **官方没有说明。** 我找到的最接近证据是日文实测:日文搜索是部分匹配,例如"内閣"能命中"内閣総理大臣"。连续的英文或数字则要整词匹配:"goo" 搜不到 "google","44510" 搜不到 "44510A1234",但 "gmail" 能命中 "gmail.com",因为句点是分隔符。
  - 来源:https://maru-note.net/entry/2022/11/22/210445 、https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12280042607
- **推论(未验证):** 中文同属 CJK,很可能也是子串匹配。这意味着"优惠"会同时命中"优惠券"和银行邮件里的"优惠利率",误伤会比英文更严重。
- **建议:**
  - 中文关键词尽量只用在 `subject:` 里,并用较长的短语,例如 `subject:(电子发票)`。少数派有实际用例:https://sspai.com/post/68333
  - 优先靠 `from:` 或 `list:` 定位发件方。
  - 另一个 agent 设计时,最好先用只读的 Gmail search_threads 搜一次"优惠",看是否命中"优惠券",用实际结果确认。

---

### 可以直接用的查询(12 条)

```
1  subject:("verification code" OR "security code" OR "one-time password" OR "new sign-in" OR "password reset" OR 验证码 OR 动态码 OR 登录提醒 OR 重置密码)   → 星标+标为重要+永不进垃圾箱,绝不归档
2  保护排除组(附在每条会归档的过滤器末尾): -{subject:(验证码 OR "verification code" OR "password reset" OR invoice OR 账单 OR 发票 OR "payment failed") from:(vip1@x.com OR *@bank.com)}
3  unsubscribe -{"verification code" invoice receipt 发票 账单}   → Newsletter 标签+跳过收件箱
4  category:promotion                                            → 标签+跳过收件箱(Google 官方)
5  category:social OR from:(linkedin.com OR facebookmail.com OR x.com)  → Social 标签+跳过收件箱+已读
6  subject:(receipt OR "order confirmation" OR "payment received" OR 收据 OR 订单确认)  → Finance/Receipts+跳过收件箱
7  has:attachment filename:pdf subject:(invoice OR 发票 OR 账单)    → Finance/Invoices,留在收件箱
8  filename:invite.ics                                            → Calendar 标签
9  header:X-Google-Calendar-Notification:rsvpAccepted OR header:X-Google-Calendar-Notification:rsvpTentative  → 

跳过收件箱 + 标为已读
```
```
10 from:notifications@github.com -cc:(mention@noreply.github.com OR author@noreply.github.com OR assign@noreply.github.com OR review_requested@noreply.github.com OR security_alert@noreply.github.com)   → GitHub 标签+跳过收件箱
11 from:notifications@github.com cc:(mention@noreply.github.com OR review_requested@noreply.github.com OR assign@noreply.github.com OR security_alert@noreply.github.com)   → GitHub 标签+标为重要
12 deliveredto:you+waiting@gmail.com                              → Waiting 标签+跳过收件箱+已读
```

第 12 条用 `deliveredto:` 而不用 `to:`,因为自己 BCC 给自己时,地址不在 To 栏里。

**另外两条可选,尚未验证在过滤器里是否生效,先用搜索测:**
- 出行:`category:reservations`
- 购物 / 物流:`category:purchases`
- 这两个分类官方只说支持搜索,没说支持过滤器。不行就退回按主题匹配,例如 `subject:(itinerary OR 行程 OR 发货 OR 物流 OR "out for delivery")`。

**写法提醒:**
- `from:(a OR b)`、`cc:(a OR b)` 这种分组写法是常见用法。
- `*@domain.com` 可以匹配整个域名(Zapier 的示例)。
- 以上所有查询都要控制在约 1,500 字符以内。
