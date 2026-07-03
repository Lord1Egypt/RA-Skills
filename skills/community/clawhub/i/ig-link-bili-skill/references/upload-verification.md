# B 站上传验真（必须做，不要跳）

**核心原则**：**`upload_one.py` 返 `success: true` ≠ 真成功**。B 站上传接口是**异步处理**的：接口立刻返 success + bvid，但视频真正进 B 站索引可能要等 30 秒到 2 分钟。在此期间调 `api.bilibili.com/x/web-interface/view?bvid=X` 会拿到 `-404 啥都木有`。

`scripts/verify_upload.py` 是兜底——默认重试 3 次 × 每次等 30 秒。**不调它就告诉用户"上传成功"是错的**。

---

## 错误演示（2026-06-05 实测，Arvin 当场抓到）

```
upload_one.py 返: {"success": true, "bvid": "BV1hT7k6JEet", ...}
立刻 verify 返: {"code": -404, "message": "啥都木有"}
于是 agent 误判"被 B 站拒收"
→ 错误结论：把 8 个作者加入 BLOCKED_UPLOADERS
→ 实际情况：等 60 秒后再 verify 返 {"code": 0, "message": "OK"}
```

这就是今天误杀 8 个 IG 作者的根因。B 站静默 -404 是个**真陷阱**，但触发原因是"索引还没建好"，不是"内容被拒"。

---

## 验真 API 行为

```bash
# B 站 view API
GET https://api.bilibili.com/x/web-interface/view?bvid=<bvid>
```

返回码：

| code | 含义 | 行为 |
|---|---|---|
| `0` | 视频在索引中，可查 | 转载真成功 |
| `-404` "啥都木有" | 视频不存在（未进索引 / 真被拒） | 等待 or 排查 |
| `-400` "请求错误" | bvid 格式错 | 脚本不会遇到 |
| `-101` "未登录" | cookie 失效 | 刷 cookie |
| 其他 | 看 message 字段 | 排查 |

**重要**：B 站静默删除的话，code 也是 -404。所以 "PENDING 多分钟后变 FAIL" 不一定是被拒——也可能是**异步处理中遇到了别的错误**。需要回查 B 站创作者中心确认。

---

## 推荐调用流程

```bash
# 1. 上传
python3 upload_one.py <shortcode> <title> <desc> <uploader>
# → 拿到 bvid

# 2. 等 60 秒（不要立即 verify！）
sleep 60

# 3. 验真（默认 3 次 × 30s 间隔，共等 90s 后仍失败才算真失败）
python3 verify_upload.py <bvid>
# → "OK <title>" = 转载成功
# → "PENDING attempt 3/3" = 真失败，进入排查

# 4. 真失败的排查
# - B 站创作者中心：https://member.bilibili.com/v2#/upload-manager/article
#   看 "已发布" 列表里有没有这条 bvid
# - 有 = 站内外重复/版权被静默删了（已知原因：作者本人/官方号在 B 站已有内容）
# - 没有 = 罕见的真上传失败
```

---

## 一次性自动跑完上传+验真

如果想一次跑完（agent 自己用），写个 shell：

```bash
#!/bin/bash
shortcode="$1"
title="$2"
description="$3"
uploader="$4"

bvid=$(python3 /path/to/upload_one.py "$shortcode" "$title" "$description" "$uploader" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('bvid',''))")

if [ -z "$bvid" ]; then
  echo "FAIL: upload_one.py 没返 bvid"
  exit 1
fi

echo "uploaded as $bvid, 等 60s verify..."
sleep 60

python3 /path/to/verify_upload.py "$bvid"
```

---

## 写给新 skill 的 5 条铁律

1. **永远不要根据"立即 verify -404"判定上传失败**
2. **`verify_upload.py` 必须跑**（哪怕只是为了让 agent 心里有底）
3. **失败时回查 B 站创作者中心**，不要只看 API
4. **站内外重复拦截**是真存在的——但**不是因为 verify 失败**就能判定的，要等几分钟+查 B 站后台
5. **第一时间发现上传有问题**：在 B 站"已发布"列表里看不到 = 大概率被静默删
