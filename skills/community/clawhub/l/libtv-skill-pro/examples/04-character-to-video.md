# Example 04：角色三视图 → 首帧图生视频（多步链）

**积分消耗**：≈150 · **耗时**：≈10 min · **难度**：⭐⭐⭐

经典工作流：先做角色 IP 资产，再用其中一张作为视频首帧。

## 用户需求

「我要做一个穿汉服的赛博朋克少女角色，先出三视图，然后用正面图做首帧生成一段她在霓虹街道行走的 5 秒视频」

## 命令链

```bash
export LIBTV_ACCESS_KEY=your_key_here

# ─── 第一段：角色三视图 ───
STEP1=$(python3 scripts/libtv.py flow character_views \
  "穿汉服的赛博朋克少女，银发，红色机械义眼，唐风刺绣旗袍混搭金属护甲")
SID=$(echo "$STEP1" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['sessionId'])")
PROJECT=$(echo "$STEP1" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['projectUrl'])")

echo "角色生成中，画布：$PROJECT"
python3 scripts/libtv.py poll "$SID" --interval 8 --timeout 300

# 下载三视图
python3 scripts/libtv.py download "$SID" --output-dir ~/Downloads/character --prefix view
# 应该会拿到 view_01.png（正面）/ view_02.png（侧面）/ view_03.png（背面）

# ─── 第二段：上传正面图作为首帧 ───
UPLOAD=$(python3 scripts/libtv.py upload ~/Downloads/character/view_01.png)
FRAME_URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['url'])")

# ─── 第三段：首帧图生视频，在同一会话内（保持上下文）───
STEP3=$(python3 scripts/libtv.py flow keyframe_to_video \
  "角色在夜晚霓虹密布的街道上缓步前行，回头一瞥，环绕运镜" \
  --ref "$FRAME_URL" \
  --session-id "$SID")

# ─── 第四段：叠加运镜修饰器（强化运镜质量）───
python3 scripts/libtv.py edit camera \
  "环绕 + 微推镜头，希区柯克变焦在回眸瞬间" \
  --target "（上一条 keyframe_to_video 的生成视频）" \
  --session-id "$SID"

# ─── 第五段：等待 + 下载 ───
python3 scripts/libtv.py monitor "$SID" --poll --interval 15 --extract-urls --timeout 600
python3 scripts/libtv.py download "$SID" --output-dir ~/Downloads/character_video
```

## 这个 case 演示的能力

1. **预设流程入口** (`flow character_views`, `flow keyframe_to_video`)
2. **本地文件上传** (`upload`)
3. **会话上下文复用** (`--session-id`)
4. **修饰器叠加** (`edit camera`)
5. **轮询 + 下载** (`poll` / `monitor` / `download`)

## 简化版（不用 flow，直接用 model.py）

如果你想精确控制每步用什么模型：

```bash
# 角色用 Midjourney（美学风）
python3 scripts/libtv.py model with midjourney "穿汉服的赛博朋克少女三视图..." --ratio 16:9

# 视频用 Kling O3（高质量长视频）
python3 scripts/libtv.py model with kling-o3 "霓虹街道行走..." --ratio 16:9 --duration 10s
```
