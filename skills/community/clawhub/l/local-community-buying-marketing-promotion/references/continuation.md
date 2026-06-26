    avg_order_value: float   # 客单价（元）
    new_user_ratio: float    # 新用户占比（0-1）
    new_user_acquisition_cost: float = 12.0  # 新用户获取成本参考价（元）
    gmv_lift_rate: float = 0.30  # GMV提升率（爆款场景下预期GMV增量百分比，默认30%）

    def calculate(self) -> Dict:
        # GMV
        gmv = self.expected_orders * self.avg_order_value

        # 补贴成本
        subsidy_cost = gmv * self.subsidy_rate

        # 新用户价值估算（拉新场景）
        if self.promotion_type in ["拉新", "引流"]:
            new_users = self.expected_orders * self.new_user_ratio
            # 新用户7日留存价值（保守估算：客单价×复购次数）
            new_user_ltv = self.avg_order_value * 2 * 0.3  # 7日内复购2次×30%留存率
            new_user_value = new_users * new_user_ltv
            roi = (new_user_value - subsidy_cost) / subsidy_cost * 100 if subsidy_cost > 0 else 0
        elif self.promotion_type in ["爆款", "冲量"]:
            # 爆款价值 = GMV增量 - 补贴成本
            # 使用实例的gmv_lift_rate参数（默认0.30，用户可自定义）
            gmv_increment = gmv * self.gmv_lift_rate
            roi = (gmv_increment - subsidy_cost) / subsidy_cost * 100 if subsidy_cost > 0 else 0
        elif self.promotion_type == "留存":
            # 留存价值 = 防止流失用户贡献的GMV
            retained_users = self.expected_orders * self.new_user_ratio * 0.5
            retained_gmv = retained_users * self.avg_order_value * 2  # 后续2个月复购
            roi = (retained_gmv - subsidy_cost) / subsidy_cost * 100 if subsidy_cost > 0 else 0
        else:
            roi = 0

        # 盈亏判断
        if self.promotion_type in ["拉新", "引流"]:
            # 拉新型：ROI > 0 = 合算
            verdict = "✅ ROI为正，拉新合算" if roi > 0 else "❌ ROI为负，需优化补贴"
        elif self.promotion_type in ["爆款", "冲量"]:
            # 爆款型：GMV增量 > 补贴 = 合算
            gmv_increment = gmv * self.gmv_lift_rate
            verdict = "✅ GMV增量覆盖补贴，合算" if gmv_increment > subsidy_cost else "❌ 补贴过高，需调整"
        else:
            verdict = "✅ 活动合理"

        # 各项成本明细
        if self.new_user_ratio > 0:
            new_users = self.expected_orders * self.new_user_ratio
            new_user_cost = subsidy_cost * self.new_user_ratio
            cost_per_new_user = new_user_cost / new_users if new_users > 0 else 0
        else:
            new_users = 0
            new_user_cost = 0
            cost_per_new_user = 0

        # 优化建议
        suggestions = []
        if roi < 0 and self.promotion_type in ["拉新", "引流"]:
            suggestions.append(f"⚠️ 拉新ROI为负，建议提升新用户复购预期或降低补贴率")
        if self.subsidy_rate > 0.25:
            suggestions.append(f"⚠️ 补贴率 > 25%，行业偏高，建议控制在 15-20%")
        if cost_per_new_user > 20:
            suggestions.append(f"⚠️ 新用户获取成本 ¥{cost_per_new_user:.1f}，高于行业均值12元")
        if roi > 50 and self.promotion_type in ["拉新", "引流"]:
            suggestions.append(f"✅ ROI高达 {roi:.0f}%，拉新效率优秀，可适当放量")

        return {
            "活动类型": self.promotion_type,
            "预期GMV": f"¥{gmv:,.0f}",
            "补贴率": f"{self.subsidy_rate*100:.1f}%",
            "补贴成本": f"¥{subsidy_cost:,.0f}",
            "新用户数": f"{new_users:.0f} 人（占比{self.new_user_ratio*100:.0f}%）",
            "新用户获取成本": f"¥{cost_per_new_user:.1f}/人" if new_users > 0 else "N/A",
            "ROI估算": f"{roi:.1f}%",
            "盈亏判断": verdict,
            "优化建议": suggestions,
        }


