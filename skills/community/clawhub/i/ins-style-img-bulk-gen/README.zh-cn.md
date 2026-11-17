# ins-style-img-bulk-gen SKILL

![](./references/demo.jpg)

批量生成 Instagram 风格(INS 风 / 小红书 / 生活方式)的图片——从 80+ 元素的 INS 风素材库中随机搭配提示词,并发调用图像生成能力出图.

还可以生成 2x2 等 4 宫格拼图，并支持两种加字模式：

| 模式 | 效果 | 适用 |
|---|---|---|
| `ins`（默认） | 半透明灰色蒙版 + 标题 + 正文 | 内页 / 内容图 |
| `cover` | 无蒙版，居中大字标题（约 2 倍）+ 黑白描边 + 阴影，**只要标题** | 社媒封面（小红书 / 公众号 / 视频号） |

```bash
# ins：灰蒙版 + 标题 + 正文
python scripts/add_ins_overlay.py -i in.jpg -o out.jpg -t "❤ 富婆的 12 个隐秘爱好" -b "1、…"

# cover：无蒙版、大字描边标题、不含正文
python scripts/add_ins_overlay.py -i in.jpg -o out.jpg -m cover -t "40+后才明白\n女人越来越差的9个原因"
```

> ⚠️ cover 模式请**自己用 `\n` 指定断行** —— 脚本不做语义断句，只会按显示宽度均衡切分。

![](./references/cover.jpg)

[← English](README.md)