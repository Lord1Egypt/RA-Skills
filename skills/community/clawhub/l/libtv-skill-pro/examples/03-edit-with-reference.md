# Example 03：基于参考图编辑（"把纸船换成爱心"）

**积分消耗**：≈14-20 · **耗时**：≈90s · **难度**：⭐⭐

用户拿一张图，要求局部编辑——这是 LibTV 的典型场景。

## 用户需求

「这张图（本地路径 `~/Desktop/origin.png`）里，把所有纸船换成白色纸爱心，保持其他不变」

## 命令链

```bash
export LIBTV_ACCESS_KEY=your_key_here

# 1. 先把本地图片上传到 LibTV OSS
UPLOAD=$(python3 scripts/libtv.py upload ~/Desktop/origin.png)
echo "$UPLOAD"
OSS_URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['url'])")

# 2. 用 edit.py mark（局部标记修改）+ OSS URL
RESULT=$(python3 scripts/libtv.py edit mark \
  "把画面里所有纸船的区域换成白色纸爱心，其他保持不变" \
  --target "$OSS_URL")
SID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['sessionId'])")

# 3. 轮询
python3 scripts/libtv.py poll "$SID" --interval 8 --timeout 300

# 4. 下载
python3 scripts/libtv.py download "$SID" --output-dir ~/Desktop/edited
```

## 替代方案：用 node.py image_to_image

如果是整张图的风格/内容大改（不只是局部），用 image_to_image：

```bash
python3 scripts/libtv.py node image_to_image \
  "把画面整体改成赛博朋克风" \
  --ref "$OSS_URL"
```

## 修饰器选择

| 用户描述 | 推荐 modifier |
|---|---|
| "把 X 换成 Y" / "去掉 X" / "加上 X" | `mark` |
| "改成 X 风格" / "做成卡通" / "宫崎骏感觉" | `style` |
| "强调右上角" / "聚焦在人物" | `focus` |
| "用环绕镜头" / "推镜头" / "希区柯克变焦" | `camera` |
| "用孙悟空作为角色" | `character_lib` |
