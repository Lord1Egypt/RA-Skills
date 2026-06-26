# Example 05：批量生成 10 张图（并发 + 自动 HTML 报告）

**积分消耗**：≈140（14 × 10）· **耗时**：≈2 min · **难度**：⭐⭐

需要做 9 宫格、分镜、产品图组等场景。

## 用户需求

「给我生成 10 张'未来城市夜景'的图，不同视角，最后导出 HTML 报告方便看」

## 命令链

```bash
export LIBTV_ACCESS_KEY=your_key_here

# ─── Step 1: 准备任务文件 ───
cat > /tmp/cyber_tasks.txt <<'EOF'
未来城市夜景，高空俯瞰，霓虹密布
未来城市夜景，街道平视，飞行汽车
未来城市夜景，巨型全息广告牌特写
未来城市夜景，地下管道仰望
未来城市夜景，机器人巡逻，雾气弥漫
未来城市夜景，雨后倒影，赛博朋克
未来城市夜景，废墟之中残存的霓虹
未来城市夜景，巨塔之巅，星空背景
未来城市夜景，市集人群，多人种共存
未来城市夜景，悬浮列车划过画面
EOF

# ─── Step 2: 批量提交（并发 5）───
python3 scripts/libtv.py batch \
  --file /tmp/cyber_tasks.txt \
  --workers 5 \
  --output /tmp/cyber_batch.json

# ─── Step 3: 逐个轮询完成 ───
for SID in $(python3 -c "
import json
data = json.load(open('/tmp/cyber_batch.json'))
for r in data:
    if r.get('sessionId'):
        print(r['sessionId'])
"); do
    echo "=== Polling $SID ==="
    python3 scripts/libtv.py poll "$SID" --interval 8 --timeout 300 --quiet &
done
wait

# ─── Step 4: 导出 HTML 报告 ───
mkdir -p ~/Downloads/cyber-batch
for SID in $(python3 -c "
import json
data = json.load(open('/tmp/cyber_batch.json'))
for r in data:
    if r.get('sessionId'):
        print(r['sessionId'])
"); do
    python3 scripts/libtv.py export "$SID" --format html --output ~/Downloads/cyber-batch/$SID.html
    python3 scripts/libtv.py download "$SID" --output-dir ~/Downloads/cyber-batch/$SID
done

# ─── Step 5: 浏览 ───
open ~/Downloads/cyber-batch/
```

## 关键参数

| 参数 | 作用 |
|---|---|
| `batch --workers 5` | 同时发 5 个，避免 IM 后端被冲 |
| `batch --output FILE.json` | 保存 sessionId 列表，便于后续轮询 |
| `export --format html` | 带预览的 HTML，看图最方便 |
| `export --format markdown` | 适合贴到 Notion / Lark |
| `export --urls-only` | 只要 URL 列表，给其他脚本用 |

## 进阶：每个任务用不同模型

如果想 10 个任务用不同模型，改用循环 + `model.py with`：

```bash
MODELS=(lib-nano-pro midjourney seedream-5.0 nano-banana lib-nano-pro \
        midjourney seedream-5.0 nano-banana lib-nano-pro midjourney)
TASKS=(...) # 10 个 prompt
for i in {0..9}; do
    python3 scripts/libtv.py model with "${MODELS[$i]}" "${TASKS[$i]}" --ratio 16:9 &
done
wait
```
