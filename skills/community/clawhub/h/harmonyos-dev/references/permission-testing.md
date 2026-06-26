# 权限配置与测试发布

> 来源：华为开发者文档
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/app-permission-mgmt
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/permission-list

---

## 权限配置

### 声明权限（module.json5 或 app.json5）

```json
{
  "app": {
    "permissions": [
      "ohos.permission.INTERNET",
      "ohos.permission.CAMERA",
      "ohos.permission.RECORD_AUDIO",
      "ohos.permission.ACCESS_LOCATION",
      "ohos.permission.READ_CONTACTS",
      "ohos.permission.WRITE_CONTACTS"
    ]
  }
}
```

### 动态请求权限（运行时）

```typescript
import abilityAccessCtrl from '@ohos.abilityAccessCtrl';
import bundleManager from '@ohos.bundle.installer';

// 获取 atManager
let atManager = abilityAccessCtrl.createAtManager();

// requestPermissionsFromUser 会弹窗请求权限
atManager.requestPermissionsFromUser(
  globalThis.context,
  ['ohos.permission.CAMERA', 'ohos.permission.RECORD_AUDIO'],
  (result) => {
    if (result.authResults[0] === 0) {
      console.info('相机权限授予成功');
    } else if (result.authResults[0] === 2) {
      console.info('用户拒绝授予权限');
    }
  }
);

// 检查权限状态
let authResult = atManager.checkAccessToken(
  bundleManager.getBundleInfoForSelfSync(0).appInfo.accessTokenId,
  'ohos.permission.CAMERA'
);

if (authResult === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
  console.info('已有相机权限');
}
```

### 常用权限列表

| 权限名 | 说明 | 是否敏感 |
|--------|------|---------|
| `ohos.permission.INTERNET` | 联网 | 否 |
| `ohos.permission.CAMERA` | 相机 | 是 |
| `ohos.permission.RECORD_AUDIO` | 麦克风 | 是 |
| `ohos.permission.ACCESS_LOCATION` | 位置 | 是 |
| `ohos.permission.READ_CONTACTS` | 读联系人 | 是 |
| `ohos.permission.WRITE_CONTACTS` | 写联系人 | 是 |
| `ohos.permission.READ_MEDIA_IMAGES` | 读图片 | 是 |
| `ohos.permission.READ_MEDIA_VIDEO` | 读视频 | 是 |
| `ohos.permission.MANAGE_EXTERNAL_STORAGE` | 存储管理 | 是 |
| `ohos.permission.SYSTEM_FLOAT_WINDOW` | 悬浮窗 | 是 |
| `ohos.permission.LOCATION_IN_BACKGROUND` | 后台定位 | 是 |

---

## 应用测试

### 单元测试

```typescript
// 测试文件: test/Example.test.ets
import hilog from '@ohos.hilog';
import describe from '@ohos.describe';

describe('Calculator', () => {
  it('should_add_two_numbers', 0, () => {
    let result = 1 + 2;
    expect(result).assertEqual(3);
  });

  it('should_handle_negative_numbers', 0, () => {
    let result = 5 - 10;
    expect(result).assertEqual(-5);
  });

  it('should_multiply', 0, () => {
    let result = 3 * 4;
    expect(result).assertEqual(12);
  });
});
```

### UI 测试

```typescript
import assert from '@ohos.assert';

@Entry
@Component
struct Index {
  @State message: string = 'Hello World';

  build() {
    Column() {
      Text(this.message)
        .id('hello_text')
      Button('Click me')
        .id('click_button')
        .onClick(() => {
          this.message = 'Button Clicked';
        })
    }
  }
}

// 测试代码
import driver from '@ohos.at/dist/element/driver';

async function testUI() {
  // 启动测试应用
  let driver = Driver.create();
  
  // 等待按钮出现
  await driver.delayMs(1000);
  
  // 点击按钮
  let button = await driver.findComponent({ id: 'click_button' });
  await button.click();
  
  // 验证文本变化
  let text = await driver.findComponent({ id: 'hello_text' });
  let content = await text.getText();
  expect(content).assertEqual('Button Clicked');
}
```

### 性能测试

```typescript
import hiPerf from '@ohos.perf';

// 在代码段前后埋点
hiPerf.beginPage('page_render_start');

Column() { ... }.build()

hiPerf.endPage('page_render_end');

// 性能打点上报
import hiPerf from '@ohos.hiPerf';
hiPerf.reportDfxData();
```

---

## 应用签名与发布

### Debug 签名

DevEco Studio 自动使用 Debug 签名（自动签名）。签名信息在 `build-profile.json5` 中：

```json
{
  "signingConfigs": {
    "debug": {
      "certpath": "$USER_HOME/.ohos/debug_cert.pem",
      "storePassword": "",
      "keyAlias": "",
      "keyPassword": "",
      "profile": "",
      "signAlg": "SHA256withRSA",
      "fileCertpath": "",
      "fileSignAlg": ""
    }
  },
  "products": {
    "debug": {
      "signingConfig": "debug"
    },
    "release": {
      "signingConfig": "release"
    }
  }
}
```

### Release 签名流程

1. 在 AppGallery Connect 创建应用，获取 **Profile** 文件（.p7b）
2. 申请 **Certificate**（.cer）+ **Private Key**（.p12）
3. 在 DevEco Studio 配置签名：

```json
{
  "signingConfigs": {
    "release": {
      "certpath": "/path/to/certificate.cer",
      "keyAlias": "my_key_alias",
      "keyPassword": "key_password",
      "profile": "/path/to/profile.p7b",
      "signAlg": "SHA256withRSA",
      "storeFile": "/path/to/key.p12",
      "storePassword": "keystore_password"
    }
  }
}
```

### 发布到应用市场

1. **构建 Release HAP**：在 DevEco Studio 选择 `Build` → `Build Release`
2. **上传到 AppGallery Connect**：开发者联盟后台 → 应用管理 → 上传 HAP
3. **填写应用信息**：名称、描述、截图、隐私政策
4. **提交审核**：审核周期约 1-3 个工作日

---

## hvigor 构建工具

> hvigor 是 HarmonyOS 的构建工具，类似 Gradle

### 项目级 build-profile.json5

```json
{
  "app": {
    "compileSdkVersion": 12,
    "compatibleSdkVersion": 12,
    "products": [
      {
        "name": "default",
        "signingConfig": "debug"
      },
      {
        "name": "release",
        "signingConfig": "release"
      }
    ]
  }
}
```

### 模块级 build-profile.json5

```json
{
  "modules": [
    {
      "name": "entry",
      "srcPath": "./modules/entry",
      "targets": [
        {
          "name": "default",
          "applyToProducts": ["default"]
        }
      ]
    }
  ]
}
```

### 常用 hvigor 命令

```bash
# 构建 debug 版本
hvigor --mode module -p product=default assembleDefault

# 构建 release 版本
hvigor --mode module -p product=default assembleRelease

# 清理构建产物
hvigor clean

# 查看帮助
hvigor --help
```
