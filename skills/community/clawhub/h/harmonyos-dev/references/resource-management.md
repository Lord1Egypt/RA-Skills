# 资源分类与访问

> 来源：华为开发者文档 - 资源分类与访问（2026-04-20）
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/resource-categories-and-access

## 资源目录结构

```
resources/                          # 应用资源根目录（必须存在）
├── base/                          # 默认资源目录（必须存在）
│   ├── element/                   # 元素资源（string/color/float/boolean/integer等）
│   │   ├── string.json           # 字符串资源
│   │   ├── color.json           # 颜色资源
│   │   ├── float.json           # 浮点资源（用于字体大小、间距等）
│   │   ├── boolean.json         # 布尔资源
│   │   ├── integer.json         # 整型资源
│   │   ├── intarray.json        # 整型数组
│   │   ├── strarray.json        # 字符串数组
│   │   └── plural.json          # 复数资源
│   ├── media/                    # 媒体资源（图片、音视频）
│   │   ├── icon.png
│   │   └── background.jpg
│   └── profile/                   # 自定义配置文件
│       └── test_profile.json
├── zh_CN/                         # 限定词目录：简体中文
├── zh_Hant_TW/                    # 限定词目录：繁体中文（台湾）
├── zh_Hant_HK/                    # 限定词目录：繁体中文（香港）
├── en_US/                         # 限定词目录：英语（美国）
├── en_GB/                         # 限定词目录：英语（英国）
├── dark/                          # 限定词目录：深色模式
├── vertical/                      # 限定词目录：竖屏
├── horizontal/                    # 限定词目录：横屏
├── mdpi/                          # 限定词目录：中密度屏幕
├── hdpi/                          # 限定词目录：高密度屏幕
├── xhdpi/                         # 限定词目录：超高密度屏幕
├── xxhdpi/                        # 限定词目录：超超高密度屏幕
├── xxxhdpi/                       # 限定词目录：超超超高密度屏幕
├── phone/                         # 限定词目录：手机设备
├── tablet/                        # 限定词目录：平板设备
├── car/                           # 限定词目录：车机设备
├── tv/                            # 限定词目录：电视设备
├── wearable/                     # 限定词目录：穿戴设备
├── rawfile/                       # 原始文件目录（不编译，无资源ID）
│   └── large_files/
│       └── data.json
└── resfile/                       # 资源文件目录（安装后解压到沙箱）
    └── configs/
        └── config.json
```

**说明**：`base` 目录是默认目录，每个 Module 都有且必须有。Stage 模型下共有资源放到 `AppScope` 下的 `resources`。

## 资源文件格式

### color.json（颜色资源）

```json
{
  "color": [
    { "name": "color_hello", "value": "#FFFF0000" },
    { "name": "color_white", "value": "#FFFFFFFF" },
    { "name": "color_black", "value": "#FF000000" },
    { "name": "color_transparent", "value": "#00000000" },
    { "name": "color_emphasize", "value": "#FF007DFF" },
    { "name": "color_warning", "value": "#FFFFB400" },
    { "name": "color_error", "value": "#FFFF3B30" },
    { "name": "color_success", "value": "#FF34C759" }
  ]
}
```

### string.json（字符串资源）

```json
{
  "string": [
    { "name": "hello", "value": "Hello" },
    { "name": "app_name", "value": "MyHarmonyApp" },
    { "name": "message", "value": "Hello, %1$s! You have %2$d messages." }
  ]
}
```

### float.json（浮点资源，用于字体大小/间距等）

```json
{
  "float": [
    { "name": "font_size_title", "value": "28.0fp" },
    { "name": "font_size_body", "value": "16.0fp" },
    { "name": "spacing_standard", "value": "8.0vp" },
    { "name": "padding_large", "value": "16.0vp" },
    { "name": "opacity_medium", "value": "0.6" }
  ]
}
```

### plural.json（复数资源）

```json
{
  "plural": [
    {
      "name": "eat_apple",
      "value": [
        { "quantity": "one", "value": "%d apple" },
        { "quantity": "other", "value": "%d apples" }
      ]
    },
    {
      "name": "unread_count",
      "value": [
        { "quantity": "zero", "value": "No unread messages" },
        { "quantity": "one", "value": "%d unread message" },
        { "quantity": "other", "value": "%d unread messages" }
      ]
    }
  ]
}
```

## 资源访问方式

### `$r('app.type.name')` — 应用资源（编译后有资源ID）

