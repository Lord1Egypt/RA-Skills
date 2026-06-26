# Examples

5 个典型 case，按"难度 / 积分 / 耗时"排列。建议第一次用按 01 → 02 → 03 → 04 → 05 顺序看。

| # | 场景 | 命令风格 | 积分 | 耗时 | 难度 |
|---|---|---|---|---|---|
| [01](./01-generate-image.md) | 生一张猫图（最小路径）| `model with lib-nano-pro` | ≈14 | ≈60s | ⭐ |
| [02](./02-generate-video.md) | 生一段 5s 视频 | `model with seedance-2.0-vip` | ≈135 | 5-8 min | ⭐⭐ |
| [03](./03-edit-with-reference.md) | 把纸船换成爱心（局部编辑）| `upload` + `edit mark` | ≈14-20 | ≈90s | ⭐⭐ |
| [04](./04-character-to-video.md) | 角色三视图 → 首帧图生视频 | `flow character_views` + `flow keyframe_to_video` + `edit camera` | ≈150 | ≈10 min | ⭐⭐⭐ |
| [05](./05-batch-images.md) | 并发批量 10 张图 + HTML 报告 | `batch` + `export html` | ≈140 | ≈2 min | ⭐⭐ |

## 跑这些 example 前

1. **设置 API key**：
   ```bash
   export LIBTV_ACCESS_KEY=your_key_here
   ```
   key 从 [LibTV 用户中心](https://www.liblib.tv) 获取（个人设置 → API / 开发者）。

2. **dry-run 先看 prompt**：每个 case 第一步都有 `--dry-run`，跑完确认 prompt 没问题再去掉它正式生成。可以省下大量积分。

3. **从最便宜的 01 开始**：14 积分一张图，跑通了再去 02。
