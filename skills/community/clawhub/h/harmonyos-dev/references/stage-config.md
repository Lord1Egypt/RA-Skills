# Stage 模型配置详解

> 来源：华为开发者文档 - 应用配置文件（Stage模型）
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-configuration-file-stage

## module.json5（Module 级配置）

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "srcEntry": "./ets/entryability/EntryAbility.ts",
    "description": "$string:module_desc",
    "process": "string",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet", "2in1"],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ts",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:icon",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:icon",
        "startWindowBackground": "$color:start_window_background",
        "excluded": false,
        "continiable": false
      }
    ],
    "extensionAbilities": [],
    "shortcuts": [
      {
        "shortcutId": "id",
        "label": "$string:shortcut_label",
        "icon": "$media:icon"
      }
    ],
    "permissions": [
      "ohos.permission.INTERNET"
    ],
    "metadata": [
      {
        "name": "client_id",
        "value": "string"
      }
    ],
    "dependencies": [],
    "distro": {
      "modulePublicDir": ".",
      "moduleType": "moduleType"
    }
  }
}
```

## app.json5（应用级配置）

```json
{
  "app": {
    "bundleName": "com.example.myapp",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:app_icon",
    "label": "$string:app_label",
    "description": "$string:app_desc",
    "size": "0",
    "targetApiVersion": 12,
    "backup": true,
    "appABIVersion": "nativeAbi",
    "compileSdkVersion": 12,
    "minCompileSdkVersion": 12,
    "permissions": [
      "ohos.permission.INTERNET"
    ]
  }
}
```

## 关键字段说明

| 字段 | 说明 |
|------|------|
| `module.name` | Module 名称 |
| `module.type` | `entry`（主包）或 `feature`（特性）|
| `module.srcEntry` | Ability 源码路径 |
| `module.mainElement` | 主 Ability 名称 |
| `module.deviceTypes` | 支持的设备：`phone`, `tablet`, `2in1`, `tv`, `car`, `wearable` 等 |
| `module.deliveryWithInstall` | 是否随应用安装 |
| `module.installationFree` | 是否免安装 |
| `module.pages` | 页面配置文件路径 |
| `abilities[].name` | Ability 名称（必须唯一）|
| `abilities[].icon` | Ability 图标（资源路径）|
| `abilities[].label` | Ability 显示名称 |
| `abilities[].startWindowIcon` | 启动窗口图标 |
| `abilities[].startWindowBackground` | 启动窗口背景色 |
| `abilities[].continiable` | 是否支持跨设备迁移 |
| `app.targetApiVersion` | 目标 API 版本 |

## 权限配置

### 声明权限（module.json5 或 app.json5）

```json
{
  "module": {
    "permissions": [
      "ohos.permission.INTERNET",
      "ohos.permission.GET_NETWORK_INFO",
      "ohos.permission.CAMERA",
      "ohos.permission.RECORD_AUDIO",
      "ohos.permission.WRITE_CONTACTS",
      "ohos.permission.READ_CONTACTS",
      "ohos.permission.ACCESS_LOCATION",
      "ohos.permission.LOCATION_IN_BACKGROUND"
    ]
  }
}
```

### 常用权限列表

| 权限名 | 说明 |
|--------|------|
| `ohos.permission.INTERNET` | 允许应用联网 |
| `ohos.permission.GET_NETWORK_INFO` | 获取网络信息 |
| `ohos.permission.CAMERA` | 使用相机 |
| `ohos.permission.RECORD_AUDIO` | 录音 |
| `ohos.permission.WRITE_CONTACTS` | 写入联系人 |
| `ohos.permission.READ_CONTACTS` | 读取联系人 |
| `ohos.permission.ACCESS_LOCATION` | 获取位置 |
| `ohos.permission.LOCATION_IN_BACKGROUND` | 后台定位 |
| `ohos.permission.READ_MEDIA_IMAGES` | 读取图片 |
| `ohos.permission.WRITE_MEDIA_IMAGES` | 写入图片 |
| `ohos.permission.READ_MEDIA_VIDEO` | 读取视频 |
| `ohos.permission.MANAGE_EXTERNAL_STORAGE` | 管理外部存储 |

### 动态请求权限（运行时）

```typescript
import abilityAccessCtrl from '@ohos.abilityAccessCtrl';
import bundleManager from '@ohos.bundle.installer';