```typescript
// 字符串
Text($r('app.string.hello'))
Text($r('app.string.message', 'Alice', 5))  // 带占位符

// 颜色
Text('Hello')
  .fontColor($r('app.color.color_emphasize'))
  .backgroundColor($r('app.color.color_white'))

// 字体大小
Text('Title')
  .fontSize($r('app.float.font_size_title'))

// 图片
Image($r('app.media.icon'))
Image($r('app.media.background'))

// 布尔值
if ($r('app.boolean.show_debug').value) { }

// 整数
console.info(`Max: ${$r('app.integer.max_count').value}`);
```

### `$rawfile('path/file.png')` — rawfile 原始文件（不编译，无资源ID）

```typescript
// rawfile 中的文件
Image($rawfile('images/icon.png'))
Text($rawfile('data/config.json'))

// 支持多层子目录
Image($rawfile('icons/dark/arrow.png'))
Video($rawfile('videos/intro.mp4'))

// 在 Web 组件中引用本地资源
Web({ src: $rawfile('html/index.html'), ... })
```

### `$sys(type, name)` — 系统资源

```typescript
// 系统颜色
Text('Hello')
  .fontColor($r('sys.color.ohos_id_color_emphasize'))
  .backgroundColor($r('sys.color.ohos_id_color_background'))

// 系统字体
Text('标题')
  .fontSize($r('sys.float.ohos_id_text_size_headline1'))
  .fontWeight(FontWeight.Bolder)

// 系统图标（SymbolGlyph 配合使用）
SymbolGlyph($r('sys.symbol.ohos_checkbox_checked'))

// 系统图片
Image($r('sys.media.ohos_app_icon'))
Image($r('sys.media.ohos_group_icon'))
```

### 跨 Module 资源访问（HSP/HAR）

```typescript
// 使用 [模块名].type.name 访问 HSP 资源
Text($r('[library].string.test_string'))
Image($r('[library].media.library_icon'))

// rawfile 跨模块
Image($rawfile('[library]/icon.png'))
```

## 限定词目录

### 命名规则

格式：`语言_文字_国家或地区-横竖屏-设备类型-颜色模式-屏幕密度`

示例：
- `zh_CN` — 简体中文，中国
- `zh_Hant_TW` — 繁体中文，台湾
- `en_US` — 英语，美国
- `dark` — 深色模式
- `zh_CN-dark` — 简体中文 + 深色模式
- `zh_CN-phone-vertical` — 简体中文手机竖屏
- `mcc460_mnc00-zh_Hans_CN` — 中国移动网络

### 限定词取值

| 限定词 | 取值示例 |
|--------|---------|
| 语言 | zh, en, ja, ko, fr, de |
| 文字 | Hans（简体）, Hant（繁体）|
| 国家/地区 | CN, US, GB, TW, HK, JP |
| 横竖屏 | vertical, horizontal |
| 设备类型 | phone, tablet, car, tv, wearable, 2in1 |
| 颜色模式 | dark, light |
| 屏幕密度 | ldpi, mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi |

## overlay 机制（动态替换资源）

```typescript
import resourceManager from '@ohos.resourceManager';

// 添加 overlay（临时替换资源，AppScope 下生效）
resourceManager.addResource('/data/overlay/resources/')
  .then(() => console.info('overlay 添加成功'))
  .catch((err) => console.error(`overlay 添加失败: ${err}`));

// 移除 overlay
resourceManager.removeResource('/data/overlay/resources/');

// overlay 目录结构示例
// /data/overlay/resources/
//   ├── base/
//   │   ├── element/
//   │   │   └── string.json   // 覆盖原有字符串
//   └── media/
//       └── icon.png          // 覆盖原有图标
```

## AppStorage / PersistentStorage（状态存储）

```typescript
// AppStorage（应用全局响应式存储）
AppStorage.setOrCreate('theme', 'dark');
let theme = AppStorage.get<string>('theme');  // 'dark'

// 与 @StorageLink 双向绑定
@StorageLink('theme') theme: string = 'light';

// PersistentStorage（持久化存储）
PersistentStorage.persistProp('theme', 'light');
let theme = AppStorage.get<string>('theme');

// 本地存储
import dataPreferences from '@ohos.data.preferences';

let context = getContext(this);
let options = dataPreferences.Options({ name: 'my_store' });
dataPreferences.getPreferences(context, options, (err, preferences) => {
  preferences.set('username', 'Alice', (err) => {
    preferences.get('username', '', (err, value) => {
      console.info(`username: ${value}`);
    });
  });
});
```
