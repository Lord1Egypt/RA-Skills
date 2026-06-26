# 猫眼 CLI 与 Skill 示例

## 输出格式

所有子命令输出 **JSON**（带 `ok`、业务字段等），便于管道或程序解析。

## CLI 示例

（从项目根目录执行，脚本路径为 `skills/maoyan-cli/scripts/maoyan_cli.py`）

```bash
# 城市：查北京
python skills/maoyan-cli/scripts/maoyan_cli.py cities -q 北京

# 筛选条件：北京
python skills/maoyan-cli/scripts/maoyan_cli.py filter 1

# 影院列表：北京、前 5 条（建议加 --lat --lng 用户位置以便按距离排序）
python skills/maoyan-cli/scripts/maoyan_cli.py cinemas 1 --limit 5
python skills/maoyan-cli/scripts/maoyan_cli.py cinemas 1 --lat 39.97 --lng 116.32 --limit 5

# 排片：影院 41671
python skills/maoyan-cli/scripts/maoyan_cli.py shows 41671 1

# 搜索电影（得 movieId）
python skills/maoyan-cli/scripts/maoyan_cli.py search 惊蛰无声 1

# 某电影的上映影院（建议加 --lat --lng 用户位置以便按距离排序）
python skills/maoyan-cli/scripts/maoyan_cli.py movie-cinemas 1563473 1 --limit 10

# 电影详情（从详情页 HTML 解析片名、评分、简介、类型、主演等）
python skills/maoyan-cli/scripts/maoyan_cli.py detail 1565122 1
python skills/maoyan-cli/scripts/maoyan_cli.py detail 1565122 1 --cinemaId 41671 --lat 39.972527 --lng 116.320122


## 在 Skill 中的使用示例

1. **「完美影城排片」**  
   → 先 `cinemas 1`（有用户位置可加 `--lat --lng`）找到「完美世界影城」的 cinemaId（如 41671），再 `shows 41671 1`。

2. **「北京海淀有哪些影院」**  
   → `filter 1` 看 district 下海淀区对应 id；`cinemas 1 [--lat --lng] --districtId <id>` 或 `cinemas 1 [--lat --lng]` 后按地址筛选；建议根据用户位置传经纬度。

3. **「上海某影院今天排片」**  
   → `cities -q 上海` 得 ci=10；`cinemas 10 [--lat --lng]` 得影院列表；选 cinemaId 后 `shows <cinemaId> 10`。建议根据用户位置传经纬度。

4. **仅已知影院 ID**  
   → 直接 `shows <cinemaId> [ci]`。

5. **「某电影在哪能看」**  
   → `search <片名> [ci]` 取 movies[0].id 作为 movieId，再 `movie-cinemas <movieId> [ci] [--lat --lng] [--day YYYY-MM-DD]`。建议根据用户位置传经纬度。

6. **「某部电影的剧情、评分、主演」**  
   → `search <片名> [ci]` 得 movieId，再 `detail <movieId> [ci]`；可选 `--cinemaId`、`--lat`、`--lng` 与详情页 URL 一致。