// 获取 atManager
let atManager = abilityAccessCtrl.createAtMANAGER();

// 检查权限
let res = atManager.checkEmptyHapCallingPermissions(
  ' bundleManager.getBundleInfoForSelfSync(0).uid'
);

// 请求权限
atManager.requestPermissionsFromUser(
  globalThis.context,
  ['ohos.permission.CAMERA'],
  (result) => {
    if (result.authResults[0] === 0) {
      console.info('权限授予成功');
    } else {
      console.info('权限被拒绝');
    }
  }
);
```

## 页面路由配置（main_pages.json）

```json
{
  "src": [
    {
      "name": "Index",
      "pageSourceFile": "./ets/pages/Index/Index.ets",
      "components": []
    },
    {
      "name": "Detail",
      "pageSourceFile": "./ets/pages/Detail/Detail.ets",
      "components": []
    }
  ]
}
```

## 组件扫描注册

```typescript
// 在 Ability 内扫描并注册组件
import componentSnapshot from '@ohos.app.ability.componentSnapshot';

// 注册组件
componentSnapshot.registerxxxCallback(callback);
```

## Want 机制（组件间跳转）

```typescript
import Want from '@ohos.app.ability.Want';

// 启动指定 Ability
let want: Want = {
  deviceId: '',           // 空字符串表示本设备
  bundleName: 'com.example.app',
  abilityName: 'EntryAbility',
  parameters: { key: 'value' }  // 传递给目标 Ability 的数据
};

// 启动
context.startAbility(want)
  .then(() => console.info('启动成功'))
  .catch((err) => console.error(`启动失败: ${err}`));

// 停止
context.stopAbility(want)
  .then(() => console.info('停止成功'))
  .catch((err) => console.error(`停止失败: ${err}`));
```

## 跨设备启动

```typescript
import wantAgent from '@ohos.want.agent';

// 跨设备启动
let want: Want = {
  deviceId: 'deviceId_of_target',
  bundleName: 'com.example.app',
  abilityName: 'EntryAbility'
};

context.startAbility(want)
  .then(() => console.info('跨设备启动成功'))
  .catch((err) => console.error(`跨设备启动失败: ${err}`));
```

---

## 窗口管理（Stage 模型）

> 来源：华为开发者文档 - 管理应用窗口（Stage模型）
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-window-stage

### 核心接口

| 接口 | 说明 |
|------|------|
| `windowStage.getMainWindow()` | 获取主窗口 |
| `windowStage.loadContent(path)` | 加载页面内容 |
| `windowStage.createSubWindow(name)` | 创建子窗口 |
| `window.createWindow(config)` | 创建子窗口或系统窗口 |
| `window.setUIContent(path)` | 为窗口加载页面 |
| `window.setWindowBrightness(v)` | 设置屏幕亮度 |
| `window.setWindowTouchable(v)` | 设置窗口是否可触 |
| `window.moveWindowTo(x, y)` | 移动窗口位置 |
| `window.setWindowLayoutFullScreen(v)` | 设置沉浸式布局 |

### 获取主窗口并设置内容

```typescript
// UIAbility 中
import window from '@ohos.window';

