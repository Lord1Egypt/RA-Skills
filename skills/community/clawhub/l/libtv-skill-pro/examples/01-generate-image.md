# Example 01：生一张猫图（最小路径）

**积分消耗**：≈14 · **耗时**：≈60s · **难度**：⭐

最简单的端到端：从输入到本地图片 4 个命令搞定。

## 用户需求

「生一张白色短毛猫坐在窗台上的图，1:1 比例，2K 分辨率，用 lib-nano-pro 模型」

## 命令链

```bash
export LIBTV_ACCESS_KEY=your_key_here

# 1. 预览将发送的 prompt（不烧积分）
python3 scripts/libtv.py model with lib-nano-pro \
  "白色短毛猫坐在窗台上" \
  --ratio 1:1 --resolution 2K --count "1张" \
  --dry-run

# 2. 真实生成
RESULT=$(python3 scripts/libtv.py model with lib-nano-pro \
  "白色短毛猫坐在窗台上" \
  --ratio 1:1 --resolution 2K --count "1张")
echo "$RESULT"
SID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['sessionId'])")

# 3. 轮询等待完成（默认 8s 间隔，10 分钟超时）
python3 scripts/libtv.py poll "$SID"

# 4. 下载到本地
python3 scripts/libtv.py download "$SID" --output-dir ~/Downloads/cat --prefix cat
```

## 预期输出

- 一张 2K PNG/JPG 保存在 `~/Downloads/cat/cat_01.png`
- 一个 `projectUrl`，浏览器打开可以看 LibTV 项目画布

## 常见故障

| 现象 | 错误 kind | 解决 |
|---|---|---|
| 第 2 步 401 | `INVALID_ACCESS_KEY` | 检查 `LIBTV_ACCESS_KEY` 是否正确 |
| 第 2 步 403 | `FORBIDDEN_OR_INSUFFICIENT_CREDITS` | 积分不足，去 LibTV 充值 |
| 第 3 步超时 | — | 后端慢，去 `projectUrl` 画布上手动看结果 |
| 第 4 步空 | — | 会话里还没有结果 URL，再等一会儿重跑 |
