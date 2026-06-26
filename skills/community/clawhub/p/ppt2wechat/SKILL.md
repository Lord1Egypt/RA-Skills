\---
name: ppt2wechat
description: mac系统某路径下某名字的PPT自动按页生成每一张截图和缩略图，然后发布到微信公众号上
\---

1、提示词输入：

例如，使用 ppt2png skill , MAC系统，桌面路径下10只小青蛙迎接春天.pptx，帮我生成图片和3行3列的缩略图，然后发布到微信公众号。我的微信公众号密钥：wechat_appid=XXX，wechat_appsecret=XXX

2、config.json配置说明：

路径赋值给config.json 下的 ppt_dir

名字赋值给ppt_file

需要用户说明自己的wechat_appid，wechat_appsecret

微信公众号如需更改作者也可以更改：wechat_author

3、skill实现说明：

基于PPT → PDF（使用 LibreOffice）
PDF → 每页 PNG（使用 Ghostscript）
每 9张图片生成 1 张缩略拼接图（3列 × 3行），可通过调整thumbnail_cols列，thumbnail_rows行来实现
兼容 Python 3.6

4、需要提前安装：
brew install ghostscript
pip3 install pillow



5、工作流程

主程序：ppt2wechat.py

配置文件：config.json

自动读取配置

支持修改 DPI、列数、行数、LibreOffice 路径、gs 路径



针对config.json
如果 which gs 输出是：
/opt/homebrew/bin/gs

就改成：

"ghostscript_path": "/opt/homebrew/bin/gs"