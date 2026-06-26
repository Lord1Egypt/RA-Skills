# ShareSDK 集成说明

> 本文档由 Android ShareSDK 集成 Skill 自动生成
> 生成日期：{date}

---

## 项目信息

| 项目 | 内容 |
|------|------|
| 集成日期 | {date} |
| 启用平台 | {platforms_list} |
| 项目路径 | {project_path} |

---

## 配置位置

### SDK 配置

- **文件**：`app/build.gradle`
- **位置**：文件末尾的 `MobSDK { ... }` 配置块
- **可修改项**：
  - `appKey` / `appSecret`：MobTech 应用密钥
  - `devInfo` 块内各平台配置（微信、QQ、微博等）

### 隐私授权

- **文件**：{privacy_file}
- **方法**：{privacy_method}
- **代码**：

```java
// 用户点击隐私政策同意按钮后调用
MobSDK.submitPolicyGrantResult(true);
```

### 分享功能

- **文件**：{share_file}
- **方法**：{share_method}
- **支持平台**：{share_platforms}

---

## 快速修改指南

### 添加新分享平台

1. 在 `app/build.gradle` 的 `devInfo` 块中添加平台配置：

```groovy
MobSDK {
    appKey "your_app_key"
    appSecret "your_app_secret"

    ShareSDK {
        devInfo {
            // 添加新平台，例如抖音
            // Douyin {
            //     appId "your_app_id"
            //     appSecret "your_app_secret"
            // }
        }
    }
}
```

2. 前往对应开放平台申请应用，获取 appId/appSecret
3. 参考官方文档：https://www.mob.com/wiki/detailed?wiki=30&id=14

### 修改分享内容

编辑 `{share_file}` 中的分享参数：

```java
OnekeyShare oks = new OnekeyShare();
oks.setTitle("修改这里：分享标题");
oks.setText("修改这里：分享文本内容");
oks.setUrl("修改这里：分享链接");
oks.setImageUrl("修改这里：分享图片URL");
oks.show(context);
```

### 修改分享平台

在分享代码中指定平台：

```java
// 分享到指定平台（微信）
Platform wechat = ShareSDK.getPlatform("Wechat");

// 分享到指定平台（QQ）
Platform qq = ShareSDK.getPlatform("QQ");

// 分享到指定平台（微博）
Platform weibo = ShareSDK.getPlatform("SinaWeibo");
```

---

## 平台申请地址

| 平台 | 开放平台地址 |
|------|-------------|
| 微信/微信朋友圈/微信收藏 | https://open.weixin.qq.com |
| QQ / QZone | https://connect.qq.com |
| 新浪微博 | https://open.weibo.com |
| Facebook | https://developers.facebook.com |
| Twitter / X | https://developer.twitter.com |
| Instagram | https://developers.instagram.com |
| LinkedIn | https://www.linkedin.com/developers/apps |
| Line | https://developers.line.biz/console/ |
| KakaoTalk / KakaoStory | https://developers.kakao.com/console/app |
| 支付宝 | https://open.alipay.com/platform/home.htm |

---

## 官方资源

- **文档中心**：https://www.mob.com/wiki/list
- **SDK 下载**：https://www.mob.com/download
- **合规指南**：https://www.mob.com/wiki/detailed?wiki=421&id=717
- **技术支持**：https://www.mob.com/about/contact

---

## 常见问题

### 微信分享失败

- 检查签名 MD5 是否与微信开放平台配置一致
- 检查包名是否与微信开放平台配置一致
- 检查 appId/appSecret 是否正确

### QQ 分享失败

- 检查是否在 QQ 互联配置了正确的包名和签名
- 检查 appId/appKey 是否正确

### 微博分享失败

- 检查回调地址是否与微博开放平台配置一致
- 检查 appKey/appSecret 是否正确

---

## 注意事项

1. **隐私合规**：确保 App 有《隐私政策》，首次启动展示并获取用户同意后才调用 `MobSDK.submitPolicyGrantResult(true)`
2. **签名一致**：微信、QQ 等平台需要配置应用签名，确保打包签名与平台配置一致
3. **混淆配置**：如需代码混淆，参考官方文档添加 ShareSDK 的混淆规则
