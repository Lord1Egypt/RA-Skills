# 昆明示例配置 — house-skills-kit

这是 house-skills-kit 的第一个完整 worked example：把一套真实业务 know-how（昆明城区板块认知 + 带看转化话术）通过 `brand.yaml` 注入通用骨架，**不改一行模板**。

## 文件

- `kunming.buy.yaml` — 昆明买房顾问的完整品牌配置
- `references/plates.md` — 昆明城区板块速查（渲染时被 references 注入 SKILL.md 末尾）

## 生成

```bash
python3 render.py --config examples/kunming/kunming.buy.yaml --out output/
# → output/kunming-buy/SKILL.md + manifest.json
```

## 教学点

1. **know-how 放配置，不放模板**：板块知识、话术全部在 yaml 与 references 里，模板保持行业通用。
2. **换城市 = 换配置**：接其他城市/品牌时复制本目录改内容即可。
3. **商业 know-how 与开源骨架分离**：骨架开源，深度 know-how 配置由品牌方自持。
