# Sample Outputs

These excerpts show the v1.0 expected behavior: direction-first setup, a business-loop state file, a visual operating cockpit, localized workspace surfaces, and optional AI-image creative prompts.

## Interaction Output Structure

Every major operation includes:

- `User Navigation View` or `用户导航版`
- `Operating Navigation` or `经营导航条`
- `Operating Snapshot` or `经营快照`
- explicit workspace-boundary and persistence details
- explicit runtime status

## Chinese Workspace Surface

```text
北辰实验室/
  00-经营总盘.md
  01-创始人约束.md
  02-价值承诺与报价.md
  03-机会与成交管道.md
  04-产品与上线状态.md
  05-客户交付与回款.md
  阅读版/
    00-经营驾驶舱.html
    00-经营总盘.html
  视觉素材/
    business-loop.svg
    revenue-pipeline.svg
    ai-image-prompts.md
  产物/
  .opcos/state/current-state.json
```

## English Workspace Surface

```text
North Star Lab/
  00-operating-dashboard.md
  01-founder-constraints.md
  02-value-promise-and-pricing.md
  03-opportunity-and-revenue-pipeline.md
  04-product-and-launch-status.md
  05-delivery-and-cash-collection.md
  reading/
    00-operating-cockpit.html
    00-operating-dashboard.html
  visual-kit/
    business-loop.svg
    revenue-pipeline.svg
    ai-image-prompts.md
  artifacts/
  .opcos/state/current-state.json
```

## State Contract

The hidden state file lives at `.opcos/state/current-state.json` and keeps the founder oriented around the operating loop.

Core sections:

- `founder`
- `offer`
- `buyer`
- `pipeline`
- `product`
- `delivery`
- `cash`
- `learning`
- `assets`
- `risk`
- `decision`
- `visuals`

## Visual Reading Layer

The reading layer starts at:

```text
阅读版/00-经营驾驶舱.html
reading/00-operating-cockpit.html
```

The cockpit includes the business-loop SVG, revenue-pipeline SVG, current bottleneck, primary arena, shortest action, and links into the editable work surfaces.
