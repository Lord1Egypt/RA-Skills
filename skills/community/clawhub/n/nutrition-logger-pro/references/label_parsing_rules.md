# 营养标签解析规则

## 来源优先级

1. `user_provided`：用户给出的是实际吃掉那份食物的总营养值。
2. `label_calculated`：用户给出每100g或每份标签，并给出吃掉的重量或份数。
3. `estimated`：用户没有给出营养值，使用常见食物估算。
4. `mixed`：同一 item 中部分字段来自用户，部分字段来自估算。

不要用低优先级数据覆盖高优先级数据。

## 总值

这些表达表示用户提供的是实际吃掉那份的总值：

- `这个面包180 kcal，蛋白质6g`
- `这盒酸奶 120 卡`
- `包装写热量 250 千卡`

处理方式：

- 直接写入对应字段。
- `source=user_provided`
- `confidence=high`
- 缺失字段可以留空；只有合理时才估算缺失字段，并把 `source` 改为 `mixed`。

## 每100g

这些表达表示需要按吃掉重量计算：

- `每100g 110 kcal，我吃了150g`
- `营养表每100g是110 kcal，蛋白质2g，碳水15g，脂肪4g`

计算：

- `实际值 = 标签值 * 吃掉克重 / 100`
- 调用 `nutrition_cli.py calculate-label`
- `source=label_calculated`
- `confidence=high`

## 每份

这些表达表示需要按份数计算：

- `每份220 kcal，我吃了2份`
- `一份蛋白质10g，我吃了半份`

计算：

- `实际值 = 每份值 * 吃掉份数`
- 调用 `nutrition_cli.py calculate-label`
- `source=label_calculated`
- `confidence=high`

## 字段映射

- `kcal`、`calories`、`卡`、`千卡`、`热量` -> `kcal`
- `protein`、`蛋白质` -> `protein_g`
- `carbs`、`carbohydrate`、`碳水`、`碳水化合物` -> `carbs_g`
- `fat`、`脂肪` -> `fat_g`
- `fiber`、`膳食纤维` -> `fiber_g`
- `sugar`、`糖` -> `sugar_g`
- `sodium`、`钠` -> `sodium_mg`
- `盐` -> 优先记录到 note；如明确需要，可按盐 1g 约等于钠 400mg 粗略换算，并说明是假设。

## 不确定场景

- 标签属于哪个食物不明确时，向用户确认。
- 餐里多个同名食物时，优先用 `entry_id` 修正；否则列候选项。
- 餐厅或超市熟食没有标签时，使用低置信度估算。
