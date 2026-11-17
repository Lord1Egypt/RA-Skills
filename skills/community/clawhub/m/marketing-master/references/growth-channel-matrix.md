# 增长渠道矩阵 Playbook（growth-channel-matrix）

> 适用技能：`seo-auditor` / `copywriting-pro` / `landing-page-builder` / `content-strategist` / `paid-ads`。
> 本 playbook 解决「该用哪个技能、按什么顺序」的问题，并给出可运行的 SEO/文案/落地页代码。

## 1. 何时使用哪个技能（选择矩阵）

| 业务目标 | 首选技能 | 关键动作 | 输出 |
|----------|----------|----------|------|
| 让更多人搜到（获取流量） | `seo-auditor` | 关键词研究、技术 SEO、竞品 | 关键词表 + 技术诊断 |
| 把访客变成读者/用户（内容） | `content-strategist` | 主题集群、编辑日历 | 内容计划 |
| 让文案更会卖（转化） | `copywriting-pro` | PAS/AIDA/StoryBrand | 着陆页/广告文案 |
| 让页面接得住流量（承接） | `landing-page-builder` | 结构、视觉层次、CTA | 高转化页面 |
| 用预算放大已验证的转化（付费） | `paid-ads` | 平台选型、账户结构、素材工厂 | 投放计划 + 素材批次 |

**黄金顺序**：先 `seo-auditor` 找机会 → `content-strategist` 排内容 → `copywriting-pro` 写词 → `landing-page-builder` 落地。倒序（先写落地页再补 SEO）往往流量接不住。

## 2. 决策树：从哪开始

```
开始
├─ 站点还没人搜到？
│   └─ 是 → seo-auditor：先做关键词 + 技术 SEO 健康检查
├─ 有流量但无内容沉淀？
│   └─ 是 → content-strategist：建主题集群 + 编辑日历
├─ 有内容但转化差？
│   ├─ 文案弱 → copywriting-pro：换 PAS/AIDA 框架
│   └─ 页面承接弱 → landing-page-builder：重做结构与 CTA
└─ 要发新品/活动？
    └─ 是 → 并行：copywriting-pro 写文案 + landing-page-builder 搭页
```

## 3. 具体命令与代码

### 3.1 SEO 审计工作流（seo-auditor）

```bash
# 1) 关键词研究：围绕核心词做聚类与意图映射
#    输入："项目管理软件" → 输出 信息型/商业型/交易型 三组
# 2) 技术 SEO 诊断：爬取站点，检查
#    - 标题/描述缺失或重复
#    - 无结构化数据（JSON-LD）
#    - 移动端可访问性、页面速度
# 3) 竞品分析：反向链接、主题覆盖、精选摘要差距
# 4) 输出：技术诊断报告 + 关键词机会表 + 行动计划
```

### 3.2 关键词按意图聚类（可运行）

可运行版本见 [scripts/keyword_cluster.py](../scripts/keyword_cluster.py)，支持 `--pair "关键词" "意图"` 或 STDIN 多行：

```python
# keyword_cluster.py —— 运行: python3 scripts/keyword_cluster.py
KW = {
    "项目管理软件": "商业", "好用的项目管理工具": "商业",
    "项目管理是什么": "信息", "如何做项目排期": "信息",
    "项目管理软件价格": "交易", "项目管理软件免费版": "交易",
}

def cluster(kws):
    out = {}
    for k, intent in kws.items():
        out.setdefault(intent, []).append(k)
    return out

if __name__ == "__main__":
    for intent, words in cluster(KW).items():
        print(f"[{intent}] " + " / ".join(words))
```

### 3.3 文案框架选择对照

| 框架 | 最适用 | 结构 |
|------|--------|------|
| PAS | 痛点明确的转化页 | Problem 问题 → Agitate 激化 → Solution 解决 |
| AIDA | 广告/短文案 | Attention 注意 → Interest 兴趣 → Desire 渴望 → Action 行动 |
| StoryBrand | 品牌/产品叙事 | 客户是主角，品牌是向导，指明计划与成功 |

选择规则：解决「痛」用 PAS；抢注意力用 AIDA；讲「为什么是你」用 StoryBrand。

### 3.4 着陆页结构骨架（landing-page-builder）

```html
<!-- 高转化结构：Hero → 价值主张 → 功能 → 社会证明 → CTA -->
<main>
  <section class="hero">
    <h1>一句话说清你帮用户解决什么</h1>
    <p class="sub">具体可感知的价值主张</p>
    <a class="cta" href="#signup">免费开始</a>
  </section>
  <section class="value">3 个核心卖点（图标 + 短句）</section>
  <section class="features">功能展示，每屏一件事</section>
  <section class="proof">用户证言 / 数据 / 客户 logo</section>
  <section id="signup" class="cta-final">再次 CTA + 紧迫感</section>
</main>
```

响应式要点：Hero 在 375px 不溢出；CTA 按钮触控区 ≥ 44px；证据区在移动端单列堆叠。

## 4. 典型陷阱与规避

| 陷阱 | 后果 | 规避 |
|------|------|------|
| 先搭落地页再补 SEO | 有页无流量 | 按黄金顺序：SEO→内容→文案→落地 |
| 文案堆砌关键词 | 读感差、被降权 | 关键词自然融入，框架优先 |
| 着陆页放多个 CTA | 用户不知所措 | 单页主 CTA 唯一且重复出现 |
| 技术 SEO 长期不查 | 爬取/索引问题 | 季度跑诊断 |
| 把社媒/SEM 当本职 | 范围蔓延 | 免费流量链路不代替付费；投放走 `paid-ads`，且先验证转化承接再放大 |
| 文案脱离产品定位 | 转化虚高不留存 | 先澄清定位再写 |

## 5. 检查清单

- [ ] 已用 `seo-auditor` 产出关键词机会表与技术诊断
- [ ] 关键词已按意图（信息/商业/交易）聚类
- [ ] 内容规划与主题集群已对齐关键词
- [ ] 文案选定框架（PAS/AIDA/StoryBrand）且贴合场景
- [ ] 着陆页含 Hero→价值→功能→证明→CTA 五段
- [ ] 主 CTA 唯一、可见、触控区 ≥ 44px
- [ ] 页面在 375/768/1280 三档无溢出
- [ ] 结构化数据（JSON-LD）已部署
- [ ] 付费投放单独走 `paid-ads`，未与免费流量链路混排
- [ ] 全链路顺序为 SEO→内容→文案→落地，无倒挂

## 6. 与路由的衔接

本篇只负责「各能力怎么串、先做哪个、代价是什么」。具体写法与命令去对应子技能：

- 关键词研究、技术 SEO 诊断、竞品与 SERP 分析 → [skills/seo-auditor](../skills/seo-auditor/SKILL.md)
- PAS / AIDA / StoryBrand 框架落成具体文案 → [skills/copywriting-pro](../skills/copywriting-pro/SKILL.md)
- 五段式骨架落成实际页面（视觉层次、响应式、CTA） → [skills/landing-page-builder](../skills/landing-page-builder/SKILL.md)
- 主题集群与编辑日历排期 → [skills/content-strategist](../skills/content-strategist/SKILL.md)，方法论见 [references/content-strategy-playbook.md](content-strategy-playbook.md)
- 付费流量采买、账户结构与素材迭代 → [skills/paid-ads](../skills/paid-ads/SKILL.md)
- 关键词聚类与内容衰减的确定性计算 → [scripts/keyword_cluster.py](../scripts/keyword_cluster.py)、[scripts/decay_score.py](../scripts/decay_score.py)