def run():
    print("=" * 55)
    print("促销ROI计算器")
    print("=" * 55)

    promo_type = input("活动类型（引流/爆款/留存）：").strip() or "引流"

    try:
        sub_rate = float(input("补贴率（0.15 = 15%）：").strip() or "0.15")
    except ValueError:
        sub_rate = 0.15

    try:
        orders = int(input("预期单量：").strip() or "5000")
    except ValueError:
        orders = 5000

    try:
        aov = float(input("客单价（元）：").strip() or "35")
    except ValueError:
        aov = 35

    try:
        new_ratio = float(input("新用户占比（0.3 = 30%）：").strip() or "0.3")
    except ValueError:
        new_ratio = 0.3

    roi_calc = PromotionROI(
        promotion_type=promo_type,
        subsidy_rate=sub_rate,
        expected_orders=orders,
        avg_order_value=aov,
        new_user_ratio=new_ratio,
    )

    result = roi_calc.calculate()

    print(f"\n{'='*55}")
    print(f"促销ROI分析报告（{result['活动类型']}）")
    print(f"{'='*55}")
    print(f"\n基础数据：")
    print(f"  预期GMV：{result['预期GMV']}")
    print(f"  补贴率：{result['补贴率']}")
    print(f"  补贴成本：{result['补贴成本']}")

    print(f"\n新用户分析：")
    print(f"  {result['新用户数']}")
    print(f"  {result['新用户获取成本']}")

    print(f"\nROI分析：")
    print(f"  ROI估算：{result['ROI估算']}")
    print(f"  盈亏判断：{result['盈亏判断']}")

    print(f"\n优化建议：")
    for s in result['优化建议']:
        print(f"  {s}")


if __name__ == "__main__":
    run()
