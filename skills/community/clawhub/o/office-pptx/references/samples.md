# 对照样张（气质，不是抄稿）

给评测和 Agent 看「不像默认 AI 模板」。**抄的是版式节奏和 theme，不是文案。** 用户没点名某气质时，用判别后的场景选一行，勿六套轮换炫技。

JSON 在 SkillHub 包 `samples/*.json`（仓库 `scripts/release/office-pptx/samples/`）。本机出可打开文件：

```powershell
zagens-office write pptx --path deliverables/consulting-brief.pptx --input-file samples/consulting-brief.json
# 一次六份（默认写到 target/office-pptx-samples/）：
# pwsh scripts/release/generate-office-pptx-samples.ps1
```

样张馆用**整份 write** 是为了可复现；Agent 做正式精修仍走骨架 + 逐页 `upsert_slide`。用 PowerPoint / WPS 打开验收，不要只看 JSON。

## 六份对照

| 文件 | theme | 气质 | 页节奏（6 页） | 用来证伪 |
|------|-------|------|----------------|----------|
| `consulting-brief.json` | `consulting` | Navy 咨询 | 封面 → 判断 → 证据 KPI → 路径 SmartArt → 图 → 下一步 | 通栏色条、标题下划线、金红大面积、全篇 bullets |
| `civic-report.json` | `civic` | 政务汇报 | 封面 → 总判断 → 三项进展 → 风险 → 安排 → 请示 | 冷暗红乱配、印章竖排、营销撞色 |
| `academic-defense.json` | `academic` | 开题/答辩 | 封面 → 问题 → 方法 → 预期 → 进度 → 文献 | 高饱和插画风、紫粉大色块、空页 |
| `data-brief.json` | `light` | 数据简报 | 封面 → 四 KPI → 柱图 → 趋势 → 渠道 → 行动 | 彩虹系列、把整表塞进 PPT、无结论标题 |
| `dark-product.json` | `dark` | 深色发布 | 封面 → 一句话 → 三能力 → 流程 → 对比 → CTA | 浅字浅底、装饰渐变堆砌、每页三卡重复 |
| `minimal-grid.json` | `minimal` | 克制网格 | 封面（大留白）→ 原则 → 2×2 → 应用 → 边界 → 结束 | 奶油底、默认蓝、卡片描边当装饰 |

## 选用规则

1. 路演 / B2B / 咨询交付 → consulting。政务 / 国企 → civic。答辩 / 教研（非课件课型）→ academic。周度数字会 → data。产品发布 / Demo → dark。品牌手册 / 设计向 → minimal。
2. 课件课型仍走 `office-kejian`（`academic`），不要用本表代替课型。
3. 相邻页布局必须错开：有 KPI 的下一页不要再三卡；有图的下一页用流程或纯结论。
4. 样张文案是虚构场景，**不要**写进客户稿。

## 打开后应看到

- 无通栏顶栏 / 底栏 / 标题下划线（`title_style.engine:false`）。
- 每页一个主论点；高潮页（KPI / 图 / SmartArt）约 2/6。
- `preflight` / `view svg` 只核 bbox。气质（咨询封面深底、政务红金、学术密不空、数据有图、深色对比、极简留白）必须 **打开 .pptx** 才看得到。
