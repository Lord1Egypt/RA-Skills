# 示例素材

直接可用的 brand kit / character / learned preset / 剧本，导入即用。

## 文件清单

| 文件 | 类型 | 用途 |
|------|------|------|
| `brand_kit-song_tea.json` | 品牌套件 | 宋韵东方茶饮品牌示例 |
| `character-silver_mecha.json` | 角色卡 | 银发机甲少女（演示跨调用一致性） |
| `learned_preset-fresh_film.json` | 学习预设 | 清新胶片风（日杂感） |
| `storyboard-cat_rainy_night.txt` | 剧本 | 一只猫的雨夜散步（6 帧） |
| `recipe-1-brand_kv.sh` | Bash 脚本 | RECIPES.md 食谱 1 的可运行版 |

## 导入方式

```bash
# Brand kit
cat examples/brand_kit-song_tea.json | scripts/brand_kit.py --import
scripts/brand_kit.py --show song_tea

# 角色卡
cat examples/character-silver_mecha.json | scripts/character.py --import
scripts/character.py --show silver_mecha

# Learned preset（直接复制到目录即可）
mkdir -p ~/.huo15/learned_presets
cp examples/learned_preset-fresh_film.json ~/.huo15/learned_presets/

# 用 learned preset 出图
scripts/enhance_prompt.py "咖啡馆窗边少女" -p "@fresh_film"

# 故事板
scripts/storyboard.py < examples/storyboard-cat_rainy_night.txt \
    -p 电影感 --scenes 6 --output ./renders/cat_rainy_night

# 完整食谱 1
bash examples/recipe-1-brand_kv.sh
```

## 自定义指南

复制示例文件改字段即可：

- **brand_kit**：改 `colors / fonts / keywords / forbidden / logo_description`
- **character**：改 `subject_description / preset / aspect / seed`
- **learned_preset**：建议用 `style_learn.py --name 你的风格 ref*.jpg` 自动生成，不要手写

## 反对的做法

❌ 手写 learned_preset.json — confidence 字段是 Claude 综合后的可信度，手写会失真
❌ 直接改示例文件 — 应该导入后用 `--update` 修改自己的副本
❌ 把 example 当生产数据 — 仅供参考，按业务场景重新建立