```

### Tool 2: 活动话术生成器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动话术生成器
输入：活动类型/商品名称/价格/活动时间
输出：团长发群文案 + 朋友圈文案 + 私聊话术
"""


def generate_promotion_copy(
    activity_type: str,
    product_name: str,
    original_price: float,
    promo_price: float,
    start_time: str,
    end_time: str,
    limit_per_person: int = 0,
    product_image_tip: str = "",
) -> Dict:
    """
    生成促销文案

    Args:
        activity_type: 活动类型（引流/爆款/满减/节日）
        product_name: 商品名称
        original_price: 原价
        promo_price: 促销价
        start_time: 开始时间
        end_time: 结束时间
        limit_per_person: 每人限购数量
        product_image_tip: 图片拍摄建议
    """
    discount_pct = (1 - promo_price / original_price) * 100
    savings = original_price - promo_price

    # 预热文案（活动前一天）
    preheat_copy = f"""🔥【{product_name}】明日开抢！

⏰明日 {start_time} 准时上线
💰原价¥{original_price} → 限时¥{promo_price}
📉直降 {discount_pct:.0f}%（省¥{savings:.1f}）
"""

    if limit_per_person > 0:
        preheat_copy += f"⛔每人限购 {limit_per_person} 份，别说我没提醒你！\n"

    preheat_copy += f"""
📦图片参考：[上传实拍图]
📍下单：点击群里链接即可

明早闹钟调好，手慢无！"""

    # 正式活动文案（活动当天）
    live_copy = f"""🔥🔥🔥 {product_name} 来了！

💰活动价：¥{promo_price}
📉比原价省：¥{savings:.1f}（{discount_pct:.0f}折）
⏰时间：{start_time} - {end_time}
"""

    if limit_per_person > 0:
        live_copy += f"⛔每人限抢 {limit_per_person} 份\n"

    live_copy += f"""
【下单方式】
点击链接 → 选择商品 → 提交订单

📦提货时间：{end_time} 后到团点自提
💬有问题群里找我

赶紧下单，手慢无！"""

    # 朋友圈文案（简洁吸睛）
    moments_copy = f"""{product_name}
{start_time} 限时 ¥{promo_price}！
省 ¥{savings:.0f}，点击链接抢购👇"""

    # 截单后催单文案
    reminder_copies = [
        f"🔥 {product_name} 还剩最后 X 份！要的赶紧下单！",
        f"⏰ {product_name} 活动还剩 30 分钟！还没下单的抓紧！",
        f"📢 还没抢到的吗？{product_name} 库存还充足，赶紧冲！",
    ]

    # 售罄文案
    sold_out_copy = f"""售罄了！

{product_name}已抢完，感谢大家支持！
下一波活动明天见🔥

[附图：战报截图/下单排行榜]"""

    # 图片拍摄建议
    image_tips = {
        "生鲜": "光线充足，实拍图，标注规格（如：约500g/份）",
        "水果": "颜色鲜艳，背景简洁，标注产地和规格",
        "标品": "正面照，包装完整，展示促销标签",
        "节日": "营造节日氛围，摆拍+实物图",
    }
    default_tip = product_image_tip or "清晰明亮，实拍为主，避免过度美化"

    return {
        "预热文案（活动前一天）": preheat_copy,
        "正式活动文案（发群）": live_copy,
        "朋友圈文案": moments_copy,
        "截单催单文案": reminder_copies,
        "售罄/结束文案": sold_out_copy,
        "图片拍摄建议": default_tip,
        "省钱信息": {
            "原价": f"¥{original_price}",
            "促销价": f"¥{promo_price}",
            "折扣": f"{discount_pct:.0f}折",
            "节省": f"¥{savings:.1f}",
        },
    }


def run():
    print("=" * 55)
    print("活动话术生成器")
    print("=" * 55)

    product = input("商品名称：").strip() or "土鸡蛋30枚"
    orig_price = float(input("原价（元）：").strip() or "32") or 32
    promo_price = float(input("促销价（元）：").strip() or "19.9") or 19.9
    start = input("开始时间（如10:00）：").strip() or "10:00"
    end = input("结束时间（如18:00）：").strip() or "18:00"
    limit = int(input("每人限购（0=不限）：").strip() or "2") or 2

    result = generate_promotion_copy(
        activity_type="爆款",
        product_name=product,
        original_price=orig_price,
        promo_price=promo_price,
        start_time=start,
        end_time=end,
        limit_per_person=limit,
    )

    print(f"\n{'='*55}")
    print("【预热文案】活动前一天发")
    print(f"{'='*55}")
    print(result["预热文案（活动前一天）"])

    print(f"\n{'='*55}")
    print("【正式活动文案】活动当天发群")
    print(f"{'='*55}")
    print(result["正式活动文案（发群）"])

    print(f"\n{'='*55}")
    print("【朋友圈文案】")
    print(f"{'='*55}")
    print(result["朋友圈文案"])

    print(f"\n{'='*55}")
    print("【截单催单文案】")
    print(f"{'='*55}")
    for i, c in enumerate(result["截单催单文案"], 1):
        print(f"{i}. {c}")

    print(f"\n{'='*55}")
    print("【售罄文案】")
    print(f"{'='*55}")
    print(result["售罄/结束文案"])

    print(f"\n图片拍摄建议：{result['图片拍摄建议']}")


if __name__ == "__main__":
    run()
```

### Tool 3: 大促战报生成器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大促战报生成器
输入：大促期间各维度数据
输出：可视化战报文本 + 团长激励榜单 + 复盘分析
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PromotionData:
    """大促数据"""
    activity_name: str
    duration_days: int
    total_gmv: float
    total_orders: int
    new_users: int
    active_leaders: int
    avg_order_value: float
    top_sku: str
    top_sku_orders: int
    complaint_count: int
    previous_gmv: float = 0.0  # 上期数据对比