class MyAbility extends UIAbility {
  onWindowStageCreate(windowStage) {
    // 获取主窗口
    let mainWindow = windowStage.getMainWindow();

    // 设置窗口属性
    mainWindow.setWindowBrightness(0.8);  // 屏幕亮度 0~1
    mainWindow.setWindowTouchable(true);

    // 加载页面内容（路径需在 main_pages.json 中注册）
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error(`加载失败: ${JSON.stringify(err)}`);
        return;
      }
      console.info('页面加载成功');
    });
  }

  onWindowStageDestroy() {
    // 窗口销毁时调用
  }
}
```

### 设置沉浸式布局（隐藏状态栏/导航栏）

```typescript
// 获取主窗口
let mainWindow = windowStage.getMainWindow();

// 开启沉浸式（隐藏状态栏和导航栏）
await mainWindow.setLayoutFullScreen(true);

// 设置系统栏（状态栏/导航栏）的显示策略
await mainWindow.setSystemBarEnable(['status', 'navigation']);

// 设置状态栏文字颜色（light-content 或 dark-content）
await mainWindow.setSystemBarProperties({
  statusBarContentColor: '#FFFFFFFF',
  navigationBarContentColor: '#FF000000'
});

// 完全沉浸（同时隐藏）
await mainWindow.setSystemBarEnable([]);

// 恢复系统栏
await mainWindow.setSystemBarEnable(['status', 'navigation']);
```

### 创建子窗口

```typescript
// 在 UIAbility 中
async createSubWindow() {
  // 创建子窗口
  let subWindow = await windowStage.createSubWindow('my_sub_window');

  // 设置子窗口大小和位置
  await subWindow.moveWindowTo(100, 100);
  await subWindow.resize(300, 500);

  // 设置子窗口背景色
  subWindow.setWindowBackgroundColor('#FFFFFF');

  // 加载子窗口页面内容
  await subWindow.setUIContent('pages/SubPage');

  // 显示窗口
  await subWindow.showWindow();

  // 关闭子窗口
  // await subWindow.destroyWindow();
}
```

### 监听窗口生命周期

```typescript
// 监听 WindowStage 生命周期事件
windowStage.on('windowStageEvent', (stageEvent) => {
  switch (stageEvent) {
    case 1:  // ACTIVE
      console.info('WindowStage 进入前台');
      break;
    case 2:  // INACTIVE
      console.info('WindowStage 进入后台');
      break;
    case 3:  // DESTROYED
      console.info('WindowStage 已销毁');
      break;
  }
});

// 监听窗口不可交互事件
mainWindow.on('touchOutSide', () => {
  console.info('点击了窗口外部');
});

// 监听窗口不可交互状态
mainWindow.setWindowTouchable(false);
```

### 全局悬浮窗

```typescript
import window from '@ohos.window';

// 创建全局悬浮窗（需要申请 ohos.permission.SYSTEM_FLOAT_WINDOW 权限）
async function createGlobalFloatWindow(context) {
  let config = {
    name: 'global_float',
    windowType: window.Type.FLOAT_CLOUD,  // 全局悬浮窗类型
    ctx: context,
  };

  let floatWindow = await window.createWindow(config);

  // 设置悬浮窗位置和大小
  await floatWindow.moveWindowTo(200, 300);
  await floatWindow.resize(200, 200);

  // 设置为应用退出后仍可显示
  await floatWindow.setPrivacyMode(true);

  // 加载悬浮窗内容
  await floatWindow.setUIContent('pages/FloatWindow');

  await floatWindow.showWindow();
}
```

### WindowStage 生命周期

```typescript
class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage) {
    // Stage 创建：加载应用主页面
    console.info('EntryAbility onWindowStageCreate');
    windowStage.loadContent('pages/Index');
  }

  onWindowStageDestroy() {
    // Stage 销毁：清理资源
    console.info('EntryAbility onWindowStageDestroy');
  }

  onWindowStageActive() {
    // WindowStage 进入前台
    console.info('WindowStage active');
  }

  onWindowStageInactive() {
    // WindowStage 进入后台
    console.info('WindowStage inactive');
  }
}
```
