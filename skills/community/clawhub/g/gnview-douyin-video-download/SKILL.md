---
name: gnview-douyin-video-download
---
# 下载抖音视频
**Summary**: 使用curl直接下载抖音无水印视频（绕过防盗链），支持配置化保存路径与文件名

**Description**:
## 中文
### 用途:
- 直接下载抖音无水印视频，绕过官方防盗链限制
- 通过抖音视频的真实播放链接，使用curl命令下载到本地
- 解决直接访问抖音视频链接时的403 Forbidden错误

### 核心原理:
抖音视频的真实播放链接带有防盗链校验，需要携带`Referer`请求头伪装成从抖音官网跳转的请求，才能正常下载。

### 步骤:
1.  **获取视频真实链接**：通过抖音API或第三方工具获取视频的真实播放地址
2.  **构造下载命令**：根据配置的路径与文件名生成保存参数
3.  **执行下载**：发送带Referer头的curl请求完成下载

### 参数说明:
| 参数/选项 | 说明 | 示例 |
|--------|------|------|
| `-H "Referer: https://www.douyin.com/"` | 必需请求头，伪装来源为抖音官网，绕过防盗链 | - |
| `-o <文件名>` | 指定下载保存的本地文件名 | `-o ./download/7615937081646272185.mp4` |
| `<视频真实链接>` | 抖音官方视频播放地址 | 示例链接：`https://v26-web.douyinvod.com/xxxx/xxx.mp4` |

### 完整命令示例（基于配置）:
```bash
# 自动使用config.json中的配置参数
curl -H "Referer: https://www.douyin.com/" -o ./download/7615937081646272185.mp4 "https://v26-web.douyinvod.com/c49fd7899f16bd8a08b2710ae46f7c2a/69d96624/video/tos/cn/tos-cn-ve-15/o0pGDVXR7BKI3AF9fA8E1XQQI1Arg4fH4FdDEl/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=4444&bt=4444&cs=2&ds=10&ft=LjhJEL998xl8uEePQ0P5NdvaUFiXQd0dkVJEIdQKIbPD-Ipz&mime_type=video_mp4&qs=15&rc=ODQ1PDc6ODNoNzM3ZWg2PEBpamRpd3k5cnhxOjMzNGkzM0AxNDVeLTRiNmAxNWBhMTQuYSNmbGE1MmRzL19hLS1kLTBzcw%3D%3D&btag=c0000e00010000&cquery=100B_100x_100z_100o_101r&dy_q=1775844326&feature_id=e297886ea4c3239306bb1d52ed307653&l=20260411020526A383B1524D4A244C3450"
```

### 命令解释:
1.  `-H "Referer: https://www.douyin.com/"`：添加请求头，告诉抖音服务器请求来自抖音官网，绕过防盗链校验
2.  `-o ./download/7615937081646272185.mp4`：将下载的视频保存为指定路径下的文件
3.  最后一长串URL：抖音官方视频播放地址，包含视频的完整数据

### 注意事项:
1.  视频真实链接有时效性，过期后需要重新获取最新的播放地址
2.  无需携带其他额外请求头，Referer头已经足够绕过大部分防盗链限制
3.  下载目录需提前创建，避免命令执行失败