def generate_war_report(data: PromotionData) -> Dict:
    """生成大促战报"""

    # GMV增长
    if data.previous_gmv > 0:
        gmv_growth = (data.total_gmv - data.previous_gmv) / data.previous_gmv * 100
        gmv_vs = f"+{gmv_growth:.1f}% vs 上期"
    else:
        gmv_vs = "（无上期数据）"

    # 核心指标
    metrics = {
        "活动名称": data.activity_name,
        "活动天数": f"{data.duration_days} 天",
        "总GMV": f"¥{data.total_gmv:,.0f}",
        "总订单量": f"{data.total_orders:,} 单",
        "日均GMV": f"¥{data.total_gmv/data.duration_days:,.0f}",
        "日均订单": f"{data.total_orders//data.duration_days:,} 单",
        "新用户数": f"{data.new_users:,} 人",
        "活跃团长数": f"{data.active_leaders} 人",
        "客单价": f"¥{data.avg_order_value:.1f}",
        "新用户占比": f"{data.new_users/data.total_orders*100:.1f}%",
        "GMV增长": gmv_vs,
    }

    # 亮点挖掘
    highlights = []
    if data.avg_order_value > 50:
        highlights.append(f"✅ 客单价 ¥{data.avg_order_value:.1f}，超过行业均值 35-40 元")
    if data.new_users / data.total_orders > 0.3:
        highlights.append(f"✅ 新用户占比 {data.new_users/data.total_orders*100:.1f}%，拉新效果显著")
    if data.complaint_count < 10:
        highlights.append(f"✅ 客诉仅 {data.complaint_count} 单，用户体验良好")

    # 改进建议
    suggestions = []
    if data.avg_order_value < 40:
        suggestions.append("⚠️ 客单价偏低，建议下一期增加组合套餐/满减活动")
    if data.new_users / data.total_orders < 0.15:
        suggestions.append("⚠️ 新用户占比偏低，建议加大拉新券力度")
    if data.complaint_count > 20:
        suggestions.append("⚠️ 客诉量偏高，需专项排查原因")

    # 团长榜单（模拟数据）
    leader_board = [
        f"[第1名] 张团长 — GMV ¥{data.total_gmv*0.03:.0f}（{int(data.total_orders*0.028)}单）",
        f"[第2名] 李团长 — GMV ¥{data.total_gmv*0.025:.0f}（{int(data.total_orders*0.023)}单）",
        f"[第3名] 王团长 — GMV ¥{data.total_gmv*0.022:.0f}（{int(data.total_orders*0.020)}单）",
    ]

    # 战报总结
    summary = f"""
{data.activity_name}战报总结

📊 核心数据：
  总GMV：{metrics['总GMV']} {metrics['GMV增长']}
  总订单：{metrics['总订单量']}
  日均GMV：{metrics['日均GMV']}
  客单价：{metrics['客单价']}
  新用户：{metrics['新用户数']}（{metrics['新用户占比']}）

🏆 团长TOP3：
{chr(10).join(leader_board)}

🔥 亮点：
{chr(10).join(['  ' + h for h in highlights]) if highlights else '  本期表现良好'}

📝 下一期改进：
{chr(10).join(['  ' + s for s in suggestions]) if suggestions else '  继续保持'}

感谢各位团长的辛勤付出！下一期活动见！
"""

    return {
        "核心指标": metrics,
        "亮点": highlights,
        "改进建议": suggestions,
        "团长榜单": leader_board,
        "完整战报": summary,
    }


def run():
    print("=" * 55)
    print("大促战报生成器")
    print("=" * 55)
    print("（演示模式：输入年货节模拟数据）\n")

    data = PromotionData(
        activity_name="2024年年货节",
        duration_days=20,
        total_gmv=8_500_000,
        total_orders=218_000,
        new_users=42_000,
        active_leaders=1_580,
        avg_order_value=39.0,
        top_sku="坚果礼盒1800g",
        top_sku_orders=8_800,
        complaint_count=12,
        previous_gmv=6_200_000,
    )

    result = generate_war_report(data)

    print(result["完整战报"])
    print("\n亮点：")
    for h in result["亮点"]:
        print(f"  {h}")
    print("\n改进建议：")
    for s in result["改进建议"]:
        print(f"  {s}")


if __name__ == "__main__":
    run()
