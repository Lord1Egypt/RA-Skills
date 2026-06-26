# Example 02：用 Seedance 生一段 5 秒视频

**积分消耗**：≈135 · **耗时**：5-8 min · **难度**：⭐⭐

文生视频，指定模型 + 参数。

## 用户需求

「用 Seedance 2.0 VIP 生成一段 5 秒、16:9、720P 的视频：黄昏草原上一只白马奔跑」

## 命令链

```bash
export LIBTV_ACCESS_KEY=your_key_here

# 1. 预览（强烈建议先 dry-run 检查参数是否传对）
python3 scripts/libtv.py model with seedance-2.0-vip \
  "黄昏草原上一只白马奔跑，阳光金黄，长鬃飘动" \
  --ratio 16:9 --resolution 720P --duration 5s --count "1个" \
  --dry-run

# 2. 真实生成
RESULT=$(python3 scripts/libtv.py model with seedance-2.0-vip \
  "黄昏草原上一只白马奔跑，阳光金黄，长鬃飘动" \
  --ratio 16:9 --resolution 720P --duration 5s --count "1个")
SID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['sessionId'])")

# 3. 视频生成慢，用 monitor 看进度（15s 间隔）
python3 scripts/libtv.py monitor "$SID" --poll --interval 15 --extract-urls --timeout 600

# 4. 下载
python3 scripts/libtv.py download "$SID" --output-dir ~/Downloads/horse --prefix horse

# 5. 加到会话历史（方便以后用 history list 找到）
python3 scripts/libtv.py history add "$SID" --desc "Seedance 白马奔跑 5s"
```

## 预期输出

- `~/Downloads/horse/horse_01.mp4`（约 5 秒、16:9、720P）
- 项目画布链接（可在 LibTV 网页上分享/编辑）

## 模型选择参考

| 想要 | 推荐模型 | 参数 |
|---|---|---|
| 快速预览 / 测试 prompt | `seedance-2.0-vip` | 720P, 5s |
| 写实人像、动作连贯 | `kling-3.0` | 1080P, 5-10s |
| 长视频、高质量 | `kling-o3` | 1080P, 10s |
| 多镜头、复杂场景 | `wan-2.6` | 1080P, 任意 |

用 `python3 scripts/libtv.py model list --kind video` 查全部视频模型。
