# Mind Map Skill Examples

## Example 1: Free mode with inline markdown

Command:

```bash
python mind_map/scripts/run_mind_map.py --layout free --input "# 项目计划\n## 目标\n- 增长\n- 降本" --filename demo_free --output-dir mind_map_output
```

## Example 2: Center mode with markdown file

Input file `test/input.md`:

```markdown
# 产品路线图
## 核心目标
- 提升留存
- 降低流失
```

Command:

```bash
python mind_map/scripts/run_mind_map.py --layout center --input test/input.md --filename demo_center --output-dir mind_map_output
```

## Example 3: Horizontal mode

Command:

```bash
python mind_map/scripts/run_mind_map.py --layout horizontal --input "# Architecture\n## API\n- Auth\n- Billing\n## Data\n- DB\n- Cache" --filename demo_horizontal --output-dir mind_map_output

If your skill directory is named `mind-map-skill`, replace `mind_map` with `mind-map-skill` in command paths.
```

By default, outputs are created under `mind_map_output/YYYY-MM-DD/`.
Add `--flat-output` if you want files directly under `mind_map_output/`.

## Project metadata

- Author: [@sawyer-shi](https://github.com/sawyer-shi)
- Email: sawyer36@foxmail.com