```

---

## 案例库

### 案例1：多多买菜"1分钱水果"拉新失败复盘

```
背景：2020年多多买菜进入湖南市场，用1分钱水果拉新

活动设计：
  商品：进口香蕉/苹果/橙子（成本约3-5元）
  价格：0.01元（平台全额补贴）
  目标：拉新10万个用户

结果（低于预期）：
  到团率：68%（用户下单后不来提货）
  复购率：仅 8%（拉来的用户没有转化为常客）
  实际获客成本：¥42/人（目标 ¥8/人，超出 5 倍）

失败原因分析：
  1. 用户质量问题：吸引来的都是"薅羊毛"用户，不是真实消费者
  2. 无后续承接：1分钱商品之后没有留存策略，用户用完就走
  3. 团长积极性受损：爆单之后发现大量用户不来提货，白忙一场
  4. 竞争对手反制：兴盛优选推出"0.5元同款"，用户被分流

改进方向：
  → 拉新补贴改为"首单满19减10"（筛选真实消费者）
  → 拉新和留存结合：新用户发连续3张券（7天/14天/30天各一张）
  → 设定团长拉新门槛：拉的必须是"有效新用户"（完成首单+复购1次）
```

### 案例1b：某平台新人券被黑产薅羊毛应急处置

```
背景：某平台新人券上线2小时被使用5000张，80%是同一地址

异常信号识别：
  → 短时间大量使用：2小时内5000张，远超日常均值200张/小时
  → 地址集中度异常：80%同一地址（正常平台<5%）
  → 设备指纹重复：同一设备多次领取
  → 行为特征：整点同步下单，无浏览轨迹

应急处置流程（P0级响应）：

Step 1：立即识别（0-30分钟）
  → 运营后台告警触发，自动冻结可疑账户
  → 数据团队导出异常订单明细（地址/手机/设备指纹）
  → 定义黑产特征标签：同地址≥3单 / 同设备≥2次 / 整点同步

Step 2：分级处置（30分钟-2小时）
  → 确认黑产（证据确凿）：永久封禁账户 + 回收已发优惠券
  → 可疑账户（特征匹配但未确凿）：限制优惠券使用（限1张/账户）
  → 已发货订单：拦截物流（未发货）或联系团长拦截（已发货到团点）

Step 3：补偿与公关（2-24小时）
  → 已使用优惠券的正常用户：不做回收（避免客诉）
  → 损失追缴：通过法律途径追缴（金额>3000元构成诈骗罪）
  → 内部复盘：排查漏洞，修复领券链路

Step 4：规则升级（24小时后）
  → 新人券改为"需完成实名认证"方可使用
  → 引入风控系统：设备指纹+行为分析+地址聚类
  → 设置单人单日领券上限（最多3张）
  → 建立黑产名单库，与供应商/团长黑名单联动

损失估算：
  → 5000张券 × ¥10面值 = ¥50,000
  → 其中黑产薅羊毛约4000张 = ¥40,000
  → 追回可能性：<10%（黑产多使用虚假信息）

核心教训：
  → 新人券上线必须配套风控系统，不能只靠人工监控
  → 优惠券发放前必须做"压力测试"：模拟极端领取场景
  → 发现异常后要"快、准、狠"处置，不能犹豫
  → 预防大于止损：事前风控成本 << 事后追缴成本
```

### 案例2：美团优选"年货节"爆品打造全流程

```
成功点：从选品到预热到执行，全链路精细化运营

年货节选品策略：
  引流款：土鸡蛋（市场价¥18 → ¥9.9，补贴50%）
  冲量款：坚果礼盒/食用油/大米（家常必备）
  利润款：白酒/茶叶/海参（礼盒装，高客单价）

预热节奏（T-7至T-1）：
  T-7：确定爆品，供应商备货120%目标量
  T-5：团长预热文案发出，开始接龙
  T-3：首日限量公布，制造稀缺感
  T-1：最后预告，团长群发红包激活

执行数据（年货节7天）：
  引流款土鸡蛋：售出 18,000 份（到团率 96%）
  坚果礼盒：售出 8,500 份（GMV ¥680,000）
  总GMV：¥2,800,000（日均 ¥400,000）
  客单价：¥52（高于日常35元，提升49%）

成功关键：
  1. 选品精准：年货节送礼场景明确，礼盒装高客单价
  2. 预热充分：7天预热期，团长充分沟通用户需求
  3. 供应链稳定：供应商提前备货，无断货情况
  4. 执行到位：配送时效达标，用户体验好
```

### 案例3：兴盛优选"端午粽子"本地化营销

```
成功点：深耕湖南本地口味，差异化竞争

背景：
  端午节是社区团购最重要的节日之一
  全国性平台主打通用款粽子（豆沙/鲜肉）
  兴盛选择做湖南特色：腊肉粽子/碱水粽子

差异化选品：
  兴盛：湖南本地工厂代工，腊肉粽/碱水粽（湖南人最爱）
  美团/多多：全国通用款（品牌粽子，如五芳斋）

定价策略：
  腊肉粽：¥8.8/个（超市同款¥12）
  碱水粽：¥3.8/个（超市同款¥5）
  组合装（4腊肉+4碱水）：¥39.9

数据效果（端午节3天）：
  湖南市场粽子GMV：¥1,200,000
  兴盛市占率：端午节湖南粽子市场 65%
  用户反馈：湖南用户好评如潮（"终于买到正宗的腊肉粽"）

成功逻辑：
  → 本地化选品：切中湖南用户的口味偏好
  → 差异化竞争：不和全国平台正面打价格战
  → 供应链优势：本地工厂代工，成本比品牌更低
  → 团长共鸣：湖南团长自发推荐，配合度高
```

### 案例4：橙心优选"烧钱换规模"失败根源

```
背景：橙心优选（滴滴）2020年进入社区团购，最高日均GMV过亿

失败的核心原因：
  1. 纯价格战，无差异化
    → 橙心和多多买菜的打法完全一样：低价拉新 → 补贴维持 → 规模变现
    → 但多多的供应链成本比橙心低，橙心补贴不起
    → 结果：每单亏损比多多高 2-3 倍

  2. 供应链短板致命
    → 滴滴没有零售/电商基因，供应链全靠外部合作
    → 美团有配送体系，多多有农产品供应链
    → 橙心什么都没有，只能烧钱买

  3. 人员成本高，效率低
    → BD团队全部自建（美团/多多早期用外包）
    → 团长全部自签（美团/多多后来也这样做）
    → 人员成本比对手高 30-40%

最终结局：
  橙心优选：2021年7月关停（1年半烧光约300亿）
  多多买菜：存活，2023年盈亏平衡
  美团优选：存活，成为行业第二

教训总结：
  → 补贴只是加速器，不是核心竞争力
  → 没有供应链优势的价格战 = 烧钱找死
  → 社区团购是持久战，烧钱撑不过对手就算输
```

---

## 附录：营销促销检查清单

```
大促活动健康检查：

□ 1. 选品：爆品是否满足"刚需/高频/标准化/供应链稳定"四要素？
□ 2. 定价：补贴率是否在预算范围内（ < 20% GMV）？
□ 3. 备货：供应商备货量是否为目标的 110-120%？
□ 4. 预热：活动前 3 天是否完成全量预热（团长群/APP推送）？
□ 5. 话术：团长话术是否符合平台规则（不得夸大/虚假宣传）？
□ 6. 配送：仓库/配送是否已确认可承接峰值单量？
□ 7. 客服：大促期间客服排班是否到位？
□ 8. 异常：是否已制定应急预案（断货/物流异常/客诉处理）？
□ 9. 数据：大促期间是否有实时数据监控（每小时 GMV 播报）？
□ 10. 复盘：大促结束后 7 天内是否完成复盘报告？

红线预警：
  → 爆品出现断货且 2 小时内无法补货 = 严重失误
  → 团长夸大宣传引发客诉 = 立即处理并公开澄清
  → 补贴被套利（刷单/虚假订单）= 立即停止活动，追责
  → 竞争对手价格更低导致用户流失 = 快速响应，但不要盲目跟进降价
```
